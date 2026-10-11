"""Reproduce every number shown in the Film Permits dashboard.

Run from any directory: python3 film-permits-2026/analyze.py
The original CSV is read-only; only public/data/analysis.json is generated.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data" / "Film_Permits_20260930.csv"
OUTPUT = ROOT / "public" / "data" / "analysis.json"
BOROUGHS = ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]
CATEGORIES = [
    "Television", "Theater", "Film", "Commercial", "Still Photography",
    "WEB", "Documentary", "Student", "Music Video",
]
DATE_FMT = "%m/%d/%Y %I:%M:%S %p"


def count_series(series, labels):
    counts = series.value_counts()
    return [{"name": label, "count": int(counts.get(label, 0))} for label in labels]


def quantile_summary(values):
    values = values.dropna()
    if values.empty:
        return None
    return {
        "n": int(len(values)),
        "p10": round(float(values.quantile(.10)), 3),
        "p25": round(float(values.quantile(.25)), 3),
        "median": round(float(values.median()), 3),
        "p75": round(float(values.quantile(.75)), 3),
        "p90": round(float(values.quantile(.90)), 3),
    }


def cramers_v(table):
    # Descriptive association only. Permit events need not be independent.
    from scipy.stats import chi2_contingency

    chi2, _, _, _ = chi2_contingency(table)
    return round(float((chi2 / (table.to_numpy().sum() * min(table.shape[0] - 1, table.shape[1] - 1))) ** .5), 3)


def main():
    raw = pd.read_csv(SOURCE, dtype=str, keep_default_na=False)
    assert len(raw) == 19420 and raw.EventID.is_unique, "Source size or IDs changed; audit before regenerating."
    malformed = ~raw.Borough.isin(BOROUGHS)
    df = raw.loc[~malformed].copy()
    for col in ["StartDateTime", "EndDateTime", "EnteredOn"]:
        df[col + "_parsed"] = pd.to_datetime(df[col], format=DATE_FMT, errors="coerce")
    df["year"] = df.StartDateTime_parsed.dt.year
    df["month"] = df.StartDateTime_parsed.dt.to_period("M")
    df["weekday"] = df.StartDateTime_parsed.dt.dayofweek
    df["duration_h"] = (df.EndDateTime_parsed - df.StartDateTime_parsed).dt.total_seconds() / 3600
    df["lead_d"] = (df.StartDateTime_parsed - df.EnteredOn_parsed).dt.total_seconds() / 86400

    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    valid_start = df.loc[df.StartDateTime_parsed.notna()]
    year_counts = valid_start.groupby("year").size()
    months = valid_start.groupby("month").size()
    monthly = [
        {"month": str(period), "count": int(count), "year": int(period.year)}
        for period, count in months.items()
    ]
    monthly_category_counts = valid_start.groupby(["month", "Category"]).size()
    monthly_category = [
        {"month": str(month), "category": category, "count": int(count)}
        for (month, category), count in monthly_category_counts.items()
    ]

    by_year = {}
    for key, frame in [("all", df)] + [(str(y), df.loc[df.year.eq(y)]) for y in [2023, 2024, 2025, 2026]]:
        matrix = pd.crosstab(frame.Category, frame.Borough).reindex(index=CATEGORIES, columns=BOROUGHS, fill_value=0)
        by_year[key] = {
            "n": int(len(frame)),
            "categories": count_series(frame.Category, CATEGORIES),
            "boroughs": count_series(frame.Borough, BOROUGHS),
            "matrix": [
                {"category": c, "borough": b, "count": int(matrix.loc[c, b])}
                for c in CATEGORIES for b in BOROUGHS
            ],
        }

    full_matrix = pd.crosstab(df.Category, df.Borough).reindex(index=CATEGORIES, columns=BOROUGHS, fill_value=0)
    from scipy.stats import chi2_contingency
    _, _, _, expected = chi2_contingency(full_matrix)
    residuals = [
        {
            "category": c, "borough": b,
            "count": int(full_matrix.loc[c, b]),
            "expected": round(float(expected[i, j]), 1),
            "residual": round(float((full_matrix.loc[c, b] - expected[i, j]) / expected[i, j] ** .5), 2),
        }
        for i, c in enumerate(CATEGORIES) for j, b in enumerate(BOROUGHS)
    ]

    valid_weekday = df.loc[df.weekday.notna()]
    weekday = [
        {"category": c, "day": day, "count": int(((valid_weekday.Category == c) & (valid_weekday.weekday == day)).sum())}
        for c in CATEGORIES for day in range(7)
    ]
    positive_duration = df.loc[df.duration_h.ge(0)]
    positive_lead = df.loc[df.lead_d.ge(0)]
    distributions = {
        "duration": {c: quantile_summary(positive_duration.loc[positive_duration.Category.eq(c), "duration_h"]) for c in CATEGORIES},
        "lead": {c: quantile_summary(positive_lead.loc[positive_lead.Category.eq(c), "lead_d"]) for c in CATEGORIES},
    }
    shooting = df.loc[df.EventType.eq("Shooting Permit")]
    shooting_matrix = pd.crosstab(shooting.Category, shooting.Borough)
    annual_change = round(float((year_counts[2025] / year_counts[2024] - 1) * 100), 1)
    quality = {
        "raw_rows": int(len(raw)), "raw_columns": int(len(raw.columns)),
        "unique_event_ids": int(raw.EventID.nunique()),
        "misaligned_rows": int(malformed.sum()), "analysis_rows": int(len(df)),
        "missing_start": int(df.StartDateTime_parsed.isna().sum()),
        "missing_end": int(df.EndDateTime_parsed.isna().sum()),
        "missing_entered": int(df.EnteredOn_parsed.isna().sum()),
        "duration_pairs": int(df.duration_h.notna().sum()),
        "duration_negative": int(df.duration_h.lt(0).sum()),
        "duration_over_7d": int(df.duration_h.gt(168).sum()),
        "lead_pairs": int(df.lead_d.notna().sum()),
        "lead_negative": int(df.lead_d.lt(0).sum()),
    }
    result = {
        "meta": {
            "source": SOURCE.name, "source_sha256": source_hash,
            "source_bytes": SOURCE.stat().st_size,
            "date_min": valid_start.StartDateTime_parsed.min().strftime("%Y-%m-%d"),
            "date_max": valid_start.StartDateTime_parsed.max().strftime("%Y-%m-%d"),
            "entered_max": df.EnteredOn_parsed.max().strftime("%Y-%m-%d"),
            "unit": "one row = one permit event (EventID)",
        },
        "quality": quality,
        "overview": {
            "annual": [{"year": int(y), "count": int(year_counts.get(y, 0))} for y in [2023, 2024, 2025, 2026]],
            "annual_change_2024_2025_pct": annual_change,
            "category_counts": count_series(df.Category, CATEGORIES),
            "borough_counts": count_series(df.Borough, BOROUGHS),
            "manhattan_share_all": round(float(df.Borough.eq("Manhattan").mean() * 100), 1),
            "manhattan_share_shooting": round(float(shooting.Borough.eq("Manhattan").mean() * 100), 1),
            "theater_manhattan_share": round(float(df.loc[df.Category.eq("Theater"), "Borough"].eq("Manhattan").mean() * 100), 1),
            "television_queens_share": round(float(df.loc[df.Category.eq("Television"), "Borough"].eq("Queens").mean() * 100), 1),
            "cramers_v_all": cramers_v(full_matrix),
            "cramers_v_shooting": cramers_v(shooting_matrix),
            "duration_median_hours": round(float(positive_duration.duration_h.median()), 1),
            "lead_median_days": round(float(positive_lead.lead_d.median()), 1),
            "weekend_share_theater": round(float(valid_weekday.loc[valid_weekday.Category.eq("Theater"), "weekday"].ge(5).mean() * 100), 1),
            "weekend_share_television": round(float(valid_weekday.loc[valid_weekday.Category.eq("Television"), "weekday"].ge(5).mean() * 100), 1),
        },
        "labels": {"boroughs": BOROUGHS, "categories": CATEGORIES},
        "monthly": monthly, "monthly_category": monthly_category,
        "by_year": by_year, "residuals": residuals,
        "weekday": weekday, "distributions": distributions,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}: {quality['analysis_rows']} usable rows, SHA-256 {source_hash}")
    print(json.dumps({"quality": quality, "overview": result["overview"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
