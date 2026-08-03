"""Render the whole neofetch-style profile card as one self-contained SVG.

Everything lives in a single file on purpose: GitHub strips CSS from README
HTML, so a flexbox layout of several images silently collapses. One SVG is the
only layout that renders identically on GitHub, in an IDE preview and locally.
"""

from __future__ import annotations

from html import escape

from profile_data import (
    ACCENT,
    ASCII_CELL_W,
    ASCII_FONT,
    ASCII_LINE_H,
    ASSETS,
    BG,
    BORDER,
    DATA,
    FOOTER,
    MUTED,
    PROMPT,
    ROWS,
    TEXT,
)

OUTPUT = ASSETS / "profile-card.svg"
ASCII_SOURCE = DATA / "ascii-portrait.txt"

WIDTH = 1080
PAD = 32
TITLEBAR_H = 48
FOOTER_H = 58

# Every ASCII line is pinned with textLength so the art keeps its proportions
# no matter which monospace font the viewer actually has installed.
ASCII_X = PAD + 2

DIVIDER_X = 452
INFO_X = 480
LABEL_X = INFO_X + 26
COLON_X = LABEL_X + 148
VALUE_X = COLON_X + 18
VALUE_LINE_H = 18
ROW_GAP = 12

MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',monospace"

# 14x14 line-art icons, keyed by the icon name used in profile_data.ROWS.
ICONS = {
    "user": '<circle cx="7" cy="4.3" r="3.1"/>'
    '<path d="M1.2 13.4c0-3.2 2.6-4.9 5.8-4.9s5.8 1.7 5.8 4.9" fill="none"/>',
    "rocket": '<path d="M7 0.6c2.5 2.1 3.9 5 3.9 8.1L9.2 10.4H4.8L3.1 8.7C3.1 5.6 4.5 2.7 7 0.6z"/>'
    '<path d="M4.4 11.2 2.2 14l3.1-0.9M9.6 11.2 11.8 14l-3.1-0.9" fill="none"/>',
    "cap": '<path d="M7 1.4 13.6 4.6 7 7.8 0.4 4.6z"/>'
    '<path d="M3 6.4v3.4c0 1.4 1.8 2.5 4 2.5s4-1.1 4-2.5V6.4" fill="none"/>',
    "code": '<path d="M4.6 2.6 0.6 7l4 4.4M9.4 2.6 13.4 7l-4 4.4" fill="none" stroke-width="1.7"/>',
    "stack": '<path d="M7 0.8 13.6 4 7 7.2 0.4 4z"/>'
    '<path d="M1.6 6.9 7 9.5l5.4-2.6M1.6 9.9 7 12.5l5.4-2.6" fill="none"/>',
    "target": '<circle cx="7" cy="7" r="6.1" fill="none"/><circle cx="7" cy="7" r="3.3" fill="none"/>'
    '<circle cx="7" cy="7" r="1.2"/>',
    "star": '<path d="M7 0.7 8.9 4.8 13.4 5.4 10.1 8.5 10.9 13 7 10.8 3.1 13 3.9 8.5 0.6 5.4 5.1 4.8z"/>',
    "trophy": '<path d="M4 1h6v4.2a3 3 0 0 1-6 0z"/>'
    '<path d="M4 2.2H1.6v1.3A2.6 2.6 0 0 0 4.2 6M10 2.2h2.4v1.3A2.6 2.6 0 0 1 9.8 6" fill="none"/>'
    '<path d="M7 8.4v2.6M4.4 13h5.2" fill="none"/>',
    "chat": '<path d="M1 2.4h12v7.4H6.2L3 12.8V9.8H1z"/>',
}


def esc(value: str) -> str:
    return escape(value, quote=False)


def ascii_lines() -> list[str]:
    if not ASCII_SOURCE.exists():
        raise FileNotFoundError("Run scripts/prep_photo.py then scripts/make_ascii.py first.")
    return ASCII_SOURCE.read_text(encoding="utf-8").rstrip("\n").split("\n")


def render_ascii(lines: list[str], top: float) -> tuple[str, float]:
    """Draw the art centred in its column; returns the drawn centre x."""
    art_width = max(len(line) for line in lines) * ASCII_CELL_W
    left = ASCII_X + (DIVIDER_X - PAD - ASCII_X - art_width) / 2

    out = []
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        y = top + index * ASCII_LINE_H
        out.append(
            f'<text x="{left:.1f}" y="{y:.1f}" textLength="{len(line) * ASCII_CELL_W:.1f}" '
            f'lengthAdjust="spacingAndGlyphs" xml:space="preserve">{esc(line)}</text>'
        )
    return "".join(out), left + art_width / 2


def render_rows(top: float, gap: float) -> tuple[str, float]:
    out = []
    y = top

    for icon, label, colour, values in ROWS:
        icon_y = y - 11
        out.append(
            f'<g transform="translate({INFO_X},{icon_y:.1f})" fill="{colour}" '
            f'stroke="{colour}" stroke-width="1.1" stroke-linejoin="round" '
            f'stroke-linecap="round">{ICONS[icon]}</g>'
        )
        out.append(f'<text class="label" x="{LABEL_X}" y="{y:.1f}" fill="{colour}">{esc(label)}</text>')
        out.append(f'<text class="colon" x="{COLON_X}" y="{y:.1f}">:</text>')
        for offset, value in enumerate(values):
            out.append(
                f'<text class="value" x="{VALUE_X}" y="{y + offset * VALUE_LINE_H:.1f}">{esc(value)}</text>'
            )
        y += len(values) * VALUE_LINE_H + gap

    return "".join(out), y - gap - VALUE_LINE_H


def build_svg() -> str:
    lines = ascii_lines()

    body_top = TITLEBAR_H + 22
    ascii_height = len(lines) * ASCII_LINE_H
    ascii_svg, ascii_centre = render_ascii(lines, body_top + ASCII_LINE_H)

    # Stretch the gap between rows so the info column spans the same height as
    # the portrait instead of stacking at the top with dead space beneath.
    text_height = sum(len(values) for *_, values in ROWS) * VALUE_LINE_H
    gap = max(ROW_GAP, (ascii_height - text_height) / (len(ROWS) - 1))

    rows_svg, rows_bottom = render_rows(body_top + 12, gap)
    body_bottom = max(body_top + ascii_height, rows_bottom + 10)

    footer_top = body_bottom + 18
    height = int(footer_top + FOOTER_H)
    footer_baseline = footer_top + 34

    title = f"{PROMPT}:~$ neofetch"
    lights = "".join(
        f'<circle cx="{WIDTH - 30 - i * 22}" cy="{TITLEBAR_H / 2:.0f}" r="6" fill="{colour}"/>'
        for i, colour in enumerate(("#28c840", "#febc2e", "#ff5f56"))
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" \
viewBox="0 0 {WIDTH} {height}" role="img" aria-label="Kabeer - neofetch style profile card">
  <title>{esc(PROMPT)} - neofetch</title>
  <defs>
    <linearGradient id="shell" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#12192333"/>
      <stop offset="1" stop-color="#010409"/>
    </linearGradient>
    <linearGradient id="ink" x1="0" y1="0" x2="0.35" y2="1">
      <stop offset="0" stop-color="#e6edf3"/>
      <stop offset="0.55" stop-color="#9fb0c0"/>
      <stop offset="1" stop-color="#6e7f8f"/>
    </linearGradient>
    <radialGradient id="halo" cx="0.5" cy="0.42" r="0.62">
      <stop offset="0" stop-color="{ACCENT}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/>
    </radialGradient>
    <style>
      text {{ font-family: {MONO}; }}
      .title {{ font-size: 15px; fill: {MUTED}; }}
      .label {{ font-size: 13.5px; font-weight: 600; }}
      .colon {{ font-size: 13.5px; fill: {MUTED}; }}
      .value {{ font-size: 13px; fill: {TEXT}; }}
      .ascii {{ font-size: {ASCII_FONT}px; fill: url(#ink); }}
      .foot {{ font-size: 13px; fill: {MUTED}; }}
      .cursor {{ animation: blink 1.1s steps(1) infinite; }}
      @keyframes blink {{ 0%, 55% {{ opacity: 1; }} 56%, 100% {{ opacity: 0; }} }}
    </style>
  </defs>

  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="18" fill="{BG}" stroke="{BORDER}"/>
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="18" fill="url(#shell)"/>

  <text class="title" x="{PAD}" y="{TITLEBAR_H / 2 + 5:.0f}">{esc(title)}</text>
  {lights}
  <line x1="0" y1="{TITLEBAR_H}" x2="{WIDTH}" y2="{TITLEBAR_H}" stroke="{BORDER}"/>

  <ellipse cx="{ascii_centre:.0f}" cy="{body_top + ascii_height * 0.5:.0f}" rx="250" \
ry="{ascii_height * 0.6:.0f}" fill="url(#halo)"/>
  <g class="ascii">{ascii_svg}</g>

  <line x1="{DIVIDER_X}" y1="{body_top - 6:.0f}" x2="{DIVIDER_X}" y2="{body_bottom:.0f}" \
stroke="{BORDER}" stroke-dasharray="3 5"/>
  {rows_svg}

  <line x1="0" y1="{footer_top:.0f}" x2="{WIDTH}" y2="{footer_top:.0f}" stroke="{BORDER}"/>
  <text class="foot" x="{PAD}" y="{footer_baseline:.0f}">
    <tspan fill="{ACCENT}">~$</tspan> {esc(FOOTER)}
    <tspan class="cursor" fill="{ACCENT}">&#9608;</tspan>
  </text>
</svg>
"""


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
