import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--name", "-n", default="", help="The playlist name. Defaults to current directory.")
parser.add_argument("--overwrite", "-ow", action="store_true", help="Overwrite the playlist file if already exists.")
parser.add_argument("--absolute", "-a", action="store_true", help="Write absolute paths instead of relative.")
args = parser.parse_args()

allowed_extensions = { ".mkv", ".mp4" }
playlist_file = args.name if args.name else Path().cwd().stem
if not playlist_file.endswith(".m3u"):
    playlist_file += ".m3u"

if (Path(playlist_file).exists() and not args.overwrite):
    print(f"ERROR: Playlist file {playlist_file} already exists, use --overwrite/-ow to overwrite the existing file")
    exit(1)

print(f"> {playlist_file}")
with open(playlist_file, 'w', encoding="utf-8") as file:
    for path in sorted(Path(".").iterdir()):
        if path.suffix.lower() in allowed_extensions:
            p = path.absolute() if args.absolute else path
            print(f"  * {p}")
            file.write(f"{p}\n")
