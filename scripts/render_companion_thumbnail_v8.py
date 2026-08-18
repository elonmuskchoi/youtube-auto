from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
FONT_BOLD = ROOT / "work/fonts/Pretendard-Bold.otf"
FONT_SEMIBOLD = ROOT / "work/fonts/Pretendard-SemiBold.otf"


def font(size, bold=True):
    path = FONT_BOLD if bold else FONT_SEMIBOLD
    return ImageFont.truetype(str(path), size)


def cover(image, box):
    x0, y0, x1, y1 = box
    scale = max((x1 - x0) / image.width, (y1 - y0) / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (image.width - (x1 - x0)) // 2
    top = (image.height - (y1 - y0)) // 2
    return image.crop((left, top, left + x1 - x0, top + y1 - y0))


def make(line1, line2, badge, output):
    sources = [Image.open(ROOT / f"work/cases/{name}.png").convert("RGB") for name in ("moonlight", "hlkyw", "aikmusic")]
    canvas = Image.new("RGB", (1280, 720), (5, 9, 17))
    boxes = [(610, 40, 930, 360), (930, 40, 1250, 360), (770, 360, 1250, 690)]
    for source, box in zip(sources, boxes):
        shot = cover(source, box).filter(ImageFilter.GaussianBlur(0.35))
        canvas.paste(shot, box[:2])
    canvas = ImageEnhance.Contrast(canvas).enhance(1.12)
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    for x in range(0, 900):
        a = round(242 - 145 * (x / 900))
        draw.line((x, 0, x, 720), fill=(4, 10, 22, a))
    draw.rounded_rectangle((48, 48, 410, 106), 20, fill=(65, 117, 245, 245))
    draw.text((229, 77), badge, font=font(25, False), fill="white", anchor="mm")
    draw.text((50, 155), line1, font=font(80), fill="white", stroke_width=4, stroke_fill=(3, 7, 15))
    draw.text((50, 265), line2, font=font(104), fill=(255, 222, 72), stroke_width=5, stroke_fill=(3, 7, 15))
    draw.rounded_rectangle((50, 455, 570, 526), 18, fill=(13, 23, 41, 230), outline=(102, 143, 255), width=2)
    draw.text((310, 491), "조회수 · 실제 화면 · 추정치", font=font(28, False), fill=(231, 237, 249), anchor="mm")
    avatar = Image.open(ROOT / "work/ai-builder-circle.png").convert("RGBA").resize((280, 280), Image.Resampling.LANCZOS)
    overlay.alpha_composite(avatar, (955, 420))
    result = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
    result.save(output, quality=95)
    print(output)


def main():
    OUT.mkdir(exist_ok=True)
    make("AI 플리", "실제 사례 3개", "공개 채널로 검증", OUT / "youtube-companion-v8-thumbnail-a.png")
    make("AI 음악 한 곡으론", "안 됩니다", "수익화 구조의 차이", OUT / "youtube-companion-v8-thumbnail-b.png")


if __name__ == "__main__":
    main()
