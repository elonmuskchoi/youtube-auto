import argparse
import json
import os
from pathlib import Path

import requests


def main(source: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    key = os.environ.get("HEYGEN_API_KEY")
    if not source.is_absolute():
        source = root / source
    if not key:
        raise SystemExit("HEYGEN_API_KEY is missing")
    if not source.exists():
        raise SystemExit(f"Asset file is missing: {source}")
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, required=True)
    args = parser.parse_args()
    main(args.file)
