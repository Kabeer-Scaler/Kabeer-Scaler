from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "images" / "source-prepped.png"
OUTPUT = ROOT / "avi-ascii.svg"
RAMP = " .`:-=+*#%@"


def ascii_rows() -> list[str]:
    if not INPUT.exists():
        raise FileNotFoundError("Run prep_photo.py first to generate images/source-prepped.png")

    image = Image.open(INPUT).convert("L")
    pixels = image.load()
    width, height = image.size
    rows: list[str] = []

    for y in range(height):
        line = []
        for x in range(width):
            gray = pixels[x, y]
            idx = int((gray / 255) * (len(RAMP) - 1))
            line.append(RAMP[idx])
        rows.append("".join(line).rstrip())

    return rows


def build_svg(rows: list[str]) -> str:
    rendered = []
    max_width = max(len(row) for row in rows)
    svg_width = max(720, max_width * 7 + 40)
    svg_height = max(560, len(rows) * 10 + 40)

    for idx, row in enumerate(rows):
        y = 30 + idx * 10
        rendered.append(
            f'<text x="18" y="{y}" fill="#d0d7de" opacity="0.96" font-family="Consolas, monospace" font-size="6.5">{row}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <defs>
    <clipPath id="portraitClip">
      <rect x="0" y="0" width="{svg_width}" height="{svg_height}" rx="16" />
    </clipPath>
  </defs>
  <rect width="{svg_width}" height="{svg_height}" rx="16" fill="#0d1117" />
  <text x="18" y="20" fill="#8b949e" font-family="Consolas, monospace" font-size="14">Kabeer@github ~ $ whoami</text>
  <g clip-path="url(#portraitClip)">
    {''.join(rendered)}
  </g>
</svg>
'''


def main() -> None:
    rows = ascii_rows()
    OUTPUT.write_text(build_svg(rows), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
