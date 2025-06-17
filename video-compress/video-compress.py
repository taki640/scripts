import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", type = str, help = "A video file to compress. If empty, all video files in the directory are compressed instead")
parser.add_argument("--recursive", "-r", action = "store_true", help = "Compress videos in subdirectories, default is false")
parser.add_argument("--quality", "-q", type = int, default = 26, help = "Quality factor, from 0 to 51, lower is better, default is 26")
parser.add_argument("--size", "-s", type = str, default = "", help = "New resolution 'width:height', e.g. '1280:720'")
parser.add_argument("--cpu-enc", action = "store_true", help = "Use libx264 instead of h264_amf.")
args = parser.parse_args()

width = 25
print("+" + "–" * width + "+")
print(f"|{'video-compress options:':^{width}}|")
print(f"|   Recursive: {str(args.recursive):<{width - 14}}|")
print(f"|   Quality: {str(args.quality):<{width - 12}}|")
print(f"|   Size: {str(args.size) if args.size else 'Original':<{width - 9}}|")
print(f"|   GPU encoding: {str(not args.cpu_enc):<{width - 17}}|")
print("+" + "–" * width + "+")

files: list[Path] = []
allowedExtensions = { ".mkv", ".mp4" }

def IteratePath():
    return Path(".").rglob("*") if args.recursive else Path(".").glob("*")

def RunFFMPEG(input: str, output: str):
    # TODO: Identify if the current GPU is AMD or Nvidia and use h264_nvenc for nvidia GPUs, I don't even know what would happen if this was ran on an Nvidia gpu
    ffmpegArgs = ["ffmpeg", "-i", input]
    if args.size:
        ffmpegArgs += ["-vf", f"scale={args.size}"]
    if args.cpu_enc:
        ffmpegArgs += [ "-c:v", "libx264", "-crf", str(args.quality), ] 
    else:
        ffmpegArgs += [ "-c:v", "h264_amf", "-rc", "cqp", "-qp_i", str(args.quality), "-qp_p", str(args.quality), "-qp_b", str(args.quality) ]
    ffmpegArgs += ["-c:a", "aac", "-strict", "experimental", "-b:a", "128k", "-map", "0", "-c:s", "copy", output]
    print(f"Running: {ffmpegArgs}")
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
