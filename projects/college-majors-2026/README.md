# College Majors 2026 · EDA + D3

## 研究问题

如果把专业、债务、收入和 AI 相关职业暴露放在一起，哪些专业家庭呈现出不同的“回报—风险”组合？页面用描述性比较讲现实意义，同时把隐私抑制和 cohort size 当作分析边界。

## EDA 流程

1. 读取 `college_majors_2026.csv`，生成字段类型、缺失率和基数 profile。
2. 将行粒度定义为 institution × CIP program × credential。
3. 按 CIP family、州、earnings trajectory 和 AI occupation share 聚合。
4. 只对至少 25 个 program 的 family、至少 20 个 program 的州做排名，避免极小样本主导图表。
5. 运行 `python3 eda.py` 生成聚合数据和页面数据。

## 关键限制

- 数据有隐私抑制、共享 campus 结果和小 cohort；数值不能当成个人收入预测。
- `ai_software_occupation_share` 是关联职业的暴露指标，不是岗位实际使用 AI 的调查比例。
- 页面重点是探索关系和提出后续问题，而不是声称因果。
