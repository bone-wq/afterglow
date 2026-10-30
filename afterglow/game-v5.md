# Afterglow v5: tuned rules, Timing, resolution and provenance

v5 builds on `game.md` (v1 rules), so anything not listed here is unchanged.

## What changed from v4
- **Timing category** (owner's request, 2026-10-29). Every card has `timing: {key, value}`:

| Key | Cards | Value | Meaning |
|---|---|---|---|
| INTERRUPT | Shade (11) | 1 | On the opponent's play, play this from hand to cancel that card's effect. The Shade joins your Line, gains its Glow and Wards you. |
| UNSTOPPABLE | Myth (13) | 1 | Cannot be interrupted. |
| STOP_TIME | Signal (16) | 1 | After it resolves, play 1 more card this turn (no extra draw). |
| UNIQUE | Oddity (5), First Light | 1 | At most one Unique card in your Line. First Light is one per game. |
| NORMAL | Muse, Tide, Sealed (54) | 0 | No timing rule. |

- **Oddity Glow 1 -> 2.** No other Glow or effect changed. The second player still starts with 2 Glow.
- **Sealed cards are unchanged and were not tuned:** 1 Glow, no effect, NORMAL.

## Resolution: which one works
Each play goes through these steps in order:

1. **Legality.** Unique is checked here; a second Unique card cannot be played at all.
2. **Placement.** The card goes on your Line. This opens the opponent's Interrupt window, unless the card is UNSTOPPABLE.
3. **Interrupt.** It resolves first (last in, first out) and cancels the card's effect.
   - The card's printed Glow and its basic +1 chain bonus still count.
   - An Interrupt cannot itself be interrupted.
4. **Resolve.** Glow, then chain bonus, then effect (unless cancelled). Ward blocks Dim here.
5. **Stop Time.** It grants the extra play only if it was not cancelled. Each extra play repeats steps 1-5.
6. **Score.** Win is checked, for both players: an Interrupt's Glow can win on the opponent's turn.

When two rules meet, the earlier step wins:
- Unique decides legality before anything else.
- Unstoppable beats Interrupt.
- Interrupt cancels any one effect.
- Ward blocks only Dim.

## Provenance: is playing provenance?
In v5, yes. Every game event is a record:
- a play, interrupt, resolve or score
- with turn, seat, tile and the card's sha256_16
- carrying the hash of the record before it

`provenance/game-seed7-0001.jsonl` is one simulated game of 35 records. Its hash chain verifies, and every interrupt sits between its target's play and that card's CANCELLED resolve. The Line shows the board; provenance shows how it got there.

## Lexicon
`game/lexicon/<term>.json` holds one file per word or phrase (40 terms), with `lexicon/index.json` listing them all. Each file has:
- definition, window, does, does_not
- **contrast** with its nearest terms, for example interrupt vs ward, stop_time vs draw, cancel vs dim, unique vs sealed, wild vs void
- interacts, phase in the resolution order, source
- the cards that carry the term, and their simulation numbers

## Simulation (greedy bot)
| | First seat | Avg turns | Max | Ties | Interrupts per game |
|---|---|---|---|---|---|
| v4 rules, comp 2 | 47.4% | 14.0 | 22 | 0 | - |
| **v5, comp 2, 10,000 games, seeds 7 and 8** | **52.1% / 52.7%** | **10.2** | 17 | 0 | 2.16 |

Play rate (played / drawn), from the 2,000-game tuning grid:

| Type | v4 | v5 |
|---|---|---|
| Signal | 7-11% | 80% |
| Shade | 4-10% | 59% |
| Oddity | 5-7% | 28% |
| Muse | 42-69% | 46% |
| Myth | 77-85% | 50% |
| Tide | 58-65% | 33% |
| Sealed | 0% | 0% |

Every non-sealed type is now played in at least 28% of draws.
- Games are shorter: 10 turns instead of 14.
- The first seat moved from 47% to 52%.
- Setting the second player's start to 3 Glow gives 46%. 2 Glow stays, being nearer 50.

This tells us what the bot does; only human play shows what is fun. The full grid is in `tune-v5-timing.csv`.
