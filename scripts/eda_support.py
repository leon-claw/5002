"""Shared, deterministic analytical primitives. No raw source file is modified."""

from pathlib import Path
import hashlib, json, math, sys
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
SEED = 20260920


def rec(df):
    return json.loads(df.to_json(orient="records", date_format="iso"))


def rho(df, x, y):
    d = df[[x, y]].replace([np.inf, -np.inf], np.nan).dropna()
    r = (
        stats.spearmanr(d[x], d[y]).statistic
        if len(d) > 2 and d[x].nunique() > 1 and d[y].nunique() > 1
        else None
    )
    return {"n": len(d), "rho": None if r is None or not np.isfinite(r) else float(r)}


def corr_matrix(df, cols, labels=None):
    labels = labels or cols
    return [
        dict(x=labels[j], y=labels[i], value=rho(df, a, b)["rho"], n=rho(df, a, b)["n"])
        for i, a in enumerate(cols)
        for j, b in enumerate(cols)
    ]


def quantiles(df, group, value, min_n=10):
    out = []
    for k, g in df.groupby(group, observed=True):
        s = g[value].dropna()
        if len(s) < min_n:
            continue
        q = s.quantile([0.1, 0.25, 0.5, 0.75, 0.9]).values
        out.append(
            dict(label=str(k), n=len(s), lo=q[0], q1=q[1], value=q[2], q3=q[3], hi=q[4])
        )
    return sorted(out, key=lambda d: d["value"], reverse=True)


def wilson(k, n):
    if not n:
        return None, None
    z = 1.959963984540054
    p = k / n
    den = 1 + z * z / n
    center = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return center - half, center + half


def sample(df, n=4500):
    return df.sample(n, random_state=SEED) if len(df) > n else df


def profile(df):
    rows = []
    for c in df:
        s = df[c]
        num = pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s)
        v = s.dropna()
        rows.append(
            dict(
                field=c,
                dtype=str(s.dtype),
                missing=int(s.isna().sum()),
                missing_rate=float(s.isna().mean()),
                unique_values=int(s.nunique()),
                median=float(v.median()) if num and len(v) else None,
                p01=float(v.quantile(0.01)) if num and len(v) else None,
                p99=float(v.quantile(0.99)) if num and len(v) else None,
            )
        )
    return pd.DataFrame(rows)


def chart(kind, title, note, data, **opts):
    return dict(kind=kind, title=title, note=note, data=data, **opts)


def finding(title, text):
    return dict(title=title, text=text)


def finish(
    out, raw, clean, meta, findings, charts, tables, sources, steps, limitations, checks
):
    out = Path(out)
    (out / "site").mkdir(exist_ok=True)
    profile(raw).to_csv(out / "eda_profile.csv", index=False)
    audit = out / "analysis"
    audit.mkdir(exist_ok=True)
    for name, table in tables.items():
        if isinstance(table, pd.DataFrame):
            table.to_csv(audit / (name + ".csv"), index=False)
        else:
            (audit / (name + ".json")).write_text(
                json.dumps(table, ensure_ascii=False, indent=2, allow_nan=False)
            )
    summary = dict(
        dataset=meta["title"],
        rows=len(raw),
        columns=len(raw.columns),
        missing_rate=float(raw.isna().mean().mean()),
        duplicate_rows=int(raw.duplicated().sum()),
        analysis_rows=len(clean),
        findings=findings,
        checks=checks,
    )
    (out / "eda_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False)
    )
    provenance = []
    for path in sources:
        p = ROOT / path
        provenance.append(
            dict(
                file=path,
                bytes=p.stat().st_size,
                sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
            )
        )
    payload = dict(
        meta=meta,
        summary=summary,
        charts=charts,
        steps=steps,
        limitations=limitations,
        provenance=provenance,
        seed=SEED,
    )
    # pandas JSON conversion normalizes numpy scalars and nonfinite values to JSON null.
    payload = json.loads(pd.Series([payload]).to_json(orient="values"))[0]
    (out / "site/data.js").write_text(
        "const DATA = "
        + json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False
        )
        + ";\n"
    )
    readme = (
        f"# {meta['title']}\n\n{meta['question']}\n\n## 数据集简介\n\n{meta.get('description', '')}\n\n**用途：** {meta.get('purpose', '')}\n\n**观测单位：** {meta.get('unit', '')}\n\n**来源说明：** {meta.get('source_note', '')}\n\n## 复现\n\n从仓库根目录运行 `python3 projects/{out.name}/eda.py`，再运行 `python3 scripts/build_sites.py`。依赖见根目录 requirements.txt。\n\n## 分析过程\n\n"
        + "\n".join(f"{i + 1}. {s}" for i, s in enumerate(steps))
        + "\n\n## 实际计算的结论\n\n"
        + "\n\n".join("### " + f["title"] + "\n\n" + f["text"] for f in findings)
        + "\n\n## 局限\n\n"
        + "\n".join("- " + s for s in limitations)
        + "\n\n## 可审计产物\n\n`eda_profile.csv` 是原始字段统计，`analysis/` 保存全量分析汇总；页面抽样不用于计算结论。`site/data.js` 保存可视化数据。原始文件的 SHA-256 记录在页面的数据来源区域。\n"
    )
    (out / "README.md").write_text(readme)
    print(
        f"{out.name}: raw {len(raw):,} × {len(raw.columns)}; analysis {len(clean):,}; {len(charts)} views; {len(findings)} findings"
    )
