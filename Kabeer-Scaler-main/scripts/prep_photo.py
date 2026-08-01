from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / "images"
OUTPUT = IMAGES_DIR / "source-prepped.png"


def find_source_image() -> Path:
    candidates = sorted(IMAGES_DIR.glob("*.png")) + sorted(IMAGES_DIR.glob("*.jpg")) + sorted(IMAGES_DIR.glob("*.jpeg"))
    if not candidates:
        raise FileNotFoundError("No supported image found in images/.")
    return candidates[0]


def main() -> None:
    source = find_source_image()
    image = Image.open(source).convert("RGB")
    image = ImageOps.fit(image, (640, 640), method=Image.Resampling.LANCZOS)
    image = ImageOps.grayscale(image)
    image = ImageEnhance.Contrast(image).enhance(1.9)
    image = image.filter(ImageFilter.SHARPEN)
    image = image.resize((100, 53), Image.Resampling.BICUBIC)
    image.save(OUTPUT)
    print(f"Prepared portrait saved to {OUTPUT}")


if __name__ == "__main__":
    main()
