from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SRC = ROOT / "data/raw/central-park-squirrel-census.csv"

def records(frame):
    return json.loads(frame.to_json(orient="records"))

df = pd.read_csv(SRC, low_memory=False)
df["date"] = pd.to_datetime(df["Date"].astype("Int64").astype(str), format="%m%d%Y", errors="coerce")
df["shift"] = df["Shift"].fillna("Unknown")
df["fur_color"] = df["Primary Fur Color"].fillna("Unknown")
behavior_cols = ["Running", "Chasing", "Climbing", "Eating", "Foraging", "Kuks", "Quaas", "Moans", "Tail flags", "Tail twitches", "Approaches", "Indifferent", "Runs from"]
for c in behavior_cols:
    df[c] = df[c].astype(str).str.lower().eq("true")
profile = pd.DataFrame({"field": df.columns, "dtype": [str(df[c].dtype) for c in df.columns],
                        "missing_rate": [float(df[c].isna().mean()) for c in df.columns],
                        "unique_values": [int(df[c].nunique(dropna=True)) for c in df.columns]})
profile.to_csv(OUT / "eda_profile.csv", index=False)

colors = df.groupby("fur_color", as_index=False).size().rename(columns={"size": "squirrels"}).sort_values("squirrels", ascending=False)
shifts = df.groupby("shift", as_index=False).size().rename(columns={"size": "squirrels"}).sort_values("squirrels", ascending=False)
dates = df.groupby(["date", "shift"], as_index=False).size().rename(columns={"size": "squirrels"}).sort_values("date")
behavior = pd.DataFrame({"behavior": behavior_cols, "rate": [float(df[c].mean()) for c in behavior_cols]}).sort_values("rate", ascending=False)
behavior_shift = []
for shift, group in df.groupby("shift"):
    for c in behavior_cols:
        behavior_shift.append({"shift": shift, "behavior": c, "rate": float(group[c].mean())})
points = df[["X", "Y", "shift", "fur_color", "date", "Unique Squirrel ID"]].dropna(subset=["X", "Y"]).copy()
if len(points) > 3500:
    points = points.sample(3500, random_state=9)
grid = (df.dropna(subset=["X", "Y"]).assign(gx=lambda x: x["X"].round(3), gy=lambda x: x["Y"].round(3))
        .groupby(["gx", "gy"], as_index=False).size().rename(columns={"size": "squirrels"}).sort_values("squirrels", ascending=False).head(1500))

summary = {
    "dataset": "2018 Central Park Squirrel Census",
    "rows": int(len(df)), "columns": int(len(df.columns) - 1),
    "missing_rate": float(df.drop(columns=["date"]).isna().mean().mean()),
    "duplicate_rows": int(df.duplicated().sum()),
    "date_range": [str(df["date"].min().date()), str(df["date"].max().date())],
    "locations": int(df[["X", "Y"]].dropna().drop_duplicates().shape[0]),
    "findings": [
        "Rows represent squirrel observations made during the census, with a Unique Squirrel ID for traceability.",
        "X/Y are longitude/latitude-like coordinates and support a point map; they should not be interpreted as a precise tracking path.",
        "Behavior fields are mostly binary observations and are summarized as observation rates by shift.",
        "Missing fur color and narrative fields are kept as Unknown rather than imputed.",
    ],
}
(OUT / "eda_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
payload = {"summary": summary, "colors": records(colors), "shifts": records(shifts), "dates": records(dates), "behavior": records(behavior), "behavior_shift": behavior_shift, "points": records(points), "grid": records(grid)}
(OUT / "site").mkdir(exist_ok=True)
(OUT / "site/data.js").write_text("const DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=str) + ";")
print(json.dumps(summary, ensure_ascii=False, indent=2))
