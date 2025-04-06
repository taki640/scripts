import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--recursive", "-r", action = "store_true", help = "Compress videos in subdirectories, default is false")
parser.add_argument("--crf", "-c", type = int, default = 23, help = "Constant Rate Factor, from 0 to 51, lower is better, default is 23")
parser.add_argument("--size", "-s", type = str, default = "", help = "New resolution 'width:height', e.g. '1280:720'")
args = parser.parse_args()

print("-----------------------")
print(f"video-compress options")
print(f"  Recursive: {args.recursive}")
print(f"  crf: {args.crf}")
print(f"  size: {args.size}")
print("-----------------------")

files: list[Path] = []
allowedExtensions = { ".mkv", ".mp4" }

def IteratePath():
    return Path(".").rglob("*") if args.recursive else Path(".").glob("*")

# Gather files first to avoid including files from the output folder
for path in IteratePath():
    if path.exists() and path.is_file() and path.suffix.lower() in allowedExtensions:
        files.append(path)

for file in files:
    if file.exists():
        outputDir = f"{file.parent}/output"
        Path(outputDir).mkdir(exist_ok = True)
        ffmpegArgs = ["ffmpeg", "-i", str(file), "-c:v", "libx264", "-crf", str(args.crf), "-c:a", "aac", "-strict", "experimental", "-b:a", "128k", "-map", "0", "-c:s", "copy", f"{outputDir}/{file.name}" ]
        if args.size:
            ffmpegArgs[3:3] = [ "-vf", f"scale={args.size}" ]
        subprocess.run(ffmpegArgs)
