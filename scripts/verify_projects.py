from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = [
    "nyc-film-permits",
    "nasa-exoplanets",
    "college-majors-2026",
    "central-park-squirrels",
    "steam-games-v2",
    "world-happiness",
]

required = ["eda_summary.json", "eda_profile.csv", "site/data.js", "index.html", "README.md"]
for slug in PROJECTS:
    project = ROOT / "projects" / slug
    missing = [p for p in required if not (project / p).exists()]
    if missing:
        raise SystemExit(f"{slug}: missing {missing}")
    summary = json.loads((project / "eda_summary.json").read_text())
    for key in ("rows", "columns", "missing_rate", "findings"):
        if key not in summary:
            raise SystemExit(f"{slug}: summary missing key {key}")
    if "const DATA =" not in (project / "site/data.js").read_text():
        raise SystemExit(f"{slug}: site/data.js does not expose DATA")
    print(f"{slug}: {summary['rows']} rows × {summary['columns']} columns; missing={summary['missing_rate']:.2%}")

print("Verified six independent EDA + D3 projects.")
