import os
from pathlib import Path

dirs = ["dir_2010_64", "dir_2012_13", "dir_2016_343", "dir_2013_48"]
laws = ["it", "nl", "bg", "pl"]

comb_a = {f"{x}_{y}" : f"{x.replace("dir", "directive")}@{y}" for x in dirs for y in laws}
comb_b = {f"{x}" : f"{x.replace("dir", "directive")}@it" for x in dirs}

comb = {**comb_a, **comb_b}

def new_name(f, i):
    splits = f.split("@")
    if splits[0] == "general_facts":
        return f"directive_2010_64@it@personId@{i}.txt"
    return f"{comb[splits[0]]}@personId@{i}.txt"

if __name__ == "__main__":
    path = os.path.join(Path(__file__).parent.absolute(), "..", "res", "extraction")
    files = [f for f in os.listdir(path) if f.endswith("txt")]
    for i, file in enumerate(files):
        if "personId" in file:
            os.rename(os.path.join(path, file), os.path.join(path, file.replace("personId", "bruno")))
            with open(os.path.join(path, file.replace("personId", "bruno")), "r+") as f:
                c = f.read().replace("personId", "bruno")
                f.seek(0)
                f.write(c)
                f.truncate()
