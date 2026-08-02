"""Render data/contributions.json into a terminal-styled contribution graph."""

from __future__ import annotations

import json
from datetime import date

from profile_data import ACCENT, ASSETS, BG, BORDER, DATA, MUTED, PROMPT, TEXT

SOURCE = DATA / "contributions.json"
OUTPUT = ASSETS / "contrib-heatmap.svg"

CELL = 12
GAP = 3
STEP = CELL + GAP

PAD = 28
TITLEBAR_H = 46
GRID_X = PAD + 34   # room for the weekday gutter
GRID_TOP = TITLEBAR_H + 46
STATS_H = 62

PALETTE = ["#1c2128", "#0e4429", "#006d32", "#26a641", "#39d353"]
WEEKDAYS = {1: "Mon", 3: "Wed", 5: "Fri"}
MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Consolas,'Liberation Mono',monospace"


def load() -> dict:
    if not SOURCE.exists():
        raise FileNotFoundError("Run scripts/fetch_contributions.py first.")
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def plural(count: int, word: str) -> str:
    return f"{count} {word}{'' if count == 1 else 's'}"


def build_svg(payload: dict) -> str:
    days = payload["days"]
    stats = payload["stats"]

    # GitHub's calendar starts on a Sunday; column = whole weeks since then.
    start = date.fromisoformat(days[0]["date"])
    origin = start.toordinal() - ((start.weekday() + 1) % 7)

    cells, month_labels = [], []
    seen_months: set[str] = set()
    columns = 0

    for day in days:
        current = date.fromisoformat(day["date"])
        column = (current.toordinal() - origin) // 7
        row = (current.weekday() + 1) % 7
        columns = max(columns, column + 1)

        x = GRID_X + column * STEP
        y = GRID_TOP + row * STEP
        count = int(day["count"])
        label = f"{plural(count, 'contribution')} on {current:%b %d, %Y}"

        cells.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
            f'fill="{PALETTE[min(int(day["level"]), 4)]}" '
            f'style="animation-delay:{column * 0.012:.2f}s"><title>{label}</title></rect>'
        )

        # Label a month at the first column it appears in.
        key = f"{current.year}-{current.month}"
        if key not in seen_months and current.day <= 7:
            seen_months.add(key)
            month_labels.append(
                f'<text class="axis" x="{x}" y="{GRID_TOP - 10}">{current:%b}</text>'
            )

    grid_right = GRID_X + columns * STEP - GAP
    width = grid_right + PAD
    grid_bottom = GRID_TOP + 7 * STEP - GAP
    legend_y = grid_bottom + 24
    stats_top = legend_y + 18
    height = stats_top + STATS_H

    weekday_labels = "".join(
        f'<text class="axis" x="{PAD}" y="{GRID_TOP + row * STEP + CELL - 2}">{name}</text>'
        for row, name in WEEKDAYS.items()
    )

    legend_left = grid_right - 36 - len(PALETTE) * (CELL + 2)
    legend = "".join(
        f'<rect x="{legend_left + index * (CELL + 2):.0f}" y="{legend_y - 10}" '
        f'width="{CELL}" height="{CELL}" rx="3" fill="{colour}"/>'
        for index, colour in enumerate(PALETTE)
    )

    best = stats["best_day"]
    tiles = [
        ("Total", f"{stats['total_contributions']}", "in the last year"),
        ("Current streak", plural(stats["current_streak"], "day"), "and counting"),
        ("Longest streak", plural(stats["longest_streak"], "day"), "personal best"),
        ("Best day", f"{best['count']}", f"{date.fromisoformat(best['date']):%b %d, %Y}"),
        ("Busiest month", stats["busiest_month"], f"{stats['active_days']} active days"),
    ]
    tile_width = (width - 2 * PAD - 4 * 12) / len(tiles)
    stat_svg = []
    for index, (label, value, hint) in enumerate(tiles):
        x = PAD + index * (tile_width + 12)
        centre = x + tile_width / 2
        stat_svg.append(
            f'<rect x="{x:.1f}" y="{stats_top}" width="{tile_width:.1f}" height="{STATS_H - 10}" '
            f'rx="10" fill="#161b22" stroke="{BORDER}"/>'
            f'<text class="tile-label" x="{centre:.1f}" y="{stats_top + 17}">{label}</text>'
            f'<text class="tile-value" x="{centre:.1f}" y="{stats_top + 36}">{value}</text>'
            f'<text class="tile-hint" x="{centre:.1f}" y="{stats_top + 48}">{hint}</text>'
        )

    span = stats["range"]
    subtitle = (
        f"{span['from']} -&gt; {span['to']}  |  "
        f"{stats['active_days']} of {stats['tracked_days']} days active"
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" \
viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="GitHub contribution graph">
  <title>{PROMPT} - contribution graph</title>
  <defs>
    <style>
      text {{ font-family: {MONO}; }}
      .title {{ font-size: 15px; fill: {TEXT}; }}
      .axis {{ font-size: 10px; fill: {MUTED}; }}
      .sub {{ font-size: 11.5px; fill: {MUTED}; }}
      .tile-label {{ font-size: 10px; fill: {MUTED}; text-anchor: middle; letter-spacing: 0.4px; }}
      .tile-value {{ font-size: 16px; font-weight: 600; fill: {TEXT}; text-anchor: middle; }}
      .tile-hint {{ font-size: 9.5px; fill: {MUTED}; text-anchor: middle; }}
      rect[style] {{ animation: pop 0.5s ease-out both; }}
      @keyframes pop {{ from {{ opacity: 0; transform: translateY(-6px); }}
                        to {{ opacity: 1; transform: translateY(0); }} }}
    </style>
  </defs>

  <rect x="0.5" y="0.5" width="{width - 1:.0f}" height="{height - 1:.0f}" rx="18" fill="{BG}" stroke="{BORDER}"/>
  <text class="title" x="{PAD}" y="28"><tspan fill="{ACCENT}">{PROMPT}:~$</tspan> ./contributions.sh</text>
  <line x1="0" y1="{TITLEBAR_H}" x2="{width:.0f}" y2="{TITLEBAR_H}" stroke="{BORDER}"/>
  <text class="sub" x="{PAD}" y="{TITLEBAR_H + 22}">{subtitle}</text>

  {"".join(month_labels)}
  {weekday_labels}
  {"".join(cells)}

  <text class="axis" x="{legend_left - 34:.0f}" y="{legend_y}">Less</text>
  {legend}
  <text class="axis" x="{legend_left + len(PALETTE) * (CELL + 2) + 4:.0f}" y="{legend_y}">More</text>
  {"".join(stat_svg)}
</svg>
"""


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(load()), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
