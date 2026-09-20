from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SRC = ROOT / "data/raw/nasa-exoplanets-ps.csv"

def records(frame):
    return json.loads(frame.to_json(orient="records"))

df = pd.read_csv(SRC, low_memory=False)
df["status"] = np.select([
    df["soltype"].fillna("").str.contains("Confirmed", case=False),
    df["soltype"].fillna("").str.contains("Candidate", case=False),
], ["Confirmed", "Candidate"], default="Other")
df["disc_year"] = pd.to_numeric(df["disc_year"], errors="coerce")
for c in ["ra", "dec", "pl_orbper", "pl_eqt", "pl_rade", "st_teff", "sy_dist"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

profile = pd.DataFrame({"field": df.columns, "dtype": [str(df[c].dtype) for c in df.columns],
                        "missing_rate": [float(df[c].isna().mean()) for c in df.columns],
                        "unique_values": [int(df[c].nunique(dropna=True)) for c in df.columns]})
profile.to_csv(OUT / "eda_profile.csv", index=False)

trend = (df.dropna(subset=["disc_year"]).groupby(["disc_year", "status"], as_index=False).size()
         .rename(columns={"size": "planets"}).sort_values(["disc_year", "status"]))
methods = (df.groupby("discoverymethod", dropna=False).size().reset_index(name="planets")
           .assign(discoverymethod=lambda x: x["discoverymethod"].fillna("Unknown"))
           .sort_values("planets", ascending=False).head(12))
facilities = (df.groupby("disc_facility", dropna=False).size().reset_index(name="planets")
              .assign(disc_facility=lambda x: x["disc_facility"].fillna("Unknown"))
              .sort_values("planets", ascending=False).head(12))
sky = df.dropna(subset=["ra", "dec"])[["ra", "dec", "status", "discoverymethod", "pl_name"]].copy()
if len(sky) > 5000:
    sky = sky.sample(5000, random_state=7)
physical = df.dropna(subset=["pl_orbper", "pl_eqt", "pl_rade"])[["pl_orbper", "pl_eqt", "pl_rade", "status", "discoverymethod", "pl_name"]]
physical = physical.query("pl_orbper > 0 and pl_eqt > 0 and pl_rade > 0")
if len(physical) > 3000:
    physical = physical.sample(3000, random_state=7)

summary = {
    "dataset": "NASA Exoplanet Archive Planetary Systems",
    "rows": int(len(df)), "columns": int(len(df.columns) - 1),
    "missing_rate": float(df.drop(columns=["status"]).isna().mean().mean()),
    "duplicate_rows": int(df.duplicated().sum()),
    "date_range": [int(df["disc_year"].min()), int(df["disc_year"].max())],
    "confirmed_rate": float((df["status"] == "Confirmed").mean()),
    "candidate_rate": float((df["status"] == "Candidate").mean()),
    "findings": [
        "The table mixes published confirmed planets with several candidate catalogs; status is kept as a first-class dimension.",
        "Missingness is structural: uncertainty, mass and stellar fields are not measured for every discovery method.",
        "Transit discoveries dominate the archive, so counts describe the survey pipeline as much as the universe.",
        "Only a compact physical-variable sample is exported to D3; the full 355-column profile remains in eda_profile.csv.",
    ],
}
(OUT / "eda_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
payload = {"summary": summary, "trend": records(trend), "methods": records(methods),
           "facilities": records(facilities), "sky": records(sky), "physical": records(physical)}
(OUT / "site").mkdir(exist_ok=True)
(OUT / "site/data.js").write_text("const DATA = " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";")
print(json.dumps(summary, ensure_ascii=False, indent=2))
