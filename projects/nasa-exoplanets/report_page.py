"""HTML report: all narrative statistics come from the reproducible payload."""
from html import escape as esc
import pandas as pd

def render_report(p):
    r = p['report']; a = r['audit']; b = r['bootstrap']; ds = r['descriptive']
    f = lambda v: f'{v:,.0f}' if abs(v) >= 1000 else f'{v:,.3g}'
    e = lambda v: esc(str(v))
    def table(headers, rows, caption):
        return '<div class="report-table"><table><caption>'+e(caption)+'</caption><thead><tr>'+''.join('<th scope="col">'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
    def chart(i, interpretation, question):
        c = p['charts'][i]
        figure = {6:1,4:2,7:3,3:4,1:5,0:6,2:7,5:8,8:9}[i]
        return f'''<article id="chart-{i}" class="chart wide" data-kind="{c['kind']}"><div class="charthead"><div><div class="eyebrow">FIGURE {figure:02d} / {e(question)}</div><h3>{e(c['title'])}</h3></div><button class="export" aria-label="导出{e(c['title'])}为SVG">导出 SVG</button></div><p class="note">{e(c['note'])}</p><div class="chart-body"></div><p class="interpretation"><strong>如何解读</strong> {interpretation}</p></article>'''
    def heading(n, title, text):
        return f'<div class="section-intro"><div><div class="eyebrow">{n} / RESEARCH NOTE</div><h2>{title}</h2></div><p>{text}</p></div>'
    methods = r['methods']; corr = p['charts'][2]['data']
    by_method = {m['label']: m for m in methods}
    within = {m['label']: m for m in corr}
    radius = next(s for s in ds if s['field']=='pl_rade')
    period = next(s for s in ds if s['field']=='pl_orbper')
    rv = next(x for x in p['charts'][3]['data'] if x['label']=='Radial Velocity')
    tr = next(x for x in p['charts'][3]['data'] if x['label']=='Transit')
    annual = pd.DataFrame(p['charts'][4]['data']).groupby('x').value.sum()
    peak_year = int(annual.loc[annual.index < a['year_max']].idxmax())
    matrix = {(x['y'], x['x']): x for x in r['correlation_matrix']}
    pr = matrix['周期','半长轴']
    sensitivity = r['sensitivity']
    sensitivity_table = table(['分析口径','完整案例 n','Spearman ρ'], [(s['label'],f"{s['n']:,}",f"{s['rho']:.4f}") for s in sensitivity], '周期–半径关系的敏感性分析；仅改变分析口径，不覆盖主结果')
    quality_table = table(['字段 / 单位','有效 n','原本缺失','有值的限制值','非正值剔除','处理后不可用'], [(s['label'], f"{s['n']:,}",f"{s['raw_missing']:,}",f"{s['limit_values']:,}",s['nonpositive'],f"{s['missing']:,} ({s['missing_pct']:.1f}%)") for s in ds], f'主样本 n={a["planets"]:,}；每个参数独立清洗，其他字段的有效值仍保留')
    stats_table = table(['字段 / 单位','均值','中位数','Q1–Q3','P10–P90','最小–最大','1.5 IQR 外 n'], [(s['label'],f(s['mean']),f(s['median']),f(s['q1'])+' – '+f(s['q3']),f(s['p10'])+' – '+f(s['p90']),f(s['minimum'])+' – '+f(s['maximum']),f"{s['iqr_outliers']:,}") for s in ds], '描述统计基于各参数的有效值；完整精度、标准差与 n 见下载 CSV')
    dictionary = table(['字段','含义与单位','分析角色'],[
        ('pl_name / hostname','行星名 / 宿主恒星名','唯一行星校验 / 系统依赖检查'),
        ('default_flag / soltype','默认参数集标记 / 参数解状态','主样本须为 1 / Published Confirmed'),
        ('discoverymethod / disc_year','发现方法 / 发现年','分组变量 / 发现历史'),
        ('pl_orbper / pl_rade','轨道周期（天）/ 半径（地球半径）','主要双变量分析'),
        ('pl_bmasse / pl_bmassprov','最佳质量（地球质量）/ 质量来源','质量–半径图仅用 Mass 来源'),
        ('pl_eqt / st_teff','平衡温度 / 恒星有效温度（K）','物理参数的关联与缺失'),
        ('pl_orbsmax / sy_dist','半长轴（AU）/ 系统距离（pc）','轨道尺度与观测距离'),
        ('*lim / pl_controv_flag','上/下限标记 / 争议标记','排除限制值 / 敏感性分析'),
    ], f"核心数据字典；{a['raw_columns']} 个原始字段的审计可在页面底部下载")
    flow = ''.join(f'<div class="flow-step"><span>{label}</span><b>{count:,}</b><small>{detail}</small></div>' for label,count,detail in [
        ('原始参数行',a['raw_rows'],'同一行星可以有多个解'),
        ('默认参数集',a['default_rows'],'default_flag = 1'),
        ('默认已确认行星',a['planets'],'再取 Published Confirmed'),
    ])
    html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="基于 NASA Planetary Systems 固定快照的可复现探索性数据分析及 D3.js 交互图表"><link rel="icon" href="data:,"><title>NASA 系外行星 · EDA 研究报告</title><link rel="stylesheet" href="site/site.css"><link rel="stylesheet" href="site/report.css"></head>
<body class="space"><a class="skip" href="#content">跳到正文</a><header><a class="brand" href="#top"><span class="brand-mark">✳</span><strong>EXOPLANET / FIELD NOTES</strong></a><nav aria-label="报告导航"><a href="#dataset">研究设计</a><a href="#quality">质量审计</a><a href="#discovery">发现历史</a><a href="#relationships">物理关系</a><a href="#reproduce">复现与下载</a></nav><button id="print-report">打印报告</button></header>
<main class="wrap" id="content"><section class="hero" id="top"><div><div class="eyebrow">NASA EXOPLANET ARCHIVE / EDA + D3.JS</div><h1>我们发现的是行星，<br>还是观测方法的偏好？</h1><p class="question">从 {a['planets']:,} 颗已确认系外行星出发，探索发现方法、测量缺失与物理参数之间的关系。</p><p class="hero-sub">数据科学课程研究报告 · Planetary Systems（PS）<br>本地固定快照，最新记录更新至 {a['max_rowupdate']}；报告编制于 2026-10-01。</p><a class="primary-link" href="#discovery">进入交互分析 <span>↓</span></a></div><aside><div class="eyebrow">THE OBSERVED UNIVERSE</div><div class="count">{a['planets']:,}</div><p>唯一已确认行星 · {a['hosts']:,} 个宿主恒星系统</p><div class="hero-metrics"><div><b>{a['raw_rows']:,}</b><span>原始文献参数行</span></div><div><b>{by_method['Transit']['share']:.1f}%</b><span>凌日法发现占比</span></div><div><b>{radius['missing_pct']:.1f}%</b><span>半径不可用比例</span></div></div><p class="small">这里观察到的，是探测与测量筛选后的样本。它不是宇宙中行星的随机抽样。</p></aside></section>
<section class="abstract"><div class="eyebrow">ABSTRACT / 研究摘要</div><p>本研究以 NASA PS 表的默认已确认参数集为分析对象，先辨别文献行与行星的统计单位，再审计缺失、重复、限制值和长尾分布。凌日法占主样本的 {by_method['Transit']['share']:.1f}%，在周期–半径完整案例中进一步升至 {a['complete_case_transit_pct']:.1f}%。该关系的总体 Spearman ρ 为 {b['rho']:.3f}（n={p['charts'][0]['population']:,}），表明观察样本内仅存在弱的单调关联。发现方法与测量覆盖的不同，使总体关系无法直接推广到全部系外行星。报告以八幅 D3 图表和一张交互区中的统计表呈现证据，并提供代码、清洗后的数据和统计结果以复现。</p></section>
<section id="dataset">{heading('01','研究设计：先确定问题与统计单位','目标是解释样本如何形成，再讨论物理关系。')}
<div class="research-questions"><article><span>Q1</span><h3>哪些行星进入了样本？</h3><p>比较发现方法与历史，识别样本构成的变化。</p></article><article><span>Q2</span><h3>哪些参数被测量了？</h3><p>检验方法之间的缺失差异，以及完整案例的构成。</p></article><article><span>Q3</span><h3>哪些关系值得解释？</h3><p>比较总体和方法内相关，检查质量来源与结论稳健性。</p></article></div>
<div class="prose"><p>数据来自 <a href="https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&amp;config=PS" target="_blank" rel="noreferrer">NASA Exoplanet Archive 的 Planetary Systems 原始表</a>。按照<a href="https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html" target="_blank" rel="noreferrer">官方字段说明</a>，PS 的每行是一个行星对应一套文献参数解；同一行星可以重复出现。另一张 PSCompPars 表追求更完整的单行星参数，但可能混合不同参考来源。本研究保留你选择的 PS 表，使用默认参数集，并不跨文献补全缺失值。</p><p><strong>观测单位：</strong>主分析每行代表一颗唯一行星；同一恒星可对应多颗行星。<strong>分析目标：</strong>描述这份观测样本，而不是估计真实行星发生率、建立因果模型或判断宜居性。<strong>数据范围：</strong>本地 CSV 的 {a['raw_columns']} 列全部审计，选取七个正值物理参数作重点探索。</p></div>{dictionary}</section>
<section id="quality">{heading('02','数据质量：从参数解到分析样本','每一步都报告分母；不把缺失值填成零。')}
<div class="sample-flow" aria-label="样本筛选过程">{flow}</div><p class="flow-detail">默认参数集中有 {a['nonconfirmed_default_rows']} 行不是 Published Confirmed；筛选后 <code>pl_name</code> 唯一，主样本的完全重复行数为 {a['confirmed_exact_duplicates']}。周期–半径分析再要求两个字段有效，得到 {p['charts'][0]['population']:,} 颗；质量–半径分析另要求 Mass 来源及两个字段有效，得到 {a['mass_radius_n']:,} 颗。这是两个不同的分析子样本。</p>
<div class="quality-notes"><article><h3>重复 ≠ 全部应删除</h3><p>原表存在 {a['exact_duplicate_rows']} 个完全重复行；大量同名行则是不同参数解，不能直接按名称随意保留第一行。主样本使用官方默认标记和解状态，不需要任意去重。</p></article><article><h3>参数的可用性单独判断</h3><p>各参数的非零 <code>*lim</code> 表示限制值，不作为点测量进入统计；非正值也排除。本次七个参数均未发现需额外剔除的非正值。不做均值插补，也不要求七个参数同时完整。</p></article><article><h3>极端值保留，尺度调整</h3><p>用 1.5 IQR 规则标记长尾候选点，结合分位数审查，不自动删除。周期、半径和质量在关系图中使用对数坐标，避免少数大值压缩主体分布。</p></article></div>{quality_table}
<p class="small">“有值的限制值”只统计原本有数值、因非零限制标记被剔除的单元格；它与原本缺失及非正值剔除互不重叠。质量列是最佳质量字段，可能包含 Msini 等来源，只有质量–半径图进一步限定 Mass。</p>
</section>
<section id="discovery">{heading('03','发现方法与历史：样本的形成过程','悬停查数值；历史图可切换方法、调整截止年份。')}
<div class="charts">{chart(6,f'凌日法发现 {by_method["Transit"]["value"]:,} 颗（{by_method["Transit"]["share"]:.1f}%），径向速度法 {by_method["Radial Velocity"]["value"]:,} 颗（{by_method["Radial Velocity"]["share"]:.1f}%）。这些比例描述档案中行星的构成，不能比较不同方法在相同条件下的探测效率。','方法是否均衡？')}
{chart(4,f'在快照中的完整历史年份里，{peak_year} 年收录的发现最多（{int(annual.loc[peak_year]):,} 颗）。这是按发现年分组的档案计数，不是论文发布量或任务观测次数。{a["year_max"]} 年仅覆盖快照中的记录，柱/线的下降不能解读成全年发现速度下降。档案回溯修订也可能影响历史计数。','何时被发现？')}</div></section>
<section id="distribution">{heading('04','描述统计：长尾比均值更有信息','以中位数和 IQR 描述主体，极端范围保留透明。')}
<div class="prose"><p>有效周期的均值为 {f(period['mean'])} 天，中位数为 {f(period['median'])} 天；有效半径的均值为 {f(radius['mean'])} R⊕，中位数为 {f(radius['median'])} R⊕。均值受大值影响明显，因此重点比较中位数、四分位区间与 P10–P90，而不只报告均值。</p></div>{stats_table}
<div class="charts">{chart(7,f'共 {radius["n"]:,} 颗行星有有效半径；中间 50% 位于 {f(radius["q1"])}–{f(radius["q3"])} R⊕。切换方法后，箱边界保持不变，方便比较形状；同时检查有效 n，因为更低的柱高可能只是样本量更小。箱末端包含全局最大值，其他箱为左闭右开。','半径如何分布？')}
{chart(3,f'凌日法周期中位数为 {f(tr["value"])} 天，径向速度法为 {f(rv["value"])} 天；两类样本的典型周期明显不同。凌日事件的几何概率和重复观测需求可能使短周期更容易进入样本，这是与结果相符的观测机制解释，未在本研究中量化校正。线段是 P10–P90，并非 Tukey 的 1.5 IQR 须；超出该区间的行星仍保留在分析里。','分方法的周期差异？')}</div></section>
<section id="coverage">{heading('05','测量覆盖：缺失本身也是结果','颜色越深表示不可用比例越高；悬停查看方法分母。')}
<div class="charts">{chart(1,f'半径处理后不可用比例为 {radius["missing_pct"]:.1f}%。方法之间的覆盖差异意味着缺失不能简单视作随机噪声。周期–半径完整案例中凌日法比例为 {a["complete_case_transit_pct"]:.1f}%，高于主样本的 {by_method["Transit"]["share"]:.1f}%；完整案例已经改变了方法构成。矩阵只展示主样本中至少 25 颗行星的方法，小方法仍包含在主统计和方法构成图中。','完整案例代表谁？')}</div>
<div class="callout"><strong>清洗决策</strong><p>不对物理量作全表插补。零半径、平均质量或跨参考文献补值可能制造关系，且无法解决方法相关的缺失。每幅图使用自己所需字段的完整案例，并明示有效 n；这保留了可解释性，也保留了选择偏差这一限制。</p></div></section>
<section id="relationships">{heading('06','物理关系：总体、分组与稳健性','散点支持方法筛选、框选联动和附近点的悬停。')}
<div class="charts">{chart(0,f'总体 Spearman ρ={b["rho"]:.3f}，按宿主系统重采样的 95% percentile 区间为 [{b["low"]:.3f}, {b["high"]:.3f}]。关联强度很弱；区间即使不含零，也不能据此声称有强预测能力或因果关系。坐标为双对数，但 Spearman 基于秩，单调对数变换不会改变该系数。筛选保持坐标范围，刷选会联动展示所选点的类别与半径分布。','周期与半径有关吗？')}
{chart(2,f'径向速度法只有 {within["Radial Velocity"]["n"]} 个周期–半径完整案例，成像法只有 {within["Imaging"]["n"]} 个。此表展示主样本至少 25 颗行星的方法；方法内的系数可以帮助识别总体汇总的局限，但极小样本的系数波动大，不能稳定排列不同方法的“相关强弱”。本研究不把总体与分组不同直接称为辛普森悖论。','总体关系在组内成立吗？')}
</div><div class="robustness"><div><div class="eyebrow">ROBUSTNESS / 稳健性检验</div><h3>改变分析口径，结论会改变吗？</h3><p>主样本含 {a['controversial']} 颗争议标记行星。排除它们后 ρ={sensitivity[1]['rho']:.3f}；将周期和半径分别限制在原完整样本各自 P1–P99 内后 ρ={sensitivity[2]['rho']:.3f}。报告保留主样本并展示这些结果，避免只挑选更显著的子样本。</p><p class="small">Bootstrap 以完整案例的 {b['clusters']:,} 个宿主为抽样单位，有放回抽取同样数量的宿主，并保留宿主内所有完整行星，共 {b['replicates']:,} 次，种子 {b['seed']}。区间只反映现有观测样本条件下的系统间变化，不能校正探测偏差或非随机缺失。</p></div>{sensitivity_table}</div>
<div class="charts">{chart(5,f'保留 {a["mass_radius_n"]:,} 颗具有 Mass 来源质量与有效半径的行星。最佳质量字段里还包含 Msini 等来源；Msini 是最小质量，不能与直接质量无区别混用。图中探索的是满足条件的子样本，未计入测量误差，不能仅凭散点拟合宣称统一的质量–半径定律。','质量来源影响关系吗？')}
{chart(8,f'周期–半长轴的成对秩相关为 {pr["value"]:.3f}（n={pr["n"]:,}）。这是值得进一步检查的物理一致性线索，但参数可能来自相互依赖的模型计算，不能当作独立验证。每对变量的有效样本不同，所以矩阵各单元格的系数不能忽略 n 直接比较；悬停可以核对分母。','哪些物理量共同变化？')}</div></section>
<section id="discussion">{heading('07','讨论与结论：能说明什么，不能说明什么','探索性分析提出证据与后续问题，不替代因果识别。')}
<div class="conclusions"><article><span>01</span><h3>首先，分析单位决定答案。</h3><p>{a['raw_rows']:,} 行参数解缩减为 {a['planets']:,} 颗唯一默认已确认行星。否则文献丰富的系统会被重复加权，发现计数和参数分布都会失真。</p></article><article><span>02</span><h3>其次，方法与缺失共同选择样本。</h3><p>凌日法在主样本与完整案例中的占比不同。缺失矩阵和分方法周期分布说明，“看得到”与“测得全”是两个筛选环节。</p></article><article><span>03</span><h3>最后，弱关联需要克制解释。</h3><p>周期–半径总体秩相关很弱；分组样本量悬殊，质量来源也需约束。结果支持继续研究测量与探测机制，不能推断全宇宙丰度或宜居概率。</p></article></div>
<div class="discussion-grid"><article><h3>主要限制</h3><ul><li>非概率抽样且缺失与方法相关，bootstrap 不能纠正总体代表性。</li><li>同一宿主的行星不是独立观测；仅核心相关区间采用系统级重采样。</li><li>此报告不传播每个参数的测量误差，也未建模上下限的删失机制。</li><li>仅使用默认参数集；更换文献参数解可能改变物理量和完整案例。</li><li>2026 年不完整，档案持续更新；本地快照不代表最新在线总量。</li></ul></article><article><h3>下一步可以怎么研究</h3><ul><li>在同一发现方法、相似观测条件与宿主属性内比较分布。</li><li>纳入测量误差和删失数据模型，比较 PS 默认解与其他参考解。</li><li>若研究真实发生率，结合具体巡天的探测效率和完整性模型。</li><li>正式建模前预先定义问题，使用恒星系统分组验证，避免同系统数据泄漏。</li></ul></article></div></section>
<section id="reproduce">{heading('08','复现与数据来源','网页由 Node.js 服务；D3 v7.9.0 本地加载，无需 CDN。')}
<div class="reproduction"><article><h3>运行与重新分析</h3><pre><code>cd projects/nasa-exoplanets\nnpm start\n# 浏览器打开 http://127.0.0.1:3000\n\n# 重跑分析（需要本项目 requirements.txt 中的 Python 依赖）\nnpm run analyze\nnpm test</code></pre><p class="small">已包含生成后的页面与数据，展示只需要 Node.js 18+，不需 npm install。Python 仅在重算时使用，可先运行 <code>python3 -m pip install -r requirements.txt</code>。若端口占用，可使用 <code>PORT=3001 npm start</code>。请勿运行旧的全项目页面生成脚本覆盖此报告。</p></article><article><h3>下载与核查</h3><div class="downloads"><a href="analysis/descriptive_statistics.csv" download>描述统计 CSV ↗</a><a href="analysis/confirmed_planets.csv" download>清洗后的行星 CSV ↗</a><a href="analysis/discovery_methods.csv" download>方法构成 CSV ↗</a><a href="eda_profile.csv" download>全部 {a['raw_columns']} 字段审计 ↗</a><a href="analysis/report.json" download>完整分析结果 JSON ↗</a><a href="analysis/bootstrap.json" download>Bootstrap 设置与结果 ↗</a><a href="build_report.py">报告生成代码 ↗</a><a href="eda.py">基础 EDA 代码 ↗</a><a href="eda_support.py">分析辅助代码 ↗</a><a href="report_page.py">页面生成代码 ↗</a><a href="analysis/field_dictionary.csv" download>92 字段完整字典 ↗</a><a href="analysis/sensitivity.csv" download>敏感性结果 CSV ↗</a><a href="README.md">运行说明 ↗</a></div><p class="small">全量有效点参与统计及绘图，未作展示抽样。依赖版本：Python {r['versions']['python']} · pandas {r['versions']['pandas']} · NumPy {r['versions']['numpy']} · SciPy {r['versions']['scipy']}。</p></article></div>
<div class="sources"><h3>官方资料与来源透明度</h3><p><a href="https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&amp;config=PS" target="_blank" rel="noreferrer">NASA PS 原始数据页面</a> · <a href="https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html" target="_blank" rel="noreferrer">字段及统计单位定义</a> · <a href="https://exoplanetarchive.ipac.caltech.edu/docs/planetarysystems_about.html" target="_blank" rel="noreferrer">PS 表说明</a> · <a href="https://exoplanetarchive.ipac.caltech.edu/docs/pscp_about.html" target="_blank" rel="noreferrer">PSCompPars 参数计算说明</a> · <a href="https://exoplanetarchive.ipac.caltech.edu/docs/TAP/usingTAP.html" target="_blank" rel="noreferrer">TAP 查询说明</a></p><p>分析使用你提供的 <code>PS_2026.10.01_06.21.14.csv</code>，原文件逐字节保存在本项目 <code>data/</code>。文件头记录 NASA 导出时间为 2026-10-01 06:21:14（时区未注明），导出共 92 列；未混用目录里的旧版全字段快照。最新 rowupdate={a['max_rowupdate']} 是记录更新时间，不能据此断言实际下载日期。需要重建相同快照时应使用已保留文件，而不是重新查询持续更新的在线表。</p><p>原始文件 {a['source_bytes']:,} bytes · SHA-256<br><code>{a['sha256']}</code></p><p>资料用于确认表结构和字段定义；本页的所有数字与结论由本地数据计算。档案中的参数来自相应观测文献，NASA Archive 是汇集与发布平台。</p></div></section>
<footer><span>5002 / DATA SCIENCE RESEARCH</span><span>NASA PS · EXPLORATORY DATA ANALYSIS · 2026</span></footer></main><div class="tooltip" role="status"></div><noscript><p class="error">请启用 JavaScript 以查看 D3 图表；上面的统计表、分析过程与结论仍可阅读。</p></noscript><script src="site/d3.v7.min.js"></script><script src="site/data.js"></script><script src="site/app.js"></script></body></html>'''
    return html
