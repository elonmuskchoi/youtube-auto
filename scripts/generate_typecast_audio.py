import argparse
import base64
import json
import os
from pathlib import Path

import requests


def main(script: Path, audio: Path, timings: Path, voice_id: str):
    api_key = os.environ.get("TYPECAST_API_KEY")
    if not api_key:
        raise SystemExit("TYPECAST_API_KEY is required in the process environment.")
    text = script.read_text(encoding="utf-8").strip()
    if not 1 <= len(text) <= 2000:
        raise SystemExit(f"Typecast text must be 1-2000 characters; got {len(text)}.")
    response = requests.post(
        "https://api.typecast.ai/v1/text-to-speech/with-timestamps?granularity=word",
        headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
        json={
            "voice_id": voice_id,
            "text": text,
            "model": "ssfm-v30",
            "language": "kor",
            "prompt": {
                "emotion_type": "preset",
                "emotion_preset": "toneup",
                "emotion_intensity": 0.75,
            },
            "output": {
                "volume": 100,
                "audio_pitch": 0,
                "audio_tempo": 1.15,
                "audio_format": "wav",
            },
            "seed": 42,
        },
        timeout=180,
    )
    response.raise_for_status()
    result = response.json()
    audio.parent.mkdir(parents=True, exist_ok=True)
    audio.write_bytes(base64.b64decode(result["audio"]))
    timings.write_text(
        json.dumps(
            {
                "audio_duration": result["audio_duration"],
                "audio_format": result["audio_format"],
                "words": result["words"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Generated {result['audio_duration']:.2f}s with {len(result['words'])} timing segments")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", type=Path, required=True)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--timings", type=Path, required=True)
    parser.add_argument("--voice-id", required=True)
    args = parser.parse_args()
    main(args.script, args.audio, args.timings, args.voice_id)
