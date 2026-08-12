import argparse
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H, FPS = 1280, 720, 24
CONTENT_H = 610
FONT = Path(r"C:\Windows\Fonts\NotoSansKR-VF.ttf")


def ease(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3 - 2 * value)


def font(size: int):
    return ImageFont.truetype(str(FONT), size)


def scroll_frame(image: Image.Image, progress: float) -> Image.Image:
    page = image.resize((W, round(image.height * W / image.width)), Image.Resampling.LANCZOS)
    max_y = max(0, page.height - CONTENT_H)
    y = round(max_y * ease(progress))
    return page.crop((0, y, W, y + CONTENT_H))


def add_caption_area(frame: Image.Image, label: str) -> Image.Image:
    canvas = Image.new("RGB", (W, H), (5, 7, 12))
    canvas.paste(frame, (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.line((0, CONTENT_H, W, CONTENT_H), fill=(47, 54, 70), width=1)
    draw.text((W // 2, 665), label, font=font(26), fill=(235, 238, 245), anchor="mm")
    return canvas


def main(captures: Path, output: Path, ffmpeg: Path):
    scenes = [
        ("studio_playlist.png", 13.0, "상황을 고르면 플레이리스트 제작 흐름이 완성됩니다"),
        ("studio.png", 11.0, "전체 제작실에서 필요한 자동화 도구를 확인합니다"),
        ("product.png", 6.0, "제품 구성과 제공 기능을 실제 화면으로 살펴봅니다"),
        ("offer_four_pack.png", 6.0, "필요한 제작 패키지와 혜택을 확인합니다"),
        ("community_reviews.png", 5.0, "관련 후기와 커뮤니티 자료를 이어서 확인합니다"),
        ("home.png", 7.0, "마지막 안내와 다음 행동 화면으로 연결합니다"),
    ]
    command = [
        str(ffmpeg), "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    for filename, duration, label in scenes:
        image = Image.open(captures / filename).convert("RGB")
        frame_count = round(duration * FPS)
        for index in range(frame_count):
            progress = index / max(1, frame_count - 1)
            frame = add_caption_area(scroll_frame(image, progress), label)
            process.stdin.write(frame.tobytes())
    process.stdin.close()
    if process.wait():
        raise SystemExit("FFmpeg failed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--captures", type=Path, default=Path("assets/landing"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ffmpeg", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    main(args.captures, args.output, args.ffmpeg)
