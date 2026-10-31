# The Watchtower: a 52-card learning deck

Made 2026-10-31 on the owner's "yes" to a deck for the Memalloc watchtower session, under the house rule that every system we learn becomes a 52-card, 4-suit game.

**Suits** (one standard deck):
- ♠ **Watch:** polls and probes.
- ♥ **Check:** rechecks and verification.
- ♦ **Load:** writing to the cloud and reading it back.
- ♣ **Record:** the chain, the logs and the canon.

**Each card** carries the five cookbook layers: principle, naming, tradeoffs, practice, journal. Every journal line is a fact from the session's logs and event chain.

**Game:** *Keep the Ledger*, solo (PvE) or two players (PvP). See `RULES.md`. Each suit answers the one before it in the cycle Watch → Check → Load → Record → Watch. You lose when eight cards are Unaccounted. Simulated over 1,000 games, a greedy keeper wins about 57%.

**Files**
- `cards.py`: the 52 cards.
- `game.py`: rules engine and simulator.
- `RULES.md`
- `build_deck.py`: writes JSON, CSV, Sheets (`.xlsx` with cards, suits and rules sheets), SQL (`.db` and `.sql`) and SPSS (`.sav`), then reads each one back.
- `test_deck.py`: 19 checks. They cover 52 unique cards, four different suits, the cycle, every move legal, all 52 cards accounted for every round, a fair win rate, exact owner quotes, and a public-safety scrub. They passed 25 of 25 runs.

**Builds:** `build-1/`: 52 of 52 read back in all six formats, text identical.

**Public-safe:** no account IDs, storage names or private paths. The scrub is part of the tests.

Lore only links: canon-003 The Watchtower is the story; this deck is the game.
