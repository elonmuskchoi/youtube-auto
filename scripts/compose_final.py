import argparse, json, subprocess
from pathlib import Path


def main(base: Path, avatar: Path | None, output: Path, config_path: Path, ffmpeg: str):
    config = json.loads(config_path.read_text(encoding="utf-8"))
    avatar_config = config.get("avatar", {})
    command = [ffmpeg, "-y", "-i", str(base)]
    filter_graph = "[0:v]null[vout]"
    if avatar and avatar_config.get("enabled", True):
        command += ["-i", str(avatar)]
        size = int(avatar_config.get("size", 230))
        x = int(avatar_config.get("x", 1005))
        y = int(avatar_config.get("y", 335))
        filter_graph = f"[1:v]scale={size}:{size}[avatar];[0:v][avatar]overlay={x}:{y}:eof_action=pass[vout]"
    command += ["-filter_complex", filter_graph, "-map", "[vout]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "copy", "-shortest", "-movflags", "+faststart", str(output)]
    subprocess.run(command, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--avatar", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    args = parser.parse_args()
    main(args.base, args.avatar, args.output, args.config, args.ffmpeg)

