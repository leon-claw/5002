from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from eda_support import *

OUT = Path(__file__).resolve().parent
source = "data/raw/central-park-squirrel-census.csv"
raw = pd.read_csv(ROOT / source)
df = raw.copy()
id_excess = int(df["Unique Squirrel ID"].duplicated().sum())
df["date"] = pd.to_datetime(
    df.Date.astype(str).str.zfill(8), format="%m%d%Y", errors="coerce"
)
beh = [
    "Running",
    "Chasing",
    "Climbing",
    "Eating",
    "Foraging",
    "Approaches",
    "Indifferent",
    "Runs from",
    "Tail twitches",
]
for c in beh:
    df[c] = df[c].astype("boolean")
# Phi correlation measures association between binary observations.
phi = []
for a in beh:
    for b in beh:
        d = df[[a, b]].dropna() if a != b else df[[a]].dropna()
        value = 1.0 if a == b else float(d[a].astype(int).corr(d[b].astype(int)))
        phi.append(dict(x=a, y=b, value=value, n=len(d)))
rates = []
for shift, g in df.groupby("Shift"):
    for b in beh:
        valid = g[b].dropna()
        k = int(valid.sum())
        n = len(valid)
        lo, hi = wilson(k, n)
        rates.append(
            dict(
                label=b + " / " + shift,
                behavior=b,
                group=shift,
                n=n,
                value=100 * k / n,
                lo=100 * lo,
                hi=100 * hi,
            )
        )
# Compare AM/PM within hectares observed in both shifts, equal hectare weight.
by = df.groupby(["Hectare", "Shift"])[beh].mean().unstack("Shift")
shared = by.dropna()
rng = np.random.default_rng(SEED)
contrasts = []
for b in beh:
    delta = (shared[(b, "PM")] - shared[(b, "AM")]).to_numpy(dtype=float)
    boot = np.array(
        [rng.choice(delta, size=len(delta), replace=True).mean() for _ in range(1000)]
    )
    contrasts.append(
        dict(
            label=b,
            value=float(delta.mean() * 100),
            lo=float(np.quantile(boot, 0.025) * 100),
            hi=float(np.quantile(boot, 0.975) * 100),
            n=len(delta),
        )
    )
contrasts.sort(key=lambda d: abs(d["value"]), reverse=True)
strong = max((d for d in phi if d["x"] != d["y"]), key=lambda d: abs(d["value"]))
lead = contrasts[0]
points = []
for _, d in df.iterrows():
    points.append(
        dict(
            x=float(d.X),
            y=float(d.Y),
            group=str(d.Shift),
            label=d["Unique Squirrel ID"],
            fur=str(d["Primary Fur Color"])
            if pd.notna(d["Primary Fur Color"])
            else "Unknown",
            behavior=", ".join(b for b in beh if pd.notna(d[b]) and d[b]),
        )
    )
calendar = df.groupby(["date", "Shift"]).size().reset_index(name="value")
calendar["x"] = calendar.date.dt.strftime("%m-%d")
calendar = calendar.rename(columns={"Shift": "y"})
fur = df["Primary Fur Color"].fillna("Unknown").value_counts()
furrows = [dict(label=k, value=int(v)) for k, v in fur.items()]
findings = [
    finding(
        "行为组合比单一排名更有信息",
        f"在 {len(df):,} 条观测里，所选行为中绝对值最大的非对角 φ 相关为 {strong['x']} 与 {strong['y']}：φ={strong['value']:.3f}。这些布尔行为允许同时出现，不能画成互斥类别饼图。",
    ),
    finding(
        "把 AM/PM 差异放回同一空间比较",
        f"同时出现 AM 与 PM 观测且所选行为完整的 {len(shared)} 个 hectare 内，等权平均的 {lead['label']} 差值（PM−AM）为 {lead['value']:+.1f} 个百分点；按 hectare 重采样 1,000 次的探索性 95% 区间为 [{lead['lo']:+.1f}, {lead['hi']:+.1f}]。",
    ),
    finding(
        "空间热点首先是“观察热点”",
        f"普查覆盖 {df.date.nunique()} 个日期、{df.Hectare.nunique()} 个 hectare。地图保持经纬度局部比例，支持缩放、班次和毛色筛选。没有记录搜索时间和漏检率，因此点密度不等于松鼠真实密度。",
    ),
]
sensitivity = (
    max(
        abs(df[b].mean() - df.drop_duplicates("Unique Squirrel ID")[b].mean())
        for b in beh
    )
    * 100
)
findings.append(
    finding(
        "观察 ID 并非完全唯一",
        f"有 {id_excess} 条超额重复 ID 记录，坐标不同，不能直接判定为重复观测。主分析保留全部记录；按 ID 仅保留首条后的敏感性检查中，所选行为率最大变化为 {sensitivity:.3f} 个百分点。",
    )
)
charts = [
    chart(
        "map",
        "公园尺度的观察分布",
        "局部等比例投影；滚轮缩放、拖动平移，按班次与毛色筛选。颜色=班次。",
        points,
    ),
    chart(
        "heatmap",
        "行为共现矩阵",
        "φ 系数（两个布尔变量的 Pearson 相关）；颜色从 −1 到 +1。",
        phi,
        diverging=True,
        fixedDomain=1,
    ),
    chart(
        "interval",
        "同一 hectare 内的 AM/PM 差异",
        "PM−AM，百分点；点=等权 hectare 平均，线=hectare bootstrap 95% 区间。抽样偏差仍存在。",
        contrasts,
        unit="百分点",
        zero=True,
    ),
    chart(
        "interval",
        "原始班次行为率与区间",
        "Wilson 95% 区间仅作为独立观测假设下的参考，不校正空间聚类。",
        rates,
        unit="%",
        zero=False,
    ),
    chart(
        "heatmap",
        "观测日程 × 班次",
        "检查 AM/PM 的日期覆盖，解释潜在混杂。",
        rec(calendar[["x", "y", "value"]]),
    ),
    chart(
        "bar",
        "毛色覆盖与 Unknown",
        "可从地图毛色控件继续探索空间分布。",
        furrows,
        unit="观测",
    ),
]
finish(
    OUT,
    raw,
    df,
    dict(
        title="Central Park Squirrels",
        kicker="FIELD ECOLOGY / CITIZEN SCIENCE",
        question="早晚行为真的不同，还是观察地点和日程改变了我们看到的松鼠？",
        theme="park",
        description="这是 2018 Central Park Squirrel Census 的 citizen-science 观测表。NYC OpenData 说明，该项目关注东部灰松鼠，并为 3,023 次观测记录坐标、年龄、毛色、海拔、活动、叫声以及与松鼠和人类的互动。",
        source_description="原始页面简介（中文翻译）：Squirrel Census 是一个聚焦东部灰松鼠的科学、设计和故事讲述项目；项目统计松鼠并向公众展示结果。该表记录 3,023 次观测，包括坐标、年龄、主/次毛色、海拔、活动、沟通以及与松鼠和人类的互动。",
        purpose="用于研究中央公园中松鼠的空间分布、AM/PM 行为差异和行为组合，同时展示公民科学观察的抽样边界。",
        unit="一行代表一次松鼠观测，不代表一个被长期追踪的生物个体；坐标、hectare、班次和多个非互斥行为字段共同描述这次观察。",
        source_note="官方记录来自 NYC OpenData / Data.gov；本地 CSV 是 2018 年普查数据的公开镜像，数据页最后更新于 2023-04-18。",
        references=[
            ["NYC OpenData / Data.gov 数据说明", "https://catalog.data.gov/dataset/2018-central-park-squirrel-census-squirrel-data"],
            ["The Squirrel Census 项目主页", "https://www.thesquirrelcensus.com/"],
            ["NYC OpenData 数据页", "https://data.cityofnewyork.us/d/vfnx-vebw"],
        ],
    ),
    findings,
    charts,
    {
        "behavior_phi": phi,
        "raw_shift_rates": rates,
        "hectare_adjusted_shift_difference": contrasts,
        "date_shift_counts": calendar,
        "shared_hectares": {"n": len(shared)},
    },
    [source],
    [
        "原始 31 字段与观察 ID 重复审计；日期按 MMDDYYYY 解析。",
        "行为转换为 nullable boolean，缺失不当作 False。",
        "计算非互斥行为的 φ 共现矩阵和 AM/PM Wilson 区间。",
        "只在共同 hectare 内比较 AM/PM，hectare 等权；固定随机种子做 1,000 次块级 bootstrap。",
        "地图基于全部原始点，按局部距离比例投影；不伪造移动轨迹或调查边界。",
    ],
    [
        "一次观察普查，不是追踪个体；观察 ID 不能保证松鼠生物个体独立。",
        "hectare 控制只消除部分空间构成差异，天气、日期、观察者与搜索时长仍未知。",
        "区间是探索性不确定性表达，不修正便利抽样和多重比较。",
        "地图无外部底图，显示实际坐标与比例尺，不代表测量了公园边界。",
    ],
    {
        "raw_columns": 31,
        "distinct_observation_ids": int(df["Unique Squirrel ID"].nunique()),
        "duplicate_id_excess": id_excess,
        "dedup_rate_max_change_pp": float(sensitivity),
        "shared_hectares": len(shared),
        "bootstrap_reps": 1000,
    },
)
