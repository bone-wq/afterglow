# Afterglow

An original card game from Bone & Saucer Labs. A city after dark: each player builds a **Line** of cards that is never taken back. The light a Line gives off is **Glow**, and the first player to 21 Glow wins.

- **Rules:** `afterglow/game.md`, plus `afterglow/game-v5.md` for the timing rules (Interrupt, Unstoppable, Stop Time, Unique) and the order in which effects resolve.
- **Cards:** `afterglow/cards-v5.json`, and one nested JSON per card in `afterglow/cards-v5/`.
- **Wireframes:** `afterglow/wireframes-v5/index.html` shows one SVG per card, with its connection points.
- **Lexicon:** `afterglow/lexicon/` has one JSON per game term, with the terms it contrasts with.
- **Lab talk:** `afterglow/lab-talk/` explains the house shorthand.
- **Canon:** `afterglow/canon/` holds the lore entries, each hash-linked to the one before.
- **Provenance:** `afterglow/provenance/` holds a hash-linked log of one played game.
- **Simulation:** run `python afterglow/run_sim.py 10000 7` for the greedy-bot simulation. Over 10,000 games the first seat wins 52.1% on seed 7 and 52.7% on seed 8, and a game lasts about 10 turns. That shows the rules hold together, not that the game is balanced.

Card art is not in this repository. Fourteen cards are Sealed and show no art anywhere.

## Shoutout to the models
Afterglow was made by people and models together:
- **Grok (xAI)** made the images the deck is built on: one card per image.
- **ComfyUI** rendered the frames, card backs and sealed faces.
- **Claude (Anthropic)** wrote the rules, the simulator, the card data, the wireframes, the lexicon and the lab-talk glossary, and drafted canon with the owner.
- **Gemma, Gemini and Qwen** belong to the house's wider model triad and pipeline work. They are thanked here as part of the crew, though they didn't write this repository.

Every decision on record is the owner's: Matthew Joseph Lansing (MatthewLLTS).

## Rights
© 2026 Bone & Saucer Labs LLC. All rights reserved unless a license file says otherwise.
