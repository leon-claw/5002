"""Independent artifact checks against the preserved user CSV; no report rebuild."""
from pathlib import Path
import hashlib, json, re
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
P = Path(__file__).resolve().parent
source = P / 'data/PS_2026.10.01_06.21.14.csv'
raw = pd.read_csv(source, comment='#', low_memory=False)
p = json.loads((P/'site/data.js').read_text().removeprefix('const DATA = ').strip().removesuffix(';'))
r = p['report']; a = r['audit']
assert (a['raw_rows'], a['raw_columns']) == raw.shape == (40188,92)
assert a['sha256'] == hashlib.sha256(source.read_bytes()).hexdigest()
df = raw.loc[raw.default_flag.eq(1) & raw.soltype.eq('Published Confirmed')].copy()
assert df.pl_name.is_unique and len(df) == a['planets'] == 6298
assert df.hostname.nunique() == a['hosts']
for row in r['descriptive']:
    field = row['field']; limit = field+'lim'
    mask = df[limit].fillna(0).ne(0) if limit in df else pd.Series(False,index=df.index)
    df.loc[mask | df[field].le(0),field] = np.nan
    assert row['n'] == df[field].notna().sum()
    assert row['raw_missing']+row['limit_values']+row['nonpositive'] == row['missing']
    assert np.isclose(row['median'], df[field].median())
    assert row['n']+row['missing'] == len(df)
pair = df.dropna(subset=['pl_orbper','pl_rade'])
assert p['charts'][0]['population'] == len(pair) == len(p['charts'][0]['data'])
assert np.isclose(r['bootstrap']['rho'],spearmanr(pair.pl_orbper,pair.pl_rade).statistic)
assert r['bootstrap']['clusters'] == pair.hostname.nunique()
assert -1 <= r['bootstrap']['low'] <= r['bootstrap']['high'] <= 1
mass=df.loc[df.pl_bmassprov.eq('Mass')].dropna(subset=['pl_bmasse','pl_rade'])
assert len(mass)==a['mass_radius_n']==len(p['charts'][5]['data'])
assert set(x['label'] for x in p['charts'][5]['data'])==set(mass.pl_name)
assert sum(row['value'] for row in r['methods'])==len(df)
assert sum(x['value'] for x in p['charts'][4]['data'])==len(df)
for group in r['histograms']:
    data=df if group['group']=='全部' else df[df.discoverymethod.eq(group['group'])]
    assert sum(x['count'] for x in group['bins'])==group['n']==data.pl_rade.notna().sum()
    edges=[x['lo'] for x in group['bins']]+[group['bins'][-1]['hi']]
    assert all(x>0 for x in edges) and np.all(np.diff(edges)>0)
    assert np.allclose(np.diff(np.log10(edges)),np.diff(np.log10(edges))[0])
for c in r['correlation_matrix']:
    reverse=next(x for x in r['correlation_matrix'] if x['x']==c['y'] and x['y']==c['x'])
    assert np.isclose(c['value'],reverse['value']) and c['n']==reverse['n']
html=(P/'index.html').read_text()
assert '6,298' in html and '40,188' in html and '全部 92 字段审计' in html
assert '6,292' not in html and '40,155' not in html and '355' not in html
for path in re.findall(r'(?:href|src)="([^"#]+)"',html):
    if ':' not in path and not path.startswith('#'): assert (P/path.split('#')[0]).is_file(),path
assert len(re.findall(r'id="chart-\d+"',html))==9
print(f'PASS: supplied snapshot, sample uniqueness, missingness accounting, pair/mass selection, histogram conservation, correlation, provenance and local links ({len(df):,} planets).')
