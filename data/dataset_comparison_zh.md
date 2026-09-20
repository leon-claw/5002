# CityU 5002 Group Project 候选数据集评估

这份评估按课程目标来做：**Python 清洗与 EDA → 形成可解释的研究问题 → D3 交互可视化 → proposal/report/poster/presentation**。评分是老师视角的项目可行性模拟，不是数据集本身的客观排名。

逐列 profiling 已另存为 [`data/metadata/dataset_profiles.md`](metadata/dataset_profiles.md)，机器可读版本是 [`data/metadata/dataset_profiles.json`](metadata/dataset_profiles.json)。原始下载和解压文件都在 `data/raw/`、`data/processed/`。

## 下载与来源状态

| 候选 | 本地数据 | 来源和状态 |
|---|---|---|
| College Majors 2026 | `data/processed/college-majors/college_majors_2026.csv` | Kaggle 下载；数据看起来是把教育、就业、债务、职业和 AI 指标拼接后的项目级表 |
| Spotify 50k | `data/processed/spotify/spotify_tracks.csv` | Kaggle 下载；随包 README 明确写为 **synthetic Spotify-style tracks**，不能当真实 Spotify 目录或用户行为 |
| NYC Airbnb | `data/processed/airbnb/AB_NYC_2019.csv` | Kaggle 下载；2019 年快照 |
| Student Exam | `data/processed/student-exam/student_exam_performance.csv` | Kaggle 下载；Kaggle 描述为 large-scale **semi-synthetic** 数据 |
| NYC Film Permits | `data/raw/nyc-film-permits-historical.csv` | NYC Open Data 原链接在当前环境的导出端点返回 403；保存了公开 GitHub 历史镜像，覆盖 2011–2015，报告中不把它称为实时全量 |
| Global Happiness | `data/raw/world-happiness-report-2026-figure-2-1.xlsx` | 原笔记链接误贴成了 Film Permits；改用 World Happiness Report 官方 Figure 2.1 数据，2011–2025 |
| Central Park Squirrel | `data/raw/central-park-squirrel-census.csv` | NYC Open Data 的公开镜像；2018 citizen-science census |
| Hong Kong Beach | `data/raw/hong-kong-beach-historical-2025-tc.csv` | 香港环保署原始繁体中文 CSV，2025 |
| Steam Games V2 | `data/processed/steam/` 下 3 张表 | Kaggle 下载；extended、SteamSpy、Wikidata 三张表，需按 `appid` 谨慎合并 |
| NASA Exoplanets | `data/raw/nasa-exoplanets-ps.csv` | NASA Exoplanet Archive TAP `ps` 表，下载时的快照日期为 2026-09-11 |
| Netflix | `data/processed/netflix/titles.csv` + `credits.csv` | Kaggle 下载；catalog/credits 快照，含 IMDB/TMDB 衍生指标 |

## 总评分表

评分权重：课程契合度 25%，真实数据与来源 20%，维度和 EDA 深度 20%，D3 交互表达 15%，新颖性 10%，可执行性 10%。

| 排名 | 数据集 | 课程契合 /25 | 真实来源 /20 | EDA 深度 /20 | D3 表达 /15 | 新颖 /10 | 可执行 /10 | 总分 /100 | 老师会怎样看 |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | NYC Film Permits | 24 | 20 | 17 | 14 | 9 | 8 | **92** | 真实城市运行数据，时间、空间、类别和文本都能形成故事；历史镜像是主要限制 |
| 2 | NASA Exoplanets | 23 | 20 | 20 | 14 | 10 | 4 | **91** | 最有科学感和新颖性，但 355 列、46.65% 缺失、候选与确认状态混杂，范围容易失控 |
| 3 | College Majors 2026 | 24 | 17 | 20 | 14 | 9 | 6 | **90** | AI、学费、债务和收入结合得很当下；大量隐私抑制值必须严谨处理 |
| 4 | Central Park Squirrel Census | 21 | 20 | 13 | 14 | 10 | 8 | **86** | 真实 citizen-science 数据，地图故事很有记忆点；样本只覆盖一次短期普查 |
| 5 | Steam Games V2 | 23 | 17 | 18 | 14 | 8 | 7 | **87** | 维度多、图形空间大；多来源拼接、重复 appid 和 SteamSpy 估计值需要清洗说明 |
| 6 | World Happiness Report | 21 | 20 | 13 | 14 | 5 | 8 | **81** | 官方、易讲、适合地图和时间动画，但题材常见且是国家层面的生态比较 |
| 7 | NYC Airbnb 2019 | 21 | 16 | 15 | 14 | 4 | 9 | **79** | 非常稳妥，空间分析清楚；经典到容易和别组撞题，且数据已是旧快照 |
| 8 | Hong Kong Beach Water Quality | 18 | 20 | 8 | 14 | 9 | 9 | **78** | 本地真实数据很加分，但只有 3 个字段；单独做容易像 dashboard 而不像完整研究 |
| 9 | Student Exam Performance | 22 | 8 | 18 | 12 | 7 | 9 | **76** | 44 维度很适合练习 EDA/ML，但半合成数据和派生目标会削弱真实研究价值 |
| 10 | Netflix Titles + Credits | 19 | 14 | 15 | 13 | 3 | 8 | **72** | 结构清楚、有网络图可能性；缺少观看量和时间变化，常见且容易停在描述性统计 |
| 11 | Spotify 50k | 20 | 4 | 17 | 13 | 8 | 9 | **71** | 特征干净、交互漂亮，但明确是合成数据；只能研究模拟数据中的模式 |

## 逐个数据集的维度与项目判断

### 1. College Majors 2026

**数据粒度和维度。** 227,980 行 × 72 列；`program_id` 唯一，实际粒度接近「学校 × CIP 专业 × credential」。包含 6,774 所机构、429 个 CIP 专业、59 个州/地区、9 种 credential。字段可以分成六组：

1. 学校和地理：控制类型、主校区、城市、州、区域、经纬度、HBCU、招生率、SAT、招生人数、州内/州外学费。
2. 专业和教育形式：CIP code/title/family、credential level/name、distance education、年度授予数。
3. 收入：1 年、4 年、5 年 median earnings、全国 P25/median/P75、与全国差异、增长轨迹。
4. 债务：median debt、借款人数、月供、debt-to-earnings、payment-to-income。
5. 就业：工作比例、州内工作、失业/未工作计数、对应 SOC 职业、就业规模、工资、2024–34 增长和年度 openings。
6. AI/technology：使用 AI software 的职业数量/比例、expert-system share、AI 工具数、示例工具。

**EDA 事实。** 总体缺失单元 27.79%，但不是普通随机缺失：4 年收入只有 58,112 行报告，`median_debt_usd` 只有 46,673 行，`count_working_in_state_5yr`、`earnings_growth_pct_1yr_to_5yr` 等约 80%–83% 缺失，`earnings_*_status` 明确标注 `privacy_suppressed`。这些值不能填 0；应把“未报告/隐私抑制”作为状态分层，主分析只使用可比的 reported 子集，并报告样本量。

**适合的研究问题。** “不同专业和 credential 的收入—债务—就业机会前沿是什么？”或“AI 暴露与早期收入、职业增长之间是否存在可视化上的分层？”D3 可以做美国地图 + 专业/credential 筛选 + earnings/debt scatter、平行坐标或 slopegraph。要避免把观察到的相关性说成专业导致收入差异；收入 cohort、学校选择和职业选择都有混杂。

**老师会担心。** 这是 Kaggle 整合数据，不等于一张官方原始表；proposal 要交代每列的上游和 cohort 年份。若组员能把隐私抑制、样本筛选和不确定性说清楚，这是最有现实议题感的候选之一。

### 2. Spotify tracks 50k

**数据粒度和维度。** 50,000 行 × 21 列；50,000 个 `track_id`，2,400 个曲名、415 个 artist、481 个 album、20 个 genre，覆盖 2000–2024。维度包括 genre、popularity、explicit、duration，以及 danceability、energy、loudness、speechiness、acousticness、instrumentalness、liveness、valence、tempo、key、mode、time signature 等音频特征。缺失为 0%，但 `popularity` 的最小值是 -5，需先核验生成规则。

**关键事实。** 随包 README 明确写的是“50K synthetic Spotify-style tracks”，由程序生成，用于教育和 benchmark。它不是 Spotify 实际目录、播放量或用户日志，不能用“真实听众偏好”作结论。

**适合的研究问题。** “模拟数据中不同 genre 的音频空间如何分布？”或“valence/energy/danceability 如何形成可听感分区？”D3 适合 scatterplot matrix、genre hull、平行坐标和可点击“播放列表画像”。但要把结论写成“在该合成数据的规则下”，否则真实数据加分会被扣掉。

### 3. New York City Airbnb 2019

**数据粒度和维度。** 48,895 个房源 × 16 列；每行是 listing，`id` 唯一，37,457 个 host。空间字段是 5 个 borough、221 个 neighbourhood、latitude/longitude；业务字段是 room type、price、minimum nights、number of reviews、last review、reviews per month、host listing count、availability_365。

**EDA 事实。** 缺失 2.58%，主要集中在 `last_review` 和 `reviews_per_month`（各 10,052，20.56%）。price 中位数 106 美元，99 分位约 799 美元，11 行 price=0；minimum nights 最大 1,250，14 行超过 365，需要做异常敏感性分析。Manhattan 的 entire home/apt 中位数约 191 美元，Brooklyn 约 145 美元，空间差异很适合讲清楚。

**D3 和风险。** 地图、房型/价格筛选、borough→neighbourhood drill-down 很稳。但这是 2019 快照，不能代表今天的 Airbnb 市场；reviews 不是入住量，不能把相关性讲成价格因果。题材常见，新颖性最低一档。

### 4. Student Exam Performance & Success

**数据粒度和维度。** 100,000 行 × 44 列，`student_id` 唯一。六个域：人口/家庭背景（gender、education、school type、family income、parent education、urban/rural）；学业基线（previous score/GPA、attendance、assignment completion、participation、tuition）；学习行为（study hours、self-study、online learning、method、revision、practice tests）；睡眠/心理（sleep、stress、motivation、anxiety）；资源和环境（internet、device、apps、courses）；考试过程和结果（difficulty、preparation days、questions attempted/correct、time management、exam score、grade、pass、level）。

**EDA 事实。** 总体缺失约 1.19%，但 attendance 缺 9.86%、time management 9.61%、notes quality 8.41%、previous GPA 7.79%。`exam_score` 均值 61.95、标准差 15.86，Pass 约 77.4%。与分数的线性相关中，previous_exam_score 约 0.494、study_hours_per_day 约 0.363、stress 约 -0.162。`pass_status`、`performance_grade`、`performance_level` 很可能由 exam_score 派生，不能把它们和 score 同时当独立预测变量，否则会产生 target leakage。

**项目判断。** 它适合 EDA、分类和交互式“学习画像”，但 Kaggle 描述是 semi-synthetic；proposal 需说明数据不是学校真实学生档案，也不能据此评价真实教育政策。D3 可做平行坐标、条件分布和 subgroup comparison。

### 5. NYC Film Permits

**数据粒度和维度。** 当前保存的历史镜像有 40,754 行 × 11 列；每行是一个 permit/event。字段有 ProjectTitle、EventName、EventType、EventStartDate、EventEndDate、Location、Boro、ProjectId、CategoryName、SubCategoryName、CompanyName。约 3,326 个项目、2,246 个公司；主要类别是 Television（27,834）和 Film（12,920），Boro 以 Manhattan（20,655）和 Brooklyn（11,465）为主。缺失约 0.28%，但有 136 个完全重复行，需去重并说明规则。

**EDA 机会。** 可以分析 permit 的年份/月份/星期/时长、borough 与 category 的组合、公司集中度、项目类型变化，以及 Location 的地址文本。`EventStartDate` 覆盖 2011-07-25 到 2015-08-04，`EventEndDate` 最晚到 2016-06-30，需核对跨年/异常时长。它是真实城市管理记录，但 permit 是获批/登记，不是实际拍摄时长、预算或观众表现。

**D3 故事。** 地图（先做地址解析或使用 borough 级地图）、时间 heatmap、category→borough Sankey、项目详情 tooltip 和公司筛选都很自然。它比 Airbnb 更独特，也更贴近“真实世界系统生成数据”的课程主题。最大限制是当前文件是历史公开镜像，不是实时 NYC 全量；proposal 必须标注这个范围。

### 6. World Happiness Report 2026 Figure 2.1

**数据粒度和维度。** 官方工作簿 2,116 行 × 13 列，168 个国家名；Year 为 2011、2012、2014–2025（没有 2013），每行是国家在某年的三年平均 life evaluation。字段包括 Rank、life evaluation、上下置信界限、六个解释因子（Log GDP、social support、healthy life expectancy、freedom、generosity、corruption）和 Dystopia + residual。

**缺失结构。** 总体缺失 35.91%，但原因很明确：2011–2018 行只有排名、life evaluation 和 whisker，六个解释因子主要从 2019 年开始提供。不要用均值填补，也不要把 2011–2018 与 2019–2025 当作同一套 13 维面板。官方 FAQ 也说明 2025 ranking 基于 2022–2024 的合并数据，所以它不是单年即时情绪。

**项目判断。** 适合国家地图、排名变化、置信区间和 factor decomposition，但“GDP 导致幸福”这种因果句不能写。主题成熟、常见；若想做，应加入有明确问题的交互，例如“哪些国家在排名上升时，主要是哪一类因素贡献变化？”而不是只做世界地图。

### 7. 2018 Central Park Squirrel Census

**数据粒度和维度。** 3,023 条 squirrel sighting × 31 列；每行是一次观测。包含 X/Y 坐标、Unique Squirrel ID、Hectare、AM/PM Shift、Date、年龄、主/高光毛色、Location（Ground Plane/Above Ground）、地面高度、Running/Chasing/Climbing/Eating/Foraging、Kuks/Quaas/Moans、Tail flags/twitches、Approaches/Indifferent/Runs from 等行为指示。

**EDA 事实。** Gray 2,473、Cinnamon 392、Black 103；Adult 2,568、Juvenile 330；PM 1,676、AM 1,347；Ground Plane 2,116、Above Ground 843。缺失约 13.02%，主要是 Color notes（93.98%）、Other Interactions（92.06%）、Other Activities（85.54%）、Specific Location（84.25%），而不是坐标全部缺失。日期是字符串编码，覆盖 2018-10-06 到 2018-10-20 左右，不能包装成长期种群趋势。

**D3 故事。** Central Park 网格/散点地图 + 毛色/行为筛选 + AM/PM 联动很有记忆点，可以做“不同位置是否对应不同活动模式”。真实 citizen-science 和可视化潜力很强；报告要说明志愿者观测、努力量和短期调查造成的 sampling bias。

### 8. Hong Kong Beach Water Quality 2025

**数据粒度和维度。** 1,409 行 × 3 列：泳灘名稱、取樣日期、每 100 mL 大腸桿菌含量；43 个海滩，日期 2025-01-06 至 2025-12-29，每个海滩约 29–45 次记录。全表无缺失。E. coli 中位数 12、均值 99.3、最大 18,000；53 行超过 500，分布极度右偏，应使用 log scale 或分位数/阈值，而不是只画均值。

**项目判断。** 它是真实、香港本地、很适合做日历热图和海滩时间序列；但只有一个指标，没有雨量、潮汐、泳客、地理坐标或分级字段。单独做可以完成小而漂亮的项目，却难支撑 4–8 人的深度 report；除非 proposal 明确围绕“极端污染事件的季节/空间模式”，或再合并官方天气/地理数据并说明 join。

### 9. Steam Games Dataset V2

**三张表必须分开看。**

| 表 | 形状 | 关键字段和问题 |
|---|---:|---|
| `extended_steam_games.csv` | 23,100 × 28 | 游戏名、开发商/发行商、positive/negative、owners 区间、playtime、price/discount、CCU、release_date、平台、Metacritic、recommendations、achievements、genres/categories、description；492 个重复 appid |
| `steamspy_raw.csv` | 30,000 × 15 | SteamSpy 估计与 playtime/评价字段；1,166 个重复 appid，约 0.06% 缺失 |
| `steam_games_wikidata.csv` | 128,348 × 8 | Wikidata 名称、ESRB、HLTB/IGDB/Metacritic/OpenCritic ID、game engine；缺失约 60.68%，appid 本身唯一 |

extended 表的 appid 去重后约 22,608 个；与 Wikidata 的交集约 21,221 个。price 中位数约 499（原始单位需核实是否为 cents），free game 4,400；CCU 极度长尾，最大超过 1,000,000；genres/categories 是多标签字符串。

**项目判断。** 这是一个很好的多表清洗和 D3 题目：研究“价格、类型、平台和玩家参与度之间的关系”，做 genre 网络/矩阵、价格—CCU scatter、发行年份 timeline、平台筛选。必须说明 owners 是区间估计、CCU 是采样时点、各表收集时间可能不同；不能把相关性写成游戏设计因果。

### 10. NASA Exoplanet Archive

**数据粒度和维度。** 40,155 行 × 355 列，6,366 个 `pl_name`、4,775 个 `hostname`；每个 host 平均 8.41 颗记录，最多 103 颗，说明“每行不是独立恒星”，层级结构很重要。字段分为发现信息（method/facility/instrument/telescope/year）、轨道参数（period、semi-major axis、inclination、eccentricity）、行星尺寸/质量/温度/辐照度、恒星光谱/质量/半径/温度/距离、观测误差上下界和 `*_lim` 限制旗标、系统计数和多个观测方法旗标。

**EDA 事实。** 36,073 行是 Transit，2,952 是 Radial Velocity；主要设施是 Kepler（28,592）。可用值示例：orbital period 36,771、planet radius 27,672、planet mass 5,160、stellar temperature 36,499、distance 39,299。总体缺失 46.65%，且 56 个完全重复行；许多 `*_err*`/`*_str` 列几乎全空。`soltype` 混合 Published Confirmed、Published Candidate、Kepler/TESS Candidate，必须先限定状态。

**项目判断。** 这是最有新颖性的候选：可以做“发现方法如何塑造我们看到的行星分布”“多行星系统的层级结构”“半径—轨道周期—恒星温度的探索”。D3 适合 discovery timeline、sky coordinate map、host→planet hierarchy、带误差条的散点图。技术风险最高：不能仅凭这些列判断“宜居”，也不能把候选当已确认行星；proposal 必须预先固定字段子集和过滤规则。

### 11. Netflix TV Shows and Movies

**两张表。** `titles.csv` 是 5,850 × 15：3,744 部 MOVIE、2,106 部 SHOW，release_year 1945–2022，包含 description、age certification、runtime、genres、production countries、seasons、IMDB/TMDB score/votes/popularity。`credits.csv` 是 77,801 × 5，54,314 个 people，角色为 ACTOR 73,251、DIRECTOR 4,550，5,489 个 title ID 可连接。titles 缺失 9.31%，seasons 缺失 64%（电影没有 season 很正常），age certification 缺失 44.77%。

**项目判断。** 适合做 title↔person 二部网络、国家/genre 的小 multiples、release-year 与评分的比较；不适合声称“Netflix 用户喜欢什么”，因为没有观看量、留存和曝光数据，只有 catalog 与第三方评分快照。数据结构好用但题材非常常见，除非把研究问题限制在制作网络、跨国合作或“评分—类型—时长”的明确关系。

## 最终建议

### 首选：NYC Film Permits

这项最符合“真实数据 + 有创意的 D3 + 足够 EDA”的平衡。一个可交 proposal 的问题是：

> 2011–2015 年，纽约影视许可的类别、borough、月份和项目/公司结构如何变化？哪些 borough 承担了哪些类型的拍摄活动？

最小可行分析是：数据质量与重复处理 → permit duration/月份/borough/category 的 EDA → 地址文本拆分或 borough 级空间编码 → D3 时间 heatmap + borough 地图/条形图联动 + 项目详情。不要声称许可证等于实际拍摄或经济影响。

### 第二选择：College Majors 2026

如果小组更偏向就业、教育和 AI，这个数据的研究价值最高，但需要把 `privacy_suppressed` 当成数据机制来研究，不能把大量空值随便补上。适合做“专业—credential—债务—收入—职业增长”的可筛选 frontier chart。

### 挑战版：NASA Exoplanets

如果组里有科学背景或愿意投入较多数据字典工作，它会最有辨识度。建议只选约 12–15 个字段，限定 Published Confirmed，单独保留误差/limit flags，并把“发现偏差”作为 EDA 的一部分。不要从 355 列全部开工，也不要把“habitable”当未经定义的标签。

### 备用：Central Park Squirrel Census

这是最容易做出有趣展示的真实小数据。若希望项目规模更可控、presentation 记忆点更强，它比 Airbnb、Netflix 和 Spotify 更有特色；报告必须把短期采样和缺失的行为描述写清楚。

## Proposal 不应写成的内容

Proposal 可以写研究动机、数据来源、字段和粒度、初步 EDA、研究问题、预计图表、清洗规则、组员分工与时间表；可以提出假设，但不能把尚未验证的模式写成结论。对上面这些数据，proposal 至少应提前写清：

- 哪一行代表什么，主要分析单位是什么；
- 哪些字段会被排除，为什么；
- 缺失、隐私抑制、重复和多值字符串如何处理；
- D3 的每个交互如何帮助回答研究问题；
- 数据能支持的结论边界，以及不会声称的因果关系。
