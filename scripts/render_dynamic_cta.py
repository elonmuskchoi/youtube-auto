import argparse
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H, FPS = 1280, 610, 24
ROOT = Path(__file__).resolve().parents[1]
REGULAR = ROOT / "work/fonts/Pretendard-Regular.otf"
SEMIBOLD = ROOT / "work/fonts/Pretendard-SemiBold.otf"
BOLD = ROOT / "work/fonts/Pretendard-Bold.otf"


def ft(size, weight="regular"):
    path = {"regular": REGULAR, "semibold": SEMIBOLD, "bold": BOLD}[weight]
    if not path.exists():
        path = Path(r"C:\Windows\Fonts\NotoSansKR-VF.ttf")
    return ImageFont.truetype(str(path), size)


def clamp(value):
    return max(0.0, min(1.0, value))


def ease(value):
    value = clamp(value)
    return value * value * (3 - 2 * value)


def alpha(t, start, duration=0.55):
    return round(255 * ease((t - start) / duration))


def draw_grid(draw):
    for x in range(30, W, 32):
        for y in range(26, H, 32):
            draw.ellipse((x, y, x + 2, y + 2), fill=(26, 35, 52, 18))


def phase_resources(t):
    canvas = Image.new("RGBA", (W, H), (246, 247, 249, 255))
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw_grid(draw)
    a = alpha(t, 0.15)
    draw.rounded_rectangle((72, 54, 255, 96), 20, fill=(30, 42, 62, a))
    draw.text((163, 75), "무료 자료 3종", font=ft(21, "semibold"), fill=(255, 255, 255, a), anchor="mm")
    draw.text((72, 128), "처음부터 헤매지 않도록", font=ft(37, "semibold"), fill=(55, 65, 82, a))
    draw.text((72, 178), "실행 순서만 정리했습니다", font=ft(54, "bold"), fill=(15, 22, 34, a))
    labels = [
        ("01", "영상 꿀팁 요약", "핵심만 빠르게 확인"),
        ("02", "A–Z 실행 가이드", "처음부터 업로드까지"),
        ("03", "AI 자동화 수익 자료", "여러 영상 주제에 활용"),
    ]
    for i, (num, title, body) in enumerate(labels):
        start = 0.8 + i * 0.22
        card_a = alpha(t, start)
        y = 282
        x = 72 + i * 390
        lift = round(18 * (1 - ease((t - start) / 0.55)))
        draw.rounded_rectangle((x, y + lift, x + 354, y + 190 + lift), 24,
                               fill=(255, 255, 255, card_a), outline=(203, 209, 219, card_a), width=2)
        draw.text((x + 26, y + 26 + lift), num, font=ft(22, "bold"), fill=(39, 103, 235, card_a))
        draw.text((x + 26, y + 77 + lift), title, font=ft(30, "bold"), fill=(18, 25, 38, card_a))
        draw.text((x + 26, y + 128 + lift), body, font=ft(20), fill=(95, 104, 120, card_a))
    return canvas


def phase_action(t):
    canvas = Image.new("RGBA", (W, H), (15, 22, 34, 255))
    draw = ImageDraw.Draw(canvas, "RGBA")
    a = alpha(t, 16.6)
    draw.rounded_rectangle((510, 68, 770, 112), 22, fill=(68, 117, 245, a))
    draw.text((640, 90), "NEXT STEP", font=ft(19, "bold"), fill=(255, 255, 255, a), anchor="mm")
    draw.text((640, 190), "영상 아래 고정댓글에서", font=ft(42, "semibold"), fill=(202, 209, 221, a), anchor="mm")
    draw.text((640, 258), "무료 자료를 확인하세요", font=ft(58, "bold"), fill=(255, 255, 255, a), anchor="mm")
    draw.rounded_rectangle((405, 344, 875, 430), 25, fill=(68, 117, 245, a))
    draw.text((640, 387), "요약본 · A–Z 가이드 · 자동화 자료", font=ft(26, "semibold"), fill=(255, 255, 255, a), anchor="mm")
    arrow_y = 478 + round(8 * ease((t % 1.2) / 1.2))
    draw.line((640, arrow_y, 640, arrow_y + 40), fill=(130, 164, 255, a), width=6)
    draw.polygon([(626, arrow_y + 30), (654, arrow_y + 30), (640, arrow_y + 48)], fill=(130, 164, 255, a))
    draw.text((640, 562), "지금 바로 확인해보세요", font=ft(22), fill=(169, 178, 194, a), anchor="mm")
    return canvas


def main(source: Path, output: Path, ffmpeg: str, duration: float, copy: str):
    command = [ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
               "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18",
               "-pix_fmt", "yuv420p", str(output)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    for frame in range(round(FPS * duration)):
        t = frame / FPS
        canvas = phase_resources(t) if t < 16.5 else phase_action(t)
        process.stdin.write(canvas.convert("RGB").tobytes())
    process.stdin.close()
    if process.wait():
        raise SystemExit("FFmpeg failed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--duration", type=float, default=26)
    parser.add_argument("--copy", default="무료 자료 확인하기")
    args = parser.parse_args()
    main(args.input, args.output, args.ffmpeg, args.duration, args.copy)

