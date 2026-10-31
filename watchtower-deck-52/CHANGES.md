# Changes

## 2026-10-31
- Created the deck (owner: "yes"). 52 cards in `cards.py`. Game "Keep the Ledger": `game.py` and `RULES.md`.
- Tuned by simulation, not by guess. Hand 5 with lose-at-8 won 12% of 2,000 games, too hard. Hand 7 with lose-at-8 wins about 57%; chosen because it keeps the Unaccounted Eight.
- Tests 19/19, 25 of 25 runs. One scrub false positive along the way: the word "secrets" on the Scrub card. The pattern now matches `secret=` / `token:` / `sk-ant-`, not the word.
- build-1: JSON, CSV, xlsx, SQLite, .sql, SPSS; 52 of 52 read back in each; manifest with hashes.
- Not committed. Not in the staged public copy yet.
