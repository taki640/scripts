import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--audio", "-a", action="append", default=[], type=int, help="Audio channels to remove")
parser.add_argument("--subtitle", "-s", action="append", default=[], type=int, help="Subtitle channels to remove")
parser.add_argument("--mode", "-m", choices=["remove", "keep"], default="remove", help="Whether to remove or keep specified channels")
args = parser.parse_args()

if len(args.audio) == 0 and len(args.subtitle) == 0:
    print("Error: No audio or subtitle channels provided")
    exit(1)

Path("output").mkdir(exist_ok = True)

allowedExtensions = { ".mkv", ".mp4" }
for path in Path(".").glob("*"):
    if path.exists() and path.is_file() and path.suffix.lower() in allowedExtensions:
        ffmpegArgs = [ "ffmpeg", "-i", str(path), "-c", "copy", "-disposition:s:0", "default", f"output/{path.name}" ]
        mapArgs: list[str] = []

        if args.mode == "remove":
            mapArgs += ["-map", "0"] # Keep everything
            for channel in args.audio:
                mapArgs += ["-map", f"-0:a:{channel}"]
            for channel in args.subtitle:
                mapArgs += ["-map", f"-0:s:{channel}"]
        elif args.mode == "keep":
            mapArgs += ["-map", "0:v"] # Keep all video channels
            if (len(args.audio) > 0):
                for channel in args.audio:
                    mapArgs += ["-map", f"0:a:{channel}"]
            else:
                mapArgs += ["-map", "0:a"] # Keep all audio if no channels are specified

            if (len(args.subtitle) > 0):
                for channel in args.subtitle:
                    mapArgs += ["-map", f"0:s:{channel}"]
            else:
                mapArgs += ["-map", "0:s"] # Keep all subtitles if no channels are specified

        ffmpegArgs[3:3] = mapArgs
        subprocess.run(ffmpegArgs)
