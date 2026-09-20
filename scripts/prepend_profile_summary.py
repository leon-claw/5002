"""Prepend a data-quality overview table to the Obsidian profiling note."""
from pathlib import Path
import json
import shutil


BASE = Path('/Users/leon.w/workspace/mine/all-for-ML/Cityu/5002')
ACTIVE = BASE / 'dataset_profiles.md'
ZH_COPY = BASE / 'dataset_profiles_zh.md'
PROFILE_JSON = Path('/Users/leon.w/Documents/ChatGPT/5002/data/metadata/dataset_profiles.json')


def mb(value: int) -> str:
    return f'{value / 1024 / 1024:.2f} MB'


def make_summary() -> str:
    profiles = {x['id']: x for x in json.loads(PROFILE_JSON.read_text(encoding='utf-8'))}

    def size(*ids: str) -> str:
        return mb(sum(profiles[i]['file_size_bytes'] for i in ids))

    rows = [
        ('College Majors 2026', '227,980 × 72', '53 数值 / 19 类别', size('college_majors'), '27.79%', '0', '学校、专业、学位、收入、债务、职业和 AI 指标；收入/债务字段有大量 privacy suppression'),
        ('Spotify 50k', '50,000 × 21', '15 数值 / 6 类别', size('spotify'), '0.00%', '0', '无缺失且无重复；README 明确说明是合成数据，popularity 最小值为 -5，需核验定义'),
        ('NYC Airbnb 2019', '48,895 × 16', '10 数值 / 6 类别', size('airbnb_nyc'), '2.58%', '0', 'last_review/reviews_per_month 缺失 20.56%；price=0 和 minimum_nights=1,250 等异常值'),
        ('Student Exam Performance', '100,000 × 44', '22 数值 / 22 类别', size('student_exam'), '1.19%', '0', '总体缺失低，但部分变量缺失 6%–10%；半合成数据，目标字段可能造成 target leakage'),
        ('NYC Film Permits', '40,754 × 11', '1 数值 / 10 类别', size('nyc_film_permits'), '0.28%', '136', '2011–2015 历史镜像；真实城市记录，但 Location 是文本，且存在重复 permit 行'),
        ('World Happiness Report', '2,116 × 13', '12 数值 / 1 类别', size('world_happiness'), '35.91%', '0', '2011–2025；2011–2018 的解释因子大多为空，是数据设计造成的结构性缺失'),
        ('Central Park Squirrel Census', '3,023 × 31', '4 数值 / 27 类别', size('squirrel'), '13.02%', '0', '2018 短期 citizen-science 普查；Color notes、Other Activities 等叙述字段缺失超过 80%'),
        ('Hong Kong Beach Water Quality', '1,409 × 3', '1 数值 / 2 类别', size('hk_beach'), '0.00%', '0', '2025 年 43 个海滩；数据完整但只有一个水质指标，E. coli 最大值 18,000，分布极度右偏'),
        ('Steam Games V2', '23,100 × 28；附表 128,348 × 8、30,000 × 15', '15 数值 / 13 类别（主表）', size('steam', 'steam_wikidata_table', 'steamspy_table'), '3.16%（主表）', '489（主表）；SteamSpy 1,166', '三张来源不同的表；appid 需去重和合并，owners/CCU 是估计或时点指标'),
        ('NASA Exoplanets', '40,155 × 355', '265 数值 / 90 类别', size('nasa_exoplanets'), '46.65%', '56', '官方科学数据；字段极多，许多误差列近乎全空，候选与已确认行星状态混合'),
        ('Netflix Titles + Credits', '5,850 × 15；credits 77,801 × 5', '7 数值 / 8 类别（titles）', size('netflix', 'netflix_credits'), '9.31%（titles）；2.51%（credits）', '0', 'catalog 快照；titles 的 seasons 缺失 64% 是电影的结构性缺失，缺少观看量和留存数据'),
    ]

    lines = [
        '## 所有候选数据集基础质量总览',
        '',
        '这张表用于快速比较数据结构和质量，不是项目优先级评分。文件大小按本地解压后的 CSV/XLSX 合计；Steam 和 Netflix 的附属表单独列出。特征类型按 profiling 时的 pandas 类型统计，字段名和类别值仍保留英文以便对应代码。',
        '',
        '| 数据集 | 主表行数 × 特征数 | 特征类型分布 | 本地文件大小（合计） | 主表缺失单元格率 | 重复行 | 时间/空间与质量提示 |',
        '|---|---:|---|---:|---:|---:|---|',
    ]
    for name, shape, types, total_size, missing, duplicates, note in rows:
        lines.append(f'| {name} | {shape} | {types} | {total_size} | {missing} | {duplicates} | {note} |')
    lines += [
        '',
        '**快速判断：** 最干净的是 Spotify 和香港泳滩数据，但前者是合成数据、后者维度较少；维度最丰富的是 NASA 和 College Majors，但缺失和数据解释风险也最高；真实数据与可视化平衡最好的是 NYC Film Permits 和 Central Park Squirrel Census。',
        '',
        '### 辅助判断指标：结构与缺失风险',
        '',
        '“高缺失字段”表示该字段缺失率超过 20% 或 50%；“近常量字段”表示某个值占该字段至少 99%。近常量字段可能是合法的标志变量，但会降低区分度。',
        '',
        '| 数据集 | 每行代表 | 缺失率 >20% 的字段数 | 缺失率 >50% 的字段数 | 全空字段 | 常量字段 | 近常量字段 | 唯一 ID / 关键键 |',
        '|---|---|---:|---:|---:|---:|---:|---|',
        '| College Majors 2026 | 学校 × 专业 × credential 项目 | 27 | 22 | 0 | 0 | 0 | `program_id`（100% 唯一） |',
        '| Spotify 50k | 一首曲目 | 0 | 0 | 0 | 0 | 0 | `track_id`（100% 唯一） |',
        '| NYC Airbnb 2019 | 一个 listing | 2 | 0 | 0 | 0 | 0 | `id`（100% 唯一） |',
        '| Student Exam Performance | 一名学生 | 0 | 0 | 0 | 0 | 0 | `student_id`（100% 唯一） |',
        '| NYC Film Permits | 一个 permit/event | 0 | 0 | 0 | 0 | 0 | 无单列唯一 ID；`ProjectId` 可作为项目键 |',
        '| World Happiness Report | 国家 × 年份 | 9 | 9 | 0 | 0 | 0 | `Country name` + `Year` 组合键 |',
        '| Central Park Squirrel Census | 一次松鼠观测 | 5 | 4 | 0 | 0 | 1 | `Unique Squirrel ID`（100% 唯一） |',
        '| Hong Kong Beach Water Quality | 海滩 × 取样日期 | 0 | 0 | 0 | 0 | 0 | `泳灘名稱` + 日期组合键 |',
        '| Steam Games V2 | 一款游戏（主表） | 1 | 1 | 0 | 4 | 5 | `appid`（主表约 98% 唯一） |',
        '| NASA Exoplanets | 一条行星记录/观测记录 | 222 | 165 | 2 | 10 | 40 | 无单列唯一 ID；`pl_name`/`hostname` 是层级键 |',
        '| Netflix Titles + Credits | 一个标题；credits 是标题—人物关系 | 2（titles） | 1（titles） | 0 | 0 | 0 | `titles.id`（100% 唯一）；`credits.id` 为关联键 |',
        '',
        '### 辅助判断指标：时间、空间与关联结构',
        '',
        '| 数据集 | 时间字段/跨度 | 空间字段 | 关联结构 | D3 可视化信号 |',
        '|---|---|---|---|---|',
        '| College Majors 2026 | 没有连续时间序列；`awards_year1/2` 是授予数量 | 学校经纬度、州、区域 | institution → CIP 专业 → credential | 美国地图、收入/债务散点、平行坐标 |',
        '| Spotify 50k | `release_year`：2000–2024 | 无真实地理字段 | 单表；artist/album 可分组 | 音频特征散点、genre 分布、雷达图 |',
        '| NYC Airbnb 2019 | `last_review`：快照中的评论日期 | latitude/longitude、borough、neighbourhood | host → listing | 地图、房型筛选、价格分布 |',
        '| Student Exam Performance | 无日期字段 | 无地理字段 | 学生级单表 | 平行坐标、条件分布、相关热图 |',
        '| NYC Film Permits | `EventStartDate`/`EventEndDate`：2011–2016 | Boro、Location 文本 | ProjectId、CompanyName、permit event | 时间热图、borough 地图、项目/公司网络 |',
        '| World Happiness Report | `Year`：2011–2025 | Country name，可连接世界地图 | country-year 面板 | 排名动画、世界地图、置信区间 |',
        '| Central Park Squirrel Census | `Date`：2018-10-06 至 2018-10-20 左右 | X/Y、Hectare、Lat/Long | 单次观测；行为字段 | 网格地图、AM/PM 联动、行为筛选 |',
        '| Hong Kong Beach Water Quality | 取样日期：2025 年 | 只有海滩名称，文件没有坐标 | beach-date 面板 | 日历热图、海滩时间序列 |',
        '| Steam Games V2 | `release_date`：约 2004–2026 | 无地理字段 | `appid` 连接 extended/SteamSpy/Wikidata | 价格—CCU 散点、genre 网络、发行时间线 |',
        '| NASA Exoplanets | `disc_year`：1992–2026 | RA/DEC、银河坐标 | `hostname` → 多颗行星层级 | 天空图、系统层级、带误差散点 |',
        '| Netflix Titles + Credits | `release_year`：1945–2022 | production countries（无坐标） | `titles.id` ↔ `credits.id` | 标题—人物二部图、国家/类型时间线 |',
        '',
    ]
    return '\n'.join(lines) + '\n'


def update(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    title = '# CityU 5002 小组项目数据集概况'
    if title not in text:
        raise RuntimeError(f'original title not found in {path}')
    suffix = text.split(title, 1)[1]
    note = '> 中文说明：字段名、类别取值、来源名称、文件路径和数值保留原文，便于与代码和原始数据核对；标题、说明文字、表头和统计标签已翻译成中文。\n\n'
    path.write_text(note + make_summary() + title + suffix, encoding='utf-8')


def main() -> None:
    update(ACTIVE)
    if ZH_COPY.exists():
        shutil.copy2(ACTIVE, ZH_COPY)
    print('updated data-quality summary in', ACTIVE)


if __name__ == '__main__':
    main()
