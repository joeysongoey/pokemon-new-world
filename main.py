import asyncio
import functools
import json
import os
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
pygame.display.set_caption("Pokemon: The New World v18.2")
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


# ==========================================
# 76 NEW POKEMON (v14.0)
# ==========================================
# Each row: (number, name, types, sprite body, HP, attack bonus, rarity,
#            Pokedex entry, four moves as (name, power, type))
NEW_SPECIES_DATA = [
    (67, "Mossaur", "Grass", "quad", 160, 2, "common",
     "Moss grows across its back, which keeps it cool in the hottest sun.",
     [("Moss Slam", 40, "Grass"), ("Leaf Crush", 45, "Grass"),
      ("Spore Bite", 36, "Poison"), ("Bark Armor", 34, "Steel")]),
    (68, "Vinefang", "Grass/Dark", "quad", 170, 2, "common",
     "It hides in tangled vines and strikes from the shadows with sharp fangs.",
     [("Vine Snare", 40, "Grass"), ("Shade Fang", 45, "Dark"),
      ("Thorn Lash", 42, "Grass"), ("Night Coil", 36, "Dark")]),
    (69, "Bloomantis", "Grass/Bug", "bug", 150, 2, "common",
     "Its wings unfold like flower petals, dusting the air with sweet pollen.",
     [("Pollen Slash", 42, "Bug"), ("Petal Blade", 44, "Grass"),
      ("Sting Dance", 38, "Bug"), ("Bloom Shield", 32, "Grass")]),
    (70, "Fernox", "Grass/Steel", "plant", 165, 2, "common",
     "Its armour-like fronds are as tough as steel and grow back quickly.",
     [("Fern Blade", 44, "Grass"), ("Iron Frond", 46, "Steel"),
      ("Razor Fern", 40, "Grass"), ("Steel Roots", 36, "Steel")]),
    (71, "Petalisk", "Grass/Dragon", "dragon", 175, 2, "common",
     "A serpent-like Pokemon whose coils bloom with petals as it moves.",
     [("Petal Storm", 42, "Grass"), ("Dragon Thorn", 46, "Dragon"),
      ("Lotus Fang", 40, "Grass"), ("Coil Rush", 36, "Dragon")]),
    (72, "Rootusk", "Grass/Ground", "quad", 170, 2, "common",
     "It digs up roots with its tusks and makes the ground tremble.",
     [("Root Quake", 44, "Ground"), ("Mossy Tusk", 42, "Grass"),
      ("Earth Vine", 40, "Ground"), ("Bramble Hide", 34, "Grass")]),
    (73, "Blossomoth", "Grass/Fairy", "bug", 150, 2, "common",
     "A gentle moth with glowing petal wings that calm anyone who sees them.",
     [("Blossom Dust", 40, "Fairy"), ("Moon Petal", 44, "Fairy"),
      ("Leaf Flutter", 42, "Grass"), ("Sweet Scale", 34, "Bug")]),
    (74, "Brambleon", "Grass/Fighting", "plant", 160, 2, "common",
     "Thorny vines wrap around its arms, ready for a fight.",
     [("Bramble Jab", 44, "Fighting"), ("Thorn Kick", 46, "Grass"),
      ("Knuckle Vine", 42, "Fighting"), ("Spiky Guard", 34, "Grass")]),
    (75, "Cindrake", "Fire/Dragon", "dragon", 175, 3, "common",
     "A dragon born in a volcano, its tail glows like burning coal.",
     [("Ember Coil", 42, "Fire"), ("Wyrm Flare", 46, "Dragon"),
      ("Scorch Tail", 40, "Fire"), ("Ash Talon", 36, "Dragon")]),
    (76, "Ashpup", "Fire", "quad", 140, 2, "common",
     "A playful puppy whose fur leaves a trail of ash wherever it runs.",
     [("Ash Nip", 36, "Fire"), ("Cinder Pounce", 42, "Fire"),
      ("Ember Yap", 38, "Fire"), ("Soot Bark", 34, "Fire")]),
    (77, "Volcaruff", "Fire/Rock", "quad", 165, 2, "common",
     "A rocky pup with lava in its veins. It is warm to the touch.",
     [("Lava Fang", 44, "Fire"), ("Rock Lava", 42, "Rock"),
      ("Molten Bite", 40, "Fire"), ("Stone Howl", 36, "Rock")]),
    (78, "Flarephant", "Fire/Ground", "golem", 180, 2, "common",
     "Its trunk spits sparks and its heavy feet shake the ground.",
     [("Flare Stomp", 46, "Fire"), ("Quake Trunk", 42, "Ground"),
      ("Magma Spray", 40, "Fire"), ("Mud Trumpet", 36, "Ground")]),
    (79, "Emberowl", "Fire/Flying", "bird", 155, 2, "common",
     "This owl's wings are wrapped in fire, and it can see in the dark.",
     [("Ember Talon", 44, "Fire"), ("Sky Ember", 42, "Flying"),
      ("Wing Blaze", 40, "Fire"), ("Feather Flare", 36, "Flying")]),
    (80, "Scorchilla", "Fire/Fighting", "imp", 165, 2, "common",
     "A fast fighter whose kicks leave scorch marks on the ground.",
     [("Scorch Kick", 46, "Fighting"), ("Flame Jab", 42, "Fire"),
      ("Blaze Chop", 40, "Fighting"), ("Ember Rage", 34, "Fire")]),
    (81, "Magmabite", "Fire/Dark", "quad", 170, 2, "common",
     "It lurks in lava caves, waiting for careless trainers.",
     [("Magma Jaw", 44, "Dark"), ("Lava Shade", 42, "Dark"),
      ("Fire Snap", 40, "Fire"), ("Ash Glare", 36, "Fire")]),
    (82, "Pyronox", "Fire/Steel", "golem", 175, 2, "common",
     "Its plated shell glows red hot and can melt metal.",
     [("Pyro Plate", 42, "Steel"), ("Heat Horn", 44, "Fire"),
      ("Iron Blaze", 40, "Steel"), ("Ember Shell", 36, "Fire")]),
    (83, "Reefin", "Water", "fish", 130, 1, "common",
     "A small fish that lives near coral reefs and glows in the dark.",
     [("Reef Splash", 38, "Water"), ("Coral Bite", 40, "Water"),
      ("Bubble Dive", 36, "Water"), ("Tide Flick", 42, "Water")]),
    (84, "Whirlpoolt", "Water/Flying", "orb", 150, 2, "common",
     "It spins through the water to make whirlpools, then glides above them.",
     [("Whirl Gust", 42, "Flying"), ("Aqua Spin", 40, "Water"),
      ("Swirl Dive", 44, "Water"), ("Sky Mist", 34, "Flying")]),
    (85, "Coralisk", "Water/Rock", "fish", 165, 2, "common",
     "Its spiky coral shell protects it from almost every attack.",
     [("Coral Spike", 44, "Rock"), ("Sea Crag", 40, "Rock"),
      ("Bubble Crash", 38, "Water"), ("Tide Shell", 36, "Water")]),
    (86, "Deepjaw", "Water/Dark", "fish", 170, 2, "common",
     "A deep-sea hunter with huge jaws that can crush rock.",
     [("Abyss Jaw", 46, "Dark"), ("Deep Splash", 40, "Water"),
      ("Shadow Tide", 42, "Dark"), ("Brine Gulp", 36, "Water")]),
    (87, "Frostfin", "Water/Ice", "fish", 160, 2, "common",
     "Its fins freeze the water as it swims through cold seas.",
     [("Frost Fin", 42, "Ice"), ("Icy Current", 44, "Ice"),
      ("Sea Frost", 40, "Water"), ("Snow Ripple", 36, "Ice")]),
    (88, "Bubbleon", "Water/Fairy", "orb", 150, 2, "common",
     "It blows enchanting bubbles that make enemies drowsy.",
     [("Bubble Charm", 40, "Fairy"), ("Sweet Foam", 42, "Water"),
      ("Pearl Dazzle", 44, "Fairy"), ("Foam Bounce", 34, "Water")]),
    (89, "Krakling", "Water/Ghost", "ghost", 145, 2, "common",
     "A baby kraken whose ink glows with an eerie light.",
     [("Ink Shadow", 42, "Ghost"), ("Tentacle Wail", 40, "Ghost"),
      ("Drift Jet", 44, "Water"), ("Murk Ink", 36, "Ghost")]),
    (90, "Seadrake", "Water/Dragon", "dragon", 180, 3, "common",
     "A sea dragon that rides the waves and stirs up storms.",
     [("Sea Wyrm", 44, "Dragon"), ("Tidal Coil", 42, "Water"),
      ("Dragon Surf", 46, "Dragon"), ("Brine Fang", 36, "Water")]),
    (91, "Sparkit", "Electric", "quad", 130, 1, "common",
     "A tiny spark-cat that loves to play with static electricity.",
     [("Spark Dash", 36, "Electric"), ("Static Nip", 40, "Electric"),
      ("Zap Hop", 38, "Electric"), ("Jolt Flick", 34, "Electric")]),
    (92, "Voltiger", "Electric", "quad", 140, 2, "common",
     "Its stripes crackle with electricity as it pounces.",
     [("Volt Pounce", 44, "Electric"), ("Thunder Dash", 42, "Electric"),
      ("Charge Claw", 40, "Electric"), ("Surge Bite", 36, "Electric")]),
    (93, "Stormpup", "Electric/Fighting", "quad", 150, 2, "common",
     "A fighting pup that runs through storms and throws electric punches.",
     [("Storm Jab", 44, "Fighting"), ("Volt Paw", 42, "Electric"),
      ("Gale Kick", 40, "Fighting"), ("Static Bark", 36, "Electric")]),
    (94, "Coilisk", "Electric/Poison", "dragon", 160, 2, "common",
     "Coiled tight, it stores electricity in its body and poison in its tail.",
     [("Toxic Coil", 42, "Poison"), ("Shock Venom", 44, "Electric"),
      ("Sludge Zap", 40, "Poison"), ("Coil Snap", 36, "Electric")]),
    (95, "Thunderox", "Electric/Ground", "golem", 170, 2, "common",
     "Each stomp of its hooves makes thunder and shakes the ground.",
     [("Quake Spark", 44, "Ground"), ("Thunder Hoof", 42, "Electric"),
      ("Dust Bolt", 40, "Electric"), ("Earth Surge", 36, "Ground")]),
    (96, "Neonwing", "Electric/Flying", "bird", 150, 2, "common",
     "Its wings glow neon bright, and it can dive faster than lightning.",
     [("Neon Gust", 42, "Flying"), ("Plasma Wing", 44, "Electric"),
      ("Glow Dive", 40, "Flying"), ("Arc Feather", 36, "Electric")]),
    (97, "Shockmoth", "Electric/Bug", "bug", 145, 2, "common",
     "Its dusty wings give off sparks whenever it flutters.",
     [("Shock Scale", 40, "Bug"), ("Volt Dust", 42, "Electric"),
      ("Stun Wing", 36, "Bug"), ("Arc Pollen", 44, "Electric")]),
    (98, "Voltgeist", "Electric/Ghost", "ghost", 150, 2, "common",
     "A ghost powered by lightning that haunts power lines.",
     [("Spirit Arc", 44, "Electric"), ("Haunt Volt", 42, "Ghost"),
      ("Ghost Zap", 40, "Ghost"), ("Wail Spark", 36, "Electric")]),
    (99, "Snowlisk", "Ice", "quad", 150, 1, "common",
     "A snow-covered lizard that hides in drifts and waits for prey.",
     [("Snow Slash", 40, "Ice"), ("Frozen Tail", 42, "Ice"),
      ("Hail Shard", 38, "Ice"), ("Chill Pounce", 34, "Ice")]),
    (100, "Glacibear", "Ice", "quad", 170, 2, "common",
     "A big, friendly bear with an icy coat. It hugs very hard.",
     [("Glacier Maul", 46, "Ice"), ("Frost Hug", 40, "Ice"),
      ("Ice Claw", 38, "Ice"), ("Frozen Roar", 36, "Ice")]),
    (101, "Icetalon", "Ice/Flying", "bird", 155, 2, "common",
     "It swoops down from frozen cliffs with icy claws.",
     [("Ice Talon", 44, "Ice"), ("Frost Gale", 42, "Flying"),
      ("Icy Dive", 40, "Ice"), ("Cold Feather", 36, "Flying")]),
    (102, "Shiverfang", "Ice/Dark", "quad", 165, 2, "common",
     "Its bite is so cold that it makes you shiver.",
     [("Shiver Bite", 42, "Ice"), ("Night Frost", 44, "Dark"),
      ("Chill Fang", 40, "Ice"), ("Dark Icicle", 36, "Dark")]),
    (103, "Crystowl", "Ice/Psychic", "bird", 150, 2, "common",
     "This owl's feathers are made of ice crystals that reflect the light.",
     [("Crystal Gaze", 42, "Psychic"), ("Prism Frost", 44, "Ice"),
      ("Mind Shard", 40, "Psychic"), ("Glint Wing", 36, "Ice")]),
    (104, "Permafrost", "Ice/Rock", "golem", 175, 2, "common",
     "A rock-hard creature that stays frozen even in summer.",
     [("Frozen Quake", 44, "Rock"), ("Ice Boulder", 42, "Ice"),
      ("Glacial Crush", 40, "Rock"), ("Hard Frost", 36, "Ice")]),
    (105, "Duskrawler", "Dark", "quad", 140, 2, "common",
     "It crawls out at dusk and hunts all through the night.",
     [("Dusk Crawl", 38, "Dark"), ("Shade Bite", 42, "Dark"),
      ("Gloom Swipe", 40, "Dark"), ("Night Stalk", 36, "Dark")]),
    (106, "Grimveil", "Ghost/Dark", "ghost", 150, 2, "common",
     "A dark spirit wrapped in a misty cloak.",
     [("Grim Shroud", 42, "Ghost"), ("Veil Strike", 44, "Dark"),
      ("Dread Mist", 40, "Ghost"), ("Black Whisper", 36, "Dark")]),
    (107, "Shadowlisk", "Dark/Dragon", "dragon", 170, 2, "common",
     "A dark serpent that slides through shadows unseen.",
     [("Shadow Coil", 42, "Dark"), ("Umbra Wyrm", 46, "Dragon"),
      ("Night Scale", 40, "Dark"), ("Dusk Tail", 36, "Dragon")]),
    (108, "Wraithowl", "Ghost/Flying", "bird", 150, 2, "common",
     "Its hoot echoes across empty graveyards on windy nights.",
     [("Wraith Swoop", 44, "Ghost"), ("Spectral Wing", 42, "Flying"),
      ("Hollow Hoot", 38, "Ghost"), ("Grave Gust", 36, "Flying")]),
    (109, "Cryptalon", "Ghost/Rock", "golem", 160, 2, "common",
     "A stony ghost that guards ancient tombs.",
     [("Crypt Smash", 44, "Rock"), ("Tomb Wail", 42, "Ghost"),
      ("Ghost Boulder", 40, "Ghost"), ("Stone Haunt", 36, "Rock")]),
    (110, "Nightmoth", "Bug/Dark", "bug", 145, 2, "common",
     "Drawn to dark places, it hides in the shadows during the day.",
     [("Night Dust", 40, "Dark"), ("Moth Lure", 38, "Bug"),
      ("Dark Scales", 42, "Dark"), ("Sting Shadow", 44, "Bug")]),
    (111, "Voidfang", "Dark/Steel", "quad", 165, 2, "common",
     "Its steel-plated fangs are said to bite through anything.",
     [("Void Bite", 42, "Dark"), ("Steel Fang", 44, "Steel"),
      ("Dark Plate", 40, "Steel"), ("Gloom Jaw", 36, "Dark")]),
    (112, "Phantasmite", "Ghost/Fairy", "ghost", 150, 2, "common",
     "A fairy-like ghost whose glow lures travellers into the mist.",
     [("Phantom Glow", 42, "Fairy"), ("Ghost Kiss", 40, "Ghost"),
      ("Fairy Haunt", 44, "Fairy"), ("Mist Wisp", 36, "Ghost")]),
    (113, "Mindrake", "Psychic/Dragon", "dragon", 165, 2, "common",
     "A dragon with a powerful mind that can read thoughts.",
     [("Mind Wyrm", 44, "Dragon"), ("Psy Claw", 40, "Psychic"),
      ("Dream Coil", 42, "Psychic"), ("Dragon Thought", 46, "Dragon")]),
    (114, "Starwhisp", "Psychic/Fairy", "orb", 155, 2, "common",
     "It drifts through the night sky, whispering to the stars.",
     [("Star Whisper", 42, "Fairy"), ("Psy Glow", 40, "Psychic"),
      ("Moon Mind", 44, "Psychic"), ("Twinkle Wish", 36, "Fairy")]),
    (115, "Dreamlynx", "Psychic", "quad", 150, 2, "common",
     "A psychic cat that can slip into your dreams.",
     [("Dream Pounce", 40, "Psychic"), ("Lynx Gaze", 42, "Psychic"),
      ("Sleep Swipe", 38, "Psychic"), ("Mind Pulse", 44, "Psychic")]),
    (116, "Mystibloom", "Fairy/Grass", "plant", 160, 2, "common",
     "A flower with mysterious powers that blooms only under the moon.",
     [("Mystic Petal", 42, "Fairy"), ("Bloom Charm", 40, "Grass"),
      ("Mist Spores", 44, "Fairy"), ("Vine Whisper", 36, "Grass")]),
    (117, "Celestuff", "Fairy", "orb", 150, 2, "common",
     "A fluffy fairy that scatters stardust wherever it goes.",
     [("Celestial Dust", 40, "Fairy"), ("Fairy Ring", 42, "Fairy"),
      ("Starlight Puff", 44, "Fairy"), ("Gentle Glow", 36, "Fairy")]),
    (118, "Astralisk", "Psychic/Rock", "orb", 170, 2, "common",
     "A rocky creature that orbits the planet with a psychic glow.",
     [("Astral Stone", 44, "Rock"), ("Mind Quarry", 42, "Psychic"),
      ("Psy Boulder", 40, "Psychic"), ("Orbit Crush", 36, "Rock")]),
    (119, "Boulderox", "Rock/Ground", "golem", 180, 2, "common",
     "A huge rock beast that charges head-first through mountains. It is known for smashing boulders and cliff walls apart with a single blow.",
     [("Boulder Charge", 46, "Rock"), ("Quake Hoof", 42, "Ground"),
      ("Rock Hide", 38, "Rock"), ("Ground Shove", 36, "Ground")]),
    (120, "Ironhorn", "Steel", "quad", 170, 2, "common",
     "Its horn is made of steel and can break through walls.",
     [("Iron Horn", 44, "Steel"), ("Metal Charge", 42, "Steel"),
      ("Hard Stomp", 38, "Steel"), ("Anvil Butt", 36, "Steel")]),
    (121, "Quakodon", "Ground", "quad", 165, 2, "common",
     "Each footstep it takes causes a small earthquake.",
     [("Quake Jaw", 44, "Ground"), ("Mud Tremor", 40, "Ground"),
      ("Tusk Stomp", 42, "Ground"), ("Sand Roar", 36, "Ground")]),
    (122, "Metashard", "Rock/Steel", "golem", 175, 2, "common",
     "Its body is covered in metal shards that shine in the sunlight.",
     [("Metal Shard", 44, "Steel"), ("Rock Sheen", 42, "Rock"),
      ("Shard Burst", 40, "Rock"), ("Alloy Guard", 36, "Steel")]),
    (123, "Drillisk", "Ground/Steel", "dragon", 165, 2, "common",
     "A steel drill-dragon that tunnels through solid rock.",
     [("Drill Spiral", 44, "Steel"), ("Dig Rush", 42, "Ground"),
      ("Metal Drill", 40, "Steel"), ("Tunnel Burst", 36, "Ground")]),
    (124, "Ferraptor", "Steel/Flying", "bird", 160, 2, "common",
     "A steel bird that dives from the sky at tremendous speed.",
     [("Steel Talon", 44, "Steel"), ("Ferro Dive", 42, "Flying"),
      ("Gale Blade", 40, "Flying"), ("Iron Feather", 36, "Steel")]),
    (125, "Gemstoneer", "Rock/Fairy", "golem", 170, 2, "common",
     "Its body is covered in gems that sparkle in the light.",
     [("Gem Toss", 40, "Rock"), ("Crystal Charm", 42, "Fairy"),
      ("Gem Storm", 44, "Rock"), ("Glitter Stone", 36, "Fairy")]),
    (126, "Seismodon", "Ground/Dragon", "dragon", 180, 2, "common",
     "A dragon that causes earthquakes whenever it roars.",
     [("Seismic Fang", 44, "Ground"), ("Dragon Quake", 46, "Dragon"),
      ("Tremor Tail", 40, "Dragon"), ("Ground Roar", 36, "Ground")]),
    (127, "Dracoflare", "Dragon/Fire", "dragon", 175, 3, "common",
     "Its breath burns hotter than a volcano.",
     [("Draco Flare", 46, "Fire"), ("Dragon Ember", 42, "Dragon"),
      ("Fire Wing", 40, "Fire"), ("Dragon Scale", 36, "Dragon")]),
    (128, "Skyragon", "Dragon/Flying", "dragon", 170, 3, "common",
     "A dragon that soars through the clouds on the wind.",
     [("Sky Wyrm", 44, "Dragon"), ("Cloud Dive", 42, "Flying"),
      ("Dragon Gale", 46, "Dragon"), ("Wing Scale", 36, "Flying")]),
    (129, "Windrake", "Dragon/Flying", "bird", 160, 2, "common",
     "It rakes the sky with its wings and makes strong gusts.",
     [("Wind Claw", 42, "Flying"), ("Gust Dragon", 44, "Dragon"),
      ("Air Rake", 40, "Flying"), ("Dragon Breeze", 36, "Dragon")]),
    (130, "Talonwyrm", "Dragon/Dark", "dragon", 170, 2, "common",
     "Sharp talons and a dark heart make it a feared hunter.",
     [("Talon Wyrm", 44, "Dragon"), ("Dark Talon", 42, "Dark"),
      ("Night Dragon", 46, "Dragon"), ("Shade Claw", 36, "Dark")]),
    (131, "Cloudrake", "Dragon/Water", "dragon", 165, 2, "common",
     "It rests on clouds and rains down when it roars.",
     [("Cloud Wyrm", 44, "Dragon"), ("Rain Coil", 42, "Water"),
      ("Mist Dragon", 40, "Dragon"), ("Hydro Wing", 36, "Water")]),
    (132, "Stormwyrm", "Dragon/Electric", "dragon", 160, 2, "common",
     "A dragon that rides lightning in the middle of a storm.",
     [("Storm Wyrm", 46, "Dragon"), ("Thunder Coil", 42, "Electric"),
      ("Dragon Volt", 44, "Dragon"), ("Gale Spark", 36, "Electric")]),
    # ---- Rare and legendary ----
    (133, "Solaryx", "Fire/Psychic", "bird", 320, 7, "legendary",
     "Legend says it was born from the first sunrise.",
     [("Solar Flare", 70, "Fire"), ("Psy Sunburst", 68, "Psychic"),
      ("Sun Wing", 64, "Fire"), ("Mind Eclipse", 72, "Psychic")]),
    (134, "Lunavex", "Dark/Fairy", "ghost", 320, 7, "legendary",
     "It appears only on nights when the moon is full.",
     [("Lunar Veil", 68, "Fairy"), ("Dark Eclipse", 70, "Dark"),
      ("Moon Fang", 64, "Dark"), ("Starless Hymn", 72, "Fairy")]),
    (135, "Tempestron", "Electric/Dragon", "dragon", 330, 7, "legendary",
     "It commands the winds and storms of the world.",
     [("Tempest Dragon", 72, "Dragon"), ("Thunder Storm", 68, "Electric"),
      ("Raging Coil", 64, "Dragon"), ("Volt Cataclysm", 70, "Electric")]),
    (136, "Aquaryth", "Water/Psychic", "fish", 320, 7, "legendary",
     "A water spirit that is said to control the tides.",
     [("Aqua Mind", 70, "Water"), ("Tidal Mind", 68, "Psychic"),
      ("Deep Current", 64, "Water"), ("Oracle Wave", 72, "Psychic")]),
    (137, "Terravion", "Ground/Steel", "golem", 330, 7, "legendary",
     "A titan of the earth that can move mountains.",
     [("Terra Quake", 72, "Ground"), ("Titan Plate", 68, "Steel"),
      ("Mountain Fall", 64, "Ground"), ("Iron Terra", 70, "Steel")]),
    (138, "Chronolux", "Psychic/Steel", "orb", 320, 7, "legendary",
     "It is said to control time itself.",
     [("Chrono Beam", 70, "Psychic"), ("Gear Crush", 68, "Steel"),
      ("Lux Pulse", 64, "Psychic"), ("Time Shift", 72, "Steel")]),
    (139, "Voidragon", "Dark/Dragon", "dragon", 340, 7, "legendary",
     "A dragon from the empty space between worlds.",
     [("Void Wyrm", 72, "Dark"), ("Abyss Dragon", 68, "Dragon"),
      ("Null Coil", 64, "Void"), ("Eclipse Claw", 70, "Dark")]),
    (140, "Eternova", "Psychic/Dragon", "orb", 350, 8, "mythical",
     "It is said to exist outside of time itself.",
     [("Eternal Nova", 74, "Psychic"), ("Ageless Wyrm", 70, "Dragon"),
      ("Nova Mind", 68, "Psychic"), ("Forever Coil", 72, "Dragon")]),
    (141, "Nebulord", "Psychic/Fairy", "orb", 340, 8, "mythical",
     "Born from a cloud of stars, it is seen once in a lifetime.",
     [("Nebula Gaze", 72, "Psychic"), ("Galaxy Veil", 70, "Fairy"),
      ("Cosmic Hymn", 66, "Fairy"), ("Star Mind", 74, "Psychic")]),
    (142, "Omnidrake", "Dragon/Steel", "dragon", 350, 8, "mythical",
     "The ultimate dragon, said to hold the power of all others.",
     [("Omni Wyrm", 74, "Dragon"), ("Titan Scale", 70, "Steel"),
      ("Steel Omen", 68, "Steel"), ("Dragon Omega", 72, "Dragon")]),
    # ---- Legendary duo ----
    (143, "Aetherion", "Dragon/Psychic", "dragon", 340, 8, "legendary",
     "A dragon that drifts between the stars, bending space with its psychic mind.",
     [("Cosmic Wyrm", 72, "Dragon"), ("Mind Starfall", 70, "Psychic"),
      ("Astral Coil", 66, "Dragon"), ("Psy Nebula", 72, "Psychic")]),
    (144, "Varkrion", "Dark/Steel", "golem", 340, 8, "legendary",
     "An armoured beast of shadow and steel that breaks through anything in its path.",
     [("Void Maul", 72, "Dark"), ("Steel Eclipse", 70, "Steel"),
      ("Titan Fang", 66, "Steel"), ("Shadow Anvil", 72, "Dark")]),
    # ---- #146 to #345 (v16.1) ----
    (146, 'Sproutlet', 'Grass', 'plant', 163, 8, 'common',
     'Sproutlet is a Grass type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Thorn Whip', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (147, 'Thornuckle', 'Grass', 'plant', 207, 6, 'common',
     'Thornuckle is a Grass type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Thorn Whip', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (148, 'Briarhorn', 'Grass/Rock', 'plant', 168, 5, 'common',
     'Briarhorn is a Grass and Rock type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (149, 'Cindimp', 'Fire', 'quad', 224, 5, 'common',
     'Cindimp is a Fire type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Cinder Lash', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (150, 'Pyroclastor', 'Fire/Rock', 'quad', 232, 8, 'common',
     'Pyroclastor is a Fire and Rock type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (151, 'Bubbloon', 'Water', 'fish', 172, 4, 'common',
     'Bubbloon is a Water type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Bubble Barrage', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (152, 'Aquavelle', 'Water/Fairy', 'fish', 196, 6, 'common',
     'Aquavelle is a Water and Fairy type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (153, 'Tidewyrm', 'Water/Dragon', 'fish', 193, 7, 'common',
     'Tidewyrm is a Water and Dragon type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (154, 'Zappup', 'Electric', 'orb', 235, 7, 'common',
     'Zappup is a Electric type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Static Snap', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (155, 'Voltusk', 'Electric/Ground', 'orb', 223, 4, 'common',
     'Voltusk is a Electric and Ground type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (156, 'Frostkit', 'Ice', 'quad', 178, 7, 'common',
     'Frostkit is a Ice type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Frost Bite', 40, 'Ice'),
      ('Quick Dash', 32, 'Normal')]),
    (157, 'Frostmaw', 'Ice/Dark', 'quad', 198, 7, 'common',
     'Frostmaw is a Ice and Dark type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (158, 'Pebblit', 'Rock', 'golem', 205, 5, 'common',
     'Pebblit is a Rock type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Pebble Blast', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (159, 'Cragwing', 'Rock/Flying', 'golem', 207, 6, 'common',
     'Cragwing is a Rock and Flying type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (160, 'Gustling', 'Flying', 'bird', 213, 6, 'common',
     'Gustling is a Flying type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Wing Flick', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (161, 'Tempestrix', 'Flying/Electric', 'bird', 210, 8, 'common',
     'Tempestrix is a Flying and Electric type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (162, 'Shadebug', 'Bug/Dark', 'bug', 167, 5, 'common',
     'Shadebug is a Bug and Dark type. It buzzes around flowers in swarms.',
     [('Swarm Bite', 42, 'Bug'),
      ('Hive Strike', 46, 'Bug'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (163, 'Silkrusher', 'Bug/Fighting', 'bug', 237, 7, 'common',
     'Silkrusher is a Bug and Fighting type. It buzzes around flowers in swarms.',
     [('Swarm Bite', 42, 'Bug'),
      ('Hive Strike', 46, 'Bug'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (164, 'Mindoodle', 'Psychic', 'imp', 231, 5, 'common',
     'Mindoodle is a Psychic type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Mind Poke', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (165, 'Cerebrion', 'Psychic/Steel', 'imp', 175, 5, 'common',
     'Cerebrion is a Psychic and Steel type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (166, 'Hauntuff', 'Ghost', 'ghost', 179, 4, 'common',
     'Hauntuff is a Ghost type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Haunt Touch', 40, 'Ghost'),
      ('Quick Dash', 32, 'Normal')]),
    (167, 'Gravewing', 'Ghost/Flying', 'ghost', 202, 6, 'common',
     'Gravewing is a Ghost and Flying type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (168, 'Dracub', 'Dragon', 'dragon', 171, 8, 'common',
     'Dracub is a Dragon type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Drake Bite', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (169, 'Drakoryx', 'Dragon/Fire', 'dragon', 200, 6, 'common',
     'Drakoryx is a Dragon and Fire type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Ember Rush', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (170, 'Scrapup', 'Steel', 'golem', 202, 7, 'common',
     'Scrapup is a Steel type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Iron Tap', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (171, 'Ironcladion', 'Steel/Fighting', 'golem', 201, 8, 'common',
     'Ironcladion is a Steel and Fighting type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (172, 'Toxmite', 'Poison', 'bug', 175, 6, 'common',
     'Toxmite is a Poison type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Acid Spit', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (173, 'Toxiraptor', 'Poison/Dragon', 'bug', 231, 6, 'common',
     'Toxiraptor is a Poison and Dragon type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (174, 'Sandimp', 'Ground', 'golem', 161, 4, 'common',
     'Sandimp is a Ground type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Sand Whirl', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (175, 'Dunecrusher', 'Ground/Rock', 'golem', 170, 7, 'common',
     'Dunecrusher is a Ground and Rock type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (176, 'Puffawn', 'Normal', 'quad', 179, 7, 'common',
     'Puffawn is a Normal type. It wanders the fields looking for berries.',
     [('Heavy Smash', 42, 'Normal'),
      ('Crush Rush', 46, 'Normal'),
      ('Body Bash', 40, 'Normal'),
      ('Quick Dash', 32, 'Normal')]),
    (177, 'Wooloom', 'Normal/Fairy', 'quad', 207, 6, 'common',
     'Wooloom is a Normal and Fairy type. It wanders the fields looking for berries.',
     [('Heavy Smash', 42, 'Normal'),
      ('Crush Rush', 46, 'Normal'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (178, 'Lunakit', 'Psychic', 'imp', 187, 8, 'common',
     'Lunakit is a Psychic type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Mind Poke', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (179, 'Moonlynx', 'Psychic/Dark', 'imp', 200, 7, 'common',
     'Moonlynx is a Psychic and Dark type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (180, 'Solsprig', 'Grass/Fire', 'plant', 227, 5, 'common',
     'Solsprig is a Grass and Fire type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Ember Rush', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (181, 'Solbloom', 'Grass/Fire', 'plant', 215, 4, 'common',
     'Solbloom is a Grass and Fire type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Ember Rush', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (182, 'Coraloo', 'Water/Rock', 'fish', 160, 7, 'common',
     'Coraloo is a Water and Rock type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (183, 'Reefang', 'Water/Dragon', 'fish', 183, 8, 'common',
     'Reefang is a Water and Dragon type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (184, 'Emberfin', 'Fire/Water', 'quad', 179, 8, 'common',
     'Emberfin is a Fire and Water type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (185, 'Magmaraid', 'Fire/Water', 'quad', 212, 6, 'common',
     'Magmaraid is a Fire and Water type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (186, 'Glimmeray', 'Electric/Water', 'orb', 179, 5, 'common',
     'Glimmeray is a Electric and Water type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (187, 'Stormanta', 'Electric/Flying', 'orb', 212, 7, 'common',
     'Stormanta is a Electric and Flying type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (188, 'Mossmite', 'Bug/Grass', 'bug', 167, 8, 'common',
     'Mossmite is a Bug and Grass type. It buzzes around flowers in swarms.',
     [('Swarm Bite', 42, 'Bug'),
      ('Hive Strike', 46, 'Bug'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (189, 'Thornmantis', 'Bug/Grass', 'bug', 204, 5, 'common',
     'Thornmantis is a Bug and Grass type. It buzzes around flowers in swarms.',
     [('Swarm Bite', 42, 'Bug'),
      ('Hive Strike', 46, 'Bug'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (190, 'Glacyowl', 'Ice/Psychic', 'quad', 190, 6, 'common',
     'Glacyowl is a Ice and Psychic type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (191, 'Prismowl', 'Ice/Psychic', 'quad', 176, 7, 'common',
     'Prismowl is a Ice and Psychic type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (192, 'Dreadling', 'Dark', 'imp', 228, 4, 'common',
     'Dreadling is a Dark type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Sneak Bite', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (193, 'Dreadmaw', 'Dark/Dragon', 'imp', 186, 6, 'common',
     'Dreadmaw is a Dark and Dragon type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (194, 'Bellibird', 'Flying/Steel', 'bird', 193, 5, 'common',
     'Bellibird is a Flying and Steel type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (195, 'Chimewing', 'Flying/Steel', 'bird', 185, 5, 'common',
     'Chimewing is a Flying and Steel type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (196, 'Mudkipper', 'Ground/Water', 'golem', 189, 8, 'common',
     'Mudkipper is a Ground and Water type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (197, 'Marshogre', 'Ground/Water', 'golem', 224, 7, 'common',
     'Marshogre is a Ground and Water type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (198, 'Flarecub', 'Fire', 'quad', 213, 6, 'common',
     'Flarecub is a Fire type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Cinder Lash', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (199, 'Blazebear', 'Fire/Fighting', 'quad', 184, 5, 'common',
     'Blazebear is a Fire and Fighting type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (200, 'Bloomisk', 'Grass/Poison', 'plant', 199, 7, 'common',
     'Bloomisk is a Grass and Poison type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Toxic Spray', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (201, 'Sporemantis', 'Grass/Poison', 'plant', 221, 8, 'common',
     'Sporemantis is a Grass and Poison type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Toxic Spray', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (202, 'Voltadile', 'Electric/Water', 'orb', 168, 5, 'common',
     'Voltadile is a Electric and Water type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (203, 'Thundrake', 'Electric/Dragon', 'orb', 230, 4, 'common',
     'Thundrake is a Electric and Dragon type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (204, 'Spookit', 'Ghost/Fairy', 'ghost', 173, 6, 'common',
     'Spookit is a Ghost and Fairy type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (205, 'Phantasmew', 'Ghost/Fairy', 'ghost', 219, 8, 'common',
     'Phantasmew is a Ghost and Fairy type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (206, 'Boulderam', 'Rock/Steel', 'golem', 234, 8, 'common',
     'Boulderam is a Rock and Steel type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (207, 'Titanolith', 'Rock/Steel', 'golem', 235, 5, 'common',
     'Titanolith is a Rock and Steel type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (208, 'Skydrop', 'Flying/Water', 'bird', 225, 7, 'common',
     'Skydrop is a Flying and Water type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (209, 'Stormrake', 'Flying/Dragon', 'bird', 203, 6, 'common',
     'Stormrake is a Flying and Dragon type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (210, 'Nibbleaf', 'Grass', 'plant', 213, 8, 'common',
     'Nibbleaf is a Grass type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Thorn Whip', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (211, 'Gnawthorn', 'Grass/Dark', 'plant', 200, 5, 'common',
     'Gnawthorn is a Grass and Dark type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (212, 'Frosthorn', 'Ice/Rock', 'quad', 215, 5, 'common',
     'Frosthorn is a Ice and Rock type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (213, 'Cryostag', 'Ice/Bug', 'quad', 170, 4, 'common',
     'Cryostag is a Ice and Bug type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (214, 'Hexlet', 'Psychic/Ghost', 'imp', 165, 6, 'common',
     'Hexlet is a Psychic and Ghost type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Shade Touch', 40, 'Ghost'),
      ('Quick Dash', 32, 'Normal')]),
    (215, 'Hexoracle', 'Psychic/Ghost', 'imp', 201, 4, 'common',
     'Hexoracle is a Psychic and Ghost type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Shade Touch', 40, 'Ghost'),
      ('Quick Dash', 32, 'Normal')]),
    (216, 'Gearbug', 'Bug/Steel', 'bug', 219, 8, 'common',
     'Gearbug is a Bug and Steel type. It buzzes around flowers in swarms.',
     [('Swarm Bite', 42, 'Bug'),
      ('Hive Strike', 46, 'Bug'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (217, 'Mechamantis', 'Bug/Steel', 'bug', 217, 7, 'common',
     'Mechamantis is a Bug and Steel type. It buzzes around flowers in swarms.',
     [('Swarm Bite', 42, 'Bug'),
      ('Hive Strike', 46, 'Bug'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (218, 'Sandrill', 'Ground', 'golem', 183, 7, 'common',
     'Sandrill is a Ground type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Sand Whirl', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (219, 'Terravolt', 'Ground/Electric', 'golem', 178, 6, 'common',
     'Terravolt is a Ground and Electric type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (220, 'Blubbit', 'Water/Fairy', 'fish', 226, 4, 'common',
     'Blubbit is a Water and Fairy type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (221, 'Aquarabbit', 'Water/Fairy', 'fish', 185, 4, 'common',
     'Aquarabbit is a Water and Fairy type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (222, 'Crowspark', 'Dark/Electric', 'imp', 161, 4, 'common',
     'Crowspark is a Dark and Electric type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (223, 'Nightvolt', 'Dark/Electric', 'imp', 227, 4, 'common',
     'Nightvolt is a Dark and Electric type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (224, 'Flamecko', 'Fire/Dragon', 'quad', 211, 8, 'common',
     'Flamecko is a Fire and Dragon type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (225, 'Pyrodrake', 'Fire/Dragon', 'quad', 222, 8, 'common',
     'Pyrodrake is a Fire and Dragon type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (226, 'Mossox', 'Grass/Steel', 'plant', 191, 8, 'common',
     'Mossox is a Grass and Steel type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (227, 'Ironfern', 'Grass/Steel', 'plant', 236, 8, 'common',
     'Ironfern is a Grass and Steel type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (228, 'Shiverpup', 'Ice', 'quad', 239, 8, 'common',
     'Shiverpup is a Ice type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Frost Bite', 40, 'Ice'),
      ('Quick Dash', 32, 'Normal')]),
    (229, 'Snowfang', 'Ice/Ground', 'quad', 184, 8, 'common',
     'Snowfang is a Ice and Ground type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (230, 'Gloomoth', 'Bug/Ghost', 'bug', 181, 5, 'common',
     'Gloomoth is a Bug and Ghost type. It buzzes around flowers in swarms.',
     [('Swarm Bite', 42, 'Bug'),
      ('Hive Strike', 46, 'Bug'),
      ('Shade Touch', 40, 'Ghost'),
      ('Quick Dash', 32, 'Normal')]),
    (231, 'Duskmoth', 'Bug/Ghost', 'bug', 213, 4, 'common',
     'Duskmoth is a Bug and Ghost type. It buzzes around flowers in swarms.',
     [('Swarm Bite', 42, 'Bug'),
      ('Hive Strike', 46, 'Bug'),
      ('Shade Touch', 40, 'Ghost'),
      ('Quick Dash', 32, 'Normal')]),
    (232, 'Staribble', 'Fairy', 'orb', 171, 6, 'common',
     'Staribble is a Fairy type. It scatters glitter when it is happy.',
     [('Charm Burst', 42, 'Fairy'),
      ('Moon Kiss', 46, 'Fairy'),
      ('Glitter Puff', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (233, 'Astralune', 'Fairy/Psychic', 'orb', 228, 8, 'common',
     'Astralune is a Fairy and Psychic type. It scatters glitter when it is happy.',
     [('Charm Burst', 42, 'Fairy'),
      ('Moon Kiss', 46, 'Fairy'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (234, 'Quakid', 'Ground/Fighting', 'golem', 196, 4, 'common',
     'Quakid is a Ground and Fighting type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (235, 'Seismotusk', 'Ground/Fighting', 'golem', 165, 4, 'common',
     'Seismotusk is a Ground and Fighting type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (236, 'Inklingo', 'Water/Dark', 'fish', 170, 5, 'common',
     'Inklingo is a Water and Dark type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (237, 'Abyssquid', 'Water/Dark', 'fish', 179, 7, 'common',
     'Abyssquid is a Water and Dark type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (238, 'Sparklit', 'Electric/Fairy', 'orb', 212, 6, 'common',
     'Sparklit is a Electric and Fairy type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (239, 'Lumivolt', 'Electric/Fairy', 'orb', 198, 8, 'common',
     'Lumivolt is a Electric and Fairy type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (240, 'Magmaut', 'Fire/Ground', 'quad', 182, 5, 'common',
     'Magmaut is a Fire and Ground type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (241, 'Volcanole', 'Fire/Ground', 'quad', 207, 7, 'common',
     'Volcanole is a Fire and Ground type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (242, 'Riftling', 'Dragon/Psychic', 'dragon', 173, 8, 'common',
     'Riftling is a Dragon and Psychic type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (243, 'Riftwyrm', 'Dragon/Psychic', 'dragon', 236, 6, 'common',
     'Riftwyrm is a Dragon and Psychic type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (244, 'Auroray', 'Ice/Fairy', 'quad', 173, 7, 'common',
     'Auroray is a Ice and Fairy type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (245, 'Borealux', 'Ice/Fairy', 'quad', 167, 7, 'common',
     'Borealux is a Ice and Fairy type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (246, 'Mipplet', 'Grass', 'plant', 168, 4, 'common',
     'Mipplet is a Grass type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Thorn Whip', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (247, 'Virdillo', 'Grass/Ground', 'plant', 204, 6, 'common',
     'Virdillo is a Grass and Ground type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (248, 'Flamberet', 'Fire', 'quad', 156, 5, 'common',
     'Flamberet is a Fire type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Cinder Lash', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (249, 'Scorchclaw', 'Fire/Fighting', 'quad', 216, 7, 'common',
     'Scorchclaw is a Fire and Fighting type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (250, 'Drizzlet', 'Water', 'fish', 180, 4, 'common',
     'Drizzlet is a Water type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Bubble Barrage', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (251, 'Marivex', 'Water/Psychic', 'fish', 192, 4, 'common',
     'Marivex is a Water and Psychic type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (252, 'Klinkit', 'Steel', 'golem', 162, 5, 'common',
     'Klinkit is a Steel type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Iron Tap', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (253, 'Ferravolt', 'Steel/Electric', 'golem', 198, 6, 'common',
     'Ferravolt is a Steel and Electric type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (254, 'Nimbli', 'Flying', 'bird', 144, 4, 'common',
     'Nimbli is a Flying type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Wing Flick', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (255, 'Aerovant', 'Flying/Dragon', 'bird', 204, 7, 'common',
     'Aerovant is a Flying and Dragon type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (256, 'Grublix', 'Bug', 'bug', 162, 5, 'common',
     'Grublix is a Bug type. It buzzes around flowers in swarms.',
     [('Swarm Bite', 42, 'Bug'),
      ('Hive Strike', 46, 'Bug'),
      ('Silk Shot', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (257, 'Caraphex', 'Bug/Rock', 'bug', 210, 6, 'common',
     'Caraphex is a Bug and Rock type. It buzzes around flowers in swarms.',
     [('Swarm Bite', 42, 'Bug'),
      ('Hive Strike', 46, 'Bug'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (258, 'Zorblin', 'Dark', 'imp', 150, 6, 'common',
     'Zorblin is a Dark type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Sneak Bite', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (259, 'Noctivane', 'Dark/Flying', 'imp', 186, 7, 'common',
     'Noctivane is a Dark and Flying type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (260, 'Lumibee', 'Fairy', 'orb', 162, 3, 'common',
     'Lumibee is a Fairy type. It scatters glitter when it is happy.',
     [('Charm Burst', 42, 'Fairy'),
      ('Moon Kiss', 46, 'Fairy'),
      ('Glitter Puff', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (261, 'Faequartz', 'Fairy/Rock', 'orb', 204, 5, 'common',
     'Faequartz is a Fairy and Rock type. It scatters glitter when it is happy.',
     [('Charm Burst', 42, 'Fairy'),
      ('Moon Kiss', 46, 'Fairy'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (262, 'Glimsk', 'Ice', 'quad', 150, 4, 'common',
     'Glimsk is a Ice type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Frost Bite', 40, 'Ice'),
      ('Quick Dash', 32, 'Normal')]),
    (263, 'Hailvorn', 'Ice/Steel', 'quad', 210, 6, 'common',
     'Hailvorn is a Ice and Steel type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (264, 'Quorble', 'Normal', 'quad', 186, 5, 'common',
     'Quorble is a Normal type. It wanders the fields looking for berries.',
     [('Heavy Smash', 42, 'Normal'),
      ('Crush Rush', 46, 'Normal'),
      ('Body Bash', 40, 'Normal'),
      ('Quick Dash', 32, 'Normal')]),
    (265, 'Brontuff', 'Normal/Fighting', 'quad', 234, 7, 'common',
     'Brontuff is a Normal and Fighting type. It wanders the fields looking for berries.',
     [('Heavy Smash', 42, 'Normal'),
      ('Crush Rush', 46, 'Normal'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (266, 'Vexling', 'Poison', 'bug', 156, 5, 'common',
     'Vexling is a Poison type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Acid Spit', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (267, 'Murkadon', 'Poison/Dark', 'bug', 210, 7, 'common',
     'Murkadon is a Poison and Dark type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (268, 'Pebblune', 'Rock', 'golem', 198, 5, 'common',
     'Pebblune is a Rock type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Pebble Blast', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (269, 'Gravolisk', 'Rock/Dragon', 'golem', 228, 7, 'common',
     'Gravolisk is a Rock and Dragon type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (270, 'Wispindle', 'Ghost', 'ghost', 144, 4, 'common',
     'Wispindle is a Ghost type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Haunt Touch', 40, 'Ghost'),
      ('Quick Dash', 32, 'Normal')]),
    (271, 'Gloamora', 'Ghost/Grass', 'ghost', 192, 5, 'common',
     'Gloamora is a Ghost and Grass type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (272, 'Mindillo', 'Psychic', 'imp', 150, 3, 'common',
     'Mindillo is a Psychic type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Mind Poke', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (273, 'Oraclyx', 'Psychic/Dragon', 'imp', 198, 6, 'common',
     'Oraclyx is a Psychic and Dragon type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (274, 'Dustrik', 'Ground', 'golem', 192, 6, 'common',
     'Dustrik is a Ground type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Sand Whirl', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (275, 'Rumblex', 'Ground/Steel', 'golem', 234, 7, 'common',
     'Rumblex is a Ground and Steel type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (276, 'Zapindle', 'Electric', 'orb', 144, 5, 'common',
     'Zapindle is a Electric type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Static Snap', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (277, 'Electrynn', 'Electric/Psychic', 'orb', 180, 5, 'common',
     'Electrynn is a Electric and Psychic type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (278, 'Berribun', 'Grass/Fairy', 'plant', 174, 4, 'common',
     'Berribun is a Grass and Fairy type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (279, 'Florvex', 'Grass/Poison', 'plant', 198, 6, 'common',
     'Florvex is a Grass and Poison type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Toxic Spray', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (280, 'Cubburn', 'Fire', 'quad', 186, 6, 'common',
     'Cubburn is a Fire type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Cinder Lash', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (281, 'Pyrelisk', 'Fire/Dragon', 'quad', 222, 8, 'common',
     'Pyrelisk is a Fire and Dragon type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (282, 'Wavlet', 'Water', 'fish', 168, 4, 'common',
     'Wavlet is a Water type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Bubble Barrage', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (283, 'Pelagorn', 'Water/Flying', 'fish', 210, 6, 'common',
     'Pelagorn is a Water and Flying type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (284, 'Shardlet', 'Rock', 'golem', 174, 5, 'common',
     'Shardlet is a Rock type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Pebble Blast', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (285, 'Obsidrake', 'Rock/Fire', 'golem', 228, 8, 'common',
     'Obsidrake is a Rock and Fire type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Ember Rush', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (286, 'Tinkrow', 'Steel/Fairy', 'golem', 168, 4, 'common',
     'Tinkrow is a Steel and Fairy type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (287, 'Bellatrixel', 'Steel/Psychic', 'golem', 204, 5, 'common',
     'Bellatrixel is a Steel and Psychic type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (288, 'Slinkit', 'Dark', 'imp', 156, 6, 'common',
     'Slinkit is a Dark type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Sneak Bite', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (289, 'Vantaclaw', 'Dark/Steel', 'imp', 210, 8, 'common',
     'Vantaclaw is a Dark and Steel type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (290, 'Puffern', 'Water/Ice', 'fish', 204, 4, 'common',
     'Puffern is a Water and Ice type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Frost Dash', 40, 'Ice'),
      ('Quick Dash', 32, 'Normal')]),
    (291, 'Cryomurk', 'Ice/Dark', 'quad', 192, 7, 'common',
     'Cryomurk is a Ice and Dark type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (292, 'Fizzlet', 'Electric/Water', 'orb', 162, 4, 'common',
     'Fizzlet is a Electric and Water type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (293, 'Amphexa', 'Electric/Dragon', 'orb', 204, 7, 'common',
     'Amphexa is a Electric and Dragon type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (294, 'Mothwick', 'Bug/Fire', 'bug', 168, 5, 'common',
     'Mothwick is a Bug and Fire type. It buzzes around flowers in swarms.',
     [('Swarm Bite', 42, 'Bug'),
      ('Hive Strike', 46, 'Bug'),
      ('Ember Rush', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (295, 'Cindermoth', 'Bug/Fire', 'bug', 204, 6, 'common',
     'Cindermoth is a Bug and Fire type. It buzzes around flowers in swarms.',
     [('Swarm Bite', 42, 'Bug'),
      ('Hive Strike', 46, 'Bug'),
      ('Ember Rush', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (296, 'Drelbit', 'Ground', 'golem', 180, 6, 'common',
     'Drelbit is a Ground type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Sand Whirl', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (297, 'Quakorra', 'Ground/Dragon', 'golem', 228, 8, 'common',
     'Quakorra is a Ground and Dragon type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (298, 'Fuzzlet', 'Normal/Fairy', 'quad', 180, 4, 'common',
     'Fuzzlet is a Normal and Fairy type. It wanders the fields looking for berries.',
     [('Heavy Smash', 42, 'Normal'),
      ('Crush Rush', 46, 'Normal'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (299, 'Velvursa', 'Normal/Psychic', 'quad', 210, 5, 'common',
     'Velvursa is a Normal and Psychic type. It wanders the fields looking for berries.',
     [('Heavy Smash', 42, 'Normal'),
      ('Crush Rush', 46, 'Normal'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (300, 'Noxibit', 'Ghost/Dark', 'ghost', 150, 6, 'common',
     'Noxibit is a Ghost and Dark type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (301, 'Vesperune', 'Ghost/Fairy', 'ghost', 192, 5, 'common',
     'Vesperune is a Ghost and Fairy type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (302, 'Crimblet', 'Fighting', 'quad', 198, 7, 'common',
     'Crimblet is a Fighting type. It trains every morning by punching trees.',
     [('Brawl Strike', 42, 'Fighting'),
      ('Combo Blow', 46, 'Fighting'),
      ('Palm Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (303, 'Kordrake', 'Fighting/Dragon', 'quad', 234, 8, 'common',
     'Kordrake is a Fighting and Dragon type. It trains every morning by punching trees.',
     [('Brawl Strike', 42, 'Fighting'),
      ('Combo Blow', 46, 'Fighting'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (304, 'Sapphlet', 'Water/Rock', 'fish', 186, 4, 'common',
     'Sapphlet is a Water and Rock type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (305, 'Azurune', 'Water/Psychic', 'fish', 204, 5, 'common',
     'Azurune is a Water and Psychic type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (306, 'Thornib', 'Grass/Bug', 'plant', 162, 5, 'common',
     'Thornib is a Grass and Bug type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (307, 'Bramblex', 'Grass/Bug', 'plant', 204, 7, 'common',
     'Bramblex is a Grass and Bug type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (308, 'Flittern', 'Flying', 'bird', 150, 4, 'common',
     'Flittern is a Flying type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Wing Flick', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (309, 'Skyrend', 'Flying/Dark', 'bird', 198, 7, 'common',
     'Skyrend is a Flying and Dark type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (310, 'Glacibun', 'Ice/Fairy', 'quad', 174, 4, 'common',
     'Glacibun is a Ice and Fairy type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (311, 'Shardiva', 'Ice/Steel', 'quad', 210, 6, 'common',
     'Shardiva is a Ice and Steel type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (312, 'Vortib', 'Flying/Electric', 'bird', 156, 4, 'common',
     'Vortib is a Flying and Electric type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (313, 'Cycloray', 'Flying/Electric', 'bird', 204, 6, 'common',
     'Cycloray is a Flying and Electric type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (314, 'Munchusk', 'Normal', 'quad', 216, 6, 'common',
     'Munchusk is a Normal type. It wanders the fields looking for berries.',
     [('Heavy Smash', 42, 'Normal'),
      ('Crush Rush', 46, 'Normal'),
      ('Body Bash', 40, 'Normal'),
      ('Quick Dash', 32, 'Normal')]),
    (315, 'Grubuff', 'Normal/Fighting', 'quad', 240, 8, 'common',
     'Grubuff is a Normal and Fighting type. It wanders the fields looking for berries.',
     [('Heavy Smash', 42, 'Normal'),
      ('Crush Rush', 46, 'Normal'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (316, 'Plinket', 'Steel', 'golem', 168, 5, 'common',
     'Plinket is a Steel type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Iron Tap', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (317, 'Alloydrum', 'Steel/Ground', 'golem', 228, 7, 'common',
     'Alloydrum is a Steel and Ground type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (318, 'Viperlet', 'Poison', 'bug', 162, 5, 'common',
     'Viperlet is a Poison type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Acid Spit', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (319, 'Slytherune', 'Poison/Psychic', 'bug', 192, 5, 'common',
     'Slytherune is a Poison and Psychic type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (320, 'Cragbit', 'Rock/Ground', 'golem', 204, 6, 'common',
     'Cragbit is a Rock and Ground type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (321, 'Monolithor', 'Rock/Ground', 'golem', 246, 7, 'common',
     'Monolithor is a Rock and Ground type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (322, 'Flarble', 'Fire/Fairy', 'quad', 162, 4, 'common',
     'Flarble is a Fire and Fairy type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (323, 'Glimmerash', 'Fire/Fairy', 'quad', 204, 5, 'common',
     'Glimmerash is a Fire and Fairy type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (324, 'Drowlix', 'Dark/Psychic', 'imp', 162, 5, 'common',
     'Drowlix is a Dark and Psychic type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (325, 'Noctyrex', 'Dark/Psychic', 'imp', 210, 7, 'common',
     'Noctyrex is a Dark and Psychic type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (326, 'Aquibble', 'Water/Bug', 'fish', 174, 4, 'common',
     'Aquibble is a Water and Bug type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (327, 'Tiderune', 'Water/Bug', 'fish', 204, 6, 'common',
     'Tiderune is a Water and Bug type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (328, 'Fernibble', 'Grass', 'plant', 168, 4, 'common',
     'Fernibble is a Grass type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Thorn Whip', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (329, 'Verdantusk', 'Grass/Steel', 'plant', 228, 7, 'common',
     'Verdantusk is a Grass and Steel type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (330, 'Wyrmlet', 'Dragon', 'dragon', 186, 6, 'common',
     'Wyrmlet is a Dragon type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Drake Bite', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (331, 'Orynthos', 'Dragon/Fairy', 'dragon', 222, 6, 'common',
     'Orynthos is a Dragon and Fairy type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (332, 'Hexibud', 'Ghost/Grass', 'ghost', 168, 4, 'common',
     'Hexibud is a Ghost and Grass type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (333, 'Mourngrove', 'Ghost/Grass', 'ghost', 216, 6, 'common',
     'Mourngrove is a Ghost and Grass type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (334, 'Sparkusk', 'Electric', 'orb', 168, 5, 'common',
     'Sparkusk is a Electric type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Static Snap', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (335, 'Voltrusk', 'Electric/Steel', 'orb', 216, 7, 'common',
     'Voltrusk is a Electric and Steel type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (336, 'Bouldib', 'Rock/Fighting', 'golem', 210, 7, 'common',
     'Bouldib is a Rock and Fighting type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (337, 'Cragmantor', 'Rock/Fighting', 'golem', 252, 8, 'common',
     'Cragmantor is a Rock and Fighting type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (338, 'Wisplette', 'Fairy', 'orb', 156, 3, 'common',
     'Wisplette is a Fairy type. It scatters glitter when it is happy.',
     [('Charm Burst', 42, 'Fairy'),
      ('Moon Kiss', 46, 'Fairy'),
      ('Glitter Puff', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (339, 'Auralisse', 'Fairy/Flying', 'orb', 198, 4, 'common',
     'Auralisse is a Fairy and Flying type. It scatters glitter when it is happy.',
     [('Charm Burst', 42, 'Fairy'),
      ('Moon Kiss', 46, 'Fairy'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (340, 'Murklet', 'Poison/Dark', 'bug', 174, 6, 'common',
     'Murklet is a Poison and Dark type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (341, 'Vilethorn', 'Poison/Grass', 'bug', 216, 7, 'common',
     'Vilethorn is a Poison and Grass type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (342, 'Chronibble', 'Psychic/Steel', 'imp', 180, 5, 'common',
     'Chronibble is a Psychic and Steel type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (343, 'Temporax', 'Psychic/Steel', 'imp', 222, 6, 'common',
     'Temporax is a Psychic and Steel type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (344, 'Starvix', 'Dragon/Flying', 'dragon', 204, 6, 'common',
     'Starvix is a Dragon and Flying type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (345, 'Galaxorun', 'Dragon/Flying', 'dragon', 246, 8, 'common',
     'Galaxorun is a Dragon and Flying type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    # ---- #347 to #446 (v18.1) ----
    (347, 'Emberlynx', 'Fire', 'quad', 252, 8, 'common',
     'Emberlynx is a Fire type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Cinder Lash', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (348, 'Thornibble', 'Grass', 'plant', 288, 6, 'common',
     'Thornibble is a Grass type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Thorn Whip', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (349, 'Aquavolt', 'Water/Electric', 'fish', 240, 8, 'common',
     'Aquavolt is a Water and Electric type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (350, 'Cragoon', 'Rock', 'golem', 330, 7, 'common',
     'Cragoon is a Rock type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Pebble Blast', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (351, 'Zephyroo', 'Flying', 'bird', 234, 7, 'common',
     'Zephyroo is a Flying type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Wing Flick', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (352, 'Snowhopper', 'Ice', 'quad', 258, 7, 'common',
     'Snowhopper is a Ice type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Frost Bite', 40, 'Ice'),
      ('Quick Dash', 32, 'Normal')]),
    (353, 'Duskmite', 'Dark', 'imp', 216, 9, 'common',
     'Duskmite is a Dark type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Sneak Bite', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (354, 'Lumisprout', 'Light', 'orb', 270, 7, 'common',
     'Lumisprout is a Light type. It glows softly to light up dark paths.',
     [('Gleam Rush', 42, 'Light'),
      ('Radiant Flash', 46, 'Light'),
      ('Glow Flash', 40, 'Light'),
      ('Quick Dash', 32, 'Normal')]),
    (355, 'Sparktusk', 'Electric', 'orb', 264, 9, 'common',
     'Sparktusk is a Electric type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Static Snap', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (356, 'Lavaclaw', 'Fire/Rock', 'quad', 312, 10, 'common',
     'Lavaclaw is a Fire and Rock type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (357, 'Mossquake', 'Grass/Ground', 'plant', 348, 8, 'common',
     'Mossquake is a Grass and Ground type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (358, 'Puffloon', 'Water/Flying', 'fish', 246, 6, 'common',
     'Puffloon is a Water and Flying type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (359, 'Shardrake', 'Dragon/Rock', 'dragon', 294, 10, 'common',
     'Shardrake is a Dragon and Rock type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (360, 'Noctibloom', 'Dark/Grass', 'imp', 276, 8, 'common',
     'Noctibloom is a Dark and Grass type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (361, 'Starwhisk', 'Psychic', 'imp', 228, 9, 'common',
     'Starwhisk is a Psychic type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Mind Poke', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (362, 'Ironmunk', 'Steel', 'golem', 318, 8, 'common',
     'Ironmunk is a Steel type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Iron Tap', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (363, 'Venomurk', 'Poison', 'bug', 264, 9, 'common',
     'Venomurk is a Poison type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Acid Spit', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (364, 'Sandrillo', 'Ground', 'golem', 306, 8, 'common',
     'Sandrillo is a Ground type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Sand Whirl', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (365, 'Frostalon', 'Ice/Flying', 'quad', 240, 9, 'common',
     'Frostalon is a Ice and Flying type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (366, 'Cindervine', 'Fire/Grass', 'quad', 282, 9, 'common',
     'Cindervine is a Fire and Grass type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (367, 'Reeflisk', 'Water/Rock', 'fish', 336, 7, 'common',
     'Reeflisk is a Water and Rock type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (368, 'Psydrake', 'Psychic/Dragon', 'imp', 270, 10, 'common',
     'Psydrake is a Psychic and Dragon type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (369, 'Thunderjaw', 'Electric/Dragon', 'orb', 300, 11, 'common',
     'Thunderjaw is a Electric and Dragon type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (370, 'Wraithorn', 'Ghost', 'ghost', 222, 10, 'common',
     'Wraithorn is a Ghost type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Haunt Touch', 40, 'Ghost'),
      ('Quick Dash', 32, 'Normal')]),
    (371, 'Bloomora', 'Grass/Fairy', 'plant', 294, 7, 'common',
     'Bloomora is a Grass and Fairy type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (372, 'Cindermole', 'Fire/Ground', 'quad', 324, 10, 'common',
     'Cindermole is a Fire and Ground type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (373, 'Skyrindle', 'Flying/Steel', 'bird', 258, 8, 'common',
     'Skyrindle is a Flying and Steel type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (374, 'Abysskit', 'Water/Dark', 'fish', 252, 9, 'common',
     'Abysskit is a Water and Dark type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (375, 'Runebark', 'Grass/Rock', 'plant', 342, 8, 'common',
     'Runebark is a Grass and Rock type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (376, 'Glimmerax', 'Light/Steel', 'orb', 276, 10, 'common',
     'Glimmerax is a Light and Steel type. It glows softly to light up dark paths.',
     [('Gleam Rush', 42, 'Light'),
      ('Radiant Flash', 46, 'Light'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (377, 'Shockfin', 'Water/Electric', 'fish', 234, 9, 'common',
     'Shockfin is a Water and Electric type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (378, 'Dracinder', 'Dragon/Fire', 'dragon', 288, 11, 'common',
     'Dracinder is a Dragon and Fire type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Ember Rush', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (379, 'Gravibite', 'Ground/Dark', 'golem', 312, 10, 'common',
     'Gravibite is a Ground and Dark type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (380, 'Silvershade', 'Ghost/Steel', 'ghost', 264, 9, 'common',
     'Silvershade is a Ghost and Steel type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (381, 'Thornlisk', 'Grass/Poison', 'plant', 282, 8, 'common',
     'Thornlisk is a Grass and Poison type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Toxic Spray', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (382, 'Cryomunk', 'Ice/Fighting', 'quad', 270, 9, 'common',
     'Cryomunk is a Ice and Fighting type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (383, 'Astraloon', 'Psychic/Flying', 'imp', 246, 7, 'common',
     'Astraloon is a Psychic and Flying type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (384, 'Bronzefang', 'Steel/Dragon', 'golem', 336, 10, 'common',
     'Bronzefang is a Steel and Dragon type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (385, 'Flarefinch', 'Fire/Flying', 'quad', 228, 8, 'common',
     'Flarefinch is a Fire and Flying type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (386, 'Moonmire', 'Dark/Water', 'imp', 300, 9, 'common',
     'Moonmire is a Dark and Water type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (387, 'Quakettle', 'Ground/Steel', 'golem', 354, 8, 'common',
     'Quakettle is a Ground and Steel type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (388, 'Virellume', 'Fairy/Grass', 'orb', 258, 7, 'common',
     'Virellume is a Fairy and Grass type. It scatters glitter when it is happy.',
     [('Charm Burst', 42, 'Fairy'),
      ('Moon Kiss', 46, 'Fairy'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (389, 'Obsidrill', 'Rock/Dark', 'golem', 330, 11, 'common',
     'Obsidrill is a Rock and Dark type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (390, 'Mindpixie', 'Psychic/Fairy', 'imp', 240, 7, 'common',
     'Mindpixie is a Psychic and Fairy type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (391, 'Stormant', 'Electric/Bug', 'orb', 252, 9, 'common',
     'Stormant is a Electric and Bug type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (392, 'Blazelisk', 'Fire/Dragon', 'quad', 306, 11, 'common',
     'Blazelisk is a Fire and Dragon type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (393, 'Glimmerfin', 'Water/Light', 'fish', 264, 8, 'common',
     'Glimmerfin is a Water and Light type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Gleam Rush', 40, 'Light'),
      ('Quick Dash', 32, 'Normal')]),
    (394, 'Bramblox', 'Grass/Ground', 'plant', 348, 9, 'common',
     'Bramblox is a Grass and Ground type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (395, 'Hauntusk', 'Ghost/Ground', 'ghost', 294, 10, 'common',
     'Hauntusk is a Ghost and Ground type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (396, 'Skyrune', 'Flying/Psychic', 'bird', 240, 8, 'common',
     'Skyrune is a Flying and Psychic type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (397, 'Frostmire', 'Ice/Dark', 'quad', 282, 9, 'common',
     'Frostmire is a Ice and Dark type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (398, 'Voltibex', 'Electric/Rock', 'orb', 318, 10, 'common',
     'Voltibex is a Electric and Rock type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (399, 'Sunspindle', 'Fire/Light', 'quad', 270, 9, 'common',
     'Sunspindle is a Fire and Light type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Gleam Rush', 40, 'Light'),
      ('Quick Dash', 32, 'Normal')]),
    (400, 'Dracobble', 'Dragon/Ground', 'dragon', 342, 11, 'common',
     'Dracobble is a Dragon and Ground type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (401, 'Murkettle', 'Poison/Water', 'bug', 288, 8, 'common',
     'Murkettle is a Poison and Water type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (402, 'Ironpetal', 'Steel/Grass', 'golem', 312, 8, 'common',
     'Ironpetal is a Steel and Grass type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (403, 'Gloomaroo', 'Dark/Fairy', 'imp', 234, 9, 'common',
     'Gloomaroo is a Dark and Fairy type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (404, 'Tundrake', 'Ice/Dragon', 'quad', 324, 11, 'common',
     'Tundrake is a Ice and Dragon type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (405, 'Sparkroot', 'Electric/Grass', 'orb', 258, 9, 'common',
     'Sparkroot is a Electric and Grass type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (406, 'Frostowl', 'Ice/Psychic', 'quad', 246, 8, 'common',
     'Frostowl is a Ice and Psychic type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (407, 'Dreadfin', 'Dark/Water', 'imp', 300, 10, 'common',
     'Dreadfin is a Dark and Water type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (408, 'Magmaraft', 'Fire/Water', 'quad', 330, 10, 'common',
     'Magmaraft is a Fire and Water type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (409, 'Lunaclaw', 'Light/Dark', 'orb', 264, 10, 'common',
     'Lunaclaw is a Light and Dark type. It glows softly to light up dark paths.',
     [('Gleam Rush', 42, 'Light'),
      ('Radiant Flash', 46, 'Light'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (410, 'Quillquake', 'Ground/Bug', 'golem', 276, 8, 'common',
     'Quillquake is a Ground and Bug type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (411, 'Venoshard', 'Poison/Rock', 'bug', 312, 10, 'common',
     'Venoshard is a Poison and Rock type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (412, 'Nimbudrake', 'Dragon/Flying', 'dragon', 282, 10, 'common',
     'Nimbudrake is a Dragon and Flying type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (413, 'Mossmunk', 'Grass/Fighting', 'plant', 294, 9, 'common',
     'Mossmunk is a Grass and Fighting type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (414, 'Rimefang', 'Ice/Steel', 'quad', 330, 10, 'common',
     'Rimefang is a Ice and Steel type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (415, 'Starviper', 'Psychic/Poison', 'imp', 240, 10, 'common',
     'Starviper is a Psychic and Poison type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Toxic Spray', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (416, 'Embercoil', 'Fire/Electric', 'quad', 276, 10, 'common',
     'Embercoil is a Fire and Electric type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (417, 'Hollowisp', 'Ghost/Fairy', 'ghost', 228, 7, 'common',
     'Hollowisp is a Ghost and Fairy type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (418, 'Rockraven', 'Rock/Flying', 'golem', 318, 9, 'common',
     'Rockraven is a Rock and Flying type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (419, 'Aquarune', 'Water/Psychic', 'fish', 270, 8, 'common',
     'Aquarune is a Water and Psychic type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (420, 'Dusklance', 'Dark/Steel', 'imp', 306, 11, 'common',
     'Dusklance is a Dark and Steel type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (421, 'Thornwing', 'Grass/Flying', 'plant', 258, 8, 'common',
     'Thornwing is a Grass and Flying type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (422, 'Pyrocrust', 'Fire/Bug', 'quad', 288, 10, 'common',
     'Pyrocrust is a Fire and Bug type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (423, 'Frostbell', 'Ice/Fairy', 'quad', 252, 7, 'common',
     'Frostbell is a Ice and Fairy type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (424, 'Voltshade', 'Electric/Ghost', 'orb', 234, 10, 'common',
     'Voltshade is a Electric and Ghost type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Shade Touch', 40, 'Ghost'),
      ('Quick Dash', 32, 'Normal')]),
    (425, 'Dracolith', 'Dragon/Rock', 'dragon', 348, 11, 'common',
     'Dracolith is a Dragon and Rock type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (426, 'Mirebloom', 'Poison/Grass', 'bug', 300, 9, 'common',
     'Mirebloom is a Poison and Grass type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (427, 'Sunmole', 'Ground/Light', 'golem', 324, 9, 'common',
     'Sunmole is a Ground and Light type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Gleam Rush', 40, 'Light'),
      ('Quick Dash', 32, 'Normal')]),
    (428, 'Ironcrest', 'Steel/Flying', 'golem', 282, 9, 'common',
     'Ironcrest is a Steel and Flying type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (429, 'Moonfinch', 'Dark/Flying', 'imp', 240, 8, 'common',
     'Moonfinch is a Dark and Flying type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (430, 'Prismole', 'Light/Ground', 'orb', 312, 8, 'common',
     'Prismole is a Light and Ground type. It glows softly to light up dark paths.',
     [('Gleam Rush', 42, 'Light'),
      ('Radiant Flash', 46, 'Light'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (431, 'Shiverjaw', 'Ice/Water', 'quad', 336, 10, 'common',
     'Shiverjaw is a Ice and Water type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (432, 'Shadebramble', 'Grass/Dark', 'plant', 294, 10, 'common',
     'Shadebramble is a Grass and Dark type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (433, 'Stormshell', 'Electric/Rock', 'orb', 342, 10, 'common',
     'Stormshell is a Electric and Rock type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (434, 'Phantorch', 'Ghost/Fire', 'ghost', 246, 9, 'common',
     'Phantorch is a Ghost and Fire type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Ember Rush', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (435, 'Celestusk', 'Psychic/Steel', 'imp', 300, 10, 'common',
     'Celestusk is a Psychic and Steel type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (436, 'Mudrindle', 'Ground/Water', 'golem', 330, 8, 'common',
     'Mudrindle is a Ground and Water type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (437, 'Flarelynx', 'Fire/Dark', 'quad', 264, 11, 'common',
     'Flarelynx is a Fire and Dark type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (438, 'Glimmeroo', 'Fairy/Light', 'orb', 252, 8, 'common',
     'Glimmeroo is a Fairy and Light type. It scatters glitter when it is happy.',
     [('Charm Burst', 42, 'Fairy'),
      ('Moon Kiss', 46, 'Fairy'),
      ('Gleam Rush', 40, 'Light'),
      ('Quick Dash', 32, 'Normal')]),
    (439, 'Venomwing', 'Poison/Flying', 'bug', 234, 9, 'common',
     'Venomwing is a Poison and Flying type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (440, 'Cragfin', 'Rock/Water', 'golem', 348, 9, 'common',
     'Cragfin is a Rock and Water type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (441, 'Dreamurk', 'Psychic/Dark', 'imp', 258, 10, 'common',
     'Dreamurk is a Psychic and Dark type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (442, 'Ironmire', 'Steel/Poison', 'golem', 324, 9, 'common',
     'Ironmire is a Steel and Poison type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Toxic Spray', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (443, 'Solavine', 'Fire/Grass', 'quad', 288, 10, 'common',
     'Solavine is a Fire and Grass type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (444, 'Nightquill', 'Dark/Bug', 'imp', 246, 9, 'common',
     'Nightquill is a Dark and Bug type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (445, 'Astradrake', 'Dragon/Light', 'dragon', 312, 11, 'common',
     'Astradrake is a Dragon and Light type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Gleam Rush', 40, 'Light'),
      ('Quick Dash', 32, 'Normal')]),
    (446, 'Voidrindle', 'Void', 'ghost', 276, 11, 'common',
     'Voidrindle is a Void type. It flickers in and out of sight.',
     [('Null Rush', 42, 'Void'),
      ('Rift Bite', 46, 'Void'),
      ('Null Touch', 40, 'Void'),
      ('Quick Dash', 32, 'Normal')]),
    # ---- #447 to #546 (v18.2) ----
    (447, 'Cobaltusk', 'Steel/Water', 'golem', 330, 9, 'common',
     'Cobaltusk is a Steel and Water type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (448, 'Fluffernox', 'Fairy', 'orb', 264, 6, 'common',
     'Fluffernox is a Fairy type. It scatters glitter when it is happy.',
     [('Charm Burst', 42, 'Fairy'),
      ('Moon Kiss', 46, 'Fairy'),
      ('Glitter Puff', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (449, 'Riftalon', 'Void/Flying', 'ghost', 252, 10, 'common',
     'Riftalon is a Void and Flying type. It flickers in and out of sight.',
     [('Null Rush', 42, 'Void'),
      ('Rift Bite', 46, 'Void'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (450, 'Blazebrook', 'Fire/Water', 'quad', 294, 10, 'common',
     'Blazebrook is a Fire and Water type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (451, 'Fernaconda', 'Grass/Dragon', 'plant', 318, 10, 'common',
     'Fernaconda is a Grass and Dragon type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (452, 'Quarzelle', 'Rock/Fairy', 'golem', 288, 7, 'common',
     'Quarzelle is a Rock and Fairy type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (453, 'Glitchimp', 'Glitch', 'orb', 240, 11, 'common',
     'Glitchimp is a Glitch type. It jumps between screens and scrambles nearby pixels.',
     [('Data Rush', 42, 'Glitch'),
      ('Byte Crash', 46, 'Glitch'),
      ('Bit Flip', 40, 'Glitch'),
      ('Quick Dash', 32, 'Normal')]),
    (454, 'Frostbyte', 'Ice/Electric', 'quad', 258, 9, 'common',
     'Frostbyte is a Ice and Electric type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (455, 'Duskodon', 'Dark/Rock', 'imp', 354, 11, 'common',
     'Duskodon is a Dark and Rock type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (456, 'Radiadrake', 'Light/Dragon', 'orb', 300, 11, 'common',
     'Radiadrake is a Light and Dragon type. It glows softly to light up dark paths.',
     [('Gleam Rush', 42, 'Light'),
      ('Radiant Flash', 46, 'Light'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (457, 'Shellume', 'Water/Light', 'fish', 312, 7, 'common',
     'Shellume is a Water and Light type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Gleam Rush', 40, 'Light'),
      ('Quick Dash', 32, 'Normal')]),
    (458, 'Briarbolt', 'Grass/Electric', 'plant', 264, 9, 'common',
     'Briarbolt is a Grass and Electric type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (459, 'Cindercrab', 'Fire/Water', 'quad', 306, 10, 'common',
     'Cindercrab is a Fire and Water type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (460, 'Vesperwing', 'Ghost/Flying', 'ghost', 234, 8, 'common',
     'Vesperwing is a Ghost and Flying type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (461, 'Mudmantis', 'Ground/Bug', 'golem', 282, 9, 'common',
     'Mudmantis is a Ground and Bug type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (462, 'Starforge', 'Psychic/Steel', 'imp', 324, 10, 'common',
     'Starforge is a Psychic and Steel type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (463, 'Drizzleon', 'Water', 'fish', 276, 7, 'common',
     'Drizzleon is a Water type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Bubble Barrage', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (464, 'Pyrospike', 'Fire/Steel', 'quad', 318, 11, 'common',
     'Pyrospike is a Fire and Steel type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (465, 'Gloomshell', 'Dark/Water', 'imp', 336, 9, 'common',
     'Gloomshell is a Dark and Water type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (466, 'Vineviper', 'Grass/Poison', 'plant', 252, 10, 'common',
     'Vineviper is a Grass and Poison type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Toxic Spray', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (467, 'Crysthorn', 'Ice/Rock', 'quad', 342, 10, 'common',
     'Crysthorn is a Ice and Rock type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (468, 'Voltwing', 'Electric/Flying', 'orb', 240, 9, 'common',
     'Voltwing is a Electric and Flying type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (469, 'Phantomole', 'Ghost/Ground', 'ghost', 300, 10, 'common',
     'Phantomole is a Ghost and Ground type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (470, 'Sunquill', 'Light/Flying', 'orb', 258, 8, 'common',
     'Sunquill is a Light and Flying type. It glows softly to light up dark paths.',
     [('Gleam Rush', 42, 'Light'),
      ('Radiant Flash', 46, 'Light'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (471, 'Bronzebloom', 'Steel/Grass', 'golem', 330, 8, 'common',
     'Bronzebloom is a Steel and Grass type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (472, 'Abysswisp', 'Void/Water', 'ghost', 270, 10, 'common',
     'Abysswisp is a Void and Water type. It flickers in and out of sight.',
     [('Null Rush', 42, 'Void'),
      ('Rift Bite', 46, 'Void'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (473, 'Magmabuck', 'Fire/Rock', 'quad', 348, 11, 'common',
     'Magmabuck is a Fire and Rock type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (474, 'Mindmoth', 'Psychic/Bug', 'imp', 228, 7, 'common',
     'Mindmoth is a Psychic and Bug type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (475, 'Stormsheller', 'Electric/Water', 'orb', 324, 9, 'common',
     'Stormsheller is a Electric and Water type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (476, 'Duskraven', 'Dark/Flying', 'imp', 252, 10, 'common',
     'Duskraven is a Dark and Flying type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (477, 'Petaldrake', 'Grass/Dragon', 'plant', 306, 11, 'common',
     'Petaldrake is a Grass and Dragon type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (478, 'Glacipillar', 'Ice/Bug', 'quad', 276, 7, 'common',
     'Glacipillar is a Ice and Bug type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (479, 'Runefang', 'Psychic/Rock', 'imp', 318, 10, 'common',
     'Runefang is a Psychic and Rock type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (480, 'Embermoth', 'Fire/Bug', 'quad', 240, 9, 'common',
     'Embermoth is a Fire and Bug type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (481, 'Ironjawl', 'Steel/Dark', 'golem', 348, 11, 'common',
     'Ironjawl is a Steel and Dark type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (482, 'Cloudfin', 'Flying/Water', 'bird', 246, 7, 'common',
     'Cloudfin is a Flying and Water type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (483, 'Thornclad', 'Grass/Steel', 'plant', 336, 9, 'common',
     'Thornclad is a Grass and Steel type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (484, 'Voidmunk', 'Void/Fighting', 'ghost', 282, 11, 'common',
     'Voidmunk is a Void and Fighting type. It flickers in and out of sight.',
     [('Null Rush', 42, 'Void'),
      ('Rift Bite', 46, 'Void'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (485, 'Quakwing', 'Ground/Flying', 'golem', 300, 9, 'common',
     'Quakwing is a Ground and Flying type. It digs burrows under rocky hills.',
     [('Quake Stomp', 42, 'Ground'),
      ('Earth Spike', 46, 'Ground'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (486, 'Luminox', 'Light', 'orb', 252, 8, 'common',
     'Luminox is a Light type. It glows softly to light up dark paths.',
     [('Gleam Rush', 42, 'Light'),
      ('Radiant Flash', 46, 'Light'),
      ('Glow Flash', 40, 'Light'),
      ('Quick Dash', 32, 'Normal')]),
    (487, 'Feralith', 'Rock/Fighting', 'golem', 354, 11, 'common',
     'Feralith is a Rock and Fighting type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (488, 'Toxifern', 'Poison/Grass', 'bug', 270, 9, 'common',
     'Toxifern is a Poison and Grass type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (489, 'Astravine', 'Psychic/Grass', 'imp', 288, 8, 'common',
     'Astravine is a Psychic and Grass type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (490, 'Frostmantle', 'Ice/Steel', 'quad', 360, 9, 'common',
     'Frostmantle is a Ice and Steel type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (491, 'Shockrill', 'Electric/Ground', 'orb', 294, 10, 'common',
     'Shockrill is a Electric and Ground type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (492, 'Nightbloom', 'Dark/Fairy', 'imp', 264, 8, 'common',
     'Nightbloom is a Dark and Fairy type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (493, 'Cindermane', 'Fire', 'quad', 318, 11, 'common',
     'Cindermane is a Fire type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Cinder Lash', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (494, 'Reefrake', 'Water/Dragon', 'fish', 330, 11, 'common',
     'Reefrake is a Water and Dragon type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (495, 'Glitchowl', 'Glitch/Flying', 'orb', 228, 10, 'common',
     'Glitchowl is a Glitch and Flying type. It jumps between screens and scrambles nearby pixels.',
     [('Data Rush', 42, 'Glitch'),
      ('Byte Crash', 46, 'Glitch'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (496, 'Obsidibun', 'Rock/Dark', 'golem', 300, 9, 'common',
     'Obsidibun is a Rock and Dark type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (497, 'Silvermole', 'Steel/Ground', 'golem', 342, 9, 'common',
     'Silvermole is a Steel and Ground type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (498, 'Flarebloom', 'Fire/Fairy', 'quad', 258, 9, 'common',
     'Flarebloom is a Fire and Fairy type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (499, 'Mistralisk', 'Flying/Poison', 'bird', 240, 8, 'common',
     'Mistralisk is a Flying and Poison type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Toxic Spray', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (500, 'Wyrmflare', 'Dragon/Fire', 'dragon', 342, 12, 'common',
     'Wyrmflare is a Dragon and Fire type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Ember Rush', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (501, 'Deepquill', 'Water/Dark', 'fish', 288, 10, 'common',
     'Deepquill is a Water and Dark type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (502, 'Mossclaw', 'Grass/Fighting', 'plant', 324, 10, 'common',
     'Mossclaw is a Grass and Fighting type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (503, 'Starshard', 'Psychic/Rock', 'imp', 276, 9, 'common',
     'Starshard is a Psychic and Rock type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (504, 'Frostwhisk', 'Ice/Fairy', 'quad', 246, 8, 'common',
     'Frostwhisk is a Ice and Fairy type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (505, 'Thunderbark', 'Electric/Grass', 'orb', 336, 10, 'common',
     'Thunderbark is a Electric and Grass type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (506, 'Ashenox', 'Fire/Ghost', 'quad', 270, 11, 'common',
     'Ashenox is a Fire and Ghost type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Shade Touch', 40, 'Ghost'),
      ('Quick Dash', 32, 'Normal')]),
    (507, 'Dreadmire', 'Dark/Poison', 'imp', 312, 10, 'common',
     'Dreadmire is a Dark and Poison type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Toxic Spray', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (508, 'Cloudspire', 'Flying/Steel', 'bird', 294, 9, 'common',
     'Cloudspire is a Flying and Steel type. It rides the wind high above the trees.',
     [('Gale Swoop', 42, 'Flying'),
      ('Wing Dive', 46, 'Flying'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (509, 'Runecrab', 'Water/Psychic', 'fish', 306, 8, 'common',
     'Runecrab is a Water and Psychic type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (510, 'Voidraven', 'Void/Dark', 'ghost', 264, 11, 'common',
     'Voidraven is a Void and Dark type. It flickers in and out of sight.',
     [('Null Rush', 42, 'Void'),
      ('Rift Bite', 46, 'Void'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (511, 'Bramblejaw', 'Grass/Rock', 'plant', 360, 11, 'common',
     'Bramblejaw is a Grass and Rock type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (512, 'Pyrolyn', 'Fire/Electric', 'quad', 252, 10, 'common',
     'Pyrolyn is a Fire and Electric type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Spark Dash', 40, 'Electric'),
      ('Quick Dash', 32, 'Normal')]),
    (513, 'Glimmerfinch', 'Light/Flying', 'orb', 234, 7, 'common',
     'Glimmerfinch is a Light and Flying type. It glows softly to light up dark paths.',
     [('Gleam Rush', 42, 'Light'),
      ('Radiant Flash', 46, 'Light'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (514, 'Steelthorn', 'Steel/Grass', 'golem', 348, 10, 'common',
     'Steelthorn is a Steel and Grass type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (515, 'Miregeist', 'Ghost/Poison', 'ghost', 258, 10, 'common',
     'Miregeist is a Ghost and Poison type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Toxic Spray', 40, 'Poison'),
      ('Quick Dash', 32, 'Normal')]),
    (516, 'Aquashard', 'Water/Ice', 'fish', 300, 8, 'common',
     'Aquashard is a Water and Ice type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Frost Dash', 40, 'Ice'),
      ('Quick Dash', 32, 'Normal')]),
    (517, 'Dracobram', 'Dragon/Fighting', 'dragon', 330, 12, 'common',
     'Dracobram is a Dragon and Fighting type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (518, 'Sparkmole', 'Electric/Ground', 'orb', 282, 9, 'common',
     'Sparkmole is a Electric and Ground type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (519, 'Duskwyrm', 'Dark/Dragon', 'imp', 324, 11, 'common',
     'Duskwyrm is a Dark and Dragon type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (520, 'Lunalith', 'Light/Rock', 'orb', 354, 9, 'common',
     'Lunalith is a Light and Rock type. It glows softly to light up dark paths.',
     [('Gleam Rush', 42, 'Light'),
      ('Radiant Flash', 46, 'Light'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
    (521, 'Petalwing', 'Grass/Flying', 'plant', 240, 8, 'common',
     'Petalwing is a Grass and Flying type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (522, 'Magmashade', 'Fire/Dark', 'quad', 306, 11, 'common',
     'Magmashade is a Fire and Dark type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (523, 'Cryorune', 'Ice/Psychic', 'quad', 270, 9, 'common',
     'Cryorune is a Ice and Psychic type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Mind Ripple', 40, 'Psychic'),
      ('Quick Dash', 32, 'Normal')]),
    (524, 'Riftclaw', 'Void/Fighting', 'ghost', 312, 12, 'common',
     'Riftclaw is a Void and Fighting type. It flickers in and out of sight.',
     [('Null Rush', 42, 'Void'),
      ('Rift Bite', 46, 'Void'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (525, 'Venomcrest', 'Poison/Flying', 'bug', 276, 10, 'common',
     'Venomcrest is a Poison and Flying type. It leaves a sticky trail wherever it goes.',
     [('Toxic Spray', 42, 'Poison'),
      ('Venom Crash', 46, 'Poison'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (526, 'Cragmantis', 'Rock/Bug', 'golem', 342, 10, 'common',
     'Cragmantis is a Rock and Bug type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (527, 'Sunflarex', 'Fire/Light', 'quad', 288, 11, 'common',
     'Sunflarex is a Fire and Light type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Gleam Rush', 40, 'Light'),
      ('Quick Dash', 32, 'Normal')]),
    (528, 'Mindshroud', 'Psychic/Ghost', 'imp', 252, 10, 'common',
     'Mindshroud is a Psychic and Ghost type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Shade Touch', 40, 'Ghost'),
      ('Quick Dash', 32, 'Normal')]),
    (529, 'Ironquill', 'Steel/Flying', 'golem', 300, 9, 'common',
     'Ironquill is a Steel and Flying type. It polishes its shiny body with dust.',
     [('Metal Claw', 42, 'Steel'),
      ('Iron Ram', 46, 'Steel'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (530, 'Stormfang', 'Electric/Dragon', 'orb', 336, 12, 'common',
     'Stormfang is a Electric and Dragon type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (531, 'Gloomfin', 'Dark/Water', 'imp', 294, 10, 'common',
     'Gloomfin is a Dark and Water type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (532, 'Mossbell', 'Grass/Fairy', 'plant', 276, 7, 'common',
     'Mossbell is a Grass and Fairy type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (533, 'Glacidrake', 'Ice/Dragon', 'quad', 348, 12, 'common',
     'Glacidrake is a Ice and Dragon type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Dragon Rush', 40, 'Dragon'),
      ('Quick Dash', 32, 'Normal')]),
    (534, 'Obsidivine', 'Rock/Grass', 'golem', 330, 10, 'common',
     'Obsidivine is a Rock and Grass type. It sits still for hours, looking like a boulder.',
     [('Boulder Hurl', 42, 'Rock'),
      ('Rock Crash', 46, 'Rock'),
      ('Leaf Rush', 40, 'Grass'),
      ('Quick Dash', 32, 'Normal')]),
    (535, 'Voltuskull', 'Electric/Dark', 'orb', 282, 11, 'common',
     'Voltuskull is a Electric and Dark type. It crackles with static when it runs.',
     [('Spark Dash', 42, 'Electric'),
      ('Volt Surge', 46, 'Electric'),
      ('Night Slash', 40, 'Dark'),
      ('Quick Dash', 32, 'Normal')]),
    (536, 'Phantasmole', 'Ghost/Ground', 'ghost', 312, 10, 'common',
     'Phantasmole is a Ghost and Ground type. It drifts through old ruins at night.',
     [('Shade Touch', 42, 'Ghost'),
      ('Spirit Pull', 46, 'Ghost'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (537, 'Coralwing', 'Water/Flying', 'fish', 258, 8, 'common',
     'Coralwing is a Water and Flying type. It splashes in streams and shallow pools.',
     [('Tide Rush', 42, 'Water'),
      ('Aqua Jet', 46, 'Water'),
      ('Gale Swoop', 40, 'Flying'),
      ('Quick Dash', 32, 'Normal')]),
    (538, 'Pyroforge', 'Fire/Steel', 'quad', 360, 12, 'common',
     'Pyroforge is a Fire and Steel type. It warms its nest with a small flame.',
     [('Ember Rush', 42, 'Fire'),
      ('Blaze Wave', 46, 'Fire'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (539, 'Starbloom', 'Psychic/Fairy', 'imp', 264, 8, 'common',
     'Starbloom is a Psychic and Fairy type. It hums quietly and seems to know what you are thinking.',
     [('Mind Ripple', 42, 'Psychic'),
      ('Psy Beam', 46, 'Psychic'),
      ('Charm Burst', 40, 'Fairy'),
      ('Quick Dash', 32, 'Normal')]),
    (540, 'Voidmantle', 'Void/Steel', 'ghost', 366, 11, 'common',
     'Voidmantle is a Void and Steel type. It flickers in and out of sight.',
     [('Null Rush', 42, 'Void'),
      ('Rift Bite', 46, 'Void'),
      ('Metal Claw', 40, 'Steel'),
      ('Quick Dash', 32, 'Normal')]),
    (541, 'Thornquake', 'Grass/Ground', 'plant', 348, 10, 'common',
     'Thornquake is a Grass and Ground type. It soaks up sunlight through its leaves.',
     [('Leaf Rush', 42, 'Grass'),
      ('Petal Blast', 46, 'Grass'),
      ('Quake Stomp', 40, 'Ground'),
      ('Quick Dash', 32, 'Normal')]),
    (542, 'Duskrill', 'Dark/Bug', 'imp', 240, 9, 'common',
     'Duskrill is a Dark and Bug type. It hunts in the shadows after sunset.',
     [('Night Slash', 42, 'Dark'),
      ('Shadow Pounce', 46, 'Dark'),
      ('Swarm Bite', 40, 'Bug'),
      ('Quick Dash', 32, 'Normal')]),
    (543, 'Frostflare', 'Ice/Fire', 'quad', 306, 11, 'common',
     'Frostflare is a Ice and Fire type. It shivers in the cold and frosts the ground.',
     [('Frost Dash', 42, 'Ice'),
      ('Glacier Spike', 46, 'Ice'),
      ('Ember Rush', 40, 'Fire'),
      ('Quick Dash', 32, 'Normal')]),
    (544, 'Lumiclaw', 'Light/Fighting', 'orb', 288, 11, 'common',
     'Lumiclaw is a Light and Fighting type. It glows softly to light up dark paths.',
     [('Gleam Rush', 42, 'Light'),
      ('Radiant Flash', 46, 'Light'),
      ('Brawl Strike', 40, 'Fighting'),
      ('Quick Dash', 32, 'Normal')]),
    (545, 'Riftfin', 'Void/Water', 'ghost', 318, 11, 'common',
     'Riftfin is a Void and Water type. It flickers in and out of sight.',
     [('Null Rush', 42, 'Void'),
      ('Rift Bite', 46, 'Void'),
      ('Tide Rush', 40, 'Water'),
      ('Quick Dash', 32, 'Normal')]),
    (546, 'Dracostone', 'Dragon/Rock', 'dragon', 372, 12, 'common',
     'Dracostone is a Dragon and Rock type. It guards a hidden cave full of shiny stones.',
     [('Dragon Rush', 42, 'Dragon'),
      ('Wyrm Blast', 46, 'Dragon'),
      ('Boulder Hurl', 40, 'Rock'),
      ('Quick Dash', 32, 'Normal')]),
]

NEW_INFO = {}
RARE_KIND = {}     # name -> "Legendary" or "Mythical"
RARE_CHANCE = {}   # name -> chance per battle (very low)
NEW_COMMON = []
NEW_RARE = []

for _row in NEW_SPECIES_DATA:
    _num, _name, _types, _shape, _hp, _bonus, _rarity, _entry, _moves = _row
    _is_rare = _rarity != "common"
    NEW_INFO[_name] = {
        "number": _num, "types": _types, "shape": _shape,
        "hp": _hp, "bonus": _bonus, "rarity": _rarity,
        "entry": _entry, "moves": _moves,
        "stage": 3 if _is_rare else (_num - 67) % 3 + 1,
        "level": (30, 35) if _is_rare else (3, 12),
    }
    for _move_name, _power, _move_type in _moves:
        MOVE_TYPES[_move_name] = _move_type
    if _is_rare:
        NEW_RARE.append((_num, _name, _types))
        RARE_KIND[_name] = _rarity.capitalize()
        RARE_CHANCE[_name] = 0.002 if _rarity == "legendary" else 0.001
    else:
        NEW_COMMON.append((_num, _name, _types))

# Eclipsar returns from v10.1 as a very rare Mythical Pokemon (#145)
NEW_INFO["Eclipsar"] = {
    "number": 145, "types": "Void/Dragon", "shape": "dragon",
    "hp": 380, "bonus": 10, "rarity": "mythical",
    "entry": ("A void dragon that swallows starlight. The star markings "
              "on its wings glow brighter just before it uses Black Hole."),
    "moves": [("Eclipse Fang", 50, "Dark"), ("Void Wing", 50, "Void"),
              ("Starfall", 55, "Cosmic"), ("Black Hole", 60, "Void")],
    "stage": 3, "level": (35, 40),
}
for _move_name, _power, _move_type in NEW_INFO["Eclipsar"]["moves"]:
    MOVE_TYPES[_move_name] = _move_type
NEW_RARE.append((145, "Eclipsar", "Void/Dragon"))
RARE_KIND["Eclipsar"] = "Mythical"
RARE_CHANCE["Eclipsar"] = 0.003

# Aura Brawler (#346): EVENT ONLY. Never appears in battles or tournaments.
# The only way to get it is the secret gift code in IMPORT CODE.
NEW_INFO["Aura Brawler"] = {
    "number": 346, "types": "Fighting/Steel", "shape": "golem",
    "hp": 330, "bonus": 9, "rarity": "event",
    "entry": ("An armoured brawler that gathers its aura into a blazing orb. "
              "It only appears to trainers who know the secret code."),
    "moves": [("Aura Fist", 62, "Fighting"), ("Bronze Guard Bash", 58, "Steel"),
              ("Visor Flare", 55, "Fire"), ("Aura Orb", 66, "Fighting")],
    "stage": 3, "level": (30, 30),
}
for _move_name, _power, _move_type in NEW_INFO["Aura Brawler"]["moves"]:
    MOVE_TYPES[_move_name] = _move_type
NEW_RARE.append((346, "Aura Brawler", "Fighting/Steel"))
RARE_KIND["Aura Brawler"] = "Event"   # not in RARE_CHANCE, so it never appears

WILD_POKEMON += NEW_COMMON
DEX_ALL = sorted(WILD_POKEMON + NEW_RARE)
DEX_TOTAL = len(DEX_ALL)

# Pokedex entries for the original 66 Pokemon
ORIGINAL_ENTRIES = {
    "Embercub": "A playful cub whose tail flickers like a candle. It sneezes sparks when it gets excited.",
    "Blazepaw": "Its paws leave scorch marks wherever it runs. It guards its den by circling it in fire.",
    "Pyroclaw": "Its claws glow white-hot in battle. It can melt through a steel door in seconds.",
    "Aquaffin": "It skips across ponds on its fins. It is often seen racing boats for fun.",
    "Tidalisk": "It controls small waves with a flick of its tail and rides them along the coast.",
    "Abyssurge": "It lives in the darkest ocean trenches and rises during storms to hunt.",
    "Leaflet": "It naps in the sun to charge the leaf on its head. It wilts when it is sad.",
    "Thornox": "Its back is covered in sharp thorns. It charges anyone who steps on its flowers.",
    "Floragon": "A dragon wrapped in vines and blossoms. Forests grow wherever it sleeps.",
    "Voltkit": "Static builds up in its fur as it plays, so it zaps anyone who pats it.",
    "Shocklynx": "It moves so fast that it leaves a trail of sparks. It hunts during thunderstorms.",
    "Thundermaw": "Its roar sounds like a thunderclap. It stores lightning in its horned jaw.",
    "Frostbit": "It nibbles icicles as snacks. Its breath frosts windows on cold mornings.",
    "Glacieron": "Its body is as hard as a glacier. It can stand still in a blizzard for days.",
    "Cryowraith": "A chilly spirit that drifts through snowy mountains, freezing everything it touches.",
    "Rockruffle": "It rolls down hills for fun and has a thick ruff of pebbles around its neck.",
    "Cragoyle": "It perches on cliffs, looking like a statue, until it swoops on its prey.",
    "Terradon": "An ancient dragon of stone. Earthquakes are said to start when it stomps.",
    "Shadelet": "A shy ghost that hides in shadows and giggles when people jump.",
    "Hauntalon": "It glides silently on misty nights. Its cry sounds like a distant whisper.",
    "Dreadgeist": "Its glowing eyes cause nightmares. Even other ghosts keep their distance.",
    "Mechling": "A small robot-like Pokemon that collects lost screws and bolts.",
    "Ironclast": "Its armour is thick enough to stop a speeding train.",
    "Titanforge": "It hammers its own steel fists into shape. Each punch rings like a bell.",
    "Mindimp": "A cheeky Pokemon that moves objects with its mind to play pranks.",
    "Psyphantom": "It can read minds and appears in dreams to deliver strange messages.",
    "Dreamora": "It spreads sweet dreams with its glittering wings. Children love it.",
    "Venomite": "A tiny bug whose sting makes your arm go numb for hours.",
    "Toxidrake": "A poisonous dragon that leaves bubbling green puddles as it walks.",
    "Skyray": "It rides air currents for hours without flapping once.",
    "Stormeagle": "It flies into storm clouds to recharge its wings with electricity.",
    "Brawlpup": "It practises punching tree trunks every morning and never gives up.",
    "Warfang": "A fierce fighter that only respects trainers who never run from battle.",
    "Fableaf": "It tells stories by rustling its leaves. Some say it can grant small wishes.",
    "Lumifawn": "Its horns shine with soft light that guides lost travellers home.",
    "Gloomora": "It feeds on bad moods. When it is near, people suddenly feel calmer.",
    "Nightreign": "The ruler of the night sky. It only appears when there is no moon.",
    "Bugbyte": "A bug that chews through cables. Computers glitch when it is nearby.",
    "Glitchor": "It lives inside old machines and travels through electrical wires.",
    "Fossilisk": "A dragon brought back from an ancient fossil. Its roar is millions of years old.",
    "Magmole": "It digs tunnels through volcanoes and pops up covered in hot ash.",
    "Spectrill": "A ghost that possessed a suit of armour. It rattles when it laughs.",
    "Starlingo": "It fell from the sky as a shooting star and still sparkles at night.",
    "Galaxion": "Its body holds a tiny swirling galaxy. Looking into it makes you dizzy.",
    "Nullvex": "Nothing is known about it. Cameras show only a blank space where it stands.",
    "NYSTRIA": "A legendary dragon of the void. Tears in the sky appear wherever it flies.",
    "Frolren": "An icy dragon with frosted horns. Snow starts falling whenever it is happy.",
    "Pyrovolt": "A ball of fire and lightning. It bounces around crackling with energy.",
    "Aquarion": "A calm water Pokemon that can sense danger before it happens.",
    "Thornblade": "Its leaves are as sharp as swords. It trims hedges in a single swipe.",
    "Voltraze": "A lightning dragon that strikes the same place twice on purpose.",
    "Glacifang": "Its fangs are made of ice that never melts. Its bite freezes instantly.",
    "Magmanta": "It swims through rivers of lava, leaving glowing ripples behind.",
    "Phantomox": "A ghostly ox with iron horns. Its footsteps echo through empty halls.",
    "Terraboom": "It is known for smashing boulders with its head to find buried gems.",
    "Mindflare": "Its thoughts burn so brightly that its head bursts into psychic flames.",
    "Venomantis": "A mantis with poisoned blades. It waits motionless for hours before striking.",
    "Skyrazor": "Its steel feathers cut through the wind with a whistling sound.",
    "Lumidrake": "A dragon made of light. It is so bright that it lights up whole valleys.",
    "Abyssalon": "A ghost of the deep sea that is said to guide sunken ships.",
    "Dreadhorn": "It charges with its huge horn and never backs down from a fight.",
    "Starflare": "A burning star in Pokemon form. It is hot enough to boil the sea.",
    "Nullshade": "A shadow with no owner. It copies the movements of whoever it follows.",
    "Ironquake": "It stamps its steel feet to make the ground shake for miles.",
    "Florawing": "It scatters seeds as it flies, so flowers bloom along its path.",
    "Chronox": "A cosmic clockwork Pokemon. Time seems to slow down around it.",
}


def make_species(name, level=None):
    info = NEW_INFO[name]
    if level is None:
        level = random.randint(*info["level"])
    mon = Creature(name, info["hp"] + random.randint(0, 15),
                   [(m, p) for m, p, _t in info["moves"]],
                   level=level, bonus=info["bonus"])
    mon.types = info["types"]
    mon.pokedex_number = info["number"]
    return mon


def dex_entry(name, types):
    if name in NEW_INFO:
        return NEW_INFO[name]["entry"]
    if name in ORIGINAL_ENTRIES:
        return ORIGINAL_ENTRIES[name]
    return f"A {types.replace('/', ' and ')} type Pokemon of the New World."


def wrap_text(text, font, width):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if font.size(test)[0] <= width:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def _int_set(values):
    result = set()
    for v in values:
        try:
            result.add(int(v))
        except (TypeError, ValueError):
            pass
    return result



def primary_type(type_text):
    return type_text.split("/")[0]


def get_move_type(move):
    return MOVE_TYPES.get(move, "Normal")


# ==========================================
# TYPE EFFECTIVENESS
# Only non-neutral matchups are listed.
# Anything missing counts as 1x (normal).
# ==========================================

TYPE_CHART = {
    "Normal":   {"Rock": 0.5, "Steel": 0.5, "Ghost": 0},
    "Fire":     {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 2,
                 "Bug": 2, "Rock": 0.5, "Dragon": 0.5, "Steel": 2},
    "Water":    {"Fire": 2, "Water": 0.5, "Grass": 0.5, "Ground": 2,
                 "Rock": 2, "Dragon": 0.5},
    "Electric": {"Water": 2, "Electric": 0.5, "Grass": 0.5,
                 "Ground": 0, "Flying": 2, "Dragon": 0.5},
    "Grass":    {"Fire": 0.5, "Water": 2, "Grass": 0.5, "Poison": 0.5,
                 "Ground": 2, "Flying": 0.5, "Bug": 0.5, "Rock": 2,
                 "Dragon": 0.5, "Steel": 0.5},
    "Ice":      {"Fire": 2, "Water": 0.5, "Grass": 2, "Ice": 0.5,
                 "Ground": 2, "Flying": 2, "Dragon": 2, "Steel": 0.5},
    "Fighting": {"Normal": 2, "Ice": 2, "Poison": 0.5, "Flying": 0.5,
                 "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0,
                 "Dark": 2, "Steel": 2, "Fairy": 0.5},
    "Poison":   {"Grass": 2, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5,
                 "Ghost": 0.5, "Steel": 0, "Fairy": 2},
    "Ground":   {"Fire": 2, "Electric": 2, "Grass": 0.5, "Poison": 2,
                 "Flying": 0, "Bug": 0.5, "Rock": 2, "Steel": 2},
    "Flying":   {"Electric": 0.5, "Grass": 2, "Fighting": 2, "Bug": 2,
                 "Rock": 0.5, "Steel": 0.5},
    "Psychic":  {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Dark": 0,
                 "Steel": 0.5},
    "Bug":      {"Fire": 0.5, "Grass": 2, "Fighting": 0.5, "Poison": 0.5,
                 "Flying": 0.5, "Psychic": 2, "Ghost": 0.5, "Dark": 2,
                 "Steel": 0.5, "Fairy": 0.5},
    "Rock":     {"Fire": 2, "Ice": 2, "Fighting": 0.5, "Ground": 0.5,
                 "Flying": 2, "Bug": 2, "Steel": 0.5},
    "Ghost":    {"Normal": 0, "Psychic": 2, "Ghost": 2, "Dark": 0.5},
    "Dragon":   {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark":     {"Fighting": 0.5, "Psychic": 2, "Ghost": 2,
                 "Dark": 0.5, "Fairy": 0.5},
    "Steel":    {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2,
                 "Rock": 2, "Steel": 0.5, "Fairy": 2},
    "Fairy":    {"Fire": 0.5, "Fighting": 2, "Poison": 0.5, "Dragon": 2,
                 "Dark": 2, "Steel": 0.5},
}


def type_multiplier(move_type, defender_types):
    multiplier = 1.0
    for defender_type in defender_types.split("/"):
        multiplier *= TYPE_CHART.get(move_type, {}).get(defender_type, 1)
    return multiplier


def effectiveness_text(multiplier):
    if multiplier == 0:
        return "It had no effect! "
    if multiplier > 1:
        return "SUPER EFFECTIVE! "
    if multiplier < 1:
        return "Not very effective... "
    return ""


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
        self.shiny = False
        # New in v18.0
        self.bond = 0
        self.titles = []
        self.title = ""
        self.mastery = {}    # move name -> times used
        self.defeats = {}    # type -> Pokemon of that type defeated

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
    if enemy.name == "NYSTRIA" or enemy.name in RARE_KIND:
        return 250
    return 8 + enemy.level * 6


# ==========================================
# MOVES LEARNED BY LEVEL (new in v17.0)
# At each of these levels a Pokemon learns a stronger move.
# Dual types take turns: Lv 15 uses the first type, Lv 25 the second, and so on.
# ==========================================

LEARN_LEVELS = [15, 25, 35, 50, 70]
LEARN_POWERS = [45, 52, 60, 70, 80]

LEARNSET = {
    "Normal":   ["Body Bash", "Rampage Rush", "Mega Stomp", "Giga Slam", "Final Charge"],
    "Fire":     ["Cinder Lash", "Blaze Kick", "Inferno Roar", "Magma Burst", "Solar Inferno"],
    "Water":    ["Bubble Barrage", "Riptide", "Torrent Crash", "Tsunami Slam", "Ocean Fury"],
    "Grass":    ["Thorn Whip", "Seed Storm", "Bloom Blast", "Forest Wrath", "Gaia Bloom"],
    "Electric": ["Static Snap", "Arc Bolt", "Thunder Lance", "Storm Surge", "Zeus Strike"],
    "Ice":      ["Frost Bite", "Hail Spear", "Glacial Crash", "Avalanche Fang", "Absolute Zero"],
    "Rock":     ["Pebble Blast", "Boulder Roll", "Crag Smash", "Landslide", "Meteor Crush"],
    "Ground":   ["Sand Whirl", "Dust Devil", "Fissure Fist", "Tectonic Slam", "World Quake"],
    "Ghost":    ["Haunt Touch", "Spectral Fang", "Wraith Wail", "Soul Rend", "Grave Eclipse"],
    "Steel":    ["Iron Tap", "Bolt Bash", "Titan Fist", "Alloy Cannon", "Steel Tempest"],
    "Psychic":  ["Mind Poke", "Psi Pulse", "Dream Crush", "Astral Mind", "Psychic Nova"],
    "Poison":   ["Acid Spit", "Sludge Bomb", "Toxic Fang", "Venom Torrent", "Plague Storm"],
    "Flying":   ["Wing Flick", "Cyclone Dive", "Tempest Wing", "Hurricane Drop", "Sky Fury"],
    "Fighting": ["Palm Strike", "Dragon Kick", "Iron Fist", "Thousand Blows", "Ultimate Smash"],
    "Fairy":    ["Glitter Puff", "Pixie Beam", "Starlight Kiss", "Moonblast Wave", "Fairy Requiem"],
    "Light":    ["Glow Flash", "Prism Ray", "Dawn Spear", "Halo Burst", "Holy Radiance"],
    "Dark":     ["Sneak Bite", "Shadow Fang", "Midnight Claw", "Eclipse Strike", "Abyss Crush"],
    "Dragon":   ["Drake Bite", "Wyvern Claw", "Draco Storm", "Elder Roar", "Dragon Ascent"],
    "Bug":      ["Silk Shot", "Stinger Rush", "Swarm Storm", "Mega Horn Drill", "Insect Empire"],
    "Cosmic":   ["Star Dust", "Comet Tail", "Nebula Beam", "Supernova", "Big Bang"],
    "Void":     ["Null Touch", "Void Rend", "Rift Collapse", "Event Horizon", "Oblivion"],
    "Glitch":   ["Bit Flip", "Data Corrupt", "Pixel Crash", "Buffer Overflow", "Fatal Error"],
}
for _type, _moves in LEARNSET.items():
    for _move in _moves:
        MOVE_TYPES[_move] = _type


def move_for_level(types, level):
    """The move a Pokemon of these types learns at this level, or None."""
    if level not in LEARN_LEVELS:
        return None
    step = LEARN_LEVELS.index(level)
    own = [t for t in types.split("/") if t in LEARNSET] or ["Normal"]
    move_type = own[step % len(own)]
    return LEARNSET[move_type][step], LEARN_POWERS[step]


def next_move_level(level):
    """The next level at which a new move is learned, or None."""
    return next((lv for lv in LEARN_LEVELS if lv > level), None)


def learn_move(creature):
    """Teaches a new move if the Pokemon just reached a learning level."""
    learned = move_for_level(creature.types, creature.level)
    if not learned:
        return None
    move, power = learned
    if any(m == move for m, _p in creature.moves):
        return None
    if len(creature.moves) < 4:
        creature.moves.append((move, power))
        return f"{creature.name} learned {move}!"
    weakest = min(range(len(creature.moves)), key=lambda i: creature.moves[i][1])
    old = creature.moves[weakest][0]
    creature.moves[weakest] = (move, power)
    return f"{creature.name} forgot {old} and learned {move}!"


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

        evolved = evolve_if_ready(creature)
        if evolved:
            messages.append(evolved)

        learned = learn_move(creature)
        if learned:
            messages.append(learned)

    if creature.level >= MAX_LEVEL:
        creature.xp = 0

    return messages


# ==========================================
# EVOLUTION (new in v16.1)
# The original Pokemon #1-#45 come in families of three.
# Stage 1 evolves at Lv 16, stage 2 evolves at Lv 32.
# ==========================================

EVOLVE_LEVELS = {1: 16, 2: 32}
EVOLUTIONS = {}   # pokedex number -> (level needed, next number, name, types)

for _number, _name, _types in WILD_POKEMON:
    if _number <= 45:
        _stage = (_number - 1) % 3 + 1
        if _stage < 3:
            _next = next(row for row in WILD_POKEMON if row[0] == _number + 1)
            EVOLUTIONS[_number] = (EVOLVE_LEVELS[_stage],) + _next


def evolve_if_ready(creature):
    """Evolves the Pokemon if it is high enough level. Returns a message."""
    info = EVOLUTIONS.get(creature.pokedex_number)
    if not info or creature.level < info[0]:
        return None

    _level, number, name, types = info
    old_name = creature.name
    creature.name = name
    creature.types = types
    creature.pokedex_number = number
    creature.max_hp += 30
    creature.hp = min(creature.max_hp, creature.hp + 30)
    creature.bonus += 4

    # Learns stronger moves that match its new types
    best = max((p for _m, p in creature.moves), default=35)
    creature.moves = [(m, max(p, best) + 8) for m, p in wild_moves(types)]

    # A Pokemon can jump two stages if it levels up a lot at once
    again = evolve_if_ready(creature)
    text = f"{old_name} evolved into {name}!"
    return text + " " + again if again else text


# ==========================================
# REGIONS (back from v4.2)
# Each region has its own common types and colours.
# ==========================================

# name -> (common types, sky colour, ground colour)
REGIONS = {
    "The New World": ((), (35, 70, 115), (35, 105, 80)),
    "Kanto": (("Fire", "Grass", "Water", "Poison"), (60, 110, 170), (55, 130, 70)),
    "Johto": (("Ghost", "Dark", "Psychic", "Fairy"), (55, 45, 100), (50, 85, 75)),
    "Hoenn": (("Water", "Ground", "Dragon", "Fire"), (40, 120, 180), (175, 150, 90)),
    "Sinnoh": (("Steel", "Ice", "Rock", "Dragon"), (100, 130, 170), (210, 225, 240)),
    "Unova": (("Electric", "Dark", "Steel", "Bug"), (45, 50, 85), (70, 80, 95)),
    "Kalos": (("Fairy", "Flying", "Psychic", "Light"), (150, 110, 180), (80, 140, 90)),
    "Alola": (("Water", "Flying", "Fairy", "Grass"), (70, 170, 220), (220, 195, 130)),
    "Galar": (("Fighting", "Steel", "Rock", "Dark"), (85, 95, 120), (70, 110, 70)),
    "Paldea": (("Ground", "Electric", "Fire", "Cosmic"), (215, 130, 80), (165, 120, 75)),
}
REGION_NAMES = list(REGIONS)
REGION_CHANCE = 0.7   # chance that a wild Pokemon is one of the region's types


def region_pool(region):
    """Wild Pokemon that live in this region."""
    common = [row for row in WILD_POKEMON if row[1] != "NYSTRIA"]
    favourite = REGIONS.get(region, ((),))[0]
    chance = 1.0 if region in SECRET_AREAS else REGION_CHANCE
    if not favourite or random.random() > chance:
        return common
    local = [row for row in common
             if any(t in favourite for t in row[2].split("/"))]
    return local or common


# ==========================================
# v18.0: BONDS, TITLES AND MOVE MASTERY
# ==========================================

# A short word for each type, used in titles and Bond moves
TYPE_WORD = {
    "Fire": "Flame", "Water": "Tide", "Grass": "Leaf", "Electric": "Storm",
    "Ice": "Frost", "Rock": "Stone", "Ground": "Quake", "Ghost": "Spirit",
    "Steel": "Iron", "Psychic": "Mind", "Poison": "Venom", "Flying": "Sky",
    "Fighting": "Fist", "Fairy": "Pixie", "Light": "Light", "Dark": "Shadow",
    "Dragon": "Dragon", "Bug": "Swarm", "Cosmic": "Cosmic", "Void": "Void",
    "Glitch": "Glitch", "Normal": "Wild",
}

# Bond: each Pokemon gets bond points for winning battles.
# Every 20 points is one heart. At 5 hearts it learns its Bond move.
BOND_STEP = 20
BOND_MAX = 100
BOND_WIN = 4
BOND_MOVE_POWER = 85
BOND_LINES = {
    1: "{n} seems happy to battle with you.",
    2: "{n} looks back at you before every attack.",
    3: "{n} trusts you completely!",
    4: "{n} would never give up on you!",
    5: "{n} is your best friend!",
}
BOND_MOVES = {}
for _type, _word in TYPE_WORD.items():
    BOND_MOVES[_type] = f"{_word} Bond Strike"
    MOVE_TYPES[f"{_word} Bond Strike"] = _type

# Move mastery: using a move 20 times masters it (+10 power, gold sparkle)
MASTERY_USES = 20
MASTERY_BONUS = 10

# Titles
HUNTER_TARGET = 10   # defeat this many of a type to become its Hunter


def join_text(first, second):
    """Joins two sentences with the right full stop between them."""
    first = first.strip()
    if first and first[-1] not in ".!?":
        first += "."
    return (first + " " + second).strip()


def type_word(types):
    return TYPE_WORD.get(types.split("/")[0], "Wild")


def teach_move(creature, move, power):
    """Adds a move, replacing the weakest if it already knows four."""
    if len(creature.moves) < 4:
        creature.moves.append((move, power))
        return f"{creature.name} learned {move}!"
    weakest = min(range(len(creature.moves)), key=lambda i: creature.moves[i][1])
    old = creature.moves[weakest][0]
    creature.moves[weakest] = (move, power)
    return f"{creature.name} forgot {old} and learned {move}!"


def give_title(creature, title):
    """Gives a title once. Returns a message, or None if it already had it."""
    if title in creature.titles:
        return None
    creature.titles.append(title)
    if not creature.title:
        creature.title = title
    return f"{creature.name} earned the title {title}!"


def bond_hearts(creature):
    return min(5, creature.bond // BOND_STEP)


def add_bond(creature, amount):
    """Adds bond points. Returns any messages about new hearts."""
    before = bond_hearts(creature)
    creature.bond = min(BOND_MAX, creature.bond + amount)
    after = bond_hearts(creature)
    messages = []
    if after > before:
        messages.append(BOND_LINES[after].format(n=creature.name)
                        + f" (Bond {after}/5)")
        if after == 5:
            move = BOND_MOVES.get(creature.types.split("/")[0],
                                  "Wild Bond Strike")
            if not any(m == move for m, _p in creature.moves):
                messages.append(teach_move(creature, move, BOND_MOVE_POWER))
            title = give_title(creature, "Best Friend")
            if title:
                messages.append(title)
    return messages


def is_mastered(creature, move):
    return creature.mastery.get(move, 0) >= MASTERY_USES


def use_move(creature, move):
    """Counts one use of a move. Returns a message when it gets mastered."""
    creature.mastery[move] = creature.mastery.get(move, 0) + 1
    if creature.mastery[move] == MASTERY_USES:
        return f"{creature.name} MASTERED {move}! (+{MASTERY_BONUS} power)"
    return None


# ==========================================
# v18.0: SECRET AREAS AND LEGENDARY ENCOUNTERS
# ==========================================

SECRET_AREAS = {
    "Hidden Cave": {
        "types": ("Rock", "Ground", "Dark", "Ghost", "Bug"),
        "sky": (30, 26, 40), "ground": (75, 62, 55),
        "need": ("wins", 15), "hint": "Win 15 battles to find it",
        "legend": "Terravion", "puzzle": None,
    },
    "Abandoned Lab": {
        "types": ("Steel", "Electric", "Poison", "Psychic"),
        "sky": (38, 46, 52), "ground": (88, 98, 104),
        "need": ("caught", 25), "hint": "Catch 25 kinds of Pokemon",
        "legend": "Chronolux", "puzzle": "lab",
    },
    "Mysterious Dimension": {
        "types": ("Void", "Cosmic", "Psychic", "Dragon", "Ghost"),
        "sky": (45, 18, 75), "ground": (28, 10, 48),
        "need": ("trophies", 1), "hint": "Win the Battle Tournament",
        "legend": "Voidragon", "puzzle": "rift",
        "duo": ("Aetherion", "Varkrion"),
    },
}
for _name, _area in SECRET_AREAS.items():
    REGIONS[_name] = (_area["types"], _area["sky"], _area["ground"])

AREA_LEGEND_CHANCE = 0.05   # chance the area's legendary appears
DUO_CHANCE = 0.03           # chance of the Duo Legendary Battle

# Puzzles: (intro, riddle, answers, index of the right answer)
PUZZLES = {
    "lab": ("A sealed door blocks the lab. Its keypad shows a riddle:",
            "I have keys but open no locks. I have space but no room.",
            ["A keyboard", "A piano", "A map", "A clock"], 0),
    "rift": ("Three portals hum. A voice whispers from the dark:",
             "The more you take, the more you leave behind. What am I?",
             ["Coins", "Footsteps", "Shadows", "Memories"], 1),
}

# Special introductions for legendary Pokemon
LEGEND_INTROS = {
    "Terravion": ["The cave walls start to shake...",
                  "Rocks crash down as TERRAVION rises from the earth!"],
    "Chronolux": ["Every clock in the lab stops at once...",
                  "CHRONOLUX steps out of a frozen moment!"],
    "Voidragon": ["The stars go out one by one...",
                  "VOIDRAGON tears through the dimension!"],
    "NYSTRIA": ["The air tears open...",
                "The legendary NYSTRIA appeared!"],
}


def legend_intro(enemy):
    if enemy.name in LEGEND_INTROS:
        return LEGEND_INTROS[enemy.name]
    kind = RARE_KIND.get(enemy.name, "Legendary").upper()
    return ["The sky goes dark and the ground trembles...",
            f"The {kind} Pokemon {enemy.name.upper()} appeared!"]


def empower_partner(partner, fallen):
    """In a Duo battle, the survivor takes the fallen partner's power."""
    best_move, best_power = max(fallen.moves, key=lambda m: m[1])
    partner.types = (partner.types.split("/")[0] + "/"
                     + fallen.types.split("/")[0])
    partner.bonus += 8
    partner.max_hp += 60
    partner.hp = partner.max_hp
    weakest = min(range(len(partner.moves)), key=lambda i: partner.moves[i][1])
    partner.moves[weakest] = (best_move, best_power + 10)
    return (f"{partner.name} absorbed {fallen.name}'s power! It became "
            f"{partner.types}, fully healed and learned {best_move}!")


# ==========================================
# v18.0: TYPE MASTER CHALLENGES
# Three trainers of one type. Win for coins, a badge, a title and a
# SHINY Pokemon of that type.
# ==========================================

TYPE_CHALLENGES = {}
for _type, _word in TYPE_WORD.items():
    _pool = sorted(n for _num, n, ty in DEX_ALL
                   if _type in ty.split("/")
                   and n not in RARE_KIND and n != "NYSTRIA")
    if len(_pool) < 6:
        continue
    _rng = random.Random(_type)
    _picks = _rng.sample(_pool, min(9, len(_pool)))
    while len(_picks) < 9:
        _picks.append(_rng.choice(_pool))
    TYPE_CHALLENGES[_type] = [
        (f"{_word} Trainer", 25, _picks[0:3], 150),
        (f"{_word} Expert", 32, _picks[3:6], 250),
        (f"{_type} Master", 40, _picks[6:9], 400),
    ]


def challenge_prize(types):
    """A random non-legendary Pokemon of this type, for the reward."""
    pool = [n for _num, n, ty in DEX_ALL
            if types in ty.split("/") and n not in RARE_KIND and n != "NYSTRIA"]
    return random.choice(pool)


# ==========================================
# v18.0: BOSS REMATCHES
# ==========================================

def make_rematch_boss(name, number):
    """A boss that gets stronger every rematch."""
    _name, hp, bonus, moves = next(b for b in BOSS_DATA if b[0] == name)
    boss = Creature(name, int(hp * (1 + 0.4 * number)) + 60 * number,
                    [(m, 40 + 10 * number) for m in moves],
                    level=40 + 10 * number, bonus=bonus + 6 * number)
    boss.types = "Boss"
    return boss


# ==========================================
# SHINY POKEMON (new in v16.1)
# ==========================================

SHINY_CHANCE = 1 / 200


def shiny_colours(surface):
    """Returns a copy of a sprite with its colours swapped around."""
    result = surface.copy()
    width, height = result.get_size()
    for x in range(width):
        for y in range(height):
            r, g, b, a = result.get_at((x, y))
            if a:
                result.set_at((x, y), (b, r, g, a))
    return result


# ==========================================
# BATTLE ITEMS (new in v16.1)
# ==========================================

ITEMS = {
    # name: (what it does, amount)
    "Potion": ("heal", 60),
    "Super Potion": ("heal", 150),
    "Revive": ("revive", 50),   # revives with 50% HP
}


# ==========================================
# SMARTER ENEMIES (new in v16.1)
# ==========================================

def choose_enemy_move(enemy, target, smart_chance):
    """Usually picks the move that does the most damage to the target."""
    if random.random() > smart_chance:
        return random.choice(enemy.moves)
    return max(enemy.moves,
               key=lambda m: m[1] * type_multiplier(get_move_type(m[0]),
                                                    target.types))


# ==========================================
# COINS AND SHOP
# ==========================================

START_COINS = 100

SHOP_PRICES = {
    "Poke Ball": 20,
    "Great Ball": 50,
    "Ultra Ball": 100,
    "Potion": 30,
    "Super Potion": 70,
    "Revive": 120,
}


def coin_reward(enemy):
    if enemy.types == "Boss":
        return 100
    if enemy.name == "NYSTRIA" or enemy.name in RARE_KIND:
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
NYSTRIA_CHANCE = 0.05          # 5% per battle (Dallas wants NYSTRIA easier to find)
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


def random_enemy(region="The New World"):
    enemy = pick_enemy(region)
    if enemy.types != "Boss" and random.random() < SHINY_CHANCE:
        enemy.shiny = True
    return enemy


def pick_enemy(region):
    if random.random() < NYSTRIA_CHANCE:
        return make_nystria()

    # Legendary and Mythical Pokemon: very rare
    for rare_name, chance in RARE_CHANCE.items():
        if random.random() < chance:
            return make_species(rare_name)

    if random.random() < 0.12:
        name, hp, bonus, moves = random.choice(BOSS_DATA)
        enemy = Creature(name, hp, [(m, 40) for m in moves],
                         level=40, bonus=bonus)
        enemy.types = "Boss"
        return enemy

    number, name, types = random.choice(region_pool(region))

    if name in NEW_INFO:
        return make_species(name)

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

# The Elite Cup unlocks after winning the first tournament (v16.1)
ELITE_CUP = [
    ("Elite Frost Nova", 40,
     ["Glacibear", "Icetalon", "Permafrost", "Frostfin"], 300),
    ("Elite Brutus", 45,
     ["Boulderox", "Metashard", "Ironhorn", "Seismodon"], 400),
    ("Elite Seraphine", 50,
     ["Starwhisp", "Mystibloom", "Dreamlynx", "Celestuff"], 500),
    ("Elite Drake", 55,
     ["Dracoflare", "Skyragon", "Stormwyrm", "Cloudrake"], 650),
    ("Grand Champion Nyx", 62,
     ["Talonwyrm", "Voidfang", "Shadowlisk", "Eclipsar"], 1000),
]

TOURNAMENTS = [TOURNAMENT, ELITE_CUP]
TOURNAMENT_NAMES = ["BATTLE TOURNAMENT", "ELITE CUP"]

POKEDEX_BY_NAME = {name: (number, types)
                   for number, name, types in WILD_POKEMON}


def trainer_pokemon(name, level, elite=False):
    if name in NEW_INFO:
        mon = make_species(name, level)
        if elite:
            # Elite Cup Pokemon are trained much harder
            mon.max_hp += level * 7
            mon.hp = mon.max_hp
            mon.bonus = level // 2 + 5
            mon.moves = [(m, p + 12) for m, p in mon.moves]
        return mon
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


def trainer_team(tier, round_index):
    trainer, level, names, prize = TOURNAMENTS[tier][round_index]
    return [trainer_pokemon(n, level, elite=tier > 0) for n in names]


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


# ==========================================
# EXPORT / IMPORT SAVE CODES (new in v16.1)
# A save code lets you move a save between the computer and the browser.
# ==========================================

CODE_FILE = "pokemon_save_code.txt"
CODE_PREFIX = "PNW1:"


GIFT_CHECK = 1822383   # the secret gift code is not written in the code


def is_gift_code(code):
    text = "".join(code.split()).upper()
    total = 7
    for ch in text:
        total = (total * 31 + ord(ch)) % 9999991
    return total == GIFT_CHECK


def make_save_code(text):
    import base64
    return CODE_PREFIX + base64.b64encode(text.encode()).decode()


def read_save_code(code):
    import base64
    code = "".join(code.split())   # ignore spaces and line breaks
    if not code.startswith(CODE_PREFIX):
        raise ValueError("not a save code")
    text = base64.b64decode(code[len(CODE_PREFIX):]).decode()
    json.loads(text)   # check it is a real save
    return text


def export_code(code):
    """Shows the code in the browser, or writes it to a file on a computer."""
    if WEB:
        import platform
        platform.window.prompt("Copy this save code and keep it safe:", code)
        return "Save code shown. Copy it to keep it safe!"
    with open(CODE_FILE, "w") as f:
        f.write(code)
    return f"Save code written to {CODE_FILE}."


def import_code():
    """Asks for a code in the browser, or reads it from the file on a computer."""
    if WEB:
        import platform
        return platform.window.prompt("Paste your save code:", "") or ""
    with open(CODE_FILE) as f:
        return f.read()


def creature_to_dict(c):
    return {
        "name": c.name, "max_hp": c.max_hp, "hp": c.hp,
        "moves": [list(m) for m in c.moves],
        "level": c.level, "bonus": c.bonus, "xp": c.xp,
        "types": c.types, "pokedex_number": c.pokedex_number,
        "shiny": c.shiny, "bond": c.bond, "titles": c.titles,
        "title": c.title, "mastery": c.mastery, "defeats": c.defeats
    }


def creature_from_dict(d):
    c = Creature(d["name"], d["max_hp"],
                 [tuple(m) for m in d["moves"]],
                 d.get("level", 1), d.get("bonus", 0))
    c.hp = max(0, min(c.max_hp, d.get("hp", c.max_hp)))
    c.types = d.get("types", "Unknown")
    c.pokedex_number = d.get("pokedex_number")
    c.xp = int(d.get("xp", 0))
    c.shiny = bool(d.get("shiny", False))
    c.bond = int(d.get("bond", 0))
    c.titles = list(d.get("titles", []))
    c.title = d.get("title", "")
    c.mastery = dict(d.get("mastery", {}))
    c.defeats = dict(d.get("defeats", {}))
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

SHAPES.update({n: i["shape"] for n, i in NEW_INFO.items()})

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
    if name in NEW_INFO:
        return NEW_INFO[name]["stage"]
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

    if name in NEW_INFO:
        offset = sum(map(ord, name)) % 41 - 20  # each species looks a bit different
        c1 = shade(c1, offset)
        c2 = shade(c2, -offset)
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


def make_aetherion_sprite(size):
    """Aetherion: a starry cosmic dragon with psychic rings."""
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    deep = (28, 20, 70)
    purple = (96, 58, 170)
    pink = (255, 120, 210)
    cyan = (120, 235, 255)
    white = (245, 245, 255)

    # Psychic rings and aura
    for r, col in ((46, (255, 120, 210, 80)), (40, (120, 235, 255, 90))):
        pygame.draw.circle(s, col, (50, 50), r, 3)
    pygame.draw.ellipse(s, (15, 10, 30, 130), (16, 88, 68, 10))

    # Wings made of cosmic space
    pygame.draw.polygon(s, deep, [(36, 46), (4, 14), (12, 36), (2, 50), (30, 62)])
    pygame.draw.polygon(s, deep, [(64, 46), (96, 14), (88, 36), (98, 50), (70, 62)])
    pygame.draw.polygon(s, purple, [(34, 48), (10, 22), (16, 38), (8, 48), (28, 58)])
    pygame.draw.polygon(s, purple, [(66, 48), (90, 22), (84, 38), (92, 48), (72, 58)])
    for a, b in (((34, 48), (10, 22)), ((66, 48), (90, 22))):
        pygame.draw.line(s, cyan, a, b, 1)

    # Serpent tail with star tip
    pygame.draw.polygon(s, deep, [(60, 74), (84, 84), (98, 76), (92, 66), (82, 74), (64, 68)])
    pygame.draw.polygon(s, pink, [(96, 72), (100, 60), (95, 68)])

    # Body and legs
    pygame.draw.ellipse(s, deep, (26, 40, 48, 42))
    pygame.draw.ellipse(s, purple, (29, 42, 42, 38))
    pygame.draw.ellipse(s, cyan, (38, 54, 22, 20))
    pygame.draw.ellipse(s, deep, (28, 74, 18, 14))
    pygame.draw.ellipse(s, deep, (54, 74, 18, 14))

    # Head with a crown of stars
    pygame.draw.polygon(s, deep, [(34, 36), (40, 10), (50, 4), (60, 10), (66, 36)])
    pygame.draw.ellipse(s, deep, (32, 12, 36, 30))
    pygame.draw.ellipse(s, purple, (34, 14, 32, 26))
    pygame.draw.polygon(s, pink, [(50, 0), (53, 6), (59, 6), (54, 10), (56, 16), (50, 12), (44, 16), (46, 10), (41, 6), (47, 6)])
    pygame.draw.circle(s, pink, (42, 26), 4)
    pygame.draw.circle(s, pink, (58, 26), 4)
    pygame.draw.circle(s, white, (43, 25), 1)
    pygame.draw.circle(s, white, (59, 25), 1)

    # Star specks
    for x, y in ((10, 70), (88, 30), (22, 20), (80, 84), (50, 96), (14, 56)):
        pygame.draw.circle(s, white, (x, y), 1)
    return pygame.transform.smoothscale(s, (size, size))


def make_varkrion_sprite(size):
    """Varkrion: an armoured shadow-steel beast with red eyes."""
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    black = (22, 20, 30)
    dark = (48, 44, 62)
    steel = (150, 160, 180)
    light_steel = (210, 220, 235)
    red = (255, 60, 60)
    purple = (110, 40, 150)

    pygame.draw.ellipse(s, (15, 10, 20, 130), (14, 88, 72, 10))

    # Spiked back plates
    for x in (30, 44, 58, 72):
        pygame.draw.polygon(s, steel, [(x - 6, 36), (x, 16), (x + 6, 36)])
        pygame.draw.polygon(s, black, [(x - 6, 36), (x, 16), (x + 6, 36)], 1)

    # Legs with claws
    for x in (26, 62):
        pygame.draw.polygon(s, dark, [(x, 66), (x + 16, 66), (x + 16, 90), (x, 90)])
        for dx in (0, 6, 12):
            pygame.draw.polygon(s, steel, [(x + dx, 90), (x + dx + 3, 90), (x + dx + 1, 96)])

    # Armoured body
    pygame.draw.polygon(s, black, [(22, 40), (30, 30), (72, 30), (80, 40), (78, 72), (24, 72)])
    pygame.draw.polygon(s, dark, [(26, 42), (32, 34), (70, 34), (76, 42), (74, 68), (28, 68)])
    for y in (46, 56):
        pygame.draw.line(s, steel, (30, y), (72, y), 2)
    pygame.draw.polygon(s, purple, [(46, 48), (54, 48), (50, 64)])

    # Arms with claws
    pygame.draw.polygon(s, dark, [(20, 44), (8, 58), (14, 64), (26, 52)])
    pygame.draw.polygon(s, dark, [(80, 44), (92, 58), (86, 64), (74, 52)])
    for x, y in ((8, 58), (92, 58)):
        pygame.draw.polygon(s, light_steel, [(x - 2, y), (x, y + 8), (x + 2, y)])

    # Armoured head with horns
    pygame.draw.polygon(s, black, [(28, 26), (22, 4), (40, 18)])
    pygame.draw.polygon(s, black, [(72, 26), (78, 4), (60, 18)])
    pygame.draw.polygon(s, black, [(30, 30), (30, 14), (50, 6), (70, 14), (70, 30)])
    pygame.draw.polygon(s, steel, [(34, 22), (50, 16), (66, 22), (62, 26), (38, 26)])
    pygame.draw.polygon(s, red, [(38, 20), (46, 22), (42, 24)])
    pygame.draw.polygon(s, red, [(62, 20), (54, 22), (58, 24)])
    return pygame.transform.smoothscale(s, (size, size))


def make_nyxtera_sprite(size):
    """Eclipsar: a void dragon with horns, wide wings and star markings."""
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    night = (20, 20, 45)
    body = (55, 60, 110)
    star = (140, 230, 255)
    white = (235, 250, 255)

    pygame.draw.ellipse(s, (10, 10, 25, 130), (14, 88, 72, 10))

    # Wide wings with star specks
    pygame.draw.polygon(s, night, [(38, 44), (2, 8), (6, 34), (0, 56), (32, 64)])
    pygame.draw.polygon(s, night, [(62, 44), (98, 8), (94, 34), (100, 56), (68, 64)])
    pygame.draw.polygon(s, body, [(36, 46), (8, 16), (11, 36), (6, 52), (30, 60)])
    pygame.draw.polygon(s, body, [(64, 46), (92, 16), (89, 36), (94, 52), (70, 60)])
    for x, y in ((14, 30), (22, 44), (12, 48), (86, 30), (78, 44), (88, 48)):
        pygame.draw.circle(s, star, (x, y), 2)

    # Tail curling to a star
    pygame.draw.polygon(s, night, [(58, 76), (80, 88), (96, 80), (90, 72), (80, 80), (62, 70)])
    pygame.draw.polygon(s, star, [(94, 70), (98, 76), (94, 82), (90, 76)])

    # Body and legs
    pygame.draw.ellipse(s, night, (27, 40, 46, 42))
    pygame.draw.ellipse(s, body, (30, 42, 40, 38))
    for x, y in ((42, 54), (54, 58), (47, 66)):
        pygame.draw.rect(s, star, (x, y, 4, 4))
    pygame.draw.ellipse(s, night, (28, 74, 18, 14))
    pygame.draw.ellipse(s, night, (54, 74, 18, 14))

    # Head with two swept-back horns
    pygame.draw.polygon(s, night, [(36, 18), (26, 0), (44, 12)])
    pygame.draw.polygon(s, night, [(64, 18), (74, 0), (56, 12)])
    pygame.draw.ellipse(s, night, (32, 10, 36, 32))
    pygame.draw.ellipse(s, body, (35, 12, 30, 27))
    pygame.draw.rect(s, star, (40, 22, 6, 5))
    pygame.draw.rect(s, star, (54, 22, 6, 5))
    pygame.draw.circle(s, white, (42, 23), 1)
    pygame.draw.circle(s, white, (56, 23), 1)
    return pygame.transform.smoothscale(s, (size, size))


# Sprites cut from the Omni-Dex screenshot (in the sprites/ folder).
# Each Pokemon name maps to one picture file.
SPRITE_FILES = {
    "Embercub": "fire1", "Blazepaw": "fire2", "Pyroclaw": "fire3",
    "Frostbit": "ice1", "Glacieron": "ice2", "Cryowraith": "ice3",
    "Leaflet": "flora1", "Thornox": "flora2", "Floragon": "flora3",
    "Mechling": "mechA1", "Ironclast": "mechA2", "Titanforge": "mechA3",
    "Rockruffle": "mechB1", "Cragoyle": "mechB2", "Terradon": "mechB3",
    "Starlingo": "celestial1", "Galaxion": "celestial2", "Lumidrake": "celestial3",
    "Shadelet": "null1", "Hauntalon": "null2", "Dreadgeist": "null3",
    # Original pixel creature, drawn for the team (not a copy of any official design)
    "Lucario": "brawler",
    "Aura Brawler": "aurabrawler",
    "Aetherion": "aetherion",
    "Varkrion": "varkrion",
    "Luxray": "spark",
    "Suicune": "tidefin", "Gyarados": "stormfin", "Morpeko": "pouchbit",
    "Dialga": "gearwyrm", "Good MissingNo": "glitchbit", "Evil MissingNo": "voidbit",
}
_picture_cache = {}


def load_picture(name, size):
    """Loads a sprite file, scaled to fit the size. Returns None if it can't."""
    key = (name, size)
    if key not in _picture_cache:
        try:
            image = pygame.image.load(
                os.path.join("sprites", SPRITE_FILES[name] + ".png")
            ).convert_alpha()
            w, h = image.get_size()
            factor = size / max(w, h)
            image = pygame.transform.scale(
                image, (max(1, int(w * factor)), max(1, int(h * factor))))
        except Exception:
            image = None
        _picture_cache[key] = image
    return _picture_cache[key]


def make_sprite(name, types="Unknown", size=160):
    if name in SPRITE_FILES:
        picture = load_picture(name, size)
        if picture is not None:
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            surface.blit(picture, ((size - picture.get_width()) // 2,
                                   size - picture.get_height()))
            return surface

    if name == "Flame":
        return make_flame(size)

    if name == "Eclipsar":
        return make_nyxtera_sprite(size)

    if name == "Aetherion":
        return make_aetherion_sprite(size)

    if name == "Varkrion":
        return make_varkrion_sprite(size)

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
def get_sprite(name, types="Unknown", size=160, shiny=False):
    # Each sprite is drawn once, then reused every frame
    if shiny:
        return shiny_colours(get_sprite(name, types, size))
    return make_sprite(name, types, size)


def draw_heart(surface, x, y, filled):
    """A small heart for the bond meter."""
    colour = (235, 70, 110) if filled else (70, 70, 95)
    pygame.draw.circle(surface, colour, (x - 3, y), 4)
    pygame.draw.circle(surface, colour, (x + 3, y), 4)
    pygame.draw.polygon(surface, colour, [(x - 7, y + 1), (x + 7, y + 1), (x, y + 9)])


def draw_star(surface, x, y, r=9, colour=(255, 215, 60)):
    """A small five-pointed star, used to mark shiny Pokemon."""
    points = []
    for i in range(10):
        radius = r if i % 2 == 0 else r * 0.45
        angle = -math.pi / 2 + i * math.pi / 5
        points.append((x + radius * math.cos(angle), y + radius * math.sin(angle)))
    pygame.draw.polygon(surface, colour, points)


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

        self.message = "Welcome to Pokemon: The New World v18.2!"

        self.balls = {
            "Poke Ball": 10,
            "Great Ball": 5,
            "Ultra Ball": 2
        }

        self.avatar_turns = 0
        self.avatar_used = False

        self.coins = START_COINS
        self.seen = set()
        self.caught = set()
        self.dex_page = 0
        self.dex_selected = None
        self.trophies = 0
        self.elite_trophies = 0
        self.tournament = None

        # New in v16.1
        self.region = "The New World"
        self.items = {name: 0 for name in ITEMS}
        self.items["Potion"] = 3
        self.shiny_caught = set()
        self.events = set()

        # New in v18.0
        self.wins = 0
        self.bosses_beaten = {}     # boss name -> times beaten
        self.rematch_wins = {}      # boss name -> rematches won
        self.master_badges = set()
        self.puzzles_solved = set()
        self.rematch = None         # boss name during a rematch
        self.duo_partner = None     # second legendary in a Duo battle
        self.intro_lines = []
        self.puzzle = None

        self.buttons = []
        self.popup = ""
        self.popup_colour = WHITE
        self.flash = 0
        self.mastery_flash = 0

        self.animation = None
        self.animation_start = 0
        self.pending_enemy_turn = False

        self.pc_page = 0
        self.chart_return = "menu"
        self.code_text = ""

        if storage_read():
            self.message = "Save file found! Press LOAD to continue."

    # ======================================
    # SAVE / LOAD
    # ======================================

    def save_text(self):
        data = {
            "version": 1,
            "team": [creature_to_dict(c) for c in self.team],
            "pc": [creature_to_dict(c) for c in self.pc],
            "active": self.active,
            "balls": self.balls,
            "coins": self.coins,
            "trophies": self.trophies,
            "pokedex": {"seen": sorted(self.seen),
                        "caught": sorted(self.caught),
                        "shiny": sorted(self.shiny_caught)},
            "elite_trophies": self.elite_trophies,
            "region": self.region,
            "items": self.items,
            "events": sorted(self.events),
            "wins": self.wins,
            "bosses_beaten": self.bosses_beaten,
            "rematch_wins": self.rematch_wins,
            "type_badges": sorted(self.master_badges),
            "puzzles": sorted(self.puzzles_solved),
        }
        return json.dumps(data)

    def save_game(self):
        if self.tournament:
            self.message = "Finish the tournament before saving!"
            return

        if self.enemy:
            self.message = "Finish or run from your battle before saving!"
            return

        try:
            storage_write(self.save_text())
            self.message = "Game saved!"
        except Exception:
            self.message = "Could not save the game."

    def load_game(self):
        text = storage_read()

        if not text:
            self.message = "No save file found."
            return

        if self.apply_save(text):
            self.message = "Game loaded!"

    def apply_save(self, text):
        """Loads a save from its text. Returns True if it worked."""
        try:
            data = json.loads(text)
            team = [creature_from_dict(d) for d in data["team"]]
            pc = [creature_from_dict(d) for d in data.get("pc", [])]
            if not team:
                raise ValueError("empty team")
        except Exception:
            self.message = "The save file is damaged and could not be loaded."
            return False

        self.team = team
        self.pc = pc
        self.active = min(max(0, data.get("active", 0)), len(team) - 1)
        for name in self.balls:
            self.balls[name] = int(data.get("balls", {}).get(name, 0))
        self.coins = int(data.get("coins", START_COINS))
        self.trophies = int(data.get("trophies", 0))
        dex = data.get("pokedex", {})
        self.seen = _int_set(dex.get("seen", []))
        self.caught = _int_set(dex.get("caught", []))
        self.shiny_caught = _int_set(dex.get("shiny", []))
        self.elite_trophies = int(data.get("elite_trophies", 0))
        self.events = set(data.get("events", []))
        self.wins = int(data.get("wins", 0))
        self.bosses_beaten = dict(data.get("bosses_beaten", {}))
        self.rematch_wins = dict(data.get("rematch_wins", {}))
        self.master_badges = set(data.get("type_badges", []))
        self.puzzles_solved = set(data.get("puzzles", []))
        self.rematch = None
        self.duo_partner = None
        region = data.get("region", "The New World")
        self.region = region if region in REGIONS else "The New World"
        if "items" in data:   # saves from before v16.1 keep the free Potions
            for name in self.items:
                self.items[name] = int(data["items"].get(name, 0))
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
        return True

    # ======================================
    # EXPORT / IMPORT SAVE CODE (v16.1)
    # ======================================

    def export_save(self):
        if self.tournament or self.enemy:
            self.message = "Finish your battle before exporting!"
            return
        try:
            self.message = export_code(make_save_code(self.save_text()))
        except Exception:
            self.message = "Could not export the save code."

    def import_save(self):
        if self.tournament or self.enemy:
            self.message = "Finish your battle before importing!"
            return
        try:
            code = import_code()
        except Exception:
            self.message = (f"No save code found. Put it in {CODE_FILE}"
                            if not WEB else "Could not read the save code.")
            return
        if not code.strip():
            self.message = "Import cancelled."
            return
        if is_gift_code(code):
            self.claim_gift()
            return
        try:
            text = read_save_code(code)
        except Exception:
            self.message = "That is not a valid save code."
            return
        if self.apply_save(text):
            storage_write(text)
            self.message = "Save code imported and saved!"

    def enter_event_code(self):
        if not self.code_text:
            self.message = "Type a code first!"
            return
        if is_gift_code(self.code_text):
            self.claim_gift()
            self.mode = "menu"
        else:
            self.message = "That code doesn't work. Check the spelling!"
        self.code_text = ""

    def claim_gift(self):
        """Gives the event-only Aura Brawler, once per save."""
        if "aura_brawler" in self.events:
            self.message = "You already claimed Aura Brawler!"
            return
        gift = make_species("Aura Brawler", 30)
        self.events.add("aura_brawler")
        self.seen.add(346)
        self.caught.add(346)
        if len(self.team) < PARTY_LIMIT:
            self.team.append(gift)
            place = "your team"
        else:
            self.pc.append(gift)
            place = "your PC"
        storage_write(self.save_text())
        self.message = f"EVENT! Aura Brawler joined {place}! Game saved."

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

    def type_badges(self, types, x, y):
        """Draws each type as a coloured label. Returns the end x."""
        for t in types.split("/"):
            colour = TYPE_COLOURS.get(t, (120, 120, 140))
            image = SMALL.render(t.upper(), True, WHITE)
            w = image.get_width() + 16
            pygame.draw.rect(screen, shade(colour, -70), (x, y, w, 22),
                             border_radius=8)
            pygame.draw.rect(screen, colour, (x, y, w, 22), 2, border_radius=8)
            screen.blit(image, (x + 8, y + 2))
            x += w + 6
        return x

    def button(self, label, rect, action, colour=BLUE):
        r = pygame.Rect(rect)
        pygame.draw.rect(screen, colour, r, border_radius=9)
        pygame.draw.rect(screen, (150, 185, 235), r, 2, border_radius=9)

        image = SMALL.render(label, True, WHITE)
        screen.blit(image, image.get_rect(center=r.center))
        self.buttons.append((r, action))

    def background(self):
        # Each region has its own sky and ground colours
        _types, sky, ground = REGIONS[self.region]
        screen.fill((20, 30, 60))
        pygame.draw.rect(screen, sky, (0, 0, 1000, 450))
        pygame.draw.rect(screen, ground, (0, 450, 1000, 250))

        # Background hills
        pygame.draw.ellipse(screen, shade(sky, 10), (-100, 350, 500, 160))
        pygame.draw.ellipse(screen, shade(ground, -10), (400, 350, 600, 160))

        # Sun
        pygame.draw.circle(screen, (255, 210, 100), (850, 90), 42)
        pygame.draw.circle(screen, (255, 235, 150), (850, 90), 30)

        # Grass
        for x in range(0, 1000, 35):
            pygame.draw.line(screen, shade(ground, 25),
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
        self.centred("VERSION 18.2 - 546 POKEMON", 150)
        self.centred(self.message, 205, SMALL)

        # Coins and trophies
        self.panel((20, 20, 300, 70))
        self.text(f"Coins: {self.coins}    Badges: {len(self.master_badges)}",
                  38, 30, SMALL, GOLD)
        self.text(f"Trophies: {self.trophies}   Elite: {self.elite_trophies}",
                  38, 55, SMALL, GOLD)

        # Current region
        self.panel((750, 20, 230, 70))
        self.text("Region:", 768, 30, SMALL, GOLD)
        self.text(self.region, 768, 55, SMALL)

        # Show Flame on the main menu
        screen.blit(get_sprite("Flame", "Fire", 170), (415, 225))

        cols = (200, 350, 500, 650)
        self.button("CONTINUE" if self.enemy else "BATTLE",
                    (200, 400, 140, 50), "battle")
        self.button("TOURNAMENT", (350, 400, 140, 50),
                    "tournament", (120, 75, 160))
        self.button("ELITE CUP", (500, 400, 140, 50), "elite",
                    (150, 60, 120) if self.trophies else (70, 65, 85))
        self.button("CHALLENGES", (650, 400, 140, 50), "challenges",
                    (170, 90, 40))

        row = [("TEAM", "team", BLUE), ("POKE BALLS", "balls", BLUE),
               ("HEAL", "heal", (190, 70, 110)), ("FLY", "fly", (50, 130, 160))]
        for x, (name, action, colour) in zip(cols, row):
            self.button(name, (x, 458, 140, 44), action, colour)

        row = [("POKEMON PC", "pc", BLUE), ("SHOP", "shop", (170, 120, 30)),
               ("POKEDEX", "pokedex", (60, 90, 150)),
               ("TYPE CHART", "typechart", (60, 90, 150))]
        for x, (name, action, colour) in zip(cols, row):
            self.button(name, (x, 510, 140, 44), action, colour)

        row = [("SAVE", "save"), ("LOAD", "load"),
               ("EXPORT CODE", "export"), ("IMPORT CODE", "import")]
        for x, (name, action) in zip(cols, row):
            self.button(name, (x, 562, 140, 44), action, (45, 115, 75))

        if WEB:
            self.button("EVENT CODE", (425, 614, 150, 40), "code",
                        (150, 60, 120))
        else:
            self.button("EVENT CODE", (340, 614, 150, 40), "code",
                        (150, 60, 120))
            self.button("QUIT", (510, 614, 150, 40), "quit", (145, 50, 60))

    def draw_code(self):
        """On-screen keyboard for event codes. Works on iPads and phones."""
        self.background()
        self.centred("ENTER EVENT CODE", 60, BIG, GOLD)

        self.panel((250, 105, 500, 70))
        shown = self.code_text + ("_" if (pygame.time.get_ticks() // 500) % 2 else " ")
        self.centred(shown, 140, BIG)

        keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for i, ch in enumerate(keys):
            col, row = i % 9, i // 9
            self.button(ch, (155 + col * 77, 200 + row * 62, 67, 52),
                        ("code_key", ch))

        self.button("DELETE", (155, 455, 200, 50), "code_del", (145, 50, 60))
        self.button("CLEAR", (400, 455, 200, 50), "code_clear", (145, 50, 60))
        self.button("ENTER", (645, 455, 200, 50), "code_enter", (45, 115, 75))

        self.centred(self.message, 550, SMALL, GOLD)
        self.button("BACK", (420, 600, 160, 45), "back")

    def draw_fly(self):
        self.background()
        self.centred("FLY TO A REGION", 40, BIG, GOLD)
        self.centred("Each region has its own common Pokemon types.", 80, SMALL)
        self.panel((60, 100, 880, 510))

        for i, name in enumerate(REGION_NAMES):
            col, row = divmod(i, 5)
            x, y = 80 + col * 430, 112 + row * 70
            favourite, sky, ground = REGIONS[name]
            colour = (45, 115, 75) if name == self.region else shade(sky, -25)
            label = name + ("  (HERE)" if name == self.region else "")
            self.button(label, (x, y, 410, 40), ("fly_to", name), colour)
            info = ", ".join(favourite) if favourite else "Every type"
            self.text(info, x + 8, y + 44, SMALL, GOLD)

        self.centred("SECRET AREAS", 478, FONT, GOLD)
        for i, name in enumerate(SECRET_AREAS):
            area = SECRET_AREAS[name]
            x, y = 80 + i * 285, 505
            if self.area_unlocked(name):
                colour = (45, 115, 75) if name == self.region else (95, 55, 135)
                self.button(name, (x, y, 270, 44), ("fly_to", name), colour)
                info = ", ".join(area["types"][:3])
            else:
                self.button("???", (x, y, 270, 44), ("locked", area["hint"]),
                            (60, 60, 75))
                info = area["hint"]
            self.text(info, x + 6, y + 50, SMALL, GOLD)

        self.centred(self.message, 625, SMALL, GOLD)
        self.button("BACK", (420, 645, 160, 42), "back")

    def draw_intro(self):
        """A dramatic introduction before a legendary battle."""
        self.background()
        shade_layer = pygame.Surface((1000, 700), pygame.SRCALPHA)
        shade_layer.fill((0, 0, 0, 150))
        screen.blit(shade_layer, (0, 0))

        pulse = (pygame.time.get_ticks() // 120) % 10
        pygame.draw.circle(screen, GOLD, (500, 300), 120 + pulse * 4, 4)

        if self.enemy:
            if self.duo_partner:
                screen.blit(get_sprite(self.enemy.name, self.enemy.types, 180,
                                       shiny=self.enemy.shiny), (260, 200))
                screen.blit(get_sprite(self.duo_partner.name,
                                       self.duo_partner.types, 180), (560, 200))
            else:
                screen.blit(get_sprite(self.enemy.name, self.enemy.types, 200,
                                       shiny=self.enemy.shiny), (400, 190))

        for i, line in enumerate(self.intro_lines):
            self.centred(line, 70 + i * 45, FONT if i else SMALL,
                         GOLD if i == 1 else WHITE)

        self.button("BATTLE!", (380, 560, 240, 60), "intro_go", (160, 50, 60))

    def draw_puzzle(self):
        self.background()
        intro, riddle, answers, _right = PUZZLES[self.puzzle]
        self.centred(self.region.upper(), 70, BIG, GOLD)
        self.panel((120, 120, 760, 160))
        self.centred(intro, 155, SMALL)
        for i, line in enumerate(wrap_text(riddle, FONT, 700)):
            self.centred(line, 200 + i * 34, FONT, GOLD)

        for i, answer in enumerate(answers):
            x = 180 + (i % 2) * 330
            y = 320 + (i // 2) * 75
            self.button(answer, (x, y, 310, 55), ("answer", i), (95, 55, 135))

        self.centred(self.message, 500, SMALL, GOLD)
        self.button("LATER", (420, 560, 160, 45), "back")

    def draw_challenges(self):
        self.background()
        self.centred("CHALLENGES", 90, BIG, GOLD)
        self.panel((220, 150, 560, 330))
        self.button("TYPE MASTERS", (300, 185, 400, 60), "typemasters",
                    (170, 90, 40))
        self.centred("Beat 3 trainers of one type for a badge, a title "
                     "and a SHINY Pokemon", 268, SMALL)
        self.button("BOSS REMATCHES", (300, 320, 400, 60), "rematches",
                    (145, 50, 60))
        self.centred("Fight bosses you have beaten. They get stronger "
                     "every time!", 403, SMALL)
        self.centred(self.message, 510, SMALL, GOLD)
        self.button("BACK", (420, 560, 160, 45), "back")

    def draw_typemasters(self):
        self.background()
        self.centred("TYPE MASTER CHALLENGES", 40, BIG, GOLD)
        self.centred(f"Badges: {len(self.master_badges)} / {len(TYPE_CHALLENGES)}",
                     82, SMALL)
        for i, types in enumerate(TYPE_CHALLENGES):
            col, row = i % 4, i // 4
            x, y = 70 + col * 220, 110 + row * 85
            colour = shade(TYPE_COLOURS.get(types, (120, 120, 140)), -55)
            self.button(types.upper(), (x, y, 200, 60),
                        ("typemaster", types), colour)
            if types in self.master_badges:
                draw_star(screen, x + 182, y + 16, 10)
        self.centred(self.message, 625, SMALL, GOLD)
        self.button("BACK", (420, 645, 160, 42), "back")

    def draw_rematches(self):
        self.background()
        self.centred("BOSS REMATCHES", 70, BIG, GOLD)
        self.panel((150, 120, 700, 360))
        for i, (name, hp, bonus, moves) in enumerate(BOSS_DATA):
            y = 150 + i * 105
            beaten = self.bosses_beaten.get(name, 0)
            won = self.rematch_wins.get(name, 0)
            self.text(name, 180, y, FONT)
            if beaten:
                self.text(f"Rematches won: {won}   Next: Rematch {won + 1} "
                          f"(Lv {50 + 10 * won})", 180, y + 32, SMALL, GOLD)
                self.button("FIGHT", (690, y + 2, 130, 50),
                            ("rematch_boss", name), (145, 50, 60))
            else:
                self.text("Beat it in a wild battle first", 180, y + 32, SMALL)
        self.centred(self.message, 510, SMALL, GOLD)
        self.button("BACK", (420, 560, 160, 45), "back")

    def draw_typechart(self):
        self.background()
        self.centred("TYPE CHART", 35, BIG, GOLD)
        self.panel((25, 65, 950, 570))
        self.text("TYPE", 50, 75, SMALL, GOLD)
        self.text("STRONG AGAINST (2x damage)", 190, 75, SMALL, GOLD)
        self.text("WEAK TO (takes 2x damage)", 590, 75, SMALL, GOLD)

        for i, attacker in enumerate(TYPE_CHART):
            y = 102 + i * 27
            self.type_badges(attacker, 45, y)
            strong = [t for t, m in TYPE_CHART[attacker].items() if m > 1]
            weak = [t for t in TYPE_CHART
                    if TYPE_CHART[t].get(attacker, 1) > 1]
            self.text(", ".join(strong) or "-", 190, y + 2, SMALL)
            self.text(", ".join(weak) or "-", 590, y + 2, SMALL)

        self.centred("Light, Cosmic, Void and Glitch take normal damage "
                     "from everything.", 616, SMALL, GOLD)
        self.button("BACK", (420, 645, 160, 42), "back")

    def draw_items(self):
        self.draw_battle()
        if not self.enemy:
            return
        self.buttons.clear()

        self.panel((250, 165, 500, 315))
        self.text("USE AN ITEM", 390, 180, BIG, GOLD)

        for i, (name, (kind, amount)) in enumerate(ITEMS.items()):
            y = 240 + i * 60
            if kind == "heal":
                info = f"+{amount} HP to {self.pokemon.name}"
            else:
                info = "Revives a fainted Pokemon"
            self.text(f"{name} x{self.items[name]}", 280, y, FONT)
            self.text(info, 280, y + 28, SMALL, GOLD)
            if self.items[name] > 0:
                self.button("USE", (620, y, 100, 40), ("use_item", name),
                            (45, 115, 75))

        self.button("BACK", (420, 435, 160, 38), "back")

    def draw_battle(self):
        self.background()

        if not self.enemy:
            self.mode = "menu"
            return

        p, e = self.pokemon, self.enemy

        self.panel((555, 35, 405, 115))
        self.text(e.name, 580, 45, BIG)
        if e.shiny:
            draw_star(screen, 940, 58)
        self.type_badges(e.types, 580, 83)
        self.text(f"Lv {e.level}", 880, 55, SMALL, GOLD)
        self.text(f"HP: {e.hp}/{e.max_hp}", 580, 108, SMALL)
        self.health_bar(580, 130, 340, e)

        self.panel((35, 350, 420, 120))
        self.text(p.name, 60, 362, BIG)
        if p.title:
            self.text(p.title, 60 + BIG.size(p.name)[0] + 12, 374, SMALL, GOLD)
        if p.shiny:
            draw_star(screen, 340, 380)
        self.type_badges(p.types, 60, 398)
        self.text(f"HP: {p.hp}/{p.max_hp}", 60, 425, SMALL)
        self.text(f"Lv {p.level}", 380, 401, SMALL, GOLD)
        self.text(f"XP {p.xp}/{xp_needed(p.level)}", 260, 425, SMALL)
        self.health_bar(60, 455, 350, p)

        screen.blit(get_sprite(e.name, e.types, shiny=e.shiny), (680, 155))
        screen.blit(get_sprite(p.name, p.types, shiny=p.shiny), (160, 190))

        if self.duo_partner:
            q = self.duo_partner
            screen.blit(get_sprite(q.name, q.types, 110), (860, 230))
            self.text(f"+ {q.name}", 860, 345, SMALL, GOLD)

        if self.mastery_flash:
            self.mastery_flash -= 1
            for i in range(6):
                angle = i * math.pi / 3 + self.mastery_flash * 0.2
                draw_star(screen, 760 + 95 * math.cos(angle),
                          235 + 95 * math.sin(angle), 11)

        if self.tournament:
            trainer = self.tournament_list()[self.tournament["round"]][0]
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
        lines = wrap_text(self.message, SMALL, 920)
        if len(lines) > 2:
            lines = lines[:2]
            lines[1] += " ..."
        for i, line in enumerate(lines):
            self.text(line, 40, 498 + i * 22, SMALL, GOLD)

        self.button("ATTACKS", (40, 550, 160, 45), "moves")
        self.button("SWITCH TEAM", (215, 550, 160, 45), "team")
        self.button("SUN AVATAR", (390, 550, 160, 45),
                    "avatar", (145, 90, 35))
        self.button("POKE BALLS", (565, 550, 150, 45), "balls")
        self.button("FORFEIT" if self.tournament else "RUN",
                    (730, 550, 100, 45), "run", (130, 55, 60))
        self.button("MENU", (845, 550, 110, 45), "menu")
        self.button("ITEMS", (40, 610, 160, 45), "items", (45, 115, 75))
        self.text(f"Region: {self.region}", 230, 622, SMALL)

    def draw_moves(self):
        self.draw_battle()
        if not self.enemy:
            return
        self.buttons.clear()

        self.panel((250, 165, 500, 315))
        self.centred("CHOOSE YOUR ATTACK", 200, BIG, GOLD)

        for i, (move, power) in enumerate(self.pokemon.moves):
            move_type = get_move_type(move)
            multiplier = type_multiplier(move_type, self.enemy.types)
            hint = {0: "  NO EFFECT", 0.25: "  x0.25", 0.5: "  x0.5",
                    2: "  x2!", 4: "  x4!!"}.get(multiplier, "")
            colour = shade(TYPE_COLOURS.get(move_type, (120, 120, 140)), -60)
            self.button(
                f"{i + 1}. {move} ({move_type}) - Power {power}{hint}",
                (270, 235 + i * 53, 460, 43),
                ("move", i), colour
            )
            if is_mastered(self.pokemon, move):
                draw_star(screen, 717, 235 + i * 53 + 21, 9)

        self.button("BACK", (420, 440, 160, 35), "back")

    def draw_team(self):
        self.background()
        self.centred("YOUR POKEMON TEAM", 25, BIG, GOLD)

        for i, p in enumerate(self.team[:12]):
            x = 25 + (i % 3) * 325
            y = 75 + (i // 3) * 145

            self.panel((x, y, 300, 130))
            screen.blit(get_sprite(p.name, p.types, 88, shiny=p.shiny),
                        (x + 8, y + 6))
            if p.shiny:
                draw_star(screen, x + 18, y + 18)

            self.text(p.name, x + 110, y + 8, SMALL)
            self.text(f"Lv {p.level}", x + 258, y + 8, SMALL, GOLD)
            if p.title:
                self.text(p.title, x + 110, y + 29, SMALL, GOLD)
            else:
                self.text("Type: " + p.types, x + 110, y + 29, SMALL)
            self.text(f"HP {p.hp}/{p.max_hp}", x + 110, y + 50, SMALL)
            for h in range(5):
                draw_heart(screen, x + 222 + h * 15, y + 58,
                           h < bond_hearts(p))
            self.health_bar(x + 110, y + 75, 160, p)
            if p.titles:
                self.button("TITLE", (x + 8, y + 98, 90, 26), ("title", i),
                            (150, 110, 30))
            upcoming = next_move_level(p.level)
            if upcoming:
                self.text(f"Move Lv{upcoming}", x + 216, y + 102, SMALL, GOLD)

            if i == self.active:
                self.text("ACTIVE", x + 110, y + 100, SMALL, GOLD)
            elif p.fainted:
                self.text("FAINTED", x + 110, y + 100, SMALL, RED)
            else:
                self.button("SELECT", (x + 110, y + 95, 100, 28),
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
        self.centred("POKE MART", 45, BIG, GOLD)
        self.panel((170, 80, 660, 500))
        self.text(f"Your coins: {self.coins}", 210, 95, FONT, GOLD)

        for i, (name, price) in enumerate(SHOP_PRICES.items()):
            y = 140 + i * 68
            have = self.balls.get(name, self.items.get(name, 0))
            self.text(name, 210, y, FONT)
            self.text(f"{price} coins  -  you have {have}", 210, y + 28, SMALL)
            self.button("BUY 1", (570, y + 4, 100, 40), ("buy", (name, 1)),
                        (45, 115, 75))
            self.button("BUY 5", (680, y + 4, 100, 40), ("buy", (name, 5)),
                        (45, 115, 75))

        self.text("Win battles and tournaments to earn coins!",
                  210, 550, SMALL)
        self.centred(self.message, 600, SMALL, GOLD)
        self.button("BACK", (420, 630, 160, 45), "back")

    def draw_tournament(self):
        self.background()
        t = self.tournament
        self.centred(self.tournament_name(), 45, BIG, GOLD)
        self.panel((150, 90, 700, 400))

        for i, (trainer, level, names, prize) in enumerate(self.tournament_list()):
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
            self.button("CLAIM REWARD" if t.get("type") else "CLAIM TROPHY",
                        (350, 550, 300, 55), "claim_trophy", (170, 120, 30))
        else:
            self.button(f"START ROUND {t['round'] + 1}", (300, 550, 250, 55),
                        "next_round", (120, 75, 160))
            self.button("TEAM", (560, 550, 140, 55), "team")
            self.button("FORFEIT", (400, 620, 200, 45),
                        "forfeit", (130, 55, 60))

    def draw_pokedex(self):
        self.background()
        self.centred("POKEDEX", 40, BIG, GOLD)
        self.centred(f"Caught {len(self.caught)}/{DEX_TOTAL}     "
                     f"Seen {len(self.seen)}/{DEX_TOTAL}", 80, SMALL, GOLD)

        per_page = 16
        pages = (DEX_TOTAL + per_page - 1) // per_page
        self.dex_page = min(self.dex_page, pages - 1)
        start = self.dex_page * per_page

        for i, (number, name, types) in enumerate(
                DEX_ALL[start:start + per_page]):
            col, row = divmod(i, 8)
            x, y = 60 + col * 470, 110 + row * 46
            if number in self.caught:
                label, colour = f"#{number:03} {name}  -  {types}", (45, 115, 75)
            elif number in self.seen:
                label, colour = f"#{number:03} {name}  -  {types}", BLUE
            else:
                label, colour = f"#{number:03} ???", (60, 60, 75)
            self.button(label, (x, y, 440, 38), ("dex", number), colour)
            if number in self.shiny_caught:
                draw_star(screen, x + 425, y + 19, 8)

        self.panel((60, 500, 880, 130))
        chosen = next((d for d in DEX_ALL if d[0] == self.dex_selected), None)
        if chosen is None:
            self.text("Click a Pokemon to read its Pokedex entry.", 90, 550, SMALL)
        else:
            number, name, types = chosen
            if number in self.seen:
                screen.blit(get_sprite(name, types, 100), (72, 512))
                self.text(f"#{number:03} {name}  ({types})", 185, 512, FONT, GOLD)
                y = 545
                for line in wrap_text(dex_entry(name, types), SMALL, 690):
                    self.text(line, 185, y, SMALL)
                    y += 22
                if name in NEW_INFO:
                    moves = ", ".join(m for m, _p, _t in NEW_INFO[name]["moves"])
                    self.text("Moves: " + moves, 185, y, SMALL, GOLD)
            else:
                self.text(f"#{number:03} ???  -  not seen yet", 185, 512, FONT)

        self.centred(f"Page {self.dex_page + 1} of {pages}", 485, SMALL)
        self.button("PREVIOUS", (60, 645, 160, 40), "dex_prev")
        self.button("TYPE CHART", (250, 645, 200, 40), "typechart",
                    (60, 90, 150))
        self.button("BACK", (480, 645, 200, 40), "back")
        self.button("NEXT", (780, 645, 160, 40), "dex_next")

    def draw_victory(self):
        self.background()
        self.centred("VICTORY!", 150, BIG, GOLD)

        beaten = self.defeated_enemy
        if beaten:
            self.centred(f"You defeated {beaten.name}!", 220)
            screen.blit(get_sprite(beaten.name, beaten.types,
                                   shiny=beaten.shiny), (420, 260))

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
        self.duo_partner = None
        self.rematch = None
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
        level_ups += self.battle_milestones(enemy)
        if self.pokemon.pokedex_number:
            # An evolved Pokemon counts as seen and caught in the Pokedex
            self.seen.add(self.pokemon.pokedex_number)
            self.caught.add(self.pokemon.pokedex_number)
        text = f"+{xp} XP"
        if coins:
            text += f", +{coins} coins"
        if level_ups:
            text += ". " + " ".join(level_ups)
        return text

    def battle_milestones(self, enemy):
        """Bond, titles and win counts after beating a Pokemon. (v18.0)"""
        p = self.pokemon
        notes = add_bond(p, BOND_WIN)

        for t in enemy.types.split("/"):
            if t == "Boss":
                continue
            p.defeats[t] = p.defeats.get(t, 0) + 1
            if p.defeats[t] == HUNTER_TARGET:
                notes.append(give_title(p, f"{TYPE_WORD.get(t, t)} Hunter"))

        if enemy.types == "Boss":
            notes.append(give_title(p, "Boss Breaker"))
            if not self.tournament:
                self.bosses_beaten[enemy.name] = (
                    self.bosses_beaten.get(enemy.name, 0) + 1)

        if p.hp < p.max_hp * 0.1:
            notes.append(give_title(p, f"{type_word(p.types)} Survivor"))

        if not self.tournament:
            self.wins += 1
        return [n for n in notes if n]

    # ======================================
    # SHOP
    # ======================================

    def buy(self, name, amount):
        cost = SHOP_PRICES[name] * amount
        if self.coins < cost:
            self.message = f"Not enough coins! You need {cost}."
            return

        self.coins -= cost
        if name in self.balls:
            self.balls[name] += amount
        else:
            self.items[name] += amount
        self.message = f"You bought {amount} {name}{'s' if amount > 1 else ''}!"

    # ======================================
    # TOURNAMENT
    # ======================================

    def tournament_list(self):
        if "rounds" in self.tournament:
            return self.tournament["rounds"]
        return TOURNAMENTS[self.tournament["tier"]]

    def tournament_name(self):
        t = self.tournament
        if t.get("type"):
            return f"{t['type'].upper()} MASTER CHALLENGE"
        return TOURNAMENT_NAMES[t["tier"]]

    def start_type_challenge(self, types):
        if self.enemy:
            self.message = "Finish your current battle first!"
            return
        for pokemon in self.team:
            pokemon.heal(pokemon.max_hp)
        self.tournament = {"round": 0, "team": [], "index": 0, "tier": 0,
                           "rounds": TYPE_CHALLENGES[types], "type": types}
        self.mode = "tournament"
        self.message = f"Beat 3 {types} trainers to earn the {types} Master badge!"

    def start_tournament(self, tier=0):
        if self.enemy:
            self.message = "Finish your current battle first!"
            return

        if tier == 1 and not self.trophies:
            self.message = "Win the Battle Tournament first to unlock the Elite Cup!"
            return

        # Everyone starts the tournament fully healed
        for pokemon in self.team:
            pokemon.heal(pokemon.max_hp)

        self.tournament = {"round": 0, "team": [], "index": 0, "tier": tier}
        self.mode = "tournament"
        if tier:
            self.message = "The Elite Cup! Beat all 5 elite trainers for an Elite trophy!"
        else:
            self.message = "Beat all 5 trainers to win a trophy!"

    def next_round(self):
        t = self.tournament
        if not t or t.get("won"):
            return

        if not self.send_out_healthy():
            self.message = "Your team needs to recover!"
            return

        if "rounds" in t:
            _trainer, level, names, _prize = t["rounds"][t["round"]]
            t["team"] = [trainer_pokemon(n, level) for n in names]
        else:
            t["team"] = trainer_team(t["tier"], t["round"])
        t["index"] = 0
        self.enemy = t["team"][0]

        self.avatar_turns = 0
        self.avatar_used = False
        self.animation = None
        self.pending_enemy_turn = False
        self.mode = "battle"

        trainer = self.tournament_list()[t["round"]][0]
        self.message = f"{trainer} sent out {self.enemy.name}!"

    def tournament_pokemon_beaten(self, enemy, reward_text):
        t = self.tournament
        trainer, level, names, prize = self.tournament_list()[t["round"]]
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

        if t["round"] >= len(self.tournament_list()):
            t["won"] = True
            if t.get("type"):
                t["final_message"] = self.type_challenge_rewards(t["type"])
            elif t["tier"]:
                self.elite_trophies += 1
                self.team_title("Elite Champion")
            else:
                self.trophies += 1
                self.team_title("Champion")
            self.message = (f"YOU BEAT {trainer.upper()}! You are the CHAMPION! "
                            f"+{prize} coins")
        else:
            # Team recovers half their HP between rounds
            for pokemon in self.team:
                pokemon.heal(pokemon.max_hp // 2)
            self.message = (f"You beat {trainer}! +{prize} coins. "
                            f"Your team recovered some HP.")

        self.mode = "tournament"

    def team_title(self, title):
        for pokemon in self.team:
            give_title(pokemon, title)

    def type_challenge_rewards(self, types):
        """Badge, titles and a SHINY Pokemon for a Type Master win."""
        first = types not in self.master_badges
        self.master_badges.add(types)
        title = f"{TYPE_WORD[types]} Champion"
        for pokemon in self.team:
            if types in pokemon.types.split("/"):
                give_title(pokemon, title)
        text = f"{types} Master badge earned! Your {types} Pokemon became {title}s."
        if first:
            name = challenge_prize(types)
            gift = trainer_pokemon(name, 30)
            gift.shiny = True
            if gift.pokedex_number:
                self.seen.add(gift.pokedex_number)
                self.caught.add(gift.pokedex_number)
                self.shiny_caught.add(gift.pokedex_number)
            if len(self.team) < PARTY_LIMIT:
                self.team.append(gift)
            else:
                self.pc.append(gift)
            text += f" A SHINY {name} joined you!"
        return text

    # ======================================
    # BOSS REMATCHES (v18.0)
    # ======================================

    def start_rematch(self, name):
        if self.enemy:
            self.message = "Finish your current battle first!"
            return
        if not self.bosses_beaten.get(name):
            self.message = f"Beat {name} in a wild battle first!"
            return
        if all(p.fainted for p in self.team):
            self.message = "Your team needs to recover!"
            return
        self.send_out_healthy()
        number = self.rematch_wins.get(name, 0) + 1
        self.enemy = make_rematch_boss(name, number)
        self.rematch = name
        self.duo_partner = None
        self.avatar_turns = 0
        self.avatar_used = False
        self.animation = None
        self.pending_enemy_turn = False
        self.mode = "battle"
        self.message = f"REMATCH {number}! {name} is stronger than ever!"

    # ======================================
    # DUO LEGENDARY BATTLES (v18.0)
    # ======================================

    def duo_continue(self, fallen, before_text):
        """The second legendary steps in and takes its partner's power."""
        partner = self.duo_partner
        self.duo_partner = None
        change = empower_partner(partner, fallen)
        self.enemy = partner
        if partner.pokedex_number:
            self.seen.add(partner.pokedex_number)
        self.avatar_turns = 0
        self.pending_enemy_turn = False
        self.animation = None
        self.mode = "battle"
        self.message = f"{before_text} {change}"

    # ======================================
    # SECRET AREAS (v18.0)
    # ======================================

    def area_unlocked(self, name):
        kind, amount = SECRET_AREAS[name]["need"]
        have = {"wins": self.wins, "caught": len(self.caught),
                "trophies": self.trophies}[kind]
        return have >= amount

    def area_encounter(self):
        """A legendary or Duo battle in a secret area, or None."""
        area = SECRET_AREAS.get(self.region)
        if not area:
            return None
        puzzle = area["puzzle"]
        if puzzle and puzzle not in self.puzzles_solved:
            return None
        if area.get("duo") and random.random() < DUO_CHANCE:
            first, second = area["duo"]
            lines = ["Two shadows circle overhead...",
                     f"{first.upper()} and {second.upper()} appear TOGETHER!",
                     "Defeat one and the other takes its power!"]
            return make_species(first), make_species(second), lines
        if random.random() < AREA_LEGEND_CHANCE:
            enemy = make_species(area["legend"])
            return enemy, None, legend_intro(enemy)
        return None

    def answer_puzzle(self, choice):
        _intro, _riddle, _answers, right = PUZZLES[self.puzzle]
        if choice == right:
            self.puzzles_solved.add(self.puzzle)
            self.puzzle = None
            self.mode = "menu"
            self.message = "The way opens! A legendary Pokemon now lives here..."
        else:
            self.message = "Nothing happens. Try again!"

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
        self.rematch = None
        self.duo_partner = None
        special = self.area_encounter()
        if special:
            self.enemy, self.duo_partner, intro = special
        else:
            self.enemy = random_enemy(self.region)
            intro = None
            if self.enemy.name == "NYSTRIA" or self.enemy.name in RARE_KIND:
                intro = legend_intro(self.enemy)
        for mon in (self.enemy, self.duo_partner):
            if mon and mon.pokedex_number:
                self.seen.add(mon.pokedex_number)

        self.avatar_turns = 0
        self.avatar_used = False
        self.animation = None
        self.pending_enemy_turn = False
        self.mode = "battle"

        if self.enemy.types == "Boss":
            self.message = f"BOSS BATTLE! {self.enemy.name} appeared!"
        elif self.enemy.name == "NYSTRIA":
            self.message = "The air tears open... the legendary NYSTRIA appeared!"
        elif self.enemy.name in RARE_KIND:
            self.message = f"A {RARE_KIND[self.enemy.name].upper()} Pokemon appeared: {self.enemy.name}!"
        else:
            self.message = f"A wild {self.enemy.name} appeared!"

        if self.enemy.shiny:
            self.message = "SHINY! " + self.message

        if self.duo_partner:
            self.message = (f"DUO BATTLE! {self.enemy.name} and "
                            f"{self.duo_partner.name} appeared!")

        if intro:
            self.intro_lines = intro
            self.mode = "intro"

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
        mastered = is_mastered(p, move)
        if mastered:
            damage += MASTERY_BONUS
            self.mastery_flash = 14
        mastery_note = use_move(p, move)

        if self.avatar_turns and p.name in SUN_TEAM:
            damage += 40

        move_type = get_move_type(move)
        multiplier = type_multiplier(move_type, e.types)
        damage = int(damage * multiplier)
        effect = effectiveness_text(multiplier)

        self.start_animation(move, True)
        e.take_damage(damage)
        self.show_hit(damage, GOLD)

        if e.fainted:
            self.pending_enemy_turn = False
            reward_text = self.reward_win(e)

            if mastery_note:
                reward_text = join_text(reward_text, mastery_note)

            if self.tournament:
                self.tournament_pokemon_beaten(e, reward_text)
                return

            if self.duo_partner:
                self.duo_continue(e, join_text(f"{e.name} fell! {reward_text}", ""))
                return

            extra = ""
            if self.rematch:
                won = self.rematch_wins.get(self.rematch, 0) + 1
                self.rematch_wins[self.rematch] = won
                bonus = 150 * won
                self.coins += bonus
                extra = f" REMATCH WON! +{bonus} bonus coins."
                self.rematch = None

            self.message = f"{e.name} was defeated! {reward_text}{extra}"
            self.defeated_enemy = e
            self.enemy = None
            self.avatar_turns = 0
            self.mode = "victory"
        else:
            self.message = (f"{effect}{p.name} used {move}! "
                            f"{damage} damage!")
            if mastered:
                self.message = "MASTERED! " + self.message
            if mastery_note:
                self.message += " " + mastery_note
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
        # Trainers almost always pick their best move, wild Pokemon often do
        smart = 0.9 if self.tournament else 0.6
        move, power = choose_enemy_move(e, p, smart)

        damage = power + random.randint(3, 10) + e.bonus
        move_type = get_move_type(move)
        multiplier = type_multiplier(move_type, p.types)
        damage = int(damage * multiplier)
        effect = effectiveness_text(multiplier)

        if self.avatar_turns:
            damage = max(1, damage - 15)
            self.avatar_turns -= 1

        hung_on = False
        if (damage >= p.hp and bond_hearts(p) >= 3
                and random.random() < 0.2):
            damage = max(0, p.hp - 1)
            hung_on = True

        self.start_animation(move, False)
        p.take_damage(damage)
        self.show_hit(damage, RED)

        self.message = (f"{effect}{e.name} used {move}! "
                        f"You lost {damage} HP!")
        if hung_on:
            self.message += f" {p.name} hung on for you!"

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

        if self.enemy.name == "NYSTRIA" or self.enemy.name in RARE_KIND:
            chance -= NYSTRIA_CATCH_PENALTY

        if random.random() < chance:
            caught = self.enemy
            if caught.pokedex_number:
                self.caught.add(caught.pokedex_number)
                if caught.shiny:
                    self.shiny_caught.add(caught.pokedex_number)
            self.enemy = None

            if len(self.team) < PARTY_LIMIT:
                self.team.append(caught)
                place = "your team"
            else:
                self.pc.append(caught)
                place = "your PC"

            shiny = "a SHINY " if caught.shiny else ""
            self.message = f"You caught {shiny}{caught.name}! Sent to {place}!"
            if self.duo_partner:
                self.duo_continue(caught, self.message)
                return
            self.mode = "menu"
            self.animation = None
            self.pending_enemy_turn = False

        else:
            self.message = "The Pokemon broke free!"
            self.mode = "battle"
            self.enemy_attack()

    # ======================================
    # BATTLE ITEMS (v16.1)
    # ======================================

    def use_item(self, name):
        if not self.enemy:
            self.message = "Items can only be used in battle!"
            return

        if self.animation:
            self.message = "Wait until the attack finishes!"
            return

        if self.items.get(name, 0) <= 0:
            self.message = f"You have no {name}s left!"
            return

        kind, amount = ITEMS[name]

        if kind == "heal":
            p = self.pokemon
            if p.fainted:
                self.message = "Use a Revive on a fainted Pokemon!"
                return
            if p.hp >= p.max_hp:
                self.message = f"{p.name} already has full HP!"
                return
            before = p.hp
            p.heal(amount)
            self.message = f"You used a {name}! {p.name} got {p.hp - before} HP back!"
        else:
            fainted = next((p for p in self.team if p.fainted), None)
            if not fainted:
                self.message = "None of your Pokemon have fainted!"
                return
            fainted.heal(fainted.max_hp * amount // 100)
            self.message = f"You used a Revive! {fainted.name} is back in the fight!"

        self.items[name] -= 1
        self.mode = "battle"
        # Using an item takes your turn
        self.pending_enemy_turn = False
        self.enemy_attack_after_item()

    def enemy_attack_after_item(self):
        note = self.message
        self.enemy_attack()
        if self.enemy and self.mode == "battle":
            self.message = note + " " + self.message

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
            elif kind == "dex":
                self.dex_selected = index
            elif kind == "code_key":
                if len(self.code_text) < 16:
                    self.code_text += index
            elif kind == "use_item":
                self.use_item(index)
            elif kind == "fly_to":
                if index in SECRET_AREAS and not self.area_unlocked(index):
                    self.message = f"Locked! {SECRET_AREAS[index]['hint']}."
                    return
                self.region = index
                self.message = f"You flew to {index}!"
                self.mode = "menu"
                area = SECRET_AREAS.get(index)
                if area and area["puzzle"] and area["puzzle"] not in self.puzzles_solved:
                    self.puzzle = area["puzzle"]
                    self.message = ""
                    self.mode = "puzzle"
            elif kind == "locked":
                self.message = f"Locked! {index}."
            elif kind == "answer":
                self.answer_puzzle(index)
            elif kind == "typemaster":
                self.start_type_challenge(index)
            elif kind == "rematch_boss":
                self.start_rematch(index)
            elif kind == "title":
                p = self.team[index]
                options = [""] + p.titles
                p.title = options[(options.index(p.title) + 1) % len(options)]
                self.message = (f"{p.name} is now {p.name} the {p.title}!"
                                if p.title else f"{p.name} has no title shown.")

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

        elif action == "code" and self.mode == "menu":
            if self.enemy:
                self.message = "Finish or run from your battle first!"
                return
            self.code_text = ""
            self.message = "Type the code, then press ENTER."
            self.mode = "code"

        elif action == "code_del":
            self.code_text = self.code_text[:-1]

        elif action == "code_clear":
            self.code_text = ""

        elif action == "code_enter":
            self.enter_event_code()

        elif action == "challenges" and self.mode == "menu":
            if self.enemy:
                self.message = "Finish or run from your battle first!"
                return
            self.message = ""
            self.mode = "challenges"

        elif action == "typemasters" and self.mode == "challenges":
            self.message = "Pick a type. A gold star means you have its badge."
            self.mode = "typemasters"

        elif action == "rematches" and self.mode == "challenges":
            self.message = ""
            self.mode = "rematches"

        elif action == "intro_go" and self.mode == "intro":
            self.mode = "battle"

        elif action == "back" and self.mode in ("typemasters", "rematches"):
            self.message = ""
            self.mode = "challenges"

        elif action == "back" and self.mode in ("challenges", "puzzle"):
            if self.mode == "puzzle":
                self.message = "You can solve the puzzle later by flying back here."
            else:
                self.message = ""
            self.puzzle = None
            self.mode = "menu"

        elif action == "back" and self.mode == "code":
            self.mode = "menu"
            self.message = ""

        elif action == "back":
            if self.mode == "typechart":
                self.mode = self.chart_return
            elif self.mode in ("moves", "team", "balls", "pc", "shop", "pokedex",
                               "items", "fly"):
                self.mode = self.return_mode

        elif action == "items" and self.mode == "battle":
            if self.animation:
                self.message = "Wait until the attack finishes!"
                return
            self.return_mode = "battle"
            self.mode = "items"

        elif action == "fly" and self.mode == "menu":
            if self.enemy:
                self.message = "Finish or run from your battle before flying!"
                return
            self.return_mode = "menu"
            self.mode = "fly"

        elif action == "typechart" and self.mode in ("menu", "pokedex"):
            # BACK goes to wherever the chart was opened from
            self.chart_return = self.mode
            self.mode = "typechart"

        elif action == "elite":
            if self.mode == "menu":
                self.start_tournament(1)

        elif action == "export":
            self.export_save()

        elif action == "import":
            self.import_save()

        elif action == "pokedex":
            if self.mode == "menu":
                self.return_mode = "menu"
                self.mode = "pokedex"

        elif action == "dex_prev":
            self.dex_page = max(0, self.dex_page - 1)

        elif action == "dex_next":
            last = (DEX_TOTAL + 15) // 16 - 1
            self.dex_page = min(last, self.dex_page + 1)

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
            if self.tournament and self.tournament.get("final_message"):
                self.end_tournament(self.tournament["final_message"])
            elif self.tournament and self.tournament["tier"]:
                self.end_tournament(
                    f"Elite trophy won! You now have {self.elite_trophies}!")
            else:
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
            self.duo_partner = None
            self.rematch = None
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
        # Typing on a real keyboard also works on the event code screen
        if self.mode == "code" and key != pygame.K_ESCAPE:
            if key == pygame.K_BACKSPACE:
                self.do("code_del")
            elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.do("code_enter")
            else:
                name = pygame.key.name(key).upper()
                if len(name) == 1 and name.isalnum():
                    self.do(("code_key", name))
            return

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
            "pokedex": self.draw_pokedex,
            "tournament": self.draw_tournament,
            "defeat": self.draw_defeat,
            "items": self.draw_items,
            "fly": self.draw_fly,
            "typechart": self.draw_typechart,
            "code": self.draw_code,
            "intro": self.draw_intro,
            "puzzle": self.draw_puzzle,
            "challenges": self.draw_challenges,
            "typemasters": self.draw_typemasters,
            "rematches": self.draw_rematches
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