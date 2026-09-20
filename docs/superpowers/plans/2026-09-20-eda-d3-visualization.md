# EDA + D3 六数据集交付 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为六个已选数据集生成独立、可复现的 EDA 代码、D3 交互页面和简短汇报材料。

**Architecture:** 每个项目在 `projects/<slug>/` 中自包含；Python EDA 读取现有数据并写出聚合 JSON/CSV，D3 页面只加载聚合产物。根目录提供统一运行和验证入口，但项目之间不共享运行时状态。

**Tech Stack:** Python 3.12, pandas/numpy, D3 v7 CDN, 原生 HTML/CSS/JavaScript, Git.

**Spec:** `docs/superpowers/specs/2026-09-20-eda-d3-visualization-design.md`

## Global Constraints

- 六个数据集必须分别位于独立文件夹。
- 暂不写正式 report；每个项目提供 EDA README 和短汇报要点。
- D3 页面不读取完整原始大表，只读取 EDA 生成的聚合数据。
- 所有清洗决定必须在 README 和代码中可追溯。

## Review Focus

- NASA 的高缺失和 candidate/confirmed 状态不能被页面误读为完整观测。
- Steam 的重复 `appid` 和多表 join 必须在 EDA 中显式记录。
- College 的隐私抑制值与小 cohort 不得呈现为精确总体结论。
- 幸福报告的数值是三年平均评价，页面必须标明时间语义。
- 用户直接打开 HTML 时不能依赖本地 fetch；数据应以 `data.js` 方式可加载。

### Task 1: 仓库与共享运行入口

**Files:** `README.md`, `.gitignore`, `scripts/run_all_eda.py`, `scripts/verify_projects.py`

- [ ] 写入项目目录约定、运行命令和本地静态服务器命令。
- [ ] 提供按项目顺序运行六个 `eda.py` 的入口。
- [ ] 验证每个项目均生成 `eda_summary.json`、`eda_profile.csv`、`site/data.js`。

### Task 2: NYC Film Permits

**Files:** `projects/nyc-film-permits/eda.py`, `README.md`, `index.html`, `site/data.js`

- [ ] 输出时间序列、borough、event type、category 和 top company 聚合。
- [ ] 页面提供年度许可趋势、borough 排名、事件类型堆叠和日期/borough 筛选。

### Task 3: NASA Exoplanets

**Files:** `projects/nasa-exoplanets/eda.py`, `README.md`, `index.html`, `site/data.js`

- [ ] 保留 `soltype`/`default_flag` 状态，计算发现年份、方法、RA/DEC、轨道周期、平衡温度和半径的可视化子集。
- [ ] 页面提供发现趋势、方法对比、天球散点和物理量散点。

### Task 4: College Majors 2026

**Files:** `projects/college-majors-2026/eda.py`, `README.md`, `index.html`, `site/data.js`

- [ ] 计算专业家庭、证书层级、收入/债务/就业/AI 指标和州级聚合。
- [ ] 页面提供收入-债务散点、专业家庭比较、AI 职业暴露和轨迹筛选。

### Task 5: Central Park Squirrel Census

**Files:** `projects/central-park-squirrels/eda.py`, `README.md`, `index.html`, `site/data.js`

- [ ] 解析日期和经纬度，计算颜色、班次、地块、行为率与空间网格。
- [ ] 页面提供地图散点、行为雷达/条形比较、班次和颜色筛选。

### Task 6: Steam Games V2

**Files:** `projects/steam-games-v2/eda.py`, `README.md`, `index.html`, `site/data.js`

- [ ] 对三张表按 `appid` 去重，报告连接覆盖率和重复数量，拆分价格、类型、年份、评价和并发玩家。
- [ ] 页面提供发行趋势、价格-评价/CCU 散点、类型排名和来源覆盖率。

### Task 7: World Happiness Report

**Files:** `projects/world-happiness/eda.py`, `README.md`, `index.html`, `site/data.js`, `data/processed/world-happiness/world_happiness.csv`

- [ ] 从原始 xlsx 生成可复现的 CSV 副本，聚合年度排名、国家轨迹、区间和解释变量。
- [ ] 页面提供年度趋势、国家排名动画/筛选、区间图和解释变量构成。

### Task 8: 统一汇报与验证

**Files:** `presentation_outline.md`, `scripts/verify_projects.py`

- [ ] 写出不超过 5 分钟的汇报提纲，包含选题差异、清洗风险和推荐后续。
- [ ] 运行全部 EDA、结构验证和静态文件检查；记录结果。
