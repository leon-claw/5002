from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SRC = ROOT / "data/raw/nyc-film-permits-historical.csv"

def records(frame):
    return json.loads(frame.to_json(orient="records", date_format="iso"))

df = pd.read_csv(SRC, low_memory=False)
df["EventStartDate"] = pd.to_datetime(df["EventStartDate"], errors="coerce")
df["EventEndDate"] = pd.to_datetime(df["EventEndDate"], errors="coerce")
df["year"] = df["EventStartDate"].dt.year.astype("Int64")
df["duration_days"] = (df["EventEndDate"] - df["EventStartDate"]).dt.days
df["Boro_clean"] = df["Boro"].fillna("Unknown").replace({"": "Unknown"})
df["EventType_clean"] = df["EventType"].fillna("Unknown")
df["Category_clean"] = df["CategoryName"].fillna("Unknown")

profile = pd.DataFrame({
    "field": df.columns,
    "dtype": [str(df[c].dtype) for c in df.columns],
    "missing_rate": [float(df[c].isna().mean()) for c in df.columns],
    "unique_values": [int(df[c].nunique(dropna=True)) for c in df.columns],
})
profile.to_csv(OUT / "eda_profile.csv", index=False)

trend = (df.dropna(subset=["year"]).groupby("year", as_index=False)
         .agg(permits=("ProjectId", "size"), projects=("ProjectId", "nunique"))
         .sort_values("year"))
trend_borough = (df.dropna(subset=["year"]).groupby(["Boro_clean", "year"], as_index=False)
                 .agg(permits=("ProjectId", "size"), projects=("ProjectId", "nunique"))
                 .sort_values("year"))
borough = (df.groupby("Boro_clean", as_index=False).agg(permits=("ProjectId", "size"), projects=("ProjectId", "nunique"))
           .sort_values("permits", ascending=False))
event_types = (df.groupby("EventType_clean", as_index=False).size().rename(columns={"size": "permits"})
               .sort_values("permits", ascending=False).head(12))
categories = (df.groupby("Category_clean", as_index=False).size().rename(columns={"size": "permits"})
              .sort_values("permits", ascending=False).head(12))
companies = (df.assign(company=df["CompanyName"].fillna("Unknown"))
             .groupby("company", as_index=False).size().rename(columns={"size": "permits"})
             .sort_values("permits", ascending=False).head(15))
duration = (df.dropna(subset=["duration_days"])
            .query("duration_days >= 0 and duration_days <= 365")
            .groupby("year", as_index=False).agg(median_days=("duration_days", "median"), mean_days=("duration_days", "mean")))

summary = {
    "dataset": "NYC Film Permits Historical",
    "rows": int(len(df)), "columns": int(len(df.columns) - 3),
    "missing_rate": float(df.drop(columns=["year", "duration_days", "Boro_clean", "EventType_clean", "Category_clean"]).isna().mean().mean()),
    "duplicate_rows": int(df.duplicated().sum()),
    "date_range": [str(df["EventStartDate"].min().date()), str(df["EventStartDate"].max().date())],
    "boroughs": int(df["Boro_clean"].nunique()),
    "projects": int(df["ProjectId"].nunique()),
    "findings": [
        "Permit records are event-level, so one project can appear across multiple permit events.",
        f"The file contains {int(df.duplicated().sum())} exact duplicate rows; they are retained and flagged for audit.",
        "Borough is missing for a meaningful minority of records; Unknown is kept as an explicit category.",
        "There are no reliable coordinates, so the D3 view uses borough and time rather than inventing point locations.",
    ],
}
(OUT / "eda_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))

payload = {
    "summary": summary,
    "trend": records(trend), "trend_borough": records(trend_borough), "borough": records(borough), "event_types": records(event_types),
    "categories": records(categories), "companies": records(companies), "duration": records(duration),
}
(OUT / "site").mkdir(exist_ok=True)
(OUT / "site/data.js").write_text("const DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";")
print(json.dumps(summary, ensure_ascii=False, indent=2))
