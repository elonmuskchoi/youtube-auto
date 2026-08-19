# V9 Longform Master

`V9 Longform Master` is the name of the current 4–5 minute standard production
version. It inherits every approved V7/V8 rule while keeping a full long-form
arc.

## Definition

- Fast real-page motion during the first ten seconds
- Typecast narration as the master clock
- HeyGen Avatar III generated from the final narration WAV
- Verbatim word-timed captions with a clean medium-heavy Korean font
- Real product pages as the main visual layer
- Restrained dynamic presentation graphics for abstract explanations
- Public cases and authorized student proof beside matching claims
- Early expectation CTA and final fixed-comment CTA
- No flashes; occasional slide/push/masked transitions
- BGM and purposeful SFX added only after picture and lip sync are locked
- A fixed lower-right circular avatar

## Current build

The approved 302.565-second master is reduced to approximately 298.08 seconds
by removing one redundant rhetorical sentence at a locked Typecast sentence
boundary. No narration speed change or time stretching is used. A 0.25-second
slide transition and audio crossfade connect the two retained segments.

```powershell
.venv\Scripts\python.exe scripts\build_longform_v9.py
```

Output: `outputs/youtube-auto-v9-longform-master.mp4`
