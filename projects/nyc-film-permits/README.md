# NYC Film Permits · EDA + D3

## 研究问题

纽约的拍摄许可在不同年份、borough 和事件类型之间如何分布？这份数据适合讲“城市作为影视基础设施”的故事，但记录粒度是 permit event，不是电影项目。

## EDA 流程

1. 读取 `data/raw/nyc-film-permits-historical.csv`，解析开始/结束日期。
2. 检查字段类型、缺失率、重复行和 `ProjectId` 基数。
3. 派生 `year` 与拍摄持续天数；保留负值/超长值供审计，展示时只画 0–365 天。
4. 对 borough、EventType、CategoryName 和 CompanyName 做频数聚合。
5. 运行 `python3 eda.py` 会生成 `eda_profile.csv`、`eda_summary.json` 和 `site/data.js`。

## 关键发现

- 数据是事件级记录，一个项目可对应多个许可事件，不能直接把行数当成电影数量。
- 有少量完全重复行，代码保留原始记录并在摘要中报告，避免无声删除。
- borough 缺失时显示为 `Unknown`；原表没有可信经纬度，因此页面不伪造地图点。
- 时间轴、borough 排名和事件类型堆叠比“纽约地图热力图”更符合字段实际。

## D3 页面

打开 `index.html` 可查看年度趋势、borough、事件类型和拍摄时长。选择 borough 后趋势与时长图会同步过滤。
