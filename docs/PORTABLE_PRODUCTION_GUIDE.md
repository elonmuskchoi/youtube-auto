# 다른 컴퓨터에서 V10 방식 재현하기

## 1. 저장소 준비

```powershell
git clone https://github.com/elonmuskchoi/youtube-auto.git
cd youtube-auto
git switch codex/environment-setup-20260812
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
Copy-Item .env.example .env
```

FFmpeg를 설치하고 실행 경로를 확인한다. Codex에서는 이 저장소의 `skills/youtube-auto-production/SKILL.md`를 먼저 읽도록 지시한다.

## 2. 비밀값과 개인 자료

`.env`에는 본인이 발급받고 사용 권한이 있는 키만 로컬로 입력한다.

- `TYPECAST_API_KEY`
- `TYPECAST_VOICE_ID` — 필재: `tc_68257f68bc6e3c161ab5078d`
- `HEYGEN_API_KEY`
- `HEYGEN_AVATAR_ID` — 권한이 있는 계정의 아바타 Look ID
- `OPENAI_API_KEY` — GPT Image 2 직접 호출 시에만 필요

공개할 수 없는 수익 인증, 아바타 원본, 음성, 다운로드 영상은 Git에 넣지 않는다. 새 컴퓨터에는 별도의 승인된 비공개 전달 경로로 제공한다.

## 3. 최소 입력

- 영상 주제와 목표 시청자
- 보여줄 최신 URL
- CTA 제공 자료와 고정댓글 문구
- 사용이 허가된 인증자료
- Typecast 음성 및 HeyGen 아바타
- 원하는 길이와 화면비

입력이 빠졌을 때 Codex는 실행을 멈추는 대신 영향이 큰 선택만 2–3개 객관식 추천안으로 제시한다. 비밀값이나 게시 권한은 임의로 가정하지 않는다.

## 4. 복붙용 시작 명령

```text
이 저장소의 skills/youtube-auto-production/SKILL.md를 사용해
한국어 AI 자동화 롱폼 영상 하나를 만들어줘.

목표:
- 조회수 10만+ 영상에서 검증할 수 있는 구조적 패턴만 조사해 적용
- 성공 가능성과 “나도 할 수 있다”는 감정 유지
- Typecast 필재 음성을 먼저 만들고 그 완성 음성을 HeyGen 일반 Avatar III에 입력
- 음성과 동일한 자막을 단어 타이밍 기준으로 동기화
- 실제 웹 화면을 메인으로 사용하고 관련 없는 설명만 동적 PPT 스타일로 표현
- 초반 기대 CTA와 마지막 CTA를 각각 한 번 배치
- 인증자료는 수익·결과 대사 구간에만 사용
- 최종 립싱크 합성 뒤 BGM과 효과음을 믹스
- 썸네일 A/B는 두 개의 서로 다른 가설로 제작

썸네일은 OPENAI_API_KEY가 준비돼 있으면 GPT Image 2를 사용하고,
정확한 프롬프트와 결과 경로를 저장해줘.

진행 전 Git 상태와 브랜치를 확인하고 새 작업 브랜치에서만 변경해.
API 키와 .env, 비공개 원본은 Git에 올리지 마.
진행 중 중요한 선택이 필요하면 2~3개 객관식 추천안을 제시하고
내 선택을 기다려. 게시·배포·유료 생성 직전에는 승인을 받아.
```

## 5. 재현 기준

영상의 “콘셉트”는 재현할 수 있지만 결과물을 바이트 단위로 동일하게 만들 수는 없다. 웹페이지 상태, 생성 모델, 공개 지표, 외부 API 버전이 달라지기 때문이다. 동일하게 유지해야 하는 것은 제작 순서, 음성 기준 싱크, 아바타 배치, 두 CTA, 증거 배치 원칙, 자막 스타일, 화면 우선순위, 오디오 후반 작업, QA 항목이다.

완료 시 사용한 대본, 타이밍 파일, 캡처 날짜, 프롬프트, 설정, 명령, QA 결과, 브랜치와 커밋을 보고한다.
