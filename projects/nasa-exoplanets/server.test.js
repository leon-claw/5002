const { test } = require('node:test');
const assert = require('node:assert/strict');
const { createServer } = require('./server');

test('Node service serves the report, local D3 and auditable data', async (t) => {
  const server = createServer();
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => server.close(resolve)));
  const base = `http://127.0.0.1:${server.address().port}`;
  for (const [url, mime] of [['/', 'text/html'], ['/site/d3.v7.min.js', 'javascript'], ['/analysis/report.json', 'application/json'], ['/eda_profile.csv', 'text/csv']]) {
    const res = await fetch(base + url);
    assert.equal(res.status, 200, url);
    assert.ok(res.headers.get('content-type').includes(mime), url);
    assert.ok((await res.text()).length > 100, url);
  }
  const head = await fetch(base, { method: 'HEAD' });
  assert.equal(head.status, 200);
  assert.equal(await head.text(), '');
  assert.equal((await fetch(base + '/not-a-file')).status, 404);
  assert.equal((await fetch(base, { method: 'POST' })).status, 405);
  assert.equal((await fetch(base + '/server.js')).status, 404);
  assert.equal((await fetch(base + '/site/%2e%2e%2fserver.js')).status, 404);
  assert.equal((await fetch(base + '/%zz')).status, 400);
});
