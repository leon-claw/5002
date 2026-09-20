from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SRC = ROOT / "data/processed/world-happiness/world_happiness.csv"

def records(frame):
    return json.loads(frame.to_json(orient="records"))

raw = pd.read_csv(SRC)
df = raw.rename(columns={
    "Year": "year", "Rank": "rank", "Country name": "country",
    "Life evaluation (3-year average)": "life", "Lower whisker": "lower", "Upper whisker": "upper",
    "Explained by: Log GDP per capita": "gdp", "Explained by: Social support": "social_support",
    "Explained by: Healthy life expectancy": "health", "Explained by: Freedom to make life choices": "freedom",
    "Explained by: Generosity": "generosity", "Explained by: Perceptions of corruption": "corruption",
    "Dystopia + residual": "dystopia",
})
profile = pd.DataFrame({"field": df.columns, "dtype": [str(df[c].dtype) for c in df.columns], "missing_rate": [float(df[c].isna().mean()) for c in df.columns], "unique_values": [int(df[c].nunique(dropna=True)) for c in df.columns]})
profile.to_csv(OUT / "eda_profile.csv", index=False)
latest_year = int(df["year"].max())
latest = df[df["year"] == latest_year].sort_values("rank")
top_bottom = pd.concat([latest.head(10), latest.tail(10)]).drop_duplicates("country")
trend_countries = latest.head(8)["country"].tolist()
trend = df[df["country"].isin(trend_countries)].sort_values(["country", "year"])
components = latest.head(8)[["country", "gdp", "social_support", "health", "freedom", "generosity", "corruption", "dystopia"]]
intervals = latest.head(18)[["country", "rank", "life", "lower", "upper"]]
summary = {
    "dataset": "World Happiness Report 2026 Figure 2.1", "rows": int(len(df)), "columns": int(len(df.columns)),
    "missing_rate": float(df.isna().mean().mean()), "duplicate_rows": int(df.duplicated().sum()),
    "date_range": [int(df["year"].min()), latest_year], "countries": int(df["country"].nunique()),
    "findings": [
        "Life evaluation is reported as a three-year average, so year-to-year changes are smoothed rather than annual survey scores.",
        "The latest ranking is paired with whisker intervals; close ranks should not be over-interpreted.",
        "Older years contain structural missingness because country coverage changes across report editions.",
        "The explanatory components are descriptive contributions to the reported evaluation, not causal estimates.",
    ],
}
(OUT / "eda_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
payload = {"summary": summary, "latest": records(top_bottom), "trend": records(trend), "components": records(components), "intervals": records(intervals), "trend_countries": trend_countries}
(OUT / "site").mkdir(exist_ok=True)
(OUT / "site/data.js").write_text("const DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";")
print(json.dumps(summary, ensure_ascii=False, indent=2))
