from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from eda_support import *

OUT = Path(__file__).resolve().parent
source = "data/raw/nyc-film-permits-historical.csv"
raw = pd.read_csv(ROOT / source)
df = raw.drop_duplicates().copy()
df["start"] = pd.to_datetime(df.EventStartDate, errors="coerce")
df["end"] = pd.to_datetime(df.EventEndDate, errors="coerce")
df["borough"] = df.Boro.fillna("Unknown")
df["category"] = df.CategoryName.fillna("Unknown")
df["duration"] = (df.end - df.start).dt.total_seconds() / 86400
df["month"] = df.start.dt.to_period("M").astype(str)
df["year"] = df.start.dt.year
# Event weighted and project weighted comparisons answer different questions.
ct = pd.crosstab(df.category, df.borough)
chi, p, dof, expected = stats.chi2_contingency(ct)
v = float(np.sqrt(chi / (ct.values.sum() * min(ct.shape[0] - 1, ct.shape[1] - 1))))
residuals = [
    dict(
        x=b,
        y=c,
        value=float((ct.loc[c, b] - expected[i, j]) / np.sqrt(expected[i, j])),
        n=int(ct.loc[c, b]),
        expected=float(expected[i, j]),
    )
    for i, c in enumerate(ct.index)
    for j, b in enumerate(ct.columns)
]
flows = [
    dict(source=c, target=b, value=int(ct.loc[c, b]))
    for c in ct.index
    for b in ct.columns
    if ct.loc[c, b] > 0
]
projects = df.drop_duplicates(["ProjectId", "borough", "category"])
shares = []
for c in ct.index:
    a = df[df.category == c]
    b = projects[projects.category == c]
    for borough in ct.columns:
        shares.append(
            dict(
                label=c + " · " + borough,
                group=c,
                left=float(a.borough.eq(borough).mean() * 100),
                right=float(b.borough.eq(borough).mean() * 100),
                n=len(b),
            )
        )
monthly = (
    df.groupby(["month", "category"], as_index=False)
    .size()
    .rename(columns={"size": "value", "month": "x", "category": "group"})
)
# Exclude boundary years from month-of-year summaries.
full = df[df.year.between(2012, 2014)].copy()
full["month_no"] = full.start.dt.month
season = (
    full.groupby(["month_no", "borough"], as_index=False)
    .size()
    .rename(columns={"month_no": "x", "borough": "y", "size": "value"})
)
companies = df.CompanyName.fillna("Unknown").value_counts()
top_share = float(companies.head(10).sum() / len(df))
company_data = [dict(label=k, value=int(v)) for k, v in companies.head(12).items()]
pro = (
    df.groupby("ProjectId")
    .agg(
        events=("ProjectId", "size"),
        borough_count=("borough", "nunique"),
        category=("category", "first"),
        name=("ProjectTitle", "first"),
    )
    .reset_index()
)
scatter = pro.rename(
    columns={"events": "y", "borough_count": "x", "category": "group", "name": "label"}
)[["x", "y", "group", "label"]]
med = quantiles(df[df.duration.ge(0)], "category", "duration")
duration_bad = int(df.duration.lt(0).sum())
film_share = float(df[df.category == "Film"].borough.eq("Manhattan").mean())
tv_share = float(df[df.category == "Television"].borough.eq("Manhattan").mean())
findings = [
    finding(
        "拍摄类型与行政区有关联",
        f"完全去重后 n={len(df):,} 条事件。类型 × borough 的 Cramér’s V={v:.3f}（0 表示无关联；本样本关联程度较弱）；Film 的 Manhattan 占比为 {film_share:.1%}，Television 为 {tv_share:.1%}。同一项目有多条事件，卡方结果仅作描述，不能按独立观测解读显著性。",
    ),
    finding(
        "少数公司贡献了大量许可事件",
        f"前 10 家公司占 {top_share:.1%} 的事件；{df.ProjectId.nunique():,} 个项目对应 {len(df):,} 条事件。右侧双点图比较事件占比和“项目–borough 组合”占比，检查大型项目重复出现的影响。项目跨多个 borough 会贡献多个组合。",
    ),
    finding(
        "时间边界会制造假的增长或衰退",
        f"开始日期覆盖 {df.start.min().date()} 至 {df.start.max().date()}；2011、2015 是不完整边界年。季节热力图只使用 2012–2014 年的 {len(full):,} 条事件。许可时间范围不能当作实际拍摄工时；发现 {duration_bad} 条结束早于开始的记录。",
    ),
]
charts = [
    chart(
        "flow",
        "类型如何流向城市各区",
        "带宽 = 去重后的事件数。悬停查看数量及源类别内占比。",
        flows,
    ),
    chart(
        "heatmap",
        "超出独立分布预期的组合",
        "Pearson 残差 = (观测−期望)/√期望；红色偏多，蓝色偏少。不是独立项目层面的显著性检验。",
        residuals,
        diverging=True,
    ),
    chart(
        "line",
        "许可事件的月份节奏",
        "2011 与 2015 的边界月份不完整；可点击图例只查看一类。",
        rec(monthly),
        xLabel="事件开始月份",
        yLabel="事件数",
    ),
    chart(
        "dumbbell",
        "换一个分母，结论是否仍成立",
        "左点：事件加权%；右点：项目–borough 组合加权%。跨区项目允许多次计入。",
        shares,
        leftLabel="事件占比",
        rightLabel="项目–borough 占比",
        unit="%",
    ),
    chart(
        "heatmap",
        "完整年份的季节 × 行政区",
        "2012–2014；颜色是观测事件量，不是人口或面积归一化的拍摄强度。",
        rec(season),
    ),
    chart(
        "scatter",
        "跨区项目是否也有更多事件",
        "全部项目；框选点后查看类别构成。重复许可不等于更多影片。",
        rec(scatter),
        xLabel="项目覆盖 borough 数",
        yLabel="项目事件数",
        scaleY="symlog",
        population=len(pro),
    ),
    chart(
        "bar",
        "公司集中度",
        "全部事件按 CompanyName 聚合，Unknown 明示。",
        company_data,
        unit="事件",
    ),
    chart(
        "box",
        "许可起止跨度的分布",
        "中位数、四分位区间和 P10–P90；不是实际拍摄时长，负时长仅从本图剔除。",
        med,
        unit="天",
    ),
]
finish(
    OUT,
    raw,
    df,
    dict(
        title="NYC Film Permits",
        kicker="CITY SYSTEMS / PERMIT ECOLOGY",
        question="城市拍摄分布来自类型偏好，还是少数高频项目的重复出现？",
        theme="city",
        description="这是纽约市 Mayor's Office of Media and Entertainment 提供的影视拍摄许可记录。官方目录说明，许可证通常用于申请独占使用街道、人行道、公园等城市空间；它记录的是获批的许可活动，不是实际拍摄工时、预算或票房。",
        purpose="用于研究城市公共空间中的影视拍摄活动如何按拍摄类型、行政区、月份、项目和公司组织。",
        unit="当前本地历史文件中，一行代表一个许可事件；同一项目可以对应多个日期、地点或行政区。",
        source_note="官方来源是 NYC Open Data 的 Film Permits 目录；本项目使用覆盖 2011–2015 的历史公开镜像，字段为 11 列，不把它当作当前实时全量。",
        references=[
            ["NYC Open Data Film Permits", "https://data.cityofnewyork.us/City-Government/Film-Permits/tg4x-b46p"],
            ["MOME 许可说明", "https://www.nyc.gov/site/mome/permits/when-permit-required.page"],
        ],
    ),
    findings,
    charts,
    {
        "category_borough": ct.reset_index(),
        "weighted_shares": shares,
        "monthly": monthly,
        "project_level": pro,
        "association": {
            "n": len(df),
            "cramers_v": v,
            "chi2": float(chi),
            "p_descriptive_only": float(p),
        },
        "duration": med,
    },
    [source],
    [
        "原表 11 字段；去掉 136 条完全重复记录。保留一项目多事件的真实结构。",
        "解析时间；缺失 borough 保留 Unknown；负时长从时长分布中剔除。",
        "计算类型 × borough 的列联表、Pearson 残差和 Cramér’s V。",
        "比较事件加权与项目–borough 组合加权；公司集中度以事件为分母。",
        "完整年份季节分析；项目级跨区分析。",
    ],
    [
        "历史公开镜像，不代表当前 NYC 的许可全量。",
        "没有可验证坐标；保留行政区关系图，不将地址伪造为地图点。",
        "同一项目内事件相关，列联统计描述关联，不证明因果。",
        "边界年不完整，审批跨度不等于拍摄时长。",
    ],
    {
        "raw_columns": 11,
        "exact_duplicates_removed": len(raw) - len(df),
        "association_n": int(ct.values.sum()),
        "project_count": int(df.ProjectId.nunique()),
    },
)
