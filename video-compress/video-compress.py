import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", type = str, help = "A video file to compress. If empty, all video files in the directory are compressed instead")
parser.add_argument("--recursive", "-r", action = "store_true", help = "Compress videos in subdirectories, default is false")
parser.add_argument("--crf", "-c", type = int, default = 23, help = "Constant Rate Factor, from 0 to 51, lower is better, default is 23")
parser.add_argument("--size", "-s", type = str, default = "", help = "New resolution 'width:height', e.g. '1280:720'")
args = parser.parse_args()

print("-----------------------")
print(f"video-compress options")
print(f"  Recursive: {args.recursive}")
print(f"  crf: {args.crf}")
print(f"  size: {(args.size if args.size else "Original")}")
print("-----------------------")

files: list[Path] = []
allowedExtensions = { ".mkv", ".mp4" }

def IteratePath():
    return Path(".").rglob("*") if args.recursive else Path(".").glob("*")

def RunFFMPEG(input: str, output: str):
    ffmpegArgs = ["ffmpeg", "-i", input, "-c:v", "libx264", "-crf", str(args.crf), "-c:a", "aac", "-strict", "experimental", "-b:a", "128k", "-map", "0", "-c:s", "copy", output ]
    if args.size:
        ffmpegArgs[3:3] = [ "-vf", f"scale={args.size}" ]
    subprocess.run(ffmpegArgs)

if args.input:
    input = Path(args.input)
    output = f"{input.stem}_compressed{input.suffix}"
    RunFFMPEG(str(input), output)
else:
    # Gather files first to avoid including files from the output folder
    for path in IteratePath():
        if path.exists() and path.is_file() and path.suffix.lower() in allowedExtensions:
            files.append(path)
    
    if len(files) == 0:
        print("No video files to compress")

    for file in files:
        if file.exists():
            outputDir = f"{file.parent}/output"
            Path(outputDir).mkdir(exist_ok = True)
            input = str(file)
            output = f"{outputDir}/{file.name}"
            RunFFMPEG(input, output)
