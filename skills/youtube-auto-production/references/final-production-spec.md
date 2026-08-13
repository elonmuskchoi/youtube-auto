# Final production specification

## Master video

- Canvas: 1280×720, 24 fps, H.264/AAC
- Reference duration: 322.52 seconds; follow the generated master audio for new topics
- Caption safe area: bottom 110 px
- Avatar: fixed lower-right 230×230 circle at x=1005, y=365
- Avatar look: `97d9eddcd53845a6b4e33a8c626665b3`
- Motion engine: HeyGen Avatar III standard/lip-sync unlimited
- Voice order: Typecast final audio → upload audio to HeyGen → avatar render
- Reference narration: `scripts/narration_final_v3.txt`
- Reference timeline: `config/timeline.json`

## Editorial timing

- Opening: begin with actual UI motion, not a static frame
- Early expectation CTA reference window: 43–68 seconds
- Revenue proof reference window: 198–216 seconds
- Final CTA reference window: 280 seconds through the end
- For new narration, relocate these sections by semantic word-timestamp cues rather than copying absolute times

## 100K+ long-form structure

- Verify the public view count immediately before using a reference; record the URL and capture date.
- Thumbnail: one concrete outcome + one mechanism + one curiosity gap, using 2–3 short text blocks. Do not promise guaranteed income.
- 0–5 seconds: state the surprising change or result and show moving proof/UI immediately.
- 5–15 seconds: contrast the old difficulty with the new AI-assisted mechanism.
- 15–30 seconds: preview the three payoffs, show one evidence glimpse, and open a curiosity loop for the final resource CTA.
- Body loop: claim → matching real screen → mechanism → limitation/objection → next question.
- Place public examples before student proof. Label estimates and distinguish general AI-automation outcomes from playlist-only revenue.
- Resolve the early curiosity loop before the final CTA; do not hide the core teaching behind the CTA.

## Motion, captions, and SFX

- Reuse the established house effects: purposeful vertical scroll, cursor movement, selective crop/zoom, browser framing, circular fixed avatar, verbatim word-timed captions, proof reveal, and restrained CTA pop.
- Do not reproduce another creator's exact shot order, graphics, audio, or caption design. Adapt general retention patterns into the existing house style.
- Add SFX only at semantic events: opening impact, UI click, page transition, proof reveal, CTA pop, and final resolve.
- Target SFX peaks roughly 8–14 dB below narration; use short fades and avoid stacking more than two effects.
- Store source URL, creator, license, download date, and required attribution for every external sound. Never commit API keys.

## Visual rules

- Match visible pages to the exact spoken subject.
- Prefer vertical page scrolling, cursor actions, and selective emphasis over continuous full-screen zoom.
- Use current captures from `mcp-auto.dev/studio/pli`, `mcp-auto.dev/studio`, and relevant supporting pages.
- Show authorized revenue proof and the Naver Cafe case only beside matching revenue/result narration.
- Keep the Naver Cafe example in a Mac-style browser frame with a purposeful 5–10 second scroll.
- Keep the circular avatar continuously present at lower-right unless the approved master explicitly changes it.

## Caption rules

- Display the spoken narration verbatim; never summarize it.
- Derive start/end boundaries from the final audio word timestamps.
- Target one line, about 18–22 Korean characters and 2.0–2.7 seconds.
- Add only a 60–100 ms readability tail after the last word.

## CTA materials

- Use an early CTA to build expectation and a final CTA for the fixed-comment action.
- Allow CTA duration to follow narration; retain both a combined master and independently reusable clips.
- Name broadly: 영상 제작 꿀팁 요약본, A–Z 실행 가이드, AI 자동화 수익 자료, 도구·템플릿 모음.
- Preserve supplied GIF/MP4 motion. Use book-cover and resource imagery only while narration explains the provided materials.

## HTML slides

- Use 16:9 scenes, dark navy panels, restrained cyan/violet accents, large Korean typography, and evidence disclaimers.
- Provide Arrow/Page/Space controls, clickable buttons, mobile swipe, progress bar, slide counter, and URL hash state.
- Use reveal/float/pulse transitions and a browser viewport with automatic scrolling.
- Avoid local absolute paths in the deployed file. Use public assets only when licensing and stability are acceptable; otherwise render with HTML/CSS.

## Security and Git

- Required secret names may include `TYPECAST_API_KEY`, `TYPECAST_VOICE_ID`, `HEYGEN_API_KEY`, `HEYGEN_AVATAR_ID`, and `OPENAI_API_KEY`.
- Never store their values in Git, `.env.example`, documentation, screenshots, commands, or logs.
- Generated audio/video/images and private proof are ignored by default. Confirm `.gitignore` before staging.
- Commit on a dedicated branch and push that branch, never silently merge to the default branch.
