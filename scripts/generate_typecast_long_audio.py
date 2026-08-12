import argparse
import base64
import io
import json
import os
import wave
from pathlib import Path

import requests


def chunks(text: str, limit: int = 1800):
    result, current = [], ""
    for paragraph in [p.strip() for p in text.split("\n\n") if p.strip()]:
        candidate = f"{current}\n\n{paragraph}".strip()
        if current and len(candidate) > limit:
            result.append(current)
            current = paragraph
        else:
            current = candidate
    if current:
        result.append(current)
    return result


def main(script: Path, audio: Path, timings: Path, voice_id: str):
    key = os.environ.get("TYPECAST_API_KEY")
    if not key:
        raise SystemExit("TYPECAST_API_KEY is required in the process environment.")
    parts = chunks(script.read_text(encoding="utf-8").strip())
    pcm_parts, words, offset = [], [], 0.0
    params = None
    for index, text in enumerate(parts, 1):
        response = requests.post(
            "https://api.typecast.ai/v1/text-to-speech/with-timestamps?granularity=word",
            headers={"X-API-KEY": key, "Content-Type": "application/json"},
            json={
                "voice_id": voice_id, "text": text, "model": "ssfm-v30", "language": "kor",
                "prompt": {"emotion_type": "preset", "emotion_preset": "toneup", "emotion_intensity": 0.75},
                "output": {"volume": 100, "audio_pitch": 0, "audio_tempo": 1.15, "audio_format": "wav"},
                "seed": 42 + index,
            }, timeout=240,
        )
        response.raise_for_status()
        data = response.json()
        with wave.open(io.BytesIO(base64.b64decode(data["audio"])), "rb") as wav:
            current_params = (wav.getnchannels(), wav.getsampwidth(), wav.getframerate())
            if params and current_params != params:
                raise SystemExit("Typecast chunks returned incompatible WAV formats")
            params = current_params
            pcm_parts.append(wav.readframes(wav.getnframes()))
        for word in data["words"]:
            words.append({**word, "start": word["start"] + offset, "end": word["end"] + offset})
        offset += float(data["audio_duration"])
        print(f"Chunk {index}/{len(parts)}: {data['audio_duration']:.2f}s")
    audio.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(audio), "wb") as out:
        out.setnchannels(params[0]); out.setsampwidth(params[1]); out.setframerate(params[2])
        for pcm in pcm_parts:
            out.writeframes(pcm)
    timings.write_text(json.dumps({"audio_duration": offset, "audio_format": "wav", "words": words}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {offset:.2f}s with {len(words)} timing segments across {len(parts)} chunks")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", type=Path, required=True)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--timings", type=Path, required=True)
    parser.add_argument("--voice-id", required=True)
    args = parser.parse_args()
    main(args.script, args.audio, args.timings, args.voice_id)
