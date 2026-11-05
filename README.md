# NonoIndo

A phone-first nonogram game where each solved puzzle reveals pixel art of everyday Indonesian life.

## Play

Open `index.html` in a browser, or serve this folder with any static host such as GitHub Pages. Phaser 3.80.1 loads from a CDN, so the first load needs internet.

## Project layout

- `index.html`: the Phaser game, with its title art embedded
- `data/`: one file per category (food, general, transport, landmark, animal) holding its puzzles; add a puzzle by appending to that file's `puzzles` list
- `assets/`: main screen art with and without the title
- `tools/check_puzzles.py`: checks that each puzzle has one solution and can be solved by logic (needs Pillow)
- `tools/title_art.py`: regenerates the main screen art (needs Pillow)
- `prototypes/canvas-version.html`: the first version, built without Phaser (paste into an HTML page or publish as an artifact)
- `docs/brainstorm.md`: game ideas and plans
