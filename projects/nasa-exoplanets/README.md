# NASA 系外行星 EDA 与 D3.js 研究报告

基于用户提供的 `PS_2026.10.01_06.21.14.csv`，不是工作目录中的旧快照。

## 启动网页

```sh
cd projects/nasa-exoplanets
npm start
```

浏览器打开 http://127.0.0.1:3000 。仅需 Node.js 18+，无需 npm install，D3 v7.9.0 随项目保存，展示不需要联网。端口冲突可用 `PORT=3001 npm start`。

## 重现分析与验证

```sh
python3 -m pip install -r requirements.txt
npm run analyze
npm test
```

必须运行 `build_report.py`（即 npm run analyze）以生成完整报告。基础 eda.py 只生成基础数据；不要使用旧的全项目 build_sites.py 覆盖报告。本项目自带原始 CSV 与 eda_support.py，可以单独复制提交。重新分析不需要 NASA API 或 Downloads 原文件。

## 数据与口径

- 导出文件头时间：2026-10-01 06:21:14，时区未注明。
- 原始 40,188 行 × 92 列；PS 一行是一颗行星的一套参考参数，不是唯一行星。
- 主样本：default_flag=1 且 soltype=Published Confirmed；6,298 颗唯一行星。
- 参数独立剔除非零限制标记与非正值；不插补，不自动删除 IQR 极端值。
- 质量–半径仅保留 pl_bmassprov=Mass，排除推算质量和最小质量混用。
- 全量有效点参与绘图和统计，未进行展示抽样。

## 分析结果

周期–半径 Spearman ρ=0.0847；按宿主系统 bootstrap 的 95% percentile 区间 [0.0515, 0.1178]，1000 次，固定种子 20261001。结果仅描述观测样本中的弱单调关系，不能推断因果或真实宇宙丰度。

网页包含研究问题、92 字段审计、核心字典、缺失与限制值处理、描述统计、八幅 D3 图和一张相关统计表、分组与敏感性分析、局限及官方来源。图表支持悬停、方法筛选、散点框选联动、历史截止年调整及 SVG 导出；支持打印报告。

## 文件

- index.html / site/：可离线展示的中文报告与 D3 图表。
- data/：用户原始导出，逐字节保留。
- analysis/：清洗 CSV、描述统计、缺失矩阵、相关、bootstrap、敏感性与完整 JSON。
- eda_profile.csv：所有原始字段的类型、缺失与分位数审计。
- build_report.py / eda.py / eda_support.py / report_page.py：可复现分析和页面生成代码。
- server.js：Node.js 本地静态服务；server.test.js 为 HTTP 集成测试。
- verify_report.py：独立核查附件口径、统计、分箱计数守恒和本地链接。

原始 CSV SHA-256：`3571f475942abda21c08596e632e1401042ff2962d762bc698446c8ee7027f37`。
