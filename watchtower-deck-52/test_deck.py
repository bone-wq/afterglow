import hashlib
"""Checks for the Watchtower deck and Keep the Ledger. Run: python test_deck.py  (exit 0 = all pass)."""
import json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from cards import CARDS, RANKS, SUITS  # noqa: E402
import game  # noqa: E402
from build_deck import rows  # noqa: E402

R = []


def check(name, ok):
    R.append((name, bool(ok)))


cards = rows()
check("52 cards", len(cards) == 52)
check("52 unique ids", len({c["card_id"] for c in cards}) == 52)
check("13 ranks in each of 4 suits", all([c[0] for c in CARDS[s]] == RANKS for s in "SHDC") and len(SUITS) == 4)
check("suits differ", len({s[3] for s in SUITS}) == 4)
check("five layers on every card", all(c[k].strip() for c in cards for k in ("principle", "naming", "tradeoffs", "practice", "journal")))
check("titles unique", len({c["title"] for c in cards}) == 52)
check("cycle is one loop through all suits",
      len(set(game.ANSWERS.values())) == 4 and all(k != v for k, v in game.ANSWERS.items())
      and (lambda s: [s := game.ANSWERS[s] for _ in range(4)][-1])("S") == "S")
check("engine deck matches the cards", sorted(game.deck()) == sorted((c["card_id"][-1], c["card_id"][:-1]) for c in cards))

text = json.dumps(cards, ensure_ascii=False)
deny = [r"[0-9a-f]{32}", r"\bbucket\b", r"[A-Z]:\\", r"\.house", r"AppData", r"secret\s*[:=]", r"token\s*[:=]", r"sk-ant-",
        r"d1/database", r"@\w+\.\w+"]
check("scrub-clean (no IDs, storage names, paths, secrets, emails)", not [d for d in deny if re.search(d, text, re.I)])
held = {"498e72b7537542866c5ed8dcd09e581fc5ae0a90aeb6e6594e6298103939a939", "d63d71f407ad92113aa5b858936038d68e0fde0a7ed8b8a03a4fea2c2eab80d5"}  # private words, kept as sha256 so the list itself stays private
check("no held words", not {hashlib.sha256(w.encode()).hexdigest() for w in re.findall(r"[a-z]+", text.lower())} & held)
quotes = re.findall(r"\"([^\"]+)\"", " ".join(c["journal"] for c in cards))
check("owner quotes are exact", set(quotes) <= {"we need a memalloc watch tower", "the inter task logic please watch",
                                                 "Yes, add it", "record everything please", "varsity-squad-session",
                                                 "(thats high praise)"})

# rules engine
check("King answers anything", all(game.legal([("C", "K")], (s, r)) for s in "SHDC" for r in ["2", "Q", "K"]))
check("wrong suit is illegal", not game.legal([("S", "10")], ("S", "2")))
check("too low is illegal", not game.legal([("H", "3")], ("S", "9")))
check("pair adds up", game.legal([("H", "4"), ("H", "5")], ("S", "9")) and not game.legal([("H", "4"), ("H", "4")], ("S", "9")))
check("three cards is illegal", not game.legal([("H", "2"), ("H", "3"), ("H", "4")], ("S", "5")))
cons = True
for seed in range(300):
    t = []
    game.play(seed, trace=t)
    cons &= all(n == 52 for n in t)
check("all 52 cards accounted for after every round (300 games)", cons)
check("same seed, same game", game.play(42) == game.play(42))
w, games = game.win_rate(1000)
check("win rate is a fair fight (40-75%)", 0.40 <= w <= 0.75)
check("games end: won or lost at 8", all(g["result"] == "won" or g["unaccounted"] >= game.LOSE_AT for g in games))

bad = [n for n, ok in R if not ok]
print(f"{len(R) - len(bad)}/{len(R)} passed" + (f"; failed: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
