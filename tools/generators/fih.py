"""1000 fih: 40 fish x 25 sneakers. A fish standing in a pair of high-top sneakers.

Usage: python3 fih.py <repo root>   (merges into en_us.json; writes FihVariants.java and fih_meta.json)
"""
import colorsys
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
HERE = os.path.dirname(os.path.abspath(__file__))


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent="\t", ensure_ascii=False)
        f.write("\n")


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# id, display, body, back (top), belly, pattern, pattern colour
FISH = [
    ("silver", "Silver", "a9b4c0", "56657a", "e6ebf0", "scales", None),
    ("gold", "Golden", "f2c443", "b8860b", "fff1b0", "scales", None),
    ("koi", "Koi", "f7f3ee", "f7f3ee", "ffffff", "patches", "ff6a1a"),
    ("clown", "Clownfish", "ff7f1e", "e05a00", "ff9a4a", "bands", "ffffff"),
    ("salmon", "Salmon", "c7a0a8", "6c7a8a", "f0d6d6", "spots", "3a3a3a"),
    ("cod", "Cod", "b89f7a", "8a7556", "e8dcc4", "spots", "6e5a3e"),
    ("tropical", "Tropical", "ffd800", "2b6fe0", "fff3a0", "bands", "2b6fe0"),
    ("puffer", "Pufferfish", "f2d35a", "b8952a", "fff7d6", "spots", "8a6a1a"),
    ("rainbow_trout", "Rainbow Trout", "b9c4b0", "6a7a5a", "eef0e6", "stripe", "ff7fa0"),
    ("bass", "Bass", "7aa05a", "3e5a2a", "dfe8c8", "spots", "34481f"),
    ("catfish", "Catfish", "7a6e60", "4a4238", "c8bca8", "plain", None),
    ("goldfish", "Goldfish", "ff9a2e", "e0701a", "ffd08a", "scales", None),
    ("betta", "Betta", "c8143c", "6a0a5a", "ff6a8a", "scales", None),
    ("blue_tang", "Blue Tang", "2a6af0", "0a1e60", "6a9aff", "stripe", "0a1e60"),
    ("neon_tetra", "Neon Tetra", "c0c8d8", "2a3a6a", "ff3a3a", "stripe", "22e0ff"),
    ("angelfish", "Angelfish", "e0e4ea", "8a90a0", "ffffff", "bands", "1a1a1a"),
    ("carp", "Carp", "b08a4a", "6a5226", "e0c890", "scales", None),
    ("tuna", "Tuna", "8aa0b8", "1a2a5a", "e0e8f0", "plain", None),
    ("mackerel", "Mackerel", "9ab8c8", "2a5a7a", "f0f4f8", "bands", "1a3a5a"),
    ("sardine", "Sardine", "b8c8d8", "3a6a9a", "f4f8fc", "scales", None),
    ("pike", "Pike", "6a8a4a", "2e4a22", "d8e0b8", "spots", "d8e0a0"),
    ("perch", "Perch", "b8b040", "5a6a22", "f0e8b0", "bands", "3a4a1a"),
    ("guppy", "Guppy", "a0a8b8", "5a6070", "e0e4ea", "rainbow_tail", None),
    ("piranha", "Piranha", "8a8e98", "4a4e58", "e04a3a", "plain", None),
    ("anglerfish", "Anglerfish", "5a4030", "2e2018", "8a6a50", "spots", "2e2018"),
    ("lionfish", "Lionfish", "f4e0d0", "c83a2a", "ffffff", "bands", "c83a2a"),
    ("mandarin", "Mandarin", "1e7ae0", "0a3a8a", "ff8a1a", "squiggle", "ff8a1a"),
    ("discus", "Discus", "d83a3a", "3a6ae0", "ffb0a0", "squiggle", "3a6ae0"),
    ("oscar", "Oscar", "2a2a2a", "141414", "ff7a1a", "patches", "ff7a1a"),
    ("arowana", "Arowana", "c8ccd4", "7a808a", "ff5a5a", "scales", None),
    ("sturgeon", "Sturgeon", "7a8088", "3a4048", "c8ccd0", "plain", None),
    ("eel", "Eel", "3a5a3a", "1a2e1a", "a0b880", "plain", None),
    ("flounder", "Flounder", "c0a880", "7a6440", "f0e4c8", "spots", "6a5430"),
    ("snapper", "Red Snapper", "e05a4a", "a02a22", "ffc0b0", "scales", None),
    ("barracuda", "Barracuda", "b0b8c0", "4a5260", "f0f2f4", "bands", "3a404a"),
    ("trans", "Trans", "5bcefa", "5bcefa", "ffffff", "trans", None),
    ("pride", "Pride", "e40303", "e40303", "ffffff", "pride", None),
    ("ghost", "Ghost", "eef0f8", "c8ccdc", "ffffff", "plain", None),
    ("shadow", "Shadow", "2a2430", "14101a", "4a4058", "plain", None),
    ("glow", "Glow", "5af0d0", "1aa088", "c8fff0", "glow", None),
]
# id, display, canvas, sole, laces, pattern
SHOES = [
    ("white", "White", "f4f4f0", "e8e4d8", "ffffff", "plain"),
    ("black", "Black", "2a2a2a", "f0ede4", "f4f4f4", "plain"),
    ("red", "Red", "d42a2a", "f0ede4", "ffffff", "plain"),
    ("pink", "Pink", "ff9ac8", "f0ede4", "ffffff", "plain"),
    ("blue", "Blue", "3a7ae0", "f0ede4", "ffffff", "plain"),
    ("navy", "Navy", "1e2a5a", "f0ede4", "ffffff", "plain"),
    ("green", "Green", "2e8a3a", "f0ede4", "ffffff", "plain"),
    ("lime", "Lime", "8ae03a", "f0ede4", "ffffff", "plain"),
    ("yellow", "Yellow", "ffd83a", "f0ede4", "ffffff", "plain"),
    ("orange", "Orange", "ff8a1e", "f0ede4", "ffffff", "plain"),
    ("purple", "Purple", "7a3ac8", "f0ede4", "ffffff", "plain"),
    ("lavender", "Lavender", "c8a8f0", "f0ede4", "ffffff", "plain"),
    ("cyan", "Cyan", "22c8d8", "f0ede4", "ffffff", "plain"),
    ("brown", "Brown", "7a4a2a", "f0ede4", "e8d8c0", "plain"),
    ("gray", "Gray", "8a8e94", "f0ede4", "ffffff", "plain"),
    ("rainbow", "Rainbow", "ffffff", "f0ede4", "ffffff", "rainbow"),
    ("trans", "Trans", "5bcefa", "f0ede4", "ffffff", "trans"),
    ("gold", "Gold", "f2c443", "b8860b", "fff1b0", "sparkle"),
    ("diamond", "Diamond", "6ee6e0", "2aa8b0", "ffffff", "sparkle"),
    ("netherite", "Netherite", "4a4048", "2a2428", "8a7a88", "plain"),
    ("glow", "Glow", "8affd8", "1aa088", "ffffff", "glow"),
    ("camo", "Camo", "6a7a3a", "f0ede4", "ffffff", "camo"),
    ("checkered", "Checkered", "ffffff", "f0ede4", "ffffff", "checkered"),
    ("galaxy", "Galaxy", "2a1450", "f0ede4", "ffffff", "galaxy"),
    ("leopard", "Leopard", "e0b060", "f0ede4", "ffffff", "leopard"),
]
assert len(FISH) == 40 and len(SHOES) == 25

PRIDE = [(228, 3, 3), (255, 140, 0), (255, 237, 0), (0, 128, 38), (0, 77, 255), (117, 7, 135)]
TRANS = [(91, 206, 250), (245, 169, 184), (255, 255, 255), (245, 169, 184), (91, 206, 250)]
EYE = (20, 20, 24)

# ------------------------------------------------------------ texture
# Regions in model UV units (0..16 on a 32 px texture = 2 px per unit):
REG = {
    "fish_side": [0, 0, 8, 8], "fish_top": [8, 0, 16, 4], "head_side": [8, 4, 12, 8], "head_front": [12, 4, 16, 8],
    "fin": [0, 8, 4, 12], "shoe_side": [4, 8, 12, 12], "shoe_top": [12, 8, 16, 12],
    "ankle": [0, 12, 8, 16], "sole": [8, 12, 12, 16], "toe": [12, 12, 16, 16],
}


def texture(fish, shoe, name):
    fid, fdisp, body, back, belly, fpat, fpc = fish
    sid, sdisp, canvas, sole, laces, spat = shoe
    body, back, belly = hx(body), hx(back), hx(belly)
    canvas, sole, laces = hx(canvas), hx(sole), hx(laces)
    rnd = random.Random(name)
    im = Image.new("RGBA", (32, 32))

    def px(x, y, c, n=0.05):
        f = 1 + rnd.uniform(-n, n)
        im.putpixel((x, y), tuple(max(0, min(255, int(v * f))) for v in c) + (255,))

    def region(key):
        u0, v0, u1, v1 = REG[key]
        return u0 * 2, v0 * 2, (u1 - u0) * 2, (v1 - v0) * 2

    # --- fish body side (16 x 16): back on top, body, belly at the bottom, plus the fish's pattern
    x0, y0, w, h = region("fish_side")
    for y in range(h):
        for x in range(w):
            if y < 3:
                c = back
            elif y >= 12:
                c = belly
            else:
                c = body
            if fpat == "scales" and y in range(3, 12) and (x + (y % 2) * 2) % 4 == 0:
                c = mix(c, WHITE, 0.35)
            elif fpat == "spots" and 3 <= y < 12 and (x * 5 + y * 7) % 9 == 0:
                c = hx(fpc)
            elif fpat == "bands" and x % 5 in (1, 2):
                c = hx(fpc)
            elif fpat == "stripe" and y in (7, 8):
                c = hx(fpc)
            elif fpat == "patches" and ((x - 4) ** 2 + (y - 6) ** 2 < 9 or (x - 12) ** 2 + (y - 9) ** 2 < 6):
                c = hx(fpc)
            elif fpat == "squiggle" and (y + abs((x % 6) - 3)) % 4 == 0 and 3 <= y < 13:
                c = hx(fpc)
            elif fpat == "pride":
                c = PRIDE[min(5, y * 6 // h)]
            elif fpat == "trans":
                c = TRANS[min(4, y * 5 // h)]
            elif fpat == "glow" and rnd.random() < 0.08:
                c = (230, 255, 250)
            elif fpat == "rainbow_tail" and x >= 12:
                c = PRIDE[(y // 3) % 6]
            px(x0 + x, y0 + y, c)
    # --- top / bottom strip
    x0, y0, w, h = region("fish_top")
    for y in range(h):
        for x in range(w):
            c = back if fpat not in ("pride", "trans") else (PRIDE[0] if fpat == "pride" else TRANS[0])
            px(x0 + x, y0 + y, c)
    # --- head sides with the derpy eye
    x0, y0, w, h = region("head_side")
    for y in range(h):
        for x in range(w):
            c = back if y < 2 else (belly if y >= 6 else body)
            if fpat == "pride":
                c = PRIDE[min(5, y * 6 // h)]
            elif fpat == "trans":
                c = TRANS[min(4, y * 5 // h)]
            px(x0 + x, y0 + y, c)
    for (dx, dy, c) in ((3, 2, WHITE), (4, 2, WHITE), (3, 3, WHITE), (4, 3, EYE), (2, 2, WHITE), (2, 3, WHITE)):
        im.putpixel((x0 + dx, y0 + dy), c + (255,))
    # --- head front (mouth)
    x0, y0, w, h = region("head_front")
    for y in range(h):
        for x in range(w):
            c = body if y < 5 else belly
            if y == 5 and 2 <= x <= 5:
                c = mix(body, BLACK, 0.5)
            px(x0 + x, y0 + y, c)
    # --- fins / tail
    x0, y0, w, h = region("fin")
    fin = mix(back, body, 0.4) if fpat not in ("rainbow_tail",) else PRIDE[2]
    for y in range(h):
        for x in range(w):
            c = fin
            if fpat == "rainbow_tail":
                c = PRIDE[(x + y) % 6]
            elif x % 2 == 0:
                c = mix(fin, BLACK, 0.15)
            px(x0 + x, y0 + y, c)

    # --- sneakers
    def canvas_at(x, y):
        if spat == "rainbow":
            return PRIDE[(y + x // 4) % 6]
        if spat == "trans":
            return TRANS[(y // 2) % 5]
        if spat == "checkered":
            return BLACK if ((x // 2) + (y // 2)) % 2 == 0 else WHITE
        if spat == "camo":
            return [canvas, mix(canvas, BLACK, 0.3), (120, 100, 60)][(x * 3 + y * 5 + (x * y) % 3) % 3]
        if spat == "galaxy":
            return (255, 250, 220) if rnd.random() < 0.08 else mix(canvas, (90, 30, 140), (x % 5) / 10)
        if spat == "leopard":
            return (60, 40, 20) if (x * 3 + y * 7) % 8 in (0, 1) else canvas
        if spat == "sparkle" and rnd.random() < 0.1:
            return WHITE
        if spat == "glow" and rnd.random() < 0.08:
            return WHITE
        return canvas

    x0, y0, w, h = region("shoe_side")
    for y in range(h):
        for x in range(w):
            if y >= h - 2:
                c = sole  # rubber sole
            elif y == h - 3:
                c = (160, 40, 40) if spat == "plain" else mix(sole, BLACK, 0.2)  # classic red stripe
            elif x < 3:
                c = sole  # toe cap
            else:
                c = canvas_at(x, y)
            px(x0 + x, y0 + y, c, 0.03)
    x0, y0, w, h = region("shoe_top")
    for y in range(h):
        for x in range(w):
            c = laces if (y % 2 == 0 and 1 <= x <= w - 2) else canvas_at(x, y)
            px(x0 + x, y0 + y, c, 0.03)
    x0, y0, w, h = region("ankle")
    for y in range(h):
        for x in range(w):
            c = canvas_at(x, y)
            if x in (2, 13) and y % 3 == 1:
                c = (200, 200, 205)  # eyelets
            if y == 0:
                c = mix(canvas_at(x, y), WHITE, 0.4)
            if 5 <= x <= 10 and 5 <= y <= 9 and spat == "plain" and fid != "x":
                c = mix(c, WHITE, 0.6) if (x + y) % 2 == 0 else c  # ankle patch
            px(x0 + x, y0 + y, c, 0.03)
    x0, y0, w, h = region("sole")
    for y in range(h):
        for x in range(w):
            px(x0 + x, y0 + y, mix(sole, BLACK, 0.15) if (x + y) % 3 == 0 else sole, 0.03)
    x0, y0, w, h = region("toe")
    for y in range(h):
        for x in range(w):
            c = sole if y >= 2 else canvas_at(x, y)
            if y in (4, 5) and 1 <= x <= 6:
                c = WHITE  # rubber toe cap
            px(x0 + x, y0 + y, c, 0.03)
    path = f"{ASSETS}/textures/block/fih/{name}.png"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)


# ------------------------------------------------------------ model
def f(**k):
    sides = {"north": "fish_side", "south": "fish_side", "east": "fish_side", "west": "fish_side",
             "up": "fish_top", "down": "fish_top"}
    sides.update(k)
    return {d: {"uv": REG[r], "texture": "#fih"} for d, r in sides.items()}


def shoe_faces():
    return f(north="toe", south="shoe_side", east="shoe_side", west="shoe_side", up="shoe_top", down="sole")


def ankle_faces():
    return f(north="ankle", south="ankle", east="ankle", west="ankle", up="shoe_top", down="sole")


ELEMENTS = [
    # sneakers (pointing north, like the fish)
    {"from": [4, 0, 3], "to": [7.5, 2.5, 11], "faces": shoe_faces()},
    {"from": [8.5, 0, 3], "to": [12, 2.5, 11], "faces": shoe_faces()},
    # high-top ankles
    {"from": [4, 2.5, 6.5], "to": [7.5, 6, 10.5], "faces": ankle_faces()},
    {"from": [8.5, 2.5, 6.5], "to": [12, 6, 10.5], "faces": ankle_faces()},
    # fish body, standing in both shoes
    {"from": [6, 5, 2], "to": [10, 10, 12.5], "faces": f()},
    # head
    {"from": [6.5, 5.5, 0], "to": [9.5, 9.5, 2], "faces": f(north="head_front", east="head_side", west="head_side")},
    # tail
    {"from": [7.5, 4.5, 12.5], "to": [8.5, 11, 15.5], "faces": f(north="fin", south="fin", east="fin", west="fin", up="fin", down="fin"),
     "rotation": {"angle": 22.5, "axis": "x", "origin": [8, 7.5, 12.5]}},
    # dorsal fin
    {"from": [7.5, 10, 5], "to": [8.5, 12, 9], "faces": f(north="fin", south="fin", east="fin", west="fin", up="fin", down="fin")},
    # side fins
    {"from": [10, 6, 3.5], "to": [10.5, 7.5, 6], "faces": f(north="fin", south="fin", east="fin", west="fin", up="fin", down="fin")},
    {"from": [5.5, 6, 3.5], "to": [6, 7.5, 6], "faces": f(north="fin", south="fin", east="fin", west="fin", up="fin", down="fin")},
]

write_json(f"{ASSETS}/models/block/fih_base.json", {
    "parent": "minecraft:block/block",
    "textures": {"particle": "#fih"},
    "elements": ELEMENTS,
    "display": {
        "gui": {"rotation": [30, 135, 0], "translation": [0, 0.5, 0], "scale": [0.85, 0.85, 0.85]},
        "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
        "fixed": {"rotation": [0, 90, 0], "translation": [0, 0, 0], "scale": [0.8, 0.8, 0.8]},
        "head": {"rotation": [0, 0, 0], "translation": [0, 14.5, 0], "scale": [1, 1, 1]},
        "thirdperson_righthand": {"rotation": [75, 45, 0], "translation": [0, 2.5, 0], "scale": [0.5, 0.5, 0.5]},
        "firstperson_righthand": {"rotation": [0, 45, 0], "translation": [0, 2, 0], "scale": [0.55, 0.55, 0.55]},
        "firstperson_lefthand": {"rotation": [0, 225, 0], "translation": [0, 2, 0], "scale": [0.55, 0.55, 0.55]},
    },
})

# ------------------------------------------------------------ variants
NAMES, LANG, META = [], {}, {}
LIGHT, RARE = {}, set()
for fish in FISH:
    for shoe in SHOES:
        name = f"{fish[0]}_fih_{shoe[0]}"
        NAMES.append(name)
        display = f"{fish[1]} Fih ({shoe[1]} Kicks)"
        if fish[0] == "silver" and shoe[0] == "white":
            display = "fih."  # the original
        LANG[f"block.{NS}.{name}"] = display
        META[name] = {"fish": fish[0], "shoe": shoe[0]}
        if fish[0] == "glow" or shoe[0] == "glow":
            LIGHT[name] = 8 if fish[0] == "glow" else 6
        if shoe[0] in ("gold", "diamond", "netherite", "galaxy") or fish[0] in ("gold", "glow"):
            RARE.add(name)
        texture(fish, shoe, name)
        write_json(f"{ASSETS}/models/block/fih/{name}.json",
                   {"parent": f"{NS}:block/fih_base", "textures": {"fih": f"{NS}:block/fih/{name}"}})
        write_json(f"{ASSETS}/blockstates/{name}.json", {"variants": {
            f"facing={d}": {"model": f"{NS}:block/fih/{name}", **({"y": r} if r else {})}
            for d, r in (("north", 0), ("east", 90), ("south", 180), ("west", 270))}})
        write_json(f"{ASSETS}/items/{name}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:block/fih/{name}"}})
        write_json(f"{DATA}/loot_table/blocks/{name}.json", {
            "type": "minecraft:block",
            "pools": [{"bonus_rolls": 0.0, "conditions": [{"condition": "minecraft:survives_explosion"}],
                       "entries": [{"type": "minecraft:item", "name": f"{NS}:{name}"}], "rolls": 1.0}],
            "random_sequence": f"{NS}:blocks/{name}",
        })
assert len(NAMES) == 1000 and len(set(NAMES)) == 1000

write_json(f"{DATA}/tags/item/fih.json", {"values": [f"{NS}:{n}" for n in NAMES]})


def java_strings(items, per_line=4):
    items = [f'"{x}"' for x in items]
    return (",\n\t\t\t").join(", ".join(items[k:k + per_line]) for k in range(0, len(items), per_line))


java = f"""package com.femboyequipment.block;

import java.util.List;
import java.util.Map;
import java.util.Set;

/** GENERATED by the fih content script: all {len(NAMES)} fih (40 fish x 25 sneakers). Do not edit by hand. */
public final class FihVariants {{
	public static final List<String> NAMES = List.of(
			{java_strings(NAMES)});

	public static final Map<String, Integer> LIGHT = Map.ofEntries(
			{(",\n\t\t\t").join(f'Map.entry("{k}", {v})' for k, v in LIGHT.items())});

	public static final Set<String> RARE = Set.of(
			{java_strings(sorted(RARE))});

	private FihVariants() {{
	}}
}}
"""
with open(os.path.join(ROOT, "src/main/java/com/femboyequipment/block/FihVariants.java"), "w") as fh:
    fh.write(java)
with open(os.path.join(HERE, "fih_meta.json"), "w") as fh:
    json.dump({"order": NAMES, "meta": META, "fish": [x[0] for x in FISH], "shoes": [x[0] for x in SHOES]}, fh)

lang_path = f"{ASSETS}/lang/en_us.json"
lang = json.load(open(lang_path, encoding="utf-8"))
lang.update(LANG)
lang["itemGroup.femboyequipment.fih"] = "fih."
write_json(lang_path, lang)
print("fih done:", len(NAMES))
