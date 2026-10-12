# NYC Film Permits EDA

本目录按原有中文提示词完成分析，仅使用 `data/Film_Permits_20260930.csv`。实际目录名是 `file-permit-v3`，未使用其他项目目录的数据或结果。

## 查看成果

- `NYC_Film_Permits_EDA.ipynb`：主要成果，含中文说明、Python 代码、真实执行输出及 10 张英文图表。
- `output/film_permits_clean.csv`：清洗数据（19,412 行），包含分析特征和异常标记。
- `output/figures/`：10 张适合课堂展示的 PNG。
- `output/findings_zh.md`：5 条核心发现及数据限制。
- `output/tables/`：原始字段概况、清洗影响记录、各项统计分母、时间覆盖及交叉分析表。
- `output/quarantined_rows.csv`：8 条多字段错位记录，保留原样以供核查。
- `output/date_anomalies_original.csv`：日期异常记录的原始字段。
- `output/execution_report.json`：执行方式、单元格数和验证限制。

## 安装与运行

在本文件所在文件夹打开终端：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter notebook NYC_Film_Permits_EDA.ipynb
```

在 Notebook 中选择 Python 3，然后运行全部单元格。运行目录应为本目录，代码全部使用相对路径，不联网获取数据。原始 CSV 不会被修改。中间表、清洗数据和 PNG 会按相同路径重新生成。

当前交付已使用 Python 3.10、pandas、matplotlib、seaborn 和 IPython 顺序执行全部 15 个代码单元，保存真实表格、图像和解释输出，分析自检通过。**当前环境缺少 Jupyter 内核组件，下载时网络/TLS 连接失败，未验证独立 Jupyter 内核的 Run All**。可在安装依赖后按上方步骤验证。

`build_notebook.py` 是本次交付的生成/执行脚本；需要用当前 IPython 执行方式重建 Notebook 时，在本目录运行 `python build_notebook.py`。正常学习和修改分析只需打开 Notebook，不需要研究该脚本。

## 主要发现

2025 年记录数较 2024 年下降 12.5%，但 2026 年上半年较 2025 年同期增加 7.0%。Television 占 41.0%；Manhattan 和 Brooklyn 的首个行政区记录合计占 83.7%；有效计划跨度中位数为 15 小时。具体统计分母、解释和限制见 Notebook。

## 口径与清洗

每行是一条许可证，不能当成一部作品。无整行或 EventID 重复。8 条字段错位记录隔离，未猜测修复；17 条负跨度仅在跨度分析中排除，原始日期保留；1 条公元 1 年的非空录入时间解析为缺失。保留其他缺失记录与长跨度；3 条录入晚于开始的记录保留并标记。清洗影响数量见审计表。

完整年度比较使用 2023–2025 年；2026 年单列上半年同窗比较。月度图排除仅含 1 条的 2026 年 7 月。地理图使用首个行政区，多值社区、警区和邮编未拆分计为独立许可。每张图下均说明口径及不能推断的事项。

## 官方来源

[NYC Open Data：Film Permits 数据介绍与字段说明](https://data.cityofnewyork.us/City-Government/Film-Permits/tg4x-b46p)，2026-10-12 查阅。官网是动态数据，本地 CSV 为固定快照；所有统计基于本地文件。时间范围按实际日期字段计算，不能由文件名中的日期推断。
