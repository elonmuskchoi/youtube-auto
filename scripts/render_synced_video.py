import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H, FPS = 1280, 720, 24
CONTENT_H = 610
ROOT = Path(__file__).resolve().parents[1]
FONT_REGULAR = Path(__file__).resolve().parents[1] / "work/fonts/Pretendard-Regular.otf"
FONT_SEMIBOLD = Path(__file__).resolve().parents[1] / "work/fonts/Pretendard-SemiBold.otf"
FONT_BOLD = Path(__file__).resolve().parents[1] / "work/fonts/Pretendard-Bold.otf"


def font(size: int, semibold: bool = False, bold: bool = False):
    path = FONT_BOLD if bold and FONT_BOLD.exists() else (FONT_SEMIBOLD if semibold and FONT_SEMIBOLD.exists() else FONT_REGULAR)
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


def slide_frame(name: str, progress: float):
    """Minimal motion-graphic inserts for narration without a matching product screen."""
    dark = name == "rights"
    bg = (10, 16, 28) if dark else (247, 248, 250)
    fg = (247, 249, 253) if dark else (16, 23, 36)
    muted = (170, 181, 200) if dark else (91, 102, 120)
    accent = (77, 125, 255)
    canvas = Image.new("RGB", (W, CONTENT_H), bg)
    draw = ImageDraw.Draw(canvas, "RGBA")
    for x in range(30, W, 34):
        for y in range(28, CONTENT_H, 34):
            draw.ellipse((x, y, x + 2, y + 2), fill=(*muted, 22))
    specs = {
        "hook": ("AI 음악 수익화의 핵심", "음악 한 곡이 아니라\n오래 듣는 구조입니다", ["청취 상황", "콘셉트 통일", "반복 제작"]),
        "system": ("플레이리스트가 오래 재생되는 이유", "사람들은 노래보다\n분위기를 오래 소비합니다", ["집중", "카페", "수면·휴식"]),
        "iterate": ("초보자의 가장 빠른 시작법", "한 가지 상황으로 만들고\n데이터로 다음 영상을 개선", ["첫 영상", "반응 확인", "다음 영상"]),
        "rights": ("자동화 전에 반드시 확인", "빠른 제작보다\n사용 권리와 정책이 먼저입니다", ["상업 이용 조건", "이미지·폰트 라이선스", "반복 콘텐츠 정책"]),
    }
    eyebrow, title, cards = specs[name]
    enter = ease(min(1, progress * 4))
    offset = round(24 * (1 - enter))
    draw.rounded_rectangle((68, 52 + offset, 340, 98 + offset), 22, fill=(*accent, round(255 * enter)))
    draw.text((204, 75 + offset), eyebrow, font=font(19, semibold=True), fill=(255, 255, 255, round(255 * enter)), anchor="mm")
    draw.multiline_text((68, 142 + offset), title, font=font(49, bold=True), fill=(*fg, round(255 * enter)), spacing=8)
    for i, label in enumerate(cards):
        reveal = ease((progress - 0.12 - i * 0.08) * 5)
        x = 68 + i * 305
        y = 402 + round(18 * (1 - reveal))
        fill = (20, 30, 48, round(245 * reveal)) if dark else (255, 255, 255, round(245 * reveal))
        outline = (*accent, round(130 * reveal))
        draw.rounded_rectangle((x, y, x + 282, y + 112), 20, fill=fill, outline=outline, width=2)
        draw.text((x + 25, y + 25), f"0{i + 1}", font=font(18, bold=True), fill=(*accent, round(255 * reveal)))
        draw.text((x + 25, y + 62), label, font=font(22, bold=True), fill=(*fg, round(255 * reveal)))
    return canvas


def montage_frame(images, time: float):
    """Fast opening montage built only from real product-page captures."""
    shots = [
        ("studio", 0.00, 0.30),
        ("studio_playlist", 0.00, 0.24),
        ("studio_playlist", 0.38, 0.62),
        ("product", 0.00, 0.66),
        ("studio_playlist", 0.72, 1.00),
    ]
    shot_duration = 2.0
    index = min(len(shots) - 1, int(time / shot_duration))
    local = (time - index * shot_duration) / shot_duration
    name, start, end = shots[index]
    visual = page_frame(images[name], local, start, end)
    # A small push-in plus a short blue wipe creates pace without hiding the UI.
    zoom = 1.0 + 0.035 * ease(local)
    resized = visual.resize((round(W * zoom), round(CONTENT_H * zoom)), Image.Resampling.LANCZOS)
    left = (resized.width - W) // 2
    top = (resized.height - CONTENT_H) // 2
    visual = resized.crop((left, top, left + W, top + CONTENT_H))
    if local < 0.18 and index > 0:
        # Dark sliding veil instead of a bright flash.
        draw = ImageDraw.Draw(visual, "RGBA")
        wipe = round(W * (1 - ease(local / 0.18)))
        draw.rectangle((0, 0, wipe, CONTENT_H), fill=(8, 13, 23, round(115 * (1 - local / 0.18))))
    return visual


def public_case_frame(image: Image.Image, index: int, progress: float):
    facts = [
        ("달빛라운지", "대표 영상 19만 회", "Nox 월 추정 약 20만 원"),
        ("Hlkyw Music", "대표 영상 2.1만 회", "공개 조회 성과"),
        ("AI K-뮤직", "대표 영상 20만 회", "공개 조회 성과"),
    ]
    channel, views, estimate = facts[index]
    canvas = Image.new("RGB", (W, CONTENT_H), (8, 13, 22))
    draw = ImageDraw.Draw(canvas, "RGBA")
    preview = contain(image).resize((760, 362), Image.Resampling.LANCZOS)
    canvas.paste(preview, (40, 132))
    draw.text((42, 36), "PUBLIC CASE", font=font(18, bold=True), fill=(82, 130, 255))
    draw.text((42, 68), f"공개 플레이리스트 사례 {index + 1}", font=font(31, bold=True), fill=(248, 250, 253))
    draw.rounded_rectangle((825, 92, 1238, 490), 24, fill=(17, 25, 40), outline=(71, 112, 205), width=2)
    draw.text((858, 128), channel, font=font(31, bold=True), fill=(250, 251, 254))
    draw.text((858, 203), views, font=font(25, bold=True), fill=(153, 184, 255))
    draw.text((858, 258), estimate, font=font(23, semibold=True), fill=(231, 236, 246))
    draw.line((858, 316, 1205, 316), fill=(58, 70, 93), width=2)
    draw.text((858, 345), "조회수 · 업로드 · 영상 길이를", font=font(18), fill=(169, 180, 200))
    draw.text((858, 374), "함께 비교하는 참고 사례", font=font(18), fill=(169, 180, 200))
    draw.text((858, 438), "※ 수익 수치는 제3자 추정치", font=font(16), fill=(130, 142, 164))
    return canvas


def student_case_frame(image: Image.Image, index: int, progress: float):
    canvas = Image.new("RGB", (W, CONTENT_H), (9, 13, 22))
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.text((48, 38), f"수강생 운영 사례 {index + 1}", font=font(30, bold=True), fill=(247, 249, 253))
    draw.text((48, 79), "개인정보를 가린 제공 자료 · 개인별 결과는 다를 수 있습니다", font=font(17), fill=(154, 166, 188))
    raw = contain(image)
    raw.thumbnail((650, 425), Image.Resampling.LANCZOS)
    canvas.paste(raw, (45, 125))
    steps = [("01", "기준 설정"), ("02", "반복 실행"), ("03", "결과 기록")]
    for i, (num, label) in enumerate(steps):
        y = 146 + i * 120
        active = i <= min(2, int(progress * 3.2))
        fill = (39, 78, 166) if active else (21, 30, 46)
        draw.rounded_rectangle((755, y, 1218, y + 88), 18, fill=fill, outline=(71, 111, 202), width=2)
        draw.text((785, y + 25), num, font=font(17, bold=True), fill=(128, 166, 255))
        draw.text((845, y + 25), label, font=font(23, bold=True), fill=(245, 248, 253))
    return canvas


def add_page_highlight(visual: Image.Image, time: float, name: str):
    targets = []
    if name == "studio_playlist" and 73 <= time <= 112:
        targets = [(275, 180, 735, 330, "설명 중인 선택 영역")]
    elif name == "product" and 176 <= time <= 198:
        targets = [(75, 165, 555, 360, "자동화 구성 확인")]
    if not targets:
        return visual
    visual = visual.convert("RGBA")
    draw = ImageDraw.Draw(visual, "RGBA")
    for x0, y0, x1, y1, label in targets:
        draw.rounded_rectangle((x0, y0, x1, y1), 18, outline=(91, 139, 255, 225), width=3)
        draw.rounded_rectangle((x0, y0 - 37, x0 + 210, y0 - 8), 14, fill=(42, 83, 185, 225))
        draw.text((x0 + 105, y0 - 23), label, font=font(15, bold=True), fill="white", anchor="mm")
    return visual.convert("RGB")


def kinetic_overlay(draw, time: float):
    phrases = [
        (60.0, 62.2, "같은 품질로 반복"),
        (104.9, 107.3, "상황 + 감정"),
        (160.0, 162.4, "조회수만 보지 않습니다"),
        (238.0, 240.4, "사용 권리 먼저"),
    ]
    for start, end, text in phrases:
        if start <= time <= end:
            p = min(1, (time - start) / 0.3)
            a = round(235 * ease(p))
            draw.rounded_rectangle((380, 42, 900, 111), 22, fill=(8, 13, 23, a))
            draw.text((640, 77), text, font=font(34, bold=True), fill=(255, 255, 255, a), anchor="mm")
            break


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
        (0, 10, "montage", 0.00, 1.00),
        (10, 18, "slide_hook", 0.00, 1.00),
        (18, 43, "studio", 0.00, 0.28),
        (43, 58, "slide_system", 0.00, 1.00),
        (58, 68, "studio_playlist", 0.20, 0.44),
        (20, 43, "studio_playlist", 0.00, 0.20),
        (43, 68, "studio_playlist", 0.20, 0.44),
        (68, 105, "studio_playlist", 0.10, 0.40),
        (105, 140, "studio_playlist", 0.36, 0.64),
        (140, 160, "studio_playlist", 0.60, 0.76),
        (160, 165.3, "public_1", 0, 1),
        (165.3, 170.6, "public_2", 0, 1),
        (170.6, 176, "public_3", 0, 1),
        (176, 198, "product", 0.00, 0.82),
        (198, 204, "student_1", 0, 1),
        (204, 210, "student_2", 0, 1),
        (210, 216, "student_3", 0, 1),
        (216, 222, "community_reviews", 0.00, 0.45),
        (222, 238, "slide_iterate", 0.00, 1.00),
        (238, 253, "slide_rights", 0.00, 1.00),
        (253, 265, "studio_playlist", 0.76, 1.00),
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
        "public_1": Image.open(ROOT / "work/cases/moonlight.png").convert("RGB"),
        "public_2": Image.open(ROOT / "work/cases/hlkyw.png").convert("RGB"),
        "public_3": Image.open(ROOT / "work/cases/aikmusic.png").convert("RGB"),
        "student_1": Image.open(ROOT / "assets/proofs/proof_2600.png").convert("RGB"),
        "student_2": Image.open(ROOT / "assets/proofs/proof_8200.png").convert("RGB"),
        "student_3": Image.open(ROOT / "assets/proofs/proof_continuous.jpg").convert("RGB"),
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
        if name == "montage":
            visual = montage_frame(images, time)
        elif name.startswith("slide_"):
            visual = slide_frame(name.removeprefix("slide_"), progress)
        elif name.startswith("public_"):
            visual = public_case_frame(images[name], int(name[-1]) - 1, progress)
        elif name.startswith("student_"):
            visual = student_case_frame(images[name], int(name[-1]) - 1, progress)
        elif name.startswith("proof"):
            visual = contain(images[name])
        else:
            visual = page_frame(images[name], progress, crop_start, crop_end)
            visual = add_page_highlight(visual, time, name)
        if name != "montage" and progress < 0.065:
            transition = ImageDraw.Draw(visual, "RGBA")
            veil = round(W * (1 - ease(progress / 0.065)))
            transition.rectangle((0, 0, veil, CONTENT_H), fill=(7, 12, 21, round(92 * (1 - progress / 0.065))))
        canvas = Image.new("RGB", (W, H), (5, 7, 12))
        canvas.paste(visual, (0, 0))
        canvas = canvas.convert("RGBA")
        if avatar is not None:
            canvas.alpha_composite(avatar, (1005, 335))
        draw = ImageDraw.Draw(canvas, "RGBA")
        draw.rectangle((0, CONTENT_H, W, H), fill=(3, 5, 10, 248))
        draw.line((0, CONTENT_H, W, CONTENT_H), fill=(52, 60, 78, 255), width=1)
        kinetic_overlay(draw, time)
        text = active_caption(cues, time)
        if text:
            caption_font = font(32, bold=True)
            draw.text((W // 2 + 2, 666 + 3), text, font=caption_font, fill=(0, 0, 0, 150), anchor="mm")
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
