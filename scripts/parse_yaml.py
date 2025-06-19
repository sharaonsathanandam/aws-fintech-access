import yaml, json, sys, os, subprocess, glob

yaml_dir = ["access-requests/finance", "access-requests/treasury-ops"]
script_dir = os.path.dirname(os.path.abspath(__file__))

requests_map = []
for d in yaml_dir:
    pattern = os.path.join(f"{d}/*.yaml")
    for path in sorted(glob.glob(pattern)):
        key = os.path.splitext(os.path.basename(path))[0]
        data = yaml.safe_load(open(path)) or {}
        requests_map.append(data)

out_path = "pipeline-config/requests.json"
with open(out_path, "w") as fp:
    json.dump(requests_map, fp, indent=2)