# NASA Exoplanets

行星的物理关系，有多少来自发现方法与测量覆盖的选择？

## 数据集简介

这是 NASA Exoplanet Archive 的 Planetary Systems（PS）表。NASA 说明该表合并了 Confirmed Planets 与 Extended Planet Data，并同时提供行星、宿主恒星和系统属性；原始表包含不同文献和参数解，不能直接当成唯一行星清单。

**用途：** 用于研究发现方法、文献参数和测量缺失如何影响我们观察到的行星周期、半径、质量及恒星属性关系。

**观测单位：** 原始一行代表一个行星参数/文献解；主分析限定 Published Confirmed、default_flag=1，并以唯一确认行星作为主要统计单位。

**来源说明：** 通过 NASA Exoplanet Archive TAP 的 ps 表下载；本地文件是 2026-09-11 的快照，不代表之后新增的完整年度数据。

## 复现

从仓库根目录运行 `python3 projects/nasa-exoplanets/eda.py`，再运行 `python3 scripts/build_sites.py`。依赖见根目录 requirements.txt。

## 分析过程

1. 原始 355 列逐列审计；原表是文献参数集而非唯一行星表。
2. 取 Published Confirmed 且 default_flag=1；断言 pl_name 唯一。
3. 各物理参数剔除 limit flag 非零和非正值。
4. 计算 pooled / 方法内 Spearman 和方法 × 参数缺失矩阵。
5. 质量–半径分析限定 pl_bmassprov=Mass，避免以半径推算质量再与半径相关。

## 实际计算的结论

### 先把“参数行”还原成“行星”

原始 40,155 行是文献参数集。主样本只取 Published Confirmed 且 default_flag=1，得到 6,292 个唯一行星；直接统计原表会把不同文献和候选目录反复计数。

### 测量方法塑造了能看见的关系

默认确认样本中 Transit 占 73.6%。周期与半径的 pooled Spearman ρ=0.082（成对完整 n=4,640）。分方法完整样本里，Radial Velocity 仅 28 个，Imaging 仅 7 个；这些小样本不足以支持稳定的跨方法比较。完整案例的选择本身就改变了样本。

### 缺失本身就是观测机制的证据

剔除上/下限值与非正值后，半径缺失率为 25.8%。质量–半径图进一步要求 pl_bmassprov=Mass，只保留 1,411 个完整点，排除由半径推算的质量，以免制造循环关系。

## 局限

- 探测样本不等于宇宙总体，不能推断行星真实丰度或宜居概率。
- 完整案例分析受非随机缺失影响；没有全表插补。
- 同一恒星可有多颗行星，不将每个点视为独立随机抽样。
- 快照截止 2026-09-11；2026 年发现数量未覆盖全年。

## 可审计产物

`eda_profile.csv` 是原始字段统计，`analysis/` 保存全量分析汇总；页面抽样不用于计算结论。`site/data.js` 保存可视化数据。原始文件的 SHA-256 记录在页面的数据来源区域。
