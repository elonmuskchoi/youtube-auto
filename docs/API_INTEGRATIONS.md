# Voice, image, and avatar integrations

## Credentials

All providers must be configured through environment variables. Never hard-code or commit API keys.

```text
TYPECAST_API_KEY
TYPECAST_VOICE_ID
HEYGEN_API_KEY
HEYGEN_AVATAR_ID
OPENAI_API_KEY
```

## Typecast narration

1. Lock the full script.
2. Generate narration at the target speed, such as `1.15`.
3. Download WAV when possible.
4. Obtain word timestamps from the provider or a local transcription pass.
5. Treat the generated audio as the master duration.

Provider request formats change; consult the current official API documentation before implementation.

## GPT Image visuals

Create premium backgrounds without final Korean typography. Prompt for composition, lighting, palette, subject, negative space, and prohibited items. Add exact Korean text locally using Pillow, Remotion, or another deterministic renderer.

## HeyGen avatar

1. Use the same final narration script as the master voice.
2. Select the desired saved avatar through an environment-configured ID.
3. Use the standard video engine requested by the project.
4. Download the full-length lip-synced video.
5. Mask it to a true circle with alpha.
6. Composite the avatar only after all main visuals and proof clips are locked.

Do not commit the downloaded avatar video. It may include personal likeness and provider-specific licensing restrictions.

