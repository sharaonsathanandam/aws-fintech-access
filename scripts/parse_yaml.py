import yaml, json, sys, os, subprocess, glob

yaml_dir = ["access-requests/finance", "access-requests/treasury-ops"]
script_dir = os.path.dirname(os.path.abspath(__file__))

account_id = subprocess.check_output([
    "aws","sts","get-caller-identity",
    "--query","Account","--output","text"
]).decode().strip()
base_arn = f"arn:aws:iam::{account_id}:role/AWSReservedSSO_FinanceAnalysts_b67570c300321d27"



requests_map = []
for d in yaml_dir:
    pattern = os.path.join(f"{d}/*.yaml")
    for path in sorted(glob.glob(pattern)):
        key = os.path.splitext(os.path.basename(path))[0]
        data = yaml.safe_load(open(path)) or {}
        data["principal_arn"] = base_arn
        requests_map.append(data)

out_path = "pipeline-config/requests.json"
with open(out_path, "w") as fp:
    json.dump(requests_map, fp, indent=2)