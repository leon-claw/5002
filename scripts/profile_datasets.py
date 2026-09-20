"""Profile the candidate datasets for the CityU 5002 group project.

The script intentionally keeps the raw downloads unchanged and writes only
machine-readable metadata plus a human-readable review into data/metadata/.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "metadata"
OUT.mkdir(parents=True, exist_ok=True)


DATASETS = [
    {
        "id": "college_majors",
        "name": "College Majors 2026: earnings, debt, jobs and AI",
        "path": ROOT / "data/processed/college-majors/college_majors_2026.csv",
        "source": "Kaggle: kylefengkfeng209/college-majors-2026-earnings-debt-jobs-ai",
        "source_url": "https://www.kaggle.com/datasets/kylefengkfeng209/college-majors-2026-earnings-debt-jobs-ai",
    },
    {
        "id": "spotify",
        "name": "Spotify tracks and audio features (50k)",
        "path": ROOT / "data/processed/spotify/spotify_tracks.csv",
        "source": "Kaggle: lorenzoscaturchio/spotify-tracks-audio-features-50k",
        "source_url": "https://www.kaggle.com/datasets/lorenzoscaturchio/spotify-tracks-audio-features-50k",
    },
    {
        "id": "airbnb_nyc",
        "name": "New York City Airbnb Open Data",
        "path": ROOT / "data/processed/airbnb/AB_NYC_2019.csv",
        "source": "Kaggle: dgomonov/new-york-city-airbnb-open-data",
        "source_url": "https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data",
    },
    {
        "id": "student_exam",
        "name": "Student exam performance and success",
        "path": ROOT / "data/processed/student-exam/student_exam_performance.csv",
        "source": "Kaggle: mobeenfatimah/student-exam-performance-and-success-dataset",
        "source_url": "https://www.kaggle.com/datasets/mobeenfatimah/student-exam-performance-and-success-dataset",
    },
    {
        "id": "nyc_film_permits",
        "name": "NYC film permits (historical public mirror)",
        "path": ROOT / "data/raw/nyc-film-permits-historical.csv",
        "source": "Public GitHub mirror of NYC MOME permits, 2011–2015",
        "source_url": "https://data.cityofnewyork.us/City-Government/Film-Permits/tg4x-b46p",
    },
    {
        "id": "world_happiness",
        "name": "World Happiness Report 2026, Figure 2.1 data",
        "path": ROOT / "data/raw/world-happiness-report-2026-figure-2-1.xlsx",
        "source": "Official World Happiness Report data sharing page",
        "source_url": "https://www.worldhappiness.report/data-sharing/",
    },
    {
        "id": "squirrel",
        "name": "2018 Central Park Squirrel Census",
        "path": ROOT / "data/raw/central-park-squirrel-census.csv",
        "source": "NYC Open Data / TidyTuesday public mirror",
        "source_url": "https://data.cityofnewyork.us/Environment/2018-Central-Park-Squirrel-Census-Squirrel-Data/vfnx-vebw",
    },
    {
        "id": "hk_beach",
        "name": "Hong Kong beach water quality (2025)",
        "path": ROOT / "data/raw/hong-kong-beach-historical-2025-tc.csv",
        "source": "Hong Kong Environmental Protection Department",
        "source_url": "https://cd.epic.epd.gov.hk/beachpsi/tc/beach-historical-data-2025-tc.csv",
    },
    {
        "id": "steam",
        "name": "Steam Games Dataset V2",
        "path": ROOT / "data/processed/steam/extended_steam_games.csv",
        "source": "Kaggle: muhammadaqeelkabir/steam-games-dataset-v2; extended table",
        "source_url": "https://www.kaggle.com/datasets/muhammadaqeelkabir/steam-games-dataset-v2",
    },
    {
        "id": "steam_wikidata_table",
        "name": "Steam Games Dataset V2 — Wikidata enrichment table",
        "path": ROOT / "data/processed/steam/steam_games_wikidata.csv",
        "source": "Kaggle: muhammadaqeelkabir/steam-games-dataset-v2",
        "source_url": "https://www.kaggle.com/datasets/muhammadaqeelkabir/steam-games-dataset-v2",
    },
    {
        "id": "steamspy_table",
        "name": "Steam Games Dataset V2 — SteamSpy raw table",
        "path": ROOT / "data/processed/steam/steamspy_raw.csv",
        "source": "Kaggle: muhammadaqeelkabir/steam-games-dataset-v2",
        "source_url": "https://www.kaggle.com/datasets/muhammadaqeelkabir/steam-games-dataset-v2",
    },
    {
        "id": "nasa_exoplanets",
        "name": "NASA Exoplanet Archive Planetary Systems table",
        "path": ROOT / "data/raw/nasa-exoplanets-ps.csv",
        "source": "NASA Exoplanet Archive TAP, table ps",
        "source_url": "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS",
    },
    {
        "id": "netflix",
        "name": "Netflix TV Shows and Movies (titles + credits)",
        "path": ROOT / "data/processed/netflix/titles.csv",
        "source": "Kaggle: victorsoeiro/netflix-tv-shows-and-movies",
        "source_url": "https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies",
    },
    {
        "id": "netflix_credits",
        "name": "Netflix TV Shows and Movies — credits table",
        "path": ROOT / "data/processed/netflix/credits.csv",
        "source": "Kaggle: victorsoeiro/netflix-tv-shows-and-movies",
        "source_url": "https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies",
    },
]


def jsonable(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def infer_dates(df: pd.DataFrame) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for col in df.columns:
        name = str(col).lower()
        if not any(k in name for k in ("date", "year", "time", "released", "entered", "start", "end")):
            continue
        s = df[col]
        # Numeric release years/years are not nanosecond timestamps. Keep them
        # as year ranges; parse strings and actual datetime columns as dates.
        if pd.api.types.is_numeric_dtype(s):
            numeric = pd.to_numeric(s, errors="coerce")
            valid_years = numeric.dropna()
            if "year" in name and not valid_years.empty and valid_years.between(1800, 2200).mean() > 0.8:
                out[str(col)] = {
                    "valid": int(valid_years.size),
                    "min": int(valid_years.min()),
                    "max": int(valid_years.max()),
                    "kind": "year",
                }
            continue
        parsed = pd.to_datetime(s, errors="coerce")
        valid = parsed.notna().sum()
        if valid >= max(3, int(len(df) * 0.25)):
            out[str(col)] = {
                "valid": int(valid),
                "min": str(parsed.min()),
                "max": str(parsed.max()),
                "kind": "datetime",
            }
    return out


def profile_csv(path: Path) -> pd.DataFrame:
    # Latin-1 fallback is useful for some older Kaggle exports.
    try:
        return pd.read_csv(path, low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, low_memory=False, encoding="latin-1")


def profile_xlsx(path: Path) -> pd.DataFrame:
    return pd.read_excel(path)


def profile_one(spec: dict[str, Any]) -> dict[str, Any]:
    path = Path(spec["path"])
    df = profile_xlsx(path) if path.suffix.lower() in (".xlsx", ".xls") else profile_csv(path)
    n, p = df.shape
    missing = df.isna().sum()
    dtypes = {str(c): str(df[c].dtype) for c in df.columns}
    numeric = df.select_dtypes(include="number")
    categorical = df.select_dtypes(exclude="number")
    numeric_summary = {}
    for col in numeric.columns:
        s = pd.to_numeric(numeric[col], errors="coerce")
        if s.notna().any():
            numeric_summary[str(col)] = {
                "non_null": int(s.notna().sum()),
                "min": jsonable(s.min()),
                "median": jsonable(s.median()),
                "max": jsonable(s.max()),
                "unique": int(s.nunique(dropna=True)),
            }
    categorical_summary = {}
    for col in categorical.columns:
        s = categorical[col]
        top = s.value_counts(dropna=False).head(5)
        categorical_summary[str(col)] = {
            "unique_including_na": int(s.nunique(dropna=False)),
            "top": [{"value": jsonable(k), "count": int(v)} for k, v in top.items()],
        }
    return {
        **{k: v for k, v in spec.items() if k != "path"},
        "path": str(path.relative_to(ROOT)),
        "file_size_bytes": path.stat().st_size,
        "rows": int(n),
        "columns": int(p),
        "duplicate_rows": int(df.duplicated().sum()),
        "total_missing_cells": int(missing.sum()),
        "missing_cell_pct": round(float(missing.sum() / max(1, n * p) * 100), 3),
        "column_names": [str(c) for c in df.columns],
        "dtypes": dtypes,
        "numeric_column_count": int(len(numeric.columns)),
        "categorical_column_count": int(len(categorical.columns)),
        "high_missing_columns": [
            {"column": str(c), "missing": int(missing[c]), "missing_pct": round(float(missing[c] / max(1, n) * 100), 2)}
            for c in missing[missing > 0].sort_values(ascending=False).index[:20]
        ],
        "date_candidates": infer_dates(df),
        "numeric_summary": numeric_summary,
        "categorical_summary": categorical_summary,
    }


def short(v: Any, maxlen: int = 120) -> str:
    s = str(v).replace("\n", " ")
    return s if len(s) <= maxlen else s[: maxlen - 1] + "…"


def make_markdown(profiles: list[dict[str, Any]]) -> str:
    lines = [
        "# Dataset profiling for CityU 5002 group project",
        "",
        "Generated from the downloaded files in `data/raw/` and `data/processed/`. The raw files are kept unchanged.",
        "",
    ]
    for p in profiles:
        lines += [f"## {p['name']}", "", f"- Source: {p['source']}", f"- Local file: `{p['path']}`", f"- Shape: **{p['rows']:,} rows × {p['columns']:,} columns**", f"- Size: {p['file_size_bytes'] / 1024 / 1024:.2f} MB; duplicate rows: {p['duplicate_rows']:,}; missing cells: {p['missing_cell_pct']:.2f}%", ""]
        lines.append("### Schema")
        lines.append("")
        lines.append("| Column | Type | Non-null / unique or range |")
        lines.append("|---|---|---|")
        for col in p["column_names"]:
            dtype = p["dtypes"].get(col, "")
            if col in p["numeric_summary"]:
                s = p["numeric_summary"][col]
                detail = f"{s['non_null']:,} non-null; min {short(s['min'])}; median {short(s['median'])}; max {short(s['max'])}; {s['unique']:,} unique"
            elif col in p["categorical_summary"]:
                s = p["categorical_summary"][col]
                tops = ", ".join(f"{short(x['value'], 35)} ({x['count']:,})" for x in s["top"][:3])
                detail = f"{s['unique_including_na']:,} unique incl. NA; top: {tops}"
            else:
                detail = ""
            lines.append(f"| `{col}` | `{dtype}` | {detail} |")
        if p["high_missing_columns"]:
            lines += ["", "### Missingness hotspots", "", "| Column | Missing | Missing % |", "|---|---:|---:|"]
            for x in p["high_missing_columns"][:12]:
                lines.append(f"| `{x['column']}` | {x['missing']:,} | {x['missing_pct']:.2f}% |")
        if p["date_candidates"]:
            lines += ["", "### Date/time candidates", ""]
            for c, x in p["date_candidates"].items():
                lines.append(f"- `{c}`: {x['valid']:,} valid; {x['min']} to {x['max']} ({x.get('kind', 'datetime')})")
        lines += ["", "---", ""]
    return "\n".join(lines)


def main() -> None:
    profiles = []
    for spec in DATASETS:
        profiles.append(profile_one(spec))
    (OUT / "dataset_profiles.json").write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "dataset_profiles.md").write_text(make_markdown(profiles), encoding="utf-8")
    print(json.dumps([{k: p[k] for k in ("id", "rows", "columns", "duplicate_rows", "missing_cell_pct")} for p in profiles], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
