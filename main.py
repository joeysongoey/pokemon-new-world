import asyncio
import functools
import json
import pygame
import random
import sys
import math

# True when running in a web browser (via pygbag)
WEB = sys.platform == "emscripten"

pygame.init()

# ==========================================
# SETTINGS
# ==========================================

WIDTH, HEIGHT = 1000, 700
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 560
FPS = 60

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
screen = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Pokemon: The New World v13.0")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 22, bold=True)
SMALL = pygame.font.SysFont("arial", 16, bold=True)
BIG = pygame.font.SysFont("arial", 36, bold=True)

WHITE = (245, 245, 255)
BLACK = (15, 15, 25)
GOLD = (255, 210, 70)
GREEN = (65, 210, 100)
RED = (230, 65, 75)
BLUE = (35, 75, 145)
DARK = (18, 27, 55)
BORDER = (105, 145, 205)

SUN_TEAM = ("Flame", "Lucario")
AVATAR_TURNS = 3
PARTY_LIMIT = 12

# ==========================================
# ORIGINAL TEAM
# ==========================================

TEAM_DATA = [
    ("Flame", 200, 20, [
        ("Flamethrower", 35), ("Fire Blast", 45),
        ("Thunder Punch", 25), ("Shadow Claw", 30)
    ]),
    ("Lucario", 180, 20, [
        ("Aura Sphere", 35), ("Dragon Pulse", 30),
        ("Flash Cannon", 35), ("Shadow Ball", 30)
    ]),
    ("Suicune", 220, 20, [
        ("Water Pulse", 35), ("Ice Beam", 35),
        ("Hydro Pump", 50), ("Aurora Beam", 25)
    ]),
    ("Gyarados", 200, 20, [
        ("Aqua Tail", 40), ("Crunch", 30),
        ("Dragon Rage", 35), ("Hydro Pump", 45)
    ]),
    ("Morpeko", 150, 20, [
        ("Thunderbolt", 35), ("Aura Wheel", 45),
        ("Crunch", 25), ("Thunder Wave", 20)
    ]),
    ("Good MissingNo", 250, 20, [
        ("Glitch Beam", 40), ("Pixel Storm", 35),
        ("Struggle", 30), ("Light Burst", 45)
    ]),
    ("Evil MissingNo", 350, 50, [
        ("Alpha Resurrection", 65), ("EXE Trooper", 55),
        ("Corrupt Beam", 60), ("Shadow Warp", 40)
    ]),
    ("Dialga", 300, 20, [
        ("Roar of Time", 55), ("Flash Cannon", 35),
        ("Dragon Claw", 35), ("Dark Pulse", 40)
    ]),
    ("Luxray", 180, 20, [
        ("Thunder Fang", 35), ("Crunch", 30),
        ("Wild Charge", 45), ("Spark", 25)
    ])
]

TEAM_TYPES = {
    "Flame": "Fire",
    "Lucario": "Fighting/Steel",
    "Suicune": "Water",
    "Gyarados": "Water/Flying",
    "Morpeko": "Electric/Dark",
    "Good MissingNo": "Glitch",
    "Evil MissingNo": "Void",
    "Dialga": "Steel/Dragon",
    "Luxray": "Electric"
}

BOSS_DATA = [
    ("Darkrai.exe", 240, 0, [
        "Dark Pulse", "Nightmare", "Shadow Strike"
    ]),
    ("Akuma", 280, 0, [
        "Glitch Blast", "Void Strike", "Dark Energy"
    ]),
    ("Vosrak", 450, 15, [
        "Shadow Burst", "Void Wave", "Dark Storm"
    ])
]

# ==========================================
# POKEDEX
# ==========================================

WILD_POKEMON = [
    (1, "Embercub", "Fire"),
    (2, "Blazepaw", "Fire"),
    (3, "Pyroclaw", "Fire"),
    (4, "Aquaffin", "Water"),
    (5, "Tidalisk", "Water"),
    (6, "Abyssurge", "Water/Dark"),
    (7, "Leaflet", "Grass"),
    (8, "Thornox", "Grass"),
    (9, "Floragon", "Grass/Dragon"),
    (10, "Voltkit", "Electric"),
    (11, "Shocklynx", "Electric"),
    (12, "Thundermaw", "Electric/Dark"),
    (13, "Frostbit", "Ice"),
    (14, "Glacieron", "Ice"),
    (15, "Cryowraith", "Ice/Ghost"),
    (16, "Rockruffle", "Rock"),
    (17, "Cragoyle", "Rock/Flying"),
    (18, "Terradon", "Ground/Dragon"),
    (19, "Shadelet", "Ghost"),
    (20, "Hauntalon", "Ghost/Flying"),
    (21, "Dreadgeist", "Ghost/Dark"),
    (22, "Mechling", "Steel"),
    (23, "Ironclast", "Steel"),
    (24, "Titanforge", "Steel/Fighting"),
    (25, "Mindimp", "Psychic"),
    (26, "Psyphantom", "Psychic/Ghost"),
    (27, "Dreamora", "Psychic/Fairy"),
    (28, "Venomite", "Poison"),
    (29, "Toxidrake", "Poison/Dragon"),
    (30, "Skyray", "Flying"),
    (31, "Stormeagle", "Flying/Electric"),
    (32, "Brawlpup", "Fighting"),
    (33, "Warfang", "Fighting/Dark"),
    (34, "Fableaf", "Fairy"),
    (35, "Lumifawn", "Fairy/Light"),
    (36, "Gloomora", "Dark"),
    (37, "Nightreign", "Dark/Dragon"),
    (38, "Bugbyte", "Bug"),
    (39, "Glitchor", "Bug/Electric"),
    (40, "Fossilisk", "Rock/Dragon"),
    (41, "Magmole", "Fire/Ground"),
    (42, "Spectrill", "Ghost/Steel"),
    (43, "Starlingo", "Cosmic"),
    (44, "Galaxion", "Cosmic/Dragon"),
    (45, "Nullvex", "Void"),
    (46, "NYSTRIA", "Void/Dragon"),
    (47, "Frolren", "Ice/Dragon"),
    (48, "Pyrovolt", "Fire/Electric"),
    (49, "Aquarion", "Water/Psychic"),
    (50, "Thornblade", "Grass/Steel"),
    (51, "Voltraze", "Electric/Dragon"),
    (52, "Glacifang", "Ice/Dark"),
    (53, "Magmanta", "Fire/Ground"),
    (54, "Phantomox", "Ghost/Steel"),
    (55, "Terraboom", "Ground/Rock"),
    (56, "Mindflare", "Psychic/Fire"),
    (57, "Venomantis", "Bug/Poison"),
    (58, "Skyrazor", "Flying/Steel"),
    (59, "Lumidrake", "Light/Dragon"),
    (60, "Abyssalon", "Water/Ghost"),
    (61, "Dreadhorn", "Dark/Fighting"),
    (62, "Starflare", "Cosmic/Fire"),
    (63, "Nullshade", "Void/Ghost"),
    (64, "Ironquake", "Steel/Ground"),
    (65, "Florawing", "Grass/Flying"),
    (66, "Chronox", "Cosmic/Steel")
]

# ==========================================
# TYPES AND MOVES
# ==========================================

TYPE_MOVES = {
    "Fire": ["Ember", "Flame Burst", "Fire Claw"],
    "Water": ["Water Pulse", "Aqua Jet", "Tidal Wave"],
    "Grass": ["Leaf Blade", "Vine Whip", "Razor Leaf"],
    "Electric": ["Spark", "Thunder Fang", "Volt Strike"],
    "Ice": ["Ice Shard", "Frost Beam", "Blizzard"],
    "Rock": ["Rock Throw", "Stone Edge", "Rock Slide"],
    "Ground": ["Mud Shot", "Earth Power", "Ground Slam"],
    "Ghost": ["Shadow Claw", "Phantom Wave", "Night Shade"],
    "Steel": ["Metal Claw", "Iron Head", "Steel Crash"],
    "Psychic": ["Confusion", "Psybeam", "Mind Blast"],
    "Poison": ["Poison Sting", "Toxic Wave", "Venom Strike"],
    "Flying": ["Gust", "Air Slash", "Sky Attack"],
    "Fighting": ["Quick Jab", "Power Strike", "Fighting Spirit"],
    "Fairy": ["Fairy Wind", "Moonbeam", "Sparkle Burst"],
    "Light": ["Light Beam", "Radiant Burst", "Sun Flash"],
    "Dark": ["Dark Pulse", "Night Slash", "Shadow Burst"],
    "Dragon": ["Dragon Breath", "Dragon Claw", "Dragon Pulse"],
    "Bug": ["Bug Bite", "Pin Missile", "Bug Buzz"],
    "Cosmic": ["Star Beam", "Meteor Strike", "Cosmic Burst"],
    "Void": ["Void Pulse", "Null Beam", "Rift Strike"]
}

TYPE_COLOURS = {
    "Fire": (255, 100, 25),
    "Water": (50, 160, 255),
    "Grass": (80, 210, 90),
    "Electric": (255, 230, 40),
    "Ice": (140, 230, 255),
    "Rock": (170, 145, 110),
    "Ground": (190, 130, 65),
    "Ghost": (160, 90, 220),
    "Steel": (180, 200, 220),
    "Psychic": (245, 100, 190),
    "Poison": (180, 65, 200),
    "Flying": (150, 210, 255),
    "Fighting": (230, 120, 70),
    "Fairy": (255, 175, 220),
    "Light": (255, 245, 150),
    "Dark": (100, 65, 110),
    "Dragon": (140, 100, 230),
    "Bug": (170, 210, 65),
    "Cosmic": (130, 140, 255),
    "Void": (100, 40, 150),
    "Glitch": (100, 255, 200)
}

MOVE_TYPES = {}

for type_name, move_names in TYPE_MOVES.items():
    for move_name in move_names:
        MOVE_TYPES[move_name] = type_name

MOVE_TYPES.update({
    "Flamethrower": "Fire",
    "Fire Blast": "Fire",
    "Thunder Punch": "Electric",
    "Shadow Claw": "Ghost",
    "Aura Sphere": "Fighting",
    "Dragon Pulse": "Dragon",
    "Flash Cannon": "Steel",
    "Shadow Ball": "Ghost",
    "Water Pulse": "Water",
    "Ice Beam": "Ice",
    "Hydro Pump": "Water",
    "Aurora Beam": "Ice",
    "Aqua Tail": "Water",
    "Crunch": "Dark",
    "Dragon Rage": "Dragon",
    "Thunderbolt": "Electric",
    "Aura Wheel": "Electric",
    "Thunder Wave": "Electric",
    "Glitch Beam": "Glitch",
    "Pixel Storm": "Cosmic",
    "Struggle": "Normal",
    "Light Burst": "Light",
    "Alpha Resurrection": "Void",
    "EXE Trooper": "Void",
    "Corrupt Beam": "Void",
    "Shadow Warp": "Ghost",
    "Roar of Time": "Dragon",
    "Dragon Claw": "Dragon",
    "Dark Pulse": "Dark",
    "Thunder Fang": "Electric",
    "Wild Charge": "Electric",
    "Spark": "Electric",
    "Nightmare": "Dark",
    "Shadow Strike": "Ghost",
    "Glitch Blast": "Glitch",
    "Void Strike": "Void",
    "Dark Energy": "Dark",
    "Shadow Burst": "Dark",
    "Void Wave": "Void",
    "Dark Storm": "Dark"
})


def primary_type(type_text):
    return type_text.split("/")[0]


def get_move_type(move):
    return MOVE_TYPES.get(move, "Normal")


def wild_moves(type_text):
    result = []
    for t in type_text.split("/"):
        for move in TYPE_MOVES.get(t, ["Tackle"]):
            result.append((move, random.randint(25, 40)))
    return result[:3]


# ==========================================
# CREATURES
# ==========================================

class Creature:
    def __init__(self, name, max_hp, moves, level=1, bonus=0):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.moves = moves
        self.level = level
        self.bonus = bonus
        self.types = "Unknown"
        self.pokedex_number = None
        self.xp = 0

    @property
    def fainted(self):
        return self.hp <= 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)


# ==========================================
# XP AND LEVELS
# ==========================================

MAX_LEVEL = 100


def xp_needed(level):
    return 10 + level * 10


def xp_reward(enemy):
    if enemy.types == "Boss":
        return 150
    if enemy.name == "NYSTRIA":
        return 250
    return 8 + enemy.level * 6


def gain_xp(creature, amount):
    """Adds XP and returns a list of level-up messages."""
    messages = []
    creature.xp += amount

    while (creature.level < MAX_LEVEL
           and creature.xp >= xp_needed(creature.level)):
        creature.xp -= xp_needed(creature.level)
        creature.level += 1
        creature.max_hp += 8
        creature.hp = min(creature.max_hp, creature.hp + 8)
        creature.bonus += 2
        messages.append(f"{creature.name} grew to Lv {creature.level}!")

    if creature.level >= MAX_LEVEL:
        creature.xp = 0

    return messages


# ==========================================
# COINS AND SHOP
# ==========================================

START_COINS = 100

SHOP_PRICES = {
    "Poke Ball": 20,
    "Great Ball": 50,
    "Ultra Ball": 100
}


def coin_reward(enemy):
    if enemy.types == "Boss":
        return 100
    if enemy.name == "NYSTRIA":
        return 150
    return 10 + enemy.level * 3


def new_team():
    team = []
    for name, hp, level, moves in TEAM_DATA:
        pokemon = Creature(name, hp, moves, level)
        pokemon.types = TEAM_TYPES.get(name, "Unknown")
        team.append(pokemon)
    return team


# Legendary NYSTRIA
NYSTRIA_CHANCE = 0.05          # extra 5% chance per battle
NYSTRIA_CATCH_PENALTY = 0.20   # harder to catch than normal Pokemon
NYSTRIA_MOVES = [
    ("Void Pulse", 45), ("Null Beam", 50),
    ("Rift Strike", 55), ("Dragon Pulse", 45)
]


def make_nystria():
    hp = random.randint(260, 300)
    nystria = Creature("NYSTRIA", hp, list(NYSTRIA_MOVES),
                       level=random.randint(30, 35), bonus=8)
    nystria.types = "Void/Dragon"
    nystria.pokedex_number = 46
    return nystria


def random_enemy():
    if random.random() < NYSTRIA_CHANCE:
        return make_nystria()

    if random.random() < 0.12:
        name, hp, bonus, moves = random.choice(BOSS_DATA)
        enemy = Creature(name, hp, [(m, 40) for m in moves],
                         level=40, bonus=bonus)
        enemy.types = "Boss"
        return enemy

    number, name, types = random.choice(WILD_POKEMON)

    if name == "NYSTRIA":
        return make_nystria()

    hp = random.randint(100, 190)

    if "/" in types:
        hp += 20

    enemy = Creature(name, hp, wild_moves(types),
                     level=random.randint(3, 12))
    enemy.types = types
    enemy.pokedex_number = number
    return enemy


# ==========================================
# BATTLE TOURNAMENT
# ==========================================

# (trainer name, level, Pokemon, coin prize)
TOURNAMENT = [
    ("Bug Catcher Mia", 14, ["Bugbyte", "Glitchor"], 50),
    ("Hiker Bram", 18, ["Rockruffle", "Cragoyle"], 80),
    ("Ace Trainer Zoe", 22, ["Shocklynx", "Aquarion", "Pyrovolt"], 120),
    ("Dragon Tamer Kai", 26, ["Floragon", "Toxidrake", "Voltraze"], 160),
    ("Champion Vex", 32,
     ["Galaxion", "Dreadgeist", "Glacifang", "NYSTRIA"], 400),
]

POKEDEX_BY_NAME = {name: (number, types)
                   for number, name, types in WILD_POKEMON}


def trainer_pokemon(name, level):
    if name == "NYSTRIA":
        # The Champion's ace is extra tough
        mon = make_nystria()
        mon.level = level + 4
        mon.bonus = level // 2 + 4
        mon.max_hp += 60
        mon.hp = mon.max_hp
        return mon

    number, types = POKEDEX_BY_NAME[name]
    hp = 130 + level * 8 + random.randint(0, 20)
    if "/" in types:
        hp += 20

    moves = [(m, p + random.randint(8, 14)) for m, p in wild_moves(types)]
    mon = Creature(name, hp, moves, level=level, bonus=level // 2)
    mon.types = types
    mon.pokedex_number = number
    return mon


def trainer_team(round_index):
    trainer, level, names, prize = TOURNAMENT[round_index]
    return [trainer_pokemon(n, level) for n in names]


# ==========================================
# SAVE / LOAD STORAGE
# ==========================================

SAVE_FILE = "pokemon_save.json"
SAVE_KEY = "pokemon_new_world_save"


def storage_write(text):
    if WEB:
        import platform  # pygbag's link to the browser
        platform.window.localStorage.setItem(SAVE_KEY, text)
    else:
        with open(SAVE_FILE, "w") as f:
            f.write(text)


def storage_read():
    try:
        if WEB:
            import platform
            return platform.window.localStorage.getItem(SAVE_KEY) or None
        with open(SAVE_FILE) as f:
            return f.read()
    except Exception:
        return None


def creature_to_dict(c):
    return {
        "name": c.name, "max_hp": c.max_hp, "hp": c.hp,
        "moves": [list(m) for m in c.moves],
        "level": c.level, "bonus": c.bonus, "xp": c.xp,
        "types": c.types, "pokedex_number": c.pokedex_number
    }


def creature_from_dict(d):
    c = Creature(d["name"], d["max_hp"],
                 [tuple(m) for m in d["moves"]],
                 d.get("level", 1), d.get("bonus", 0))
    c.hp = max(0, min(c.max_hp, d.get("hp", c.max_hp)))
    c.types = d.get("types", "Unknown")
    c.pokedex_number = d.get("pokedex_number")
    c.xp = int(d.get("xp", 0))
    return c


# ==========================================
# NEW SPRITE SYSTEM
# ==========================================

def outline(surf, colour, rect, radius=0, width=3):
    if radius:
        pygame.draw.rect(surf, colour, rect, width, border_radius=radius)
    else:
        pygame.draw.ellipse(surf, colour, rect, width)


def make_flame(size):
    """Custom sprite for Flame."""

    s = pygame.Surface((100, 100), pygame.SRCALPHA)

    navy = (25, 55, 120)
    blue = (40, 100, 205)
    light_blue = (90, 165, 245)
    cream = (250, 230, 185)
    dark = (15, 25, 55)
    orange = (255, 100, 20)
    yellow = (255, 220, 55)

    # Shadow
    pygame.draw.ellipse(s, (15, 20, 35, 120), (12, 83, 76, 12))

    # Tail
    pygame.draw.polygon(s, navy, [
        (72, 67), (91, 77), (96, 58), (89, 48), (82, 61)
    ])
    pygame.draw.polygon(s, orange, [
        (88, 62), (100, 39), (94, 64), (99, 75), (84, 72)
    ])
    pygame.draw.polygon(s, yellow, [
        (94, 60), (98, 45), (97, 65), (90, 69)
    ])

    # Back legs
    pygame.draw.ellipse(s, navy, (57, 70, 22, 19))
    pygame.draw.ellipse(s, navy, (23, 70, 22, 19))

    # Body
    pygame.draw.ellipse(s, dark, (14, 37, 72, 48))
    pygame.draw.ellipse(s, blue, (17, 35, 66, 45))
    pygame.draw.ellipse(s, cream, (34, 48, 34, 31))

    # Front paws
    pygame.draw.ellipse(s, navy, (17, 75, 25, 12))
    pygame.draw.ellipse(s, navy, (58, 75, 25, 12))

    # Head
    pygame.draw.ellipse(s, dark, (19, 10, 63, 54))
    pygame.draw.ellipse(s, blue, (22, 9, 57, 51))

    # Ears
    pygame.draw.polygon(s, dark, [(25, 25), (15, 2), (39, 17)])
    pygame.draw.polygon(s, light_blue, [(26, 22), (19, 7), (35, 19)])
    pygame.draw.polygon(s, dark, [(67, 19), (85, 3), (78, 30)])
    pygame.draw.polygon(s, light_blue, [(70, 19), (81, 9), (76, 25)])

    # Cream face
    pygame.draw.ellipse(s, cream, (34, 31, 39, 26))
    pygame.draw.ellipse(s, cream, (48, 42, 27, 16))

    # Eyes
    pygame.draw.ellipse(s, dark, (37, 29, 9, 13))
    pygame.draw.ellipse(s, dark, (62, 29, 9, 13))
    pygame.draw.circle(s, WHITE, (40, 33), 3)
    pygame.draw.circle(s, WHITE, (65, 33), 3)

    # Nose and mouth
    pygame.draw.circle(s, dark, (66, 48), 3)
    pygame.draw.arc(s, dark, (52, 45, 19, 13), 0, math.pi, 2)

    # Fiery mane around neck
    pygame.draw.polygon(s, orange, [
        (18, 42), (5, 32), (13, 52), (4, 62),
        (23, 60), (29, 76), (40, 62), (54, 72),
        (58, 55), (43, 42)
    ])

    pygame.draw.polygon(s, yellow, [
        (19, 45), (12, 37), (18, 53), (13, 59),
        (27, 56), (32, 68), (40, 57), (51, 64),
        (52, 52), (39, 46)
    ])

    # Head flame
    pygame.draw.polygon(s, orange, [
        (39, 15), (34, 1), (47, 10),
        (53, 0), (59, 13), (72, 7), (65, 24)
    ])
    pygame.draw.polygon(s, yellow, [
        (43, 14), (42, 6), (51, 13),
        (55, 5), (59, 17), (65, 13), (59, 24)
    ])

    # Flame highlights
    pygame.draw.circle(s, WHITE, (45, 55), 2)
    pygame.draw.circle(s, WHITE, (33, 48), 2)

    return pygame.transform.smoothscale(s, (size, size))


def make_nystria_sprite(size):
    """Custom sprite for the legendary NYSTRIA (Void/Dragon)."""

    s = pygame.Surface((100, 100), pygame.SRCALPHA)

    void_dark = (30, 10, 55)
    void = (80, 35, 140)
    void_light = (150, 95, 225)
    magenta = (255, 40, 140)
    pink = (255, 140, 210)
    cyan = (100, 230, 255)
    horn = (225, 205, 255)

    # Void aura
    pygame.draw.circle(s, (160, 40, 200, 70), (50, 50), 48)
    pygame.draw.circle(s, (255, 40, 140, 150), (50, 50), 47, 2)

    # Shadow
    pygame.draw.ellipse(s, (15, 10, 30, 130), (14, 85, 72, 11))

    # Wings (behind body)
    pygame.draw.polygon(s, void_dark, [
        (38, 42), (2, 8), (8, 30), (0, 40), (12, 48), (4, 60), (30, 58)
    ])
    pygame.draw.polygon(s, void_dark, [
        (62, 42), (98, 8), (92, 30), (100, 40), (88, 48), (96, 60), (70, 58)
    ])
    pygame.draw.polygon(s, void, [
        (36, 44), (8, 15), (12, 32), (6, 41), (16, 48), (10, 57), (31, 55)
    ])
    pygame.draw.polygon(s, void, [
        (64, 44), (92, 15), (88, 32), (94, 41), (84, 48), (90, 57), (69, 55)
    ])
    for end in ((8, 15), (6, 41), (10, 57)):
        pygame.draw.line(s, magenta, (34, 46), end, 1)
    for end in ((92, 15), (94, 41), (90, 57)):
        pygame.draw.line(s, magenta, (66, 46), end, 1)

    # Serpent tail curling round the front
    pygame.draw.polygon(s, void_dark, [
        (60, 78), (80, 86), (94, 78), (96, 66), (90, 70), (84, 79), (66, 74)
    ])
    pygame.draw.polygon(s, magenta, [(95, 68), (100, 58), (97, 72)])
    pygame.draw.polygon(s, cyan, [(93, 70), (95, 62), (96, 72)])

    # Legs
    pygame.draw.ellipse(s, void_dark, (28, 74, 18, 14))
    pygame.draw.ellipse(s, void_dark, (54, 74, 18, 14))

    # Body
    pygame.draw.ellipse(s, void_dark, (26, 40, 48, 44))
    pygame.draw.ellipse(s, void, (29, 41, 42, 40))
    pygame.draw.ellipse(s, void_light, (38, 50, 24, 26))

    # Rift in the chest
    rift = [(50, 50), (54, 57), (51, 61), (56, 68), (49, 76),
            (51, 68), (46, 63), (49, 58)]
    pygame.draw.polygon(s, (5, 0, 15), rift)
    pygame.draw.polygon(s, magenta, rift, 2)
    pygame.draw.circle(s, WHITE, (51, 63), 1)

    # Neck and head
    pygame.draw.polygon(s, void, [(42, 46), (58, 46), (56, 30), (44, 30)])
    pygame.draw.ellipse(s, void_dark, (31, 10, 38, 30))
    pygame.draw.ellipse(s, void, (33, 11, 34, 27))

    # Snout
    pygame.draw.polygon(s, void, [(42, 28), (58, 28), (55, 40), (45, 40)])
    pygame.draw.polygon(s, void_light, [(45, 32), (55, 32), (53, 39), (47, 39)])
    pygame.draw.circle(s, void_dark, (48, 37), 1)
    pygame.draw.circle(s, void_dark, (52, 37), 1)

    # Horns sweeping back
    pygame.draw.polygon(s, horn, [(37, 16), (20, 0), (30, 4), (42, 13)])
    pygame.draw.polygon(s, horn, [(63, 16), (80, 0), (70, 4), (58, 13)])
    pygame.draw.polygon(s, magenta, [(24, 2), (20, 0), (27, 4)])
    pygame.draw.polygon(s, magenta, [(76, 2), (80, 0), (73, 4)])

    # Crest gem
    pygame.draw.polygon(s, cyan, [(50, 8), (54, 13), (50, 18), (46, 13)])
    pygame.draw.circle(s, WHITE, (49, 12), 1)

    # Glowing eyes
    pygame.draw.ellipse(s, magenta, (38, 20, 9, 6))
    pygame.draw.ellipse(s, magenta, (53, 20, 9, 6))
    pygame.draw.ellipse(s, pink, (40, 21, 4, 3))
    pygame.draw.ellipse(s, pink, (55, 21, 4, 3))

    # Stars floating in the aura
    for x, y in ((12, 72), (88, 24), (20, 22), (84, 62), (50, 94)):
        pygame.draw.circle(s, WHITE, (x, y), 1)

    return pygame.transform.smoothscale(s, (size, size))


# ==========================================
# WILD POKEMON SPRITES (unique body shapes)
# ==========================================

SHAPES = {
    "Embercub": "quad", "Blazepaw": "quad", "Pyroclaw": "quad",
    "Aquaffin": "fish", "Tidalisk": "fish", "Abyssurge": "fish",
    "Leaflet": "plant", "Thornox": "plant", "Floragon": "dragon",
    "Voltkit": "quad", "Shocklynx": "quad", "Thundermaw": "quad",
    "Frostbit": "quad", "Glacieron": "golem", "Cryowraith": "ghost",
    "Rockruffle": "quad", "Cragoyle": "bird", "Terradon": "dragon",
    "Shadelet": "ghost", "Hauntalon": "bird", "Dreadgeist": "ghost",
    "Mechling": "golem", "Ironclast": "golem", "Titanforge": "golem",
    "Mindimp": "imp", "Psyphantom": "ghost", "Dreamora": "imp",
    "Venomite": "bug", "Toxidrake": "dragon",
    "Skyray": "bird", "Stormeagle": "bird",
    "Brawlpup": "imp", "Warfang": "quad",
    "Fableaf": "plant", "Lumifawn": "quad",
    "Gloomora": "ghost", "Nightreign": "dragon",
    "Bugbyte": "bug", "Glitchor": "bug",
    "Fossilisk": "dragon", "Magmole": "quad", "Spectrill": "ghost",
    "Starlingo": "orb", "Galaxion": "dragon", "Nullvex": "orb",
    "Frolren": "dragon", "Pyrovolt": "orb", "Aquarion": "fish",
    "Thornblade": "plant", "Voltraze": "dragon", "Glacifang": "quad",
    "Magmanta": "fish", "Phantomox": "ghost", "Terraboom": "golem",
    "Mindflare": "imp", "Venomantis": "bug", "Skyrazor": "bird",
    "Lumidrake": "dragon", "Abyssalon": "fish", "Dreadhorn": "quad",
    "Starflare": "orb", "Nullshade": "ghost", "Ironquake": "golem",
    "Florawing": "bird", "Chronox": "golem",
}

FLOPPY_EARS = ("Rockruffle", "Warfang", "Magmole", "Embercub")
HORNED = ("Dreadhorn", "Lumifawn", "Glacifang", "Thundermaw")
EYE_DARK = (20, 15, 35)


def shade(colour, amount):
    return tuple(max(0, min(255, c + amount)) for c in colour[:3])


def draw_eye(s, x, y, r=4, angry=False, colour=EYE_DARK):
    pygame.draw.circle(s, colour, (x, y), r)
    pygame.draw.circle(s, WHITE, (x - r // 3, y - r // 3), max(1, r // 3))
    if angry:
        pygame.draw.line(s, EYE_DARK, (x - r - 1, y - r - 2),
                         (x + r, y - r + 1), 2)


def shape_poly(s, fill, points, edge):
    pygame.draw.polygon(s, fill, points)
    pygame.draw.polygon(s, edge, points, 2)


def shape_oval(s, fill, rect, edge):
    pygame.draw.ellipse(s, fill, rect)
    pygame.draw.ellipse(s, edge, rect, 2)


def type_accent(s, kind, x, y):
    """Small type symbol (flame, bolt, leaf...) at a point."""
    if kind == "Fire":
        pygame.draw.polygon(s, (255, 90, 20), [
            (x - 7, y + 6), (x - 8, y - 4), (x - 3, y), (x, y - 12),
            (x + 3, y - 2), (x + 7, y - 6), (x + 7, y + 6)])
        pygame.draw.polygon(s, (255, 220, 60), [
            (x - 4, y + 5), (x - 3, y - 1), (x, y - 6), (x + 3, y), (x + 4, y + 5)])
    elif kind == "Electric":
        pygame.draw.polygon(s, GOLD, [
            (x - 2, y - 12), (x + 7, y - 12), (x + 1, y - 3), (x + 8, y - 3),
            (x - 6, y + 12), (x - 1, y + 1), (x - 7, y + 1)])
        pygame.draw.polygon(s, EYE_DARK, [
            (x - 2, y - 12), (x + 7, y - 12), (x + 1, y - 3), (x + 8, y - 3),
            (x - 6, y + 12), (x - 1, y + 1), (x - 7, y + 1)], 1)
    elif kind == "Water":
        pygame.draw.polygon(s, (60, 170, 255), [
            (x, y - 10), (x + 6, y + 1), (x - 6, y + 1)])
        pygame.draw.circle(s, (60, 170, 255), (x, y + 2), 6)
        pygame.draw.circle(s, WHITE, (x - 2, y), 2)
    elif kind == "Ice":
        for dx, h in ((-5, 8), (0, 13), (5, 8)):
            pygame.draw.polygon(s, (215, 245, 255), [
                (x + dx - 3, y + 3), (x + dx, y - h), (x + dx + 3, y + 3)])
            pygame.draw.polygon(s, (90, 180, 230), [
                (x + dx - 3, y + 3), (x + dx, y - h), (x + dx + 3, y + 3)], 1)
    elif kind == "Grass":
        pygame.draw.ellipse(s, (60, 190, 75), (x - 4, y - 12, 9, 16))
        pygame.draw.line(s, (25, 110, 40), (x, y + 4), (x, y - 10), 1)
    elif kind in ("Ghost", "Void"):
        col = (190, 120, 255) if kind == "Ghost" else (255, 40, 140)
        pygame.draw.circle(s, col, (x, y), 5)
        pygame.draw.circle(s, col, (x + 6, y - 7), 3)
        pygame.draw.circle(s, col, (x - 5, y - 10), 2)
    elif kind == "Dark":
        pygame.draw.circle(s, (230, 230, 120), (x, y), 6)
        pygame.draw.circle(s, (60, 35, 70), (x + 3, y - 2), 5)
    elif kind == "Psychic":
        pygame.draw.polygon(s, (255, 110, 200), [
            (x, y - 7), (x + 6, y), (x, y + 7), (x - 6, y)])
        pygame.draw.circle(s, WHITE, (x - 1, y - 2), 1)
    elif kind == "Poison":
        for dx, dy, r in ((0, 0, 5), (6, -6, 3), (-5, -8, 2)):
            pygame.draw.circle(s, (190, 80, 220), (x + dx, y + dy), r)
    elif kind == "Fairy" or kind == "Light":
        col = (255, 190, 230) if kind == "Fairy" else (255, 245, 150)
        pygame.draw.polygon(s, col, [
            (x, y - 8), (x + 2, y - 2), (x + 8, y), (x + 2, y + 2),
            (x, y + 8), (x - 2, y + 2), (x - 8, y), (x - 2, y - 2)])
    elif kind == "Cosmic":
        pygame.draw.circle(s, (230, 235, 255), (x, y), 3)
        pygame.draw.circle(s, (160, 170, 255), (x, y), 7, 1)
    elif kind == "Dragon":
        pygame.draw.polygon(s, (255, 190, 100), [
            (x - 6, y + 4), (x - 2, y - 10), (x + 1, y + 1), (x + 5, y - 8), (x + 6, y + 4)])
    elif kind in ("Steel", "Rock", "Ground"):
        col = {"Steel": (200, 215, 235), "Rock": (175, 150, 110),
               "Ground": (195, 140, 75)}[kind]
        pygame.draw.polygon(s, col, [
            (x - 6, y + 4), (x - 4, y - 5), (x + 3, y - 7), (x + 7, y + 1), (x + 3, y + 6)])
        pygame.draw.polygon(s, shade(col, -70), [
            (x - 6, y + 4), (x - 4, y - 5), (x + 3, y - 7), (x + 7, y + 1), (x + 3, y + 6)], 1)
    elif kind == "Flying":
        pygame.draw.polygon(s, (220, 240, 255), [
            (x - 8, y + 3), (x + 8, y - 8), (x + 2, y + 4)])
    elif kind == "Fighting":
        pygame.draw.circle(s, (240, 140, 80), (x, y), 6)
        pygame.draw.circle(s, EYE_DARK, (x, y), 6, 1)
    elif kind == "Bug":
        pygame.draw.ellipse(s, (170, 220, 70), (x - 5, y - 4, 10, 8))
        pygame.draw.line(s, EYE_DARK, (x, y - 4), (x, y + 4), 1)


def draw_quad(s, name, c1, c2, stage, rng):
    edge, light = shade(c1, -80), shade(c1, 85)
    # two-tone bushy tail
    shape_poly(s, c2, [(24, 62), (10, 50), (2, 36), (12, 34), (20, 44), (30, 56)],
               shade(c2, -80))
    # back legs
    shape_oval(s, shade(c1, -35), (22, 70, 15, 16), edge)
    shape_oval(s, shade(c1, -35), (58, 70, 15, 16), edge)
    # body
    shape_oval(s, c1, (18, 46, 60, 34), edge)
    pygame.draw.ellipse(s, light, (34, 60, 32, 17))
    # stripes on the back
    for x in (28, 38, 48):
        x += rng.randint(-2, 2)
        pygame.draw.polygon(s, c2, [(x, 48), (x + 6, 48), (x + 1, 62)])
    # front legs
    shape_oval(s, c1, (32, 72, 13, 15), edge)
    shape_oval(s, c1, (52, 72, 13, 15), edge)
    # mane on evolved forms
    if stage >= 3:
        shape_poly(s, c2, [(44, 30), (36, 42), (44, 46), (40, 56),
                           (52, 52), (56, 60), (60, 48)], shade(c2, -80))
    # ears
    if name in FLOPPY_EARS:
        shape_oval(s, shade(c1, -30), (44, 20, 12, 22), edge)
        shape_oval(s, shade(c1, -30), (80, 20, 12, 22), edge)
    else:
        shape_poly(s, c1, [(50, 26), (48, 4), (64, 20)], edge)
        shape_poly(s, c1, [(74, 20), (88, 4), (86, 28)], edge)
        pygame.draw.polygon(s, c2, [(52, 22), (51, 10), (60, 20)])
        pygame.draw.polygon(s, c2, [(77, 20), (85, 10), (84, 24)])
    if name in HORNED:
        shape_poly(s, (235, 225, 200), [(58, 20), (54, 0), (64, 16)], edge)
        shape_poly(s, (235, 225, 200), [(76, 16), (84, -2), (82, 20)], edge)
    # head
    shape_oval(s, c1, (44, 16, 46, 40), edge)
    pygame.draw.ellipse(s, light, (60, 34, 26, 17))
    pygame.draw.circle(s, EYE_DARK, (82, 39), 3)
    pygame.draw.line(s, EYE_DARK, (76, 46), (82, 44), 2)
    draw_eye(s, 61, 31, 4, stage >= 3)
    draw_eye(s, 77, 29, 4, stage >= 3)
    # cheek mark
    pygame.draw.circle(s, c2, (55, 42), 3)
    return (8, 36), (67, 12)


def draw_fish(s, name, c1, c2, stage, rng):
    edge, light = shade(c1, -80), shade(c1, 90)
    fin = shade(c2, 10)
    # tail fin
    shape_poly(s, fin, [(30, 52), (4, 30), (12, 52), (4, 74)], shade(fin, -80))
    # dorsal fin
    shape_poly(s, fin, [(40, 34), (52, 8 if stage >= 3 else 16), (70, 34)],
               shade(fin, -80))
    # body
    shape_oval(s, c1, (20, 30, 66, 44), edge)
    pygame.draw.ellipse(s, light, (34, 54, 46, 17))
    # scales
    for _ in range(5):
        x, y = rng.randint(30, 60), rng.randint(36, 52)
        pygame.draw.circle(s, shade(c1, 35), (x, y), 4, 1)
    # stripe
    pygame.draw.line(s, c2, (36, 34), (40, 70), 4)
    # side fin
    shape_poly(s, fin, [(52, 58), (42, 78), (64, 64)], shade(fin, -80))
    # face
    draw_eye(s, 72, 44, 6, stage >= 3)
    pygame.draw.line(s, EYE_DARK, (78, 58), (86, 55), 2)
    if stage >= 3:
        pygame.draw.polygon(s, WHITE, [(80, 57), (82, 62), (84, 56)])
    # bubbles
    pygame.draw.circle(s, (220, 245, 255), (92, 34), 4, 1)
    pygame.draw.circle(s, (220, 245, 255), (95, 22), 3, 1)
    return (8, 40), (56, 18)


def draw_dragon(s, name, c1, c2, stage, rng):
    edge, light = shade(c1, -80), shade(c1, 80)
    wing = shade(c2, -10)
    # wings
    shape_poly(s, wing, [(38, 46), (6, 12), (12, 34), (2, 46), (30, 58)],
               shade(wing, -90))
    shape_poly(s, wing, [(62, 46), (94, 12), (88, 34), (98, 46), (70, 58)],
               shade(wing, -90))
    pygame.draw.line(s, shade(wing, -60), (36, 48), (8, 16), 1)
    pygame.draw.line(s, shade(wing, -60), (64, 48), (92, 16), 1)
    # tail
    shape_poly(s, c1, [(62, 76), (86, 88), (98, 72), (86, 78), (66, 70)], edge)
    # legs
    shape_oval(s, shade(c1, -30), (30, 74, 16, 14), edge)
    shape_oval(s, shade(c1, -30), (54, 74, 16, 14), edge)
    # body
    shape_oval(s, c1, (30, 42, 40, 40), edge)
    pygame.draw.ellipse(s, light, (40, 50, 20, 28))
    for y in (56, 63, 70):
        pygame.draw.line(s, shade(light, -50), (42, y), (58, y), 1)
    # neck + head
    pygame.draw.polygon(s, c1, [(42, 48), (58, 48), (58, 30), (44, 30)])
    shape_oval(s, c1, (34, 10, 34, 28), edge)
    shape_poly(s, c1, [(52, 22), (76, 26), (74, 36), (54, 36)], edge)
    pygame.draw.circle(s, EYE_DARK, (72, 30), 1)
    # horns
    horn = (240, 230, 200)
    shape_poly(s, horn, [(40, 16), (28, 0), (46, 12)], shade(horn, -90))
    shape_poly(s, horn, [(56, 12), (62, -2), (62, 16)], shade(horn, -90))
    draw_eye(s, 50, 22, 4, True)
    # back spikes
    for x, y in ((32, 50), (30, 60), (32, 70)):
        pygame.draw.polygon(s, c2, [(x, y - 4), (x - 7, y), (x, y + 4)])
    return (94, 72), (50, 4)


def draw_bird(s, name, c1, c2, stage, rng):
    edge, light = shade(c1, -80), shade(c1, 90)
    feather = shade(c2, 0)
    # tail feathers
    shape_poly(s, feather, [(30, 64), (6, 74), (10, 82), (34, 74)], shade(feather, -80))
    shape_poly(s, c1, [(32, 70), (10, 88), (36, 78)], edge)
    # raised back wing on evolved forms
    if stage >= 2:
        shape_poly(s, feather, [(46, 46), (18, 8), (26, 28), (14, 30), (40, 56)],
                   shade(feather, -80))
    # legs
    for x in (44, 58):
        pygame.draw.line(s, (240, 170, 40), (x, 76), (x, 90), 3)
        pygame.draw.line(s, (240, 170, 40), (x, 90), (x - 5, 94), 2)
        pygame.draw.line(s, (240, 170, 40), (x, 90), (x + 5, 94), 2)
    # body
    shape_oval(s, c1, (26, 38, 48, 44), edge)
    pygame.draw.ellipse(s, light, (42, 52, 26, 26))
    # front wing
    shape_poly(s, feather, [(36, 48), (14, 66), (30, 76), (56, 66)], shade(feather, -80))
    for i in range(3):
        pygame.draw.line(s, shade(feather, -60), (36, 52), (18 + i * 8, 68 + i * 3), 1)
    # head
    pygame.draw.circle(s, c1, (60, 30), 17)
    pygame.draw.circle(s, edge, (60, 30), 17, 2)
    # crest
    shape_poly(s, feather, [(52, 16), (46, 0), (58, 12), (62, 0), (66, 14)],
               shade(feather, -80))
    # beak
    shape_poly(s, (250, 190, 50), [(72, 28), (92, 34), (72, 40)], (150, 100, 20))
    draw_eye(s, 64, 26, 4, stage >= 3)
    return (12, 76), (56, 6)


def draw_golem(s, name, c1, c2, stage, rng):
    edge = shade(c1, -90)
    # legs
    shape_poly(s, shade(c1, -30), [(28, 70), (44, 70), (44, 90), (26, 90)], edge)
    shape_poly(s, shade(c1, -30), [(56, 70), (72, 70), (74, 90), (56, 90)], edge)
    # arms
    shape_oval(s, shade(c1, -15), (4, 40, 22, 34), edge)
    shape_oval(s, shade(c1, -15), (74, 40, 22, 34), edge)
    shape_oval(s, c2, (6, 64, 18, 16), shade(c2, -90))
    shape_oval(s, c2, (76, 64, 18, 16), shade(c2, -90))
    # body
    body = [(20, 40), (32, 26), (68, 26), (80, 40), (76, 76), (24, 76)]
    shape_poly(s, c1, body, edge)
    # plates and rivets
    pygame.draw.line(s, shade(c1, 50), (26, 44), (74, 44), 2)
    for x in (28, 72):
        for y in (32, 70):
            pygame.draw.circle(s, shade(c1, 60), (x, y), 2)
    # cracks
    for _ in range(2):
        x = rng.randint(28, 66)
        pygame.draw.lines(s, edge, False, [(x, 50), (x + 4, 56), (x, 62)], 1)
    # glowing core
    pygame.draw.circle(s, shade(c2, -60), (50, 58), 10)
    pygame.draw.circle(s, c2, (50, 58), 7)
    pygame.draw.circle(s, WHITE, (48, 56), 2)
    # head with visor
    shape_poly(s, c1, [(36, 8), (64, 8), (66, 28), (34, 28)], edge)
    pygame.draw.rect(s, EYE_DARK, (39, 14, 22, 8))
    pygame.draw.rect(s, c2, (42, 16, 16, 4))
    if stage >= 3:
        for x in (38, 50, 62):
            pygame.draw.polygon(s, c2, [(x - 4, 8), (x, -2), (x + 4, 8)])
    return (85, 46), (50, 2)


def draw_ghost(s, name, c1, c2, stage, rng):
    edge, light = shade(c1, -70), shade(c1, 70)
    # floating orbs
    for _ in range(3):
        x, y = rng.randint(6, 94), rng.randint(10, 70)
        pygame.draw.circle(s, c2, (x, y), rng.randint(2, 4))
    # wispy body
    body = [(22, 44), (24, 80), (32, 72), (40, 90), (50, 76),
            (60, 92), (68, 74), (78, 84), (78, 44)]
    shape_poly(s, c1, body, edge)
    shape_oval(s, c1, (20, 12, 60, 58), edge)
    pygame.draw.ellipse(s, c1, (23, 40, 54, 30))
    pygame.draw.ellipse(s, light, (32, 18, 22, 12))
    # little arms
    shape_poly(s, c1, [(22, 48), (6, 56), (22, 58)], edge)
    shape_poly(s, c1, [(78, 48), (94, 40), (80, 58)], edge)
    # hollow eyes
    for x in (38, 62):
        pygame.draw.ellipse(s, EYE_DARK, (x - 7, 30, 14, 18))
        pygame.draw.circle(s, c2, (x + 1, 38), 3)
    # jagged mouth
    pygame.draw.lines(s, EYE_DARK, False, [
        (38, 56), (43, 60), (48, 55), (53, 60), (58, 55), (62, 58)], 2)
    if stage >= 3:
        shape_poly(s, c2, [(34, 16), (30, 0), (42, 12), (50, -2),
                           (58, 12), (70, 0), (66, 16)], shade(c2, -80))
    return (86, 84), (50, 6)


def draw_bug(s, name, c1, c2, stage, rng):
    edge, light = shade(c1, -80), shade(c1, 80)
    # wings (opaque, pale)
    if stage >= 2:
        wing = shade(c2, 110)
        shape_oval(s, wing, (26, 18, 26, 36), shade(c2, -40))
        shape_oval(s, wing, (40, 14, 22, 34), shade(c2, -40))
    # legs
    for x in (32, 46, 60):
        pygame.draw.line(s, EYE_DARK, (x, 66), (x - 6, 86), 2)
        pygame.draw.line(s, EYE_DARK, (x + 2, 66), (x + 8, 86), 2)
    # abdomen with stripes
    shape_oval(s, c1, (8, 46, 42, 32), edge)
    for x in (18, 28, 38):
        pygame.draw.line(s, c2, (x, 48), (x, 76), 4)
    # thorax
    shape_oval(s, shade(c1, -20), (42, 46, 24, 26), edge)
    # head
    pygame.draw.circle(s, c1, (76, 50), 15)
    pygame.draw.circle(s, edge, (76, 50), 15, 2)
    # compound eyes
    shape_oval(s, c2, (72, 38, 12, 14), shade(c2, -90))
    pygame.draw.circle(s, WHITE, (77, 42), 2)
    # antennae
    pygame.draw.lines(s, EYE_DARK, False, [(72, 38), (70, 22), (62, 14)], 2)
    pygame.draw.lines(s, EYE_DARK, False, [(80, 38), (86, 22), (94, 18)], 2)
    pygame.draw.circle(s, c2, (62, 14), 3)
    pygame.draw.circle(s, c2, (94, 18), 3)
    # mandibles / stinger
    pygame.draw.polygon(s, light, [(86, 56), (94, 60), (86, 62)])
    if stage >= 3:
        pygame.draw.polygon(s, c2, [(8, 62), (-2, 66), (10, 70)])
    return (10, 64), (62, 10)


def draw_plant(s, name, c1, c2, stage, rng):
    edge, light = shade(c1, -80), shade(c1, 80)
    leaf = (70, 190, 80) if c1 != (80, 210, 90) else (40, 150, 60)
    bladed = "Steel" in name or name == "Thornblade"
    # roots
    for x in (30, 50, 68):
        shape_oval(s, shade(c1, -40), (x - 4, 80, 14, 10), edge)
    # big leaves
    for pts in ([(50, 30), (14, 8), (22, 34)], [(50, 30), (86, 8), (78, 34)],
                [(46, 28), (40, 0), (56, 22)]):
        col = (190, 205, 220) if bladed else leaf
        shape_poly(s, col, pts, shade(col, -90))
        pygame.draw.line(s, shade(col, -60), pts[0], pts[1], 1)
    # thorns
    if stage >= 2:
        for x, y in ((22, 52), (78, 52), (30, 72), (70, 72)):
            pygame.draw.polygon(s, c2, [(x - 3, y), (x, y - 8 if y < 60 else y + 8), (x + 3, y)])
    # bulb body
    shape_oval(s, c1, (22, 30, 56, 54), edge)
    pygame.draw.ellipse(s, light, (34, 54, 32, 24))
    # flower on evolved forms
    if stage >= 3:
        for ang in range(0, 360, 60):
            px = 50 + int(9 * math.cos(math.radians(ang)))
            py = 26 + int(9 * math.sin(math.radians(ang)))
            pygame.draw.circle(s, c2, (px, py), 6)
        pygame.draw.circle(s, GOLD, (50, 26), 5)
    # face
    draw_eye(s, 41, 50, 4, stage >= 3)
    draw_eye(s, 59, 50, 4, stage >= 3)
    pygame.draw.lines(s, EYE_DARK, False, [(44, 62), (50, 66), (56, 62)], 2)
    pygame.draw.circle(s, (255, 150, 170), (34, 58), 3)
    pygame.draw.circle(s, (255, 150, 170), (66, 58), 3)
    return (82, 70), (50, 12)


def draw_imp(s, name, c1, c2, stage, rng):
    edge, light = shade(c1, -80), shade(c1, 85)
    # tail
    shape_poly(s, c1, [(36, 70), (14, 76), (8, 66), (16, 70)], edge)
    # legs
    shape_oval(s, shade(c1, -30), (34, 74, 14, 16), edge)
    shape_oval(s, shade(c1, -30), (52, 74, 14, 16), edge)
    # body
    shape_oval(s, c1, (32, 44, 36, 36), edge)
    pygame.draw.ellipse(s, light, (40, 52, 20, 22))
    # arms with fists
    shape_poly(s, c1, [(34, 50), (18, 58), (22, 64), (36, 58)], edge)
    shape_poly(s, c1, [(66, 50), (82, 44), (84, 50), (66, 58)], edge)
    shape_oval(s, c2, (12, 56, 12, 12), shade(c2, -90))
    shape_oval(s, c2, (80, 40, 12, 12), shade(c2, -90))
    # head
    pygame.draw.circle(s, c1, (50, 28), 21)
    pygame.draw.circle(s, edge, (50, 28), 21, 2)
    # hair tufts
    shape_poly(s, c2, [(32, 18), (34, 2), (42, 10), (50, 0), (58, 10),
                       (66, 2), (68, 18), (50, 12)], shade(c2, -80))
    # headband for fighters, gem for psychics
    if "Fighting" in POKEDEX_BY_NAME.get(name, (0, ""))[1]:
        pygame.draw.rect(s, RED, (30, 16, 40, 5))
        pygame.draw.polygon(s, RED, [(30, 18), (20, 14), (22, 24)])
    else:
        pygame.draw.polygon(s, (255, 110, 200), [(50, 12), (54, 17), (50, 22), (46, 17)])
    draw_eye(s, 42, 30, 4, stage >= 2)
    draw_eye(s, 58, 30, 4, stage >= 2)
    pygame.draw.lines(s, EYE_DARK, False, [(44, 40), (50, 43), (56, 40)], 2)
    return (10, 64), (50, 0)


def draw_orb(s, name, c1, c2, stage, rng):
    edge, light = shade(c1, -80), shade(c1, 90)
    # star points
    pts = []
    for i in range(16):
        r = 46 if i % 2 == 0 else 30
        a = math.radians(i * 22.5 - 90)
        pts.append((50 + int(r * math.cos(a)), 50 + int(r * math.sin(a))))
    shape_poly(s, c2, pts, shade(c2, -90))
    # orbit ring
    pygame.draw.ellipse(s, light, (4, 40, 92, 22), 2)
    # core
    pygame.draw.circle(s, edge, (50, 50), 28)
    pygame.draw.circle(s, c1, (50, 50), 26)
    pygame.draw.circle(s, light, (50, 50), 17)
    pygame.draw.circle(s, WHITE, (42, 40), 5)
    # face
    draw_eye(s, 42, 50, 4, stage >= 3)
    draw_eye(s, 58, 50, 4, stage >= 3)
    pygame.draw.lines(s, EYE_DARK, False, [(45, 60), (50, 63), (55, 60)], 2)
    # little moons
    pygame.draw.circle(s, WHITE, (90, 46), 4)
    pygame.draw.circle(s, shade(c2, 60), (10, 56), 3)
    return (88, 18), (50, 8)


SHAPE_DRAWERS = {
    "quad": draw_quad, "fish": draw_fish, "dragon": draw_dragon,
    "bird": draw_bird, "golem": draw_golem, "ghost": draw_ghost,
    "bug": draw_bug, "plant": draw_plant, "imp": draw_imp, "orb": draw_orb,
}


def wild_stage(name):
    number = POKEDEX_BY_NAME.get(name, (46, ""))[0]
    if number <= 45:
        return (number - 1) % 3 + 1
    return 2


def make_wild_sprite(name, types, size):
    parts = types.split("/")
    c1 = TYPE_COLOURS.get(parts[0], (150, 150, 170))
    c2 = TYPE_COLOURS.get(parts[1], shade(c1, 70)) if len(parts) > 1 \
        else shade(c1, 70)
    if c2 == c1:
        c2 = shade(c1, 70)
    if types == "Electric":
        c2 = (45, 65, 150)  # navy stripes so they look like their own species

    stage = wild_stage(name)
    rng = random.Random(name)  # same "random" details every time

    art = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.ellipse(art, (15, 20, 35, 110), (14, 86, 72, 11))
    tail_point, head_point = SHAPE_DRAWERS[SHAPES[name]](
        art, name, c1, c2, stage, rng)

    if types == "Electric" and SHAPES[name] == "quad":
        type_accent(art, "Electric", *head_point)  # bolt crest on the head
    else:
        type_accent(art, parts[0], *tail_point)
        if len(parts) > 1:
            type_accent(art, parts[1], *head_point)

    # First forms are smaller, final forms are full size
    scale = {1: 0.78, 2: 0.9, 3: 1.0}[stage]
    inner = int(size * scale)
    final = pygame.Surface((size, size), pygame.SRCALPHA)
    final.blit(pygame.transform.smoothscale(art, (inner, inner)),
               ((size - inner) // 2, size - inner))
    return final


def make_sprite(name, types="Unknown", size=160):
    if name == "Flame":
        return make_flame(size)

    if name == "NYSTRIA":
        return make_nystria_sprite(size)

    if name in SHAPES:
        return make_wild_sprite(name, types, size)

    base = primary_type(types) if types != "Unknown" else "Normal"
    colour = TYPE_COLOURS.get(base, (120, 150, 200))

    s = pygame.Surface((100, 100), pygame.SRCALPHA)

    dark_colour = tuple(max(0, c - 65) for c in colour)
    light_colour = tuple(min(255, c + 65) for c in colour)

    # Shadow
    pygame.draw.ellipse(s, (15, 20, 35, 110), (12, 83, 76, 12))

    # Different body shapes for different types
    if base in ("Dragon", "Flying"):
        pygame.draw.polygon(s, dark_colour, [
            (20, 48), (5, 25), (29, 36),
            (48, 24), (73, 37), (95, 22),
            (82, 55), (70, 78), (30, 78)
        ])
        pygame.draw.polygon(s, colour, [
            (24, 46), (10, 29), (35, 40),
            (50, 29), (73, 42), (89, 29),
            (78, 57), (66, 75), (33, 75)
        ])
    elif base in ("Steel", "Rock", "Ground"):
        pygame.draw.polygon(s, dark_colour, [
            (20, 35), (36, 12), (65, 12),
            (85, 38), (78, 75), (25, 78)
        ])
        pygame.draw.polygon(s, colour, [
            (25, 35), (39, 18), (63, 18),
            (79, 39), (72, 70), (29, 72)
        ])
    elif base in ("Ghost", "Void"):
        pygame.draw.ellipse(s, colour, (18, 17, 64, 66))
        pygame.draw.polygon(s, dark_colour, [
            (25, 65), (12, 94), (42, 75),
            (58, 94), (82, 66)
        ])
    else:
        pygame.draw.ellipse(s, dark_colour, (15, 27, 72, 58))
        pygame.draw.ellipse(s, colour, (19, 23, 64, 58))

    # Head
    pygame.draw.ellipse(s, dark_colour, (24, 5, 53, 47))
    pygame.draw.ellipse(s, colour, (27, 7, 47, 41))

    # Ears or horns
    if base in ("Dragon", "Dark", "Ghost", "Ice"):
        pygame.draw.polygon(s, dark_colour, [
            (31, 23), (17, 0), (42, 13)
        ])
        pygame.draw.polygon(s, dark_colour, [
            (65, 22), (84, 0), (72, 30)
        ])
    else:
        pygame.draw.polygon(s, colour, [
            (30, 20), (18, 2), (42, 16)
        ])
        pygame.draw.polygon(s, colour, [
            (65, 16), (83, 2), (72, 25)
        ])

    # Face
    pygame.draw.ellipse(s, light_colour, (32, 24, 37, 22))
    pygame.draw.circle(s, BLACK, (41, 27), 5)
    pygame.draw.circle(s, BLACK, (61, 27), 5)
    pygame.draw.circle(s, WHITE, (42, 25), 2)
    pygame.draw.circle(s, WHITE, (62, 25), 2)

    # Feet
    pygame.draw.ellipse(s, dark_colour, (23, 73, 25, 12))
    pygame.draw.ellipse(s, dark_colour, (55, 73, 25, 12))

    # Type-specific details
    if base == "Fire":
        pygame.draw.polygon(s, (255, 90, 15), [
            (32, 12), (26, -3), (44, 8),
            (53, -5), (59, 13), (72, 4), (65, 25)
        ])
        pygame.draw.polygon(s, (255, 225, 50), [
            (39, 12), (39, 2), (51, 13),
            (57, 3), (60, 19)
        ])

    elif base == "Water":
        pygame.draw.arc(s, (210, 245, 255), (22, 15, 56, 57), 0, math.pi, 5)
        pygame.draw.circle(s, WHITE, (76, 48), 6)

    elif base == "Electric":
        pygame.draw.polygon(s, GOLD, [
            (50, 35), (66, 35), (55, 53),
            (69, 53), (39, 77), (47, 55), (35, 55)
        ])

    elif base == "Ice":
        pygame.draw.polygon(s, WHITE, [
            (50, 0), (58, 17), (50, 28), (42, 17)
        ])
        pygame.draw.circle(s, WHITE, (75, 55), 5)

    elif base == "Grass":
        pygame.draw.polygon(s, (35, 150, 55), [
            (50, 15), (35, -2), (44, 23)
        ])
        pygame.draw.polygon(s, (100, 240, 100), [
            (53, 15), (70, -2), (60, 25)
        ])

    elif base == "Ghost":
        pygame.draw.circle(s, (220, 180, 255), (50, 51), 25, 3)

    elif base == "Steel":
        pygame.draw.line(s, WHITE, (30, 44), (70, 44), 4)
        pygame.draw.circle(s, WHITE, (50, 50), 24, 2)

    elif base == "Dragon":
        pygame.draw.polygon(s, (255, 180, 90), [
            (20, 45), (3, 30), (28, 36)
        ])
        pygame.draw.polygon(s, (255, 180, 90), [
            (80, 45), (97, 30), (72, 36)
        ])

    elif base == "Cosmic":
        pygame.draw.circle(s, WHITE, (50, 50), 28, 2)
        pygame.draw.circle(s, GOLD, (50, 50), 5)
        pygame.draw.circle(s, WHITE, (23, 25), 3)
        pygame.draw.circle(s, WHITE, (77, 30), 3)

    elif base == "Void":
        pygame.draw.line(s, (255, 40, 90), (20, 20), (80, 80), 5)
        pygame.draw.line(s, (255, 40, 90), (80, 20), (20, 80), 5)

    # Special Pokémon
    if name == "Evil MissingNo":
        pygame.draw.line(s, (255, 20, 70), (10, 10), (90, 90), 7)
        pygame.draw.line(s, (255, 20, 70), (90, 10), (10, 90), 7)
        pygame.draw.circle(s, (255, 30, 70), (50, 50), 34, 3)

    elif name == "Good MissingNo":
        pygame.draw.circle(s, (220, 255, 255), (50, 50), 32, 3)
        pygame.draw.rect(s, (220, 255, 255), (36, 49, 28, 5))

    elif name == "Frolren":
        pygame.draw.polygon(s, WHITE, [
            (28, 14), (14, -5), (42, 12)
        ])
        pygame.draw.polygon(s, WHITE, [
            (67, 14), (86, -5), (58, 12)
        ])
        pygame.draw.circle(s, (80, 210, 255), (50, 50), 30, 3)

    elif name == "Dialga":
        pygame.draw.polygon(s, (180, 220, 255), [
            (50, 0), (63, 24), (50, 35), (37, 24)
        ])
        pygame.draw.circle(s, (60, 180, 255), (50, 52), 9)

    elif name == "Lucario":
        pygame.draw.polygon(s, dark_colour, [
            (25, 17), (15, -2), (38, 13)
        ])
        pygame.draw.polygon(s, dark_colour, [
            (70, 17), (85, -2), (62, 13)
        ])
        pygame.draw.circle(s, (255, 210, 70), (50, 53), 8)

    elif name == "Suicune":
        pygame.draw.polygon(s, (100, 220, 255), [
            (28, 12), (5, -2), (30, 22)
        ])
        pygame.draw.polygon(s, (100, 220, 255), [
            (72, 12), (95, -2), (70, 22)
        ])
        pygame.draw.arc(s, (40, 130, 255), (10, 35, 80, 50), 0, math.pi, 5)

    elif name == "Gyarados":
        pygame.draw.polygon(s, (255, 220, 70), [
            (15, 55), (0, 42), (22, 45)
        ])
        pygame.draw.polygon(s, (255, 220, 70), [
            (85, 55), (100, 42), (78, 45)
        ])

    elif name == "Morpeko":
        pygame.draw.ellipse(s, (245, 220, 170), (25, 15, 50, 50))
        pygame.draw.circle(s, BLACK, (41, 32), 5)
        pygame.draw.circle(s, BLACK, (60, 32), 5)
        pygame.draw.circle(s, (255, 230, 60), (50, 57), 8)

    elif name == "Luxray":
        pygame.draw.polygon(s, BLACK, [
            (25, 20), (10, -2), (39, 16)
        ])
        pygame.draw.polygon(s, BLACK, [
            (72, 20), (90, -2), (62, 16)
        ])
        pygame.draw.circle(s, GOLD, (41, 29), 6)
        pygame.draw.circle(s, GOLD, (61, 29), 6)

    return pygame.transform.smoothscale(s, (size, size))


@functools.lru_cache(maxsize=256)
def get_sprite(name, types="Unknown", size=160):
    # Each sprite is drawn once, then reused every frame
    return make_sprite(name, types, size)


# ==========================================
# GAME
# ==========================================

class Game:
    def __init__(self):
        self.team = new_team()
        self.pc = []
        self.active = 0
        self.enemy = None
        self.defeated_enemy = None

        self.mode = "menu"
        self.return_mode = "menu"

        self.message = "Welcome to Pokemon: The New World v13.0!"

        self.balls = {
            "Poke Ball": 10,
            "Great Ball": 5,
            "Ultra Ball": 2
        }

        self.avatar_turns = 0
        self.avatar_used = False

        self.coins = START_COINS
        self.trophies = 0
        self.tournament = None

        self.buttons = []
        self.popup = ""
        self.popup_colour = WHITE
        self.flash = 0

        self.animation = None
        self.animation_start = 0
        self.pending_enemy_turn = False

        self.pc_page = 0

        if storage_read():
            self.message = "Save file found! Press LOAD to continue."

    # ======================================
    # SAVE / LOAD
    # ======================================

    def save_game(self):
        if self.tournament:
            self.message = "Finish the tournament before saving!"
            return

        if self.enemy:
            self.message = "Finish or run from your battle before saving!"
            return

        data = {
            "version": 1,
            "team": [creature_to_dict(c) for c in self.team],
            "pc": [creature_to_dict(c) for c in self.pc],
            "active": self.active,
            "balls": self.balls,
            "coins": self.coins,
            "trophies": self.trophies
        }

        try:
            storage_write(json.dumps(data))
            self.message = "Game saved!"
        except Exception:
            self.message = "Could not save the game."

    def load_game(self):
        text = storage_read()

        if not text:
            self.message = "No save file found."
            return

        try:
            data = json.loads(text)
            team = [creature_from_dict(d) for d in data["team"]]
            pc = [creature_from_dict(d) for d in data.get("pc", [])]
            if not team:
                raise ValueError("empty team")
        except Exception:
            self.message = "The save file is damaged and could not be loaded."
            return

        self.team = team
        self.pc = pc
        self.active = min(max(0, data.get("active", 0)), len(team) - 1)
        for name in self.balls:
            self.balls[name] = int(data.get("balls", {}).get(name, 0))
        self.coins = int(data.get("coins", START_COINS))
        self.trophies = int(data.get("trophies", 0))
        self.tournament = None

        self.enemy = None
        self.defeated_enemy = None
        self.avatar_turns = 0
        self.avatar_used = False
        self.animation = None
        self.pending_enemy_turn = False
        self.pc_page = 0
        self.mode = "menu"
        self.send_out_healthy()
        self.message = "Game loaded!"

    # ======================================
    # HEAL (free)
    # ======================================

    def heal_team(self):
        if self.tournament:
            self.message = "No healing during the tournament!"
            return

        if self.enemy:
            self.message = "Finish or run from your battle before healing!"
            return

        # Restores full HP, which also revives fainted Pokemon
        for pokemon in self.team:
            pokemon.heal(pokemon.max_hp)

        self.send_out_healthy()

        # Keep the healed HP in the save file
        self.save_game()

        if self.message == "Game saved!":
            self.message = "Your Pokémon have been fully healed!"
        else:
            self.message = "Your Pokémon have been fully healed! (Could not save.)"

    @property
    def pokemon(self):
        return self.team[self.active]

    def text(self, value, x, y, font=FONT, colour=WHITE):
        screen.blit(font.render(str(value), True, colour), (x, y))

    def centred(self, value, y, font=FONT, colour=WHITE):
        image = font.render(str(value), True, colour)
        screen.blit(image, image.get_rect(center=(500, y)))

    def panel(self, rect, colour=DARK):
        pygame.draw.rect(screen, colour, rect, border_radius=12)
        pygame.draw.rect(screen, BORDER, rect, 2, border_radius=12)

    def button(self, label, rect, action, colour=BLUE):
        r = pygame.Rect(rect)
        pygame.draw.rect(screen, colour, r, border_radius=9)
        pygame.draw.rect(screen, (150, 185, 235), r, 2, border_radius=9)

        image = SMALL.render(label, True, WHITE)
        screen.blit(image, image.get_rect(center=r.center))
        self.buttons.append((r, action))

    def background(self):
        screen.fill((20, 30, 60))
        pygame.draw.rect(screen, (35, 70, 115), (0, 0, 1000, 450))
        pygame.draw.rect(screen, (35, 105, 80), (0, 450, 1000, 250))

        # Background hills
        pygame.draw.ellipse(screen, (40, 90, 105), (-100, 350, 500, 160))
        pygame.draw.ellipse(screen, (45, 100, 90), (400, 350, 600, 160))

        # Sun
        pygame.draw.circle(screen, (255, 210, 100), (850, 90), 42)
        pygame.draw.circle(screen, (255, 235, 150), (850, 90), 30)

        # Grass
        for x in range(0, 1000, 35):
            pygame.draw.line(screen, (45, 135, 80),
                             (x, 475), (x - 5, 455), 2)

    def health_bar(self, x, y, width, creature):
        pygame.draw.rect(screen, (55, 55, 70),
                         (x, y, width, 16), border_radius=5)

        ratio = max(0, creature.hp / creature.max_hp)

        colour = (
            GREEN if ratio > 0.5
            else GOLD if ratio > 0.2
            else RED
        )

        if ratio > 0:
            pygame.draw.rect(screen, colour,
                             (x, y, int(width * ratio), 16),
                             border_radius=5)

    # ======================================
    # ANIMATIONS
    # ======================================

    def start_animation(self, move, attacker_is_player):
        move_lower = move.lower()

        if any(w in move_lower for w in
               ("fire", "flame", "ember", "blaze", "magma")):
            kind = "Fire"
        elif any(w in move_lower for w in
                 ("water", "aqua", "hydro", "tidal")):
            kind = "Water"
        elif any(w in move_lower for w in
                 ("thunder", "spark", "volt", "electric")):
            kind = "Electric"
        elif any(w in move_lower for w in
                 ("ice", "frost", "blizzard", "glacier")):
            kind = "Ice"
        elif any(w in move_lower for w in
                 ("leaf", "vine", "grass", "thorn")):
            kind = "Grass"
        elif any(w in move_lower for w in
                 ("void", "null", "rift")):
            kind = "Void"
        elif any(w in move_lower for w in
                 ("shadow", "dark", "night", "phantom")):
            kind = "Ghost"
        elif any(w in move_lower for w in
                 ("dragon", "meteor", "star", "cosmic")):
            kind = "Dragon"
        elif any(w in move_lower for w in
                 ("iron", "metal", "steel")):
            kind = "Steel"
        else:
            kind = "Psychic"

        self.animation = {
            "kind": kind,
            "player": attacker_is_player,
            "move": move
        }
        self.animation_start = pygame.time.get_ticks()

    def update_animation(self):
        if not self.animation:
            return

        elapsed = pygame.time.get_ticks() - self.animation_start

        if elapsed >= 550:
            self.animation = None

            if self.pending_enemy_turn:
                self.pending_enemy_turn = False
                self.enemy_attack()

    def draw_animation(self):
        if not self.animation:
            return

        elapsed = pygame.time.get_ticks() - self.animation_start
        progress = min(1, elapsed / 550)

        if self.animation["player"]:
            start, end = (340, 310), (750, 260)
        else:
            start, end = (750, 260), (340, 310)

        x = int(start[0] + (end[0] - start[0]) * progress)
        y = int(start[1] + (end[1] - start[1]) * progress)

        kind = self.animation["kind"]
        colour = TYPE_COLOURS.get(kind, WHITE)

        if kind == "Fire":
            pygame.draw.circle(screen, (255, 80, 20), (x, y), 28)
            pygame.draw.circle(screen, (255, 220, 60), (x, y), 15)

        elif kind == "Water":
            pygame.draw.circle(screen, (50, 150, 255), (x, y), 23)
            pygame.draw.circle(screen, (180, 235, 255), (x, y), 12)

        elif kind == "Electric":
            pygame.draw.lines(screen, GOLD, False, [
                (x - 25, y - 20), (x + 5, y - 5),
                (x - 5, y + 5), (x + 25, y + 20)
            ], 7)

        elif kind == "Ice":
            pygame.draw.polygon(screen, WHITE, [
                (x, y - 30), (x + 20, y),
                (x, y + 30), (x - 20, y)
            ])
            pygame.draw.circle(screen, colour, (x, y), 13)

        elif kind == "Grass":
            pygame.draw.ellipse(screen, colour, (x - 24, y - 10, 48, 20))

        elif kind == "Ghost":
            pygame.draw.circle(screen, colour, (x, y), 24, 6)
            pygame.draw.circle(screen, colour, (x, y), 12, 3)

        elif kind == "Steel":
            pygame.draw.rect(screen, colour, (x - 20, y - 20, 40, 40))

        elif kind == "Void":
            pygame.draw.circle(screen, (60, 20, 100), (x, y), 28)
            pygame.draw.circle(screen, (255, 40, 140), (x, y), 28, 4)
            pygame.draw.line(screen, (255, 40, 140),
                             (x - 14, y - 14), (x + 14, y + 14), 4)
            pygame.draw.line(screen, (255, 40, 140),
                             (x + 14, y - 14), (x - 14, y + 14), 4)

        else:
            pygame.draw.circle(screen, colour, (x, y), 25)
            pygame.draw.circle(screen, WHITE, (x, y), 12)

        self.text(self.animation["move"], 420, 390, SMALL, GOLD)

    # ======================================
    # MENUS
    # ======================================

    def draw_menu(self):
        self.background()

        self.centred("POKEMON: THE NEW WORLD", 95, BIG, GOLD)
        self.centred("VERSION 13.0 - SHOP & TOURNAMENT UPDATE", 150)
        self.centred(self.message, 205, SMALL)

        # Coins and trophies
        self.panel((20, 20, 210, 70))
        self.text(f"Coins: {self.coins}", 38, 30, SMALL, GOLD)
        self.text(f"Trophies: {self.trophies}", 38, 55, SMALL, GOLD)

        # Show Flame on the main menu
        screen.blit(get_sprite("Flame", "Fire", 170), (415, 225))

        label = "CONTINUE BATTLE" if self.enemy else "START BATTLE"
        self.button(label, (300, 405, 195, 52), "battle")
        self.button("TOURNAMENT", (505, 405, 195, 52),
                    "tournament", (120, 75, 160))
        self.button("TEAM", (300, 467, 127, 45), "team")
        self.button("POKE BALLS", (437, 467, 126, 45), "balls")
        self.button("HEAL", (573, 467, 127, 45), "heal", (190, 70, 110))
        self.button("POKEMON PC", (300, 522, 195, 45), "pc")
        self.button("SHOP", (505, 522, 195, 45), "shop", (170, 120, 30))
        if WEB:
            self.button("SAVE", (300, 577, 195, 45), "save", (45, 115, 75))
            self.button("LOAD", (505, 577, 195, 45), "load", (45, 115, 75))
        else:
            self.button("SAVE", (300, 577, 127, 45), "save", (45, 115, 75))
            self.button("LOAD", (437, 577, 126, 45), "load", (45, 115, 75))
            self.button("QUIT", (573, 577, 127, 45), "quit", (145, 50, 60))

    def draw_battle(self):
        self.background()

        if not self.enemy:
            self.mode = "menu"
            return

        p, e = self.pokemon, self.enemy

        self.panel((555, 35, 405, 115))
        self.text(e.name, 580, 48, BIG)
        self.text("Type: " + e.types, 580, 85, SMALL, GOLD)
        self.text(f"Lv {e.level}", 880, 55, SMALL, GOLD)
        self.text(f"HP: {e.hp}/{e.max_hp}", 580, 108, SMALL)
        self.health_bar(580, 130, 340, e)

        self.panel((35, 350, 420, 120))
        self.text(p.name, 60, 365, BIG)
        self.text("Type: " + p.types, 60, 400, SMALL, GOLD)
        self.text(f"HP: {p.hp}/{p.max_hp}", 60, 425, SMALL)
        self.text(f"Lv {p.level}", 360, 372, SMALL, GOLD)
        self.text(f"XP {p.xp}/{xp_needed(p.level)}", 260, 425, SMALL)
        self.health_bar(60, 455, 350, p)

        screen.blit(get_sprite(e.name, e.types), (680, 155))
        screen.blit(get_sprite(p.name, p.types), (160, 190))

        if self.tournament:
            trainer = TOURNAMENT[self.tournament["round"]][0]
            left = len(self.tournament["team"]) - self.tournament["index"]
            self.panel((20, 20, 330, 60))
            self.text(f"ROUND {self.tournament['round'] + 1} - {trainer}",
                      35, 28, SMALL, GOLD)
            self.text(f"Pokemon left: {left}", 35, 52, SMALL)

        if self.avatar_turns:
            self.text("TRUE SUN AVATAR!", 370, 25, FONT, GOLD)
            self.text(f"{self.avatar_turns} turns remaining",
                      390, 58, SMALL, GOLD)

        if self.flash:
            pygame.draw.circle(screen, GOLD, (750, 250), 85, 7)

        if self.popup:
            self.text(self.popup, 730, 155, BIG, self.popup_colour)

        self.draw_animation()

        self.panel((20, 490, 960, 190))
        self.text(self.message, 40, 505, SMALL, GOLD)

        self.button("ATTACKS", (40, 550, 160, 45), "moves")
        self.button("SWITCH TEAM", (215, 550, 160, 45), "team")
        self.button("SUN AVATAR", (390, 550, 160, 45),
                    "avatar", (145, 90, 35))
        self.button("POKE BALLS", (565, 550, 150, 45), "balls")
        self.button("FORFEIT" if self.tournament else "RUN",
                    (730, 550, 100, 45), "run", (130, 55, 60))
        self.button("MENU", (845, 550, 110, 45), "menu")

    def draw_moves(self):
        self.draw_battle()
        self.buttons.clear()

        self.panel((250, 165, 500, 315))
        self.text("CHOOSE YOUR ATTACK", 335, 180, BIG, GOLD)

        for i, (move, power) in enumerate(self.pokemon.moves):
            self.button(
                f"{i + 1}. {move} - Power {power}",
                (300, 235 + i * 53, 400, 43),
                ("move", i)
            )

        self.button("BACK", (420, 440, 160, 35), "back")

    def draw_team(self):
        self.background()
        self.centred("YOUR POKEMON TEAM", 25, BIG, GOLD)

        for i, p in enumerate(self.team[:12]):
            x = 25 + (i % 3) * 325
            y = 75 + (i // 3) * 145

            self.panel((x, y, 300, 130))
            screen.blit(get_sprite(p.name, p.types, 100),
                        (x + 5, y + 10))

            self.text(p.name, x + 110, y + 10, SMALL)
            self.text(f"Lv {p.level}", x + 245, y + 10, SMALL, GOLD)
            self.text("Type: " + p.types, x + 110, y + 32, SMALL)
            self.text(f"HP {p.hp}/{p.max_hp}", x + 110, y + 52, SMALL)
            self.health_bar(x + 110, y + 75, 160, p)

            if i == self.active:
                self.text("ACTIVE", x + 110, y + 100, SMALL, GOLD)
            elif p.fainted:
                self.text("FAINTED", x + 110, y + 100, SMALL, RED)
            else:
                self.button("SELECT", (x + 110, y + 95, 120, 28),
                            ("switch", i))

        self.button("BACK", (790, 650, 160, 42), "back")

    def draw_balls(self):
        self.background()
        self.centred("POKE BALLS", 80, BIG, GOLD)
        self.panel((250, 150, 500, 370))

        for i, (name, amount) in enumerate(self.balls.items()):
            y = 210 + i * 85
            self.text(f"{name}: {amount}", 310, y, FONT)

            if amount > 0:
                self.button("THROW", (550, y - 5, 140, 45),
                            ("catch", name))

        if self.enemy:
            self.text("Opponent: " + self.enemy.name,
                      310, 460, SMALL, GOLD)
        else:
            self.text("Start a battle to catch Pokemon!",
                      310, 460, SMALL)

        self.button("BACK", (420, 555, 160, 45), "back")

    def draw_pc(self):
        self.background()
        self.centred("POKEMON PC", 25, BIG, GOLD)

        self.panel((25, 80, 455, 535))
        self.panel((520, 80, 455, 535))

        self.text("YOUR TEAM - DEPOSIT", 45, 95, FONT, GOLD)
        self.text("PC STORAGE - WITHDRAW", 540, 95, FONT, GOLD)

        for i, p in enumerate(self.team[:12]):
            y = 140 + i * 36
            self.text(f"{i + 1}. {p.name} ({p.hp}/{p.max_hp})",
                      45, y, SMALL)
            self.button("DEPOSIT", (335, y - 5, 120, 32),
                        ("deposit", i))

        start = self.pc_page * 12

        for i, p in enumerate(self.pc[start:start + 12]):
            y = 140 + i * 36
            self.text(f"{start + i + 1}. {p.name} ({p.hp}/{p.max_hp})",
                      540, y, SMALL)
            self.button("WITHDRAW", (830, y - 5, 120, 32),
                        ("withdraw", start + i))

        self.button("PREVIOUS", (535, 570, 130, 35), "pc_previous")
        self.button("NEXT", (815, 570, 130, 35), "pc_next")
        self.button("BACK", (420, 635, 160, 45), "back")

    def draw_shop(self):
        self.background()
        self.centred("POKE MART", 70, BIG, GOLD)
        self.panel((200, 120, 600, 430))
        self.text(f"Your coins: {self.coins}", 240, 140, FONT, GOLD)

        for i, (name, price) in enumerate(SHOP_PRICES.items()):
            y = 210 + i * 95
            self.text(name, 240, y, FONT)
            self.text(f"{price} coins  -  you have {self.balls[name]}",
                      240, y + 32, SMALL)
            self.button("BUY 1", (560, y, 100, 40), ("buy", (name, 1)),
                        (45, 115, 75))
            self.button("BUY 5", (670, y, 100, 40), ("buy", (name, 5)),
                        (45, 115, 75))

        self.text("Win battles and tournaments to earn coins!",
                  240, 500, SMALL)
        self.centred(self.message, 585, SMALL, GOLD)
        self.button("BACK", (420, 620, 160, 45), "back")

    def draw_tournament(self):
        self.background()
        self.centred("BATTLE TOURNAMENT", 45, BIG, GOLD)

        t = self.tournament
        self.panel((150, 90, 700, 400))

        for i, (trainer, level, names, prize) in enumerate(TOURNAMENT):
            y = 115 + i * 72
            if t and i < t["round"]:
                status, colour = "BEATEN", GREEN
            elif t and i == t["round"] and not t.get("won"):
                status, colour = "NEXT", GOLD
            else:
                status, colour = "", WHITE

            self.text(f"Round {i + 1}: {trainer}", 180, y, FONT, colour)
            self.text(f"Lv {level}  -  {len(names)} Pokemon  -  "
                      f"Prize {prize} coins", 180, y + 30, SMALL)
            if status:
                self.text(status, 720, y + 8, FONT, colour)

        self.centred(self.message, 515, SMALL, GOLD)

        if t and t.get("won"):
            self.button("CLAIM TROPHY", (350, 550, 300, 55),
                        "claim_trophy", (170, 120, 30))
        else:
            self.button(f"START ROUND {t['round'] + 1}", (300, 550, 250, 55),
                        "next_round", (120, 75, 160))
            self.button("TEAM", (560, 550, 140, 55), "team")
            self.button("FORFEIT", (400, 620, 200, 45),
                        "forfeit", (130, 55, 60))

    def draw_victory(self):
        self.background()
        self.centred("VICTORY!", 150, BIG, GOLD)

        beaten = self.defeated_enemy
        if beaten:
            self.centred(f"You defeated {beaten.name}!", 220)
            screen.blit(get_sprite(beaten.name, beaten.types),
                        (420, 260))

        self.panel((150, 425, 700, 70))
        self.centred(self.message, 460, SMALL, GOLD)

        self.button("NEXT BATTLE", (350, 510, 300, 55), "battle")
        self.button("MAIN MENU", (350, 580, 300, 50), "menu")

    def draw_defeat(self):
        self.background()
        self.centred("TEAM DEFEATED", 190, BIG, RED)
        self.centred("Your Pokemon have been healed!", 250)
        self.centred(self.message, 300, SMALL, GOLD)
        self.button("MAIN MENU", (350, 400, 300, 55), "menu")

    # ======================================
    # BATTLE SYSTEM
    # ======================================

    def show_hit(self, damage, colour):
        self.popup = f"-{damage}"
        self.popup_colour = colour
        self.flash = 12

    def send_out_healthy(self):
        if not self.pokemon.fainted:
            return True

        for i, p in enumerate(self.team):
            if not p.fainted:
                self.active = i
                return True

        return False

    def team_defeated(self):
        for pokemon in self.team:
            pokemon.heal(pokemon.max_hp)

        if self.tournament:
            round_number = self.tournament["round"] + 1
            self.tournament = None
            self.message = f"You were knocked out of the tournament in Round {round_number}."
        else:
            self.message = ""

        self.active = 0
        self.enemy = None
        self.avatar_turns = 0
        self.pending_enemy_turn = False
        self.mode = "defeat"

    # ======================================
    # REWARDS
    # ======================================

    def reward_win(self, enemy):
        """Give XP to the active Pokemon and coins. Returns a message."""
        xp = xp_reward(enemy)
        coins = 0 if self.tournament else coin_reward(enemy)
        self.coins += coins

        level_ups = gain_xp(self.pokemon, xp)
        text = f"+{xp} XP"
        if coins:
            text += f", +{coins} coins"
        if level_ups:
            text += ". " + " ".join(level_ups)
        return text

    # ======================================
    # SHOP
    # ======================================

    def buy(self, name, amount):
        cost = SHOP_PRICES[name] * amount
        if self.coins < cost:
            self.message = f"Not enough coins! You need {cost}."
            return

        self.coins -= cost
        self.balls[name] += amount
        self.message = f"You bought {amount} {name}{'s' if amount > 1 else ''}!"

    # ======================================
    # TOURNAMENT
    # ======================================

    def start_tournament(self):
        if self.enemy:
            self.message = "Finish your current battle first!"
            return

        # Everyone starts the tournament fully healed
        for pokemon in self.team:
            pokemon.heal(pokemon.max_hp)

        self.tournament = {"round": 0, "team": [], "index": 0}
        self.mode = "tournament"
        self.message = "Beat all 5 trainers to win a trophy!"

    def next_round(self):
        t = self.tournament
        if not t or t.get("won"):
            return

        if not self.send_out_healthy():
            self.message = "Your team needs to recover!"
            return

        t["team"] = trainer_team(t["round"])
        t["index"] = 0
        self.enemy = t["team"][0]

        self.avatar_turns = 0
        self.avatar_used = False
        self.animation = None
        self.pending_enemy_turn = False
        self.mode = "battle"

        trainer = TOURNAMENT[t["round"]][0]
        self.message = f"{trainer} sent out {self.enemy.name}!"

    def tournament_pokemon_beaten(self, enemy, reward_text):
        t = self.tournament
        trainer, level, names, prize = TOURNAMENT[t["round"]]
        t["index"] += 1

        if t["index"] < len(t["team"]):
            self.enemy = t["team"][t["index"]]
            self.message = (f"{enemy.name} fainted! {reward_text}. "
                            f"{trainer} sent out {self.enemy.name}!")
            return

        # Round won
        self.enemy = None
        self.avatar_turns = 0
        self.coins += prize
        t["round"] += 1

        if t["round"] >= len(TOURNAMENT):
            t["won"] = True
            self.trophies += 1
            self.message = (f"YOU BEAT {trainer.upper()}! You are the CHAMPION! "
                            f"+{prize} coins")
        else:
            # Team recovers half their HP between rounds
            for pokemon in self.team:
                pokemon.heal(pokemon.max_hp // 2)
            self.message = (f"You beat {trainer}! +{prize} coins. "
                            f"Your team recovered some HP.")

        self.mode = "tournament"

    def end_tournament(self, message):
        self.tournament = None
        self.enemy = None
        self.avatar_turns = 0
        self.animation = None
        self.pending_enemy_turn = False
        self.mode = "menu"
        self.message = message

    def start_battle(self):
        # Resume a battle that was left via the MENU button
        if self.enemy:
            self.mode = "battle"
            self.message = f"The battle with {self.enemy.name} continues!"
            return

        if not self.team or all(p.fainted for p in self.team):
            self.message = "Your team needs to recover!"
            return

        self.send_out_healthy()
        self.enemy = random_enemy()

        self.avatar_turns = 0
        self.avatar_used = False
        self.animation = None
        self.pending_enemy_turn = False
        self.mode = "battle"

        if self.enemy.types == "Boss":
            self.message = f"BOSS BATTLE! {self.enemy.name} appeared!"
        elif self.enemy.name == "NYSTRIA":
            self.message = "The air tears open... the legendary NYSTRIA appeared!"
        else:
            self.message = f"A wild {self.enemy.name} appeared!"

    # ======================================
    # PLAYER ATTACK
    # ======================================

    def player_attack(self, index):
        if not self.enemy:
            return

        if self.animation:
            self.message = "Wait for the attack animation to finish!"
            return

        if index < 0 or index >= len(self.pokemon.moves):
            return

        p, e = self.pokemon, self.enemy

        if p.fainted:
            self.message = "Choose a healthy Pokemon!"
            return

        move, power = p.moves[index]
        damage = power + random.randint(5, 15) + p.bonus

        if self.avatar_turns and p.name in SUN_TEAM:
            damage += 40

        move_type = get_move_type(move)
        super_effective = (move_type == "Ice"
                           and "Fire" in e.types.split("/"))

        if super_effective:
            damage = int(damage * 2.5)

        self.start_animation(move, True)
        e.take_damage(damage)
        self.show_hit(damage, GOLD)

        if e.fainted:
            self.pending_enemy_turn = False
            reward_text = self.reward_win(e)

            if self.tournament:
                self.tournament_pokemon_beaten(e, reward_text)
                return

            self.message = f"{e.name} was defeated! {reward_text}"
            self.defeated_enemy = e
            self.enemy = None
            self.avatar_turns = 0
            self.mode = "victory"
        else:
            self.message = f"{p.name} used {move}! {damage} damage!"
            if super_effective:
                self.message = "SUPER EFFECTIVE! " + self.message
            self.pending_enemy_turn = True

    # ======================================
    # ENEMY ATTACK
    # ======================================

    def enemy_attack(self):
        if not self.enemy or self.animation:
            return

        if self.pokemon.fainted:
            if not self.send_out_healthy():
                self.team_defeated()
                return

        p, e = self.pokemon, self.enemy
        move, power = random.choice(e.moves)

        damage = power + random.randint(3, 10) + e.bonus
        move_type = get_move_type(move)
        super_effective = (move_type == "Ice"
                           and "Fire" in p.types.split("/"))

        if super_effective:
            damage = int(damage * 2.5)

        if self.avatar_turns:
            damage = max(1, damage - 15)
            self.avatar_turns -= 1

        self.start_animation(move, False)
        p.take_damage(damage)
        self.show_hit(damage, RED)

        if super_effective:
            self.message = (f"SUPER EFFECTIVE! {e.name}'s {move} "
                            f"hit {p.name} hard! -{damage} HP!")
        else:
            self.message = f"{e.name} used {move}! You lost {damage} HP!"

        if p.fainted:
            fainted_name = p.name

            if self.send_out_healthy():
                self.message = (
                    f"{fainted_name} fainted! "
                    f"{self.pokemon.name} was sent out!"
                )
            else:
                self.team_defeated()

    # ======================================
    # SUN AVATAR
    # ======================================

    def activate_avatar(self):
        if self.animation:
            self.message = "Wait until the attack finishes!"
            return

        p = self.pokemon

        if self.avatar_used:
            self.message = "True Sun Avatar was already used!"
        elif p.fainted:
            self.message = "A fainted Pokemon cannot activate it!"
        elif p.name not in SUN_TEAM:
            self.message = "Only the Sun Team can use this!"
        else:
            self.avatar_turns = AVATAR_TURNS
            self.avatar_used = True
            p.heal(20)
            self.message = f"{p.name} activated TRUE SUN AVATAR!"

    # ======================================
    # SWITCH POKEMON
    # ======================================

    def switch_to(self, index):
        if self.animation:
            self.message = "Wait until the attack finishes!"
            return

        if index >= len(self.team):
            return

        if self.team[index].fainted:
            self.message = "That Pokemon has fainted!"
            return

        if index == self.active:
            self.message = "That Pokemon is already active!"
            return

        self.active = index
        self.message = f"{self.pokemon.name} joined the battle!"

        if self.return_mode == "battle" and self.enemy:
            self.mode = "battle"
            self.enemy_attack()

    # ======================================
    # POKEBALL CATCHING
    # ======================================

    def catch_pokemon(self, ball_name):
        if not self.enemy:
            self.message = "There is no Pokemon to catch!"
            return

        if self.enemy.fainted:
            self.message = "That Pokemon has already been defeated!"
            return

        if self.tournament:
            self.message = "You can't catch another trainer's Pokemon!"
            self.mode = "battle"
            return

        if self.enemy.types == "Boss":
            self.message = "You cannot catch this boss!"
            return

        if self.animation:
            self.message = "Wait until the attack finishes!"
            return

        if self.balls[ball_name] <= 0:
            self.message = "You have no " + ball_name + "s left!"
            return

        self.balls[ball_name] -= 1

        chances = {
            "Poke Ball": 0.35,
            "Great Ball": 0.60,
            "Ultra Ball": 0.85
        }

        chance = chances[ball_name]

        if self.enemy.hp < self.enemy.max_hp * 0.5:
            chance += 0.15

        if self.enemy.hp < self.enemy.max_hp * 0.25:
            chance += 0.15

        if self.enemy.name == "NYSTRIA":
            chance -= NYSTRIA_CATCH_PENALTY

        if random.random() < chance:
            caught = self.enemy
            self.enemy = None

            if len(self.team) < PARTY_LIMIT:
                self.team.append(caught)
                place = "your team"
            else:
                self.pc.append(caught)
                place = "your PC"

            self.message = f"You caught {caught.name}! Sent to {place}!"
            self.mode = "menu"
            self.animation = None
            self.pending_enemy_turn = False

        else:
            self.message = "The Pokemon broke free!"
            self.mode = "battle"
            self.enemy_attack()

    # ======================================
    # POKEMON PC
    # ======================================

    def deposit(self, index):
        if index >= len(self.team):
            return

        if len(self.team) <= 1:
            self.message = "You must keep at least one Pokemon!"
            return

        if not any(
            p.hp > 0
            for i, p in enumerate(self.team)
            if i != index
        ):
            self.message = "You need one healthy Pokemon on your team!"
            return

        pokemon = self.team.pop(index)
        self.pc.append(pokemon)

        if index == self.active:
            self.active = 0
        elif index < self.active:
            self.active -= 1

        self.send_out_healthy()
        self.message = f"{pokemon.name} was deposited!"

    def withdraw(self, index):
        if len(self.team) >= PARTY_LIMIT:
            self.message = "Your team is full!"
            return

        if index >= len(self.pc):
            return

        pokemon = self.pc.pop(index)
        self.team.append(pokemon)
        self.pc_page = min(self.pc_page, max(0, (len(self.pc) - 1) // 12))
        self.message = f"{pokemon.name} was withdrawn!"

    # ======================================
    # BUTTON ACTIONS
    # ======================================

    def do(self, action):
        if isinstance(action, tuple):
            kind, index = action

            if kind == "move":
                self.player_attack(index)
            elif kind == "switch":
                self.switch_to(index)
            elif kind == "catch":
                self.catch_pokemon(index)
            elif kind == "deposit":
                self.deposit(index)
            elif kind == "withdraw":
                self.withdraw(index)
            elif kind == "buy":
                self.buy(*index)

            return

        if action == "battle":
            self.start_battle()

        elif action == "moves" and self.mode == "battle":
            self.return_mode = "battle"
            self.mode = "moves"

        elif action == "team":
            if self.mode in ("menu", "battle", "tournament"):
                if self.animation:
                    self.message = "Wait until the attack finishes!"
                    return

                self.return_mode = self.mode
                self.mode = "team"

        elif action == "balls":
            if self.mode in ("menu", "battle"):
                self.return_mode = self.mode
                self.mode = "balls"

        elif action == "pc":
            self.return_mode = self.mode
            self.mode = "pc"

        elif action == "back":
            if self.mode in ("moves", "team", "balls", "pc", "shop"):
                self.mode = self.return_mode

        elif action == "shop":
            if self.mode == "menu":
                self.return_mode = "menu"
                self.mode = "shop"

        elif action == "tournament":
            if self.mode == "menu":
                self.start_tournament()

        elif action == "next_round":
            self.next_round()

        elif action == "forfeit":
            self.end_tournament("You left the tournament.")

        elif action == "claim_trophy":
            self.end_tournament(
                f"Trophy won! You now have {self.trophies} "
                f"troph{'y' if self.trophies == 1 else 'ies'}!")

        elif action == "avatar":
            self.activate_avatar()

        elif action == "run":
            if self.animation:
                self.message = "Wait until the attack finishes!"
                return

            if self.tournament:
                self.end_tournament("You forfeited the tournament.")
                return

            self.enemy = None
            self.avatar_turns = 0
            self.animation = None
            self.pending_enemy_turn = False
            self.mode = "menu"
            self.message = "You escaped from battle!"

        elif action == "menu":
            if self.animation:
                self.message = "Wait until the attack finishes!"
                return

            if self.tournament:
                self.message = "You can't leave mid-tournament! Use FORFEIT."
                return

            self.mode = "menu"

        elif action == "pc_previous":
            self.pc_page = max(0, self.pc_page - 1)

        elif action == "pc_next":
            max_page = max(0, (len(self.pc) - 1) // 12)
            self.pc_page = min(max_page, self.pc_page + 1)

        elif action == "heal":
            self.heal_team()

        elif action == "save":
            self.save_game()

        elif action == "load":
            self.load_game()

        elif action == "quit":
            pygame.quit()
            sys.exit()

    # ======================================
    # KEYBOARD
    # ======================================

    def handle_key(self, key):
        if key == pygame.K_ESCAPE:
            self.do("back")

        elif key == pygame.K_b and self.mode == "menu":
            self.do("battle")

        elif key == pygame.K_a and self.mode == "battle":
            self.do("moves")

        elif pygame.K_1 <= key <= pygame.K_4 and self.mode == "moves":
            self.do(("move", key - pygame.K_1))

    # ======================================
    # MAIN LOOP
    # ======================================

    async def run(self):
        screens = {
            "menu": self.draw_menu,
            "battle": self.draw_battle,
            "moves": self.draw_moves,
            "team": self.draw_team,
            "balls": self.draw_balls,
            "pc": self.draw_pc,
            "victory": self.draw_victory,
            "shop": self.draw_shop,
            "tournament": self.draw_tournament,
            "defeat": self.draw_defeat
        }

        while True:
            clock.tick(FPS)
            self.update_animation()

            for event in pygame.event.get():
                if event.type == pygame.QUIT and not WEB:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx = event.pos[0] * WIDTH // WINDOW_WIDTH
                        my = event.pos[1] * HEIGHT // WINDOW_HEIGHT

                        for rect, action in self.buttons:
                            if rect.collidepoint((mx, my)):
                                self.do(action)
                                break

                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            if self.flash > 0:
                self.flash -= 1
            else:
                self.popup = ""

            self.buttons = []
            screens[self.mode]()

            pygame.transform.scale(
                screen,
                (WINDOW_WIDTH, WINDOW_HEIGHT),
                window
            )

            pygame.display.flip()

            # Lets the browser update between frames
            await asyncio.sleep(0)


# ==========================================
# START GAME
# ==========================================

if __name__ == "__main__":
    asyncio.run(Game().run())