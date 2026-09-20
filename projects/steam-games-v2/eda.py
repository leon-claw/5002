from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BASE = ROOT / "data/processed/steam"

def records(frame):
    return json.loads(frame.to_json(orient="records"))

main_raw = pd.read_csv(BASE / "extended_steam_games.csv", low_memory=False)
wiki_raw = pd.read_csv(BASE / "steam_games_wikidata.csv", low_memory=False)
spy_raw = pd.read_csv(BASE / "steamspy_raw.csv", low_memory=False)
dupes = {"main": int(main_raw.duplicated("appid").sum()), "wikidata": int(wiki_raw.duplicated("appid").sum()), "steamspy": int(spy_raw.duplicated("appid").sum())}
main = main_raw.drop_duplicates("appid", keep="last").copy()
wiki = wiki_raw.drop_duplicates("appid", keep="last")
spy = spy_raw.drop_duplicates("appid", keep="last")
merged = main.merge(wiki[["appid", "esrb_rating", "game_engine"]], on="appid", how="left", indicator="wiki_join")
merged = merged.merge(spy[["appid", "ccu"]].rename(columns={"ccu": "steamspy_ccu"}), on="appid", how="left", indicator="spy_join")
merged["release"] = pd.to_datetime(merged["release_date"], errors="coerce", dayfirst=True)
merged["year"] = merged["release"].dt.year
for c in ["positive", "negative", "ccu", "price"]:
    merged[c] = pd.to_numeric(merged[c], errors="coerce")
merged["review_ratio"] = merged["positive"] / (merged["positive"] + merged["negative"]).replace(0, np.nan)
profile = pd.DataFrame({"field": main.columns, "dtype": [str(main[c].dtype) for c in main.columns], "missing_rate": [float(main[c].isna().mean()) for c in main.columns], "unique_values": [int(main[c].nunique(dropna=True)) for c in main.columns]})
profile.to_csv(OUT / "eda_profile.csv", index=False)
release = merged.dropna(subset=["year"]).query("year >= 1990 and year <= 2026").groupby("year", as_index=False).agg(games=("appid", "count"), median_price=("price", "median"))
genres = (merged[["appid", "genres"]].dropna().assign(genre=lambda x: x["genres"].str.split(",\\s*")).explode("genre").groupby("genre", as_index=False).agg(games=("appid", "nunique")).sort_values("games", ascending=False).head(18))
scatter = merged[["appid", "name", "price", "positive", "negative", "ccu", "review_ratio", "genres", "year"]].dropna(subset=["price", "positive", "ccu"]).copy().query("positive >= 0 and ccu >= 0")
if len(scatter) > 3500:
    scatter = scatter.sample(3500, random_state=11)
coverage = pd.DataFrame({"source": ["Extended main", "Wikidata", "SteamSpy"], "rows": [len(main), len(wiki), len(spy)], "unique_appid": [main["appid"].nunique(), wiki["appid"].nunique(), spy["appid"].nunique()], "matched_to_main": [len(main), int(merged["wiki_join"].eq("both").sum()), int(merged["spy_join"].eq("both").sum())]})
summary = {"dataset": "Steam Games Dataset V2", "rows": int(len(main)), "columns": int(len(main.columns)), "missing_rate": float(main.isna().mean().mean()), "duplicate_rows": int(main_raw.duplicated().sum()), "appid_duplicates": dupes, "wikidata_match_rate": float(merged["wiki_join"].eq("both").mean()), "steamspy_match_rate": float(merged["spy_join"].eq("both").mean()), "findings": [f"The main table has {dupes['main']} repeated appid rows; the EDA keeps the last row and reports the decision.", "Wikidata and SteamSpy are left joins, so unmatched games remain visible rather than being dropped.", "Review ratio is defined as positive / (positive + negative) and is not a Steam recommendation probability.", "Release dates are messy text; only years parsed into 1990–2026 are used in the trend view."]}
(OUT / "eda_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
payload = {"summary": summary, "release": records(release), "genres": records(genres), "scatter": records(scatter), "coverage": records(coverage)}
(OUT / "site").mkdir(exist_ok=True)
(OUT / "site/data.js").write_text("const DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=str) + ";")
print(json.dumps(summary, ensure_ascii=False, indent=2))
