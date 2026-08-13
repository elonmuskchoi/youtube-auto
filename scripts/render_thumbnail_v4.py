from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/youtube-thumbnail-v4.png"
FONT = Path("C:/Windows/Fonts/malgunbd.ttf")


def fit_text(draw, text, max_width, start_size):
    size = start_size
    while size > 30:
        font = ImageFont.truetype(str(FONT), size)
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(str(FONT), size)


def main():
    source = Image.open(ROOT / "assets/landing/studio_playlist.png").convert("RGB")
    scale = max(1280 / source.width, 720 / source.height)
    source = source.resize((round(source.width * scale), round(source.height * scale)), Image.Resampling.LANCZOS)
    left = (source.width - 1280) // 2
    image = source.crop((left, 0, left + 1280, 720)).filter(ImageFilter.GaussianBlur(1.2))
    image = ImageEnhance.Contrast(image).enhance(1.15)

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(800):
        alpha = int(225 * (1 - x / 800) + 25 * (x / 800))
        draw.line((x, 0, x, 720), fill=(5, 13, 28, alpha))
    draw.rounded_rectangle((52, 48, 390, 105), 18, fill=(33, 232, 190, 235))
    badge = ImageFont.truetype(str(FONT), 29)
    draw.text((74, 61), "실제 채널·수강생 사례", font=badge, fill=(5, 20, 31, 255))

    main_font = fit_text(draw, "음악 몰라도", 700, 108)
    main2_font = fit_text(draw, "됩니다", 700, 124)
    sub_font = ImageFont.truetype(str(FONT), 52)
    draw.text((54, 145), "음악 몰라도", font=main_font, fill="white", stroke_width=5, stroke_fill=(3, 8, 20, 255))
    draw.text((54, 275), "됩니다", font=main2_font, fill=(255, 229, 74, 255), stroke_width=5, stroke_fill=(3, 8, 20, 255))
    draw.rounded_rectangle((54, 466, 572, 550), 18, fill=(37, 94, 255, 235))
    draw.text((82, 480), "AI 플리 자동화", font=sub_font, fill="white")

    avatar = Image.open(ROOT / "work/ai-builder-circle.png").convert("RGBA").resize((330, 330), Image.Resampling.LANCZOS)
    overlay.alpha_composite(avatar, (900, 350))
    image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT, quality=95)
    print(OUT)


if __name__ == "__main__":
    main()

