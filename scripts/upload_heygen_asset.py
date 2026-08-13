import json
import os
from pathlib import Path

import requests


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    key = os.environ.get("HEYGEN_API_KEY")
    source = root / "audio" / "narration-case-upgrade.wav"
    if not key:
        raise SystemExit("HEYGEN_API_KEY is missing")
    with source.open("rb") as handle:
        response = requests.post(
            "https://api.heygen.com/v3/assets",
            headers={"X-Api-Key": key},
            files={"file": (source.name, handle, "audio/wav")},
            timeout=300,
        )
    response.raise_for_status()
    payload = response.json()
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
