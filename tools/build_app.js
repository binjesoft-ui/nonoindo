// Builds www/, the offline copy of the game used inside the Android app.
// Run from the repo root after `npm install`: node tools/build_app.js
const fs = require('fs');
const path = require('path');

const OUT = 'www';
const FONTS = [
  ['Bungee', 400, '@fontsource/bungee/files/bungee-latin-400-normal.woff2'],
  ['Figtree', 500, '@fontsource/figtree/files/figtree-latin-500-normal.woff2'],
  ['Figtree', 700, '@fontsource/figtree/files/figtree-latin-700-normal.woff2'],
  ['Figtree', 800, '@fontsource/figtree/files/figtree-latin-800-normal.woff2'],
];

fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(path.join(OUT, 'vendor'), { recursive: true });
fs.cpSync('data', path.join(OUT, 'data'), { recursive: true });
fs.copyFileSync('node_modules/phaser/dist/phaser.min.js', path.join(OUT, 'vendor/phaser.min.js'));

const faces = FONTS.map(([family, weight, file]) => {
  const name = path.basename(file);
  fs.copyFileSync(path.join('node_modules', file), path.join(OUT, 'vendor', name));
  return `@font-face { font-family: "${family}"; font-weight: ${weight}; src: url("vendor/${name}") format("woff2"); }`;
}).join('\n');

let page = fs.readFileSync('index.html', 'utf8');
const swap = (pattern, value) => {
  const next = page.replace(pattern, value);
  if (next === page) throw new Error(`index.html has changed, nothing matched ${pattern}`);
  page = next;
};
swap(/<link rel="preconnect"[^>]*>\n/g, '');
swap(/<link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com[^>]*>\n/, `<style>\n${faces}\n</style>\n`);
swap(/const urls = \[[\s\S]*?\];/, "const urls = ['vendor/phaser.min.js'];");
if (/https:\/\//.test(page)) throw new Error('index.html still points to the internet');
fs.writeFileSync(path.join(OUT, 'index.html'), page);
console.log('Built www/ for offline use');
