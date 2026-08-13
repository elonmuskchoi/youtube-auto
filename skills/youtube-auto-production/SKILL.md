---
name: youtube-auto-production
description: Reproduce and extend the youtube-auto final v3 workflow for Korean AI-monetization videos and companion dynamic HTML slide decks. Use when Codex must plan, script, capture web pages, generate Typecast-first narration, create a HeyGen Avatar III presenter from uploaded audio, synchronize verbatim captions, place revenue proof and two CTAs, composite the final video, build interactive slides, or deploy the slides to Vercel without changing the established production style.
---

# YouTube Auto Production

Preserve the repository pipeline. Read `references/final-production-spec.md`, then inspect `docs/FINAL_V3_RUNBOOK.md`, the active timeline, and the relevant scripts before changing or rendering anything.

## Protect the repository and credentials

1. Run `git status --short --branch` before work.
2. Work only on a new or explicitly approved non-default branch.
3. Preserve unrelated user changes and never delete source assets.
4. Keep keys in process environment variables only. Never commit `.env`, tokens, private avatar downloads, proofs, generated audio, or rendered media.
5. Run a secret-pattern scan and inspect `git diff --cached` before every commit.

## Produce a video

1. Confirm the minimum inputs: topic, audience, URLs, CTA offer, fixed-comment wording, authorized proofs, Typecast voice, and HeyGen avatar look.
2. Write a long-form Korean narration matching the established energetic explanatory style. Include an expectation CTA near the opening and a final CTA.
3. Lock the narration before visual editing.
4. Generate the final Typecast Filjae audio first. Preserve word timestamps; treat this audio as the master clock.
5. Upload the completed audio file to HeyGen. Use saved look `97d9eddcd53845a6b4e33a8c626665b3` with standard **Avatar III**, not a premium Avatar IV/V engine. Never create the avatar from pasted narration text.
6. Capture each current webpage for this production. Use real scroll/click movement and do not reuse unrelated old captures.
7. Build the cue-to-visual map from word timestamps. Show proof only during revenue, results, or evidence narration.
8. Keep the moving avatar in a fixed 230×230 circular mask at the lower-right. Keep captions verbatim in the reserved bottom safe area.
9. Preserve GIF and MP4 CTA sources as motion. Use the early expectation CTA and final fixed-comment CTA.
10. Run preflight, render, and inspect representative opening, CTA, proof, Studio, subtitle, and ending frames.

## Build the companion HTML slide deck

1. Summarize the final video into 16:9 slide scenes rather than transcribing every sentence.
2. Preserve the same message order, evidence disclaimers, two-CTA logic, dark navy/cyan/violet visual language, and factual cautions.
3. Implement keyboard, button, swipe, progress, hash navigation, reveal motion, and purposeful browser-scroll animation.
4. Prefer a self-contained deployable HTML file. Do not embed secrets, private proofs, or local absolute paths.
5. Keep source in `slides/`, build to `slides/dist/`, and verify slide count, Korean encoding, local asset references, mobile behavior, and browser console errors.
6. Deploy only after the user authorizes publication. Use the connected Vercel account and return the production URL plus the local deliverable.

## Keep claims honest

- Treat public channel revenue as a third-party estimate, never an actual settlement figure.
- State that results vary and monetization is not guaranteed.
- Verify time-sensitive channel metrics immediately before use.
- Blur or omit personal identifiers in authorized proof.

## Hand off reproducibly

Report the narration, timing source, avatar engine/look, input paths, render command, output paths, QA result, remaining private inputs, deployed URL, branch, commit, and push result. Update the runbook when the approved workflow changes.
