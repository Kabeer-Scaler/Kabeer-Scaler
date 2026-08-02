<div align="center">
  <img src="./assets/profile-card.svg" alt="Kabeer - neofetch style profile card" width="100%">
</div>

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Kabeer--Scaler-58a6ff?style=for-the-badge&logo=github&logoColor=white&labelColor=0d1117)](https://github.com/Kabeer-Scaler)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0a66c2?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=0d1117)](https://www.linkedin.com/in/)
[![Email](https://img.shields.io/badge/Email-Say%20hello-ea4335?style=for-the-badge&logo=gmail&logoColor=white&labelColor=0d1117)](mailto:)
[![Profile views](https://komarev.com/ghpvc/?username=Kabeer-Scaler&style=for-the-badge&color=3fb950&label=PROFILE+VIEWS)](https://github.com/Kabeer-Scaler)

</div>

---

## `whoami`

I am **Kabeer**, a Computer Science undergrad studying at **Scaler School of Technology** and
**BITS Pilani** at the same time. I spend most of my time on **machine learning**, **deep
learning** and **LLM-powered systems**, and the rest of it building the backends and tools that
those systems need in order to be useful.

- Currently building end-to-end ML and AI projects, from data prep to a deployed interface.
- Currently exploring LLMs, RAG pipelines and agentic systems.
- Comfortable moving between a Jupyter notebook, a Spring Boot service and a React front end.
- Always happy to talk about model evaluation, system design or a good terminal setup.

---

## `cat education.txt`

| Institution | Programme | Timeline |
| :--- | :--- | :--- |
| **Scaler School of Technology** | Computer Science and Engineering | 2024 - 2028 |
| **BITS Pilani** | B.Sc. Computer Science | 2024 - 2027 |

---

## `ls ~/stack`

**Languages**

![Python](https://img.shields.io/badge/Python-3776ab?style=flat-square&logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-f0883e?style=flat-square&logo=openjdk&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-f7df1e?style=flat-square&logo=javascript&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178c6?style=flat-square&logo=typescript&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-39c5cf?style=flat-square&logo=mysql&logoColor=white)
![C++](https://img.shields.io/badge/C++-00599c?style=flat-square&logo=cplusplus&logoColor=white)

**Machine learning and data**

![PyTorch](https://img.shields.io/badge/PyTorch-ee4c2c?style=flat-square&logo=pytorch&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-f7931e?style=flat-square&logo=scikitlearn&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5c3ee8?style=flat-square&logo=opencv&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-f37626?style=flat-square&logo=jupyter&logoColor=white)

**Backend, data stores and tooling**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![Spring](https://img.shields.io/badge/Spring-6db33f?style=flat-square&logo=spring&logoColor=white)
![React](https://img.shields.io/badge/React-61dafb?style=flat-square&logo=react&logoColor=black)
![MongoDB](https://img.shields.io/badge/MongoDB-47a248?style=flat-square&logo=mongodb&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479a1?style=flat-square&logo=mysql&logoColor=white)
![Git](https://img.shields.io/badge/Git-f14e32?style=flat-square&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ed?style=flat-square&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-fcc624?style=flat-square&logo=linux&logoColor=black)

---

## `./contributions.sh`

<div align="center">
  <img src="./assets/contrib-heatmap.svg" alt="Contribution graph" width="100%">
</div>

<div align="center">

![Stats](https://github-readme-stats.vercel.app/api?username=Kabeer-Scaler&show_icons=true&hide_border=true&bg_color=0d1117&title_color=58a6ff&text_color=c9d1d9&icon_color=3fb950&include_all_commits=true&count_private=true)
![Top languages](https://github-readme-stats.vercel.app/api/top-langs/?username=Kabeer-Scaler&layout=compact&hide_border=true&bg_color=0d1117&title_color=58a6ff&text_color=c9d1d9&langs_count=8)

</div>

---

## `cat build.md`

This repository is not just a README; it is the generator that draws one. Every image above is
an SVG built by the scripts in [`scripts/`](./scripts), from a single source of truth in
[`scripts/profile_data.py`](./scripts/profile_data.py).

| Script | What it does |
| :--- | :--- |
| `profile_data.py` | Every string, colour and layout constant used by the renderers. |
| `prep_photo.py` | Cuts the portrait out of its background and frames it head-and-shoulders. |
| `make_ascii.py` | Samples that matte into fixed-width ASCII, correcting for cell aspect ratio. |
| `make_profile_card.py` | Draws the whole neofetch card as one self-contained SVG. |
| `fetch_contributions.py` | Scrapes the public contribution calendar into `data/contributions.json`. |
| `render_heatmap_svg.py` | Renders that data as the contribution graph and stat tiles. |
| `build_all.py` | Runs the above in dependency order. |

```bash
git clone https://github.com/Kabeer-Scaler/Kabeer-Scaler.git
cd Kabeer-Scaler
python -m venv .venv && .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/build_all.py --all               # portrait + contributions + all SVGs
python scripts/build_all.py                     # just redraw from committed data
```

The card is deliberately **one** SVG rather than a row of images in HTML: GitHub strips CSS from
README markup, so a flexbox layout silently collapses into a stack. A single SVG renders
identically on GitHub, in an editor preview and on disk.

A [GitHub Action](./.github/workflows/update-profile.yml) re-runs the contribution steps every
morning and commits the refreshed graph, so the numbers above are never stale.

---

<div align="center">

<sub>`~$ Keep learning. Keep building. Ship impact.`</sub>

</div>
