from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USER = os.environ.get("GH_PROFILE_USER", "Kabeer-Scaler")
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUTPUT = DATA_DIR / "contributions.json"
URL = f"https://github.com/users/{USER}/contributions"


def fetch_calendar() -> list[dict[str, object]]:
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    cells = soup.select("[data-date][data-level]")
    if not cells:
        raise RuntimeError("No contribution calendar cells were found in the public GitHub page.")

    data: list[dict[str, object]] = []
    for cell in cells:
        date_text = (cell.get("data-date") or "").strip()
        level = (cell.get("data-level") or "0").strip()
        if not date_text:
            continue

        try:
            level_value = int(level)
        except ValueError:
            continue

        data.append({"date": date_text, "level": level_value})

    if not data:
        raise RuntimeError("Unable to parse any contribution dates or levels from the public GitHub page.")

    return sorted(data, key=lambda item: item["date"])


def compute_stats(entries: list[dict[str, object]]) -> dict[str, object]:
    by_day: dict[str, int] = {}
    for entry in entries:
        date_text = str(entry["date"])
        level = int(entry["level"])
        by_day[date_text] = level

    dates = sorted(by_day)
    if not dates:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "best_day": 0,
            "monthly_totals": {},
            "total_contributions": 0,
        }

    total = sum(by_day.values())

    current_streak = 0
    cursor = datetime.strptime(dates[-1], "%Y-%m-%d").date()
    while by_day.get(cursor.isoformat(), 0) > 0:
        current_streak += 1
        cursor -= timedelta(days=1)

    longest_streak = 0
    streak = 0
    previous: datetime.date | None = None
    for day in sorted(by_day):
        current_date = datetime.strptime(day, "%Y-%m-%d").date()
        if by_day[day] > 0:
            if previous is None or (current_date - previous).days == 1:
                streak += 1
            else:
                streak = 1
            longest_streak = max(longest_streak, streak)
            previous = current_date
        else:
            streak = 0
            previous = current_date

    best_day = max(by_day.values()) if by_day else 0

    monthly_totals: dict[str, int] = defaultdict(int)
    for day, level in by_day.items():
        month_key = datetime.strptime(day, "%Y-%m-%d").strftime("%b %Y")
        monthly_totals[month_key] += level

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "monthly_totals": dict(monthly_totals),
        "total_contributions": total,
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    calendar = fetch_calendar()
    payload = {
        "username": USER,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "days": calendar,
        "stats": compute_stats(calendar),
    }
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
