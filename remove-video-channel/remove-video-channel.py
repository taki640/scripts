import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--audio", "-a", action="append", default=[], type=int, help="Audio channels to remove")
parser.add_argument("--subtitle", "-s", action="append", default=[], type=int, help="Subtitle channels to remove")
args = parser.parse_args()

if len(args.audio) == 0 and len(args.subtitle) == 0:
    print("Error: No audio or subtitle channels provided")
    exit(1)

Path("output").mkdir(exist_ok = True)

allowedExtensions = { ".mkv", ".mp4" }
for path in Path(".").glob("*"):
    if path.exists() and path.is_file() and path.suffix.lower() in allowedExtensions:
        ffmpegArgs = [ "ffmpeg", "-i", str(path), "-map", "0", "-c", "copy", "-disposition:s:0", "default", f"output/{path.name}" ]
        channels: list[str] = []
        if len(args.audio) > 0:
            for channel in args.audio:
                channels.append("-map")
                channels.append(f"-0:a:{channel}")

        if len(args.subtitle) > 0:
            for channel in args.subtitle:
                channels.append("-map")
                channels.append(f"-0:s:{channel}")

        ffmpegArgs[5:5] = channels
        subprocess.run(ffmpegArgs)
