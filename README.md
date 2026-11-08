# Pokemon: The New World v12.0

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
