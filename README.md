# youtube-auto

Reusable production kit for Korean long-form YouTube explainers built from real product pages, AI-generated editorial visuals, synchronized captions, proof screenshots, dynamic CTAs, and a circular presenter avatar.

For the current end-to-end method—including the fast opening, synchronized
Typecast/HeyGen Avatar III presenter, evidence scenes, dynamic CTA, final BGM/SFX
mix, A/B thumbnails, and V8 companion edit—start with
[docs/LATEST_WORKFLOW.md](docs/LATEST_WORKFLOW.md). The original locked v3
reproduction specification remains in
[docs/FINAL_V3_RUNBOOK.md](docs/FINAL_V3_RUNBOOK.md). Private media and API keys
are deliberately not stored in Git.

The current release profile is **V10 Positive Playlist Longform**. It uses
Typecast Filjae audio as the master clock, a standard HeyGen Avatar III presenter,
verbatim captions, two CTAs, proof-aligned visuals, and a final BGM/SFX pass. See
[docs/V10_VIDEO_BUILD.md](docs/V10_VIDEO_BUILD.md) and
[docs/PORTABLE_PRODUCTION_GUIDE.md](docs/PORTABLE_PRODUCTION_GUIDE.md).

The current thumbnail pair and reusable prompts are documented in
[docs/V10_THUMBNAIL_AB.md](docs/V10_THUMBNAIL_AB.md).

This repository documents the production method used for a 4 minute 36 second AI-music playlist explainer. It contains no API keys, private testimonials, copyrighted benchmark footage, or final customer media.

## What this pipeline does

- captures real landing and Studio pages;
- opens with a moving page instead of a static slide;
- aligns page demonstrations to narration meaning;
- inserts authorized revenue proof and testimonials near matching claims;
- creates GIF-like CTA motion: scroll deceleration, button pop, cursor movement, click ripple;
- uses AI-generated premium backgrounds while rendering Korean text separately;
- keeps one-line captions in a dedicated 110 px safe area;
- mixes narration and BGM without changing narration timing;
- overlays a lip-synced presenter inside a true circle.

## Recommended environment

- Windows 11
- Python 3.11+
- FFmpeg 7+
- Chromium + Playwright
- Noto Sans KR Variable Font

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
Copy-Item .env.example .env
Copy-Item config\project.example.json config\project.json
```

Add local credentials to `.env`. Never paste credentials into source files.

## Quick workflow

1. Write and lock narration.
2. Generate narration audio and word timings.
3. Capture every page needed by the script.
4. Prepare AI visuals and authorized proof screenshots.
5. Build the timeline manifest.
6. Render the base video with captions and BGM.
7. Add dynamic scroll and CTA clips.
8. Add the circular avatar last.
9. Extract QA frames from every important scene.

See [production guide](docs/PRODUCTION_GUIDE.md) and [timing guide](docs/TIMING_AND_MATCHING.md).

## Commands

```powershell
python scripts/capture_pages.py --config config/pages.example.json
python scripts/build_proof_cards.py --input assets/proofs --output work/proofs
python scripts/render_dynamic_cta.py --input assets/landing/landing-full.png --output work/cta.mp4
python scripts/validate_timeline.py --config config/project.json --timeline config/timeline.example.json
```

Final FFmpeg composition patterns are documented in `docs/FFMPEG_RECIPES.md`.

## Safety and publication

- Blur all personal and financial identifiers in proof images.
- Use only assets you own or have permission to publish.
- Revenue examples are not guarantees; show an appropriate disclaimer.
- Do not commit `.env`, API keys, raw customer files, or generated avatar source videos.
- Rotate any credential that has previously been shared in chat or source code.

## License

MIT for the code and documentation. Input media retains its original ownership and license.

