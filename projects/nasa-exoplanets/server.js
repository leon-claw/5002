'use strict';
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = __dirname;
const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.csv': 'text/csv; charset=utf-8', '.md': 'text/plain; charset=utf-8', '.py': 'text/plain; charset=utf-8' };
function createServer() {
  return http.createServer((req, res) => {
    if (!['GET', 'HEAD'].includes(req.method)) {
      res.writeHead(405, { Allow: 'GET, HEAD' }); return res.end();
    }
    let name;
    try { name = decodeURIComponent(new URL(req.url, 'http://localhost').pathname); }
    catch { res.writeHead(400); return res.end('Bad request'); }
    if (name === '/') name = '/index.html';
    const target = path.resolve(root, '.' + name);
    const relative = path.relative(root, target).split(path.sep).join('/');
    const publicFile = ['index.html', 'README.md', 'eda.py', 'eda_support.py', 'requirements.txt', 'verify_report.py', 'build_report.py', 'report_page.py', 'eda_profile.csv', 'eda_summary.json'].includes(relative)
      || /^(site|analysis)\/[A-Za-z0-9_.-]+\.(js|css|json|csv)$/.test(relative);
    if (!target.startsWith(root + path.sep) || !publicFile) {
      res.writeHead(404); return res.end('Not found');
    }
    fs.stat(target, (error, stat) => {
      if (error || !stat.isFile()) { res.writeHead(404); return res.end('Not found'); }
      res.writeHead(200, { 'Content-Type': types[path.extname(target)] || 'text/plain; charset=utf-8', 'Content-Length': stat.size, 'Cache-Control': 'no-cache', 'X-Content-Type-Options': 'nosniff' });
      if (req.method === 'HEAD') return res.end();
      const stream = fs.createReadStream(target);
      stream.on('error', () => res.destroy());
      stream.pipe(res);
    });
  });
}
if (require.main === module) {
  const port = Number(process.env.PORT || 3000);
  if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error('PORT must be between 1 and 65535');
  const server = createServer();
  server.on('error', error => { console.error(error.code === 'EADDRINUSE' ? `Port ${port} is busy. Try PORT=3001 npm start.` : error.message); process.exitCode = 1; });
  server.listen(port, process.env.HOST || '127.0.0.1', () => console.log(`NASA EDA · http://127.0.0.1:${port}`));
}
module.exports = { createServer };
