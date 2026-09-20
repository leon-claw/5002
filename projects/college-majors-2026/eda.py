from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SRC = ROOT / "data/processed/college-majors/college_majors_2026.csv"

def records(frame):
    return json.loads(frame.to_json(orient="records"))

df = pd.read_csv(SRC, low_memory=False)
profile = pd.DataFrame({"field": df.columns, "dtype": [str(df[c].dtype) for c in df.columns],
                        "missing_rate": [float(df[c].isna().mean()) for c in df.columns],
                        "unique_values": [int(df[c].nunique(dropna=True)) for c in df.columns]})
profile.to_csv(OUT / "eda_profile.csv", index=False)

work = df.copy()
work["family"] = work["cip_family_title"].fillna("Unknown")
work["trajectory"] = work["earnings_trajectory_category"].fillna("Unknown")
work["state"] = work["institution_state"].fillna("Unknown")
family = (work.groupby("family", as_index=False)
          .agg(programs=("program_id", "count"), median_earnings=("median_earnings_4yr_usd", "median"),
               median_debt=("median_debt_usd", "median"), working_5yr=("pct_working_5yr", "median"),
               ai_share=("ai_software_occupation_share", "median"), growth=("earnings_growth_pct_1yr_to_5yr", "median"))
          .query("programs >= 25").sort_values("median_earnings", ascending=False).head(16))
state = (work.groupby("state", as_index=False)
         .agg(programs=("program_id", "count"), median_earnings=("median_earnings_4yr_usd", "median"),
              median_debt=("median_debt_usd", "median"), ai_share=("ai_software_occupation_share", "median"))
         .query("state != 'Unknown' and programs >= 20").sort_values("median_earnings", ascending=False).head(15))
trajectory = work.groupby("trajectory", as_index=False).agg(programs=("program_id", "count"), median_earnings=("median_earnings_4yr_usd", "median"), median_growth=("earnings_growth_pct_1yr_to_5yr", "median")).sort_values("programs", ascending=False)
scatter = work[["program_id", "cip_title", "family", "median_earnings_4yr_usd", "median_debt_usd", "ai_software_occupation_share", "pct_working_5yr", "earnings_trajectory_category"]].dropna(subset=["median_earnings_4yr_usd", "median_debt_usd"]).copy()
if len(scatter) > 3500:
    scatter = scatter.sample(3500, random_state=21)
scatter = scatter.replace({np.nan: None})
ai = (work.assign(ai_bin=pd.cut(work["ai_software_occupation_share"], bins=[-1, .05, .15, .3, 1], labels=["0–5%", "5–15%", "15–30%", "30%+"]))
       .groupby("ai_bin", observed=False, as_index=False).agg(programs=("program_id", "count"), median_earnings=("median_earnings_4yr_usd", "median")))

summary = {
    "dataset": "College Majors 2026 Earnings, Debt, Jobs & AI",
    "rows": int(len(df)), "columns": int(len(df.columns)),
    "missing_rate": float(df.isna().mean().mean()),
    "duplicate_rows": int(df.duplicated().sum()),
    "families": int(work["family"].nunique()), "institutions": int(work["institution_name"].nunique()),
    "findings": [
        "Rows are institution × CIP program × credential observations, not individual graduates.",
        "Privacy suppression and small cohorts make displayed medians unsuitable for precise causal claims.",
        "The page compares income, debt and AI exposure as descriptive signals; it does not infer that AI causes earnings.",
        "State aggregates exclude Unknown and require a minimum program count to reduce unstable rankings.",
    ],
}
(OUT / "eda_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
payload = {"summary": summary, "family": records(family), "state": records(state), "trajectory": records(trajectory), "scatter": records(scatter), "ai": records(ai)}
(OUT / "site").mkdir(exist_ok=True)
(OUT / "site/data.js").write_text("const DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";")
print(json.dumps(summary, ensure_ascii=False, indent=2))
