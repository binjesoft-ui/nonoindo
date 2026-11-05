"""Copy the title art layers into index.html. Run after tools/title_art.py."""
import base64
import json
import re

NAMES = ('sky', 'city', 'bus', 'stall', 'ojol', 'title')
layers = {}
for name in NAMES:
    data = base64.b64encode(open(f'assets/title_layers/{name}.png', 'rb').read()).decode()
    layers[name] = 'data:image/png;base64,' + data

page = open('index.html').read()
line = 'const TITLE_LAYERS = ' + json.dumps(layers) + ';'
page, count = re.subn(r'const TITLE_LAYERS = .*;', lambda m: line, page, count=1)
if count != 1:
    raise SystemExit('TITLE_LAYERS line not found in index.html')
open('index.html', 'w').write(page)
