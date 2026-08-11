import argparse, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 610, 24
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"


def ft(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def clamp(value):
    return max(0.0, min(1.0, value))


def ease(value):
    value = clamp(value)
    return 1 - (1 - value) ** 3


def main(source: Path, output: Path, ffmpeg: str, duration: float, copy: str):
    raw = Image.open(source).convert("RGB")
    page = raw.resize((W, int(raw.height * W / raw.width)), Image.Resampling.LANCZOS)
    command = [ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p", str(output)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    for frame in range(round(FPS * duration)):
        t = frame / FPS
        p = ease(t / max(1, duration * 0.62))
        y = min(int((page.height - H) * 0.58 * p), page.height - H)
        canvas = page.crop((0, y, W, y + H)).convert("RGBA")
        d = ImageDraw.Draw(canvas, "RGBA")
        show = ease((t - 1.2) / 0.7)
        if show:
            pulse = 1 + 0.04 * math.sin((t - 2) * math.pi * 2) * clamp((t - 2) / 0.8) * clamp((7 - t) / 1)
            bw, bh = int(580 * pulse), int(106 * pulse)
            box = (W // 2 - bw // 2, 386 - bh // 2, W // 2 + bw // 2, 386 + bh // 2)
            d.rounded_rectangle(box, 34, fill=(5, 8, 14, int(235 * show)), outline=(55, 235, 158, int(255 * show)), width=4)
            d.text((W // 2, 374), copy, font=ft(38, "Black"), fill=(250, 250, 247, int(255 * show)), anchor="mm")
            d.text((W // 2, 417), "영상 아래 고정 댓글에서 확인", font=ft(18, "Medium"), fill=(55, 235, 158, int(255 * show)), anchor="mm")
            cursor_p = ease((t - 4) / 1.5)
            cx, cy = int(1040 + (735 - 1040) * cursor_p), int(270 + (394 - 270) * cursor_p)
            if 5.55 <= t <= 6.25:
                rp = (t - 5.55) / 0.7
                radius = int(10 + 62 * rp)
                d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=(55, 235, 158, int(210*(1-rp))), width=5)
            d.polygon([(cx,cy),(cx+3,cy+27),(cx+11,cy+19),(cx+21,cy+31),(cx+27,cy+25),(cx+16,cy+14),(cx+28,cy+10)], fill="white", outline="black")
        process.stdin.write(canvas.convert("RGB").tobytes())
    process.stdin.close()
    if process.wait():
        raise SystemExit("FFmpeg failed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--duration", type=float, default=12)
    parser.add_argument("--copy", default="무료 비법서 받아가세요")
    args = parser.parse_args()
    main(args.input, args.output, args.ffmpeg, args.duration, args.copy)

