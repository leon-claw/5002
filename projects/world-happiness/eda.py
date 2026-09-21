from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from eda_support import *

OUT = Path(__file__).resolve().parent
source = "data/raw/world-happiness-report-2026-figure-2-1.xlsx"
raw = pd.read_excel(ROOT / source)
cols = [
    "year",
    "rank",
    "country",
    "life",
    "lower",
    "upper",
    "gdp",
    "support",
    "health",
    "freedom",
    "generosity",
    "corruption",
    "residual",
]
df = raw.copy()
df.columns = cols
assert not df.duplicated(["country", "year"]).any()
years = sorted(df.year.unique())
latest = df[df.year == max(years)].sort_values("rank")
first = df[df.year == min(years)]
paired = first[["country", "life"]].merge(
    latest[["country", "life"]],
    on="country",
    suffixes=("_first", "_last"),
    validate="one_to_one",
)
paired["delta"] = paired.life_last - paired.life_first
balanced_names = set.intersection(*(set(g.country) for _, g in df.groupby("year")))
balanced = df[df.country.isin(balanced_names)]
trend = pd.concat(
    [
        df.groupby("year", as_index=False).life.mean().assign(group="当年所有国家等权"),
        balanced.groupby("year", as_index=False)
        .life.mean()
        .assign(group=f"固定 {len(balanced_names)} 国等权"),
    ]
).rename(columns={"year": "x", "life": "value"})
coverage = [
    dict(x=str(int(y)), y=c, value=float(g[c].notna().mean() * 100), n=len(g))
    for y, g in df.groupby("year")
    for c in [
        "life",
        "lower",
        "upper",
        "gdp",
        "support",
        "health",
        "freedom",
        "generosity",
        "corruption",
    ]
]
components = [
    "gdp",
    "support",
    "health",
    "freedom",
    "generosity",
    "corruption",
    "residual",
]
complete = df.dropna(subset=["life"] + components).copy()
complete["identity_error"] = complete[components].sum(axis=1) - complete.life
maxerr = float(complete.identity_error.abs().max())
# Contributions are model outputs. Cross/within associations are diagnostics only.
cor = []
for c in components[:-1]:
    dd = complete[["country", "year", c, "life"]].copy()
    between = rho(dd, c, "life")
    rr = dd[[c, "life"]].rank()
    rr = rr - rr.groupby(dd.country).transform("mean")
    within = float(rr.corr().iloc[0, 1])
    cor.append(
        dict(label=c, n=len(dd), pooled_rho=between["rho"], within_rank_r=within)
    )
intervals = [
    dict(
        label=r.country, value=float(r.life), lo=float(r.lower), hi=float(r.upper), n=1
    )
    for _, r in latest.head(20).iterrows()
]
# Adjacent interval overlap is descriptive, NOT a pairwise significance test.
ls = latest.dropna(subset=["lower", "upper"])
overlap = sum(
    max(a.lower, b.lower) <= min(a.upper, b.upper)
    for (_, a), (_, b) in zip(ls.iloc[:-1].iterrows(), ls.iloc[1:].iterrows())
)
top = paired.sort_values("delta", ascending=False)
allslopes = paired.rename(
    columns={"country": "label", "life_first": "left", "life_last": "right"}
).sort_values("delta", ascending=False)
country_trend = df.rename(columns={"year": "x", "life": "value", "country": "group"})[
    ["x", "value", "group"]
]
compdata = [
    dict(
        country=r.country, parts=[dict(label=c, value=float(r[c])) for c in components]
    )
    for _, r in latest.dropna(subset=components).iterrows()
]
findings = [
    finding(
        "排名接近时，先看区间",
        f"最新数据 Year={int(latest.year.iloc[0])}，{len(latest)} 国。带区间的相邻排名共 {len(ls) - 1} 对，其中 {overlap} 对区间重叠。重叠不是正式差异检验，但说明单凭名次难以支持精确优劣判断。",
    ),
    finding(
        "跨年比较必须固定国家集合",
        f"所有 {len(years)} 个可用年份都存在的国家有 {len(balanced_names)} 个。可切换“当年样本均值”和“固定国家均值”检查覆盖变化。{min(years)} 与 {max(years)} 共同出现的 {len(paired)} 国中，{top.iloc[0].country} 的分数增加最多（{top.iloc[0].delta:+.3f}），{top.iloc[-1].country} 下降最多（{top.iloc[-1].delta:+.3f}）；均是三年平均评价的差。",
    ),
    finding(
        "解释项与总分存在构造关系",
        f"完整分解的 {len(complete):,} 行中，六项贡献加 residual 与总分的最大绝对差为 {maxerr:.4f}（舍入及源数据差异）。用这些贡献项预测总分会有构造性循环，不能把高拟合度当研究发现；页面把分解用作描述。",
    ),
    finding(
        "早期缺失是整批字段缺失",
        f"2019 年以前的 lower/upper 和分解贡献在当前文件中整批缺失；2013 年没有记录。保留真实年份间隔，不能把缺失值填 0 或连成不存在的年度观测。",
    ),
]
charts = [
    chart(
        "line",
        "换成固定国家集合，趋势如何变化？",
        "国家等权；不代表世界人口加权幸福感。真实年份间隔，无 2013 数据。",
        rec(trend),
        xLabel="原表 Year",
        yLabel="三年平均 life evaluation",
        zeroBaseline=False,
    ),
    chart(
        "interval",
        "最新排名与不确定区间",
        "最新 Year 前 20 国；原表 Lower/Upper whisker，未重新估计。",
        intervals,
        unit="0–10 分",
        zero=False,
    ),
    chart(
        "dumbbell",
        "从起点到终点：同一国家的变化",
        "共同国家按分数变化排序；可搜索国家查看全部配对。名次变化与分数变化分开。",
        rec(allslopes[["label", "left", "right", "delta"]]),
        leftLabel=str(min(years)),
        rightLabel=str(max(years)),
        unit="分",
        search=True,
    ),
    chart(
        "line",
        "逐国轨迹：检查变化发生在何时",
        "选择国家；缺失年份保留间隔，各点仍是三年平均。",
        rec(country_trend),
        xLabel="原表 Year",
        yLabel="life evaluation / 0–10",
        single=True,
    ),
    chart(
        "composition",
        "解释项构成：作为描述，不作因果归因",
        "选择国家；贡献项 + residual 应近似总分，可与排名分数核对。",
        compdata,
    ),
    chart(
        "heatmap",
        "字段覆盖 × 年份",
        "颜色 = 非缺失比例 %；整批缺失显示为 0%，不是零分。",
        coverage,
        percent=True,
    ),
    chart(
        "table",
        "国家间关系与国家内变化",
        "输入为报告分解贡献，不是原始 GDP/健康等指标。Pooled Spearman 与按国家去均值后的秩相关仅作构成诊断。",
        cor,
    ),
]
finish(
    OUT,
    raw,
    df,
    dict(
        title="World Happiness",
        kicker="COUNTRIES / UNCERTAINTY / CHANGE",
        question="排名背后的差异有多确定？固定国家样本后，跨年变化还成立吗？",
        theme="happiness",
        description="这是 World Happiness Report Figure 2.1 的官方数据。报告说明数据以 Gallup World Poll 为基础，并提供 life evaluation 的三年平均、95% 置信区间和六个解释因素的贡献；因此这里的年份不是单一年份的即时幸福度。",
        purpose="用于研究国家排名的不确定性、固定国家集合后的跨年变化，以及报告分解中的解释项覆盖，而不是把国家排名直接当作因果结论。",
        unit="一行代表一个国家 × Year 的报告记录；life evaluation 是滚动三年平均，早期年份没有后期才出现的完整贡献字段。",
        source_note="官方来源是 World Happiness Report 的 Data Sharing 页面；本地文件是 2026 Figure 2.1 工作簿，保留真实缺失年份和字段缺失结构。",
        references=[
            ["World Happiness Report 数据共享", "https://www.worldhappiness.report/data-sharing/"],
            ["指标与因果解释 FAQ", "https://www.worldhappiness.report/faq/"],
        ],
    ),
    findings,
    charts,
    {
        "paired_change": paired,
        "balanced_trend": trend,
        "coverage": coverage,
        "component_identity": complete[["country", "year", "identity_error"]],
        "cross_vs_within": cor,
        "latest_intervals": intervals,
    },
    [source],
    [
        "直接从原始 xlsx 读取，验证国家 × Year 唯一；保留三年平均语义。",
        "按真实年份索引；2013 缺失不补假点。",
        "计算全年份平衡国家面板，与当年全样本等权均值对比。",
        "比较共同国家的起止分数；原表区间用于表达排名不确定性。",
        "审计贡献项之和与总分的构造关系，不训练循环预测模型。",
        "逐年逐字段覆盖审计，并比较国家间和国家内关联。",
    ],
    [
        "国家等权均值不是世界人口平均；国家命名差异按原表精确匹配，未猜测合并。",
        "连续 Year 的三年平均窗口可能重叠，变化不等于独立年度冲击。",
        "分解贡献是模型输出，不是原始宏观变量或清晰因果效应。",
        "区间重叠仅作可视诊断，不替代两国差值的正式统计检验。",
    ],
    {
        "country_year_unique": True,
        "balanced_countries": len(balanced_names),
        "paired_countries": len(paired),
        "identity_max_abs_error": maxerr,
        "adjacent_overlap": overlap,
    },
)
