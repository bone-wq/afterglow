"""Build the Watchtower deck into JSON plus Sheets (xlsx), SQL (SQLite + .sql) and SPSS (.sav). Every file read back.

Usage: python build_deck.py --out <new folder>
"""
import argparse, contextlib, hashlib, json, pathlib, sqlite3, sys

import pandas as pd
import pyreadstat

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from cards import CARDS, RANKS, SUITS  # noqa: E402
import game  # noqa: E402

SUIT = {s[0]: s for s in SUITS}


def rows():
    out = []
    for code, name, sym, theme, _ in SUITS:
        for rank, title, principle, tradeoff, practice, journal in CARDS[code]:
            ans = [k for k, v in game.ANSWERS.items() if v == code][0]
            out.append({
                "card_id": rank + code, "glyph": rank + sym, "suit": name, "suit_symbol": sym, "suit_theme": theme,
                "rank": rank, "value": game.VALUE[rank], "title": title,
                "principle": principle, "naming": title, "tradeoffs": tradeoff, "practice": practice, "journal": journal,
                "answers": SUIT[ans][3], "answered_by": SUIT[game.ANSWERS[code]][3],
                "power": {"A": "Blip: as an event, needs no answer", "K": "Head of the Chain: answers any event",
                          "Q": "Read-back: recover one Unaccounted card"}.get(rank, ""),
            })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    out = pathlib.Path(ap.parse_args().out)
    out.mkdir(parents=True, exist_ok=False)
    cards = rows()
    w, _ = game.win_rate(1000)
    deck = {"title": "The Watchtower", "set_code": "watchtower-52", "game": "Keep the Ledger (see RULES.md)",
            "learned_from": "the Memalloc watchtower session, 2026-10-29 to 2026-10-31",
            "suits": [{"code": c, "name": n, "symbol": s, "theme": t, "about": a} for c, n, s, t, a in SUITS],
            "cycle": {SUIT[k][3]: SUIT[v][3] for k, v in game.ANSWERS.items()},
            "hand": game.HAND, "lose_at": game.LOSE_AT, "simulated_win_rate_1000": round(w, 3),
            "total_cards": len(cards), "cards": cards}
    (out / "watchtower-deck-52.json").write_text(json.dumps(deck, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    df = pd.DataFrame(cards)
    df.to_csv(out / "watchtower-deck-52.csv", index=False, encoding="utf-8")
    with pd.ExcelWriter(out / "watchtower-deck-52.xlsx") as x:
        df.to_excel(x, sheet_name="cards", index=False)
        pd.DataFrame(deck["suits"]).to_excel(x, sheet_name="suits", index=False)
        pd.DataFrame([{"rule": l} for l in (pathlib.Path(__file__).parent / "RULES.md").read_text(encoding="utf-8").splitlines()]
                     ).to_excel(x, sheet_name="rules", index=False)
    cols = list(df.columns)
    create = "CREATE TABLE cards (" + ", ".join(f"{c} {'INTEGER' if c == 'value' else 'TEXT'}" for c in cols) + ", PRIMARY KEY (card_id));"
    with contextlib.closing(sqlite3.connect(out / "watchtower-deck-52.db")) as con, con:
        con.execute(create)
        con.executemany(f"INSERT INTO cards VALUES ({','.join('?' * len(cols))})", [tuple(r) for r in df.itertuples(index=False)])
    lit = lambda v: str(v) if isinstance(v, int) or hasattr(v, "item") else "'" + str(v).replace("'", "''") + "'"
    sql = ["-- The Watchtower deck, 52 cards", "BEGIN;", create]
    sql += [f"INSERT INTO cards VALUES ({', '.join(lit(v) for v in r)});" for r in df.itertuples(index=False)] + ["COMMIT;"]
    (out / "watchtower-deck-52.sql").write_text("\n".join(sql) + "\n", encoding="utf-8")
    pyreadstat.write_sav(df, str(out / "watchtower-deck-52.sav"),
                         column_labels={c: c.replace("_", " ").capitalize() for c in cols})

    # read back
    with contextlib.closing(sqlite3.connect(out / "watchtower-deck-52.db")) as con:
        db = con.execute("SELECT count(*) FROM cards").fetchone()[0]
    with contextlib.closing(sqlite3.connect(":memory:")) as con:
        con.executescript((out / "watchtower-deck-52.sql").read_text(encoding="utf-8"))
        script = [r[0] for r in con.execute("SELECT journal FROM cards ORDER BY rowid")]
    rb = {"json": len(json.loads((out / "watchtower-deck-52.json").read_text(encoding="utf-8"))["cards"]),
          "csv": len(pd.read_csv(out / "watchtower-deck-52.csv")), "xlsx": len(pd.read_excel(out / "watchtower-deck-52.xlsx")),
          "sav": len(pyreadstat.read_sav(str(out / "watchtower-deck-52.sav"))[0]), "sqlite": db, "sql_script": len(script)}
    same = script == list(df["journal"]) and pyreadstat.read_sav(str(out / "watchtower-deck-52.sav"))[0]["journal"].tolist() == list(df["journal"])
    files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir())}
    (out / "manifest.json").write_text(json.dumps({"readback": rb, "text_identical": same, "files": files}, indent=2))
    print(json.dumps({"readback": rb, "text_identical": same, "win_rate": deck["simulated_win_rate_1000"]}))
    return 0 if all(v == 52 for v in rb.values()) and same else 1


if __name__ == "__main__":
    sys.exit(main())
