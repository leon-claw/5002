from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from eda_support import *

OUT = Path(__file__).resolve().parent
source = "data/raw/nasa-exoplanets-ps.csv"
raw = pd.read_csv(ROOT / source, low_memory=False)
df = raw[(raw.default_flag == 1) & (raw.soltype == "Published Confirmed")].copy()
assert df.pl_name.is_unique
fields = [
    "pl_orbper",
    "pl_rade",
    "pl_bmasse",
    "pl_eqt",
    "st_teff",
    "sy_dist",
    "pl_orbsmax",
]
labels = [
    "周期 / 天",
    "半径 / 地球",
    "质量 / 地球",
    "平衡温度 / K",
    "恒星温度 / K",
    "距离 / pc",
    "半长轴 / AU",
]
# A limit is not an ordinary point measurement.
limits = {}
for c in fields:
    limit = c + "lim"
    bad = df[limit].fillna(0).ne(0) if limit in df else pd.Series(False, index=df.index)
    limits[c] = int(bad.sum())
    df.loc[bad, c] = np.nan
    df.loc[df[c].le(0), c] = np.nan
methods = df.discoverymethod.value_counts()
main_methods = methods[methods >= 25].index.tolist()
missing = [
    dict(
        x=l,
        y=m,
        value=float(df.loc[df.discoverymethod == m, c].isna().mean() * 100),
        n=int((df.discoverymethod == m).sum()),
    )
    for m in main_methods
    for c, l in zip(fields, labels)
]
r = rho(df, "pl_orbper", "pl_rade")
within = []
for m in main_methods:
    rr = rho(df[df.discoverymethod == m], "pl_orbper", "pl_rade")
    within.append(
        dict(label=m, **rr, support="n<20，仅作探索" if rr["n"] < 20 else "报告有效 n")
    )
pair = df.dropna(subset=["pl_orbper", "pl_rade"])
points = pair[["pl_orbper", "pl_rade", "discoverymethod", "pl_name"]].rename(
    columns={
        "pl_orbper": "x",
        "pl_rade": "y",
        "discoverymethod": "group",
        "pl_name": "label",
    }
)[["x", "y", "group", "label"]]
periods = quantiles(df, "discoverymethod", "pl_orbper", 25)
trend = (
    df.groupby(["disc_year", "discoverymethod"], as_index=False)
    .size()
    .rename(columns={"disc_year": "x", "discoverymethod": "group", "size": "value"})
)
# Insert true zero count year/method pairs for continuous curves.
index = pd.MultiIndex.from_product(
    [range(int(df.disc_year.min()), int(df.disc_year.max()) + 1), methods.index],
    names=["x", "group"],
)
trend = trend.set_index(["x", "group"]).reindex(index, fill_value=0).reset_index()
mass = df[df.pl_bmassprov.eq("Mass")].dropna(subset=["pl_bmasse", "pl_rade"])
mp = mass[["pl_bmasse", "pl_rade", "discoverymethod", "pl_name"]].rename(
    columns={
        "pl_bmasse": "x",
        "pl_rade": "y",
        "discoverymethod": "group",
        "pl_name": "label",
    }
)[["x", "y", "group", "label"]]
missing_radius = float(df.pl_rade.isna().mean())
transit = float(df.discoverymethod.eq("Transit").mean())
findings = [
    finding(
        "先把“参数行”还原成“行星”",
        f"原始 {len(raw):,} 行是文献参数集。主样本只取 Published Confirmed 且 default_flag=1，得到 {len(df):,} 个唯一行星；直接统计原表会把不同文献和候选目录反复计数。",
    ),
    finding(
        "测量方法塑造了能看见的关系",
        f"默认确认样本中 Transit 占 {transit:.1%}。周期与半径的 pooled Spearman ρ={r['rho']:.3f}（成对完整 n={r['n']:,}）。分方法完整样本里，Radial Velocity 仅 28 个，Imaging 仅 7 个；这些小样本不足以支持稳定的跨方法比较。完整案例的选择本身就改变了样本。",
    ),
    finding(
        "缺失本身就是观测机制的证据",
        f"剔除上/下限值与非正值后，半径缺失率为 {missing_radius:.1%}。质量–半径图进一步要求 pl_bmassprov=Mass，只保留 {len(mass):,} 个完整点，排除由半径推算的质量，以免制造循环关系。",
    ),
]
charts = [
    chart(
        "scatter",
        "周期与半径：用发现方法拆开总体关系",
        "全量成对完整样本。双对数坐标；选择方法或刷选区域，联动查看构成和分布。",
        rec(points),
        xLabel="轨道周期 / 天",
        yLabel="半径 / 地球半径",
        scaleX="log",
        scaleY="log",
        population=len(pair),
    ),
    chart(
        "heatmap",
        "哪些方法没有提供哪些物理量？",
        "有效测量缺失率 %；含上/下限的参数在相关分析中视为缺失。",
        missing,
        percent=True,
    ),
    chart(
        "table",
        "总体与方法内的相关性",
        "Spearman 秩相关，不做因果解释；同一恒星系统内行星可能相关。",
        [dict(label="全部", **r)] + within,
    ),
    chart(
        "box",
        "不同方法采到的轨道周期",
        "中位数、IQR、P10–P90，n≥25；对数横轴。",
        periods,
        unit="天",
        scale="log",
    ),
    chart(
        "line",
        "发现历史：统计唯一确认行星",
        "每个行星仅计一次；2026 为快照当年，不能与完整年直接比较。",
        rec(trend),
        xLabel="发现年",
        yLabel="行星数",
    ),
    chart(
        "scatter",
        "质量–半径关系：排除推算质量",
        "仅保留质量来源 Mass、非限制值、双变量为正且完整。",
        rec(mp),
        xLabel="质量 / 地球质量",
        yLabel="半径 / 地球半径",
        scaleX="log",
        scaleY="log",
        population=len(mass),
    ),
]
finish(
    OUT,
    raw,
    df,
    dict(
        title="NASA Exoplanets",
        kicker="OBSERVATION / SELECTION / PHYSICS",
        question="行星的物理关系，有多少来自发现方法与测量覆盖的选择？",
        theme="space",
        description="这是 NASA Exoplanet Archive 的 Planetary Systems（PS）表。NASA 说明该表合并了 Confirmed Planets 与 Extended Planet Data，并同时提供行星、宿主恒星和系统属性；原始表包含不同文献和参数解，不能直接当成唯一行星清单。",
        purpose="用于研究发现方法、文献参数和测量缺失如何影响我们观察到的行星周期、半径、质量及恒星属性关系。",
        unit="原始一行代表一个行星参数/文献解；主分析限定 Published Confirmed、default_flag=1，并以唯一确认行星作为主要统计单位。",
        source_note="通过 NASA Exoplanet Archive TAP 的 ps 表下载；本地文件是 2026-09-11 的快照，不代表之后新增的完整年度数据。",
        references=[
            ["NASA Exoplanet Archive 概览", "https://exoplanetarchive.ipac.caltech.edu/docs/intro.html"],
            ["Planetary Systems 表说明", "https://exoplanetarchive.ipac.caltech.edu/docs/planetarysystems_about.html"],
            [
                "NASA 参数定义",
                "https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html",
            ]
        ],
    ),
    findings,
    charts,
    {
        "correlations_by_method": within,
        "measurement_missingness": missing,
        "period_distribution": periods,
        "confirmed_planets": df[
            ["pl_name", "hostname", "default_flag", "discoverymethod", "disc_year"]
            + fields
        ],
        "limits_removed": limits,
    },
    [source],
    [
        "原始 355 列逐列审计；原表是文献参数集而非唯一行星表。",
        "取 Published Confirmed 且 default_flag=1；断言 pl_name 唯一。",
        "各物理参数剔除 limit flag 非零和非正值。",
        "计算 pooled / 方法内 Spearman 和方法 × 参数缺失矩阵。",
        "质量–半径分析限定 pl_bmassprov=Mass，避免以半径推算质量再与半径相关。",
    ],
    [
        "探测样本不等于宇宙总体，不能推断行星真实丰度或宜居概率。",
        "完整案例分析受非随机缺失影响；没有全表插补。",
        "同一恒星可有多颗行星，不将每个点视为独立随机抽样。",
        "快照截止 2026-09-11；2026 年发现数量未覆盖全年。",
    ],
    {
        "unique_planets": int(df.pl_name.nunique()),
        "default_confirmed_rows": len(df),
        "period_radius_complete": len(pair),
        "measured_mass_radius_complete": len(mass),
    },
)
