import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FFMPEG = ROOT / "work/ffmpeg/ffmpeg-9.0-essentials_build/bin/ffmpeg.exe"
ASSETS = ROOT / "work/cta-assets"
ACTION = ROOT / "outputs/cta-dynamic-master-v4.mp4"
OUTPUT = ROOT / "outputs/cta-motion-no-books-v5.mp4"


def main():
    inputs = [ASSETS / f"seg{i:02}.mp4" for i in range(2, 6)] + [ACTION]
    command = [str(FFMPEG), "-y"]
    for source in inputs:
        command += ["-i", str(source)]
    filters = (
        "[0:v]fps=24,scale=1280:610,setsar=1,trim=0:4.5,setpts=PTS-STARTPTS[s0];"
        "[1:v]fps=24,scale=1280:610,setsar=1,trim=0:4.5,setpts=PTS-STARTPTS[s1];"
        "[2:v]fps=24,scale=1280:610,setsar=1,trim=0:4,setpts=PTS-STARTPTS[s2];"
        "[3:v]fps=24,scale=1280:610,setsar=1,trim=0:4,setpts=PTS-STARTPTS[s3];"
        "[4:v]fps=24,scale=1280:610,setsar=1,trim=start=16.5:end=25.5,setpts=PTS-STARTPTS[s4];"
        "[s0][s1][s2][s3][s4]concat=n=5:v=1:a=0[v]"
    )
    command += ["-filter_complex", filters, "-map", "[v]", "-c:v", "libx264", "-preset", "fast",
                "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUTPUT)]
    subprocess.run(command, check=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
