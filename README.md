# NonoIndo

NonoIndo is a phone-first nonogram (picross) game. Each solved puzzle reveals pixel art of everyday Indonesian life, such as bakso, angkot, Monas, and wayang.

Made by binjesoft.

> **License:** This repository is source-available for review and portfolio purposes only. It is not open source. You may not copy, modify, or reuse any part of it without written permission from binjesoft. See [LICENSE](LICENSE).

## Features

- 76 solver-checked 10x10 and 15x15 puzzles across 10 categories, from Kuliner to Perayaan
- Every puzzle has one solution and can be solved by logic, without guessing
- Drag-to-fill, Isi and Silang tools, undo, and row or column lock
- Pink highlight when a line can no longer match its numbers
- One-use Petunjuk (hint) and Periksa (check), with gold, silver, and bronze medals
- Difficulty labels (Mudah, Sedang, Sulit) worked out by a built-in solver
- Animated pixel-art main screen, five original songs, and sound effects
- First-time guide, how-to-play pages, and tips, in Indonesian and English
- Progress saved on the device

## Tech stack

| Part | Technology |
|---|---|
| Game | Phaser 3.80.1 and JavaScript |
| Puzzle data | One JavaScript file per category in `data/` |
| Music and sound | Web Audio API, generated in code |
| Saves | Browser `localStorage` |
| Tools | Python with Pillow, and Node.js |
| Android app | Capacitor (in progress) |
| Web hosting | Vercel |

## Project layout

| Path | What it holds |
|---|---|
| `index.html` | The game, with the main screen art embedded |
| `data/` | Puzzles, one file per category |
| `assets/` | Main screen art, its animation layers, and Android icon and splash images |
| `docs/` | Game plan (`brainstorm.md`) and planned puzzle subjects (`puzzle_list.csv`) |
| `prototypes/` | The first version, built without Phaser |
| `tools/check_data.py` | Checks every puzzle and can save a contact sheet |
| `tools/check_puzzles.py` | The line solver used by the checks |
| `tools/title_art.py` | Redraws the main screen art and its layers |
| `tools/embed_title.py` | Copies the main screen layers into `index.html` |
| `tools/app_art.py` | Redraws the Android icon and splash images |
| `tools/build_app.js` | Builds the offline game into `www/` for the Android app |
| `capacitor.config.json`, `package.json` | Android app name, ID (`com.binjesoft.nonoindo`), and build packages |

## Running it (for the owner and approved collaborators)

- **Web:** Serve the repository folder with any static web server and open `index.html`. The web version loads Phaser and fonts from the internet.
- **Puzzle check:** Run `python3 tools/check_data.py sheet.png` from the repository root. It must end with `0 failed`.
- **Offline build:** Run `npm install`, then `node tools/build_app.js`. This creates `www/` with Phaser and the fonts included.

## Third-party components

These components keep their own licenses and are not covered by the NonoIndo license:

- [Phaser](https://phaser.io), MIT License
- Bungee and Figtree fonts, SIL Open Font License 1.1
- [Capacitor](https://capacitorjs.com), MIT License

## Contact

For permission requests or other questions, contact binjesoft through its published contact details.

---

## Ringkasan Bahasa Indonesia

NonoIndo adalah game nonogram (picross) untuk HP. Setiap puzzle yang selesai akan menampilkan pixel art kehidupan sehari-hari di Indonesia. Dibuat oleh binjesoft.

Repositori ini hanya untuk ditinjau dan sebagai portofolio, bukan open source. Dilarang menyalin, mengubah, atau memakai sebagian maupun seluruh isinya tanpa persetujuan tertulis dari binjesoft. Lihat [LICENSE](LICENSE).
