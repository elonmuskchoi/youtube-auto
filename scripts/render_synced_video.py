import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H, FPS = 1280, 720, 24
CONTENT_H = 610
FONT_REGULAR = Path(__file__).resolve().parents[1] / "work/fonts/Pretendard-Regular.otf"
FONT_SEMIBOLD = Path(__file__).resolve().parents[1] / "work/fonts/Pretendard-SemiBold.otf"


def font(size: int, semibold: bool = False):
    path = FONT_SEMIBOLD if semibold and FONT_SEMIBOLD.exists() else FONT_REGULAR
    if not path.exists():
        path = Path(r"C:\Windows\Fonts\NotoSansKR-VF.ttf")
    return ImageFont.truetype(str(path), size)


def ease(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3 - 2 * value)


def page_frame(image: Image.Image, progress: float, start: float = 0.0, end: float = 1.0):
    page = image.resize((W, round(image.height * W / image.width)), Image.Resampling.LANCZOS)
    max_y = max(0, page.height - CONTENT_H)
    y = round(max_y * (start + (end - start) * ease(progress)))
    return page.crop((0, y, W, y + CONTENT_H)).convert("RGB")


def contain(image: Image.Image):
    scale = min(W / image.width, CONTENT_H / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (W, CONTENT_H), (5, 7, 12))
    canvas.paste(resized, ((W - resized.width) // 2, (CONTENT_H - resized.height) // 2))
    return canvas


def captions(words):
    cues, current = [], []
    for word in words:
        candidate = " ".join(item["text"] for item in current + [word]).strip()
        duration = word["end"] - (current[0]["start"] if current else word["start"])
        if current and (len(candidate) > 22 or duration > 2.65):
            cues.append({"start": current[0]["start"], "end": current[-1]["end"] + 0.08,
                         "text": " ".join(item["text"] for item in current).strip()})
            current = []
        current.append(word)
    if current:
        cues.append({"start": current[0]["start"], "end": current[-1]["end"] + 0.08,
                     "text": " ".join(item["text"] for item in current).strip()})
    return cues


def active_caption(cues, time):
    for cue in cues:
        if cue["start"] <= time <= cue["end"]:
            return cue["text"]
    return ""


def circle_avatar(source: Image.Image, size=230):
    avatar = source.resize((size, size), Image.Resampling.LANCZOS).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((2, 2, size - 3, size - 3), fill=255)
    avatar.putalpha(mask)
    ring = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((2, 2, size - 3, size - 3), outline=(181, 133, 255, 255), width=5)
    return Image.alpha_composite(avatar, ring)


def scene_for(time, duration):
    scenes = [
        (0, 20, "studio", 0.00, 0.28),
        (20, 43, "studio_playlist", 0.00, 0.20),
        (43, 68, "studio_playlist", 0.20, 0.44),
        (68, 105, "studio_playlist", 0.10, 0.40),
        (105, 140, "studio_playlist", 0.36, 0.64),
        (140, 176, "studio_playlist", 0.60, 0.90),
        (176, 198, "product", 0.00, 0.82),
        (198, 207, "proof_1", 0, 1),
        (207, 216, "proof_2", 0, 1),
        (216, 238, "community_reviews", 0.00, 1.00),
        (238, 265, "studio_playlist", 0.76, 1.00),
        (265, 280, "offer", 0.00, 0.90),
        (280, duration, "home", 0.00, 1.00),
    ]
    for start, end, name, crop_start, crop_end in scenes:
        if start <= time < end:
            return start, end, name, crop_start, crop_end
    return scenes[-1]


def main(captures: Path, proofs: Path, avatar_path: Path | None, audio: Path,
         timings_path: Path, output: Path, ffmpeg: Path):
    timing = json.loads(timings_path.read_text(encoding="utf-8"))
    duration = float(timing["audio_duration"])
    cues = captions(timing["words"])
    images = {
        "studio_playlist": Image.open(captures / "studio_playlist.png").convert("RGB"),
        "studio": Image.open(captures / "studio.png").convert("RGB"),
        "product": Image.open(captures / "product.png").convert("RGB"),
        "offer": Image.open(captures / "offer_four_pack.png").convert("RGB"),
        "community_reviews": Image.open(captures / "community_reviews.png").convert("RGB"),
        "home": Image.open(captures / "home.png").convert("RGB"),
        "proof_1": Image.open(proofs / "proof_01.png").convert("RGB"),
        "proof_2": Image.open(proofs / "proof_02.png").convert("RGB"),
    }
    avatar = circle_avatar(Image.open(avatar_path).convert("RGB")) if avatar_path else None
    command = [
        str(ffmpeg), "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(audio),
        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium",
        "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart", str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    for frame_index in range(round(duration * FPS)):
        time = frame_index / FPS
        start, end, name, crop_start, crop_end = scene_for(time, duration)
        progress = (time - start) / max(0.001, end - start)
        if name.startswith("proof"):
            visual = contain(images[name])
        else:
            visual = page_frame(images[name], progress, crop_start, crop_end)
        canvas = Image.new("RGB", (W, H), (5, 7, 12))
        canvas.paste(visual, (0, 0))
        canvas = canvas.convert("RGBA")
        if avatar is not None:
            canvas.alpha_composite(avatar, (1005, 335))
        draw = ImageDraw.Draw(canvas, "RGBA")
        draw.rectangle((0, CONTENT_H, W, H), fill=(3, 5, 10, 248))
        draw.line((0, CONTENT_H, W, CONTENT_H), fill=(52, 60, 78, 255), width=1)
        text = active_caption(cues, time)
        if text:
            caption_font = font(29, semibold=True)
            bounds = draw.textbbox((0, 0), text, font=caption_font)
            box_w = min(W - 80, bounds[2] - bounds[0] + 54)
            box = (W // 2 - box_w // 2, 635, W // 2 + box_w // 2, 697)
            draw.rounded_rectangle(box, 18, fill=(12, 15, 22, 218), outline=(255, 255, 255, 30), width=1)
            draw.text((W // 2, 666), text, font=caption_font, fill=(250, 251, 253, 255), anchor="mm")
        if name.startswith("proof"):
            draw.rounded_rectangle((42, 42, 430, 83), 18, fill=(5, 8, 14, 225), outline=(181, 133, 255, 220), width=2)
            draw.text((236, 62), "제공된 실제 사례 · 개인별 결과 상이", font=font(17), fill=(240, 238, 246), anchor="mm")
        process.stdin.write(canvas.convert("RGB").tobytes())
    process.stdin.close()
    if process.wait():
        raise SystemExit("FFmpeg failed")
    print(f"Rendered {duration:.2f}s with {len(cues)} exact-timing caption cues")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--captures", type=Path, default=Path("assets/landing"))
    parser.add_argument("--proofs", type=Path, default=Path("work/proofs"))
    parser.add_argument("--avatar", type=Path)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--timings", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ffmpeg", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    main(args.captures, args.proofs, args.avatar, args.audio, args.timings,
         args.output, args.ffmpeg)
