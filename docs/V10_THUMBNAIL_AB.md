# V10 썸네일 A/B

## A — 달성 가능성

- 이미지: `assets/thumbnails/v10-thumbnail-a.png`
- 문구: `AI 플리 / 나도 만들었다`
- 가설: 비전공자도 시작할 수 있다는 감정을 가장 먼저 전달한다.
- 추천 제목: **음악 몰라도 AI 플레이리스트 채널을 시작할 수 있는 이유**

## B — 실행 구조

- 이미지: `assets/thumbnails/v10-thumbnail-b.png`
- 문구: `하루 1시간 / 플리 자동화`
- 가설: 세 단계 자동화 구조와 구체적인 시간 투입을 보여 실행 가능성을 높인다.
- 추천 제목: **하루 1시간, AI 음악 플레이리스트를 쌓는 자동화 순서**

## 권장 우선순위

첫 게시에는 A를 권장한다. V10 대본의 핵심 감정인 “나도 할 수 있다”와 직접 연결되기 때문이다. B는 자동화 방법을 찾는 검색형 시청자에게 더 적합하다.

두 안을 비교할 때 제목은 고정하고 썸네일만 변경한다. 충분한 노출 이후 CTR과 첫 30초 유지율을 함께 본다.

## 재생성 프롬프트

### A

```text
Create a premium 16:9 Korean YouTube thumbnail for an achievable, credible AI music playlist automation video. Dark navy cinematic background, neon violet/cyan AI music workflow and playlist UI on the left, one confident approachable Korean male creator in black on the right, crisp commercial lighting, strong mobile readability. Exact large bold Korean text only: "AI 플리" and "나도 만들었다". White and warm yellow text, no thin outline, no small copy. No logos, watermark, currency, guaranteed-income implication, clutter, misspelled Korean, or distorted hands.
```

### B

```text
Create a premium alternative 16:9 Korean YouTube thumbnail for an achievable AI music playlist automation video. Elegant dark charcoal background, one approachable Korean male creator in black on the left pointing toward a luminous three-step workflow on center-right: AI music note, playlist screen, play window, connected cleanly. Cobalt blue, vivid purple, warm amber accent, polished photorealistic creator plus sophisticated 3D UI graphics, highly readable on mobile. Exact large bold Korean text only: "하루 1시간" and "플리 자동화". White and warm yellow, minimal shadow, no thin outline. No logos, watermark, money piles, guaranteed-income claim, clutter, red arrows, tiny captions, misspelled Korean, or distorted hands.
```

이번 시안은 Codex 내장 이미지 생성으로 제작했다. 다른 환경에서 GPT Image 2를 명시적으로 사용하려면 `OPENAI_API_KEY`를 로컬 환경변수로 설정한 뒤 같은 프롬프트를 전달한다.
