import subprocess
from pathlib import Path

for path in Path(".").glob("screenshot *.png"):
    print(f"> Processing '{path}'...")
    unix_timestamp = str(path.stem).removeprefix("screenshot ")
    args = [ "exiftool", "-d", "%s", f"-AllDates={unix_timestamp}", "-overwrite_original", path ]
    subprocess.run(args, check=False)
    print("  Done")
