"""Run the greedy-bot simulation on cards-v5.json. Usage: python afterglow/run_sim.py [games] [seed]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import simulate_v5 as S  # noqa: E402
d = json.load(open(os.path.join(HERE, 'cards-v5.json'), encoding='utf-8'))
cards = d['cards'] if isinstance(d, dict) else d
play = [dict(c, timing=c['timing']['key'], tv=c['timing']['value']) for c in cards if c['type'] != 'Marker']
games, seed = (int(a) for a in (sys.argv[1:] + ['10000', '7'][len(sys.argv) - 1:])[:2])
r = S.run(play, 2, games, seed)
print('games', games, 'seed', seed, 'first seat wins %.1f%%' % (100.0 * r['wins'][0] / games), {k: v for k, v in r.items() if k != 'wins'})
