"""simulate.play() with a per-card trace. Same rules, same RNG calls in the same order, so run_traced(g, t, seed)
gives the same wins as simulate.run(g, t, seed) (checked in build_v4.py). Counts per tile: drawn, played,
played by the eventual winner, chained when played, Glow gained when played, discarded."""
import collections, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rules  # noqa: E402
import simulate as S  # noqa: E402


def play(rng, target, st):
    deck = S.DECK[:]
    rng.shuffle(deck)
    hands = [[deck.pop() for _ in range(5)], [deck.pop() for _ in range(5)]]
    for h in hands:
        for c in h:
            st['drawn'][c['tile']] += 1
    lines, glow, ward = [[], []], [0, rules.COMP_GLOW], [False, False]
    plays = [[], []]
    turn = 0

    def draw(p):
        c = deck.pop()
        st['drawn'][c['tile']] += 1
        hands[p].append(c)

    while True:
        p, o = turn % 2, 1 - turn % 2
        ward[p] = False
        for _ in range(2):
            if deck:
                draw(p)
        if not hands[p]:
            if not deck and not hands[o]:
                w = 0 if glow[0] > glow[1] else 1 if glow[1] > glow[0] else None
                return w, turn, plays
            turn += 1
            continue
        best = max(hands[p], key=lambda c: S.value(c, lines[p], ward[o], glow[o])[0])
        hands[p].remove(best)
        gain = S.value(best, lines[p], ward[o], glow[o])[1]
        st['chained'][best['tile']] += S.chains(best, lines[p][-1] if lines[p] else None)
        st['gain'][best['tile']] += gain
        glow[p] += gain
        e = best['effect']
        if e == 'DRAW':
            for _ in range(best['n']):
                if deck:
                    draw(p)
        elif e == 'DIM' and not ward[o]:
            glow[o] = max(0, glow[o] - best['n'])
        elif e == 'WARD':
            ward[p] = True
        lines[p].append(best)
        plays[p].append(best['tile'])
        while len(hands[p]) > 7:
            d = min(hands[p], key=lambda c: c['glow'])
            hands[p].remove(d)
            st['discarded'][d['tile']] += 1
        if glow[p] >= target:
            return p, turn, plays
        if turn > 400:
            raise RuntimeError('game did not end')
        turn += 1


def run_traced(games=5000, target=21, seed=1):
    rng = random.Random(seed)
    st = {k: collections.Counter() for k in ('drawn', 'played', 'won', 'chained', 'gain', 'discarded')}
    wins = [0, 0]
    for _ in range(games):
        w, _, plays = play(rng, target, st)
        for p in (0, 1):
            for t in plays[p]:
                st['played'][t] += 1
                st['won'][t] += (w == p)
        if w is not None:
            wins[w] += 1
    return wins, st
