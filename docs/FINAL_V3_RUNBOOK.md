# Final v3 reproduction runbook

This document is the source of truth for reproducing the 2026-08-12 23:08 KST video style.

## Non-negotiable production rules

- Lock the narration before editing visuals.
- Generate the Typecast Filjae voice first and retain its word timestamps.
- Upload that completed WAV to HeyGen. Do not generate the avatar from pasted script text.
- Select private look `97d9eddcd53845a6b4e33a8c626665b3` and motion engine **Avatar III** (`lip-sync, unlimited`). Do not use Avatar IV/V premium engines.
- Keep narration and subtitles verbatim. Subtitle boundaries come from Typecast word timestamps.
- Keep the circular moving avatar fixed at the lower-right. Do not make it appear intermittently.
- Prefer page scrolling and purposeful movement over a continuous full-frame zoom.
- Match the visible page to the sentence being spoken.
- Show authorized proof only while the narration discusses revenue, results, or proof.
- Use the early expectation CTA and the final fixed-comment CTA. Preserve GIF/MP4 motion.
- Never reuse screenshots from an unrelated previous production.

## Final v3 master specification

- Duration: 322.52 seconds
- Canvas: 1280x720, 24 fps, H.264/AAC
- Caption safe area: bottom 110 px
- Early CTA: 43.00-68.00
- Revenue proof: 198.00-216.00
- Final CTA: 280.00-322.52
- Avatar: 230x230 circle, x=1005, y=365
- Narration: `scripts/narration_final_v3.txt`
- Timeline: `config/timeline.json`

## Private inputs

Private and large files are intentionally excluded from Git. Place them at the paths listed in `config/final-v3-inputs.json`. Run `scripts/preflight_final_v3.ps1` before rendering. It reports missing files and validates reference hashes when provided.

API keys must be process environment variables only:

```powershell
$env:TYPECAST_API_KEY = '<value supplied privately>'
```

Do not put keys in `.env`, source code, JSON, shell history committed to Git, or screenshots.

## Reproduction sequence

1. Create and activate `.venv`; install `requirements.txt` and Playwright Chromium.
2. Capture every current page using `config/pages.json` and `scripts/capture_pages.py`.
3. Generate `audio/narration-long-v3.wav` and `audio/word-timings-long-v3.json` from the final narration:

```powershell
python scripts/generate_typecast_long_audio.py `
  --script scripts/narration_final_v3.txt `
  --audio audio/narration-long-v3.wav `
  --timings audio/word-timings-long-v3.json `
  --voice-id '<Filjae voice ID>'
```

4. In HeyGen, upload the WAV, select the exact look ID, choose Avatar III, render 1080p MP4, and save the complete file as `work/heygen-avatar-iii-typecast-v3-full.mp4`.
5. Put authorized proof sources in `assets/proofs`, build privacy-safe cards, and visually inspect every identifier.
6. Put the approved moving CTA master at `outputs/cta-dynamic-master.mp4`.
7. Run the preflight and final build:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/preflight_final_v3.ps1
powershell -ExecutionPolicy Bypass -File scripts/build_final_v3.ps1
```

8. Verify duration, 7,740 video frames, subtitle/audio sync, both CTA sections, both proof sections, and avatar presence near the beginning, middle, and end.

## Minimum input for a new topic

- Topic and target audience
- Main product/page URLs
- CTA offer and fixed-comment destination wording
- Authorized proof files for that topic
- Approved avatar look and Typecast voice
- Any product claims that must or must not be made

Keep the pipeline and layout unchanged unless the user explicitly approves a production-method change.
