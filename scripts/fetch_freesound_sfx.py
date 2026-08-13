import json
import os
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "work" / "sfx"
API = "https://freesound.org/apiv2/search/text/"
QUERIES = {
    "cinematic-impact.mp3": "cinematic impact short",
    "soft-whoosh.mp3": "soft whoosh transition",
    "ui-click.mp3": "soft ui click",
    "soft-pop.mp3": "soft pop notification",
    "success-chime.mp3": "short success chime",
    "page-swipe.mp3": "page swipe short",
}


def request_json(url, key):
    req = urllib.request.Request(url, headers={"Authorization": f"Token {key}"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def download(url, target):
    with urllib.request.urlopen(url, timeout=60) as response:
        target.write_bytes(response.read())


def main():
    key = os.environ.get("FREESOUND_API_KEY")
    if not key:
        raise SystemExit("FREESOUND_API_KEY 환경변수가 필요합니다.")

    DEST.mkdir(parents=True, exist_ok=True)
    manifest = []
    for filename, query in QUERIES.items():
        params = urllib.parse.urlencode({
            "query": query,
            "filter": 'duration:[0.05 TO 4] license:"Creative Commons 0"',
            "fields": "id,name,username,license,url,previews,duration",
            "page_size": 15,
        })
        data = request_json(f"{API}?{params}", key)
        results = data.get("results", [])
        if not results:
            raise RuntimeError(f"검색 결과 없음: {query}")
        item = min(results, key=lambda row: abs(float(row.get("duration", 1)) - 0.8))
        preview = item.get("previews", {}).get("preview-hq-mp3") or item.get("previews", {}).get("preview-lq-mp3")
        if not preview:
            raise RuntimeError(f"미리듣기 URL 없음: {item.get('id')}")
        download(preview, DEST / filename)
        manifest.append({
            "file": filename,
            "id": item["id"],
            "name": item["name"],
            "creator": item["username"],
            "license": item["license"],
            "source": item["url"],
            "duration": item["duration"],
        })

    (DEST / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Downloaded {len(manifest)} CC0 effects to {DEST}")


if __name__ == "__main__":
    main()

