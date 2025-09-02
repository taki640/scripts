import os
import argparse
import math
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--only", "-o", default="", type=str, help="Only show executables whose path contains the given string(s). Use commas to separate multiple values.")
parser.add_argument("--ignore", "-i", default="", type=str, help="Ignore executables whose path contains the given string(s). Use commas to separate multiple values.")
parser.add_argument("--columns", "-c", default=3, type=int, help="Number of columns used when printing the executables.")
args = parser.parse_args()

only_dirs = args.only.lower().split(',')
ignore_dirs = args.ignore.lower().split(',')

path_dirs = os.environ["PATH"].split(os.pathsep)
extensions = [".exe", ".bat", ".cmd"]

executables = []
largest_name = 0

for dir_path in path_dirs:
    dir_path = Path(dir_path)
    dir_path_lower = str(dir_path).lower()

    if args.ignore != "":
        if any(d in dir_path_lower for d in ignore_dirs):
            continue
    if args.only != "":
        if not all(d in dir_path_lower for d in only_dirs):
            continue

    if dir_path.exists() and dir_path.is_dir():
        for file in dir_path.iterdir():
            if file.is_file() and file.suffix.lower() in extensions:
                f = file.stem
                largest_name = max(len(f), largest_name)
                executables.append(f)

if args.columns <= 1:
    for executable in sorted(executables):
        print(executable)
else:
    executables = sorted(executables)
    num_cols = args.columns
    num_rows = math.ceil(len(executables) / num_cols)

    for row in range(num_rows):
        line = ""
        for col in range(num_cols):
            index = row * num_cols + col
            if index < len(executables):
                line += f"{executables[index]:<{largest_name + 2}}"
        print(line)
