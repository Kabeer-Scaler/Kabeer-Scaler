from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "info-card.svg"


def wrap_text(value: str, max_chars: int = 58) -> list[str]:
    words = value.split()
    lines: list[str] = []
    current = ""

    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines or [value]


def build_svg() -> str:
    rows = [
        ("Role", "Aspiring Machine Learning Engineer"),
        ("Stack", "Python • NumPy • Pandas • Scikit-learn • PyTorch • SQL • Git • Java • MongoDB"),
        ("Current Focus", "Deep Learning • PyTorch • Machine Learning • Computer Vision • NLP • LLM Systems"),
    ]
    fragments = []
    card_height = 300
    y_start = 76

    for idx, (label, value) in enumerate(rows):
        value_lines = wrap_text(value, max_chars=52 if idx == 1 else 58)
        fragments.append(
            f'<text x="28" y="{y_start + idx * 68}" fill="#8b949e" font-family="Consolas, monospace" font-size="14">[{label}]</text>'
        )
        for line_idx, line in enumerate(value_lines):
            fragments.append(
                f'<text x="145" y="{y_start + idx * 68 + line_idx * 18}" fill="#d0d7de" font-family="Consolas, monospace" font-size="13">{line}</text>'
            )
        card_height = max(card_height, y_start + idx * 68 + len(value_lines) * 18 + 28)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 {card_height}" width="720" height="{card_height}">
  <rect width="720" height="{card_height}" rx="16" fill="#0d1117" stroke="#30363d" />
  <text x="26" y="26" fill="#58a6ff" font-family="Consolas, monospace" font-size="16">neofetch-style profile card</text>
  <line x1="26" y1="38" x2="694" y2="38" stroke="#30363d" />
  {''.join(fragments)}
</svg>
'''


def main() -> None:
    OUTPUT.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
