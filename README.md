# CityU 5002 · EDA Research Studio

六个独立项目的第二版：先确认统计单位和数据质量，再分析变量关系，最后用交互图检验解释。结论直接写入每个 HTML。

**打开 [index.html](index.html)** 进入六项目导航。每个项目的 `index.html` 也可直接打开；D3 7.9.0 和数据都已放到项目自己的 `site/`，支持离线演示。

候选数据集的来源核对、数据用途和观测单位见 [`data/dataset_comparison_zh.md`](data/dataset_comparison_zh.md)；六个项目页面的“这个数据集是什么？”区域也保留了对应发布页面链接。

| 项目目录 | 核心研究问题 | 视图 |
|---|---|---:|
| `projects/nyc-film-permits` | 类型与行政区关联，是否受高频项目重复出现影响？ | 8 |
| `projects/nasa-exoplanets` | 发现方法与测量覆盖如何塑造物理关系？ | 6 |
| `projects/college-majors-2026` | 收入–债务总体关系能否在学位和专业层级内成立？ | 6 |
| `projects/central-park-squirrels` | AM/PM 行为差异能否在共同地块内成立？ | 6 |
| `projects/steam-games-v2` | 价格、评价、快照 CCU 与多类型结构如何关联？ | 6 |
| `projects/world-happiness` | 排名不确定性、固定国家趋势与分解贡献如何解释？ | 7 |

## 复现

Python 3.10+，依赖见 `requirements.txt`：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/run_all_eda.py
python3 scripts/verify_projects.py
```

`run_all_eda.py` 会依次运行六个管线并生成页面。也可单独重跑：

```bash
python3 projects/nasa-exoplanets/eda.py
python3 scripts/build_sites.py
```

可选 HTTP 预览：

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

访问 `http://127.0.0.1:8765/`。无需 npm 构建。

## 交付结构

每个项目包含：

- `eda.py`：该数据集的清洗、关系分析、验证和发现生成。
- `README.md`：研究问题、实际计算的结论、方法和限制。
- `eda_profile.csv`：所有**原始字段**的类型、缺失、基数、分位数。
- `eda_summary.json`：原始规模、分析规模、结论和关键断言。
- `analysis/`：全量汇总、敏感性分析、统计表等可审计结果。
- `index.html`：静态写入结论，图表通过本地 D3 交互渲染。
- `site/`：该页面自己的 D3、样式、代码和数据，可连同 HTML 单独复制演示。

Python 管线共用 `scripts/eda_support.py` 中的数学和导出函数，原始数据统一保留在 `data/`，不重复复制大文件。六个页面运行时互不依赖。

## 验证

`scripts/verify_projects.py` 独立核对原始行数、NASA 默认确认行星口径、College 完整案例、Steam 美分转换、松鼠重复 ID、幸福报告平衡面板、source hash 及 HTML 结论。

`scripts/browser_verify.js` 是 Playwright CLI 的浏览器检查函数，检查六页的筛选/框选、时间滑块、空搜索、SVG 导出和手机宽度布局。在启动本地服务器及 Playwright 会话后：

```bash
playwright-cli -s=eda-review run-code --filename=scripts/browser_verify.js
```

检查截图位于 `output/playwright/`（本地保留，不纳入版本控制）。简单汇报见 [presentation_outline.md](presentation_outline.md)。
