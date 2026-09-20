# CityU 5002 · EDA + D3 数据可视化

当前分支：`codex/eda-d3-visualization`

本仓库包含六个独立的数据科学硕士课程项目。每个目录都有自己的 EDA 脚本、清洗决策、统计输出和 D3 页面：

| 项目 | 叙事重点 |
|---|---|
| `projects/nyc-film-permits` | 城市拍摄许可的时间、borough 与项目类型 |
| `projects/nasa-exoplanets` | 系外行星发现方法、时间与天球位置 |
| `projects/college-majors-2026` | 收入、债务、就业和 AI 暴露 |
| `projects/central-park-squirrels` | 松鼠空间热点、班次和行为 |
| `projects/steam-games-v2` | 游戏发行、价格、评价、并发玩家和类型 |
| `projects/world-happiness` | 幸福评价的年度变化和解释变量 |

## 运行

```bash
python3 scripts/run_all_eda.py
python3 scripts/verify_projects.py
```

每个项目也可以单独运行：

```bash
cd projects/nyc-film-permits
python3 eda.py
python3 -m http.server 8000
```

然后打开 `http://localhost:8000`。页面使用 D3 v7 CDN，不需要 npm 构建。

## 交付物

- `eda.py`：从仓库数据重新计算统计和 D3 数据。
- `eda_profile.csv`：字段级缺失率、类型和基数。
- `eda_summary.json`：可引用的关键 EDA 结果。
- `site/data.js`：浏览器直接可加载的聚合数据。
- `index.html`：交互式 D3 展示。
- `README.md`：EDA 过程、清洗决定、限制和汇报要点。
