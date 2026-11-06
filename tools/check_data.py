"""Check every puzzle in data/*.js and save a contact sheet.

Run from the repo root: python3 tools/check_data.py [sheet.png]
Each puzzle must have a valid shape and colors, and be fully solvable by logic.
Exits with an error if any puzzle fails. Needs Node.js and Pillow.
"""
import json
import subprocess
import sys

from PIL import Image

code = open('tools/check_puzzles.py').read().split('results = {n:')[0]
solver = {}
exec(code, solver)

DUMP = """
global.window = {};
for (const f of require('fs').readdirSync('data')) if (f.endsWith('.js')) require(process.cwd() + '/data/' + f);
console.log(JSON.stringify(window.PACKS));
"""
packs = json.loads(subprocess.check_output(['node', '-e', DUMP]))
puzzles = [p for pack in packs for p in pack['puzzles']]
seen, failures = set(), []

for p in puzzles:
    art, problems = p['art'], []
    size = len(art)
    if p['id'] in seen:
        problems.append('duplicate id')
    seen.add(p['id'])
    if size not in (10, 15) or any(len(row) != size for row in art):
        problems.append('art is not 10x10 or 15x15')
    else:
        symbols = set(''.join(art)) - {'.'}
        missing = symbols - set(p.get('pal', {}))
        if p.get('pal') and missing:
            problems.append(f'no color for {sorted(missing)}')
        grid = [[0 if ch == '.' else 1 for ch in row] for row in art]
        rows = [solver['runs'](row) for row in grid]
        cols = [solver['runs']([row[c] for row in grid]) for c in range(size)]
        result = solver['line_solve'](rows, cols, size)
        unknown = sum(v is None for row in result for v in row)
        if unknown:
            problems.append(f'needs guessing ({unknown} squares unresolved)')
    if problems:
        failures.append(p['id'])
    print(f"{p['id']:<20} {size}x{size} {'; '.join(problems) or 'ok'}")

if len(sys.argv) > 1:
    PAL = {'W': '#F7F7F2', 'G': '#BEC3C8', 'R': '#CD322D', 'B': '#825537', 'b': '#A5734B', 'Y': '#F0BE3C',
           'S': '#AFCDE1', 'D': '#552D19', 'K': '#78411E', 'O': '#B95F1E', 'T': '#D7AA6E', 'I': '#E1F0F5', 'P': '#C8E1EB'}
    tile, per_row = 150, 8
    sheet = Image.new('RGB', (per_row * (tile + 8), ((len(puzzles) + per_row - 1) // per_row) * (tile + 8)), 'white')
    for i, p in enumerate(puzzles):
        size = len(p['art'])
        im = Image.new('RGB', (size, size), p['bg'])
        colors = p.get('pal') or PAL
        for r, row in enumerate(p['art']):
            for c, ch in enumerate(row):
                if ch != '.' and ch in colors:
                    im.putpixel((c, r), tuple(int(colors[ch][j:j + 2], 16) for j in (1, 3, 5)))
        sheet.paste(im.resize((tile, tile), Image.NEAREST), ((i % per_row) * (tile + 8), (i // per_row) * (tile + 8)))
    sheet.save(sys.argv[1])

print(f'{len(puzzles)} puzzles, {len(failures)} failed')
sys.exit(1 if failures else 0)
