# File syntax: <filename> : <start_time> : <end_time> : <output_dir>
# Example:
#   video_1.mkv | 00:10:00 | 00:11:00 | output
#   video_2.mkv | 00:05:00 | 00:06:49 | output
#   video_3.mkv | 00:00:10 | 01:12:00 | output

import os
import sys
import re
import subprocess
from datetime import datetime

if len(sys.argv) < 2:
    print("Error: Input file not provided")
    print("Usage: batch-trim.py <trim_list_file_path> [<new_format>]")
    exit(1)

def is_valid_line(s: str):
    return re.match(r'^.+\|\d{2}:\d{2}:\d{2}\|\d{2}:\d{2}:\d{2}\|.+$', s) is not None

def get_duration(start_time: str, end_time: str) -> str:
    duration = int((datetime.strptime(end_time, "%H:%M:%S") - datetime.strptime(start_time, "%H:%M:%S")).total_seconds())
    durationStr = f"{(duration // 3600):02}:{((duration % 3600) // 60):02}:{(duration % 60):02}"
    return durationStr

def get_output_filename(input_file: str, format: str, output_dir: str) -> str:
    base = os.path.basename(input_file)
    name, ext = os.path.splitext(base)

    if format:
        ext = format if format.startswith('.') else f".{format}"

    candidate = os.path.join(output_dir, name + ext)
    counter = 1
    while os.path.exists(candidate):
        candidate = os.path.join(output_dir, f"{name}_{counter}{ext}")
        counter += 1

    return os.path.basename(candidate)

def trim_video(options: list[str], format: str):
    if len(options) < 4:
        print("Error: invalid options")
        return

    input_file = options[0]
    start_time = options[1]
    duration = get_duration(options[1], options[2]) # Convert to duration because -t is more reliable than -to
    output_dir = options[3]
    os.makedirs(output_dir, exist_ok=True)
    subprocess.run([ "ffmpeg", "-ss", start_time, "-t", duration, "-i", input_file, "-map_chapters", "-1", "-c", "copy", f"{output_dir}/{get_output_filename(input_file, format, output_dir)}" ])

config_path = sys.argv[1]
format = ""
if len(sys.argv) > 2:
    format = sys.argv[2]

with open(config_path) as file:
    for i, line in enumerate(file.readlines()):
        line = line.strip().replace(" | ", "|").replace(" |", "|").replace("| ", "|") # This is disgusting lol
        if line:
            if not is_valid_line(line):
                print(f"Line {i + 1} has incorrect syntax and was ignored")
                continue
            trim_video(line.split('|'), format)
