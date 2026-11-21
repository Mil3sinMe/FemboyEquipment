"""Advancements for FemboyEquipment (usage: python3 advancements.py <repo root>).

Run after content.py / blahaj.py / phase3.py (merges into en_us.json).
"""
import json
import os
import random
import sys

from PIL import Image

ROOT = sys.argv[1]
RES = os.path.join(ROOT, "src/main/resources")
ASSETS = os.path.join(RES, "assets/femboyequipment")
DATA = os.path.join(RES, "data/femboyequipment")
NS = "femboyequipment"
ADV = f"{DATA}/advancement"
LANG = {}


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent="\t", ensure_ascii=False)
        f.write("\n")


def i(name):
    return name if ":" in name else f"{NS}:{name}"


# ------------------------------------------------------------ criteria helpers
def has(*items):
    """Have all of these items in your inventory."""
    return {"trigger": "minecraft:inventory_changed",
            "conditions": {"items": [{"items": i(x)} for x in items]}}


def wearing(head=None, chest=None, legs=None, feet=None):
    eq = {k: {"items": i(v)} for k, v in (("head", head), ("chest", chest), ("legs", legs), ("feet", feet)) if v}
    return {"trigger": "minecraft:tick", "conditions": {"player": [{
        "condition": "minecraft:entity_properties", "entity": "this", "predicate": {"equipment": eq}}]}}


def adv(path, title, desc, icon, criteria, parent=None, frame="task", background=None, hidden=False,
        xp=0, toast=True, chat=True, requirements=None):
    key = path.replace("/", ".")
    LANG[f"advancements.{NS}.{key}.title"] = title
    LANG[f"advancements.{NS}.{key}.description"] = desc
    display = {
        "icon": {"id": i(icon), "count": 1},
        "title": {"translate": f"advancements.{NS}.{key}.title"},
        "description": {"translate": f"advancements.{NS}.{key}.description"},
        "frame": frame,
        "show_toast": toast,
        "announce_to_chat": chat,
        "hidden": hidden,
    }
    if background:
        display["background"] = background
    obj = {}
    if parent:
        obj["parent"] = f"{NS}:{parent}"
    obj["display"] = display
    obj["criteria"] = criteria
    obj["requirements"] = requirements or [[k] for k in criteria]
    if xp:
        obj["rewards"] = {"experience": xp}
    write_json(f"{ADV}/{path}.json", obj)
    _collect(criteria)


COVERED = set()


def _collect(node):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "items" and isinstance(v, str) and not v.startswith("#"):
                COVERED.add(v)
            elif k == "items" and isinstance(v, list) and all(isinstance(x, str) for x in v):
                COVERED.update(x for x in v if not x.startswith("#"))
            else:
                _collect(v)
    elif isinstance(node, list):
        for v in node:
            _collect(v)


# ------------------------------------------------------------ backgrounds
def background(name, base, accent, seed):
    rnd = random.Random(seed)
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            c = accent if (x + y) % 8 == 0 or (x - y) % 8 == 0 else base
            f = 1 + rnd.uniform(-0.04, 0.04)
            im.putpixel((x, y), tuple(max(0, min(255, int(v * f))) for v in c) + (255,))
    path = f"{ASSETS}/textures/gui/advancements/backgrounds/{name}.png"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)
    return f"{NS}:gui/advancements/backgrounds/{name}"


PINK_BG = background("pink", (236, 150, 190), (250, 200, 225), 1)
SEA_BG = background("sea", (60, 110, 150), (90, 150, 190), 2)

# ------------------------------------------------------------ main tab
M = "main"
adv(f"{M}/root", "Femboy Equipment", "Cute equipment for cute people~", "pink_ribbon",
    {"tick": {"trigger": "minecraft:tick"}}, background=PINK_BG, toast=False, chat=False)

# ribbons & accessories
adv(f"{M}/pink_ribbon", "Tied With a Bow", "Get a Pink Ribbon", "pink_ribbon", {"got": has("pink_ribbon")}, f"{M}/root")
adv(f"{M}/hair_clip", "Clip It, Clip It Good", "Get a Hair Clip", "hair_clip", {"got": has("hair_clip")}, f"{M}/pink_ribbon")
adv(f"{M}/choker", "Choker? I Hardly Know Her", "Get a Choker", "choker", {"got": has("choker")}, f"{M}/pink_ribbon")
adv(f"{M}/ribbon_block", "Ribbon Hoarder", "Craft a Block of Ribbons", "ribbon_block", {"got": has("ribbon_block")}, f"{M}/pink_ribbon")
adv(f"{M}/programming_socks", "Hello, World!", "Get a pair of Programming Socks. Your code will compile now",
    "programming_socks", {"got": has("programming_socks")}, f"{M}/root")
adv(f"{M}/thigh_highs", "Unlimited Power", "Get the legendary Thigh Highs", "thigh_highs",
    {"got": has("thigh_highs")}, f"{M}/programming_socks", frame="challenge", xp=100)
adv(f"{M}/wear_thigh_highs", "Absolutely Broken", "Actually put the Thigh Highs on", "thigh_highs",
    {"worn": wearing(feet="thigh_highs")}, f"{M}/thigh_highs", frame="goal", xp=50)

# cat outfit
adv(f"{M}/cat_ears", "Nya~", "Get a pair of Cat Ears", "cat_ears", {"got": has("cat_ears")}, f"{M}/root")
adv(f"{M}/femboy_hoodie", "Hoodie Season", "Get a Femboy Hoodie", "femboy_hoodie", {"got": has("femboy_hoodie")}, f"{M}/cat_ears")
adv(f"{M}/pleated_skirt", "Twirl!", "Get a Pleated Skirt", "pleated_skirt", {"got": has("pleated_skirt")}, f"{M}/femboy_hoodie")
adv(f"{M}/cat_set", "Purrfect Outfit", "Wear Cat Ears, a Femboy Hoodie, a Pleated Skirt and Thigh Highs at once",
    "cat_ears", {"worn": wearing("cat_ears", "femboy_hoodie", "pleated_skirt", "thigh_highs")},
    f"{M}/pleated_skirt", frame="challenge", xp=100)

# maid outfit
adv(f"{M}/maid_headband", "At Your Service", "Get a Maid Headband", "maid_headband", {"got": has("maid_headband")}, f"{M}/root")
adv(f"{M}/maid_dress", "Little Black Dress", "Get a Maid Dress", "maid_dress", {"got": has("maid_dress")}, f"{M}/maid_headband")
adv(f"{M}/maid_apron", "Apron Strings", "Get a Maid Apron", "maid_apron", {"got": has("maid_apron")}, f"{M}/maid_dress")
adv(f"{M}/mary_janes", "Click Your Heels", "Get a pair of Mary Janes", "mary_janes", {"got": has("mary_janes")}, f"{M}/maid_apron")
adv(f"{M}/maid_set", "Welcome Home, Master~", "Wear the full maid outfit", "maid_dress",
    {"worn": wearing("maid_headband", "maid_dress", "maid_apron", "mary_janes")}, f"{M}/mary_janes", frame="goal", xp=50)

# bunny outfit
adv(f"{M}/bunny_ears", "Hop to It", "Get a pair of Bunny Ears", "bunny_ears", {"got": has("bunny_ears")}, f"{M}/root")
adv(f"{M}/bunny_hoodie", "Fluffy and Proud", "Get a Bunny Hoodie", "bunny_hoodie", {"got": has("bunny_hoodie")}, f"{M}/bunny_ears")
adv(f"{M}/fluffy_slippers", "Soft Landing", "Get a pair of Fluffy Slippers", "fluffy_slippers", {"got": has("fluffy_slippers")}, f"{M}/bunny_hoodie")
adv(f"{M}/bunny_set", "Some Bunny Loves You", "Wear the full bunny outfit", "bunny_ears",
    {"worn": wearing(head="bunny_ears", chest="bunny_hoodie", feet="fluffy_slippers")}, f"{M}/fluffy_slippers", frame="goal", xp=50)

# dyeing
DYEABLE = ["cat_ears", "femboy_hoodie", "pleated_skirt", "thigh_highs", "maid_headband", "maid_dress",
           "maid_apron", "mary_janes", "bunny_ears", "bunny_hoodie", "fluffy_slippers"]
adv(f"{M}/dye_outfit", "Taste the Rainbow", "Dye a piece of your outfit", "minecraft:pink_dye",
    {"dyed": {"trigger": "minecraft:recipe_crafted", "conditions": {
        "recipe_id": "minecraft:armor_dye", "ingredients": [{"items": [i(x) for x in DYEABLE]}]}}}, f"{M}/cat_ears")

# tools, food, blocks
adv(f"{M}/sparkly_sword", "Pretty Deadly", "Get a Sparkly Sword", "sparkly_sword", {"got": has("sparkly_sword")}, f"{M}/root")
adv(f"{M}/sparkly_pickaxe", "Sparkle Miner", "Get a Sparkly Pickaxe", "sparkly_pickaxe", {"got": has("sparkly_pickaxe")}, f"{M}/sparkly_sword")
adv(f"{M}/strawberry_milk", "Strawberry Milk Enjoyer", "Drink some Strawberry Milk", "strawberry_milk",
    {"drank": {"trigger": "minecraft:consume_item", "conditions": {"item": {"items": i("strawberry_milk")}}}}, f"{M}/root")
adv(f"{M}/pastel_bloom", "Stop and Smell the Flowers", "Pick a Pastel Bloom", "pastel_bloom", {"got": has("pastel_bloom")}, f"{M}/root")
adv(f"{M}/pastel_pink_bricks", "Pretty in Pink", "Craft some Pastel Pink Bricks", "pastel_pink_bricks",
    {"got": has("pastel_pink_bricks")}, f"{M}/pastel_bloom")

# world stuff
adv(f"{M}/cute_house", "Home Sweet Home", "Find a cute house", "pastel_pink_bricks",
    {"found": {"trigger": "minecraft:location", "conditions": {"player": [{
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"location": {"structures": i("cute_house")}}}]}}}, f"{M}/root", frame="goal")
adv(f"{M}/trade", "Cute Commerce", "Trade with a Femboy Trader", "minecraft:emerald",
    {"traded": {"trigger": "minecraft:villager_trade", "conditions": {"villager": [{
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"type": i("femboy_villager")}}]}}}, f"{M}/cute_house")
adv(f"{M}/pink_cat", "Pink Kitty", "Tame a pink cat", "minecraft:cod",
    {"tamed": {"trigger": "minecraft:tame_animal", "conditions": {"entity": [{
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"components": {"minecraft:cat/variant": i("pink")}}}]}}}, f"{M}/cute_house", frame="goal", xp=30)

# everything!
EVERYTHING = ["pink_ribbon", "hair_clip", "choker", "programming_socks", "strawberry_milk", "cat_ears", "femboy_hoodie",
              "pleated_skirt", "thigh_highs", "maid_headband", "maid_dress", "maid_apron", "mary_janes", "bunny_ears",
              "bunny_hoodie", "fluffy_slippers", "sparkly_sword", "sparkly_pickaxe", "pastel_pink_bricks",
              "ribbon_block", "pastel_bloom"]
adv(f"{M}/everything", "Fully Equipped", "Collect every Femboy Equipment item", "thigh_highs",
    {x: has(x) for x in EVERYTHING}, f"{M}/thigh_highs", frame="challenge", xp=500)

# ------------------------------------------------------------ Blåhaj tab
META = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "blahaj_meta.json")))
ALL_SHARKS = META["order"]
SHARKS = [x for x in ALL_SHARKS if META["category"][x] != "mystery"]  # the 130 hand-made ones
MYSTERY = [x for x in ALL_SHARKS if META["category"][x] == "mystery"]
CATEGORY = META["category"]
assert len(SHARKS) == 130 and len(MYSTERY) == 870
lang_all = json.load(open(f"{ASSETS}/lang/en_us.json", encoding="utf-8"))

write_json(f"{DATA}/tags/item/blahaj.json", {"values": [i(s) for s in ALL_SHARKS]})

B = "blahaj"
adv(f"{B}/root", "Blåhaj Collection", "Gotta hug 'em all!", "blahaj", {"got": has("blahaj")},
    background=SEA_BG, toast=True, chat=True)
FUN = {
    "trans_blahaj": "Trans rights are shark rights 🏳️‍⚧️",
    "pride_blahaj": "Taste the shark rainbow 🌈",
    "femboy_blahaj": "The most important shark",
    "glow_blahaj": "A night-light that hugs back",
    "golden_blahaj": "Worth its weight in gold",
    "diamond_blahaj": "Shiny AND squishy",
    "netherite_blahaj": "Survives lava. You might not",
    "goth_blahaj": "It's not a phase, mom",
    "ghost_blahaj": "Boo! (affectionate)",
    "progress_pride_blahaj": "Everyone's included 🏳️‍🌈",
    "transfem_blahaj": "Girl power, shark edition",
    "transmasc_blahaj": "He/him/shark",
    "strawberry_blahaj": "Berry cute",
    "watermelon_blahaj": "One in a melon",
    "cake_blahaj": "The cake is not a lie",
    "cotton_candy_blahaj": "Sweet and fluffy",
    "creeper_blahaj": "That's a very nice everything you have there",
    "enderman_blahaj": "Don't look it in the eyes (it's shy)",
    "axolotl_blahaj": "Two friends in one",
    "bee_blahaj": "Bzz~",
    "warden_blahaj": "Shhh… it's sleeping",
    "dragon_blahaj": "The end? Never",
    "panda_blahaj": "Black and white and hugged all over",
    "sakura_blahaj": "Cherry blossom season",
    "star_blahaj": "You're a star!",
    "sun_blahaj": "Brightens up any room (literally)",
    "galaxy_blahaj": "Out of this world",
    "void_blahaj": "Stare into the void. It hugs back",
    "fire_blahaj": "Hot shark summer",
    "emo_blahaj": "Still not a phase",
    "vaporwave_blahaj": "A E S T H E T I C",
    "christmas_blahaj": "Sharky holidays!",
    "halloween_blahaj": "Spooky scary sharkeleton",
    "valentine_blahaj": "Be my shark-entine?",
}
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blahaj_jokes import JOKES  # noqa: E402
FUN.update(JOKES)
SPECIAL = {"glow_blahaj", "golden_blahaj", "diamond_blahaj", "netherite_blahaj", "star_blahaj", "sun_blahaj",
           "dragon_blahaj", "echo_blahaj", "emerald_blahaj"}
# One branch per category so the tree isn't one giant column.
GROUPS = {}
for s in SHARKS[1:]:
    GROUPS.setdefault(CATEGORY[s], []).append(s)
for group in GROUPS.values():
    head = group[0]
    for s in group:
        name = lang_all[f"block.{NS}.{s}"]
        adv(f"{B}/{s}", name, FUN.get(s, f"Get {'an' if name[0] in 'AEIOU' else 'a'} {name}"), s, {"got": has(s)},
            f"{B}/root" if s == head else f"{B}/{head}", frame="goal" if s in SPECIAL else "task")
adv(f"{B}/shark_hat", "Shark Hat", "Wear a Blåhaj on your head", "blahaj",
    {"worn": {"trigger": "minecraft:tick", "conditions": {"player": [{
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"equipment": {"head": {"items": f"#{NS}:blahaj"}}}}]}}}, f"{B}/root")
adv(f"{B}/place_blahaj", "Shark Week", "Place a Blåhaj somewhere cozy", "blahaj",
    {"placed": {"trigger": "minecraft:placed_block", "conditions": {"location": [{
        "condition": "minecraft:match_tool", "predicate": {"items": f"#{NS}:blahaj"}}]}}}, f"{B}/root")
adv(f"{B}/classic_collection", "The Original 30", "Collect the first 30 Blåhaj", "trans_blahaj",
    {s: has(s) for s in SHARKS[:30]}, f"{B}/root", frame="challenge", xp=500)
adv(f"{B}/all_blahaj", "Gotta Hug 'Em All", f"Collect all {len(SHARKS)} hand-made Blåhaj", "femboy_blahaj",
    {s: has(s) for s in SHARKS}, f"{B}/classic_collection", frame="challenge", xp=2000)

# ---- gacha
write_json(f"{DATA}/tags/item/blahaj_mystery.json", {"values": [i(x) for x in MYSTERY]})
adv(f"{B}/capsule", "Gacha Time!", "Get a Blåhaj Capsule. Right-click it. You know you want to", "blahaj_capsule",
    {"got": has("blahaj_capsule")}, f"{B}/root")
adv(f"{B}/mystery", "Mystery Shark", "Pull one of the 870 capsule-only Blåhaj", "tie_dye_coral_blahaj",
    {"got": {"trigger": "minecraft:inventory_changed", "conditions": {"items": [{"items": f"#{NS}:blahaj_mystery"}]}}},
    f"{B}/capsule")
adv(f"{B}/cursed", "Cursed Pull", "Pull a Cursed Blåhaj. It's fine. Everything is fine", "cursed_lavender_blahaj",
    {x: has(x) for x in MYSTERY if x.startswith("cursed_")}, f"{B}/mystery",
    requirements=[[x for x in MYSTERY if x.startswith("cursed_")]])
adv(f"{B}/holographic", "Ultra Rare Pull", "Pull a Holographic Blåhaj ✨", "holographic_rose_blahaj",
    {x: has(x) for x in MYSTERY if x.startswith("holographic_")}, f"{B}/mystery",
    requirements=[[x for x in MYSTERY if x.startswith("holographic_")]], frame="goal")

# ---- new gear (main tab)
adv(f"{M}/rose_quartz", "Rose-Tinted", "Craft some Rose Quartz", "rose_quartz", {"got": has("rose_quartz")}, f"{M}/root")
adv(f"{M}/rose_quartz_set", "Pretty Tough", "Wear a full set of Rose Quartz armor", "rose_quartz_chestplate",
    {"worn": wearing("rose_quartz_helmet", "rose_quartz_chestplate", "rose_quartz_leggings", "rose_quartz_boots")},
    f"{M}/rose_quartz", frame="goal", xp=50)
for piece, title, desc in (("helmet", "Rose-Colored Glasses", "Get a Rose Quartz Helmet"),
                          ("chestplate", "Heart of Stone (Pink)", "Get a Rose Quartz Chestplate"),
                          ("leggings", "Legs for Days", "Get Rose Quartz Leggings"),
                          ("boots", "Pink Steps", "Get Rose Quartz Boots")):
    adv(f"{M}/rose_quartz_{piece}", title, desc, f"rose_quartz_{piece}", {"got": has(f"rose_quartz_{piece}")}, f"{M}/rose_quartz")
adv(f"{M}/rose_quartz_spear", "Pointy & Pink", "Get a Rose Quartz Spear", "rose_quartz_spear",
    {"got": has("rose_quartz_spear")}, f"{M}/rose_quartz")
adv(f"{M}/sparkly_toolset", "Sparkle Everything", "Have every Sparkly tool at once", "sparkly_axe",
    {x: has(x) for x in ("sparkly_sword", "sparkly_pickaxe", "sparkly_axe", "sparkly_shovel", "sparkly_hoe")},
    f"{M}/sparkly_pickaxe", frame="goal", xp=50)
adv(f"{M}/fih_slapper", "Slap Happy", "Get a Fih Slapper. Go slap something", "fih_slapper",
    {"got": has("fih_slapper")}, f"{M}/root")
adv(f"{M}/blahaj_bat", "Home Run", "Get a Blåhaj Bat. Bonk", "blahaj_bat", {"got": has("blahaj_bat")}, f"{M}/fih_slapper")
adv(f"{M}/pastel_palette", "Pastel Palette", "Have every color of pastel bricks", "pastel_lavender_bricks",
    {x: has(x) for x in ("pastel_pink_bricks", "pastel_blue_bricks", "pastel_lavender_bricks", "pastel_mint_bricks",
                         "pastel_yellow_bricks")}, f"{M}/pastel_pink_bricks", frame="goal")

# ---- fih. tab
FIH_META = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fih_meta.json")))
FIHS = FIH_META["order"]
F = "fih"
FIH_BG = background("fih", (238, 236, 230), (215, 225, 235), 3)
adv(f"{F}/root", "fih.", "fih", "silver_fih_white",
    {"got": {"trigger": "minecraft:inventory_changed", "conditions": {"items": [{"items": f"#{NS}:fih"}]}}},
    background=FIH_BG)
adv(f"{F}/original", "The Original", "Get the one true fih (Silver Fih, White Kicks)", "silver_fih_white",
    {"got": has("silver_fih_white")}, f"{F}/root", frame="goal")
adv(f"{F}/capsule", "Gacha Fih", "Get a Fih Capsule", "fih_capsule", {"got": has("fih_capsule")}, f"{F}/root")
adv(f"{F}/fih_hat", "Fih Hat", "Wear a fih on your head. fih", "koi_fih_pink",
    {"worn": {"trigger": "minecraft:tick", "conditions": {"player": [{
        "condition": "minecraft:entity_properties", "entity": "this",
        "predicate": {"equipment": {"head": {"items": f"#{NS}:fih"}}}}]}}}, f"{F}/root")


def fih_any(pred):
    names = [n for n in FIHS if pred(FIH_META["meta"][n])]
    return {n: has(n) for n in names}, [names]


for key, title, desc, icon, pred, frame in [
    ("drip", "Drip", "Get a fih wearing Gold, Diamond or Netherite Kicks", "gold_fih_diamond",
     lambda m: m["shoe"] in ("gold", "diamond", "netherite"), "goal"),
    ("glow", "Glow Fih", "Get a fih that glows in the dark", "glow_fih_glow", lambda m: "glow" in (m["fish"], m["shoe"]), "task"),
    ("pride", "Fih With Pride", "Get a Pride or Trans fih, or one in Rainbow or Trans Kicks", "trans_fih_trans",
     lambda m: m["fish"] in ("pride", "trans") or m["shoe"] in ("rainbow", "trans"), "task"),
    ("galaxy", "Fih From Space", "Get a fih in Galaxy Kicks", "shadow_fih_galaxy", lambda m: m["shoe"] == "galaxy", "task"),
    ("clown", "Finding Fih", "Get a Clownfish fih", "clown_fih_white", lambda m: m["fish"] == "clown", "task"),
    ("puffer", "Puffed Up", "Get a Pufferfish fih", "puffer_fih_yellow", lambda m: m["fish"] == "puffer", "task"),
    ("checkered", "Skater Fih", "Get a fih in Checkered Kicks", "silver_fih_checkered", lambda m: m["shoe"] == "checkered", "task"),
]:
    crit, req = fih_any(pred)
    adv(f"{F}/{key}", title, desc, icon, crit, f"{F}/original" if key == "drip" else f"{F}/capsule",
        frame=frame, requirements=req)

# ---- one advancement for EVERY plushie, laid out as grids
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adv_lines import FISH_LINES, SHOE_LINES, PATTERN_LINES, COLOR_LINES  # noqa: E402
from blahaj_proc import PATTERNS, COLORS  # noqa: E402


def display_name(n):
    return lang_all.get(f"block.{NS}.{n}") or LANG.get(f"block.{NS}.{n}") or n


# fih.: one row per fish, 25 sneakers along the row
for fish in FIH_META["fish"]:
    prev = f"{F}/root"
    for shoe in FIH_META["shoes"]:
        n = f"{fish}_fih_{shoe}"
        frame = "goal" if shoe in ("gold", "diamond", "netherite", "galaxy") else "task"
        adv(f"{F}/{n}", display_name(n), f"{FISH_LINES[fish]} {SHOE_LINES[shoe]}", n, {"got": has(n)}, prev,
            frame=frame, chat=False)
        prev = f"{F}/{n}"
adv(f"{F}/all", "Fih Collector", "Collect all 1000 fih. Seek help (fih)", "silver_fih_diamond",
    {n: has(n) for n in FIHS}, f"{F}/root", frame="challenge", xp=10000)

# Mystery Blåhaj: a tab of its own, one row per pattern, 29 colors along the row
Y = "mystery"
MYSTERY_BG = background("mystery", (70, 60, 110), (110, 95, 160), 4)
adv(f"{Y}/root", "Mystery Blåhaj", "Pull a capsule-only Blåhaj", "galaxy_plum_blahaj",
    {"got": {"trigger": "minecraft:inventory_changed", "conditions": {"items": [{"items": f"#{NS}:blahaj_mystery"}]}}},
    background=MYSTERY_BG)
for pid, _ in PATTERNS:
    prev = f"{Y}/root"
    for cid, _, _ in COLORS:
        n = f"{pid}_{cid}_blahaj"
        frame = "goal" if pid in ("holographic", "royal") else "task"
        adv(f"{Y}/{n}", display_name(n), f"{PATTERN_LINES[pid]} {COLOR_LINES[cid]}", n, {"got": has(n)}, prev,
            frame=frame, chat=False)
        prev = f"{Y}/{n}"
adv(f"{Y}/all", "Gacha Legend", "Collect all 870 Mystery Blåhaj", "holographic_rose_blahaj",
    {n: has(n) for n in MYSTERY}, f"{Y}/root", frame="challenge", xp=10000)

# ---- everything else that still has no advancement
PARENTS = [("rose_quartz", f"{M}/rose_quartz"), ("sparkly_", f"{M}/sparkly_pickaxe"), ("pastel_", f"{M}/pastel_pink_bricks"),
           ("_spawn_egg", f"{M}/cute_house"), ("capsule", f"{M}/root")]
all_ids = sorted({k.split(".", 2)[2] for k in lang_all if k.startswith((f"item.{NS}.", f"block.{NS}."))}
                 | {k.split(".", 2)[2] for k in LANG if k.startswith((f"item.{NS}.", f"block.{NS}."))})
missing = [x for x in all_ids if i(x) not in COVERED]
for x in missing:
    name = lang_all.get(f"item.{NS}.{x}") or lang_all.get(f"block.{NS}.{x}") or x
    parent = next((p for key, p in PARENTS if key in x), f"{M}/root")
    art = "an" if name[0] in "AEIOU" else "a"
    adv(f"{M}/items/{x}", name, f"Get {art} {name}", x, {"got": has(x)}, parent, chat=False)
print("extra coverage:", missing)
still = [x for x in all_ids if i(x) not in COVERED]
assert not still, still

lang_all.update(LANG)
write_json(f"{ASSETS}/lang/en_us.json", lang_all)
print("advancements:", len([k for k in LANG if k.endswith(".title")]))
