"""Scrape the public contribution calendar into data/contributions.json.

The calendar cells only carry a 0-4 intensity `data-level`, which is not a
contribution count. The real number lives in the sibling <tool-tip> ("3
contributions on ..."), so we join the two on the cell id and store both.
"""

from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup

from profile_data import DATA, USERNAME

USER = os.environ.get("GH_PROFILE_USER", USERNAME)
OUTPUT = DATA / "contributions.json"
URL = f"https://github.com/users/{USER}/contributions"

COUNT_PATTERN = re.compile(r"^(No|[\d,]+)\s+contribution")


def parse_count(tooltip_text: str) -> int:
    match = COUNT_PATTERN.match(tooltip_text.strip())
    if not match:
        return 0
    value = match.group(1)
    return 0 if value == "No" else int(value.replace(",", ""))


def fetch_calendar() -> list[dict[str, object]]:
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    counts = {
        tip["for"]: parse_count(tip.get_text())
        for tip in soup.find_all("tool-tip")
        if tip.get("for")
    }

    cells = soup.select("[data-date][data-level]")
    if not cells:
        raise RuntimeError("No contribution cells found; GitHub's markup may have changed.")

    days: list[dict[str, object]] = []
    for cell in cells:
        day = (cell.get("data-date") or "").strip()
        if not day:
            continue
        try:
            level = int((cell.get("data-level") or "0").strip())
        except ValueError:
            level = 0
        days.append({"date": day, "level": level, "count": counts.get(cell.get("id"), 0)})

    if not days:
        raise RuntimeError("Parsed zero contribution days from the calendar.")

    return sorted(days, key=lambda item: item["date"])


def compute_stats(days: list[dict[str, object]]) -> dict[str, object]:
    counts = {str(day["date"]): int(day["count"]) for day in days}
    if not counts:
        return {}

    ordered = sorted(counts)
    monthly: dict[str, int] = defaultdict(int)
    for day, count in counts.items():
        monthly[datetime.strptime(day, "%Y-%m-%d").strftime("%b %Y")] += count

    # Start from the last day that has data: today's cell can still be empty
    # while the streak is alive, and that should not zero it out.
    current_streak = 0
    cursor = date.fromisoformat(ordered[-1])
    if counts[ordered[-1]] == 0:
        cursor -= timedelta(days=1)
    while counts.get(cursor.isoformat(), 0) > 0:
        current_streak += 1
        cursor -= timedelta(days=1)

    longest_streak = streak = 0
    for day in ordered:
        streak = streak + 1 if counts[day] > 0 else 0
        longest_streak = max(longest_streak, streak)

    best_day = max(counts, key=lambda day: counts[day])

    return {
        "total_contributions": sum(counts.values()),
        "active_days": sum(1 for value in counts.values() if value > 0),
        "tracked_days": len(counts),
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": {"date": best_day, "count": counts[best_day]},
        "busiest_month": max(monthly, key=lambda key: monthly[key]),
        "monthly_totals": dict(monthly),
        "range": {"from": ordered[0], "to": ordered[-1]},
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    days = fetch_calendar()
    payload = {
        "username": USER,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "days": days,
        "stats": compute_stats(days),
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(days)} days -> {OUTPUT} ({payload['stats']['total_contributions']} contributions)")


if __name__ == "__main__":
    main()
