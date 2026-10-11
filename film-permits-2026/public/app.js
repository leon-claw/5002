"use strict";

const COLORS = ["#32596f", "#4b8796", "#78a9a3", "#e88b53", "#c0a46d"];
const CATEGORY_ZH = {
  Television: "电视", Theater: "剧场", Film: "电影", Commercial: "广告",
  "Still Photography": "静态摄影", WEB: "网络", Documentary: "纪录片",
  Student: "学生作品", "Music Video": "音乐视频",
};
const BOROUGH_ZH = {
  Manhattan: "曼哈顿", Brooklyn: "布鲁克林", Queens: "皇后区",
  Bronx: "布朗克斯", "Staten Island": "史泰登岛",
};
const fmt = d3.format(",");
const tip = document.getElementById("tooltip");

function tooltip(event, text) {
  tip.textContent = text;
  tip.style.display = "block";
  tip.style.left = `${Math.min(window.innerWidth - 275, event.clientX + 14)}px`;
  tip.style.top = `${Math.min(window.innerHeight - 120, event.clientY + 14)}px`;
}
function hideTip() { tip.style.display = "none"; }
function hover(selection, text) {
  selection.on("pointermove", (event, d) => tooltip(event, text(d))).on("pointerleave", hideTip);
  selection.append("title").text(text);
}
function base(id, width, height, margins) {
  const host = d3.select(`#${id}`);
  host.selectAll("*").remove();
  const svg = host.append("svg").attr("viewBox", `0 0 ${width} ${height}`)
    .attr("preserveAspectRatio", "xMidYMid meet");
  const g = svg.append("g").attr("transform", `translate(${margins.left},${margins.top})`);
  return { svg, g, width: width - margins.left - margins.right, height: height - margins.top - margins.bottom };
}
function xAxis(g, x, height, ticks = 6, format) {
  g.append("g").attr("class", "axis").attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).ticks(ticks).tickFormat(format || null).tickSizeOuter(0));
}
function grid(g, y, width, ticks = 5) {
  g.append("g").attr("class", "grid").call(d3.axisLeft(y).ticks(ticks).tickSize(-width).tickFormat(""));
}
function axisStyle(svg) {
  svg.selectAll(".axis text").attr("fill", "#557180");
  svg.selectAll(".axis path,.axis line").attr("stroke", "#aabec3");
}

function trend(data, category) {
  const m = { left: 53, top: 24, right: 23, bottom: 55 };
  const { svg, g, width, height } = base("trend-chart", 1080, 380, m);
  const monthCounts = new Map(data.monthly_category.filter(d => d.category === category).map(d => [d.month, d.count]));
  const series = data.monthly.map(d => ({ date: d3.timeParse("%Y-%m")(d.month), month: d.month, count: category === "all" ? d.count : monthCounts.get(d.month) || 0 }));
  const x = d3.scaleTime().domain(d3.extent(series, d => d.date)).range([0, width]);
  const y = d3.scaleLinear().domain([0, d3.max(series, d => d.count) * 1.13]).nice().range([height, 0]);
  grid(g, y, width);
  const cutoff = d3.timeParse("%Y-%m")("2026-01");
  g.append("rect").attr("x", x(cutoff)).attr("width", width - x(cutoff)).attr("height", height)
    .attr("fill", "#e8ece8").attr("opacity", .9);
  g.append("line").attr("x1", x(cutoff)).attr("x2", x(cutoff)).attr("y2", height).attr("stroke", "#b78866").attr("stroke-dasharray", "4 4");
  g.append("text").attr("x", Math.min(width - 85, x(cutoff) + 8)).attr("y", 17).attr("fill", "#a36c4a").text("2026 · 非完整年");
  g.append("path").datum(series).attr("fill", "none").attr("stroke", "#2f7887")
    .attr("stroke-width", 3).attr("d", d3.line().x(d => x(d.date)).y(d => y(d.count)));
  hover(g.selectAll("circle.event").data(series).join("circle").attr("class", "event hit")
    .attr("cx", d => x(d.date)).attr("cy", d => y(d.count)).attr("r", 5)
    .attr("fill", "#e88b53").attr("stroke", "#f5f8f8").attr("stroke-width", 1.5),
    d => `${d.month} · ${category === "all" ? "全部类别" : CATEGORY_ZH[category]}\n${fmt(d.count)} 条许可事件`);
  xAxis(g, x, height, d3.timeYear.every(1), d3.timeFormat("%Y"));
  g.append("g").attr("class", "axis").call(d3.axisLeft(y).ticks(5).tickFormat(d3.format("d")));
  axisStyle(svg);
}

function borough(data, year) {
  const m = { left: 104, top: 12, right: 20, bottom: 42 };
  const { svg, g, width, height } = base("borough-chart", 1080, 520, m);
  const c = data.by_year[year];
  const lookup = new Map(c.matrix.map(d => [`${d.category}|${d.borough}`, d.count]));
  const x = d3.scaleLinear().domain([0, 100]).range([0, width]);
  const y = d3.scaleBand().domain(data.labels.categories).range([0, height]).padding(.34);
  const rows = [];
  data.labels.categories.forEach(category => {
    const total = d3.sum(data.labels.boroughs, b => lookup.get(`${category}|${b}`) || 0);
    let cursor = 0;
    data.labels.boroughs.forEach((b, i) => {
      const count = lookup.get(`${category}|${b}`) || 0;
      const share = total ? count / total * 100 : 0;
      rows.push({ category, borough: b, count, total, share, x0: cursor, color: COLORS[i] });
      cursor += share;
    });
  });
  g.selectAll("line.guide").data([0,25,50,75,100]).join("line").attr("class", "guide")
    .attr("x1", d => x(d)).attr("x2", d => x(d)).attr("y2", height).attr("stroke", "#d7e2e4");
  hover(g.selectAll("rect.segment").data(rows).join("rect").attr("class", "segment hit")
    .attr("x", d => x(d.x0)).attr("y", d => y(d.category)).attr("width", d => Math.max(0, x(d.share)))
    .attr("height", y.bandwidth()).attr("fill", d => d.color),
    d => `${CATEGORY_ZH[d.category]} × ${BOROUGH_ZH[d.borough]}\n${fmt(d.count)} / ${fmt(d.total)} 条 · ${d.share.toFixed(1)}%`);
  g.append("g").attr("class", "axis").call(d3.axisLeft(y).tickFormat(d => CATEGORY_ZH[d]).tickSize(0)).select(".domain").remove();
  xAxis(g, x, height, 5, d => `${d}%`);
  axisStyle(svg);
  d3.select("#borough-legend").selectAll("span").data(data.labels.boroughs).join("span")
    .html((b, i) => `<i style="background:${COLORS[i]}"></i>${BOROUGH_ZH[b]}`);
}

function heatmap(data, id, kind) {
  const isResidual = kind === "residual";
  const m = { left: 89, top: 25, right: 12, bottom: 55 };
  const { svg, g, width, height } = base(id, 640, 450, m);
  const cats = data.labels.categories;
  const columns = isResidual ? data.labels.boroughs : [0,1,2,3,4,5,6];
  const x = d3.scaleBand().domain(columns).range([0, width]).padding(.055);
  const y = d3.scaleBand().domain(cats).range([0, height]).padding(.08);
  let cells, color;
  if (isResidual) {
    cells = data.residuals;
    color = d3.scaleDiverging().domain([-20, 0, 20]).interpolator(d3.interpolateRgbBasis(["#e3996b", "#e9eff0", "#408f9a"])).clamp(true);
  } else {
    const totals = new Map(cats.map(c => [c, d3.sum(data.weekday.filter(d => d.category === c), d => d.count)]));
    cells = data.weekday.map(d => ({ ...d, total: totals.get(d.category), share: totals.get(d.category) ? d.count / totals.get(d.category) * 100 : 0 }));
    color = d3.scaleSequential().domain([0, 26]).interpolator(d3.interpolateRgb("#e8eff0", "#397f8c")).clamp(true);
  }
  hover(g.selectAll("rect.cell").data(cells).join("rect").attr("class", "cell hit")
    .attr("x", d => x(isResidual ? d.borough : d.day))
    .attr("y", d => y(d.category)).attr("width", x.bandwidth()).attr("height", y.bandwidth())
    .attr("fill", d => color(isResidual ? d.residual : d.share)),
    d => isResidual
      ? `${CATEGORY_ZH[d.category]} × ${BOROUGH_ZH[d.borough]}\n观测 ${fmt(d.count)} · 期望 ${d.expected}\nPearson 残差 ${d.residual}`
      : `${CATEGORY_ZH[d.category]} · ${["周一","周二","周三","周四","周五","周六","周日"][d.day]}\n${fmt(d.count)} / ${fmt(d.total)} 条 · ${d.share.toFixed(1)}%`);
  g.append("g").attr("class", "axis").call(d3.axisLeft(y).tickFormat(d => CATEGORY_ZH[d]).tickSize(0)).select(".domain").remove();
  g.append("g").attr("class", "axis").attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x).tickFormat(d => isResidual ? BOROUGH_ZH[d] : ["一","二","三","四","五","六","日"][d]).tickSize(0))
    .select(".domain").remove();
  svg.selectAll(".axis text").attr("font-size", isResidual ? 10 : 11);
}

function quantiles(data, id, metric) {
  const isDuration = metric === "duration";
  const cats = data.labels.categories.slice(0, 6);
  const m = { left: 93, top: 12, right: 16, bottom: 47 };
  const { svg, g, width, height } = base(id, isDuration ? 640 : 1080, isDuration ? 385 : 345, m);
  const values = cats.map(c => ({ category: c, ...data.distributions[metric][c] }));
  const max = d3.max(values, d => d.p90) * 1.06;
  const x = isDuration ? d3.scaleSymlog().domain([0, max]).range([0, width]) : d3.scaleLinear().domain([0, max]).range([0, width]);
  const y = d3.scaleBand().domain(cats).range([0, height]).padding(.45);
  g.selectAll("line.row-guide").data(values).join("line").attr("class", "row-guide")
    .attr("x2", width).attr("y1", d => y(d.category) + y.bandwidth()/2)
    .attr("y2", d => y(d.category) + y.bandwidth()/2).attr("stroke", "#e0e9ea");
  g.selectAll("line.whisker").data(values).join("line").attr("class", "whisker")
    .attr("x1", d => x(d.p10)).attr("x2", d => x(d.p90))
    .attr("y1", d => y(d.category) + y.bandwidth()/2).attr("y2", d => y(d.category) + y.bandwidth()/2)
    .attr("stroke", "#4b8796").attr("stroke-width", 2);
  g.selectAll("rect.iqr").data(values).join("rect").attr("class", "iqr")
    .attr("x", d => x(d.p25)).attr("y", d => y(d.category))
    .attr("width", d => Math.max(2, x(d.p75) - x(d.p25))).attr("height", y.bandwidth())
    .attr("fill", "#4b8796");
  g.selectAll("circle.median").data(values).join("circle").attr("class", "median")
    .attr("cx", d => x(d.median)).attr("cy", d => y(d.category) + y.bandwidth()/2)
    .attr("r", 5).attr("fill", "#fff").attr("stroke", "#22475d").attr("stroke-width", 1.5);
  hover(g.selectAll("rect.hitbox").data(values).join("rect").attr("class", "hitbox hit")
    .attr("x", 0).attr("y", d => y(d.category)-3).attr("width", width).attr("height", y.step())
    .attr("fill", "transparent"),
    d => `${CATEGORY_ZH[d.category]} · n=${fmt(d.n)}\n中位数 ${d.median.toFixed(1)} ${isDuration ? "小时" : "天"}\nP25–P75 ${d.p25.toFixed(1)}–${d.p75.toFixed(1)}`);
  g.append("g").attr("class", "axis").call(d3.axisLeft(y).tickFormat(d => CATEGORY_ZH[d]).tickSize(0)).select(".domain").remove();
  xAxis(g, x, height, isDuration ? 6 : 7, d => d);
  axisStyle(svg);
}

function annualTable(data) {
  d3.select("#annual-table").selectAll("div").data(data.overview.annual).join("div")
    .attr("class", d => `annual-row ${d.year === 2026 ? "partial" : ""}`)
    .html(d => `<span>${d.year}${d.year === 2026 ? "*" : ""}</span><strong>${fmt(d.count)}</strong>`);
}

fetch("/data/analysis.json").then(response => {
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}).then(data => {
  document.getElementById("hero-count").textContent = fmt(data.quality.analysis_rows);
  document.getElementById("metric-raw").textContent = fmt(data.quality.raw_rows);
  document.getElementById("metric-valid").textContent = fmt(data.quality.analysis_rows);
  document.getElementById("source-hash").textContent = data.meta.source_sha256;
  annualTable(data);
  const trendSelect = document.getElementById("trend-category");
  data.labels.categories.forEach(category => {
    const option = document.createElement("option"); option.value = category; option.textContent = CATEGORY_ZH[category]; trendSelect.append(option);
  });
  trendSelect.addEventListener("change", () => trend(data, trendSelect.value));
  document.getElementById("borough-year").addEventListener("change", event => borough(data, event.target.value));
  trend(data, "all"); borough(data, "all");
  heatmap(data, "residual-chart", "residual"); heatmap(data, "weekday-chart", "weekday");
  quantiles(data, "duration-chart", "duration"); quantiles(data, "lead-chart", "lead");
}).catch(error => {
  document.querySelectorAll(".chart-root").forEach(node => node.textContent = `图表数据加载失败：${error.message}。请运行 npm start 后访问本页面。`);
});
