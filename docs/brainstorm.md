# Indonesian Nonogram Game: Brainstorm

Status: early brainstorm. Title: NonoIndo.

**Stack update:** The game is now built with HTML and Phaser so it can be developed from a phone. The Flutter notes below are kept for reference. Android packaging will use PWABuilder or Capacitor.

## Concept

A mobile nonogram (Picross-style) game where every solved puzzle reveals pixel art of everyday Indonesian life, such as bakso, preman, and busway.

The mechanics are familiar, so the theme is what sets the game apart. The key moment is the reveal: a plain grid bursts into a colored picture with a funny caption that players want to share.

## Feature list

| Feature | What it does | Target |
|---|---|---|
| Core puzzles | 5x5, 10x10, and 15x15 nonograms | First release |
| Reveal and captions | Colored art plus a short joke in bahasa gaul | First release |
| Tips and tricks | Teaches solving techniques | First release |
| Collection | Shows every image the player has unlocked | First release |
| Big environment | Combines all images into one large world | First release (simple), then expand |
| Multiplayer race | Same puzzle, first correct solve wins | After release |

## Content

### Collections

- **Kuliner:** bakso, sate, es teh plastik
- **Jalanan:** preman, tukang parkir, ojol, Pak Ogah
- **Transportasi:** busway, angkot, bajaj
- **Nostalgia SD:** jajanan, seragam merah putih

### Language

Launch in Indonesian first, because the humor is the product. English can come later.

### Content rules

- Use generic designs, with no real logos or brands such as TransJakarta or Indomie.
- Keep the humor affectionate.
- Avoid ethnic or religious stereotypes.

## Feature details

### Multiplayer race

- Two players get the same puzzle, and the first correct solve wins.
- Show a live progress bar for the opponent, not their actual grid.
- Start with private rooms using a code or a WhatsApp invite link. Random matchmaking needs a large player base to work well.
- The server chooses the puzzle and checks the winning solution, which makes cheating harder.
- Rewards could include a win streak, a badge, or an exclusive image.

**Random images:** Pick randomly from the approved puzzle pool. Fully generated images would usually look like noise and might not be solvable without guessing.

**Fairness:** A player who has already solved an image has an advantage. Prefer images neither player has solved, or flip the image so it is harder to recognize.

### Tips and tricks

- Interactive tutorial for the basics, played on a real 5x5 puzzle
- Tip of the day on the loading or home screen
- Technique lessons, such as overlap, edge logic, and crossing out finished rows
- Hints that explain why a square is correct, not only where to place it

### Collection

- Gallery grouped by theme, with locked images shown as silhouettes
- Each image shows its caption, its best time, and possibly a short fact
- Progress for each set, such as "Kuliner 8/12"
- Share button that creates an image for WhatsApp or Instagram

### Big environment

- All images become part of one large scene, such as a busy Jakarta street.
- Each solved image appears in its own place: the bakso cart on the corner, the busway on the road.
- Players can pan and zoom around the world and watch it fill in.
- Each collection can unlock one district, such as market, terminal, or school.
- Light animation can come later, such as a moving busway.

**Design note:** Plan the world map before drawing the puzzles. Each image needs a place in the scene, a consistent art style, and a palette that fits. The world version of each object can be more detailed than the small puzzle version.

## Hard parts

- **Readability:** Some subjects may look like blobs at 10x10. Test the hardest ones early.
- **Fair puzzles:** Each puzzle should have one solution and never require guessing. A solver must check every image.
- **Phone controls:** Grids get cramped from about 15x15. The game needs drag-to-fill, zoom, row and column highlighting, undo, and a fill/cross toggle.
- **Multiplayer scope:** Real-time play adds a backend, disconnection handling, cheating prevention, and running costs.
- **Art volume:** Each image needs a puzzle version and a world version, so the amount of art grows quickly.

## Proposed stack

| Area | Choice | Notes |
|---|---|---|
| App | Flutter | One codebase for Android and iOS, with `CustomPainter` for the grid |
| World map | Flutter, with Flame if needed | Start with layered images and pan/zoom |
| Art | Aseprite | Export each puzzle as a PNG |
| Puzzle pipeline | Python | PNG to clues, solver check, difficulty rating, JSON output |
| Local saves | Device storage | Single-player works offline with no login |
| Multiplayer backend | Decide later | Compare Supabase Realtime, Firebase, and Nakama |

Alternatives: Godot if game feel and animation become the priority. Unity is probably overkill.

Build Android-first, and keep the app small and fast on cheap phones.

## Monetization ideas

- Rewarded ads for hints
- A cheap one-time purchase to remove ads
- Paid puzzle packs later

Decide this after testing whether people enjoy the game.

## Roadmap

1. **Art test:** Draw 10 subjects and run them through the solver.
2. **Prototype:** Build one playable puzzle with good controls and the reveal.
3. **Friend test:** See whether people laugh and want another puzzle.
4. **First release:** Add 30-50 puzzles, tips, collection, and a first version of the world.
5. **Multiplayer test:** Add private two-player races.
6. **Growth:** Add more districts and collections, English, and possibly matchmaking.

## Open questions

- [ ] What is the developer's coding background?
- [ ] Who will draw the art?
- [ ] Is the goal a fun project or income?
- [ ] Will the world be one Jakarta street or an imaginary mix of Indonesia?
- [ ] Should multiplayer be live only, or also allow asynchronous challenges through a shared link?
- [ ] Should grids go beyond 15x15?
