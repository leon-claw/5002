"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { createServer } = require("./server");

const report = JSON.parse(fs.readFileSync(path.join(__dirname, "public/data/analysis.json"), "utf8"));

test("EDA totals and chart population reconcile", () => {
  assert.equal(report.quality.raw_rows - report.quality.misaligned_rows, report.quality.analysis_rows);
  assert.equal(report.overview.category_counts.reduce((n, x) => n + x.count, 0), report.quality.analysis_rows);
  assert.equal(report.overview.borough_counts.reduce((n, x) => n + x.count, 0), report.quality.analysis_rows);
  assert.equal(report.overview.annual.reduce((n, x) => n + x.count, 0), report.quality.analysis_rows - report.quality.missing_start);
  assert.equal(report.by_year.all.matrix.reduce((n, x) => n + x.count, 0), report.quality.analysis_rows);
  assert.equal(report.quality.lead_pairs - report.quality.lead_negative, 17012);
});

test("Node service serves D3, the page and JSON, and blocks traversal", async (context) => {
  const server = createServer().listen(0, "127.0.0.1");
  await new Promise(resolve => server.once("listening", resolve));
  context.after(() => server.close());
  const origin = `http://127.0.0.1:${server.address().port}`;
  for (const [url, contentType] of [["/", "text/html"], ["/app.js", "text/javascript"], ["/vendor/d3.v7.min.js", "text/javascript"], ["/data/analysis.json", "application/json"]]) {
    const response = await fetch(origin + url);
    assert.equal(response.status, 200, url);
    assert.match(response.headers.get("content-type"), new RegExp(contentType), url);
    assert.ok((await response.text()).length > 100, url);
  }
  const forbidden = await fetch(origin + "/%2e%2e%2fdata%2fFilm_Permits_20260930.csv");
  assert.equal(forbidden.status, 403);
});
