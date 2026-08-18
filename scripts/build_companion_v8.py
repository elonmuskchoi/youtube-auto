import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = ROOT / "work/ffmpeg/ffmpeg-9.0-essentials_build/bin/ffmpeg.exe"
SOURCE = ROOT / "outputs/youtube-auto-final-v4-avatar3-bgm-sfx.mp4"
OUTPUT = ROOT / "outputs/youtube-auto-companion-v8-public-cases.mp4"


def main():
    # Sentence-boundary selections from the approved long-form master.
    sections = [(0.0, 25.9), (152.666, 216.8), (234.951, 302.565)]
    fade = 0.45
    d0 = sections[0][1] - sections[0][0]
    d1 = sections[1][1] - sections[1][0]
    first_join_duration = d0 + d1 - fade
    filters = (
        f"[0:v]trim=start={sections[0][0]}:end={sections[0][1]},setpts=PTS-STARTPTS[v0];"
        f"[0:a]atrim=start={sections[0][0]}:end={sections[0][1]},asetpts=PTS-STARTPTS[a0];"
        f"[0:v]trim=start={sections[1][0]}:end={sections[1][1]},setpts=PTS-STARTPTS[v1];"
        f"[0:a]atrim=start={sections[1][0]}:end={sections[1][1]},asetpts=PTS-STARTPTS[a1];"
        f"[0:v]trim=start={sections[2][0]}:end={sections[2][1]},setpts=PTS-STARTPTS[v2];"
        f"[0:a]atrim=start={sections[2][0]}:end={sections[2][1]},asetpts=PTS-STARTPTS[a2];"
        f"[v0][v1]xfade=transition=fade:duration={fade}:offset={d0-fade}[v01];"
        f"[a0][a1]acrossfade=d={fade}:c1=tri:c2=tri[a01];"
        f"[v01][v2]xfade=transition=slideleft:duration={fade}:offset={first_join_duration-fade}[vout];"
        f"[a01][a2]acrossfade=d={fade}:c1=tri:c2=tri[aout]"
    )
    command = [
        str(FFMPEG), "-y", "-i", str(SOURCE), "-filter_complex", filters,
        "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "fast",
        "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(OUTPUT),
    ]
    subprocess.run(command, check=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
