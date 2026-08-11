import argparse, json
from pathlib import Path


def main(config_path: Path, timeline_path: Path):
    project = json.loads(config_path.read_text(encoding="utf-8"))
    timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
    duration = timeline["duration"]
    scenes = sorted(timeline["scenes"], key=lambda scene: scene["start"])
    errors = []
    for scene in scenes:
        if not 0 <= scene["start"] < scene["end"] <= duration:
            errors.append(f"Invalid interval: {scene}")
        if scene["type"] == "proof" and not any(word in scene.get("purpose", "").lower() for word in ("revenue", "success", "credibility")):
            errors.append(f"Proof lacks a matching claim: {scene}")
    if project["subtitle_safe_height"] < 90:
        errors.append("Subtitle safe area should be at least 90 px for 720p Korean captions.")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Timeline OK: {len(scenes)} scenes, {duration:.2f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--timeline", type=Path, required=True)
    args = parser.parse_args()
    main(args.config, args.timeline)

