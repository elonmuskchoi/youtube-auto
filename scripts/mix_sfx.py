import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = ROOT / "work/ffmpeg/ffmpeg-9.0-essentials_build/bin/ffmpeg.exe"
SOURCE = ROOT / "outputs/youtube-auto-final-v3-avatar3-typecast.mp4"
OUTPUT = ROOT / "outputs/youtube-auto-final-v3-avatar3-typecast-sfx.mp4"
CUES = json.loads((ROOT / "config/sfx_cues.json").read_text(encoding="utf-8"))["cues"]


def main():
    probe = subprocess.run(
        [str(FFMPEG.with_name("ffprobe.exe")), "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(SOURCE)],
        capture_output=True,
        text=True,
    ) if SOURCE.exists() else None
    if probe is None or probe.returncode != 0:
        subprocess.run([str(ROOT / ".venv/Scripts/python.exe"), str(ROOT / "scripts/compose_final_v3.py")], check=True)

    command = [str(FFMPEG), "-y", "-i", str(SOURCE)]
    for cue in CUES:
        command.extend(["-i", str(ROOT / "work/sfx" / cue["asset"])])

    filters = ["[0:a]volume=1.0[voice]"]
    labels = ["[voice]"]
    for index, cue in enumerate(CUES, start=1):
        delay = round(float(cue["time"]) * 1000)
        gain = float(cue["gain"])
        filters.append(f"[{index}:a]atrim=0:3,asetpts=PTS-STARTPTS,volume={gain},adelay={delay}|{delay}[s{index}]")
        labels.append(f"[s{index}]")
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:duration=first:normalize=0,alimiter=limit=0.95[aout]")

    command.extend([
        "-filter_complex", ";".join(filters),
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(OUTPUT),
    ])
    subprocess.run(command, check=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
