# Afterglow — deck 1 (Grok tiles 1–100)

One card per image, 100 cards. A first draft: the simulation shows the rules end and seat order is close to even.
It does not show the game is fun.

## Concept
A city after dark. Each player builds a **Line**: cards laid in a row, never taken back. Light given off by the
Line is **Glow**. First to 21 Glow wins.

## Suits come from the art style
| Suit | Style in `tiles.csv` | Cards |
|---|---|---|
| Photo | photoreal | 34 |
| Ink | cartoon, sketch | 19 |
| Cel | anime | 16 |
| Pixel | digital, 3d, pixel, abstract, graphic, neon | 16 |
| Void | sealed cards and First Light | 15 |

## Types come from the first motif
| Type | Motifs | Glow | Effect | Cards |
|---|---|---|---|---|
| Muse | none listed, portrait, beach, comic, sport… | 2 | **Chain 2**: if it chains, the bonus is +2 | 30 |
| Signal | neon, cyberpunk, city, digital, robot, space… | 1 | **Draw 1** | 16 |
| Myth | fantasy, fairy, dragon, royal, stars, warrior | 1 | **Boost 2**: gain 2 more | 13 |
| Shade | gothic, vampire, demon, horror, glass | 1 | **Ward**: can't be Dimmed until your next turn | 11 |
| Tide | tentacle, slime | 1 | **Dim 2**: opponent loses 2 | 10 |
| Oddity | pet, satire, ink | 1 | **Wild**: chains with any suit | 5 |
| Sealed | the 14 held tiles | 1 | Face down; chains with nothing | 14 |
| Marker | First Light (tile 41) | — | Decides who goes first | 1 |

## Turn
1. Start: shuffle 99 cards (First Light stays out). Each player draws 5. First Light's holder goes first;
   the second player starts with **2 Glow**.
2. Each turn: draw 2, play one card to the end of your Line, resolve it, discard down to 7.
3. **Chain**: if the card's suit matches the previous card in your Line, gain +1 (Muse: +2). Wild chains with
   any suit; Void never chains.
4. Win at 21 Glow. If the deck and both hands run out, the higher Glow wins.

## Simulation (greedy bot, 10,000 games each)
| Second player starts with | First wins | Second wins | Avg turns |
|---|---|---|---|
| 0 Glow | 70.4% | 29.6% | 14.5 |
| 1 Glow | 58.5% | 41.5% | 14.3 |
| **2 Glow (chosen)** | **47.4%** | **52.6%** | **14.0** |
| 3 Glow | 33.7% | 66.3% | 13.6 |

No ties, every game ended (max 22 turns).

## Sealed cards
Tiles 4, 27, 31, 47, 63, 64, 74, 78, 79, 83, 86, 87, 91, 98 stay in the count as **Sealed No. N**. Their art is not
shown and their text says nothing about the image. They are held for privacy.

## Sale
23 cards carry someone else's brand, character, signature or watermark (`marks_ip_text`). They are marked
**licence needed**: not sold unless there is a licence for that mark. No licences are recorded.
