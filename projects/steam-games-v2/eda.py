from pathlib import Path
import sys, re
from itertools import combinations

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from eda_support import *

OUT = Path(__file__).resolve().parent
sources = [
    "data/processed/steam/extended_steam_games.csv",
    "data/processed/steam/steam_games_wikidata.csv",
    "data/processed/steam/steamspy_raw.csv",
]
raw, wiki, spy = [pd.read_csv(ROOT / p, low_memory=False) for p in sources]


def canonical(d):
    # No timestamp exists. Completeness then review count is a declared, reproducible choice.
    x = d.copy()
    x["_complete"] = x.notna().sum(axis=1)
    x["_order"] = np.arange(len(x))
    x["_reviews"] = pd.to_numeric(
        x.get("positive", pd.Series(0, index=x.index)), errors="coerce"
    ).fillna(0) + pd.to_numeric(
        x.get("negative", pd.Series(0, index=x.index)), errors="coerce"
    ).fillna(0)
    return (
        x.sort_values(
            ["appid", "_complete", "_reviews", "_order"],
            ascending=[True, False, False, True],
        )
        .drop_duplicates("appid")
        .drop(columns=["_complete", "_order", "_reviews"])
    )


df = canonical(raw)
spy_clean = canonical(spy)
conflicting = sum(
    g.drop_duplicates().shape[0] > 1 for _, g in raw.groupby("appid") if len(g) > 1
)
# Aggregate multiple categorical source values instead of creating many-to-many rows.
wiki_clean = wiki.groupby("appid", as_index=False).agg(
    game_engine=(
        "game_engine",
        lambda s: "; ".join(sorted(set(s.dropna().astype(str)))),
    )
)
df = df.merge(
    wiki_clean, on="appid", how="left", validate="one_to_one", indicator="wiki_join"
)
df = df.merge(
    spy_clean[["appid", "ccu", "positive", "price"]].rename(
        columns={c: "spy_" + c for c in ["ccu", "positive", "price"]}
    ),
    on="appid",
    how="left",
    validate="one_to_one",
    indicator="spy_join",
)
assert df.appid.is_unique
# SteamSpy schema reports current US price in cents. Preserve raw price and convert once.
df["usd"] = pd.to_numeric(df.price, errors="coerce") / 100
df["release"] = pd.to_datetime(
    df.release_date, format="mixed", dayfirst=False, errors="coerce"
)
df["year"] = df.release.dt.year
df["reviews"] = df.positive + df.negative
df["ratio"] = df.positive / df.reviews.replace(0, np.nan)
df["genre_list"] = df.genres.fillna("").map(
    lambda s: sorted(set(x.strip() for x in s.split(",") if x.strip()))
)
df["primary_genre"] = df.genres.fillna("Unknown").str.split(",").str[0].str.strip()
df["price_group"] = np.select(
    [df.usd.eq(0), df.usd.le(10), df.usd.le(30)],
    ["当前价格为零", "付费 ≤$10", "付费 $10–30"],
    default="付费 >$30",
)
valid = df[df.reviews.ge(50) & df.ccu.ge(0) & df.usd.ge(0)].copy()
corr = rho(valid, "ratio", "ccu")
by = []
for g, d in valid.groupby("price_group"):
    by.append(dict(label=g, **rho(d, "ratio", "ccu")))
rank = valid[["ratio", "ccu"]].rank()
strata = valid.primary_genre + " / " + valid.year.fillna(-1).astype(str)
res = rank - rank.groupby(strata).transform("mean")
adjust = float(res.corr().iloc[0, 1])
ccu = df.ccu.fillna(0).clip(lower=0).sort_values()
total = float(ccu.sum())
topn = max(1, int(np.ceil(len(ccu) * 0.01)))
share = float(ccu.tail(topn).sum() / total)
lorenz = [
    dict(
        x=i / len(ccu) * 100,
        value=float(ccu.iloc[:i].sum() / total * 100),
        group="累计 CCU",
    )
    for i in np.unique(np.linspace(0, len(ccu), 151).astype(int))
]
lorenz += [dict(x=i, value=i, group="完全均等参照") for i in [0, 100]]
counts = {}
pairs = {}
for tags in df.genre_list:
    for t in tags:
        counts[t] = counts.get(t, 0) + 1
    for a, b in combinations(tags, 2):
        pairs[(a, b)] = pairs.get((a, b), 0) + 1
edges = [
    dict(source=a, target=b, value=n, lift=n * len(df) / (counts[a] * counts[b]))
    for (a, b), n in pairs.items()
    if n >= 100 and counts[a] >= 100 and counts[b] >= 100
]
edges = sorted(edges, key=lambda d: d["value"], reverse=True)[:35]
used = {x for e in edges for x in [e["source"], e["target"]]}
network = dict(nodes=[dict(id=k, value=counts[k]) for k in sorted(used)], links=edges)
sc = sample(valid).rename(
    columns={"usd": "x", "ccu": "y", "price_group": "group", "name": "label"}
)
quality = valid.rename(
    columns={"ratio": "x", "ccu": "y", "price_group": "group", "name": "label"}
)
review_bins = pd.cut(
    valid.reviews,
    [49, 100, 1000, 10000, np.inf],
    labels=["50–100", "101–1,000", "1,001–10,000", ">10,000"],
)
qdist = quantiles(valid.assign(review_bin=review_bins), "review_bin", "ratio", 20)
parsed = int(df.release.notna().sum())
zeros = int(df.ccu.eq(0).sum())
wikim = float(df.wiki_join.eq("both").mean())
mismatch = int(df.ccu.ne(df.spy_ccu).sum())
findings = [
    finding(
        "CCU 极度集中，总体均值很容易误导",
        f"按唯一 appid 统计，CCU 最高的 1%（{topn} 个游戏）贡献 {share:.1%} 的快照 CCU；{zeros:,} 个游戏 CCU=0。价格图使用 symlog，保留零价格、零 CCU，不用 log 轴无声删除长尾。",
    ),
    finding(
        "好评率不等于热度",
        f"至少 50 条评价的 {len(valid):,} 个游戏中，好评率与 CCU 的 Spearman ρ={corr['rho']:.3f}。对秩值按首个类型标签 × 发行年去均值后为 {adjust:.3f}；两者差异提示类型与年龄构成值得关注，但未消除营销和存活偏差。",
    ),
    finding(
        "多标签组合需要同时看数量与 lift",
        f"网络保留共同出现≥100 次的前 {len(edges)} 对类型。线宽表示共同游戏数，悬停显示 lift=联合概率/(边际概率乘积)；高频类别不一定有最强的超预期共现。",
    ),
    finding(
        "多来源连接必须保留审计记录",
        f"主表 {len(raw):,} 行归并为 {len(df):,} 个 appid；{conflicting} 个重复键含冲突内容。采用完整度、评价数和原始顺序选择，不能称为“最新记录”。Wikidata 匹配率 {wikim:.1%}，SteamSpy CCU 不一致 {mismatch} 行；日期成功解析 {parsed:,} 行。",
    ),
]
charts = [
    chart(
        "scatter",
        "价格与活跃度：保留零值与长尾",
        "价格按 SteamSpy 美分字段除以 100；CCU 为快照并发。抽样最多 4,500 条，统计用全量。",
        rec(sc[["x", "y", "group", "label"]]),
        xLabel="当前价格 / USD",
        yLabel="快照 CCU",
        scaleX="symlog",
        scaleY="symlog",
        population=len(valid),
    ),
    chart(
        "line",
        "市场注意力有多集中？",
        "游戏按 CCU 从低到高排序；曲线越远离对角线，分布越集中。",
        lorenz,
        xLabel="累计游戏比例 / %",
        yLabel="累计 CCU 比例 / %",
    ),
    chart(
        "network",
        "类型之间的共现网络",
        "可拖动节点；边的 tooltip 显示游戏数和 lift。多标签结构，不是独立分类。",
        network,
    ),
    chart(
        "scatter",
        "好评率 × 热度：按价格层分开",
        "至少 50 条评价；CCU=0 保留。好评率来自累计评价，与快照热度的时间口径不同。",
        rec(sample(quality)[["x", "y", "group", "label"]]),
        xLabel="正面评价占比 / 0–1",
        yLabel="快照 CCU",
        scaleY="symlog",
        population=len(valid),
    ),
    chart(
        "table",
        "好评率与 CCU 的总体/分组关系",
        "Spearman；最后一行为类型 × 发行年内的秩残差 Pearson。",
        [dict(label="全部 ≥50 评价", **corr)]
        + by
        + [dict(label="类型 × 年份去均值", n=len(valid), rho=adjust)],
    ),
    chart(
        "box",
        "不同评价规模的好评率分布",
        "以累计评价数量分层；中位数/IQR/P10–P90。",
        qdist,
        unit="比例",
    ),
]
finish(
    OUT,
    raw,
    df,
    dict(
        title="Steam Games V2",
        kicker="DIGITAL MARKETS / ATTENTION ECONOMY",
        question="价格、好评与在线热度之间的关系，能跨过类型与发行年龄的差异吗？",
        theme="steam",
        description="这是一个以 appid 为连接键的 Steam 游戏多来源快照：主表包含商店字段和玩家参与指标，另有 SteamSpy 估计以及 Wikidata 元数据。它用于观察数字游戏市场中的价格、评价、在线人数、发行时间和多标签类型结构，不是 Valve 的销售账本。",
        purpose="用于研究价格、好评率、快照 CCU、发行年龄和游戏类型之间的关系，并展示长尾集中、多标签共现和多表连接的影响。",
        unit="主分析一行代表归并后的唯一 appid；genres/categories 是多标签字段，CCU、评价和价格来自不同时间口径，不能把它们直接解释成因果链。",
        source_note="本地文件是 Kaggle 发布的 Steam 数据快照，结合 Steam/SteamSpy/Wikidata 表；SteamSpy 官方说明其数据来自多日样本且对新游戏不可靠，因此这里把 CCU 当作快照指标。",
        references=[
            ["Kaggle Steam Games Dataset", "https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/data"],
            ["SteamSpy API", "https://steamspy.com/api.php"],
            ["SteamSpy 方法与限制", "https://steamspy.com/about"],
            [
                "SteamSpy 客户端字段说明",
                "https://jslth.github.io/steamr/reference/steamspy.html",
            ],
        ],
    ),
    findings,
    charts,
    {
        "price_group_correlations": by,
        "ccu_concentration": {
            "top_one_percent_n": topn,
            "top_share": share,
            "zero_ccu": zeros,
        },
        "genre_edges": edges,
        "join_audit": {
            "raw": len(raw),
            "unique_appids": len(df),
            "duplicate_key_excess": int(raw.duplicated("appid").sum()),
            "conflicting_keys": conflicting,
            "wikidata_match_rate": wikim,
            "steamspy_ccu_mismatches": mismatch,
            "parsed_dates": parsed,
        },
        "stratified_correlation": {"n": len(valid), "rho": adjust},
        "canonical_games": df[
            ["appid", "name", "usd", "ccu", "reviews", "ratio", "year", "primary_genre"]
        ],
    },
    sources,
    [
        "逐表检查 appid 重复与冲突；主表按完整度→评价数→原始顺序归并，无 timestamp 不假称最新。",
        "Wikidata 分类属性按键聚合，所有 merge 强制 one_to_one，验证行数与唯一性。",
        "保留美分原值并派生 USD；混合日期格式解析，记录失败数。",
        "评价关系要求 n_reviews≥50，零价格/零 CCU 均保留。",
        "比较总体、价格分层、类型 × 年份内秩相关。",
        "计算 CCU Lorenz 曲线和多标签共现 lift，限制低支持组合。",
    ],
    [
        "快照 CCU、累计评价、当前促销价格的时间口径不同，不推断价格导致流行。",
        "零价格可能与免费发行、不可购买或商店状态有关，不将零价格等同于 free-to-play。",
        "首个类型标签只是粗控制；发行年龄混杂仍可能存在。",
        "重复冲突只能按明确规则选择，没有可靠更新时间可确定真值。",
    ],
    {
        "unique_appids": int(df.appid.nunique()),
        "merged_rows": len(df),
        "valid_reviews_n": len(valid),
        "top_ccu_share": share,
        "price_conversion_divisor": 100,
    },
)
