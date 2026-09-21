"""Render real conclusions into HTML; copy runtime assets for independent offline pages."""

from pathlib import Path
import html, json, shutil

ROOT = Path(__file__).resolve().parents[1]
slugs = [
    "nyc-film-permits",
    "nasa-exoplanets",
    "college-majors-2026",
    "central-park-squirrels",
    "steam-games-v2",
    "world-happiness",
]
e = html.escape
for slug in slugs:
    out = ROOT / "projects" / slug
    data = json.loads(
        (out / "site/data.js")
        .read_text()
        .removeprefix("const DATA = ")
        .strip()
        .removesuffix(";")
    )
    meta = data["meta"]
    s = data["summary"]
    for asset in ["site.css", "app.js", "d3.v7.min.js", "D3-LICENSE"]:
        shutil.copyfile(ROOT / "scripts/visuals" / asset, out / "site" / asset)
    findings = "".join(
        f'<article class="finding"><div class="tag">FINDING {i + 1:02d}</div><h3>{e(f["title"])}</h3><p>{e(f["text"])}</p></article>'
        for i, f in enumerate(s["findings"])
    )
    chartlinks = "".join(
        f'<a href="#chart-{i}">{e(c["title"])}</a>'
        for i, c in enumerate(data["charts"])
    )
    chartslots = "".join(
        f'<article id="chart-{i}" class="chart {"wide" if c["kind"] in ["scatter", "map", "flow", "network"] else ""}" data-kind="{c["kind"]}"><div class="charthead"><h3>{e(c["title"])}</h3><button class="export" aria-label="导出 {e(c["title"])} 为 SVG">导出 SVG</button></div><p class="note">{e(c["note"])}</p><div class="chart-body"></div></article>'
        for i, c in enumerate(data["charts"])
    )
    steps = "".join(f"<li>{e(x)}</li>" for x in data["steps"])
    limits = "".join(f"<li>{e(x)}</li>" for x in data["limitations"])
    provenance = "".join(
        f"<p>{e(p['file'])} · {p['bytes']:,} bytes<br><code>SHA-256 {p['sha256']}</code></p>"
        for p in data["provenance"]
    )
    refs = " · ".join(
        f'<a href="{e(url)}" target="_blank" rel="noreferrer">{e(label)}</a>'
        for label, url in meta.get("references", [])
    )
    intro_cards = "".join(
        [
            f'<article class="finding"><div class="tag">DATASET</div><h3>它是什么？</h3><p>{e(meta.get("description", ""))}</p></article>',
            f'<article class="finding"><div class="tag">PURPOSE</div><h3>用来研究什么？</h3><p>{e(meta.get("purpose", ""))}</p></article>',
            f'<article class="finding"><div class="tag">UNIT & SOURCE</div><h3>一行代表什么？</h3><p>{e(meta.get("unit", ""))}</p><p class="source-note">{e(meta.get("source_note", ""))}</p></article>',
            f'<article class="finding translation-card"><div class="tag">SOURCE DESCRIPTION / 中文翻译</div><h3>原始页面简介</h3><p>{e(meta.get("source_description", ""))}</p><p class="source-note">这是根据页面 Description 的中文翻译或忠实整理；它与本项目后面的统计发现分开呈现。</p><p class="source-links"><strong>原始链接（点击新页面打开）：</strong> {refs}</p></article>',
        ]
    )
    links = " · ".join(
        f'<a href="analysis/{e(p.name)}">{e(p.stem)}</a>'
        for p in sorted((out / "analysis").glob("*"))
    )
    (out / "index.html").write_text(f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><link rel="icon" href="data:,"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(meta["title"])} · EDA Research Studio</title><link rel="stylesheet" href="site/site.css"></head>
<body class="{meta["theme"]}"><header><a href="../../index.html"><strong>5002 / RESEARCH STUDIO</strong></a><nav><a href="#dataset">数据集</a><a href="#findings">研究发现</a><a href="#evidence">交互证据</a><a href="#methods">方法与限制</a></nav></header><main class="wrap"><div class="eyebrow">{e(meta["kicker"])}</div><section class="hero"><div><h1>{e(meta["title"])}</h1><p class="question">{e(meta["question"])}</p><div class="audit"><span>原始 <b>{s["rows"]:,} × {s["columns"]}</b></span><span>原始缺失 <b>{s["missing_rate"]:.2%}</b></span><span><b>{len(data["charts"])}</b> 个分析视图</span></div></div><aside><div class="eyebrow">ANALYSIS POPULATION</div><div class="count">{s["analysis_rows"]:,}</div><p>清洗或筛选后的主分析记录。各图另标完整案例数、抽样方式与统计单位。</p><p>先阅读结论，再用筛选、框选和分组检验证据。页面可以离线打开。</p></aside></section><section id="dataset"><div class="section-intro"><h2>这个数据集是什么？</h2><p>下面的简介根据数据发布页面、官方数据目录和本地文件的实际字段整理；来源链接在页面底部。</p></div><div class="findings dataset-facts">{intro_cards}</div></section><section id="findings"><div class="section-intro"><h2>从数据中得到的发现</h2><p>统计量来自全量 Python 分析；以下文字已写入 HTML。</p></div><div class="findings">{findings}</div></section><section id="evidence"><div class="section-intro"><h2>证据与交互探索</h2><p>图表提供分母、单位、样本量及分析边界。</p></div><nav class="chart-index">{chartlinks}</nav><div class="charts">{chartslots}</div></section><section class="method" id="methods"><article><h2>可复现的分析过程</h2><ol>{steps}</ol><a href="eda.py">分析代码</a> · <a href="eda_profile.csv">全部原始字段 profile</a> · <a href="README.md">分析说明</a></article><article><h2>结论的适用边界</h2><ul>{limits}</ul></article></section><section class="sources"><h3>数据与可审计结果</h3><p>{refs}</p><p>{links}</p>{provenance}<p>固定随机种子 {data["seed"]}。没有对原始数据文件作覆盖修改。</p></section><footer>CITYU 5002 / EDA + D3 / EXPLORATORY ANALYSIS, NOT CAUSAL IDENTIFICATION</footer></main><div class="tooltip" role="status"></div><script src="site/d3.v7.min.js"></script><script src="site/data.js"></script><script src="site/app.js"></script></body></html>''')
    print("built", slug)
# Lightweight launch page with relative links supports file:// and a local server.
cards = "".join(
    f'<article class="finding"><h2><a href="projects/{s}/index.html">{json.loads((ROOT / "projects" / s / "eda_summary.json").read_text())["dataset"]}</a></h2><p>研究发现 · 联动探索 · 方法与数据审计</p></article>'
    for s in slugs
)
(ROOT / "index.html").write_text(
    f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><link rel="icon" href="data:,"><meta name="viewport" content="width=device-width,initial-scale=1"><title>5002 Research Studio</title><link rel="stylesheet" href="projects/nyc-film-permits/site/site.css"><main class="wrap"><div class="eyebrow">CITYU 5002 / SIX RESEARCH QUESTIONS</div><h1>EDA Research Studio</h1><p>六个独立数据集，从研究问题、数据口径到交互证据和结论。选择一个项目开始。</p><div class="findings">{cards}</div></main></html>'
)
