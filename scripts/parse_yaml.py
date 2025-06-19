import yaml, json, sys, os, subprocess, glob

yaml_dir = ["access-requests/finance", "access-requests/treasury-ops"]
script_dir = os.path.dirname(os.path.abspath(__file__))

requests_map = []
for d in yaml_dir:
    pattern = os.path.join(f"{d}/*.yaml")
    for path in sorted(glob.glob(pattern)):
        key = os.path.splitext(os.path.basename(path))[0]
        data = yaml.safe_load(open(path)) or {}
        if d == "access-requests/finance":
            data['principal_arn'] = "AWSReservedSSO_FinanceAnalysts_b67570c300321d27"
        elif d == "access-requests/treasury-ops":
            data['principal_arn'] = "AWSReservedSSO_TreasuryOps_c96dc0d2a167af60"
        requests_map.append(data)

out_path = "pipeline-config/requests.json"
with open(out_path, "w") as fp:
    json.dump(requests_map, fp, indent=2)