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
    files = [f for f in os.listdir(Path(__file__).parent.absolute()) if f.endswith("txt")]
    path = Path(__file__).parent.absolute()
    for i, file in enumerate(files):
        os.rename(os.path.join(path, file), os.path.join(path, new_name(file, i)))
