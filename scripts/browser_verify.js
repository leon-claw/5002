async (page) => {
  const slugs = [
    "nyc-film-permits",
    "nasa-exoplanets",
    "college-majors-2026",
    "central-park-squirrels",
    "steam-games-v2",
    "world-happiness",
  ];
  const summary = [];
  let errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  for (const slug of slugs) {
    errors = [];
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto("http://127.0.0.1:8765/projects/" + slug + "/");
    await page.waitForFunction(() => document.body.dataset.ready === "true");
    const initial = await page.evaluate(() => ({
      errors: [...document.querySelectorAll(".error")].map(
        (d) => d.textContent,
      ),
      charts: document.querySelectorAll(".chart").length,
      findings: document.querySelectorAll(".finding").length,
      invalid: [...document.querySelectorAll("svg *")].filter((el) =>
        [...el.attributes].some(
          (a) =>
            /^(d|x|y|cx|cy|width|height|transform)$/.test(a.name) &&
            /NaN|Infinity/.test(a.value),
        ),
      ).length,
      negative: [...document.querySelectorAll("svg rect")].filter(
        (el) => +el.getAttribute("width") < 0 || +el.getAttribute("height") < 0,
      ).length,
      overflow: document.documentElement.scrollWidth > innerWidth + 1,
    }));
    if (
      errors.length ||
      initial.errors.length ||
      initial.invalid ||
      initial.negative ||
      initial.overflow
    )
      throw new Error(
        slug + " initial " + JSON.stringify({ errors, ...initial }),
      );
    const selects = page.locator(".chart select");
    for (let i = 0; i < (await selects.count()); i++) {
      let s = selects.nth(i),
        options = await s
          .locator("option")
          .evaluateAll((els) => els.map((e) => e.value));
      if (options.length > 1) {
        await s.selectOption(options[options.length - 1]);
        await s.selectOption(options[0]);
      }
    }
    const sc = page.locator('.chart[data-kind="scatter"]').first();
    let brushed = false;
    if (await sc.count()) {
      await sc.scrollIntoViewIfNeeded();
      const before = await sc.locator(".selection-status").textContent();
      let box = await sc.locator(".brush .overlay").boundingBox();
      await page.mouse.move(box.x + box.width * 0.15, box.y + box.height * 0.2);
      await page.mouse.down();
      await page.mouse.move(
        box.x + box.width * 0.65,
        box.y + box.height * 0.82,
        { steps: 12 },
      );
      await page.mouse.up();
      let after = await sc.locator(".selection-status").textContent();
      if (before === after) throw new Error(slug + " brush did not update");
      brushed = true;
      await sc.locator(".reset-brush").click();
      if ((await sc.locator(".selection-status").textContent()) !== before)
        throw new Error(slug + " brush reset failed");
    }
    const ranges = page.locator("input[type=range]");
    for (let i = 0; i < (await ranges.count()); i++) {
      let s = ranges.nth(i);
      await s.evaluate((el) => {
        el.value = "0";
        el.dispatchEvent(new Event("input", { bubbles: true }));
      });
      await s.evaluate((el) => {
        el.value = el.max;
        el.dispatchEvent(new Event("input", { bubbles: true }));
      });
    }
    if (slug === "world-happiness") {
      const s = page.getByRole("searchbox", { name: "搜索国家" });
      await s.fill("Finland");
      if (!(await page.locator('[data-kind="dumbbell"] svg').count()))
        throw new Error("search no SVG");
      await s.fill("NO_COUNTRY_MATCH");
      if (!(await page.locator('[data-kind="dumbbell"] .chart-empty').count()))
        throw new Error("search empty state missing");
      await s.fill("");
      await page
        .locator('[data-kind="composition"] select')
        .selectOption("Afghanistan");
    }
    if (slug === "central-park-squirrels") {
      let s = page.locator('[data-kind="map"]');
      await s.getByLabel("班次").selectOption("AM");
      await s.getByLabel("毛色").selectOption("Gray");
      const label = await s.locator(".selection-status").textContent();
      if (label.includes("显示 3,023 /"))
        throw new Error("map filters ineffective");
      await s.getByLabel("班次").selectOption("全部");
      await s.getByLabel("毛色").selectOption("全部");
    }
    if (errors.length || (await page.locator(".error").count()))
      throw new Error(slug + " interaction errors " + errors.join(","));
    const exportButton = page.locator(".export").first();
    await exportButton.scrollIntoViewIfNeeded();
    const dlPromise = page.waitForEvent("download");
    await exportButton.click();
    const dl = await dlPromise;
    await dl.saveAs("output/playwright/" + slug + "-chart.svg");
    await page.evaluate(() => scrollTo(0, 0));
    await page.screenshot({
      path: "output/playwright/" + slug + "-desktop.png",
      fullPage: true,
    });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.evaluate(() => scrollTo(0, 0));
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth > innerWidth + 1,
    );
    if (overflow) throw new Error(slug + " mobile body overflow");
    await page.screenshot({
      path: "output/playwright/" + slug + "-mobile.png",
      fullPage: true,
    });
    const geometry = await page.evaluate(
      () =>
        [...document.querySelectorAll("svg *")].filter((el) =>
          [...el.attributes].some(
            (a) =>
              /^(d|x|y|cx|cy|width|height|transform)$/.test(a.name) &&
              /NaN|Infinity/.test(a.value),
          ),
        ).length,
    );
    if (geometry) throw new Error(slug + " invalid geometry after interaction");
    summary.push({
      slug,
      charts: initial.charts,
      findings: initial.findings,
      brushed,
      selects: await selects.count(),
      exported: true,
      mobile: true,
      errors: errors.length,
    });
  }
  return summary;
}
