"""Render the prepped portrait matte into fixed-width ASCII art."""

from __future__ import annotations

import numpy as np
from PIL import Image

from profile_data import ASCII_CELL_W, ASCII_COLS, ASCII_LINE_H, DATA, IMAGES

SOURCE = IMAGES / "source-prepped.png"
OUTPUT = DATA / "ascii-portrait.txt"

COLS = ASCII_COLS
CELL_ASPECT = ASCII_CELL_W / ASCII_LINE_H
RAMP = " .:-=+*abc%@#"
# Below this the pixel is a lighting artefact, not shape. Blanking it is what
# separates a readable portrait from a grey rectangle of punctuation.
FLOOR = 0.14


def render(cols: int = COLS) -> list[str]:
    if not SOURCE.exists():
        raise FileNotFoundError("Run scripts/prep_photo.py first.")

    matte = Image.open(SOURCE).convert("LA")
    rows = max(1, round(cols * (matte.height / matte.width) * CELL_ASPECT))
    matte = matte.resize((cols, rows), Image.Resampling.LANCZOS)

    pixels = np.asarray(matte, dtype=np.float32)
    luma, alpha = pixels[..., 0], pixels[..., 1]

    # Normalise brightness across the subject only, then invert: dark hair and
    # jacket become the dense glyphs, highlights fade toward blank.
    subject = luma[alpha > 128]
    low, high = (np.percentile(subject, 4), np.percentile(subject, 96)) if subject.size else (0.0, 255.0)
    span = max(high - low, 1.0)
    density = np.clip((high - luma) / span, 0.0, 1.0)

    lines: list[str] = []
    for y in range(rows):
        line = []
        for x in range(cols):
            if alpha[y, x] < 110 or density[y, x] < FLOOR:
                line.append(" ")
                continue
            scaled = (density[y, x] - FLOOR) / (1.0 - FLOOR)
            idx = int(round(scaled * (len(RAMP) - 1)))
            # Anything that survived the floor is real shape, so keep it visible.
            line.append(RAMP[max(idx, 1)])
        lines.append("".join(line).rstrip())

    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def main() -> None:
    lines = render()
    DATA.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} rows x {COLS} cols -> {OUTPUT}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
