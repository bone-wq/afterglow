"""Greedy-bot simulation of Afterglow v5: v4's rules plus the Timing category (owner's request, 2026-10-29).
Timing keys (value in brackets):
- INTERRUPT [n]   Shade. When the opponent plays a card, you may play this from your hand at once: that card's
                  effect is cancelled (its own Glow and chain bonus still count). The Shade joins your Line
                  (its Glow counts, it does not chain) and its Ward applies.
- UNSTOPPABLE [1] Myth. Cannot be interrupted.
- STOP_TIME [n]   Signal. After it resolves, play n more cards this turn (no extra draw).
- UNIQUE [1]      Oddity: at most one in your Line. First Light: one per game (already not shuffled in).
- NORMAL [0]      Everything else, Sealed included.
Card dicts need: tile, type, suit, glow, effect, n, timing, tv. run(deck, comp, games, seed) -> stats.
"""
import collections, random

INTERRUPT_WORTH = 2   # bot interrupts when the cancelled effect is worth at least this much Glow


def chains(card, prev):
    if not prev or 'Void' in (card['suit'], prev['suit']):
        return False
    return card['suit'] == prev['suit'] or 'WILD' in (card['effect'], prev['effect'])


def allowed(card, line):
    return not (card['timing'] == 'UNIQUE' and any(c['timing'] == 'UNIQUE' for c in line))


def value(card, line, opp_warded, opp_glow):
    chain = (card['n'] if card['effect'] == 'CHAIN' else 1) if chains(card, line[-1] if line else None) else 0
    gain = card['glow'] + chain + (card['n'] if card['effect'] == 'BOOST' else 0)
    score = gain
    if card['effect'] == 'DRAW':
        score += 0.6 * card['n']
    if card['effect'] == 'DIM' and not opp_warded:
        score += 0.9 * min(card['n'], opp_glow)
    if card['effect'] == 'WARD':
        score += 0.4
    if card['timing'] == 'STOP_TIME':
        score += 1.5 * card['tv']
    return score, gain


def effect_worth(card, chained):
    e = card['effect']
    return {'DIM': card['n'], 'BOOST': card['n'], 'DRAW': card['n'],
            'CHAIN': card['n'] - 1 if chained else 0}.get(e, 0) + (2 * card['tv'] if card['timing'] == 'STOP_TIME' else 0)


def play(rng, deck0, comp, target, st, log=None):
    emit = log.append if log is not None else (lambda e: None)
    deck = deck0[:]
    rng.shuffle(deck)
    hands = [[deck.pop() for _ in range(5)], [deck.pop() for _ in range(5)]]
    for h in hands:
        for c in h:
            st['drawn'][c['tile']] += 1
    lines, glow, ward = [[], []], [0, comp], [False, False]
    plays = [[], []]

    def draw(p):
        c = deck.pop()
        st['drawn'][c['tile']] += 1
        hands[p].append(c)

    def put(p, o, card):
        """Play card for p; o may interrupt. Returns True if the game ended."""
        emit({'turn': turn, 'seat': p, 'event': 'play', 'tile': card['tile']})
        prev = lines[p][-1] if lines[p] else None
        ch = chains(card, prev)
        gain = value(card, lines[p], ward[o], glow[o])[1]
        effect_on = True
        if card['timing'] != 'UNSTOPPABLE' and effect_worth(card, ch) >= INTERRUPT_WORTH:
            sh = next((c for c in hands[o] if c['timing'] == 'INTERRUPT'), None)
            if sh:
                hands[o].remove(sh)
                lines[o].append(sh)
                plays[o].append(sh['tile'])
                glow[o] += sh['glow']
                ward[o] = True
                st['interrupts'][sh['tile']] += 1
                st['interrupted'][card['tile']] += 1
                emit({'turn': turn, 'seat': o, 'event': 'interrupt', 'tile': sh['tile'], 'target': card['tile'], 'glow': sh['glow']})
                effect_on = False
                if card['effect'] == 'BOOST':
                    gain -= card['n']
                if card['effect'] == 'CHAIN' and ch:
                    gain -= card['n'] - 1
        st['chained'][card['tile']] += ch
        emit({'turn': turn, 'seat': p, 'event': 'resolve', 'tile': card['tile'], 'glow': gain, 'chained': ch,
              'effect': card['effect'] if effect_on else 'CANCELLED'})
        st['gain'][card['tile']] += gain
        glow[p] += gain
        e = card['effect']
        if effect_on and e == 'DRAW':
            for _ in range(card['n']):
                if deck:
                    draw(p)
        elif effect_on and e == 'DIM' and not ward[o]:
            glow[o] = max(0, glow[o] - card['n'])
        elif e == 'WARD':
            ward[p] = True
        lines[p].append(card)
        plays[p].append(card['tile'])
        emit({'turn': turn, 'event': 'score', 'glow': list(glow)})
        return glow[p] >= 21 or glow[o] >= 21, (card['tv'] if effect_on and card['timing'] == 'STOP_TIME' else 0)

    turn = 0
    while True:
        p, o = turn % 2, 1 - turn % 2
        ward[p] = False
        for _ in range(2):
            if deck:
                draw(p)
        extra = 1
        while extra > 0:
            extra -= 1
            options = [c for c in hands[p] if allowed(c, lines[p])]
            if not options:
                break
            best = max(options, key=lambda c: value(c, lines[p], ward[o], glow[o])[0])
            hands[p].remove(best)
            over, more = put(p, o, best)
            if over:
                w = p if glow[p] >= 21 else o
                return w, turn, plays
            extra += more
        if not hands[p] and not deck and not hands[o]:
            return (0 if glow[0] > glow[1] else 1 if glow[1] > glow[0] else None), turn, plays
        while len(hands[p]) > 7:
            d = min(hands[p], key=lambda c: c['glow'])
            hands[p].remove(d)
            st['discarded'][d['tile']] += 1
        if turn > 400:
            raise RuntimeError('game did not end')
        turn += 1


def run(deck, comp, games=5000, seed=1):
    rng = random.Random(seed)
    st = {k: collections.Counter() for k in
          ('drawn', 'played', 'won', 'chained', 'gain', 'discarded', 'interrupts', 'interrupted')}
    wins, ties, turns = [0, 0], 0, []
    for _ in range(games):
        w, t, plays = play(rng, deck, comp, 21, st)
        for q in (0, 1):
            for tl in plays[q]:
                st['played'][tl] += 1
                st['won'][tl] += (w == q)
        if w is None:
            ties += 1
        else:
            wins[w] += 1
        turns.append(t + 1)
    return {'wins': wins, 'ties': ties, 'avg_turns': sum(turns) / games, 'max_turns': max(turns), 'st': st}
