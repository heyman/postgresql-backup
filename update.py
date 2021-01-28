import os
import re
import shutil


# versions will be a list of all #, ## and ##.## directories
versions = [p for p in os.listdir() if os.path.isdir(p) and re.match(r"^\d+(\.\d+)?$", p)]

with open(os.path.join("template", "Dockerfile.template"), "r", encoding="utf-8") as f:
    dockerfile_template = f.read()

for version in versions:
    # write Dockerfile in version directory
    with open(os.path.join(version, "Dockerfile"), "w", encoding="utf-8") as f:
        f.write(dockerfile_template % {"VERSION":version})
    
    # copy other files into version directory
    for file_name in os.listdir("template"):
        if file_name == "Dockerfile.template":
            continue
        shutil.copyfile(os.path.join("template", file_name), os.path.join(version, file_name))

