# Timing and content matching

## Priority scores

| Priority | Method | Score |
|---:|---|---:|
| 1 | Word-timestamp-based visual matching | 98 |
| 2 | Actual page scroll and click capture | 95 |
| 3 | Evidence immediately after matching claims | 93 |
| 4 | CTA motion tied to the real landing page | 91 |
| 5 | Premium AI visuals for abstract concepts | 88 |
| 6 | Sequential animation inside each scene | 86 |
| 7 | Fixed caption safe area | 84 |
| 8 | Music-beat-based transitions | 72 |

## Matching table

For every narration cue, record:

| Field | Example |
|---|---|
| Spoken phrase | "곡과 커버를 한 번에 만듭니다" |
| Start/end | `64.2–68.8` |
| Visual source | Studio playlist page |
| Visual action | category select → cover preview |
| Evidence | none |
| CTA | none |

Only use proof when the narration mentions results, revenue, users, or success. Only use CTA when the narration tells the viewer what they can receive or where to act.

## Caption generation

Group word timestamps until either:

- the line exceeds about 22 Korean characters;
- the duration exceeds 2.65 seconds; or
- punctuation closes the thought.

The caption start should equal the first word start. The caption end should equal the final word end plus a small 60–100 ms readability tail.

