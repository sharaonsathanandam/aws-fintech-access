import subprocess, sys , yaml, json, os

yaml_path = sys.argv[1]

# Get contents of deleted file from last commit
print(f"Extracting deleted content from git history for {yaml_path}")
try:
    content = subprocess.check_output(
        ["git", "show", f"HEAD~1:{yaml_path}"]
    ).decode("utf-8")
except subprocess.CalledProcessError:
    print(f"Could not find deleted file content in git history: {yaml_path}")
    sys.exit(0)

data = yaml.safe_load(content)

if not data.get("is_access_request", False):
    print(f"Skipping: {yaml_path} was not an access request file.")
    sys.exit(0)

# Auto-inject principal ARN based on user_id (for access-requests)
account_id = subprocess.check_output([
    "/usr/local/bin/aws", "sts", "get-caller-identity", "--query", "Account", "--output", "text"
]).decode("utf-8").strip()
# data["principal_arn"] = f"arn:aws:iam::{account_id}:role/AWSReservedSSO_FinanceAnalysts_b67570c300321d27"

data["is_access_request"] = False
with open("pipeline-config/terraform.tfvars.json", "w") as f:
    json.dump(data, f, indent=2)

with open("pipeline-config/terraform.tfvars.json", "w") as out:
    json.dump(data, out, indent=2)

print("Final tfvars file content:")
with open("pipeline-config/terraform.tfvars.json") as f:
    print(f.read())