# Latest production workflow

This is the source of truth for the latest `youtube-auto` production method. It
extends the locked Typecast/HeyGen v3 workflow with the V4/V7 retention edit and
the V8 public-case companion package.

## Creative rules

- The narration is the master clock. Generate Typecast audio first, then upload
  that exact audio to HeyGen; never create the avatar from pasted script text.
- Use avatar look `97d9eddcd53845a6b4e33a8c626665b3` with the regular Avatar III
  engine. Composite it as a fixed lower-right circle.
- Captions reproduce the spoken narration verbatim and use word timings from
  the generated voice. Use a clean, medium-heavy Korean font without an
  outlined/stroked appearance.
- Make the first ten seconds a fast sequence of real page motion, scrolls, and
  short transitions. Do not open on a static presentation slide.
- Real product pages remain the primary visual layer. Use restrained dynamic
  presentation graphics only where there is no relevant page to demonstrate.
- Avoid flashes and repetitive blinking. Use occasional slide, push, masked
  reveal, and audio-supported transitions.
- Show revenue proof only during matching revenue or results narration. Retain
  the original evidence inside a browser/device frame and add a disclaimer.
- Use an expectation CTA early and a final fixed-comment CTA. Preserve the
  supplied GIF/MP4 motion assets; do not replace them with static screenshots.
- Add BGM and SFX only after the full HeyGen/Typecast visual sync is locked.

## Private inputs

The repository intentionally excludes `.env`, raw narration, avatar renders,
proof screenshots, captured pages, downloaded sound effects, and final MP4s.
Put local assets at the paths declared in `config/final-v4-inputs.json` and run
the preflight before rendering. Credentials belong in process environment
variables and must never be committed.

## Full production order

1. Write and lock the long-form narration. Use the hook and retention findings
   in `docs/LONGFORM_REFERENCE_ANALYSIS.md` and the scene language in
   `docs/MAKER_EVAN_BENCHMARK.md`.
2. Generate the Typecast voice and word timing JSON.
3. Upload the final WAV to HeyGen, select Avatar III and the approved look, and
   render the full-length lip-synced presenter.
4. Capture every current product page with Playwright. Never reuse captures
   from an unrelated production.
5. Prepare authorized public cases and student proof. Redact personal data and
   label third-party revenue estimates as estimates.
6. Build CTA motion modules from the supplied GIF/MP4 sources.
7. Render the synced base composition with real pages, semantic screen matching,
   captions, evidence, and the fixed circular avatar.
8. Add the fast opening montage, restrained transitions, section highlights,
   and dynamic presentation inserts.
9. Mix BGM and frequent but purposeful SFX after picture and lip sync are final.
10. Render A/B thumbnails, extract QA frames, inspect scene boundaries, and run
    loudness/media validation.

## Commands

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium

python scripts\capture_pages.py --config config\pages.json
python scripts\generate_typecast_long_audio.py `
  --script scripts\narration_final_v4.txt `
  --audio audio\narration-final-v4-long.wav `
  --timings audio\word-timings-final-v4-long.json `
  --voice-id '<Typecast Filjae voice ID>'

powershell -ExecutionPolicy Bypass -File scripts\preflight_final_v3.ps1
powershell -ExecutionPolicy Bypass -File scripts\build_final_v4.ps1
python scripts\mix_master_v4.py
python scripts\render_thumbnail_v4.py
```

The render and mix scripts are direct build commands, not CLI wrappers; do not
append `--help` because execution starts immediately and overwrites the named
Git-ignored output with a newly rendered copy.

Use `config/sfx_cues_v4.json` to revise SFX positions without changing the
locked edit. `scripts/fetch_freesound_sfx.py` downloads permitted sounds to a
Git-ignored local directory; verify every sound's license before publication.

## V8 companion video

After the approved full master exists at
`outputs/youtube-auto-final-v4-avatar3-bgm-sfx.mp4`, create the evidence-focused
companion and its thumbnail alternatives:

```powershell
python scripts\build_companion_v8.py
python scripts\render_companion_thumbnail_v8.py
```

The companion is a sentence-boundary recut of the approved synchronized master,
so it does not consume additional Typecast or HeyGen credits. Its editorial
package is documented in `docs/COMPANION_V8_PACKAGE.md`.

## Publication QA

- Confirm H.264/AAC output, 1280x720 canvas, and expected duration.
- Check lip sync and caption onset at the opening, every edit boundary, both
  CTA sections, and the ending.
- Confirm no proof appears beside unrelated narration and no identifier remains
  readable in student material.
- Listen for SFX collisions and ensure narration remains intelligible over BGM.
- Verify thumbnail readability at mobile size and use an evidence-oriented title
  without guaranteeing revenue.
- Run `git diff --check` and scan tracked files for credential patterns before
  every push.

## Minimum inputs for another topic

- Topic, target viewer, and desired running time
- Final product/page URLs
- CTA offer and fixed-comment wording
- Authorized evidence relevant to that topic
- Approved avatar look and Typecast voice
- Supplied GIF/MP4 CTA materials
- Claims, disclaimers, and prohibited wording

Keep this structure unchanged unless a production-method change is explicitly
approved.
