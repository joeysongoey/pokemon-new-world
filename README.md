# Pokemon: The New World v14.0

A Pokemon-style battle game made with Python and pygame.

## Play online

Once GitHub Pages is switched on (see below), the game is at:

`https://YOUR-USERNAME.github.io/REPO-NAME/`

Click the page once to start it.

## Play on your computer

```
pip install pygame
python main.py
```

## Controls

- Mouse: click the buttons
- B: start a battle (main menu)
- A: open attacks (in battle)
- 1 to 4: choose an attack
- Esc: go back

## Healing

Click HEAL on the main menu to restore every Pokemon on your team to full HP
(fainted ones are revived). It is free and saves automatically.

## Saving

Use SAVE and LOAD on the main menu. On your computer the save goes to
`pokemon_save.json` next to the game. Online it is stored in your browser,
so it stays on that browser and device.

## How the online version works

Every time you push to the `main` branch, the GitHub Action in
`.github/workflows/deploy.yml` uses [pygbag](https://pypi.org/project/pygbag/)
to turn `main.py` into a web version and publish it to the `gh-pages` branch.

## What's new in v13.0

- **XP and levels:** your active Pokemon earns XP for every win. Each level
  gives +8 max HP and +2 attack power.
- **Coins and the Poke Mart:** win battles to earn coins, then press SHOP on
  the main menu to buy Poke Balls (20), Great Balls (50) and Ultra Balls (100).
- **Battle Tournament:** beat 4 trainers and Champion Vex in a row to win a
  trophy and coins. Your team recovers half its HP between rounds. No
  catching, no healing, and RUN becomes FORFEIT.
- **New sprites:** every wild Pokemon now has its own body shape (cats, fish,
  dragons, birds, golems, ghosts, bugs, plants, imps and star-orbs), and first
  forms are smaller than final forms.

## What's new in v14.0

- **76 new Pokemon** (numbers 67 to 142), each with its own sprite, HP, attack
  bonus, four attacks and Pokedex entry. Numbers 133 to 142 are legendary and
  mythical.
- **Rare encounters:** legendary Pokemon appear in about 1 in 500 battles each,
  and mythical ones in about 1 in 1000. Catching them is harder.
- **POKEDEX** button on the main menu: shows how many Pokemon you have caught
  and seen, lets you read entries, and is saved with your game.

- **Legendary duo:** Aetherion (Dragon/Psychic, #143) and Varkrion (Dark/Steel, #144), with their own sprites and very rare encounters.
