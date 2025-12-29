import argparse
import subprocess
import uuid
import os

parser = argparse.ArgumentParser()
parser.add_argument("--video",  "-v",    help="The youtube video to be used as video")
parser.add_argument("--audio",  "-a",    help="The youtube video to be used as audio")
parser.add_argument("--output", "-o",    help="The output filename without extension",    default="output")
parser.add_argument("--start",  "-s",    help="Start the video after download and merge", action="store_true")
parser.add_argument("--keep-temp-files", help="Keep the temporary video and audio files", action="store_true")
args = parser.parse_args()

print(f"Video: {args.video}")
print(f"Audio: {args.audio}")

def run_ytdlp(format, url):
    result = subprocess.run(f"yt-dlp -t {format} {url}")
    return result.returncode

def run_ytdlp_with_output(output, format, url):
    result = subprocess.run(f"yt-dlp -o {output} -t {format} {url}")
    return result.returncode

video_file_name = f"{uuid.uuid4()}"
audio_file_name = f"{uuid.uuid4()}"

print(f"Temporary video filename: {video_file_name}")
print(f"Temporary audio filename: {audio_file_name}")

print("Starting video download...")
if run_ytdlp_with_output(f"{video_file_name}.%(ext)s", "mp4", args.video) != 0:
    print("Failed to download video")
    exit(1)

print("Starting audio download...")
if run_ytdlp_with_output(f"{audio_file_name}.%(ext)s", "aac", args.audio) != 0:
    # TODO: Delete video file
    print("Failed to download audio")
    exit(1)

output_file = f"{args.output}.mp4"
print("Merging video and audio...")
result = subprocess.run(f"ffmpeg -i {video_file_name}.mp4 -i {audio_file_name}.m4a -c:v copy -c:a copy -map 0:v:0 -map 1:a:0 \"{output_file}\"")

if not args.keep_temp_files:
    print("Deleting temporary files...")
    video_file = f"{video_file_name}.mp4"
    audio_file = f"{audio_file_name}.m4a"
    try:
        os.remove(video_file)
        print(f"  Deleted '{video_file}'")
    except OSError as e:
        print(f"ERROR: Failed to delete temporary video file '{video_file}': {e}")

    try:
        os.remove(audio_file)
        print(f"  Deleted '{audio_file}'")
    except OSError as e:
        print(f"ERROR: Failed to delete temporary audio file '{audio_file}': {e}")

if args.start and result.returncode == 0:
    print(f"Starting '{output_file}'...")
    os.startfile(output_file)
