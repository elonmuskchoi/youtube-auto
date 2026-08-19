from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = ROOT / "work/ffmpeg/ffmpeg-9.0-essentials_build/bin/ffmpeg.exe"
SOURCE = ROOT / "outputs/youtube-auto-final-v4-avatar3-bgm-sfx.mp4"
OUTPUT = ROOT / "outputs/youtube-auto-v9-longform-master.mp4"

# Remove one redundant rhetorical sentence after the early expectation CTA.
# Boundaries come from the locked Typecast word-timing file.
CUT_START = 43.319
CUT_END = 47.552
SOURCE_END = 302.565
TRANSITION = 0.25


def main() -> None:
    if not FFMPEG.exists():
        raise FileNotFoundError(f"FFmpeg not found: {FFMPEG}")
    if not SOURCE.exists():
        raise FileNotFoundError(f"Approved master not found: {SOURCE}")

    first_duration = CUT_START
    second_duration = SOURCE_END - CUT_END
    transition_offset = first_duration - TRANSITION

    filter_complex = (
        f"[0:v]trim=start=0:end={CUT_START},setpts=PTS-STARTPTS[v0];"
        f"[0:a]atrim=start=0:end={CUT_START},asetpts=PTS-STARTPTS[a0];"
        f"[0:v]trim=start={CUT_END}:end={SOURCE_END},setpts=PTS-STARTPTS[v1];"
        f"[0:a]atrim=start={CUT_END}:end={SOURCE_END},asetpts=PTS-STARTPTS[a1];"
        f"[v0][v1]xfade=transition=slideleft:duration={TRANSITION}:"
        f"offset={transition_offset}[v];"
        f"[a0][a1]acrossfade=d={TRANSITION}:c1=tri:c2=tri[a]"
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(FFMPEG),
        "-y",
        "-i",
        str(SOURCE),
        "-filter_complex",
        filter_complex,
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "24",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        str(OUTPUT),
    ]
    subprocess.run(command, check=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
