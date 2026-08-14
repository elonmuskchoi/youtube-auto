import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = ROOT / "work/ffmpeg/ffmpeg-9.0-essentials_build/bin/ffmpeg.exe"
BASE = ROOT / "work/base-long-v4-noavatar.mp4"
CTA = ROOT / "outputs/cta-motion-no-books-v5.mp4"
AVATAR = ROOT / "work/heygen-avatar-iii-typecast-v4-long.mp4"
OUTPUT = ROOT / "outputs/youtube-auto-final-v4-synced-no-music.mp4"
TIMINGS = ROOT / "audio/word-timings-final-v4-long.json"


def main():
    duration = float(json.loads(TIMINGS.read_text(encoding="utf-8"))["audio_duration"])
    filter_graph = (
        "[1:v]fps=24,scale=1280:610,trim=0:12.2,setpts=PTS-STARTPTS+29.5/TB[cta_early];"
        "[2:v]fps=24,scale=1280:610,trim=0:26,tpad=stop_mode=clone:stop_duration=20,setpts=PTS-STARTPTS+259.8/TB[cta_final];"
        "[0:v][cta_early]overlay=0:0:eof_action=pass[early];"
        "[early][cta_final]overlay=0:0:eof_action=pass[with_cta];"
        "[3:v]fps=24,crop=650:650:635:150,scale=230:230,format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lte(hypot(X-W/2,Y-H/2),W/2-4),255,0)'[avatar_circle];"
        "[with_cta][avatar_circle]overlay=1005:365:"
        f"enable='not(between(t,29.5,41.7)+between(t,259.8,{duration}))':"
        "eof_action=pass[vout]"
    )
    command = [
        str(FFMPEG), "-y", "-i", str(BASE),
        "-i", str(CTA), "-i", str(CTA), "-i", str(AVATAR),
        "-filter_complex", filter_graph,
        "-map", "[vout]", "-map", "0:a", "-t", str(duration),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
        str(OUTPUT),
    ]
    subprocess.run(command, check=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
