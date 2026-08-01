from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "info-card.svg"


def build_svg() -> str:
    rows = [
        ("Role", "Aspiring Machine Learning Engineer"),
        ("Stack", "Python • NumPy • Pandas • Scikit-learn • PyTorch • SQL • Git • Java • MongoDB"),
        ("Current Focus", "Deep Learning • PyTorch • Machine Learning • Computer Vision • NLP • LLM Systems"),
    ]
    fragments = []
    for idx, (label, value) in enumerate(rows):
        y = 76 + idx * 42
        fragments.append(
            f'<text x="28" y="{y}" fill="#8b949e" font-family="Consolas, monospace" font-size="14">[{label}]</text>'
        )
        fragments.append(
            f'<text x="145" y="{y}" fill="#d0d7de" font-family="Consolas, monospace" font-size="14">{value}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 240" width="520" height="240">
  <rect width="520" height="240" rx="16" fill="#0d1117" stroke="#30363d" />
  <text x="26" y="26" fill="#58a6ff" font-family="Consolas, monospace" font-size="16">neofetch-style profile card</text>
  <line x1="26" y1="38" x2="494" y2="38" stroke="#30363d" />
  {''.join(fragments)}
</svg>
'''


def main() -> None:
    OUTPUT.write_text(build_svg(), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
