from PIL import Image, ImageDraw, ImageFont

PAL = {
    'W': (245, 245, 240), 'G': (190, 195, 200), 'R': (205, 50, 45),
    'B': (130, 85, 55), 'b': (165, 115, 75), 'Y': (240, 190, 60),
    'S': (175, 205, 225), 'D': (85, 45, 25), 'K': (120, 65, 30),
    'O': (185, 95, 30), 'T': (215, 170, 110), 'I': (225, 240, 245),
    'P': (200, 225, 235), 'L': (120, 170, 70), 'C': (225, 215, 195),
}
BG = (255, 248, 230)

ART = {
    'bakso': [
        "...S..S...",
        "..BB..BB..",
        ".BbBDBbBB.",
        ".BBBDBBBB.",
        "WWWWWWWWWW",
        "WRWRWWRWRW",
        ".WWWWWWWW.",
        "..WWWWWW..",
        "...WWWW...",
        "...GGGG...",
    ],
    'sate': [
        ".......T..",
        "......KK..",
        ".....KDK.T",
        "....KKK.KK",
        "...KDK.KDK",
        "..KKK.KKK.",
        ".KDK.KDK..",
        ".TK.KKK...",
        "WT.KDK..WW",
        "WWWWWWWWW.",
    ],
    'es_teh_plastik': [
        "......R...",
        "..P...R.P.",
        "..PP..RPP.",
        "...PPPRP..",
        ".....YY...",
        "...OOOOO..",
        "..OIOOOOO.",
        "..OOOOIOO.",
        "..OOIOOOO.",
        "...OOOOO..",
    ],
}


def runs(line):
    out, n = [], 0
    for v in line:
        if v:
            n += 1
        elif n:
            out.append(n)
            n = 0
    if n:
        out.append(n)
    return out


def placements(clue, size):
    if not clue:
        return [tuple([0] * size)]
    res = []
    def rec(i, pos, cur):
        if i == len(clue):
            res.append(tuple(cur + [0] * (size - len(cur))))
            return
        rest = sum(clue[i + 1:]) + len(clue[i + 1:])
        for s in range(pos, size - clue[i] - rest + 1):
            prefix = cur + [0] * (s - len(cur)) + [1] * clue[i]
            if i < len(clue) - 1:
                prefix = prefix + [0]
            rec(i + 1, len(prefix), prefix)
    rec(0, 0, [])
    return res


def line_solve(rc, cc, size):
    """Logic only: returns the grid (None = undetermined)."""
    g = [[None] * size for _ in range(size)]
    rp = [placements(c, size) for c in rc]
    cp = [placements(c, size) for c in cc]
    changed = True
    while changed:
        changed = False
        for r in range(size):
            rp[r] = [p for p in rp[r] if all(g[r][i] in (None, p[i]) for i in range(size))]
            for i in range(size):
                vals = {p[i] for p in rp[r]}
                if len(vals) == 1 and g[r][i] is None:
                    g[r][i] = vals.pop()
                    changed = True
        for c in range(size):
            cp[c] = [p for p in cp[c] if all(g[i][c] in (None, p[i]) for i in range(size))]
            for i in range(size):
                vals = {p[i] for p in cp[c]}
                if len(vals) == 1 and g[i][c] is None:
                    g[i][c] = vals.pop()
                    changed = True
    return g


def count_solutions(rc, cc, size, limit=5):
    rp = [placements(c, size) for c in rc]
    found = []
    def ok(rows):
        for c in range(size):
            col = [r[c] for r in rows]
            target = cc[c]
            partial = runs(col)
            if len(rows) == size:
                if partial != target:
                    return False
            else:
                closed = partial[:-1] if col[-1] else partial
                if closed != target[:len(closed)]:
                    return False
                if col[-1] and partial:
                    idx = len(partial) - 1
                    if idx >= len(target) or partial[-1] > target[idx]:
                        return False
                elif len(closed) > len(target):
                    return False
        return True
    def rec(rows):
        if len(found) >= limit:
            return
        if len(rows) == size:
            found.append([list(r) for r in rows])
            return
        for p in rp[len(rows)]:
            if ok(rows + [p]):
                rec(rows + [p])
    rec([])
    return found


def check(name, art):
    size = len(art)
    assert all(len(r) == size for r in art), name
    grid = [[0 if ch == '.' else 1 for ch in row] for row in art]
    rc = [runs(r) for r in grid]
    cc = [runs([grid[r][c] for r in range(size)]) for c in range(size)]
    g = line_solve(rc, cc, size)
    unknown = sum(v is None for row in g for v in row)
    sols = count_solutions(rc, cc, size)
    filled = sum(map(sum, grid))
    print(f"{name}: filled={filled}/100 solutions={len(sols)}{'+' if len(sols) >= 5 else ''} "
          f"unknown_after_logic={unknown}")
    print("  rows", rc)
    print("  cols", cc)
    return rc, cc, grid, unknown, len(sols)


def render(results):
    cell, gap, label = 34, 40, 34
    n = len(ART)
    W = n * (10 * cell) + (n + 1) * gap
    H = 2 * (10 * cell) + 3 * gap + 2 * label
    img = Image.new('RGB', (W, H), (250, 250, 250))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
    except OSError:
        font = ImageFont.load_default()
    for i, (name, art) in enumerate(ART.items()):
        ox = gap + i * (10 * cell + gap)
        oy = gap + label
        d.text((ox, gap), name.replace('_', ' '), fill=(40, 40, 40), font=font)
        oy2 = oy + 10 * cell + gap + label
        d.text((ox, oy + 10 * cell + gap), 'puzzle shape', fill=(110, 110, 110), font=font)
        for r, row in enumerate(art):
            for c, ch in enumerate(row):
                x, y = ox + c * cell, oy + r * cell
                d.rectangle([x, y, x + cell, y + cell], fill=PAL.get(ch, BG))
                y2 = oy2 + r * cell
                d.rectangle([x, y2, x + cell, y2 + cell],
                            fill=(35, 35, 40) if ch != '.' else (255, 255, 255),
                            outline=(200, 200, 200))
    img.save('puzzle_check.png')


results = {n: check(n, a) for n, a in ART.items()}
render(results)
