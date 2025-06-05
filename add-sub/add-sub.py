import argparse
import subprocess
from pathlib import Path
import sys

VIDEO_EXTS = ['.mp4', '.mkv']
SUB_EXTS = ['.srt', '.ass']
OUTPUT_DIR = Path('output')

def run_ffmpeg(video_path: Path, sub_path: Path, output_path: Path):
    print(f"- Adding subtitle '{sub_path}' on video '{video_path}'...")
    cmd = ['ffmpeg', '-i', str(video_path), '-i', str(sub_path), '-c', 'copy']
    if video_path.suffix == '.mp4':
        cmd += ['-c:s', 'mov_text']
    cmd += ['-disposition:s:0', 'default', str(output_path)]
    subprocess.run(cmd, check=True)

def process_from_txt(txt_path: Path):
    base_dir = txt_path.parent
    OUTPUT_DIR.mkdir(exist_ok=True)
    with txt_path.open('r', encoding='utf-8') as f:
        for line in f:
            if '<' not in line:
                continue
            video_rel, sub_rel = map(str.strip, line.strip().split('<', 1))
            video_path = base_dir / video_rel
            sub_path = base_dir / sub_rel
            output_file = OUTPUT_DIR / video_path.name
            run_ffmpeg(video_path, sub_path, output_file)


def process_single_file(video: Path, subtitle: Path):
    if not video.exists() or not subtitle.exists():
        print("Error: One or both input files do not exist.")
        sys.exit(1)
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_file = OUTPUT_DIR / video.name
    run_ffmpeg(video, subtitle, output_file)

parser = argparse.ArgumentParser(
    description="Add subtitles to video files using ffmpeg.",
    epilog="Examples:\n"
           "  add-sub video_sub_data.txt\n"
           "  add-sub video.mp4 subtitle.srt",
    formatter_class=argparse.RawTextHelpFormatter
)


if (len(sys.argv) == 1):
    parser.print_help()    
    sys.exit(1)

parser.add_argument("inputs", nargs='+', help="Either a .txt file or a video + subtitle pair.")
args = parser.parse_args()

if len(args.inputs) == 1:
    txt_path = Path(args.inputs[0])
    if not txt_path.exists():
        print(f"Error: File '{txt_path}' does not exist.")
        sys.exit(1)
    process_from_txt(txt_path)
elif len(args.inputs) == 2:
    video = Path(args.inputs[0])
    subtitle = Path(args.inputs[1])
    process_single_file(video, subtitle)
