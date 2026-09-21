from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from eda_support import *

OUT = Path(__file__).resolve().parent
source = "data/processed/college-majors/college_majors_2026.csv"
raw = pd.read_csv(ROOT / source, low_memory=False)
assert raw.program_id.is_unique
earn = "median_earnings_4yr_usd"
debt = "median_debt_usd"
ai = "ai_software_occupation_share"
df = raw.copy()
pair = (
    df[df.earnings_4yr_status.eq("reported") & df.debt_status.eq("reported")]
    .dropna(subset=[earn, debt])
    .copy()
)
pair = pair[(pair[earn] > 0) & (pair[debt] >= 0)]
coverage = []
for cred, g in raw.groupby("credential_name"):
    for label, col in [
        ("4 年收入", earn),
        ("债务", debt),
        ("1 年收入", "median_earnings_1yr_usd"),
        ("5 年收入", "median_earnings_5yr_usd"),
    ]:
        coverage.append(
            dict(
                x=label,
                y=cred,
                value=float(g[col].notna().mean() * 100),
                n=len(g),
                reported=int(g[col].notna().sum()),
            )
        )
correlations = [dict(label="全部 credential", **rho(pair, earn, debt))]
for c, g in pair.groupby("credential_name"):
    correlations.append(dict(label=c, **rho(g, earn, debt)))
# Institution means and broad strata are descriptive controls, not causal adjustment.
ranked = pair[[earn, debt]].rank()
strata = pair.cip_family_title.fillna("Unknown") + " / " + pair.credential_name
res = ranked - ranked.groupby(strata).transform("mean")
adjusted = float(res.corr().iloc[0, 1])
bachelor = pair[pair.credential_name.eq("Bachelor's Degree")].copy()
# AI occupation link is replicated across institutions; use major-level unit, not every program.
ba = raw[raw.credential_name.eq("Bachelor's Degree")].copy()
major = ba.groupby(["cip_code_4digit", "cip_title"], as_index=False).agg(
    earnings=(earn, "median"),
    reported_n=(earn, "count"),
    ai=(ai, "median"),
    institutions=("institution_name", "nunique"),
    debt=(debt, "median"),
    family=("cip_family_title", "first"),
)
major = major[(major.reported_n >= 10) & major.earnings.gt(0) & major.ai.notna()]
ar = rho(major, "ai", "earnings")
family = []
for f, g in bachelor.groupby("cip_family_title"):
    if len(g) < 30:
        continue
    family.append(
        dict(
            label=f,
            x=float(g[debt].median()),
            y=float(g[earn].median()),
            n=len(g),
            group="专业大类",
        )
    )
front = []
for d in family:
    d["frontier"] = not any(
        z["x"] <= d["x"] and z["y"] >= d["y"] and (z["x"] < d["x"] or z["y"] > d["y"])
        for z in family
    )
    d["group"] = "样本内非支配" if d["frontier"] else "其他专业大类"
    front.append(d)
sc = sample(pair).rename(
    columns={debt: "x", earn: "y", "credential_name": "group", "program_id": "id"}
)
sc["label"] = sc.institution_name + " / " + sc.cip_title
ain = major.rename(columns={"ai": "x", "earnings": "y", "cip_title": "label"}).copy()
top_families = major.family.value_counts().head(8).index
ain["group"] = ain.family.where(ain.family.isin(top_families), "其他专业大类")
ain["label"] = ain["label"] + " / " + ain.family
status_counts = raw.earnings_4yr_status.value_counts().to_dict()
valid_share = len(pair) / len(raw)
findings = [
    finding(
        "“可比较样本”比原始规模小得多",
        f"{len(raw):,} 个项目中，4 年收入被隐私抑制的有 {status_counts.get('privacy_suppressed', 0):,} 个；同时报告收入和债务且值有效的仅 {len(pair):,} 个（{valid_share:.1%}）。热力图展示 credential 层面的报告率，避免完整案例偏差被大样本量掩盖。",
    ),
    finding(
        "收入与债务关系需要按层级拆开",
        f"完整案例总体 Spearman ρ={correlations[0]['rho']:.3f}；对全样本秩值在“专业大类 × credential”内去均值后，残差相关为 {adjusted:.3f}。这是粗分层诊断，尚未控制院校选择、家庭背景和 cohort 构成。",
    ),
    finding(
        "AI 关系改用专业作为分析单位",
        f"只保留本科且至少 10 个项目报告收入的 {len(major)} 个 CIP 专业，每个专业只计一次；AI 关联职业占比与项目收入中位数的 Spearman ρ={ar['rho']:.3f}。这里的 AI 指标表示职业链接中的软件工具覆盖，不表示替代概率。",
    ),
    finding(
        "收入–债务前沿是探索工具",
        f"本科完整案例按专业大类聚合并要求 n≥30，共 {len(family)} 个专业大类，其中 {sum(d['frontier'] for d in front)} 个处于样本内“债务较低、收入较高”的非支配前沿。均为项目中位数的中位数，未按毕业生人数加权，不是个人投资回报。",
    ),
]
charts = [
    chart(
        "scatter",
        "收入 × 债务：比较同一学位层级",
        "分析统计使用全量完整案例；交互图固定随机种子抽取最多 4,500 条。选择 credential 或刷选区域查看构成。",
        rec(sc[["x", "y", "group", "label"]]),
        xLabel="项目债务中位数 / USD",
        yLabel="4 年收入中位数 / USD",
        scaleX="symlog",
        scaleY="log",
        population=len(pair),
    ),
    chart(
        "heatmap",
        "谁的结果被报告出来？",
        "颜色 = 非缺失报告率 %；悬停显示项目数和有值数。",
        coverage,
        percent=True,
    ),
    chart(
        "table",
        "总体、credential 内与分层后的关系",
        "前几行是 Spearman；最后一行是秩值分层去均值后的 Pearson，不是因果估计。",
        correlations
        + [dict(label="秩值按专业大类 × credential 去均值", n=len(pair), rho=adjusted)],
    ),
    chart(
        "scatter",
        "AI 暴露 × 收入：一个专业只计一次",
        "本科；CIP 专业收入为机构项目中位数的中位数；每专业至少 10 个报告值；颜色保留八个最多专业的专业大类，其余合并。",
        rec(ain[["x", "y", "group", "label"]]),
        xLabel="AI 关联职业占比 / 0–1",
        yLabel="专业项目收入中位数 / USD",
        scaleY="log",
        population=len(major),
    ),
    chart(
        "scatter",
        "本科专业大类的收入–债务前沿",
        "颜色标出样本内非支配专业大类；仅完整收入/债务对，n≥30。悬停查看名称。",
        front,
        xLabel="专业大类债务中位数 / USD",
        yLabel="专业大类 4 年收入中位数 / USD",
        population=len(front),
    ),
    chart(
        "box",
        "学位层级的收入分布",
        "完整收入–债务案例中的收入；P10–P90、IQR 和中位数。",
        quantiles(pair, "credential_name", earn, 30),
        unit="USD",
    ),
]
finish(
    OUT,
    raw,
    pair,
    dict(
        title="College Majors 2026",
        kicker="EDUCATION / DEBT / OPPORTUNITY",
        question="高收入专业也意味着高债务吗？学位层级与隐私抑制如何改变答案？",
        theme="college",
        description="这是 Kaggle 发布的 College Majors 2026: Earnings, Debt, Jobs, AI 整合表，面向美国高校项目与职业结果探索。它把学校、CIP 专业、学位层级、收入、债务、就业和 AI 关联职业字段拼在同一张研究表中，不是一张单一的官方原始表。",
        source_description="原始页面简介（中文整理）：Kaggle 数据集以“College Majors 2026: Earnings, Debt, Jobs, AI”为题，配套分析围绕大学项目的收入、债务、就业结果和 AI 关联职业指标展开；页面显示 CSV 包含 227,980 行和 72 个字段。",
        purpose="用于研究专业大类和学位层级如何对应收入、债务、就业与 AI 职业暴露，并观察隐私抑制如何改变可比较样本。",
        unit="一行大致对应一个学校 × CIP 专业 × credential 项目；部分结果在跨校区共享，收入与债务的 privacy_suppressed 必须保留为状态而不能填成零。",
        source_note="本地文件来自 Kaggle 数据集；数据集页面将它作为教育结果与 AI 关联指标的整合数据，具体上游字段和 cohort 年份需在报告中注明，不能包装成个人级调查。",
        references=[
            ["Kaggle College Majors 2026", "https://www.kaggle.com/datasets/kylefengkfeng209/college-majors-2026-earnings-debt-jobs-ai"],
            ["Kaggle 数据分析页面", "https://www.kaggle.com/code/lalit7881/college-majors-2026-earnings-debt-jobs-ai-eda"],
        ],
    ),
    findings,
    charts,
    {
        "coverage": coverage,
        "correlations": correlations,
        "stratified_rank_correlation": {"n": len(pair), "rho": adjusted},
        "major_level_ai": major,
        "family_frontier": front,
        "credential_distributions": quantiles(pair, "credential_name", earn, 30),
    },
    [source],
    [
        "原表 72 列审计，验证 program_id 唯一。保留 privacy_suppressed 状态，不填 0。",
        "主样本要求 4 年收入和债务均 reported、完整、收入正且债务非负。",
        "计算 credential × 结果报告率，以及总体和层级内秩相关。",
        "对秩值按专业大类 × credential 去均值，检查组间混杂的影响。",
        "AI 分析仅本科，按 CIP 专业聚合，每专业至少 10 个有收入项目。",
        "本科专业大类前沿以完整配对样本聚合，n≥30；仅用于描述。",
    ],
    [
        "Kaggle 拼接数据，源 cohort 年份和跨校园共享结果仍限制可比性。",
        "机构/职业链接重复、非随机隐私抑制仍存在；无个人级因果解释。",
        "AI 指标不是自动化风险，也不是调查得到的实际使用比例。",
        "前沿不是个人择校建议；金额是项目中位数的汇总。",
    ],
    {
        "complete_pairs": len(pair),
        "ai_major_count": len(major),
        "ai_spearman": ar,
        "reported_earnings": int(raw[earn].notna().sum()),
        "scatter_sample": len(sc),
    },
)
