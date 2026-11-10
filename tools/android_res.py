"""Create Android launcher icons and the splash image in assets/android/res/.

Run from the repo root after tools/app_art.py. Needs Pillow.
tools/android_setup.js copies these into the generated Android project.
"""
import os

from PIL import Image

OUT = 'assets/android/res'
LEGACY = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
FOREGROUND = {'mdpi': 108, 'hdpi': 162, 'xhdpi': 216, 'xxhdpi': 324, 'xxxhdpi': 432}

icon = Image.open('assets/icon-only.png').convert('RGBA')
foreground = Image.open('assets/icon-foreground.png').convert('RGBA')
background = Image.open('assets/icon-background.png').convert('RGBA')
full = background.copy()
full.alpha_composite(foreground)

for density, size in LEGACY.items():
    folder = os.path.join(OUT, f'mipmap-{density}')
    os.makedirs(folder, exist_ok=True)
    icon.resize((size, size), Image.LANCZOS).save(os.path.join(folder, 'ic_launcher.png'))
    full.resize((size, size), Image.LANCZOS).save(os.path.join(folder, 'ic_launcher_round.png'))
    foreground.resize((FOREGROUND[density],) * 2, Image.LANCZOS).save(os.path.join(folder, 'ic_launcher_foreground.png'))

# The splash art is centred on blue by drawable/splash.xml, so it is never stretched.
art = Image.open('assets/title.png').convert('RGB').resize((810, 1440), Image.NEAREST)
os.makedirs(os.path.join(OUT, 'drawable-nodpi'), exist_ok=True)
art.save(os.path.join(OUT, 'drawable-nodpi', 'splash_art.png'), optimize=True)
