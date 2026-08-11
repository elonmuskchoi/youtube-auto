# FFmpeg recipes

## True circular avatar overlay

Prepare an avatar clip with alpha, then overlay it inside a separately designed circular placeholder:

```text
[1:v]scale=230:230[avatar];
[0:v][avatar]overlay=1005:335:eof_action=pass[vout]
```

## Offset a prepared clip on the master timeline

```text
[1:v]setpts=PTS-STARTPTS+91/TB[cta];
[0:v][cta]overlay=0:0:eof_action=pass:repeatlast=0[vout]
```

Pre-render still-image scenes into short clips. This avoids decoding and scaling a large source image for the entire master duration.

## Audio mix

```text
[voice]volume=1[v];
[bgm]volume=0.055,afade=t=in:st=0:d=2[b];
[v][b]amix=inputs=2:duration=first:normalize=0[a]
```

Use the narration stream as the duration authority.

