"""Create a Chinese version of the generated dataset profiling note.

Column names, categorical values, source names, file paths, and numeric values
remain unchanged so the note stays traceable to the downloaded data and code.
"""
from pathlib import Path
import re
import shutil


SRC = Path('/Users/leon.w/workspace/mine/all-for-ML/Cityu/5002/dataset_profiles.md')
DST = SRC.with_name('dataset_profiles_zh.md')

HEADINGS = {
    '## College Majors 2026: earnings, debt, jobs and AI': '## College Majors 2026：收入、债务、就业与 AI',
    '## Spotify tracks and audio features (50k)': '## Spotify 曲目与音频特征（5 万条）',
    '## New York City Airbnb Open Data': '## 纽约市 Airbnb 开放数据',
    '## Student exam performance and success': '## 学生考试表现与学业成功',
    '## NYC film permits (historical public mirror)': '## 纽约市影视拍摄许可证（历史公开镜像）',
    '## World Happiness Report 2026, Figure 2.1 data': '## 《世界幸福报告》2026：图 2.1 数据',
    '## 2018 Central Park Squirrel Census': '## 2018 年中央公园松鼠普查',
    '## Hong Kong beach water quality (2025)': '## 香港泳滩水质（2025）',
    '## Steam Games Dataset V2': '## Steam 游戏数据集 V2',
    '## Steam Games Dataset V2 — Wikidata enrichment table': '## Steam 游戏数据集 V2——Wikidata 补充表',
    '## Steam Games Dataset V2 — SteamSpy raw table': '## Steam 游戏数据集 V2——SteamSpy 原始表',
    '## NASA Exoplanet Archive Planetary Systems table': '## NASA 系外行星档案馆：行星系统表',
    '## Netflix TV Shows and Movies (titles + credits)': '## Netflix 影视节目（标题 + 演职员）',
    '## Netflix TV Shows and Movies — credits table': '## Netflix 影视节目——演职员表',
}


def translate_table_row(line: str) -> str:
    if not line.startswith('|'):
        return line
    line = line.replace('| Column | Type | Non-null / unique or range |', '| 字段 | 类型 | 非空数 / 唯一值数或范围 |')
    line = line.replace('| Column | Missing | Missing % |', '| 字段 | 缺失数量 | 缺失比例 |')
    line = line.replace('`object`', '`object`（文本）')
    line = line.replace('`float64`', '`float64`（浮点数）')
    line = line.replace('`int64`', '`int64`（整数）')
    line = line.replace('`bool`', '`bool`（布尔值）')
    line = line.replace(' non-null;', ' 个非空值；')
    line = line.replace(' unique incl. NA;', ' 个唯一值（含 NA）；')
    line = line.replace(' unique incl. NA |', ' 个唯一值（含 NA） |')
    line = line.replace(' unique;', ' 个唯一值；')
    line = line.replace(' unique |', ' 个唯一值 |')
    line = line.replace('min ', '最小值 ')
    line = line.replace('median ', '中位数 ')
    line = line.replace('max ', '最大值 ')
    line = line.replace('top: ', '常见值：')
    line = line.replace('; ', '；')
    return line


def translate_line(line: str) -> str:
    stripped = line.rstrip('\n')
    if stripped in HEADINGS:
        return HEADINGS[stripped]
    if stripped == '# Dataset profiling for CityU 5002 group project':
        return '# CityU 5002 小组项目数据集概况'
    if stripped.startswith('Generated from the downloaded files'):
        return '本报告根据已下载到 `data/raw/` 和 `data/processed/` 的文件生成。原始文件保持不变。'
    if stripped == '### Schema':
        return '### 字段结构'
    if stripped == '### Missingness hotspots':
        return '### 缺失值重点'
    if stripped == '### Date/time candidates':
        return '### 日期/时间候选字段'
    if stripped.startswith('- Source:'):
        return stripped.replace('- Source:', '- 来源：', 1)
    if stripped.startswith('- Local file:'):
        return stripped.replace('- Local file:', '- 本地文件：', 1)
    if stripped.startswith('- Shape:'):
        value = stripped.replace('- Shape:', '- 数据形状：', 1)
        value = re.sub(r'\brows\b', '行', value)
        value = re.sub(r'\bcolumns\b', '列', value)
        return value
    if stripped.startswith('- Size:'):
        value = stripped.replace('- Size:', '- 文件大小：', 1)
        value = value.replace('duplicate rows:', '重复行：').replace('missing cells:', '缺失单元格：')
        return value
    if stripped.startswith('- `') and ' valid;' in stripped:
        value = stripped.replace(' valid;', ' 个有效值；').replace(' to ', ' 至 ')
        value = value.replace('(year)', '（年份）').replace('(datetime)', '（日期时间）')
        return value
    if stripped.startswith('|'):
        return translate_table_row(stripped)
    return stripped


def main() -> None:
    original = SRC.read_text(encoding='utf-8')
    translated = [
        '> 中文说明：字段名、类别取值、来源名称、文件路径和数值保留原文，便于与代码和原始数据核对；标题、说明文字、表头和统计标签已翻译成中文。',
        '',
    ]
    translated.extend(translate_line(line) for line in original.splitlines())
    DST.write_text('\n'.join(translated) + '\n', encoding='utf-8')
    print(f'wrote {DST} ({DST.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
