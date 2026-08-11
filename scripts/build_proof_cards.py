import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1280, 610
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"


def ft(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def render(source: Path, output: Path, label: str, headline: str):
    bg = Image.new("RGB", (W, H), (4, 6, 11)).convert("RGBA")
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow, "RGBA")
    gd.ellipse((470, -330, 1280, 480), fill=(85, 48, 150, 70))
    bg = Image.alpha_composite(bg, glow.filter(ImageFilter.GaussianBlur(90)))
    d = ImageDraw.Draw(bg, "RGBA")
    d.rounded_rectangle((42, 38, 1238, 568), 28, fill=(7, 10, 17, 235), outline=(176, 126, 255, 190), width=2)
    src = Image.open(source).convert("RGB")
    scale = min(650 / src.width, 420 / src.height)
    src = src.resize((int(src.width * scale), int(src.height * scale)), Image.Resampling.LANCZOS)
    d.rounded_rectangle((70, 80, 760, 542), 22, fill=(16, 19, 26), outline=(255, 255, 255, 60), width=2)
    bg.alpha_composite(src.convert("RGBA"), (70 + (690 - src.width) // 2, 80 + (462 - src.height) // 2))
    d.rounded_rectangle((790, 82, 1178, 126), 22, fill=(176, 126, 255, 240))
    d.text((984, 104), label, font=ft(19, "Black"), fill=(5, 8, 12), anchor="mm")
    d.text((790, 186), headline, font=ft(40, "Black"), fill=(250, 249, 245), anchor="la")
    d.text((790, 506), "제공된 실제 인증·후기 자료", font=ft(19, "Medium"), fill=(160, 165, 176), anchor="la")
    d.text((790, 538), "개인별 결과는 실행 방식에 따라 달라질 수 있습니다", font=ft(16, "Medium"), fill=(115, 121, 135), anchor="la")
    bg.convert("RGB").save(output, quality=96)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for index, source in enumerate(sorted(args.input.glob("*.*")), 1):
        if source.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        render(source, args.output / f"proof_{index:02d}.png", "실제 사례", source.stem.replace("_", " "))

