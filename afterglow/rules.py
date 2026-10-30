"""Afterglow rules data: suit from art style, type from first motif. Shared by build_game.py and simulate.py."""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from carddata import CARDS, SEALED_NAME, SEALED_FLAVOR, MARKER  # noqa: E402

SUIT_OF_STYLE = {'photoreal': 'Photo', 'cartoon': 'Ink', 'sketch': 'Ink', 'anime': 'Cel'}  # anything else: Pixel
TYPE_OF_MOTIF = {
    'tentacle': 'Tide', 'slime': 'Tide',
    'gothic': 'Shade', 'vampire': 'Shade', 'demon': 'Shade', 'horror': 'Shade', 'glass': 'Shade',
    'neon': 'Signal', 'cyberpunk': 'Signal', 'city': 'Signal', 'digital': 'Signal', 'robot': 'Signal',
    'machine': 'Signal', 'steampunk': 'Signal', 'space': 'Signal', 'finance': 'Signal',
    'fantasy': 'Myth', 'fairy': 'Myth', 'dragon': 'Myth', 'royal': 'Myth', 'stars': 'Myth', 'warrior': 'Myth',
    'pet': 'Oddity', 'satire': 'Oddity', 'ink': 'Oddity',
}  # anything else: Muse
# type -> (glow, effect, n)
TYPES = {
    'Muse': (2, 'CHAIN', 2), 'Tide': (1, 'DIM', 2), 'Shade': (1, 'WARD', 0), 'Signal': (1, 'DRAW', 1),
    'Myth': (1, 'BOOST', 2), 'Oddity': (1, 'WILD', 0), 'Sealed': (1, 'NONE', 0), 'Marker': (0, 'FIRST', 0),
}
TEXT = {
    'CHAIN': 'If this chains, the chain bonus is +{n} instead of +1.', 'DIM': 'Your opponent loses {n} Glow (unless warded).',
    'WARD': 'Until your next turn, you cannot be Dimmed.', 'DRAW': 'Draw {n}.', 'BOOST': 'Gain {n} extra Glow.',
    'WILD': 'Chains with any suit.', 'NONE': 'Face down. Chains with nothing.',
    'FIRST': 'Not shuffled in. Its holder goes first; the second player starts with {n} Glow.',
}
COMP_GLOW = int(os.environ.get('COMP_GLOW', 2))


def tiles():
    return {int(r['tile']): r for r in csv.DictReader(open(os.path.join(HERE, '..', 'tiles.csv'), encoding='utf-8'))}


def licence_marks(r):
    return [m for m in r['marks_ip_text'].split(';') if m.split(':')[0] in ('brand', 'ip', 'mark')]


def cards():
    out = []
    for t, r in sorted(tiles().items()):
        sealed = bool(r['hold'])
        if t == MARKER:
            typ = 'Marker'
        elif sealed:
            typ = 'Sealed'
        else:
            first = next((m for m in r['motifs'].split(';') if m in TYPE_OF_MOTIF), None)
            typ = TYPE_OF_MOTIF.get(first, 'Muse')
        glow, eff, n = TYPES[typ]
        if eff == 'FIRST':
            n = COMP_GLOW
        name, flavor = (SEALED_NAME % t, SEALED_FLAVOR) if sealed else CARDS[t]
        out.append({
            'tile': t, 'name': name, 'type': typ, 'suit': 'Void' if sealed or typ == 'Marker' else SUIT_OF_STYLE.get(r['style'], 'Pixel'),
            'glow': glow, 'effect': eff, 'n': n, 'text': TEXT[eff].format(n=n), 'flavor': flavor,
            'sealed': sealed, 'art': None if sealed else 'tile-%02d.jpg' % t if t < 100 else 'tile-100.jpg',
            'sale': 'licence needed' if licence_marks(r) else 'ok', 'marks': licence_marks(r), 'sha256_16': r['sha256_16'],
        })
    return out
