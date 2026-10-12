"""生成教学 Notebook，并使用当前环境的 IPython 逐单元执行、保存真实输出。"""
import base64
import contextlib
import io
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'output' / '.mplconfig'))
import matplotlib
matplotlib.use('Agg')
from IPython.core.interactiveshell import InteractiveShell

cells = []
def md(s):
    cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': s.strip()})
def code(s):
    cells.append({'cell_type': 'code', 'metadata': {}, 'source': s.strip(), 'execution_count': None, 'outputs': []})

md('''# NYC Film Permits：探索性数据分析

课堂项目 · 中文分析 / English charts · 本地 CSV 为唯一统计来源

按「数据认识 → 清洗 → 特征 → 探索分析 → 结论」组织。所有数字由下方代码计算，不从网站抄入统计结果。项目路径均相对于本 Notebook 所在文件夹。

**阅读官网**：[数据介绍和字段说明](https://data.cityofnewyork.us/City-Government/Film-Permits/tg4x-b46p)。2026-10-12 查阅：数据由纽约市 MOME 提供，一行是一条许可证。EventID 是活动标识；开始/结束时间是计划活动时间，EnteredOn 是申请提交时间；Category/SubCategoryName 描述制作类别；Borough 是当天活动的首个行政区，Country 是项目来源。许可证可涉及拍摄、布景和剧院装卸等活动。统计不能解释为影视作品数量或收入。

官网目前约 19.5K 行、14 列，动态网页更新至 2026-10-08；本地文件是另一快照，数据量和覆盖范围以下方读入结果为准，不下载新数据替换本地文件。官网字段语义与本地列名吻合，但本地有字段错位和日期异常。

**执行说明**：当前环境未能下载 Jupyter 内核依赖。随附输出通过真实 IPython 按顺序执行全部 Python 单元生成；独立 Jupyter 内核的 Run All 尚未验证。代码使用标准 Python，没有依赖该执行器的语法。''')
code('''from pathlib import Path
import calendar
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from IPython.display import display, Markdown

DATA_DIR = Path('data')
OUT = Path('output')
FIG = OUT / 'figures'
TABLE = OUT / 'tables'
for folder in [FIG, TABLE]:
    folder.mkdir(parents=True, exist_ok=True)
sns.set_theme(style='whitegrid', context='notebook', font='DejaVu Sans')
plt.rcParams.update({'figure.dpi': 110, 'savefig.dpi': 180,
                     'axes.spines.top': False, 'axes.spines.right': False})
COLORS = ['#237A91', '#E89842', '#6A8D50', '#8B6AAB', '#CC6B68']

def finish(name, note):
    # 保存与 Notebook 内嵌完全相同的图，图下注明筛选口径和样本数。
    fig = plt.gcf()
    fig.text(0.01, 0.005, note, fontsize=8, color='#555555')
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    fig.savefig(FIG / (name + '.png'), bbox_inches='tight')
    plt.show()
    plt.close(fig)

def explain(text):
    display(Markdown(text))

files = [p for p in DATA_DIR.glob('*.csv') if 'clean' not in p.stem.lower()]
if len(files) != 1:
    raise ValueError(f'预期 data/ 中只有一个原始 CSV，实际找到 {len(files)} 个。')
raw = pd.read_csv(files[0])
print('数据文件：', files[0])
print('行数、列数：', raw.shape)
print('列名：', raw.columns.tolist())
display(raw.head())''')
md('## 1. 认识数据\n先检查真实列名、缺失、分类取值与日期范围，再确定分析字段。唯一标识符重复仅供检查，不机械删除同一 ID 的不同记录。')
code('''profile = pd.DataFrame({'dtype': raw.dtypes.astype(str),
                        'missing_n': raw.isna().sum(),
                        'missing_pct': raw.isna().mean().mul(100).round(2),
                        'distinct_n': raw.nunique()})
display(profile)
profile.to_csv(TABLE / 'raw_profile.csv', encoding='utf-8-sig')
print('完全重复行：', raw.duplicated().sum())
if 'EventID' in raw:
    print('EventID 缺失：', raw.EventID.isna().sum())
    print('EventID 重复（除第一次外）：', raw.EventID.duplicated().sum())

# 分类字段经实际列名确认；高基数字段属于地址或多值编码，不作为类别排行榜。
cat_cols = ['EventType', 'EventAgency', 'Borough', 'Category', 'SubCategoryName', 'Country']
for col in cat_cols:
    print('\\n', col, '不同取值数 =', raw[col].nunique())
    display(raw[col].value_counts(dropna=False).rename('records').to_frame().head(12))

date_cols = ['StartDateTime', 'EndDateTime', 'EnteredOn']
date_format = '%m/%d/%Y %I:%M:%S %p'
date_checks = []
for col in date_cols:
    parsed = pd.to_datetime(raw[col], format=date_format, errors='coerce')
    date_checks.append({'field': col, 'min': parsed.min(), 'max': parsed.max(),
                        'missing_n': int(raw[col].isna().sum()),
                        'invalid_nonmissing_n': int((raw[col].notna() & parsed.isna()).sum())})
display(pd.DataFrame(date_checks))
explain(f'本地有 **{len(raw):,} 条许可证记录、{raw.shape[1]} 列**；EventID 没有重复。制作类别、活动类型、行政区和计划时间适合分析。开始日期缺失 {raw.StartDateTime.isna().sum():,} 条，录入日期缺失 {raw.EnteredOn.isna().sum():,} 条；这些记录仍可用于其他字段的统计。ParkingHeld 是停车位置文本，多值社区/警区/邮编不能直接按拆分后的数量当作许可证总数。')''')
md('''## 2. 清洗并保留审计记录

字段错位的判据来自本地检查：Borough 出现活动类型、EventType 出现机构名、EventAgency 出现时间，且 Category 出现日期。这些行不能当成新类别。保守地单独留档，不尝试猜测缺失或错位字段。

对其他行仅去除文本首尾空格、将空白视作缺失，转换日期。负时间跨度仅对跨度分析置空；负提前量保留为录入晚于开始的标记。长跨度不据大小删除，所有原始字段保存在原始文件与异常日期审计表中。''')
code('''clean = raw.copy()
audit = []
def log(action, affected, reason):
    audit.append({'action': action, 'affected_records': int(affected), 'reason': reason})

n_dup = clean.duplicated().sum()
clean = clean.drop_duplicates().copy()
log('移除完全重复行', n_dup, '仅相同的整行重复才删除')
for col in clean.select_dtypes(include='object'):
    old = clean[col].copy()
    clean[col] = clean[col].str.strip().replace('', pd.NA)
    changed = (old.fillna('<NA>') != clean[col].fillna('<NA>')).sum()
    log('文本首尾空格/空白处理：' + col, changed, '统一格式；不改变地址内部空格或合并语义不同的类别')

boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
# 用日期形式识别错位后的 Category，兼容 pandas 旧版本。
misaligned = (~clean.Borough.isin(boroughs)
              & clean.EventType.eq("Mayor's Office of Media & Entertainment")
              & clean.Category.str.match(r'^\\d{1,2}/\\d{1,2}/\\d{4}'))
raw.loc[misaligned].to_csv(OUT / 'quarantined_rows.csv', index=False, encoding='utf-8-sig')
clean = clean.loc[~misaligned].copy()
log('隔离字段错位行', misaligned.sum(), '多个字段同时违反语义，无法可靠恢复全部字段；不进入主要分析')

invalid_masks = {}
for col in date_cols:
    parsed = pd.to_datetime(clean[col], format=date_format, errors='coerce')
    invalid_masks[col] = clean[col].notna() & parsed.isna()
    log('日期解析失败：' + col, invalid_masks[col].sum(), '非空但无法解析的值设为 NaT')
    clean[col] = parsed
span = (clean.EndDateTime - clean.StartDateTime).dt.total_seconds() / 3600
lead = (clean.StartDateTime - clean.EnteredOn).dt.total_seconds() / 86400
clean['negative_duration_flag'] = span.lt(0)
clean['late_entry_flag'] = lead.lt(0)
clean['duration_hours'] = span.where(span.ge(0))
clean['lead_days'] = lead
log('负跨度设为缺失（保留原日期）', span.lt(0).sum(), '结束早于开始，不能作为有效跨度；其他分析仍可使用')
log('标记录入晚于开始（保留数值）', lead.lt(0).sum(), '可能为补录或异常，不能推断实际审批时间')
log('保留超过 7 天的跨度', span.gt(168).sum(), '可能为连续多日活动，不以数值大为由删除')

any_invalid = pd.DataFrame(invalid_masks).any(axis=1)
flagged = any_invalid | clean.negative_duration_flag | clean.late_entry_flag
raw.loc[clean.index[flagged]].to_csv(OUT / 'date_anomalies_original.csv', index=False, encoding='utf-8-sig')
audit_df = pd.DataFrame(audit)
display(audit_df)
audit_df.to_csv(TABLE / 'cleaning_audit.csv', index=False, encoding='utf-8-sig')
print('清洗后保留记录：', len(clean))
print('主要类别：', clean.Category.value_counts().to_dict())
print('未识别行政区：', clean.loc[~clean.Borough.isin(boroughs), 'Borough'].unique())
explain(f'清洗后保留 **{len(clean):,} 条**。隔离 {misaligned.sum()} 条字段错位记录，占原始数据 {misaligned.mean():.3%}。没有完全重复行；未发现需要合并的明确拼写变体。{span.lt(0).sum()} 条负跨度和 {any_invalid.sum()} 条非空日期解析异常均留档。')''')
md('''## 3. 构造分析变量与统计口径

开始日期提取年份、月份、星期、小时、周末；缺失日期不虚构。跨度是计划结束减计划开始，并非劳动时长。提前量是计划开始减提交时间，并非审批耗时。官网时间为未带时区的本地时间戳，本分析按记录中的墙钟时间计算，不进行跨夏令时校正。

所有分析一条保留记录计一次。Borough 只代表首个行政区，不能表示全部地点覆盖。全体构成保留日期缺失行；时间图使用有效开始日期；跨度和提前量各自筛选。''')
code('''clean['year'] = clean.StartDateTime.dt.year.astype('Int64')
clean['month'] = clean.StartDateTime.dt.month.astype('Int64')
clean['weekday'] = clean.StartDateTime.dt.dayofweek.astype('Int64')
clean['start_hour'] = clean.StartDateTime.dt.hour.astype('Int64')
clean['is_weekend'] = clean.weekday.ge(5).astype('boolean')
clean.to_csv(OUT / 'film_permits_clean.csv', index=False, encoding='utf-8-sig')
timed = clean.loc[clean.StartDateTime.notna()].copy()
valid_span = clean.loc[clean.duration_hours.notna()].copy()
valid_lead = clean.loc[clean.lead_days.notna()].copy()
latest = timed.StartDateTime.max()
# 最晚一天只有一条记录，不能将其所在的 7 月作为完整月；保守使用此前的月份。
last_month_start = latest.to_period('M').to_timestamp()
monthly_data = timed[timed.StartDateTime.lt(last_month_start)].copy()
# 完整年度仅表示本地时间覆盖 1–12 月，不能保证源系统无漏报。
coverage = timed.groupby('year').agg(first=('StartDateTime', 'min'), last=('StartDateTime', 'max'), records=('EventID', 'size'))
coverage['months_observed'] = timed.groupby('year').month.nunique()
full_years = coverage.index[(coverage['first'].dt.month.eq(1)) & (coverage['last'].dt.month.eq(12))].tolist()
display(coverage)
scopes = pd.Series({'raw_records': len(raw), 'clean_records': len(clean),
                    'valid_start': len(timed), 'missing_start': clean.StartDateTime.isna().sum(),
                    'valid_nonnegative_duration': len(valid_span), 'valid_lead_including_negative': len(valid_lead),
                    'nonnegative_lead': valid_lead.lead_days.ge(0).sum()})
display(scopes.to_frame('records'))
scopes.to_csv(TABLE / 'analysis_denominators.csv', encoding='utf-8-sig')
coverage.to_csv(TABLE / 'year_coverage.csv', encoding='utf-8-sig')
explain(f'有效开始日期为 **{timed.StartDateTime.min():%Y-%m-%d} 至 {latest:%Y-%m-%d}**，共 {len(timed):,} 条。最新月份只有 {(timed.StartDateTime.ge(last_month_start)).sum()} 条，月度主图截止 {last_month_start - pd.Timedelta(days=1):%Y-%m}。2026 年只有上半年及 7 月 1 日的一条，不能与全年总数直接比较。')''')
md('## 4. 探索分析\n先看年度、月份和单变量构成，再比较行政区、时间习惯与计划跨度。图表数字均由对应分析子集计算。')
md('### 图 1：完整年度与同一上半年窗口')
code('''annual = timed.groupby('year').size()
h1 = timed[timed.month.le(6)].groupby('year').size()
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
for ax, values, title in [(axes[0], annual.loc[full_years], 'Annual permits: full calendar coverage'),
                           (axes[1], h1, 'January–June permits: comparable window')]:
    bars = ax.bar(values.index.astype(str), values.values, color=COLORS[0])
    ax.bar_label(bars, fmt='%d', padding=3)
    ax.set(title=title, xlabel='Start year', ylabel='Permit records')
    ax.set_ylim(0, values.max() * 1.15)
finish('01_year_comparison', f'Valid start dates only; full-year coverage: {full_years}; H1 includes January–June only.')
change = (annual.loc[2025] / annual.loc[2024] - 1) * 100
h1_change = (h1.loc[2026] / h1.loc[2025] - 1) * 100
explain(f'**展示**：全年和同一上半年分别比较。**发现**：2024 年 {annual.loc[2024]:,} 条，2025 年 {annual.loc[2025]:,} 条，变化 {change:+.1f}%；2026 年上半年 {h1.loc[2026]:,} 条，相比 2025 年同期 {h1.loc[2025]:,} 条变化 {h1_change:+.1f}%。**可能含义**：不同时间窗口的许可活动规模存在变化。**不能推断**：不能把记录增减视为作品产量或行业收入变化，也不能仅凭本图解释成因。')''')
md('### 图 2：月度变化与季节性线索')
code('''monthly = monthly_data.set_index('StartDateTime').resample('MS').size()
season = pd.crosstab(monthly_data.year, monthly_data.month).reindex(columns=range(1, 13)).astype(float)
# 2026 尚未覆盖的月份保持空白，而不是补成零。
season.loc[int(latest.year), list(range(int(latest.month), 13))] = np.nan
fig, axes = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [1, 1.2]})
axes[0].plot(monthly.index, monthly.values, color=COLORS[0], marker='o', markersize=3)
axes[0].set(title='Monthly permit records', xlabel='Start month', ylabel='Permit records')
axes[0].xaxis.set_major_locator(mdates.MonthLocator(interval=3))
axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
axes[0].tick_params(axis='x', rotation=35)
sns.heatmap(season, annot=True, fmt='.0f', cmap='YlGnBu', ax=axes[1], cbar_kws={'label': 'Permit records'},
            xticklabels=[calendar.month_abbr[m] for m in range(1, 13)])
axes[1].set(title='Calendar month by year', xlabel='Start month', ylabel='Start year')
finish('02_monthly_patterns', f'n={len(monthly_data):,}; latest partial month excluded; blank cells are outside observed coverage.')
peaks = monthly.sort_values(ascending=False).head(2)
explain(f'**展示**：月度数量及各年份的月历热力图。**发现**：最高月份为 {peaks.index[0]:%Y-%m}（{peaks.iloc[0]:,} 条），其次为 {peaks.index[1]:%Y-%m}（{peaks.iloc[1]:,} 条）；2023 年 7 月只有 {monthly.loc["2023-07-01"]} 条。**可能含义**：月份之间存在明显波动。**不能推断**：有限年份内峰值并不总落在同一月，不能据此确认稳定季节性，更不能认定某一事件导致下降。')''')
md('### 图 3：制作类别与活动类型')
code('''categories = clean.Category.value_counts()
events = clean.EventType.value_counts()
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for ax, values, title in [(axes[0], categories, 'Production categories'), (axes[1], events, 'Permitted activity types')]:
    bars = ax.barh(values.index[::-1], values.values[::-1], color=COLORS[0])
    ax.bar_label(bars, labels=[f'{v:,} ({v/len(clean):.1%})' for v in values.values[::-1]], padding=3, fontsize=9)
    ax.set(title=title, xlabel='Permit records', ylabel='')
    ax.set_xlim(0, values.max() * 1.35)
finish('03_categories_and_activities', f'n={len(clean):,}; includes records with missing start dates; two separate classifications.')
display(pd.DataFrame({'records': categories, 'share_pct': categories / len(clean) * 100}))
explain(f'**展示**：制作类别与许可活动类型是两个不同维度。**发现**：Television 为 {categories["Television"]:,} 条（{categories["Television"]/len(clean):.1%}）；Shooting Permit 为 {events["Shooting Permit"]:,} 条（{events["Shooting Permit"]/len(clean):.1%}），剧院装卸为 {events["Theater Load in and Load Outs"]:,} 条。**可能含义**：电视相关许可在本地记录中最常见，剧院装卸也占有一定规模。**不能推断**：同一作品可申请多条许可；类别由申请人选择，不等于独立作品数量。')''')
md('### 图 4：首个行政区的记录分布')
code('''borough_counts = clean.Borough.value_counts().reindex(boroughs)
fig, ax = plt.subplots(figsize=(10, 4.8))
bars = ax.barh(borough_counts.index[::-1], borough_counts.values[::-1], color=COLORS)
ax.bar_label(bars, labels=[f'{v:,} ({v/len(clean):.1%})' for v in borough_counts.values[::-1]], padding=4)
ax.set(title='Permit records by first borough', xlabel='Permit records', ylabel='First borough', xlim=(0, borough_counts.max() * 1.25))
finish('04_borough_distribution', f'n={len(clean):,}; one first borough per record; no multi-location expansion.')
explain(f'**展示**：每条记录的首个行政区。**发现**：Manhattan {borough_counts["Manhattan"]:,} 条，Brooklyn {borough_counts["Brooklyn"]:,} 条，合计占 {(borough_counts["Manhattan"]+borough_counts["Brooklyn"])/len(clean):.1%}。**可能含义**：许可记录的首站分布较集中。**不能推断**：不能表示全部拍摄地点，未按面积、人口或产业设施数量标准化，也不能用于评价行政区拍摄强度。')''')
md('### 图 5：各行政区内部的类别构成')
code('''cross = pd.crosstab(clean.Borough, clean.Category).reindex(index=boroughs, columns=categories.index)
shares = cross.div(cross.sum(axis=1), axis=0).mul(100)
fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(shares, annot=True, fmt='.1f', cmap='YlGnBu', ax=ax, cbar_kws={'label': 'Within-borough share (%)'})
ax.set(title='Production mix within each first borough', xlabel='Production category', ylabel='First borough')
ax.tick_params(axis='x', rotation=35)
finish('05_borough_category_mix', 'Rows sum to 100%; borough sample sizes: ' + ', '.join(f'{b}={borough_counts[b]:,}' for b in boroughs))
shares.to_csv(TABLE / 'borough_category_pct.csv', encoding='utf-8-sig')
explain(f'**展示**：行政区内部的行百分比，避免大行政区主导绝对数量。**发现**：Manhattan 的 Theater 占 {shares.loc["Manhattan", "Theater"]:.1f}%，Brooklyn 的 Television 占 {shares.loc["Brooklyn", "Television"]:.1f}%。**可能含义**：不同首个行政区的制作类别组合存在差别。**不能推断**：Staten Island 仅 {borough_counts["Staten Island"]} 条，比例对少量记录敏感；本图不能证明地区设施或政策造成这些差异。')''')
md('### 图 6：星期与工作日/周末（校正日历天数）')
code('''# 使用已覆盖到 2026-06-30 的窗口，避免将不完整的 7 月 1 日计作完整观察日。
week_data = monthly_data.copy()
days = pd.date_range(week_data.StartDateTime.min().normalize(), last_month_start - pd.Timedelta(days=1), freq='D')
calendar_counts = pd.Series(days.dayofweek).value_counts().reindex(range(7))
weekday_counts = week_data.weekday.value_counts().reindex(range(7), fill_value=0)
weekday_rates = weekday_counts / calendar_counts
weekend_n = week_data.is_weekend.sum()
weekday_n = len(week_data) - weekend_n
weekend_days = int((days.dayofweek >= 5).sum())
weekday_days = len(days) - weekend_days
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
labels = [calendar.day_abbr[d] for d in range(7)]
axes[0].bar(labels, weekday_counts.values, color=[COLORS[0]]*5 + [COLORS[1]]*2)
axes[0].set(title='Starts by weekday', xlabel='Start weekday', ylabel='Permit records')
bars = axes[1].bar(['Weekday', 'Weekend'], [weekday_n/weekday_days, weekend_n/weekend_days], color=COLORS[:2])
axes[1].bar_label(bars, fmt='%.2f', padding=3)
axes[1].set(title='Starts per calendar day', xlabel='Day type', ylabel='Permit records / calendar day')
finish('06_weekday_and_weekend', f'n={len(week_data):,}; {days.min():%Y-%m-%d}–{days.max():%Y-%m-%d}; denominator includes zero-record calendar days.')
display(pd.DataFrame({'records': weekday_counts.values, 'calendar_days': calendar_counts.values, 'records_per_day': weekday_rates.values}, index=labels))
explain(f'**展示**：星期总数和按日历天数标准化的工作日/周末比较。**发现**：周末占 {weekend_n/len(week_data):.1%}；工作日平均 {weekday_n/weekday_days:.2f} 条/日，周末 {weekend_n/weekend_days:.2f} 条/日。**可能含义**：许可活动的安排偏向工作日。**不能推断**：原始工作日总数本来受每周五天对两天影响，因此这里补充每天指标；缺失开始日期可能带来偏差，也不能推断人员实际出勤时间。')''')
md('### 图 7：工作日与周末的开始时段')
code('''hour_data = timed.copy()
hour_data['day_type'] = np.where(hour_data.is_weekend, 'Weekend', 'Weekday')
hour_counts = pd.crosstab(hour_data.day_type, hour_data.start_hour).reindex(index=['Weekday','Weekend'], columns=range(24), fill_value=0)
hour_pct = hour_counts.div(hour_counts.sum(axis=1), axis=0).mul(100)
fig, ax = plt.subplots(figsize=(13, 3.6))
sns.heatmap(hour_pct, annot=True, fmt='.0f', cmap='YlGnBu', ax=ax, cbar_kws={'label':'Within-day-type share (%)'})
ax.set(title='Start-hour distribution: weekday vs weekend', xlabel='Start hour (local clock, 0–23)', ylabel='Day type')
finish('07_start_hour_patterns', f'n={len(timed):,}; percentages sum to 100% within each day type; integer annotations are rounded.')
peak_hour = timed.start_hour.value_counts().idxmax()
explain(f'**展示**：分别在工作日和周末内部计算小时占比。**发现**：全体最常见开始小时为 {peak_hour:02d}:00–{peak_hour:02d}:59，占 {timed.start_hour.eq(peak_hour).mean():.1%}；工作日峰值小时为 {hour_pct.loc["Weekday"].idxmax():02d}，周末为 {hour_pct.loc["Weekend"].idxmax():02d}。**可能含义**：两类日子的许可活动安排存在差异。**不能推断**：这些是计划开始时间，不代表摄像机开始拍摄时间；剧院装卸等活动也包含在内。')''')
md('### 图 8：计划时间跨度的分布和长尾')
code('''duration_stats = valid_span.duration_hours.describe(percentiles=[.5, .9, .95, .99])
display(duration_stats.to_frame('hours'))
longest = valid_span.nlargest(10, 'duration_hours')[['EventID','EventType','Category','StartDateTime','EndDateTime','duration_hours']]
display(longest)
longest.to_csv(TABLE / 'longest_scheduled_spans.csv', index=False, encoding='utf-8-sig')
fig, ax = plt.subplots(figsize=(10, 4.8))
bins = np.geomspace(valid_span.duration_hours.min(), valid_span.duration_hours.max(), 45)
ax.hist(valid_span.duration_hours, bins=bins, color=COLORS[0], edgecolor='white')
ax.set_xscale('log')
ax.axvline(valid_span.duration_hours.median(), color=COLORS[1], linestyle='--', label=f'Median: {valid_span.duration_hours.median():.1f} h')
ax.set(title='Scheduled activity span: full distribution', xlabel='Scheduled span (hours, log scale)', ylabel='Permit records')
ax.legend()
finish('08_scheduled_span_distribution', f'n={len(valid_span):,}; nonnegative valid spans; all long spans retained; 17 negative spans excluded.')
explain(f'**展示**：保留长尾的完整有效跨度分布，横轴使用对数刻度。**发现**：中位数 {valid_span.duration_hours.median():.1f} 小时，均值 {valid_span.duration_hours.mean():.1f} 小时；超过 7 天有 {valid_span.duration_hours.gt(168).sum()} 条，最长 {valid_span.duration_hours.max():.1f} 小时，短于 1 小时有 {valid_span.duration_hours.lt(1).sum()} 条。**可能含义**：少数多日许可拉高平均值。**不能推断**：跨度不是连续工作或实际拍摄时长；极长值需结合许可原件核实，不能只因很大就认定错误。')''')
md('### 图 9：不同制作类别的计划跨度')
code('''span_summary = valid_span.groupby('Category').duration_hours.agg(['count','median','mean','min','max']).sort_values('median')
display(span_summary)
fig, ax = plt.subplots(figsize=(11, 6))
sns.boxplot(data=valid_span, x='duration_hours', y='Category', order=span_summary.index,
            color=COLORS[0], showfliers=True, flierprops={'markersize': 2, 'alpha': .25}, ax=ax)
ax.set_xscale('log')
ax.set(title='Scheduled activity span by production category', xlabel='Scheduled span (hours, log scale)', ylabel='Production category')
finish('09_span_by_category', f'n={len(valid_span):,}; all positive valid spans shown; points beyond whiskers are retained observations.')
explain(f'**展示**：不同制作类别的跨度中位数、四分位范围和长尾点。**发现**：Theater 中位数 {span_summary.loc["Theater","median"]:.1f} 小时，Television {span_summary.loc["Television","median"]:.1f} 小时，Film {span_summary.loc["Film","median"]:.1f} 小时。**可能含义**：类别间安排方式不同，剧院多日装卸可能与长跨度有关。**不能推断**：类别与 EventType 混杂，不能把差异解释为某类作品的实际制作效率；箱线图离群点不是已确认错误。')''')
md('### 图 10：提交到计划开始的提前量')
code('''positive_lead = valid_lead[valid_lead.lead_days.ge(0)].copy()
lead_table = valid_lead.groupby('Category').lead_days.agg(['count', 'median']).sort_values('median')
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# 右侧保留全数据，左图为方便观察单独展示 0–30 天，并明确披露尾部。
near_lead = positive_lead[positive_lead.lead_days.le(30)]
axes[0].hist(near_lead.lead_days, bins=30, color=COLORS[0], edgecolor='white')
axes[0].set(title='Submission lead time: 0–30 days', xlabel='Scheduled start minus submission (days)', ylabel='Permit records')
axes[1].barh(lead_table.index, lead_table['median'], color=COLORS[1])
axes[1].set(title='Median lead time by category', xlabel='Median lead time (days)', ylabel='Production category')
finish('10_submission_lead_time', f'Valid lead n={len(valid_lead):,}; left n={len(near_lead):,}, >30 d={positive_lead.lead_days.gt(30).sum()}, negative={valid_lead.lead_days.lt(0).sum()}; right uses all valid leads.')
display(valid_lead.lead_days.describe(percentiles=[.5,.9,.95,.99]).to_frame('days'))
display(lead_table)
explain(f'**展示**：申请提交到计划开始的间隔。**发现**：有效提前量共 {len(valid_lead):,} 条，中位数 {valid_lead.lead_days.median():.2f} 天；3 条为负值，超过 30 天有 {positive_lead.lead_days.gt(30).sum()} 条。**可能含义**：多数可观测记录在开始前数天提交。**不能推断**：EnteredOn 不是获批日期，不能计算审批效率；录入日期缺失 {clean.EnteredOn.isna().sum():,} 条，完整案例可能有选择偏差。左图截取视窗没有从清洗数据删除长提前量。')''')
md('## 5. 最有价值的结论与限制')
code('''conclusions = f"""1. **时间比较必须对齐窗口**：2025 年完整年度 {annual.loc[2025]:,} 条，相比 2024 年变化 {change:+.1f}%；2026 年上半年 {h1.loc[2026]:,} 条，相比 2025 年同期变化 {h1_change:+.1f}%。2026 年全年不可比较。
2. **电视相关记录最多**：Television {categories['Television']:,} 条，占 {categories['Television']/len(clean):.1%}；许可活动中拍摄许可占 {events['Shooting Permit']/len(clean):.1%}。这些都是许可记录，不是作品数。
3. **首个行政区分布集中、类别组合不同**：Manhattan 与 Brooklyn 合计占 {(borough_counts['Manhattan']+borough_counts['Brooklyn'])/len(clean):.1%}；Manhattan 内 Theater 占 {shares.loc['Manhattan','Theater']:.1f}%，Brooklyn 内 Television 占 {shares.loc['Brooklyn','Television']:.1f}%。
4. **开始安排偏向工作日，计划跨度存在长尾**：工作日平均 {weekday_n/weekday_days:.2f} 条/日，周末 {weekend_n/weekend_days:.2f} 条/日；有效跨度中位数 {valid_span.duration_hours.median():.1f} 小时，均值 {valid_span.duration_hours.mean():.1f} 小时。
5. **可观测提交提前量通常为数天**：中位数 {valid_lead.lead_days.median():.2f} 天，但此项只覆盖 {len(valid_lead):,} 条完整案例，不能视作审批用时。

**数据限制**：本地快照无法保证涵盖全部许可，更不涵盖不需许可的制作。时间覆盖完整年度不等于记录完整；日期缺失会使时间分析低于全体构成的样本数。8 条错位行隔离，17 条负跨度与异常录入日期需进一步核实。Borough 只是首个行政区；多值编码不拆分为独立许可；缺少作品唯一 ID、收入、实际执行状态、审批日期和外部事件变量。因此分析是描述性比较，不支持因果、收入、作品数量或效率推断。"""
explain(conclusions)
(OUT / 'findings_zh.md').write_text('# NYC Film Permits：主要发现\\n\\n' + conclusions, encoding='utf-8')
# 这些断言只是交付自检，不引入单元测试框架。
assert len(raw) == len(clean) + int(misaligned.sum()) + int(n_dup)
assert clean.EventID.is_unique
assert clean.duration_hours.dropna().ge(0).all()
assert int(annual.sum()) == len(timed)
assert int(categories.sum()) == len(clean)
assert int(borough_counts.sum()) == len(clean)
assert len(list(FIG.glob('*.png'))) == 10
print('交付自检通过：行数守恒、唯一标识、统计分母和 10 张图一致。')''')

# IPython 执行器：代码输出来自真实执行；没有伪造 Jupyter kernel 执行声明。
shell = InteractiveShell.instance()
current = None
original_display = None

def add_display(obj=None, **kwargs):
    if obj is None:
        return
    if isinstance(obj, dict):
        data = obj
    else:
        data = {'text/plain': repr(obj)}
        if hasattr(obj, '_repr_html_'):
            value = obj._repr_html_()
            if value:
                data['text/html'] = value
        if hasattr(obj, '_repr_markdown_'):
            data['text/markdown'] = obj._repr_markdown_()
    current['outputs'].append({'output_type':'display_data','data':data,'metadata':{}})

import matplotlib.pyplot as plt

def show_figures(*args, **kwargs):
    for num in plt.get_fignums():
        fig = plt.figure(num)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=110, bbox_inches='tight')
        add_display({'image/png': base64.b64encode(buf.getvalue()).decode('ascii'), 'text/plain':'<Matplotlib figure>'})
plt.show = show_figures
count = 0
for current in cells:
    if current['cell_type'] != 'code':
        continue
    count += 1
    current['execution_count'] = count
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        result = shell.run_cell(current['source'], store_history=False)
    if stdout.getvalue():
        current['outputs'].insert(0, {'output_type':'stream','name':'stdout','text':stdout.getvalue()})
    if stderr.getvalue():
        current['outputs'].append({'output_type':'stream','name':'stderr','text':stderr.getvalue()})
    error = result.error_before_exec or result.error_in_exec
    if error:
        raise RuntimeError(f'Cell {count} failed: {error}\n{stdout.getvalue()}\n{stderr.getvalue()}')
    # 替换显示函数，后续每个单元格使用真实富文本捕获。
    shell.user_ns['display'] = add_display
    print(f'Executed cell {count}', flush=True)

notebook = {'nbformat':4, 'nbformat_minor':5,
            'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
                        'language_info':{'name':'python','version':__import__('sys').version.split()[0]},
                        'execution_method':'Sequential IPython execution; standalone Jupyter kernel unavailable'},
            'cells':cells}
for i, cell in enumerate(cells):
    cell['id'] = f'cell-{i:03d}'
(ROOT / 'NYC_Film_Permits_EDA.ipynb').write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding='utf-8')
(ROOT / 'output' / 'execution_report.json').write_text(json.dumps({'method':'Sequential IPython execution', 'code_cells':count,
    'errors':0, 'jupyter_kernel_verified':False, 'figures':10}, indent=2), encoding='utf-8')
print('Notebook saved:', ROOT / 'NYC_Film_Permits_EDA.ipynb')
