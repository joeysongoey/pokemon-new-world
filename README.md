# Pokemon: The New World v18.0

A Pokemon-style battle game made with Python and pygame.

## Play online

Once GitHub Pages is switched on (see below), the game is at:

https://joeysongoey.github.io/pokemon-new-world/

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

To move a save between your computer and the browser, press EXPORT CODE and
then IMPORT CODE on the other one. Online, the code is shown in a box to copy
and paste. On a computer, it goes in `pokemon_save_code.txt` next to the game.

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

## What's new in v18.0

- **Bond system:** Pokemon gain bond for every battle they win. Every 20 points
  is a heart (shown on the team screen) with its own line of dialogue. At 3 hearts
  a Pokemon can hang on with 1 HP. At 5 hearts it learns its own Bond Strike move.
- **Titles:** Pokemon earn titles like Void Hunter (beat 10 Void Pokemon),
  Flame Champion (Fire Type Master), Glitch Survivor (win under 10% HP),
  Boss Breaker, Champion and Best Friend. The title shows next to their name.
  Tap TITLE on the team screen to change it.
- **Move Mastery:** using a move 20 times masters it, adding +10 power, a gold
  star and a gold sparkle when it hits.
- **CHALLENGES** button on the menu:
  - **Type Masters:** beat 3 trainers of one type (18 types) for coins, a badge,
    a title and a SHINY Pokemon of that type.
  - **Boss Rematches:** fight bosses you've beaten again. They get stronger
    every time, with bonus coins for winning.
- **Secret Areas** on the FLY screen: Hidden Cave (win 15 battles), Abandoned Lab
  (catch 25 kinds) and Mysterious Dimension (win the Battle Tournament). Each has
  its own wild Pokemon.
- **Legendary encounters:** each secret area has its own legendary, with a
  special introduction screen. The Lab and the Dimension have a riddle to solve first.
- **Duo Legendary Battles:** in the Mysterious Dimension, Aetherion and Varkrion
  can appear together. Beat or catch one and the other takes its power.

## What's new in v17.2

- **EVENT CODE button** with an on-screen keyboard, so event codes work on
  iPads and phones that block pop-up boxes. A real keyboard works too.

## What's new in v17.1

- **Aura Brawler (#346), an event-only Pokemon.** It never appears in battles or
  tournaments. Enter the secret code with the EVENT CODE button to get it. Your save stays
  as it is, and a save code exported afterwards keeps Aura Brawler.

## What's new in v17.0

- **New moves by level:** every Pokemon learns a stronger move at Lv 15, 25, 35, 50 and 70.
  Dual types take turns between their two types.
- With four moves already, the new move replaces the weakest one.
- 110 new moves, with power from 45 at Lv 15 up to 80 at Lv 70.
- The team screen shows the level of the next new move.
- Game files now get a new name on every update, so browsers load the latest version.

## What's new in v16.2

- The starting team now uses new original pixel-art creatures for Lucario, Luxray, Suicune, Gyarados, Morpeko, Dialga and both MissingNo. (Flame is unchanged).

- **Omni-Dex sprites:** 21 sprites cut from the Omni-Dex screenshot now appear in the game
  for Embercub, Blazepaw, Pyroclaw, Frostbit, Glacieron, Cryowraith, Leaflet, Thornox,
  Floragon, Mechling, Ironclast, Titanforge, Rockruffle, Cragoyle, Terradon, Starlingo,
  Galaxion, Lumidrake, Shadelet, Hauntalon and Dreadgeist. The pictures are in `sprites/`.

## What's new in v16.1

- **200 new Pokemon, #146 to #345**, bringing the Pokedex to 345. Every one has
  a type, stats, four moves and a Pokedex entry. Their entries and moves are
  short placeholders you can rewrite.
- Stats for #246 to #345 come from the stats file. Stats for #146 to #245 are
  placeholder values.
- Duplicate names were renamed: Tidewyrm, Frostmaw, Cragwing, Gravewing,
  Toxmite, Glacyowl, Bloomisk, Sporemantis, Stormrake, Mossox, Seismotusk,
  Magmaut and Scorchclaw.

## What's new in v16.0

- **Evolution:** Pokemon #1 to #45 come in families of three. Stage 1 evolves
  at Lv 16 and stage 2 at Lv 32, getting more HP, power and new moves.
- **Regions and FLY:** fly between 10 regions. Each one has its own colours
  and its own common Pokemon types.
- **Battle items:** buy Potions, Super Potions and Revives in the shop, then
  press ITEMS in battle. Using one takes your turn. You start with 3 Potions.
- **Shiny Pokemon:** a 1 in 200 chance of a different colour, marked with a
  gold star. Caught shinies get a star in the Pokedex.
- **Elite Cup:** a harder second tournament with five Lv 40 to 62 trainers.
  It unlocks after you win the Battle Tournament.
- **Eclipsar returns** from v10.1 as Mythical Pokemon #145 (0.3% per battle).
- **Types shown in battle** as coloured labels, and attack buttons are
  coloured by type with a x2 or x0.5 hint.
- **Smarter enemies** that usually pick their most effective move.
- **TYPE CHART** screen on the main menu and in the Pokedex.
- **Pokedex entries** for all of the original 66 Pokemon.
- **Export and import save codes.**
- NYSTRIA stays at a 5% chance per battle.

## What's new in v15.0

- **Type effectiveness** in every battle, for your attacks and the enemy's.
  - Super effective moves do 2x damage, and 4x when both of the defender's types are weak.
  - Not very effective moves do 0.5x, and some matchups have no effect at all.
  - Battle messages show SUPER EFFECTIVE!, Not very effective... or It had no effect!
- Uses the standard 18-type chart, with Ice kept super effective against Fire.

## What's new in v14.0

- **76 new Pokemon** (numbers 67 to 142), each with its own sprite, HP, attack
  bonus, four attacks and Pokedex entry. Numbers 133 to 142 are legendary and
  mythical.
- **Rare encounters:** legendary Pokemon appear in about 1 in 500 battles each,
  and mythical ones in about 1 in 1000. Catching them is harder.
- **POKEDEX** button on the main menu: shows how many Pokemon you have caught
  and seen, lets you read entries, and is saved with your game.

- **Legendary duo:** Aetherion (Dragon/Psychic, #143) and Varkrion (Dark/Steel, #144), with their own sprites and very rare encounters.
