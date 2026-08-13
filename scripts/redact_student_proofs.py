from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "proofs"
OUTPUT = ROOT / "slides" / "assets"
FONT = r"C:\Windows\Fonts\malgunbd.ttf"


def cover(image: Image.Image, box: tuple[int, int, int, int], label: str = "금액 비공개") -> None:
    draw = ImageDraw.Draw(image)
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=max(6, (y1 - y0) // 6), fill=(24, 31, 43))
    font = ImageFont.truetype(FONT, max(12, int((y1 - y0) * 0.28)))
    draw.text(((x0 + x1) // 2, (y0 + y1) // 2), label, font=font, fill="white", anchor="mm")


def save(source: str, target: str, boxes: list[tuple[int, int, int, int]]) -> None:
    image = Image.open(SOURCE / source).convert("RGB")
    for box in boxes:
        cover(image, box)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT / target, "WEBP", quality=88, method=6)


save("proof_8200.png", "student-proof-a.webp", [(105, 88, 420, 168)])
save("proof_2600.png", "student-proof-b.webp", [(85, 75, 350, 143)])
save(
    "proof_continuous.jpg",
    "student-proof-c.webp",
    [(12, 150, 310, 245), (12, 402, 310, 497), (12, 650, 310, 755)],
)
