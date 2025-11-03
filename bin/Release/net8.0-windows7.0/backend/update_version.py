import os
os.chdir(os.path.dirname(__file__))
lines = open("pyproject.toml", "r").readlines()
version = [l for l in lines if l.startswith("version")][0].split("=")[1].strip().strip('"')
a = version.split(".")[0]
b = version.split(".")[1]
c = version.split(".")[2]
new_version = f"{a}.{b}.{int(c)+1}"
with open("pyproject.toml", "w") as f:
    for line in lines:
        if line.startswith("version"):
            f.write(f'version = "{new_version}"\n')
        else:
            f.write(line)