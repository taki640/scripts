import argparse
import os
import stat
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--execute", "-e", action="store_true", help="Execute the rename operation. This script does a dry run by default.")
parser.add_argument("--replace", "-r", default="", help="A string to replace. E.g. 'old:new'")
parser.add_argument("--prefix-timestamp", "-pt", action="store_true", help="Prefix the timestamp in the file name.")
parser.add_argument("--separator", "-s", default="-", help="The character after the timestamp.")
args = parser.parse_args()

if not args.execute:
    print("--- DRY RUN ---")

replace = []
if len(args.replace) > 0:
    replace = args.replace.split(':')
    if len(replace) != 2:
        print("ERROR: --replace/-r argument has an invalid value, the correct format is: '<old>:<new>'")
        exit(1)

SKIP = stat.FILE_ATTRIBUTE_SYSTEM | stat.FILE_ATTRIBUTE_HIDDEN

for path in Path(".").iterdir():
    if not path.is_file():
        continue
    if os.stat(path).st_file_attributes & SKIP:
        continue

    new_path = f"{path}"
    if len(replace) > 0:
        new_path = new_path.replace(replace[0], replace[1])

    if args.prefix_timestamp:
        new_path = f"{int(path.stat().st_mtime)}{args.separator}{new_path}"

    print(f"{path} -> {new_path}")
    if args.execute:
        path.rename(new_path)

if not args.execute:
    print("--- DRY RUN ---")
