import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = ROOT / "work/ffmpeg/ffmpeg-9.0-essentials_build/bin/ffmpeg.exe"
SOURCE = ROOT / "outputs/youtube-auto-final-v4-synced-no-music.mp4"
BGM = ROOT / "audio/bgm-ai-tech-cc0.mp3"
OUTPUT = ROOT / "outputs/youtube-auto-final-v4-avatar3-bgm-sfx.mp4"
CUES = json.loads((ROOT / "config/sfx_cues_v4.json").read_text(encoding="utf-8"))["cues"]


def main():
    command = [str(FFMPEG), "-y", "-i", str(SOURCE), "-stream_loop", "-1", "-i", str(BGM)]
    for cue in CUES:
        command.extend(["-i", str(ROOT / "work/sfx" / cue["asset"])])

    filters = [
        "[0:a]aresample=48000,volume=1.0[voice]",
        "[1:a]aresample=48000,volume=0.075,afade=t=in:st=0:d=2[bgm]",
        "[bgm][voice]sidechaincompress=threshold=0.012:ratio=10:attack=18:release=550:makeup=1[ducked]",
    ]
    labels = ["[voice]", "[ducked]"]
    for index, cue in enumerate(CUES, start=2):
        delay = round(float(cue["time"]) * 1000)
        gain = float(cue["gain"])
        filters.append(f"[{index}:a]aresample=48000,atrim=0:3,asetpts=PTS-STARTPTS,volume={gain},adelay={delay}|{delay}[s{index}]")
        labels.append(f"[s{index}]")
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:duration=first:normalize=0,alimiter=limit=0.95[aout]")

    command.extend([
        "-filter_complex", ";".join(filters),
        "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUTPUT),
    ])
    subprocess.run(command, check=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()

