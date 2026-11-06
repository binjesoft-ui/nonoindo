"""Create the Android icon and splash source images. Run from the repo root.

The icon is the letters NI filled in on a nonogram grid. Needs Pillow.
"""
from PIL import Image, ImageDraw

BLUE, PAPER, INK, LINE, RED = (23, 63, 163), (255, 249, 232), (20, 32, 77), (201, 194, 171), (226, 58, 46)
LETTERS = ['1...1.111', '11..1..1.', '11..1..1.', '1.1.1..1.', '1..11..1.', '1..11..1.', '1...1.111']
COLS, ROWS, CELL = 11, 9, 84
CORNERS = ((0, 0), (0, COLS - 1), (ROWS - 1, 0), (ROWS - 1, COLS - 1))


def board(scale=1.0, fill_paper=True):
    size = 1024
    im = Image.new('RGBA', (size, size), PAPER + (255,) if fill_paper else (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cell = round(CELL * scale)
    left, top = (size - COLS * cell) // 2, (size - ROWS * cell) // 2
    mark = max(8, round(12 * scale))
    for r in range(ROWS):
        for c in range(COLS):
            x, y = left + c * cell, top + r * cell
            on = 1 <= r <= 7 and 1 <= c <= 9 and LETTERS[r - 1][c - 1] == '1'
            d.rectangle([x, y, x + cell, y + cell], fill=BLUE if on else PAPER, outline=LINE, width=max(3, round(4 * scale)))
    d.rectangle([left, top, left + COLS * cell, top + ROWS * cell], outline=INK, width=mark)
    for r, c in CORNERS:
        x, y, m = left + c * cell, top + r * cell, round(cell * 0.24)
        d.line([x + m, y + m, x + cell - m, y + cell - m], fill=RED, width=mark)
        d.line([x + cell - m, y + m, x + m, y + cell - m], fill=RED, width=mark)
    return im


board().save('assets/icon-only.png')
board(0.74, fill_paper=False).save('assets/icon-foreground.png')  # Android may crop the outer edge.
Image.new('RGBA', (1024, 1024), PAPER).save('assets/icon-background.png')

title = Image.open('assets/title.png').convert('RGBA')
for name in ('splash.png', 'splash-dark.png'):
    splash = Image.new('RGBA', (2732, 2732), BLUE)
    scaled = title.resize((1350, 2400), Image.NEAREST)
    splash.paste(scaled, ((2732 - 1350) // 2, (2732 - 2400) // 2))
    splash.save(f'assets/{name}', optimize=True)
