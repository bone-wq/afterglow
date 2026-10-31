# Keep the Ledger

The Watchtower deck's game. It's for one keeper against the Lake (PvE), or two keepers against each other (PvP). It plays with this deck or with any standard 52-card deck.

## The cycle
Every event is answered by the suit that follows it. This is the pipeline the deck was learned from:

| The Lake flips | You answer with | Because |
|---|---|---|
| ♠ Watch: something changed | ♥ Check | what you see, you check |
| ♥ Check: something needs verifying | ♦ Load | what you check, you load and read back |
| ♦ Load: something was written | ♣ Record | what you load, you record in the chain |
| ♣ Record: the chain grew | ♠ Watch | what you record, you watch again |

Values: A = 1, 2-10 as shown, J = 11, Q = 12, K = 13.

## Solo (PvE)
1. **Setup:** shuffle, and the keeper draws **7**. The rest is the Lake.
2. **Each round:** flip the Lake's top card. That's the event.
   - **An Ace is a Blip.** The Lake read empty, but it was all there. Set it aside; no answer is needed.
   - **Otherwise, answer it** with one card of the answering suit worth at least the event, or two cards of that suit that add up to at least the event (a second check). The event and your cards go to your **Ledger**.
   - **Any King answers any event** (Head of the Chain). It's played alone.
   - **No answer?** The event goes to **Unaccounted**.
3. **Read-back:** at the end of the round, you may play a Queen of any suit to move one Unaccounted card into your Ledger.
4. **Draw back up to 7** while the Lake has cards.
5. **Lose** when 8 cards are Unaccounted (the Unaccounted Eight). **Win** if the Lake runs out first. Your score is the size of your Ledger.

## Two keepers (PvP)
- **Shared Lake:** one Lake, and each keeper holds 7.
- **Events:** keepers take turns flipping, and each answers their own event.
- **Read-back:** a Queen moves one card from **your own** Unaccounted pile.
- **Winning:** the first keeper to reach 8 Unaccounted loses. If the Lake runs out, the bigger Ledger wins, and the fewer Unaccounted breaks a tie.

## Checked by simulation
`game.py` plays solo games with a greedy keeper. It answers with the smallest single card, then the smallest pair, then a King. It plays a Queen whenever something is Unaccounted.

| Hand size | Lose at 8 | Lose at 10 | Lose at 12 |
|---|---|---|---|
| 5 | 12% | 22% | 35% |
| 6 | 33% | 50% | 66% |
| **7** | **57%** | 74% | 83% |
| 8 | 74% | 88% | 94% |

That's the share of games won over 1,000 seeds each. Hand 7 with "lose at 8" was chosen because it's close to a fair fight and keeps the Eight. `test_deck.py` checks that every move is legal and that all 52 cards are accounted for after every round.

## Each card teaches
The five cookbook layers are on every card:
- **principle:** the idea.
- **naming:** its title.
- **tradeoffs:** what it costs.
- **practice:** what to do.
- **journal:** what actually happened in the session it came from.

The journal lines are facts from the watchtower session's logs and event chain, kept public-safe.
