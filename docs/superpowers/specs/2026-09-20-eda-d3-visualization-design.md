# EDA + D3 六数据集交付设计

## 目标

以数据科学硕士生视角，为 NYC Film Permits、NASA Exoplanets、College Majors 2026、Central Park Squirrel Census、Steam Games V2 和 World Happiness Report 各提供一份可复现 EDA、一份面向 D3 的聚合数据文件和一个可直接演示的独立网页。暂不编写正式 report；另提供简短汇报提纲。

## 结构

每个数据集位于 `projects/<slug>/`，包含 `eda.py`、`README.md`、`index.html` 和 `site/data.js`。`eda.py` 只读取仓库已有的原始或 processed 数据，输出 `eda_summary.json`、`eda_profile.csv` 和 D3 数据。页面使用 D3 v7 CDN，避免额外前端构建步骤。

## 分析原则

- EDA 明确记录行粒度、字段类型、缺失、重复、异常值和可解释的派生变量。
- D3 只消费 EDA 产物，不在浏览器中重新清洗原始数据。
- 每个页面至少包含一个核心叙事图、一个分组比较图和一个可交互过滤或悬停说明。
- NASA 保留候选星体与确认状态，Steam 先按 `appid` 去重并记录多来源连接，College 对隐私抑制和小样本不做伪精确推断，Happiness 标明三年平均值含义。

## 六个页面的叙事

- NYC Film Permits：城市拍摄许可的时间节奏、borough 空间分布和项目类型。
- NASA Exoplanets：发现方法和发现年份如何改变我们看到的系外行星样本，并用天球坐标展示空间分布。
- College Majors：专业/机构层面的收入、债务和 AI 相关职业暴露之间的张力。
- Squirrel Census：中央公园松鼠的空间热点、班次和行为组合。
- Steam Games：发行增长、价格/评价/并发玩家关系和类型生态。
- World Happiness：国家幸福评价的年度变化、不确定区间和解释变量构成。
