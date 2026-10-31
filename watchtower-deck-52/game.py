"""Keep the Ledger: the Watchtower deck's game. Rules engine plus a simulator for checking them.

One standard 52-card deck. The Lake flips events; the keeper answers them with the suit that follows in the cycle
Watch -> Check -> Load -> Record -> Watch. Rules are in RULES.md; this file is the reference implementation.
"""
import random

ANSWERS = {"S": "H", "H": "D", "D": "C", "C": "S"}  # event suit -> suit that answers it
VALUE = {"A": 1, "J": 11, "Q": 12, "K": 13} | {str(n): n for n in range(2, 11)}
HAND, LOSE_AT = 7, 8  # tuned by simulation: hand 5 won 12%, hand 7 wins about 57% (see RULES.md)


def deck():
    return [(s, r) for s in "SHDC" for r in ["A"] + [str(n) for n in range(2, 11)] + ["J", "Q", "K"]]


def answer(hand, event):
    """The keeper's greedy choice: smallest single card, else smallest pair, else a King. None if no answer."""
    s, r = event
    need, suit = VALUE[r], ANSWERS[s]
    ok = sorted((c for c in hand if c[0] == suit and c[1] != "K"), key=lambda c: VALUE[c[1]])
    for c in ok:
        if VALUE[c[1]] >= need:
            return [c]
    best = None
    for i in range(len(ok)):
        for j in range(i + 1, len(ok)):
            t = VALUE[ok[i][1]] + VALUE[ok[j][1]]
            if t >= need and (best is None or t < best[0]):
                best = (t, [ok[i], ok[j]])
    if best:
        return best[1]
    kings = [c for c in hand if c[1] == "K"]
    return kings[:1] or None


def legal(play, event):
    s, r = event
    if len(play) == 1 and play[0][1] == "K":
        return True
    return (1 <= len(play) <= 2 and all(c[0] == ANSWERS[s] and c[1] != "K" for c in play)
            and sum(VALUE[c[1]] for c in play) >= VALUE[r])


def play(seed, trace=None):
    """One solo game. Returns dict(result, ledger, unaccounted, rounds, blips)."""
    rng = random.Random(seed)
    d = deck()
    rng.shuffle(d)
    hand, ledger, unacc, blips, rounds = [d.pop() for _ in range(HAND)], [], [], [], 0
    while d:
        rounds += 1
        ev = d.pop()
        if ev[1] == "A":  # The Blip: the Lake read empty but it was all there
            blips.append(ev)
        else:
            p = answer(hand, ev)
            if p:
                assert legal(p, ev)
                for c in p:
                    hand.remove(c)
                ledger += [ev] + p
            else:
                unacc.append(ev)
        # Read-back: a Queen in hand may recover one unaccounted event, if it isn't needed this round
        q = next((c for c in hand if c[1] == "Q"), None)
        if q and unacc:
            hand.remove(q)
            ledger += [q, unacc.pop()]
        while len(hand) < HAND and d:
            hand.append(d.pop())
        if trace is not None:
            trace.append(len(hand) + len(d) + len(ledger) + len(unacc) + len(blips))
        if len(unacc) >= LOSE_AT:
            return {"result": "lost", "ledger": len(ledger), "unaccounted": len(unacc), "rounds": rounds, "blips": len(blips)}
    return {"result": "won", "ledger": len(ledger), "unaccounted": len(unacc), "rounds": rounds, "blips": len(blips)}


def win_rate(n=2000, start=0):
    games = [play(s) for s in range(start, start + n)]
    return sum(g["result"] == "won" for g in games) / n, games


if __name__ == "__main__":
    for seed in (7, 8):
        print(seed, play(seed))
    w, games = win_rate()
    print(f"win rate over 2000 seeds: {w:.1%}; mean ledger {sum(g['ledger'] for g in games) / len(games):.1f}")
