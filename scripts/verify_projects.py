"""Independent source reconciliation and artifact/data contracts."""

from pathlib import Path
import json, re, hashlib
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
slugs = [
    "nyc-film-permits",
    "nasa-exoplanets",
    "college-majors-2026",
    "central-park-squirrels",
    "steam-games-v2",
    "world-happiness",
]
data = {}
for slug in slugs:
    p = ROOT / "projects" / slug
    d = json.loads(
        (p / "site/data.js")
        .read_text()
        .removeprefix("const DATA = ")
        .strip()
        .removesuffix(";")
    )
    data[slug] = d
    s = d["summary"]
    text = (p / "index.html").read_text()
    assert len(d["charts"]) >= 6 and len(s["findings"]) >= 3
    for f in s["findings"]:
        assert f["title"] in text and f["text"] in text
    assert "https://cdn." not in text
    prof = pd.read_csv(p / "eda_profile.csv")
    assert len(prof) == s["columns"]
    assert np.isclose(prof.missing_rate.mean(), s["missing_rate"])
    for source in d["provenance"]:
        assert (
            hashlib.sha256((ROOT / source["file"]).read_bytes()).hexdigest()
            == source["sha256"]
        )
    for c in d["charts"]:
        assert c["data"], (slug, c["title"])
        if c["kind"] == "scatter":
            assert len(c["data"]) <= c["population"]
            for row in c["data"]:
                assert row["x"] is not None and row["y"] is not None
                if c.get("scaleX") == "log":
                    assert row["x"] > 0
                if c.get("scaleY") == "log":
                    assert row["y"] > 0
        if c["kind"] in ["interval", "box"]:
            for row in c["data"]:
                assert row["lo"] <= row["value"] <= row["hi"]
    print(
        f"{slug}: {len(d['charts'])} charts, {s['rows']:,} × {s['columns']} raw, {s['analysis_rows']:,} analysis"
    )
f = pd.read_csv(ROOT / "data/raw/nyc-film-permits-historical.csv")
assert len(f.drop_duplicates()) == data[slugs[0]]["summary"]["analysis_rows"]
assert data[slugs[0]]["summary"]["columns"] == 11
n = pd.read_csv(
    ROOT / "data/raw/nasa-exoplanets-ps.csv",
    usecols=["pl_name", "soltype", "default_flag"],
)
n = n[(n.soltype == "Published Confirmed") & (n.default_flag == 1)]
assert len(n) == n.pl_name.nunique() == data[slugs[1]]["summary"]["analysis_rows"]
c = pd.read_csv(
    ROOT / "data/processed/college-majors/college_majors_2026.csv",
    usecols=[
        "median_earnings_4yr_usd",
        "median_debt_usd",
        "earnings_4yr_status",
        "debt_status",
    ],
)
valid = c[
    c.earnings_4yr_status.eq("reported")
    & c.debt_status.eq("reported")
    & c.median_earnings_4yr_usd.gt(0)
    & c.median_debt_usd.ge(0)
]
assert len(valid) == data[slugs[2]]["summary"]["analysis_rows"]
s = pd.read_csv(ROOT / "data/raw/central-park-squirrel-census.csv")
assert len(s.columns) == 31
assert (
    s["Unique Squirrel ID"].duplicated().sum()
    == data[slugs[3]]["summary"]["checks"]["duplicate_id_excess"]
    == 5
)
st = pd.read_csv(ROOT / "data/processed/steam/extended_steam_games.csv")
assert st.appid.nunique() == data[slugs[4]]["summary"]["analysis_rows"]
clean = pd.read_csv(ROOT / "projects/steam-games-v2/analysis/canonical_games.csv")
assert clean.appid.is_unique
# Verify cent conversion for every non-conflicting appid against the raw value.
unique = st[~st.appid.duplicated(False)][["appid", "price"]].merge(
    clean[["appid", "usd"]], on="appid", validate="one_to_one"
)
assert np.allclose(unique.price / 100, unique.usd, equal_nan=True)
h = pd.read_excel(ROOT / "data/raw/world-happiness-report-2026-figure-2-1.xlsx")
balanced = set.intersection(*(set(g["Country name"]) for _, g in h.groupby("Year")))
assert len(balanced) == data[slugs[5]]["summary"]["checks"]["balanced_countries"]
assert not h.duplicated(["Country name", "Year"]).any()
print(
    "Source counts, corrected units, raw profiles, evidence text, population filters and source hashes verified."
)
