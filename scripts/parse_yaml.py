import yaml, json, sys, os, subprocess, glob

yaml_dir = ["access-requests/finance", "access-requests/treasury-ops"]
script_dir = os.path.dirname(os.path.abspath(__file__))

requests = []
for d in yaml_dir:
    pattern = os.path.join(f"{d}/*.yaml")
    for path in sorted(glob.glob(pattern)):
        with open(path) as f:
            fragment = yaml.safe_load(f) or {}
        requests.append(fragment)

out = {"requests": requests}
out_path = "pipeline-config/terraform.tfvars.json"
with open(out_path, "w") as fp:
    json.dump(out, fp, indent=2)