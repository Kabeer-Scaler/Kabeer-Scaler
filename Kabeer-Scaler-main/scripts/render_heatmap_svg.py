from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "contributions.json"
OUTPUT_FILE = ROOT / "contrib-heatmap.svg"

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]


def load_days() -> list[dict[str, int | str]]:
    payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return payload.get("days", [])


def build_svg(days: list[dict[str, int | str]]) -> str:
    cells: list[str] = []
    if not days:
        return "<svg></svg>"

    start_date = datetime.strptime(str(days[0]["date"]), "%Y-%m-%d")
    for offset, entry in enumerate(days):
        level = int(entry["level"])
        day = datetime.strptime(str(entry["date"]), "%Y-%m-%d")
        week_index = int((day - start_date).days // 7)
        row = (day.weekday() + 1) % 7
        x = 24 + week_index * 14
        y = 58 + row * 14
        fill = PALETTE[min(level, len(PALETTE) - 1)]
        delay = offset * 0.015
        cells.append(
            f'<rect x="{x}" y="{y}" width="10" height="10" rx="3" fill="{fill}" opacity="0.92" '
            f'style="animation: reveal 0.45s ease-out {delay}s both;" />'
        )

    style = """
    <style>
      .frame { fill: #0d1117; stroke: #30363d; stroke-width: 1; }
      .title { font: 600 18px 'Segoe UI', Arial, sans-serif; fill: #c9d1d9; }
      .small { font: 12px 'Segoe UI', Arial, sans-serif; fill: #8b949e; }
      @keyframes reveal {
        from { opacity: 0; transform: translate(14px, -12px) scale(0.3); }
        to { opacity: 1; transform: translate(0, 0) scale(1); }
      }
    </style>
    """

    legend = "".join(
        f'<rect x="{16 + i * 18}" y="178" width="12" height="12" rx="2" fill="{PALETTE[i]}" />'
        for i in range(len(PALETTE))
    )

    footer = (
        f'<text x="18" y="214" class="small">{len(days)} daily cells rendered from GitHub\'s '
        'public contributions calendar.</text>'
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 260" width="860" height="260">
  {style}
  <rect x="1" y="1" width="858" height="258" rx="16" class="frame" />
  <text x="18" y="26" class="title">avi@github ~ $ ./contributions.sh</text>
  <text x="18" y="48" class="small">public contribution graph · refreshed from GitHub</text>
  {''.join(cells)}
  <text x="18" y="172" class="small">Less</text>
  <text x="270" y="172" class="small">More</text>
  {legend}
  {footer}
</svg>
'''


def main() -> None:
    days = load_days()
    svg = build_svg(days)
    OUTPUT_FILE.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
