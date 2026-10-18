import argparse
import json
import random
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--shuffle", "-s", action="store_true", help="Shuffle the output")
args = parser.parse_args()

class movie_duration:
    hours: int
    minutes: int
    seconds: int

class movie:
    name: str
    duration: movie_duration

def find_movie_duration(file: Path):
    cmd = [ "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", file ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    duration_secs = float(data["format"]["duration"])
    duration = movie_duration()
    duration.minutes, duration.seconds = divmod(int(duration_secs), 60)
    duration.hours, duration.minutes = divmod(duration.minutes, 60)
    return duration

def process_movie_folder(directory: Path):
    extensions = { ".mkv", ".mp4" }

    for path in directory.iterdir():
        if path.is_file() and path.suffix.lower() in extensions:
            m = movie()
            m.name = str(directory)
            m.duration = find_movie_duration(path)
            return m

movies = []

for path in Path(".").glob("*"):
    if (path.is_dir()):
        movies.append(process_movie_folder(path))

name_width = max(len(movie.name) for movie in movies)

if (args.shuffle):
    random.shuffle(movies)

print(f"{'[Name]':<{name_width}}    [Duration]")
for movie in movies:
    duration = f"{movie.duration.hours:02}:{movie.duration.minutes:02}:{movie.duration.seconds:02}"
    print(f"{movie.name:<{name_width}}     {duration}")
