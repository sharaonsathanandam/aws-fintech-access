import yaml, json, sys, os, subprocess, glob

yaml_dir = ["finance", "treasury-ops"]

# with open(input_file) as f:
#     data = yaml.safe_load(f)
#
# folder_name = os.path.basename(os.path.dirname(input_file))
#
# # Auto-inject principal ARN based on user_id (for access-requests)
# account_id = subprocess.check_output([
#     "/usr/local/bin/aws", "sts", "get-caller-identity", "--query", "Account", "--output", "text"
# ]).decode("utf-8").strip()
# # data["principal_arn"] = f"arn:aws:iam::{account_id}:role/AWSReservedSSO_FinanceAnalysts_b67570c300321d27"
#
# out_path = "pipeline-config/terraform.tfvars.json"
#
# print(data)

requests = []
for d in yaml_dir:
    pattern = os.path.join(d, "*.yaml")
    print(d)
    for path in sorted(glob.glob(pattern)):
        with open(path) as f:
            fragment = yaml.safe_load(f) or {}
            print(fragment)
        requests.append(fragment)

out = {"requests": requests}
out_path = "pipeline-config/terraform.tfvars.json"
with open(out_path, "w") as fp:
    json.dump(out, fp, indent=2)