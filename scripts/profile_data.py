"""Single source of truth for everything rendered onto the profile art.

Edit this file and re-run `python scripts/build_all.py` to refresh every SVG.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DATA = ROOT / "data"
IMAGES = ROOT / "images"

USERNAME = "Kabeer-Scaler"
PROMPT = "kabeer@github"

# ASCII geometry, shared so the renderer and the card can never disagree.
# A monospace cell is roughly twice as tall as it is wide; the art is squashed
# by that ratio when sampled and unsquashed by the same ratio when drawn.
ASCII_COLS = 60
ASCII_CELL_W = 7.0
ASCII_LINE_H = 12.2
ASCII_FONT = 12.0

# GitHub dark-theme palette, so the card sits natively inside a README.
BG = "#0d1117"
PANEL = "#010409"
BORDER = "#30363d"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
ACCENT = "#58a6ff"

BLUE = "#58a6ff"
PURPLE = "#bc8cff"
GREEN = "#3fb950"
ORANGE = "#f0883e"
RED = "#ff7b72"
YELLOW = "#e3b341"
CYAN = "#39c5cf"
PINK = "#f778ba"

# Each row: (icon key, label, label colour, [value lines])
ROWS = [
    ("user", "Name", BLUE, ["Kabeer"]),
    ("rocket", "Role", PURPLE, ["Aspiring Machine Learning Engineer"]),
    (
        "cap",
        "Education",
        GREEN,
        [
            "Scaler School of Technology (2024 - 2028)",
            "BITS Pilani, B.Sc. Computer Science (2024 - 2027)",
        ],
    ),
    (
        "stack",
        "Tech Stack",
        CYAN,
        [
            "Python • NumPy • Pandas • Scikit-learn • PyTorch",
            "SQL • Git • Java • MongoDB",
        ],
    ),
    (
        "target",
        "Current Focus",
        RED,
        [
            "Deep Learning • PyTorch • Machine Learning",
            "Computer Vision • NLP • LLM Systems",
        ],
    ),
    (
        "star",
        "Highlights",
        YELLOW,
        [
            "• Building end-to-end ML and AI projects",
            "• Exploring LLMs, RAG and agentic systems",
        ],
    ),
    ("chat", "Fun Fact", PINK, ["I turn chai into code and ideas"]),
]

FOOTER = "Keep learning. Keep building. Ship impact."

# Grouped for the README tech-stack badges.
STACK = {
    "Languages": ["Python", "Java", "JavaScript", "SQL"],
    "ML & Data": ["PyTorch", "scikit-learn", "NumPy", "Pandas", "Jupyter"],
}

EMAIL = "KABEER.24299@gmail.com"
