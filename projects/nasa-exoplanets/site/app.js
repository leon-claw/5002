/* Offline D3 v7 evidence views. Statistical findings are computed in Python. */
"use strict";
const palette = [
  "#3875bd",
  "#db7444",
  "#409b83",
  "#9c6bb2",
  "#bc9940",
  "#d66080",
  "#628293",
  "#79a242",
  "#7864cc",
  "#46a2b8",
  "#bd6670",
];
const methodColor = d3.scaleOrdinal(DATA.methodOrder, palette);
const theme = getComputedStyle(document.body),
  ink = theme.getPropertyValue("--ink").trim(),
  muted = theme.getPropertyValue("--muted").trim(),
  accent = theme.getPropertyValue("--accent").trim(),
  accent2 = theme.getPropertyValue("--accent2").trim(),
  paper = theme.getPropertyValue("--paper").trim();
const tip = document.querySelector(".tooltip"),
  fmt = (v) =>
    v == null
      ? "—"
      : Math.abs(v) >= 1000
        ? d3.format(",.0f")(v)
        : d3.format(".3~f")(v),
  num = d3.format(",");
const short = (s, n = 30) =>
  String(s).length > n ? String(s).slice(0, n - 1) + "…" : s;
function show(e, text) {
  tip.textContent = text;
  tip.style.display = "block";
  tip.style.left =
    Math.max(5, Math.min(innerWidth - 350, e.clientX + 14)) + "px";
  tip.style.top =
    Math.max(5, Math.min(innerHeight - 140, e.clientY + 14)) + "px";
}
function hide() {
  tip.style.display = "none";
}
function hover(sel, fn) {
  sel
    .on("pointermove.tip", (e, d) => show(e, fn(d)))
    .on("pointerleave.tip", hide);
  sel.append("title").text(fn);
}
function legend(body, groups, color) {
  const l = body.append("div").attr("class", "legend");
  groups.forEach((g) => {
    let s = l.append("span");
    s.append("i").style("background", color(g));
    s.append("b").style("font-weight", "400").text(g);
  });
  return l;
}
function controls(body) {
  return body.append("div").attr("class", "controls");
}
function select(control, label, values, selected) {
  const l = control.append("label").text(label + " "),
    s = l.append("select").attr("aria-label", label);
  s.selectAll("option")
    .data(values)
    .join("option")
    .attr("value", (d) => d)
    .text((d) => d);
  if (selected != null) s.property("value", selected);
  return s;
}
function setup(body, { w = 620, h = 360, left = 70, bottom = 60 } = {}) {
  let m = { l: left, r: 22, t: 22, b: bottom };
  let svg = body
    .append("div")
    .attr("class", "plot")
    .append("svg")
    .attr("viewBox", `0 0 ${w} ${h}`)
    .attr("role", "img");
  return { svg, w, h, m };
}
function scale(kind, values, range, zero = false) {
  let ext = d3.extent(
    values.filter((v) => v != null && Number.isFinite(+v)),
    Number,
  );
  if (!Number.isFinite(ext[0])) ext = [0, 1];
  if (zero) ext[0] = Math.min(0, ext[0]);
  if (ext[0] === ext[1])
    ext = [
      ext[0] - (kind === "log" ? ext[0] * 0.1 : 0.5),
      ext[1] + (kind === "log" ? ext[1] * 0.1 : 0.5),
    ];
  if (kind === "log") ext[0] = Math.max(Number.MIN_VALUE, ext[0]);
  return (
    kind === "log"
      ? d3.scaleLog()
      : kind === "symlog"
        ? d3.scaleSymlog()
        : d3.scaleLinear()
  )
    .domain(ext)
    .nice()
    .range(range);
}
function numericalAxis(side, s) {
  const axis = (side === "bottom" ? d3.axisBottom : d3.axisLeft)(s).ticks(6);
  if (s.base || s.constant) {
    const [lo, hi] = s.domain();
    let candidates = [];
    if (lo <= 0 && hi >= 0) candidates.push(0);
    for (let e = -5; e <= 10; e++) {
      const v = 10 ** e;
      if (v >= lo && v <= hi) candidates.push(v);
      if (-v >= lo && -v <= hi) candidates.push(-v);
    }
    candidates.sort((a, b) => a - b);
    // Keep separated labels in display coordinates, including symlog's zero neighborhood.
    let previous = -Infinity;
    const ticks = candidates.filter((v) => {
      let px = Math.abs(s(v) - s(lo));
      if (px - previous < 35) return false;
      previous = px;
      return true;
    });
    if (ticks.length >= 2) axis.tickValues(ticks);
  }
  return axis.tickFormat((v) =>
    Math.abs(v) >= 1000 ? d3.format("~s")(v) : d3.format(".3~g")(v),
  );
}
function axes(ctx, x, y, xLabel = "", yLabel = "") {
  const { svg, w, h, m } = ctx;
  svg
    .append("g")
    .attr("class", "gridline")
    .attr("transform", `translate(${m.l},0)`)
    .call(
      d3
        .axisLeft(y)
        .ticks(5)
        .tickSize(-(w - m.l - m.r))
        .tickFormat(""),
    );
  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${h - m.b})`)
    .call(numericalAxis("bottom", x));
  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(${m.l},0)`)
    .call(numericalAxis("left", y));
  svg
    .append("text")
    .attr("class", "xlabel")
    .attr("x", (m.l + w - m.r) / 2)
    .attr("y", h - 12)
    .attr("text-anchor", "middle")
    .text(xLabel);
  svg
    .append("text")
    .attr("class", "ylabel")
    .attr("transform", `translate(16,${(m.t + h - m.b) / 2}) rotate(-90)`)
    .attr("text-anchor", "middle")
    .text(yLabel);
}
function empty(body) {
  body
    .append("p")
    .attr("class", "chart-empty")
    .text("当前筛选没有可显示的数据，请重置筛选。");
}
function scatter(body, c) {
  const all = c.data.filter(
    (d) =>
      d.x != null &&
      d.y != null &&
      Number.isFinite(+d.x) &&
      Number.isFinite(+d.y) &&
      (c.scaleX !== "log" || d.x > 0) &&
      (c.scaleY !== "log" || d.y > 0),
  );
  const groups = [...new Set(all.map((d) => d.group))].sort(),
    color = methodColor,
    bar = controls(body),
    sel = select(bar, "分组", ["全部", ...groups]);
  bar
    .append("button")
    .attr("class", "reset-brush")
    .text("清除框选")
    .on("click", () => brushLayer.call(brush.move, null));
  const status = body
    .append("div")
    .attr("class", "selection-status")
    .attr("aria-live", "polite");
  const ctx = setup(body, { w: 1050, h: 470, left: 85 }),
    { svg, w, h, m } = ctx;
  const x = scale(
      c.scaleX,
      all.map((d) => +d.x),
      [m.l, w - m.r],
    ),
    y = scale(
      c.scaleY,
      all.map((d) => +d.y),
      [h - m.b, m.t],
    );
  axes(ctx, x, y, c.xLabel, c.yLabel);
  const dots = svg
    .append("g")
    .attr("class", "points")
    .selectAll("circle")
    .data(all)
    .join("circle")
    .attr("cx", (d) => x(d.x))
    .attr("cy", (d) => y(d.y))
    .attr("r", all.length > 1500 ? 2.8 : 4.5)
    .attr("fill", (d) => color(d.group))
    .attr("opacity", 0.58);
  const brush = d3
    .brush()
    .extent([
      [m.l, m.t],
      [w - m.r, h - m.b],
    ])
    .on("brush end", ({ selection }) => update(selection));
  const brushLayer = svg.append("g").attr("class", "brush").call(brush);
  const companion = body.append("div").attr("class", "selection-grid"),
    groupBox = companion.append("div"),
    histBox = companion.append("div");
  groupBox.append("h4").text("选中点的类别构成");
  histBox.append("h4").text("选中点的纵轴分布（按轴尺度等宽分箱）");
  let active = all,
    nearest = d3.Delaunay.from(
      active,
      (d) => x(d.x),
      (d) => y(d.y),
    );
  brushLayer
    .on("pointermove.tooltip", function (e) {
      if (e.buttons || !active.length) return;
      let [px, py] = d3.pointer(e, svg.node()),
        d = active[nearest.find(px, py)];
      if (Math.hypot(px - x(d.x), py - y(d.y)) < 18)
        show(
          e,
          `${d.label}\n${d.group}\n${c.xLabel}: ${fmt(d.x)}\n${c.yLabel}: ${fmt(d.y)}`,
        );
      else hide();
    })
    .on("pointerleave", hide);
  function update(selection) {
    let group = sel.property("value");
    active = all.filter((d) => group === "全部" || d.group === group);
    let chosen = active.filter(
      (d) =>
        !selection ||
        (x(d.x) >= selection[0][0] &&
          x(d.x) <= selection[1][0] &&
          y(d.y) >= selection[0][1] &&
          y(d.y) <= selection[1][1]),
    );
    let set = new Set(chosen);
    dots
      .attr("opacity", (d) => (set.has(d) ? 0.68 : 0.035))
      .attr("r", (d) => (set.has(d) ? (all.length > 1500 ? 2.8 : 4.5) : 2));
    nearest = d3.Delaunay.from(
      active,
      (d) => x(d.x),
      (d) => y(d.y),
    );
    status.text(
      `分析总体 ${num(c.population || all.length)}；图中 ${num(all.length)} 点；当前筛选 ${num(active.length)} 点；框选 ${num(chosen.length)} 点。${chosen.length ? "选中点的纵轴中位数 = " + fmt(d3.median(chosen, (d) => +d.y)) + "。" : ""} 以下汇总仅描述显示点。`,
    );
    groupBox.selectAll("svg").remove();
    histBox.selectAll("svg").remove();
    if (!chosen.length) {
      groupBox.append("svg").attr("viewBox", "0 0 420 150");
      histBox.append("svg").attr("viewBox", "0 0 420 150");
      return;
    }
    let sums = d3
        .rollups(
          chosen,
          (v) => v.length,
          (d) => d.group,
        )
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6),
      ss = groupBox.append("svg").attr("viewBox", "0 0 470 150"),
      bx = d3.scaleLinear([0, d3.max(sums, (d) => d[1])], [160, 420]),
      by = d3
        .scaleBand(
          sums.map((d) => d[0]),
          [4, 144],
        )
        .padding(0.25);
    ss.selectAll("rect")
      .data(sums)
      .join("rect")
      .attr("x", 160)
      .attr("y", (d) => by(d[0]))
      .attr("width", (d) => bx(d[1]) - 160)
      .attr("height", by.bandwidth())
      .attr("fill", (d) => color(d[0]));
    ss.selectAll("text.name")
      .data(sums)
      .join("text")
      .attr("class", "name")
      .attr("x", 152)
      .attr("y", (d) => by(d[0]) + by.bandwidth() / 2 + 4)
      .attr("text-anchor", "end")
      .text((d) => short(d[0], 21));
    ss.selectAll("text.count")
      .data(sums)
      .join("text")
      .attr("class", "count")
      .attr("x", (d) => bx(d[1]) + 6)
      .attr("y", (d) => by(d[0]) + by.bandwidth() / 2 + 4)
      .text((d) => num(d[1]));
    let hs = histBox.append("svg").attr("viewBox", "0 0 470 150"),
      hx = scale(
        c.scaleY,
        chosen.map((d) => +d.y),
        [35, 450],
      );
    let boundaries = d3
        .range(1, 12)
        .map((i) => hx.invert(35 + ((450 - 35) * i) / 12)),
      bins = d3.bin().domain(hx.domain()).thresholds(boundaries)(
        chosen.map((d) => +d.y),
      );
    let hy = d3.scaleLinear([0, d3.max(bins, (d) => d.length) || 1], [116, 7]);
    hs.selectAll("rect")
      .data(bins)
      .join("rect")
      .attr("x", (d) => hx(d.x0) + 1)
      .attr("width", (d) => Math.max(0, hx(d.x1) - hx(d.x0) - 2))
      .attr("y", (d) => hy(d.length))
      .attr("height", (d) => 116 - hy(d.length))
      .attr("fill", accent);
    hs.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(0,116)")
      .call(numericalAxis("bottom", hx));
  }
  sel.on("change", () => {
    brushLayer.call(brush.move, null);
    update(null);
  });
  update(null);
  legend(body, groups.slice(0, 15), color);
  body
    .append("p")
    .attr("class", "footnote")
    .text(
      "拖动框选 → 下方两个视图同步更新。双对数图只包含正值；方法筛选保持全样本坐标范围。",
    );
}
function heatmap(body, c) {
  let d = c.data,
    xs = [...new Set(d.map((v) => String(v.x)))],
    ys = [...new Set(d.map((v) => String(v.y)))],
    w = 680,
    h = Math.max(320, ys.length * 36 + 95),
    m = { l: 190, r: 28, t: 22, b: 90 },
    ctx = setup(body, { w, h, left: m.l, bottom: m.b }),
    svg = ctx.svg;
  let x = d3.scaleBand(xs, [m.l, w - m.r]).padding(0.07),
    y = d3.scaleBand(ys, [m.t, h - m.b]).padding(0.08),
    max = c.fixedDomain || d3.max(d, (v) => Math.abs(v.value || 0)) || 1,
    color = c.diverging
      ? d3.scaleDiverging([-max, 0, max], d3.interpolateRdBu)
      : d3.scaleSequential([0, c.percent ? 100 : max], d3.interpolateBlues);
  // Positive residuals/associations are red; negative values blue.
  if (c.diverging)
    color = d3.scaleDiverging([-max, 0, max], (t) => d3.interpolateRdBu(1 - t));
  let cells = svg
    .selectAll("rect.cell")
    .data(d)
    .join("rect")
    .attr("class", "cell")
    .attr("x", (d) => x(String(d.x)))
    .attr("y", (d) => y(String(d.y)))
    .attr("width", x.bandwidth())
    .attr("height", y.bandwidth())
    .attr("rx", 3)
    .attr("fill", (d) => (d.value == null ? "#e1e5eb" : color(d.value)));
  hover(
    cells,
    (d) =>
      `${d.y} / ${d.x}\n值: ${fmt(d.value)}${c.percent ? "%" : ""}${d.n != null ? "\nn = " + num(d.n) : ""}${d.expected != null ? "\n期望 = " + fmt(d.expected) : ""}${d.reported != null ? "\n有值 = " + num(d.reported) : ""}`,
  );
  svg
    .selectAll("text.row")
    .data(ys)
    .join("text")
    .attr("x", m.l - 10)
    .attr("y", (d) => y(d) + y.bandwidth() / 2 + 4)
    .attr("text-anchor", "end")
    .text((d) => short(d, 28))
    .append("title")
    .text((d) => d);
  svg
    .selectAll("text.col")
    .data(xs)
    .join("text")
    .attr(
      "transform",
      (d) =>
        `translate(${x(d) + x.bandwidth() / 2},${h - m.b + 14}) rotate(-32)`,
    )
    .attr("text-anchor", "end")
    .text((d) => short(d, 20));
  if (x.bandwidth() > 36)
    svg
      .selectAll("text.value")
      .data(d)
      .join("text")
      .attr("x", (d) => x(String(d.x)) + x.bandwidth() / 2)
      .attr("y", (d) => y(String(d.y)) + y.bandwidth() / 2 + 4)
      .attr("text-anchor", "middle")
      .style("fill", (d) =>
        Math.abs(d.value || 0) > max * 0.5 ? "#fff" : "#21334a",
      )
      .style("font-size", "10px")
      .style("pointer-events", "none")
      .text((d) =>
        d.value == null
          ? "—"
          : c.percent
            ? Math.round(d.value)
            : d3.format(".2f")(d.value),
      );
  body
    .append("p")
    .attr("class", "footnote")
    .text(
      c.diverging
        ? `色域 −${fmt(max)} … 0 … +${fmt(max)}；蓝色为负，红色为正。`
        : `色域 0 … ${c.percent ? "100%" : fmt(max)}；颜色越深，值越高。`,
    );
}
function interval(body, c) {
  let d = c.data,
    h = Math.max(320, d.length * 28 + 80),
    ctx = setup(body, { w: 650, h, left: 220, bottom: 45 }),
    { svg, w, m } = ctx;
  let values = d.flatMap((z) => [z.lo, z.hi, z.value]).filter((v) => v != null),
    x = scale(c.scale, values, [m.l, w - m.r], c.zero),
    y = d3
      .scaleBand(
        d.map((z) => z.label),
        [m.t, h - m.b],
      )
      .padding(0.3);
  if (c.zero && x.domain()[0] <= 0 && x.domain()[1] >= 0)
    svg
      .append("line")
      .attr("x1", x(0))
      .attr("x2", x(0))
      .attr("y1", m.t)
      .attr("y2", h - m.b)
      .attr("stroke", muted)
      .attr("stroke-dasharray", "3 3");
  let g = svg
    .selectAll("g.row")
    .data(d)
    .join("g")
    .attr("class", "row")
    .attr("transform", (z) => `translate(0,${y(z.label) + y.bandwidth() / 2})`);
  g.append("line")
    .attr("x1", (z) => x(z.lo))
    .attr("x2", (z) => x(z.hi))
    .attr("stroke", accent)
    .attr("stroke-width", c.kind === "box" ? 2 : 3);
  if (c.kind === "box")
    g.append("rect")
      .attr("x", (z) => x(z.q1))
      .attr("width", (z) => Math.max(1, x(z.q3) - x(z.q1)))
      .attr("y", -7)
      .attr("height", 14)
      .attr("fill", accent)
      .attr("opacity", 0.4);
  g.append("circle")
    .attr("cx", (z) => x(z.value))
    .attr("r", 4)
    .attr("fill", accent2);
  hover(
    g,
    (z) =>
      `${z.label}\nn=${num(z.n)}\n中位数/估计值: ${fmt(z.value)}\n范围: ${fmt(z.lo)}–${fmt(z.hi)} ${c.unit || ""}${z.q1 != null ? "\nIQR: " + fmt(z.q1) + "–" + fmt(z.q3) : ""}`,
  );
  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(${m.l},0)`)
    .call(d3.axisLeft(y).tickFormat((z) => short(z, 29)));
  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${h - m.b})`)
    .call(numericalAxis("bottom", x));
  svg
    .append("text")
    .attr("x", w - 30)
    .attr("y", h - 8)
    .attr("text-anchor", "end")
    .text(c.unit || "");
}
function barChart(body, c) {
  let ctx = setup(body, {
      w: 650,
      h: Math.max(300, c.data.length * 28 + 60),
      left: 210,
      bottom: 35,
    }),
    { svg, w, h, m } = ctx,
    d = c.data;
  let x = d3.scaleLinear(
      [0, d3.max(d, (z) => z.value) || 1],
      [m.l, w - m.r - 45],
    ),
    y = d3
      .scaleBand(
        d.map((z) => z.label),
        [m.t, h - m.b],
      )
      .padding(0.25);
  hover(
    svg
      .selectAll("rect")
      .data(d)
      .join("rect")
      .attr("x", m.l)
      .attr("y", (z) => y(z.label))
      .attr("width", (z) => x(z.value) - m.l)
      .attr("height", y.bandwidth())
      .attr("fill", accent),
    (z) => `${z.label}: ${fmt(z.value)} ${c.unit || ""}`,
  );
  svg
    .append("g")
    .attr("class", "axis")
    .attr("transform", `translate(${m.l},0)`)
    .call(d3.axisLeft(y).tickFormat((z) => short(z, 29)));
  svg
    .selectAll("text.count")
    .data(d)
    .join("text")
    .attr("x", (z) => x(z.value) + 7)
    .attr("y", (z) => y(z.label) + y.bandwidth() / 2 + 4)
    .text((z) => num(z.value));
}
function dumbbell(body, c) {
  let control = controls(body),
    search = c.search
      ? control
          .append("input")
          .attr("type", "search")
          .attr("placeholder", "搜索国家名称")
          .attr("aria-label", "搜索国家")
      : null;
  let holder = body.append("div");
  function draw() {
    holder.html("");
    let query = search ? search.property("value").toLowerCase() : "",
      arr = c.data.filter(
        (d) => !query || d.label.toLowerCase().includes(query),
      );
    if (c.search && !query) arr = [...arr.slice(0, 10), ...arr.slice(-10)];
    if (!arr.length) {
      empty(holder);
      return;
    }
    let ctx = setup(holder, {
        w: 650,
        h: Math.max(310, arr.length * 27 + 70),
        left: 210,
        bottom: 40,
      }),
      { svg, w, h, m } = ctx,
      x = scale(
        null,
        arr.flatMap((d) => [d.left, d.right]),
        [m.l, w - m.r],
        !c.search,
      ),
      y = d3
        .scaleBand(
          arr.map((d) => d.label),
          [m.t, h - m.b],
        )
        .padding(0.3);
    let g = svg
      .selectAll("g.row")
      .data(arr)
      .join("g")
      .attr("class", "row")
      .attr(
        "transform",
        (d) => `translate(0,${y(d.label) + y.bandwidth() / 2})`,
      );
    g.append("line")
      .attr("x1", (d) => x(d.left))
      .attr("x2", (d) => x(d.right))
      .attr("stroke", muted)
      .attr("stroke-width", 2);
    g.append("circle")
      .attr("cx", (d) => x(d.left))
      .attr("r", 4)
      .attr("fill", accent);
    g.append("circle")
      .attr("cx", (d) => x(d.right))
      .attr("r", 4)
      .attr("fill", accent2);
    hover(
      g,
      (d) =>
        `${d.label}\n${c.leftLabel}: ${fmt(d.left)}\n${c.rightLabel}: ${fmt(d.right)}\n变化: ${fmt(d.right - d.left)} ${c.unit || ""}`,
    );
    svg
      .append("g")
      .attr("class", "axis")
      .attr("transform", `translate(${m.l},0)`)
      .call(d3.axisLeft(y).tickFormat((z) => short(z, 30)));
    svg
      .append("g")
      .attr("class", "axis")
      .attr("transform", `translate(0,${h - m.b})`)
      .call(d3.axisBottom(x).ticks(5));
  }
  legend(body, [c.leftLabel, c.rightLabel], (d) =>
    d === c.leftLabel ? accent : accent2,
  );
  if (search) search.on("input", draw);
  draw();
}
function lineChart(body, c) {
  let arr = c.data.map((d) => ({
      ...d,
      xx:
        typeof d.x === "string" && /^\d{4}-\d{2}$/.test(d.x)
          ? +new Date(d.x + "-01T00:00:00Z")
          : +d.x,
    })),
    date = arr.some((d) => typeof d.x === "string"),
    groups = [...new Set(arr.map((d) => d.group))],
    color = methodColor,
    control = controls(body),
    sel = select(
      control,
      c.single ? "国家" : "曲线",
      c.single ? groups : ["全部", ...groups],
      c.single ? (groups.includes("Finland") ? "Finland" : groups[0]) : "全部",
    );
  const years = [...new Set(arr.map((d) => d.xx))].sort((a, b) => a - b);
  let range = control
      .append("label")
      .text("截止点 ")
      .append("input")
      .attr("type", "range")
      .attr("min", 0)
      .attr("max", years.length - 1)
      .attr("value", years.length - 1)
      .attr("aria-label", "截止时间"),
    stamp = control.append("span");
  let holder = body.append("div");
  function draw() {
    holder.html("");
    let value = sel.property("value"),
      end = years[+range.property("value")],
      d = arr.filter(
        (d) => d.xx <= end && (value === "全部" || d.group === value),
      );
    stamp.text(date ? d3.utcFormat("%Y-%m")(new Date(end)) : end);
    if (!d.length) {
      empty(holder);
      return;
    }
    let ctx = setup(holder, { w: 660, h: 370, left: 62 }),
      { svg, w, h, m } = ctx,
      x = scale(
        null,
        arr.map((d) => d.xx),
        [m.l, w - m.r],
      ),
      y = scale(
        null,
        d.map((d) => d.value),
        [h - m.b, m.t],
        !c.single && c.zeroBaseline !== false,
      );
    axes(ctx, x, y, c.xLabel, c.yLabel);
    svg
      .selectAll(".axis")
      .filter((_, i) => i === 0)
      .call(
        d3
          .axisBottom(x)
          .ticks(6)
          .tickFormat((v) =>
            date ? d3.utcFormat("%Y-%m")(new Date(v)) : d3.format("d")(v),
          ),
      );
    let grouped = d3.group(d, (z) => z.group),
      path = d3
        .line()
        .defined((z) => z.value != null)
        .x((z) => x(z.xx))
        .y((z) => y(z.value));
    for (let [g, rows] of grouped) {
      rows.sort((a, b) => a.xx - b.xx);
      svg
        .append("path")
        .datum(rows)
        .attr("d", path)
        .attr("fill", "none")
        .attr("stroke", color(g))
        .attr("stroke-width", 2.4);
      hover(
        svg
          .append("g")
          .selectAll("circle")
          .data(rows.filter((d) => d.value != null))
          .join("circle")
          .attr("cx", (d) => x(d.xx))
          .attr("cy", (d) => y(d.value))
          .attr("r", 3)
          .attr("fill", color(g)),
        (d) => `${d.group}\n${d.x}: ${fmt(d.value)}`,
      );
    }
  }
  sel.on("change", draw);
  range.on("input", draw);
  draw();
  if (!c.single) legend(body, groups, color);
}
function flow(body, c) {
  let ctx = setup(body, { w: 1050, h: 440, left: 180, bottom: 25 }),
    { svg, w, h } = ctx,
    left = [...new Set(c.data.map((d) => d.source))],
    right = [...new Set(c.data.map((d) => d.target))],
    total = d3.sum(c.data, (d) => d.value),
    pad = 16,
    k = (h - 65 - Math.max(left.length, right.length) * pad) / total,
    color = d3.scaleOrdinal(left, palette),
    ly = {},
    ry = {},
    lcur = {},
    rcur = {};
  function pos(keys, field, dest, cursor) {
    let y = 38;
    keys.forEach((key) => {
      let value = d3.sum(
          c.data.filter((d) => d[field] === key),
          (d) => d.value,
        ),
        hh = value * k;
      dest[key] = { y, height: hh, value };
      cursor[key] = y;
      y += hh + pad;
    });
  }
  pos(left, "source", ly, lcur);
  pos(right, "target", ry, rcur);
  let links = c.data.map((d) => {
    let hh = d.value * k,
      l = lcur[d.source],
      r = rcur[d.target];
    lcur[d.source] += hh;
    rcur[d.target] += hh;
    return { ...d, l, r, hh };
  });
  let x1 = 210,
    x2 = 780;
  hover(
    svg
      .selectAll("path.flow")
      .data(links)
      .join("path")
      .attr("class", "flow")
      .attr(
        "d",
        (d) =>
          `M${x1},${d.l} C470,${d.l} 520,${d.r} ${x2},${d.r} L${x2},${d.r + d.hh} C520,${d.r + d.hh} 470,${d.l + d.hh} ${x1},${d.l + d.hh} Z`,
      )
      .attr("fill", (d) => color(d.source))
      .attr("opacity", 0.35)
      .on("pointerenter", function () {
        d3.select(this).attr("opacity", 0.8);
      })
      .on("pointerleave", function () {
        d3.select(this).attr("opacity", 0.35);
      }),
    (d) =>
      `${d.source} → ${d.target}\n${num(d.value)} 条事件\n源类别占比 ${d3.format(".1%")(d.value / ly[d.source].value)}`,
  );
  for (let [keys, dict, x, side] of [
    [left, ly, x1, "left"],
    [right, ry, x2, "right"],
  ]) {
    svg
      .selectAll("rect." + side)
      .data(keys)
      .join("rect")
      .attr("x", side === "left" ? x - 12 : x)
      .attr("y", (d) => dict[d].y)
      .attr("width", 12)
      .attr("height", (d) => Math.max(1, dict[d].height))
      .attr("fill", side === "left" ? (d) => color(d) : accent);
    svg
      .selectAll("text." + side)
      .data(keys)
      .join("text")
      .attr("x", side === "left" ? x - 20 : x + 20)
      .attr("y", (d) => dict[d].y + dict[d].height / 2 + 4)
      .attr("text-anchor", side === "left" ? "end" : "start")
      .style("font-size", "14px")
      .text((d) => `${d} · ${num(dict[d].value)}`);
  }
}
function mapChart(body, c) {
  const control = controls(body),
    shift = select(control, "班次", ["全部", "AM", "PM"]),
    fur = select(control, "毛色", [
      "全部",
      ...new Set(c.data.map((d) => d.fur)),
    ]);
  let reset = control.append("button").text("重置地图");
  let status = body.append("p").attr("class", "selection-status"),
    ctx = setup(body, { w: 1050, h: 530, left: 25, bottom: 30 }),
    { svg, w, h } = ctx;
  let lat = (d3.mean(c.data, (d) => d.y) * Math.PI) / 180,
    coords = c.data.map((d) => [d.x * Math.cos(lat) * 111320, d.y * 111320]),
    xe = d3.extent(coords, (d) => d[0]),
    ye = d3.extent(coords, (d) => d[1]),
    k = Math.min((w - 100) / (xe[1] - xe[0]), (h - 75) / (ye[1] - ye[0])),
    x = (v) => w / 2 + (v * Math.cos(lat) * 111320 - (xe[0] + xe[1]) / 2) * k,
    y = (v) => h / 2 - (v * 111320 - (ye[0] + ye[1]) / 2) * k,
    color = d3.scaleOrdinal(["AM", "PM"], palette),
    layer = svg.append("g");
  // No fabricated park boundary: actual observation cloud in a metric local projection.
  let grid = layer.append("g").attr("opacity", 0.35);
  for (let yy = Math.floor(ye[0] / 500) * 500; yy <= ye[1]; yy += 500)
    grid
      .append("line")
      .attr("x1", w / 2 + (xe[0] - (xe[0] + xe[1]) / 2) * k - 20)
      .attr("x2", w / 2 + (xe[1] - (xe[0] + xe[1]) / 2) * k + 20)
      .attr("y1", h / 2 - (yy - (ye[0] + ye[1]) / 2) * k)
      .attr("y2", h / 2 - (yy - (ye[0] + ye[1]) / 2) * k)
      .attr("stroke", muted);
  let dots = layer
    .selectAll("circle")
    .data(c.data)
    .join("circle")
    .attr("cx", (d) => x(d.x))
    .attr("cy", (d) => y(d.y))
    .attr("r", 2.6)
    .attr("fill", (d) => color(d.group))
    .attr("opacity", 0.7);
  hover(
    dots,
    (d) =>
      `${d.label}\n${d.group} · ${d.fur}\n${d.behavior || "所选行为均未记录为 true"}\n${d.x.toFixed(5)}, ${d.y.toFixed(5)}`,
  );
  let zoom = d3
    .zoom()
    .scaleExtent([1, 8])
    .on("zoom", (e) => {
      layer.attr("transform", e.transform);
      dots.attr("r", 2.6 / Math.sqrt(e.transform.k));
      scaleText.text(`比例尺：${fmt(500 / e.transform.k)} m`);
    });
  svg.call(zoom);
  reset.on("click", () => svg.call(zoom.transform, d3.zoomIdentity));
  svg
    .append("text")
    .attr("x", 45)
    .attr("y", 40)
    .style("font-size", "18px")
    .text("N ↑");
  svg
    .append("line")
    .attr("x1", 45)
    .attr("x2", 45 + 500 * k)
    .attr("y1", h - 40)
    .attr("y2", h - 40)
    .attr("stroke", ink)
    .attr("stroke-width", 3);
  let scaleText = svg
    .append("text")
    .attr("x", 45)
    .attr("y", h - 18)
    .text("比例尺：500 m");
  function update() {
    let a = shift.property("value"),
      b = fur.property("value"),
      selected = c.data.filter(
        (d) => (a === "全部" || d.group === a) && (b === "全部" || d.fur === b),
      );
    let set = new Set(selected);
    dots.attr("display", (d) => (set.has(d) ? null : "none"));
    status.text(
      `显示 ${num(selected.length)} / ${num(c.data.length)} 条观测；坐标近似转换为局部米制比例。`,
    );
  }
  shift.on("change", update);
  fur.on("change", update);
  update();
  legend(body, ["AM", "PM"], color);
}
function network(body, c) {
  let ctx = setup(body, { w: 1050, h: 510 }),
    { svg, w, h } = ctx,
    nodes = c.data.nodes.map((d) => ({ ...d })),
    links = c.data.links.map((d) => ({ ...d })),
    radius = d3.scaleSqrt([0, d3.max(nodes, (d) => d.value)], [8, 32]),
    stroke = d3.scaleSqrt([0, d3.max(links, (d) => d.value)], [1, 10]);
  let sim = d3
    .forceSimulation(nodes)
    .randomSource(d3.randomLcg(0.42))
    .force(
      "link",
      d3
        .forceLink(links)
        .id((d) => d.id)
        .distance(135),
    )
    .force("charge", d3.forceManyBody().strength(-400))
    .force("center", d3.forceCenter(w / 2, h / 2))
    .force(
      "collision",
      d3.forceCollide((d) => radius(d.value) + 24),
    )
    .stop();
  for (let i = 0; i < 220; i++) sim.tick();
  nodes.forEach((d) => {
    d.x = Math.max(60, Math.min(w - 80, d.x));
    d.y = Math.max(45, Math.min(h - 45, d.y));
  });
  let edges = svg
    .append("g")
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke", accent)
    .attr("stroke-opacity", 0.28)
    .attr("stroke-width", (d) => stroke(d.value));
  hover(
    edges,
    (d) =>
      `${d.source.id} × ${d.target.id}\n共同游戏 ${num(d.value)}\nlift ${fmt(d.lift)}`,
  );
  let g = svg.append("g").selectAll("g").data(nodes).join("g");
  g.append("circle")
    .attr("r", (d) => radius(d.value))
    .attr("fill", accent)
    .attr("fill-opacity", 0.8)
    .attr("stroke", paper)
    .attr("stroke-width", 2);
  g.append("text")
    .attr("text-anchor", "middle")
    .attr("y", (d) => -radius(d.value) - 8)
    .style("fill", ink)
    .text((d) => d.id);
  hover(g, (d) => `${d.id}\n${num(d.value)} 个游戏`);
  function tick() {
    edges
      .attr("x1", (d) => d.source.x)
      .attr("x2", (d) => d.target.x)
      .attr("y1", (d) => d.source.y)
      .attr("y2", (d) => d.target.y);
    g.attr("transform", (d) => `translate(${d.x},${d.y})`);
  }
  g.call(
    d3.drag().on("drag", (e, d) => {
      d.x = Math.max(35, Math.min(w - 35, e.x));
      d.y = Math.max(35, Math.min(h - 35, e.y));
      tick();
    }),
  );
  tick();
}
function composition(body, c) {
  let control = controls(body),
    sel = select(
      control,
      "国家",
      c.data.map((d) => d.country),
      "Finland",
    ),
    holder = body.append("div");
  function draw() {
    holder.html("");
    let d =
        c.data.find((d) => d.country === sel.property("value")) || c.data[0],
      parts = d.parts,
      ctx = setup(holder, { w: 660, h: 400, left: 60, bottom: 100 }),
      { svg, w, h, m } = ctx,
      color = d3.scaleOrdinal(
        parts.map((d) => d.label),
        palette,
      ),
      running = 0,
      segments = parts.map((p) => {
        let d = { ...p, start: running, end: running + p.value };
        running += p.value;
        return d;
      }),
      x = d3
        .scaleBand(
          parts.map((d) => d.label),
          [m.l, w - m.r],
        )
        .padding(0.25),
      y = scale(
        null,
        [0, 10, ...segments.flatMap((d) => [d.start, d.end])],
        [h - m.b, m.t],
      );
    svg
      .append("g")
      .attr("class", "axis")
      .attr("transform", `translate(${m.l},0)`)
      .call(d3.axisLeft(y).ticks(5));
    svg
      .append("g")
      .attr("class", "axis")
      .attr("transform", `translate(0,${h - m.b})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .attr("transform", "rotate(-32)")
      .attr("text-anchor", "end");
    hover(
      svg
        .selectAll("rect")
        .data(segments)
        .join("rect")
        .attr("x", (d) => x(d.label))
        .attr("y", (d) => y(Math.max(d.start, d.end)))
        .attr("width", x.bandwidth())
        .attr("height", (d) => Math.max(1, Math.abs(y(d.start) - y(d.end))))
        .attr("fill", (d) => (d.value < 0 ? accent2 : color(d.label))),
      (d) => `${d.label}: ${fmt(d.value)}\n累积: ${fmt(d.end)}`,
    );
    svg
      .selectAll("line.connector")
      .data(segments.slice(0, -1))
      .join("line")
      .attr("x1", (d) => x(d.label) + x.bandwidth())
      .attr("x2", (_, i) => x(segments[i + 1].label))
      .attr("y1", (d) => y(d.end))
      .attr("y2", (d) => y(d.end))
      .attr("stroke", muted)
      .attr("stroke-dasharray", "3 3");
    holder
      .append("p")
      .attr("class", "footnote")
      .text(
        `${d.country} · 分解之和 ${fmt(running)}；瀑布图保留负贡献项，负值向下。`,
      );
  }
  sel.on("change", draw);
  draw();
}
function table(body, c) {
  let rows = c.data,
    keys = [...new Set(rows.flatMap(Object.keys))],
    labels = {
      label: "分组 / 变量",
      n: "有效 n",
      rho: "相关系数",
    support: "解读限制",
      pooled_rho: "总体 Spearman",
      within_rank_r: "国家内秩残差 r",
    };
  let t = body.append("div").attr("class", "data-table").append("table");
  t.append("thead")
    .append("tr")
    .selectAll("th")
    .data(keys)
    .join("th")
    .text((k) => labels[k] || k);
  t.append("tbody")
    .selectAll("tr")
    .data(rows)
    .join("tr")
    .selectAll("td")
    .data((d) => keys.map((k) => ({ k, v: d[k] })))
    .join("td")
    .text((d) =>
      d.v == null
        ? "—"
        : typeof d.v === "number"
          ? d.k === "n"
            ? num(d.v)
            : d3.format(".3f")(d.v)
          : d.v,
    );
}
function histogram(body, c) {
  const control = controls(body);
  const chosen = select(control, "发现方法", c.data.map(d => d.group));
  const status = body.append("p").attr("class", "selection-status");
  const holder = body.append("div");
  const first = c.data[0].bins;
  function draw() {
    holder.html("");
    const row = c.data.find(d => d.group === chosen.property("value"));
    status.text(`当前方法：${row.group} · 有效半径 n = ${num(row.n)} · 所有方法使用相同的 24 个箱边界`);
    if (!row.n) { empty(holder); return; }
    const ctx = setup(holder, {w:800, h:380, left:65}), {svg,w,h,m} = ctx;
    const x = d3.scaleLog().domain([first[0].lo, first.at(-1).hi]).range([m.l,w-m.r]);
    const y = d3.scaleLinear().domain([0,d3.max(row.bins,d=>d.count)||1]).nice().range([h-m.b,m.t]);
    axes(ctx,x,y,c.xLabel,c.yLabel);
    hover(svg.selectAll("rect.bin").data(row.bins).join("rect").attr("class","bin")
      .attr("x",d=>x(d.lo)+1).attr("width",d=>Math.max(0,x(d.hi)-x(d.lo)-2))
      .attr("y",d=>y(d.count)).attr("height",d=>h-m.b-y(d.count)).attr("fill",accent),
      d=>`${fmt(d.lo)}–${fmt(d.hi)} R⊕\n${num(d.count)} 颗 · 占当前有效样本 ${d3.format(".1%")(d.count/row.n)}`);
  }
  chosen.on("change",draw); draw();
}
const renderers = {
  histogram,
  scatter,
  heatmap,
  interval,
  box: interval,
  bar: barChart,
  dumbbell,
  line: lineChart,
  flow,
  map: mapChart,
  network,
  composition,
  table,
};
DATA.charts.forEach((c, i) => {
  let root = d3.select("#chart-" + i),
    body = root.select(".chart-body");
  try {
    renderers[c.kind](body, c);
    root.selectAll("svg").attr("aria-label", c.title);
    if (c.kind === "table") root.select(".export").remove();
    else
      root.select(".export").on("click", () => {
        const original = root.select("svg").node();
        if (!original) return;
        let clone = original.cloneNode(true),
          orig = [original, ...original.querySelectorAll("*")],
          copies = [clone, ...clone.querySelectorAll("*")];
        orig.forEach((node, index) => {
          let style = getComputedStyle(node);
          ["fill", "stroke", "font-size", "font-family", "opacity"].forEach(
            (k) =>
              copies[index].style.setProperty(k, style.getPropertyValue(k)),
          );
        });
        clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
        const bounds = original.viewBox.baseVal;
        clone.setAttribute("width", bounds.width);
        clone.setAttribute("height", bounds.height);
        const background = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "rect",
        );
        background.setAttribute("x", bounds.x);
        background.setAttribute("y", bounds.y);
        background.setAttribute("width", bounds.width);
        background.setAttribute("height", bounds.height);
        background.setAttribute("fill", paper);
        clone.prepend(background);
        let desc = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "desc",
        );
        desc.textContent = c.title + " — " + c.note;
        clone.prepend(desc);
        const url = URL.createObjectURL(
            new Blob([new XMLSerializer().serializeToString(clone)], {
              type: "image/svg+xml;charset=utf-8",
            }),
          ),
          a = document.createElement("a");
        a.href = url;
        a.download = DATA.meta.title + "-" + (i + 1) + ".svg";
        document.body.append(a);
        a.click();
        a.remove();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
      });
  } catch (e) {
    console.error(c.title, e);
    body
      .append("p")
      .attr("class", "error")
      .text("该视图加载失败：" + e.message);
  }
});
document.body.dataset.ready = "true";

document.querySelector("#print-report")?.addEventListener("click", () => window.print());
