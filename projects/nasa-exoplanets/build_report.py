"""Reproduce the original EDA, extend its audit, and build the coursework report.

Run from any directory: python3 /path/to/projects/nasa-exoplanets/build_report.py
No download or raw-data mutation occurs. Statistical results use every eligible row.
"""
from pathlib import Path
import json
import runpy
import sys
import hashlib
import platform
import numpy as np
import pandas as pd
import scipy
from scipy import stats

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT))
base = runpy.run_path(str(OUT / 'eda.py'))
raw, df = base['raw'], base['df']
fields, labels = base['fields'], base['labels']
payload = json.loads((OUT / 'site/data.js').read_text().removeprefix('const DATA = ').strip().removesuffix(';'))
original = raw[(raw.default_flag == 1) & (raw.soltype == 'Published Confirmed')].copy()
SEED, REPS = 20261001, 1000

def records(frame):
    return json.loads(frame.to_json(orient='records'))

def write_json(name, value):
    (OUT / 'analysis' / (name + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')

def rank_correlation(frame):
    pair = frame[['pl_orbper', 'pl_rade']].dropna()
    return {'n': len(pair), 'rho': float(stats.spearmanr(pair.pl_orbper, pair.pl_rade).statistic)}

pair = df.dropna(subset=['pl_orbper', 'pl_rade'])
# Host-level bootstrap preserves dependence among planets sharing one host.
clusters = [g[['pl_orbper', 'pl_rade']].to_numpy() for _, g in pair.groupby('hostname')]
rng = np.random.default_rng(SEED)
boot = []
for _ in range(REPS):
    sampled = np.concatenate([clusters[i] for i in rng.integers(0, len(clusters), len(clusters))])
    boot.append(float(stats.spearmanr(sampled[:, 0], sampled[:, 1]).statistic))
ci = np.quantile(boot, [.025, .975])
sensitivity = [dict(label='主分析', **rank_correlation(df))]
sensitivity.append(dict(label='排除争议标记', **rank_correlation(df.loc[df.pl_controv_flag.eq(0)])))
central = pair.copy()
for c in ['pl_orbper', 'pl_rade']:
    lo, hi = pair[c].quantile([.01, .99])
    central = central.loc[central[c].between(lo, hi)]
sensitivity.append(dict(label='双变量均在 P1–P99 内', **rank_correlation(central)))

descriptive = []
for c, label in zip(fields, labels):
    values = df[c].dropna()
    before = original[c]
    q = values.quantile([.1, .25, .5, .75, .9])
    iqr = q.loc[.75] - q.loc[.25]
    limcol = c + 'lim'
    limits = original[limcol].fillna(0).ne(0) if limcol in original else pd.Series(False, index=original.index)
    descriptive.append(dict(field=c, label=label, n=len(values), raw_missing=int(before.isna().sum()), limits=int(limits.sum()), limit_values=int((limits & before.notna()).sum()), nonpositive=int((before.le(0) & ~limits).sum()), missing=int(df[c].isna().sum()), missing_pct=float(df[c].isna().mean()*100), mean=float(values.mean()), std=float(values.std()), minimum=float(values.min()), p10=float(q.loc[.1]), q1=float(q.loc[.25]), median=float(q.loc[.5]), q3=float(q.loc[.75]), p90=float(q.loc[.9]), maximum=float(values.max()), iqr_outliers=int((values.lt(q.loc[.25]-1.5*iqr) | values.gt(q.loc[.75]+1.5*iqr)).sum())))

method_counts = df.discoverymethod.value_counts()
method_table = [dict(label=m, value=int(n), share=float(n/len(df)*100), period_radius=int(pair.discoverymethod.eq(m).sum()), radius=int(df.loc[df.discoverymethod.eq(m), 'pl_rade'].notna().sum())) for m, n in method_counts.items()]
log_radius = np.log10(df.pl_rade.dropna())
edges = np.linspace(log_radius.min(), log_radius.max(), 25)
hist = []
for method in ['全部', *method_counts.index]:
    v = df.loc[df.discoverymethod.eq(method), 'pl_rade'].dropna() if method != '全部' else df.pl_rade.dropna()
    counts, _ = np.histogram(np.log10(v), bins=edges)
    hist.append(dict(group=method, n=len(v), bins=[dict(lo=float(10**edges[i]), hi=float(10**edges[i+1]), count=int(count)) for i, count in enumerate(counts)]))

corfields = ['pl_orbper', 'pl_rade', 'pl_orbsmax', 'pl_eqt', 'st_teff', 'sy_dist']
corlabels = ['周期', '半径', '半长轴', '平衡温度', '恒星温度', '距离']
corr = []
for a, al in zip(corfields, corlabels):
    for b, bl in zip(corfields, corlabels):
        pp = df[[a, b]].dropna() if a != b else df[[a]].dropna()
        value = float(stats.spearmanr(pp[a], pp[b]).statistic) if a != b and len(pp)>2 else (1.0 if len(pp)>2 else None)
        corr.append(dict(x=bl, y=al, value=value, n=len(pp)))

audit = dict(raw_rows=len(raw), raw_columns=len(raw.columns), exact_duplicate_rows=int(raw.duplicated().sum()), raw_unique_names=int(raw.pl_name.nunique()), published_confirmed_rows=int(raw.soltype.eq('Published Confirmed').sum()), default_rows=int(raw.default_flag.eq(1).sum()), nonconfirmed_default_rows=int(((raw.default_flag==1)&raw.soltype.ne('Published Confirmed')).sum()), planets=len(df), hosts=int(df.hostname.nunique()), multiple_planet_hosts=int(df.hostname.value_counts().ge(2).sum()), confirmed_exact_duplicates=int(original.duplicated().sum()), controversial=int(df.pl_controv_flag.eq(1).sum()), year_min=int(df.disc_year.min()), year_max=int(df.disc_year.max()), max_rowupdate=str(pd.to_datetime(raw.rowupdate, errors='coerce').max().date()), source_bytes=(base['ROOT']/base['source']).stat().st_size, sha256=hashlib.sha256((base['ROOT']/base['source']).read_bytes()).hexdigest(), complete_case_transit_pct=float(pair.discoverymethod.eq('Transit').mean()*100), radius_n=int(df.pl_rade.notna().sum()), mass_radius_n=len(base['mass']), radius_median=float(df.pl_rade.median()), period_median=float(df.pl_orbper.median()))
bootstrap = dict(rho=rank_correlation(df)['rho'], low=float(ci[0]), high=float(ci[1]), replicates=REPS, seed=SEED, cluster_unit='hostname', clusters=len(clusters), method='percentile host-cluster bootstrap; 2.5% and 97.5%', scope='Conditional on observed host systems; does not correct detection selection or missingness.')
report = dict(audit=audit, descriptive=descriptive, methods=method_table, histograms=hist, correlation_matrix=corr, bootstrap=bootstrap, sensitivity=sensitivity, versions=dict(python=platform.python_version(), pandas=pd.__version__, numpy=np.__version__, scipy=scipy.__version__))
write_json('report', report)
pd.DataFrame(descriptive).to_csv(OUT/'analysis/descriptive_statistics.csv', index=False)
pd.DataFrame(method_table).to_csv(OUT/'analysis/discovery_methods.csv', index=False)
pd.DataFrame(sensitivity).to_csv(OUT/'analysis/sensitivity.csv', index=False)
write_json('bootstrap', bootstrap)

# Preserve the existing chart identities, append three analytical views.
payload['charts'] += [
    dict(kind='bar', title='发现方法构成：样本的入口并不均匀', note=f'分母为全部 {len(df):,} 颗默认已确认行星；显示所有 {len(method_table)} 种方法，计数不等于探测效率。', data=[dict(label=m['label'], value=m['value']) for m in method_table], unit='颗'),
    dict(kind='histogram', title='半径分布：用对数尺度看长尾', note='24 个 log₁₀ 等宽箱，箱边界在筛选前固定；计数图的柱宽代表倍数区间，不是线性半径区间。', data=hist, xLabel='半径 / 地球半径', yLabel='行星数'),
    dict(kind='heatmap', title='物理参数的秩相关：先检查共同测量样本', note='每个单元格各用成对完整样本，悬停显示 n；质量因来源混杂而不纳入。正负关系都不代表因果。', data=corr, diverging=True, fixedDomain=1),
]
payload['report'] = report
payload['methodOrder'] = sorted(method_counts.index.tolist())
payload['meta']['source_note'] = f'使用用户提供的 PS 92 列固定导出；文件中最新 rowupdate 为 {audit["max_rowupdate"]}。本次不实时更新数据，文件头导出时间为 2026-10-01 06:21:14，时区未注明。'
payload['charts'][5]['note'] = '只保留 pl_bmassprov=Mass 的质量，排除 Msini 等来源；质量与半径均须为正、非限制值且完整。'
payload['charts'][2]['data'] = [dict(label=x['label'], n=x['n'], rho=x['rho'], support=('n<30，极小样本' if x['n']<30 else '探索性关联')) for x in payload['charts'][2]['data']]
(OUT/'site/data.js').write_text('const DATA = '+json.dumps(payload, ensure_ascii=False, separators=(',', ':'), allow_nan=False)+';\n', encoding='utf-8')
# Preserve all metadata descriptions supplied by NASA in the CSV comment header.
import re
field_dictionary = []
for line in (base['ROOT']/base['source']).read_text(encoding='utf-8').splitlines():
    if not line.startswith('#'): break
    match = re.match(r'# COLUMN ([^:]+):\s*(.*)', line)
    if match:
        field_dictionary.append(dict(field=match.group(1).strip(), description=match.group(2).strip()))
assert len(field_dictionary) == len(raw.columns)
pd.DataFrame(field_dictionary).to_csv(OUT/'analysis/field_dictionary.csv',index=False)

from report_page import render_report
(OUT/'index.html').write_text(render_report(payload), encoding='utf-8')
print(f'Report built: {len(payload["charts"])} views; radius n={audit["radius_n"]}; rho={bootstrap["rho"]:.4f}, host bootstrap [{ci[0]:.4f}, {ci[1]:.4f}]')

(OUT/'README.md').write_text(f"""# NASA 系外行星 EDA 与 D3.js 研究报告

基于用户提供的 `PS_2026.10.01_06.21.14.csv`，不是工作目录中的旧快照。

## 启动网页

```sh
cd projects/nasa-exoplanets
npm start
```

浏览器打开 http://127.0.0.1:3000 。仅需 Node.js 18+，无需 npm install，D3 v7.9.0 随项目保存，展示不需要联网。端口冲突可用 `PORT=3001 npm start`。

## 重现分析与验证

```sh
python3 -m pip install -r requirements.txt
npm run analyze
npm test
```

必须运行 `build_report.py`（即 npm run analyze）以生成完整报告。基础 eda.py 只生成基础数据；不要使用旧的全项目 build_sites.py 覆盖报告。本项目自带原始 CSV 与 eda_support.py，可以单独复制提交。重新分析不需要 NASA API 或 Downloads 原文件。

## 数据与口径

- 导出文件头时间：2026-10-01 06:21:14，时区未注明。
- 原始 {len(raw):,} 行 × {len(raw.columns)} 列；PS 一行是一颗行星的一套参考参数，不是唯一行星。
- 主样本：default_flag=1 且 soltype=Published Confirmed；{len(df):,} 颗唯一行星。
- 参数独立剔除非零限制标记与非正值；不插补，不自动删除 IQR 极端值。
- 质量–半径仅保留 pl_bmassprov=Mass，排除推算质量和最小质量混用。
- 全量有效点参与绘图和统计，未进行展示抽样。

## 分析结果

周期–半径 Spearman ρ={bootstrap['rho']:.4f}；按宿主系统 bootstrap 的 95% percentile 区间 [{bootstrap['low']:.4f}, {bootstrap['high']:.4f}]，1000 次，固定种子 20261001。结果仅描述观测样本中的弱单调关系，不能推断因果或真实宇宙丰度。

网页包含研究问题、92 字段审计、核心字典、缺失与限制值处理、描述统计、八幅 D3 图和一张相关统计表、分组与敏感性分析、局限及官方来源。图表支持悬停、方法筛选、散点框选联动、历史截止年调整及 SVG 导出；支持打印报告。

## 文件

- index.html / site/：可离线展示的中文报告与 D3 图表。
- data/：用户原始导出，逐字节保留。
- analysis/：清洗 CSV、描述统计、缺失矩阵、相关、bootstrap、敏感性与完整 JSON。
- eda_profile.csv：所有原始字段的类型、缺失与分位数审计。
- build_report.py / eda.py / eda_support.py / report_page.py：可复现分析和页面生成代码。
- server.js：Node.js 本地静态服务；server.test.js 为 HTTP 集成测试。
- verify_report.py：独立核查附件口径、统计、分箱计数守恒和本地链接。

原始 CSV SHA-256：`{audit['sha256']}`。
""", encoding='utf-8')
