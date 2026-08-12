import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = ROOT / "work/ffmpeg/ffmpeg-9.0-essentials_build/bin/ffmpeg.exe"
BASE = ROOT / "work/base-long-v3-noavatar.mp4"
CTA = ROOT / "outputs/cta-dynamic-master.mp4"
AVATAR = ROOT / "work/heygen-avatar-iii-typecast-v3-full.mp4"
OUTPUT = ROOT / "outputs/youtube-auto-final-v3-avatar3-typecast.mp4"


FILTER = r"""
[1:v]fps=24,scale=1280:610[cta];
[0:v][cta]overlay=0:0:enable='between(t,43,68)+between(t,280,322.52)':eof_action=pass[with_cta];
[2:v]fps=24,crop=650:650:635:150,scale=230:230,format=rgba,
geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lte(hypot(X-W/2,Y-H/2),W/2-4),255,0)'[avatar_circle];
[with_cta][avatar_circle]overlay=1005:365:eof_action=pass[vout]
""".replace("\n", "")


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(FFMPEG), "-y",
        "-i", str(BASE),
        "-stream_loop", "-1", "-i", str(CTA),
        "-i", str(AVATAR),
        "-filter_complex", FILTER,
        "-map", "[vout]", "-map", "0:a",
        "-t", "322.52",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy", "-movflags", "+faststart",
        str(OUTPUT),
    ]
    subprocess.run(command, check=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
