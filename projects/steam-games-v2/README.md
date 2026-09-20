# Steam Games V2 · EDA + D3

## 研究问题

Steam 游戏市场的发行速度、价格、评价和并发玩家之间有什么可视化关系？这个项目重点展示多表清洗本身：同一个 `appid` 来自主表、Wikidata 和 SteamSpy，不能直接拼接后假定一一对应。

## EDA 流程

1. 读取三个 processed CSV，分别统计重复 appid。
2. 每张表按 appid 去重后，以主表为中心做 left join，报告匹配率。
3. 解析 release date 年份，计算正面评价比例 `positive/(positive+negative)`。
4. 拆分 genres，聚合发行年份、类型和价格/评价/CCU 散点。

## 关键限制

- SteamSpy 与主表的采集时间/口径可能不同，join 结果是描述性匹配。
- 评价数和 CCU 都受热门游戏长尾分布影响，页面使用 log 轴。
- 日期无法解析的游戏不进入年度趋势，但仍保留在主表 profile 中。
