import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = ROOT / "work/ffmpeg/ffmpeg-9.0-essentials_build/bin/ffmpeg.exe"
BASE = ROOT / "work/base-v10-noavatar.mp4"
CTA = ROOT / "outputs/cta-motion-no-books-v5.mp4"
AVATAR = ROOT / "work/heygen-avatar-iii-typecast-v10.mp4"
TIMINGS = ROOT / "audio/word-timings-v10-playlist.json"
OUTPUT = ROOT / "outputs/youtube-auto-v10-synced-no-music.mp4"


def main() -> None:
    duration = float(json.loads(TIMINGS.read_text(encoding="utf-8"))["audio_duration"])
    early_start, early_end = 22.4, 34.6
    final_start = 281.2
    final_length = max(0.1, duration - final_start)
    graph = (
        f"[1:v]fps=24,scale=1280:610,trim=0:{early_end-early_start},"
        f"setpts=PTS-STARTPTS+{early_start}/TB[cta_early];"
        f"[2:v]fps=24,scale=1280:610,trim=0:{final_length},"
        f"setpts=PTS-STARTPTS+{final_start}/TB[cta_final];"
        "[0:v][cta_early]overlay=0:0:eof_action=pass[early];"
        "[early][cta_final]overlay=0:0:eof_action=pass[with_cta];"
        "[3:v]fps=24,crop=650:650:635:150,scale=230:230,format=rgba,"
        "geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
        "a='if(lte(hypot(X-W/2,Y-H/2),W/2-4),255,0)'[avatar_circle];"
        "[with_cta][avatar_circle]overlay=1005:335:eof_action=pass[vout]"
    )
    command = [
        str(FFMPEG), "-y", "-i", str(BASE), "-i", str(CTA), "-i", str(CTA),
        "-i", str(AVATAR), "-filter_complex", graph, "-map", "[vout]",
        "-map", "0:a", "-t", str(duration), "-c:v", "libx264", "-preset",
        "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "copy",
        "-movflags", "+faststart", str(OUTPUT),
    ]
    subprocess.run(command, check=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
