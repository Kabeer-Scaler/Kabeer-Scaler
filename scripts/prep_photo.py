"""Turn the source portrait into a clean, background-free matte for ASCII art.

A crisp silhouette is what actually makes the ASCII readable, so we cut the
subject out with `rembg` when it is installed. The fallback is a border-seeded
flood fill in RGB distance, which is fine for a flat studio backdrop but leaks
wherever clothing matches the wall.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from profile_data import IMAGES

OUTPUT = IMAGES / "source-prepped.png"
BG_TOLERANCE = 44.0


def find_source_image() -> Path:
    candidates = [
        path
        for pattern in ("*.png", "*.jpg", "*.jpeg", "*.webp")
        for path in sorted(IMAGES.glob(pattern))
        if path.name != OUTPUT.name
    ]
    if not candidates:
        raise FileNotFoundError(f"Drop a portrait into {IMAGES} first.")
    return candidates[0]


def segment_mask(image: Image.Image) -> np.ndarray | None:
    """True where the pixel is background, via rembg. None if it is unavailable."""
    try:
        from rembg import remove
    except Exception:
        return None

    try:
        cut = remove(image.convert("RGBA"))
    except Exception as exc:  # missing onnxruntime, no model download, ...
        print(f"rembg unavailable ({exc}); falling back to flood fill.")
        return None

    return np.asarray(cut)[..., 3] < 128


def flood_fill_mask(rgb: np.ndarray) -> np.ndarray:
    """Border-seeded flood fill over pixels close to the sampled backdrop colour."""
    height, width, _ = rgb.shape
    # Median of the top strip: corners pick up shadow and skew a mean badly.
    backdrop = np.median(rgb[:30, :].reshape(-1, 3), axis=0)
    close = np.linalg.norm(rgb - backdrop, axis=2) < BG_TOLERANCE

    is_bg = np.zeros((height, width), dtype=bool)
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        for y in (0, height - 1):
            if close[y, x] and not is_bg[y, x]:
                is_bg[y, x] = True
                queue.append((y, x))
    for y in range(height):
        for x in (0, width - 1):
            if close[y, x] and not is_bg[y, x]:
                is_bg[y, x] = True
                queue.append((y, x))

    while queue:
        y, x = queue.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width and close[ny, nx] and not is_bg[ny, nx]:
                is_bg[ny, nx] = True
                queue.append((ny, nx))

    return is_bg


HEAD_WIDTHS = 2.05   # frame width, measured in head widths
FRAME_ASPECT = 1.18  # frame height / frame width


def crop_to_subject(image: Image.Image, mask: np.ndarray) -> tuple[Image.Image, np.ndarray]:
    """Frame head-and-shoulders, scaled off the measured head width."""
    subject = ~mask
    ys, xs = np.where(subject)
    if ys.size == 0:
        return image, mask

    top = int(ys.min())
    bottom = int(ys.max())

    # Sample across the forehead: that row is all head, no shoulders or ears.
    brow = min(mask.shape[0] - 1, top + int((bottom - top) * 0.12))
    brow_xs = np.where(subject[brow])[0]
    if brow_xs.size < 4:
        return image, mask
    head_width = int(brow_xs.max() - brow_xs.min())
    head_centre = int((brow_xs.max() + brow_xs.min()) // 2)

    frame_width = int(head_width * HEAD_WIDTHS)
    frame_height = int(frame_width * FRAME_ASPECT)

    left = max(0, head_centre - frame_width // 2)
    right = min(image.width, left + frame_width)
    left = max(0, right - frame_width)

    top = max(0, top - int(head_width * 0.12))
    bottom = min(image.height, top + frame_height)
    top = max(0, bottom - frame_height)

    return image.crop((left, top, right, bottom)), mask[top:bottom, left:right]


def main() -> None:
    source = find_source_image()
    original = Image.open(source).convert("RGB")

    # Work at a reduced size: segmentation is the slow step and we only need shape.
    working = ImageOps.contain(original, (720, 720), Image.Resampling.LANCZOS)
    mask = segment_mask(working)
    if mask is None:
        mask = flood_fill_mask(np.asarray(working, dtype=np.float32))

    cropped, cropped_mask = crop_to_subject(working, mask)

    grey = ImageOps.grayscale(cropped)
    grey = ImageOps.autocontrast(grey, cutoff=2)
    grey = ImageEnhance.Contrast(grey).enhance(1.35)
    grey = grey.filter(ImageFilter.UnsharpMask(radius=2, percent=140, threshold=3))

    # Alpha carries the silhouette so the ASCII step can leave the backdrop blank.
    alpha = Image.fromarray(((~cropped_mask) * 255).astype(np.uint8), mode="L")
    alpha = alpha.filter(ImageFilter.MedianFilter(size=5))

    matte = Image.merge("LA", (grey, alpha))
    matte.save(OUTPUT)
    print(f"Prepared portrait ({matte.width}x{matte.height}) -> {OUTPUT}")


if __name__ == "__main__":
    main()
