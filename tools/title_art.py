import os
import random
from PIL import Image, ImageDraw

W, H, SCALE = 135, 240, 8
random.seed(17)
LAYERS = {}


def begin_layer(name):
    global img, d
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    LAYERS[name] = img


begin_layer('sky')


def R(x, y, w, h, c):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)


def P(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), tuple(c) + (255,))


def hexc(s):
    return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))


# Sky: hard colour bands with a dithered seam, like hand-placed pixels
BANDS = ['#173FA3', '#2A49B4', '#4B4FBE', '#7A4FB5', '#B04F9C', '#E05A72', '#F4814E', '#FBAE45', '#FFD35A']
top, bot = 0, 172
bh = (bot - top) / len(BANDS)
for y in range(top, bot):
    i = min(len(BANDS) - 1, int((y - top) / bh))
    for x in range(W):
        frac = ((y - top) / bh) % 1
        use = i
        if frac > .72 and i < len(BANDS) - 1 and (x + y) % 2 == 0:
            use = i + 1
        P(x, y, hexc(BANDS[use]))

# Stars in the high sky
for _ in range(34):
    x, y = random.randrange(W), random.randrange(0, 62)
    P(x, y, hexc('#FFF9E8') if random.random() < .4 else hexc('#AFC2FF'))

# Sun with cut bands
cx, cy, rad = 67, 138, 34
for y in range(cy - rad, cy + rad):
    for x in range(cx - rad, cx + rad):
        if (x - cx) ** 2 + (y - cy) ** 2 <= rad ** 2:
            if y > cy + 2 and (y - cy) % 7 < 2:
                continue
            P(x, y, hexc('#FFE27A') if y < cy - 8 else hexc('#FFC93C'))

begin_layer('city')

# Far skyline
FAR = hexc('#6A3F9E')
x = 0
while x < W:
    w = random.randint(7, 13)
    h = random.randint(16, 44)
    if not (52 < x < 76):
        R(x, 172 - h, w, h, FAR)
    x += w
NEAR, LIT = hexc('#2D2470'), hexc('#FFD35A')
x = -2
while x < W:
    w = random.randint(9, 15)
    h = random.randint(10, 30)
    if not (46 < x < 80):
        R(x, 172 - h, w, h, NEAR)
        for wy in range(172 - h + 2, 170, 3):
            for wx in range(x + 2, x + w - 1, 3):
                if random.random() < .38:
                    P(wx, wy, LIT)
    x += w + random.randint(0, 2)

# Monas-style monument in silhouette
MON, GOLD = hexc('#231C5C'), hexc('#FFE27A')
R(52, 168, 31, 4, MON)
R(56, 163, 23, 5, MON)
R(61, 158, 13, 5, MON)
for i, y in enumerate(range(102, 158)):
    half = 1 + i // 18
    R(67 - half, y, half * 2 + 1, 1, MON)
R(65, 100, 5, 2, MON)
R(66, 96, 3, 4, GOLD)
R(67, 92, 1, 4, GOLD)
P(66, 95, hexc('#F4814E'))
P(68, 94, GOLD)

# Power line with hanging cables
POLE = hexc('#1B1646')
R(9, 120, 2, 58, POLE)
R(4, 123, 12, 1, POLE)
R(5, 128, 10, 1, POLE)
for y0, y1 in ((123, 134), (128, 142)):
    for x in range(10, 135):
        t = (x - 10) / 125
        y = int(y0 + (y1 - y0) * t + 11 * (1 - (2 * t - 1) ** 2))
        P(x, y, POLE)

# Sidewalk and road
R(0, 172, W, 8, hexc('#9C93B8'))
for x in range(0, W, 12):
    R(x, 172, 1, 8, hexc('#7E76A0'))
R(0, 179, W, 1, hexc('#5C5582'))
R(0, 180, W, 36, hexc('#37335E'))
for x in range(-3, W, 18):
    R(x, 202, 10, 2, hexc('#F7E9B8'))
R(0, 216, W, 2, hexc('#FFCB2E'))
R(0, 218, W, 22, hexc('#A89FC2'))
for x in range(4, W, 16):
    R(x, 218, 1, 22, hexc('#8D84AB'))

begin_layer('bus')

# Bus in the middle lane (generic, no logo)
BODY, STRIPE, GLASS, DARK = hexc('#E8EEF5'), hexc('#E23A2E'), hexc('#6FB7D8'), hexc('#1B1646')
bx, by = 42, 170
R(bx, by, 74, 28, BODY)
R(bx + 1, by - 1, 72, 1, BODY)
R(bx, by + 20, 74, 4, STRIPE)
R(bx + 3, by + 3, 68, 11, GLASS)
for i in range(1, 7):
    R(bx + 3 + i * 10, by + 3, 1, 11, DARK)
R(bx + 12, by + 3, 8, 17, hexc('#3F8FB5'))
R(bx + 51, by + 3, 8, 17, hexc('#3F8FB5'))
R(bx + 15, by + 3, 1, 17, DARK)
R(bx + 54, by + 3, 1, 17, DARK)
R(bx + 72, by + 22, 2, 2, hexc('#FFE27A'))
R(bx, by + 24, 74, 3, hexc('#8D95A5'))
for wx in (bx + 8, bx + 58):
    R(wx, by + 24, 10, 7, DARK)
    R(wx + 3, by + 26, 4, 3, hexc('#BEC3C8'))

begin_layer('stall')

# Warung stall on the left foreground, with the three puzzle foods on the sign
PAL = {'W': '#F7F7F2', 'G': '#BEC3C8', 'R': '#CD322D', 'B': '#825537', 'b': '#A5734B', 'Y': '#F0BE3C',
       'S': '#AFCDE1', 'D': '#552D19', 'K': '#78411E', 'O': '#B95F1E', 'T': '#D7AA6E', 'I': '#E1F0F5', 'P': '#C8E1EB'}
ART = {
    'bakso': ("#F2A33A", ["...S..S...", "..BB..BB..", ".BbBDBbBB.", ".BBBDBBBB.", "WWWWWWWWWW", "WRWRWWRWRW", ".WWWWWWWW.", "..WWWWWW..", "...WWWW...", "...GGGG..."]),
    'sate': ("#8FD0C4", [".......T..", "......KK..", ".....KDK.T", "....KKK.KK", "...KDK.KDK", "..KKK.KKK.", ".KDK.KDK..", ".TK.KKK...", "WT.KDK..WW", "WWWWWWWWW."]),
    'esteh': ("#2F6FDE", ["......R...", "..P...R.P.", "..PP..RPP.", "...PPPRP..", ".....YY...", "...OOOOO..", "..OIOOOOO.", "..OOOOIOO.", "..OOIOOOO.", "...OOOOO.."]),
}


def stamp(name, x, y):
    bg, rows = ART[name]
    R(x - 1, y - 1, 12, 12, hexc('#1B1646'))
    R(x, y, 10, 10, hexc(bg))
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != '.':
                P(x + c, y + r, hexc(PAL[ch]))


sx, sy = 2, 188
R(sx + 2, sy - 4, 2, 44, hexc('#2D2470'))
R(sx + 42, sy - 4, 2, 44, hexc('#2D2470'))
for i in range(0, 46, 6):
    R(sx + i, sy - 8, 6, 7, hexc('#E23A2E') if (i // 6) % 2 == 0 else hexc('#FFF9E8'))
for i in range(0, 46, 6):
    R(sx + i + 1, sy - 1, 4, 1, hexc('#E23A2E') if (i // 6) % 2 == 0 else hexc('#FFF9E8'))
stamp('bakso', sx + 5, sy + 3)
stamp('sate', sx + 18, sy + 3)
stamp('esteh', sx + 31, sy + 3)
# Counter
R(sx, sy + 20, 46, 3, hexc('#FFCB2E'))
R(sx + 2, sy + 23, 42, 15, hexc('#173FA3'))
for i in range(0, 42, 7):
    R(sx + 2 + i, sy + 23, 1, 15, hexc('#0F2C78'))
# Pot and steam on the counter
R(sx + 7, sy + 16, 12, 4, hexc('#BEC3C8'))
R(sx + 6, sy + 15, 14, 1, hexc('#8D95A5'))
for sxx, syy in ((sx + 10, sy + 14), (sx + 15, sy + 14)):
    P(sxx, syy, hexc('#FFF9E8'))
# Row of tea bags
for tx in (sx + 27, sx + 33, sx + 39):
    R(tx, sy + 16, 4, 4, hexc('#B95F1E'))
    R(tx + 1, sy + 15, 2, 1, hexc('#F0BE3C'))
    P(tx + 3, sy + 14, hexc('#CD322D'))
# Shadow
R(sx + 2, sy + 38, 44, 2, hexc('#7E76A0'))

begin_layer('ojol')

# Ojol rider in the foreground lane
ox, oy = 96, 203
TIRE, GREEN, SKIN, HELM = hexc('#1B1646'), hexc('#2FA36B'), hexc('#C68A5E'), hexc('#FFF9E8')
R(ox - 1, oy + 22, 32, 2, hexc('#2A2750'))
for wx in (ox + 1, ox + 21):
    R(wx, oy + 14, 9, 9, TIRE)
    R(wx + 3, oy + 17, 3, 3, hexc('#BEC3C8'))
R(ox + 7, oy + 12, 15, 6, hexc('#E23A2E'))
R(ox + 4, oy + 10, 8, 3, hexc('#1B1646'))
R(ox + 20, oy + 7, 3, 7, hexc('#E23A2E'))
R(ox + 22, oy + 5, 5, 2, hexc('#1B1646'))
R(ox + 25, oy + 8, 2, 2, hexc('#FFE27A'))
R(ox + 8, oy - 2, 7, 13, GREEN)
R(ox + 7, oy + 10, 9, 5, hexc('#2D2470'))
R(ox + 14, oy + 2, 8, 3, GREEN)
R(ox + 21, oy + 3, 2, 2, SKIN)
R(ox + 9, oy - 9, 8, 7, HELM)
R(ox + 14, oy - 6, 3, 3, hexc('#1B1646'))
R(ox + 9, oy - 3, 5, 1, GREEN)
# Green delivery box
R(ox + 1, oy, 7, 9, hexc('#247F54'))
R(ox + 2, oy + 1, 5, 1, hexc('#2FA36B'))

begin_layer('parkir')

# Tukang parkir on the far sidewalk
tx, ty = 122, 150
R(tx + 1, ty + 1, 6, 5, SKIN)
R(tx, ty, 8, 2, hexc('#1B1646'))
R(tx - 1, ty + 1, 10, 1, hexc('#1B1646'))
R(tx, ty + 6, 8, 11, hexc('#F4814E'))
R(tx, ty + 10, 8, 1, hexc('#FFE27A'))
R(tx - 3, ty + 6, 3, 3, hexc('#F4814E'))
R(tx - 3, ty + 3, 2, 3, SKIN)
R(tx + 1, ty + 17, 2, 8, hexc('#2D2470'))
R(tx + 5, ty + 17, 2, 8, hexc('#2D2470'))
P(tx - 3, ty + 2, hexc('#FFCB2E'))

begin_layer('title')

# Title in a chunky 5x7 pixel face
FONT = {
    'N': ["1...1", "11..1", "11..1", "1.1.1", "1..11", "1..11", "1...1"],
    'O': [".111.", "1...1", "1...1", "1...1", "1...1", "1...1", ".111."],
    'I': ["11111", "..1..", "..1..", "..1..", "..1..", "..1..", "11111"],
    'D': ["1111.", "1...1", "1...1", "1...1", "1...1", "1...1", "1111."],
}


def word(text, y, s, gap):
    tw = len(text) * 5 * s + (len(text) - 1) * gap
    x = (W - tw) // 2
    for ch in text:
        for r, row in enumerate(FONT[ch]):
            for c, b in enumerate(row):
                if b == '1':
                    R(x + c * s + 2, y + r * s + 2, s, s, hexc('#E23A2E'))
        for r, row in enumerate(FONT[ch]):
            for c, b in enumerate(row):
                if b == '1':
                    R(x + c * s, y + r * s, s, s, hexc('#FFCB2E'))
        x += 5 * s + gap


word('NONO', 22, 4, 3)
word('INDO', 56, 4, 3)
LAYERS['city'].alpha_composite(LAYERS.pop('parkir'))
clean = Image.new('RGBA', (W, H))
for name in ('sky', 'city', 'bus', 'stall', 'ojol'):
    clean.alpha_composite(LAYERS[name])
full = clean.copy()
full.alpha_composite(LAYERS['title'])

for name, im in (('assets/title.png', full), ('assets/title_clean.png', clean)):
    im.convert('RGB').resize((W * SCALE, H * SCALE), Image.NEAREST).save(name)
os.makedirs('assets/title_layers', exist_ok=True)
for name, im in LAYERS.items():
    im.save(f'assets/title_layers/{name}.png', optimize=True)
