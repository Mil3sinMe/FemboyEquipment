"""Generates the 30 Blåhaj variants: textures, block/item models, blockstates, loot, recipes, lang.

Usage: python3 blahaj.py <repo root>
Keep VARIANTS in sync with Blahaj.java.
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


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent="\t", ensure_ascii=False)
        f.write("\n")


def hexc(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def dye(name):
    return f"minecraft:{name}_dye"


# name: (display name, stripe colors top->bottom, recipe extras added to a classic Blåhaj)
VARIANTS = {
    "blahaj": ("Blåhaj", ["4f7d96"], None),
    "trans_blahaj": ("Trans Blåhaj", ["5bcefa", "f5a9b8", "ffffff", "f5a9b8", "5bcefa"],
                     [dye("light_blue"), dye("pink"), dye("white")]),
    "pride_blahaj": ("Pride Blåhaj", ["e40303", "ff8c00", "ffed00", "008026", "004dff", "750787"],
                     [dye(c) for c in ("red", "orange", "yellow", "green", "blue", "purple")]),
    "bi_blahaj": ("Bi Blåhaj", ["d60270", "d60270", "9b4f96", "0038a8", "0038a8"],
                  [dye("magenta"), dye("purple"), dye("blue")]),
    "pan_blahaj": ("Pan Blåhaj", ["ff218c", "ffd800", "21b1ff"], [dye("pink"), dye("yellow"), dye("light_blue")]),
    "lesbian_blahaj": ("Lesbian Blåhaj", ["d52d00", "ff9a56", "ffffff", "d362a4", "a30262"],
                       [dye("orange"), dye("white"), dye("magenta")]),
    "gay_blahaj": ("Gay Blåhaj", ["078d70", "98e8c1", "ffffff", "7bade2", "3d1a78"],
                   [dye("cyan"), dye("white"), dye("blue")]),
    "nonbinary_blahaj": ("Nonbinary Blåhaj", ["fcf434", "ffffff", "9c59d1", "2c2c2c"],
                         [dye("yellow"), dye("white"), dye("purple"), dye("black")]),
    "ace_blahaj": ("Ace Blåhaj", ["000000", "a3a3a3", "ffffff", "800080"],
                   [dye("black"), dye("gray"), dye("white"), dye("purple")]),
    "aro_blahaj": ("Aro Blåhaj", ["3da542", "a7d379", "ffffff", "a9a9a9", "000000"],
                   [dye("green"), dye("lime"), dye("white"), dye("gray"), dye("black")]),
    "genderfluid_blahaj": ("Genderfluid Blåhaj", ["ff76a4", "ffffff", "c011d7", "000000", "2f3cbe"],
                           [dye("pink"), dye("white"), dye("purple"), dye("black"), dye("blue")]),
    "agender_blahaj": ("Agender Blåhaj", ["000000", "bcc4c7", "ffffff", "b7f684", "ffffff", "bcc4c7", "000000"],
                       [dye("black"), dye("light_gray"), dye("white"), dye("lime")]),
    "intersex_blahaj": ("Intersex Blåhaj", ["ffd800", "ffd800", "7902aa", "ffd800", "ffd800"],
                        [dye("yellow"), dye("purple")]),
    "demiboy_blahaj": ("Demiboy Blåhaj", ["7f7f7f", "c4c4c4", "9ad9eb", "ffffff", "9ad9eb", "c4c4c4", "7f7f7f"],
                       [dye("gray"), dye("light_blue"), dye("white")]),
    "demigirl_blahaj": ("Demigirl Blåhaj", ["7f7f7f", "c4c4c4", "fdadc8", "ffffff", "fdadc8", "c4c4c4", "7f7f7f"],
                        [dye("gray"), dye("pink"), dye("white")]),
    "femboy_blahaj": ("Femboy Blåhaj", ["d260a5", "e4afcd", "ffffff", "57cef8", "ffffff", "e4afcd", "d260a5"],
                      [dye("pink"), dye("white"), dye("light_blue"), dye("blue")]),
    "pink_blahaj": ("Pink Blåhaj", ["f08cbe"], [dye("pink")]),
    "red_blahaj": ("Red Blåhaj", ["c8303c"], [dye("red")]),
    "orange_blahaj": ("Orange Blåhaj", ["f08c3c"], [dye("orange")]),
    "yellow_blahaj": ("Yellow Blåhaj", ["f0d24b"], [dye("yellow")]),
    "mint_blahaj": ("Mint Blåhaj", ["7ad7a8"], [dye("lime")]),
    "purple_blahaj": ("Purple Blåhaj", ["8c5ac8"], [dye("purple")]),
    "goth_blahaj": ("Goth Blåhaj", ["2a2430"], [dye("black")]),
    "ghost_blahaj": ("Ghost Blåhaj", ["e6e6f0"], [dye("white")]),
    "chocolate_blahaj": ("Chocolate Blåhaj", ["7a4a32"], [dye("brown")]),
    "magenta_blahaj": ("Magenta Blåhaj", ["c84bc8"], [dye("magenta")]),
    "golden_blahaj": ("Golden Blåhaj", ["fadc5a", "f0c03c", "fadc5a"], ["minecraft:gold_ingot"]),
    "diamond_blahaj": ("Diamond Blåhaj", ["6ee6e0", "4bc8d2", "6ee6e0"], ["minecraft:diamond"]),
    "netherite_blahaj": ("Netherite Blåhaj", ["4a4048", "3a3238", "4a4048"], ["minecraft:netherite_scrap"]),
    "glow_blahaj": ("Glow Blåhaj", ["78f0c8"], ["minecraft:glow_ink_sac"]),
}

CATEGORY = {}
for _n in VARIANTS:
    CATEGORY[_n] = "classic"
for _n in list(VARIANTS)[1:16]:
    CATEGORY[_n] = "flags"
for _n in list(VARIANTS)[16:26]:
    CATEGORY[_n] = "colors"
for _n in list(VARIANTS)[26:]:
    CATEGORY[_n] = "fancy"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blahaj_more import MORE, LIGHT, RARE, FIRE_RESISTANT, SPARKLY  # noqa: E402
from blahaj_proc import PROC, PROC_LIGHT, PROC_RARE, PROC_SPARKLY, overlay as proc_overlay  # noqa: E402
for _n, (_disp, _cols, _extra, _cat) in MORE.items():
    assert _n not in VARIANTS, _n
    VARIANTS[_n] = (_disp, _cols, _extra)
    CATEGORY[_n] = _cat
# 870 procedural ones (no recipes: they come out of Blåhaj Capsules)
for _n, (_disp, _cols, _pat, _hex) in PROC.items():
    assert _n not in VARIANTS, _n
    VARIANTS[_n] = (_disp, _cols, [])
    CATEGORY[_n] = "mystery"
LIGHT.update(PROC_LIGHT)
RARE |= PROC_RARE
SPARKLY |= PROC_SPARKLY

# sanity: recipes must be unique
seen = {}
for name, (_, _, extra) in VARIANTS.items():
    if not extra:
        continue
    key = tuple(sorted(extra))
    assert key not in seen, (name, seen.get(key))
    seen[key] = name
assert len(VARIANTS) == 1000, len(VARIANTS)


# ----------------------------------------------------------------- textures
WHITE = (246, 242, 240)
PINK_MOUTH = (232, 130, 150)
EYE = (24, 20, 28)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def stripes(colors, n):
    """Spread the stripe colors across n pixels."""
    return [colors[min(len(colors) - 1, i * len(colors) // n)] for i in range(n)]


def texture(name, colors):
    """32x32 texture. Regions (16x16 texels = 8 model units each):
    S side [0,0], T top [16,0], B belly [0,16], F fin [16,16], E eye [24,16], X tail [16,24], M mouth [24,24]."""
    rnd = random.Random(name)
    cols = [hexc(c) for c in colors]
    im = Image.new("RGBA", (32, 32))

    def px(x, y, c, noise=0.06):
        f = 1 + rnd.uniform(-noise, noise)
        im.putpixel((x, y), shade(c, f) + (255,))

    # side: stripes on the upper 10 rows, white belly below
    rows = stripes(cols, 10)
    for y in range(16):
        for x in range(16):
            px(x, y, rows[y] if y < 10 else WHITE)
    # top: stripes running along the body
    top = stripes(cols, 16)
    for y in range(16):
        for x in range(16):
            px(16 + x, y, shade(top[x], 1.05))
    # belly
    for y in range(16):
        for x in range(16):
            px(x, 16 + y, WHITE)
    fin = shade(cols[0], 0.82)
    # fins (8x8 texels)
    for y in range(8):
        for x in range(8):
            px(16 + x, 16 + y, fin)
    # eye side (8x8): color on top, white below, little eye
    erows = stripes(cols, 5)
    for y in range(8):
        for x in range(8):
            px(24 + x, 16 + y, erows[y] if y < 5 else WHITE)
    for x, y in ((26, 18), (26, 19), (27, 18), (27, 19)):
        im.putpixel((x, y), EYE + (255,))
    im.putpixel((26, 18), (230, 230, 240, 255))  # sparkle in the eye
    # tail end (8x8)
    for y in range(8):
        for x in range(8):
            px(16 + x, 24 + y, rows[min(9, y * 10 // 8)])
    # mouth front (8x8): color on top, white chin with a pink smile and tiny teeth
    for y in range(8):
        for x in range(8):
            c = erows[y] if y < 4 else WHITE
            if y == 5 and 1 <= x <= 6:
                c = PINK_MOUTH
            px(24 + x, 24 + y, c, noise=0.03)
    for x in (25, 27, 29):
        im.putpixel((x + 1, 29), (255, 255, 255, 255))
    if name in PROC:
        proc_overlay(im, name, rnd)
    if name in SPARKLY:
        for x, y in ((19, 3), (26, 9), (4, 2), (12, 6), (29, 5), (8, 11)):
            im.putpixel((x, y), (255, 255, 240, 255))
    if name == "glow_blahaj":
        for x, y in ((18, 2), (22, 6), (28, 3), (5, 4), (11, 8)):
            im.putpixel((x, y), (230, 255, 240, 255))
    if name in ("golden_blahaj", "diamond_blahaj"):
        for x, y in ((19, 3), (26, 9), (4, 2), (12, 6)):
            im.putpixel((x, y), (255, 255, 255, 255))
    path = f"{ASSETS}/textures/block/blahaj/{name}.png"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)


# --------------------------------------------------------------- base model
S, T, B = [0, 0, 8, 8], [8, 0, 16, 8], [0, 8, 8, 16]
F, E, X, M = [8, 8, 12, 12], [12, 8, 16, 12], [8, 12, 12, 16], [12, 12, 16, 16]


def faces(north=S, south=S, east=S, west=S, up=T, down=B):
    return {k: {"uv": v, "texture": "#shark"} for k, v in
            (("north", north), ("south", south), ("east", east), ("west", west), ("up", up), ("down", down))}


ELEMENTS = [
    # body (chonky)
    {"from": [4.5, 0, 3], "to": [11.5, 6, 12], "faces": faces()},
    # head (points north)
    {"from": [5, 0.5, 0.5], "to": [11, 5.5, 3], "faces": faces(north=M, east=E, west=E)},
    # tail stem
    {"from": [6.5, 1, 12], "to": [9.5, 4.5, 14.5], "faces": faces(south=X)},
    # tail fin: a tall vertical crescent
    {"from": [7.25, -0.5, 14], "to": [8.75, 8, 16], "faces": faces(F, F, F, F, F, F),
     "rotation": {"angle": 22.5, "axis": "x", "origin": [8, 2.5, 14.5]}},
    # dorsal fin
    {"from": [7.25, 5.5, 5.5], "to": [8.75, 9.5, 8.5], "faces": faces(F, F, F, F, F, F),
     "rotation": {"angle": -22.5, "axis": "x", "origin": [8, 6, 7]}},
    # pectoral fins
    {"from": [1.5, 0, 4.5], "to": [4.5, 1, 8], "faces": faces(F, F, F, F, F, F),
     "rotation": {"angle": 22.5, "axis": "z", "origin": [4.5, 0.5, 6.5]}},
    {"from": [11.5, 0, 4.5], "to": [14.5, 1, 8], "faces": faces(F, F, F, F, F, F),
     "rotation": {"angle": -22.5, "axis": "z", "origin": [11.5, 0.5, 6.5]}},
]

write_json(f"{ASSETS}/models/block/blahaj_base.json", {
    "parent": "minecraft:block/block",
    "textures": {"particle": "#shark"},
    "elements": ELEMENTS,
    "display": {
        "gui": {"rotation": [30, 135, 0], "translation": [0, 1.5, 0], "scale": [0.85, 0.85, 0.85]},
        "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
        "fixed": {"rotation": [0, 90, 0], "translation": [0, 0, 0], "scale": [0.8, 0.8, 0.8]},
        "head": {"rotation": [0, 0, 0], "translation": [0, 14.5, 0], "scale": [1, 1, 1]},
        "thirdperson_righthand": {"rotation": [75, 45, 0], "translation": [0, 2.5, 0], "scale": [0.5, 0.5, 0.5]},
        "firstperson_righthand": {"rotation": [0, 45, 0], "translation": [0, 2, 0], "scale": [0.55, 0.55, 0.55]},
        "firstperson_lefthand": {"rotation": [0, 225, 0], "translation": [0, 2, 0], "scale": [0.55, 0.55, 0.55]},
    },
})

def java_strings(items, per_line=4):
    items = [f'"{x}"' for x in items]
    lines = [", ".join(items[k:k + per_line]) for k in range(0, len(items), per_line)]
    return (",\n\t\t\t").join(lines)


java = f"""package com.femboyequipment.block;

import java.util.List;
import java.util.Map;
import java.util.Set;

/** GENERATED by the Blåhaj content script: all {len(VARIANTS)} Blåhaj variants. Do not edit by hand. */
public final class BlahajVariants {{
	public static final List<String> NAMES = List.of(
			{java_strings(VARIANTS)});

	/** Light level for the glowing ones. */
	public static final Map<String, Integer> LIGHT = Map.ofEntries(
			{(",\n\t\t\t").join(f'Map.entry("{k}", {v})' for k, v in LIGHT.items())});

	public static final Set<String> RARE = Set.of(
			{java_strings(sorted(RARE))});

	public static final Set<String> FIRE_RESISTANT = Set.of(
			{java_strings(sorted(FIRE_RESISTANT))});

	private BlahajVariants() {{
	}}
}}
"""
with open(os.path.join(ROOT, "src/main/java/com/femboyequipment/block/BlahajVariants.java"), "w") as f:
    f.write(java)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "blahaj_meta.json"), "w") as f:
    json.dump({"order": list(VARIANTS), "category": CATEGORY}, f)

lang = {"itemGroup.femboyequipment.blahaj": "Blåhaj"}
for name, (display, colors, extra) in VARIANTS.items():
    texture(name, colors)
    write_json(f"{ASSETS}/models/block/{name}.json", {
        "parent": f"{NS}:block/blahaj_base",
        "textures": {"shark": f"{NS}:block/blahaj/{name}"},
    })
    write_json(f"{ASSETS}/blockstates/{name}.json", {"variants": {
        f"facing={d}": {"model": f"{NS}:block/{name}", **({"y": r} if r else {})}
        for d, r in (("north", 0), ("east", 90), ("south", 180), ("west", 270))
    }})
    write_json(f"{ASSETS}/items/{name}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:block/{name}"}})
    write_json(f"{DATA}/loot_table/blocks/{name}.json", {
        "type": "minecraft:block",
        "pools": [{
            "bonus_rolls": 0.0,
            "conditions": [{"condition": "minecraft:survives_explosion"}],
            "entries": [{"type": "minecraft:item", "name": f"{NS}:{name}"}],
            "rolls": 1.0,
        }],
        "random_sequence": f"{NS}:blocks/{name}",
    })
    if extra == []:
        pass  # capsule-only
    elif extra is None:
        write_json(f"{DATA}/recipe/{name}.json", {
            "type": "minecraft:crafting_shaped",
            "category": "misc",
            "key": {"B": "minecraft:light_blue_wool", "C": "minecraft:cyan_wool", "W": "minecraft:white_wool"},
            "pattern": [" C ", "CBC", "WWB"],
            "result": {"count": 1, "id": f"{NS}:{name}"},
        })
    else:
        write_json(f"{DATA}/recipe/{name}.json", {
            "type": "minecraft:crafting_shapeless",
            "category": "misc",
            "group": "blahaj",
            "ingredients": [f"{NS}:blahaj", *extra],
            "result": {"count": 1, "id": f"{NS}:{name}"},
        })
    lang[f"block.{NS}.{name}"] = display

lang_path = f"{ASSETS}/lang/en_us.json"
merged = json.load(open(lang_path, encoding="utf-8"))
merged.update(lang)
write_json(lang_path, merged)
print("blahaj done:", len(VARIANTS))
