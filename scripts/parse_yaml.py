import yaml, json, sys, os, subprocess, glob

yaml_dir = ["access-requests/finance", "access-requests/treasury-ops"]
script_dir = os.path.dirname(os.path.abspath(__file__))

requests = []
for d in yaml_dir:
    pattern = os.path.join(os.path.dirname(script_dir),f"{d}/*.yaml")
    print("pattern: ", pattern)
    for path in sorted(glob.glob(pattern)):
        print("inside for")
        with open(path) as f:
            fragment = yaml.safe_load(f) or {}
            print(fragment)
        requests.append(fragment)

out = {"requests": requests}
out_path = "terraform.tfvars.json"
with open(out_path, "w") as fp:
    json.dump(out, fp, indent=2)