from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = [
    "nyc-film-permits",
    "nasa-exoplanets",
    "college-majors-2026",
    "central-park-squirrels",
    "steam-games-v2",
    "world-happiness",
]

for slug in PROJECTS:
    project = ROOT / "projects" / slug
    print(f"\n=== {slug} ===")
    subprocess.run([sys.executable, "eda.py"], cwd=project, check=True)

print("\nAll EDA pipelines completed.")
