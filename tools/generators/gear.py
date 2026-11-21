"""Gear update: Rose Quartz (material, armor, tools, spear), extra Sparkly tools, joke weapons,
gacha capsules, pastel brick colors + stairs/slabs/walls.

Usage: python3 gear.py <repo root>   (merges into en_us.json)
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
MC = os.path.join(RES, "data/minecraft")
NS = "femboyequipment"
LANG = {}


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent="\t", ensure_ascii=False)
        f.write("\n")


def save(im, rel):
    path = os.path.join(ASSETS, "textures", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)


def i(n):
    return n if ":" in n else f"{NS}:{n}"


RAMPS = {
    "q": [(150, 60, 100), (215, 120, 160), (245, 170, 200), (255, 205, 225), (255, 235, 245)],  # rose quartz
    "c": [(150, 40, 110), (220, 100, 170), (250, 160, 210), (255, 205, 235), (255, 240, 250)],  # sparkly crystal
    "h": [(50, 25, 40), (80, 40, 65), (110, 60, 90), (140, 85, 115), (170, 110, 140)],          # handle
    "w": [(120, 110, 130), (190, 182, 198), (228, 222, 234), (246, 242, 250), (255, 255, 255)],
    "s": [(60, 70, 85), (110, 125, 140), (165, 178, 192), (205, 214, 224), (235, 240, 246)],    # fish silver
    "b": [(30, 50, 70), (55, 95, 125), (80, 125, 155), (110, 155, 185), (150, 190, 215)],      # blåhaj blue
    "t": [(40, 90, 100), (60, 150, 160), (90, 200, 205), (140, 230, 230), (200, 250, 250)],     # teal capsule
    "y": [(120, 80, 20), (200, 140, 40), (240, 190, 60), (255, 220, 100), (255, 245, 180)],
    "k": [(10, 8, 12), (30, 24, 34), (48, 40, 54), (70, 60, 78), (100, 90, 110)],
}
FLAT = {"Y": (255, 240, 150, 255), "E": (20, 20, 24, 255), "W": (255, 255, 255, 255)}


def sprite(pixels, size=16):
    """pixels: dict (x, y) -> material. Adds outlines + simple top-left lighting."""
    solid = lambda x, y: (x, y) in pixels and pixels[(x, y)] not in FLAT
    im = Image.new("RGBA", (size, size))
    for y in range(size):
        for x in range(size):
            m = pixels.get((x, y))
            if m is None:
                for nx, ny in ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)):
                    if solid(nx, ny):
                        im.putpixel((x, y), RAMPS[pixels[(nx, ny)]][0] + (255,))
                        break
                continue
            if m in FLAT:
                im.putpixel((x, y), FLAT[m])
                continue
            up, left, down, right = solid(x, y - 1), solid(x - 1, y), solid(x, y + 1), solid(x + 1, y)
            shade = 4 if not up and not left else 3 if not up or not left else 1 if not down or not right else 2
            im.putpixel((x, y), RAMPS[m][shade] + (255,))
    return im


def grid(rows, mat_map=None):
    px = {}
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != ".":
                px[(x, y)] = (mat_map or {}).get(ch, ch)
    return px


def line(px, a, b, m):
    (x0, y0), (x1, y1) = a, b
    n = max(abs(x1 - x0), abs(y1 - y0))
    for k in range(n + 1):
        px[(round(x0 + (x1 - x0) * k / n), round(y0 + (y1 - y0) * k / n))] = m


def tool(kind, head, handle="h"):
    px = {}
    if kind == "spear":
        line(px, (2, 13), (10, 5), handle)
        for p in ((11, 4), (12, 3), (13, 2), (12, 2), (13, 3), (11, 3), (12, 4)):
            px[p] = head
        px[(14, 1)] = head
        return px
    line(px, (2, 13), (10, 5), handle)
    heads = {
        "axe": [(10, 1), (11, 1), (12, 1), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (9, 3), (10, 3), (11, 3),
                (12, 3), (13, 3), (12, 4), (13, 4), (13, 5), (11, 4)],
        "shovel": [(11, 1), (12, 1), (10, 2), (11, 2), (12, 2), (13, 2), (10, 3), (11, 3), (12, 3), (13, 3),
                   (11, 4), (12, 4)],
        "hoe": [(7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3),
                (11, 4)],
    }
    for p in heads[kind]:
        px[p] = head
    return px


SWORD = [
    "..............Y.",
    ".............ww.",
    "............wcw.",
    "...Y.......wcw..",
    "..........wcw...",
    ".........wcw....",
    "........wcw.....",
    ".......wcw......",
    "......wcw.......",
    "..yy.wcw........",
    "...yywc.........",
    "....yyy.........",
    "....h.yy........",
    "...h............",
    "..h.............",
]
PICKAXE = [
    "...........Y....",
    "....ccccc.......",
    "...cwwwwwcc.....",
    "....ccc..wcc....",
    "........hywcc...",
    ".......h.yy.cc..",
    "......h......wc.",
    ".....h.......wc.",
    "....h.........c.",
    "...h..........c.",
    "..h.............",
    ".h..............",
]

ITEM_SPRITES = {}
ITEM_SPRITES["rose_quartz"] = grid([
    "", "",
    "......qqqq......",
    ".....qqWqqq.....",
    "....qqWqqqqq....",
    "...qqqqqqqqqq...",
    "....qqqqqqqq....",
    ".....qqqqqq.....",
    "......qqqq......",
    ".......qq.......",
])
ITEM_SPRITES["rose_quartz_helmet"] = grid(["", "", "", "....qqqqqqqq....", "...qqqqqqqqqq...", "...qqqWqqqqqq...",
                                           "...qqq....qqq...", "...qq......qq...", "...qq......qq..."])
ITEM_SPRITES["rose_quartz_chestplate"] = grid(["", "..qqq......qqq..", "..qqqq....qqqq..", "..qqqqqqqqqqqq..",
                                               "...qqqqWqqqqq...", "....qqqqqqqq....", "....qqqqqqqq....",
                                               "....qqqqqqqq....", "....qqqqqqqq....", "....qqqqqqqq....",
                                               "....qqqqqqqq....", "....qqqqqqqq...."])
ITEM_SPRITES["rose_quartz_leggings"] = grid(["", "", "...qqqqqqqqqq...", "...qqqqqqqqqq...", "...qqqq..qqqq...",
                                             "...qqq....qqq...", "...qqq....qqq...", "...qqq....qqq...",
                                             "...qqq....qqq...", "...qqq....qqq...", "...qqq....qqq..."])
ITEM_SPRITES["rose_quartz_boots"] = grid(["", "", "", "", "", "", "...qqq....qqq...", "...qqq....qqq...",
                                          "...qqq....qqq...", ".qqqqq....qqqqq.", ".qqqqq....qqqqq."])
ITEM_SPRITES["rose_quartz_sword"] = grid(SWORD, {"c": "q", "w": "q"})
ITEM_SPRITES["rose_quartz_pickaxe"] = grid(PICKAXE, {"c": "q", "w": "q"})
for kind in ("axe", "shovel", "hoe", "spear"):
    ITEM_SPRITES[f"rose_quartz_{kind}"] = tool(kind, "q")
for kind in ("axe", "shovel", "hoe"):
    ITEM_SPRITES[f"sparkly_{kind}"] = tool(kind, "c")
    ITEM_SPRITES[f"sparkly_{kind}"][(14, 1)] = "Y"

# Fih Slapper: a silver fish on a stick
slap = {}
line(slap, (2, 13), (7, 8), "h")
for y in range(2, 8):
    for x in range(7, 14):
        if (x - 10) ** 2 / 9 + (y - 5) ** 2 / 4 <= 1.0:
            slap[(x, y)] = "s"
for p in ((13, 2), (14, 1), (13, 8), (14, 9), (14, 5)):
    slap[p] = "s"
slap[(9, 4)] = "E"
ITEM_SPRITES["fih_slapper"] = slap

# Blåhaj Bat: a chunky blue bat with a white belly stripe
bat = {}
for k in range(12):
    x, y = 2 + k, 13 - k
    width = 1 + k // 4
    for d in range(-width, width + 1):
        bat[(x + d, y)] = "b" if d < width else "w"
line(bat, (1, 14), (3, 12), "h")
ITEM_SPRITES["blahaj_bat"] = bat


def capsule(top, label):
    px = {}
    for y in range(2, 14):
        for x in range(2, 14):
            if (x - 7.5) ** 2 + (y - 7.5) ** 2 <= 30:
                px[(x, y)] = top if y < 8 else "w"
    for x in range(2, 14):
        if (x, 8) in px:
            px[(x, 8)] = "k"
    px[(7, 8)] = "W"
    px[(8, 8)] = "W"
    for p in label:
        px[p] = "W"
    return px


ITEM_SPRITES["blahaj_capsule"] = capsule("b", [(5, 4), (6, 4), (5, 5)])
ITEM_SPRITES["fih_capsule"] = capsule("t", [(5, 4), (6, 4), (5, 5)])

for name, px in ITEM_SPRITES.items():
    save(sprite(px), f"item/{name}.png")

# 32x32 in-hand spear
spear = {}
for k in range(22):
    spear[(4 + k, 27 - k)] = "h"
    spear[(5 + k, 27 - k)] = "h"
for p in [(26, 5), (27, 4), (28, 3), (29, 2), (27, 5), (28, 4), (29, 3), (26, 4), (27, 3), (28, 2),
          (25, 6), (26, 6), (25, 5), (24, 6), (25, 7), (30, 1), (29, 1), (30, 2)]:
    spear[p] = "q"
save(sprite(spear, 32), "item/rose_quartz_spear_in_hand.png")

HANDHELD = [n for n in ITEM_SPRITES if any(n.endswith(s) for s in ("sword", "pickaxe", "axe", "shovel", "hoe"))
            and not n.startswith("rose_quartz_spear")] + ["fih_slapper", "blahaj_bat"]
for name in ITEM_SPRITES:
    if name == "rose_quartz_spear":
        write_json(f"{ASSETS}/models/item/{name}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": i(f"item/{name}")}})
        write_json(f"{ASSETS}/models/item/{name}_in_hand.json", {"parent": "minecraft:item/spear_in_hand", "textures": {"layer0": i(f"item/{name}_in_hand")}})
        write_json(f"{ASSETS}/items/{name}.json", {"model": {
            "type": "minecraft:select", "property": "minecraft:display_context",
            "cases": [{"model": {"type": "minecraft:model", "model": i(f"item/{name}")}, "when": ["gui", "ground", "fixed", "on_shelf"]}],
            "fallback": {"type": "minecraft:model", "model": i(f"item/{name}_in_hand")}}, "swap_animation_scale": 1.95})
        continue
    write_json(f"{ASSETS}/models/item/{name}.json", {
        "parent": "minecraft:item/handheld" if name in HANDHELD else "minecraft:item/generated",
        "textures": {"layer0": i(f"item/{name}")}})
    write_json(f"{ASSETS}/items/{name}.json", {"model": {"type": "minecraft:model", "model": i(f"item/{name}")}})


# ------------------------------------------------------------ worn rose quartz armor
def faces(u, v, w, h, d):
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + d + w + d, v + d, w, h)}


HEAD, BODY, ARM, LEG = faces(0, 0, 8, 8, 8), faces(16, 16, 8, 12, 4), faces(40, 16, 4, 12, 4), faces(0, 16, 4, 12, 4)
Q = RAMPS["q"]


def paint(im, rect, fn):
    x0, y0, w, h = rect
    for dy in range(h):
        for dx in range(w):
            c = fn(dx, dy, w, h)
            if c is not None:
                im.putpixel((x0 + dx, y0 + dy), c + (255,))


def crystal(dx, dy, w, h):
    if dy == 0 or dx == 0:
        return Q[4]
    if dy == h - 1 or dx == w - 1:
        return Q[1]
    return Q[3] if (dx + dy) % 4 == 0 else Q[2]


main = Image.new("RGBA", (64, 32))
for side, rect in HEAD.items():
    if side == "front":
        paint(main, rect, lambda x, y, w, h: None if (2 <= x <= 5 and 3 <= y <= 6) else crystal(x, y, w, h))
    elif side != "bottom":
        paint(main, rect, crystal)
for rect in BODY.values():
    paint(main, rect, crystal)
for rect in ARM.values():
    paint(main, rect, lambda x, y, w, h: crystal(x, y, w, h) if y <= 8 else None)
for side, rect in LEG.items():
    paint(main, rect, lambda x, y, w, h: crystal(x, y, w, h) if y >= 8 or side in ("bottom",) else None)
save(main, "entity/equipment/humanoid/rose_quartz.png")
legs = Image.new("RGBA", (64, 32))
for side in ("right", "front", "left", "back"):
    paint(legs, BODY[side], lambda x, y, w, h: crystal(x, y, w, h) if y >= 8 else None)
    paint(legs, LEG[side], lambda x, y, w, h: crystal(x, y, w, h) if y <= 9 else None)
paint(legs, BODY["bottom"], crystal)
save(legs, "entity/equipment/humanoid_leggings/rose_quartz.png")
write_json(f"{ASSETS}/equipment/rose_quartz.json", {"layers": {
    "humanoid": [{"texture": i("rose_quartz")}], "humanoid_leggings": [{"texture": i("rose_quartz")}]}})


# ------------------------------------------------------------ blocks
def bricks(ramp, mortar, seed):
    rnd = random.Random(seed)
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            im.putpixel((x, y), mortar[(x + y) % 2] + (255,))
    for row in range(4):
        y0, off = row * 4, 0 if row % 2 == 0 else 4
        for x0 in range(-off, 16, 8):
            tone = rnd.choice([0, 0, 1])
            for y in range(y0, y0 + 3):
                for x in range(x0, x0 + 7):
                    if 0 <= x < 16:
                        s = 4 if y == y0 else 2 if (x == x0 + 6 or y == y0 + 2) else 3
                        s -= tone
                        if rnd.random() < 0.12:
                            s = max(1, s - 1)
                        im.putpixel((x, y), ramp[s] + (255,))
    return im


def ramp(rgb):
    return [tuple(int(v * f) for v in rgb) for f in (0.55, 0.75, 0.88, 1.0)] + [tuple(min(255, int(v + (255 - v) * 0.5)) for v in rgb)]


BRICK_COLORS = {
    "pastel_blue_bricks": ((150, 200, 245), [(225, 240, 255), (212, 230, 250)]),
    "pastel_lavender_bricks": ((200, 170, 240), [(240, 230, 255), (230, 218, 250)]),
    "pastel_mint_bricks": ((150, 225, 190), [(225, 250, 238), (212, 242, 228)]),
    "pastel_yellow_bricks": ((245, 225, 140), [(255, 250, 220), (250, 242, 205)]),
}
for k, (name, (rgb, mortar)) in enumerate(BRICK_COLORS.items()):
    save(bricks(ramp(rgb), mortar, 10 + k), f"block/{name}.png")
save(bricks(Q, [(255, 228, 240), (248, 215, 232)], 20), "block/rose_quartz_bricks.png")
rq = Image.new("RGBA", (16, 16))
rnd = random.Random(5)
for y in range(16):
    for x in range(16):
        facet = ((x // 4) + (y // 4) * 3) % 5
        s = [2, 3, 4, 3, 1][facet]
        if (x + y) % 7 == 0:
            s = 4
        rq.putpixel((x, y), tuple(min(255, int(v * (1 + rnd.uniform(-0.04, 0.04)))) for v in Q[s]) + (255,))
save(rq, "block/rose_quartz_block.png")

FULL_BLOCKS = list(BRICK_COLORS) + ["rose_quartz_block", "rose_quartz_bricks"]


def loot(name, extra=None):
    entry = {"type": "minecraft:item", "name": i(name)}
    if extra:
        entry["functions"] = extra
    write_json(f"{DATA}/loot_table/blocks/{name}.json", {
        "type": "minecraft:block",
        "pools": [{"bonus_rolls": 0.0, "conditions": [{"condition": "minecraft:survives_explosion"}] if not extra else [],
                   "entries": [entry], "rolls": 1.0}],
        "random_sequence": f"{NS}:blocks/{name}"})


for name in FULL_BLOCKS:
    write_json(f"{ASSETS}/blockstates/{name}.json", {"variants": {"": {"model": i(f"block/{name}")}}})
    write_json(f"{ASSETS}/models/block/{name}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": i(f"block/{name}")}})
    write_json(f"{ASSETS}/items/{name}.json", {"model": {"type": "minecraft:model", "model": i(f"block/{name}")}})
    loot(name)

SHAPE_BASES = {"pastel_pink_brick": "pastel_pink_bricks", "pastel_blue_brick": "pastel_blue_bricks",
               "pastel_lavender_brick": "pastel_lavender_bricks", "pastel_mint_brick": "pastel_mint_bricks",
               "pastel_yellow_brick": "pastel_yellow_bricks", "rose_quartz_brick": "rose_quartz_bricks"}


import zipfile  # noqa: E402

_CLIENT = zipfile.ZipFile("/root/.gradle/caches/fabric-loom/1.21.11/minecraft-client.jar")


def vanilla_states(vanilla, ours):
    """Copy a vanilla brick blockstate and point it at our models."""
    text = _CLIENT.read(f"assets/minecraft/blockstates/{vanilla}.json").decode()
    return json.loads(text.replace(f"minecraft:block/{vanilla}", i(f"block/{ours}")))


for shape_base, base in SHAPE_BASES.items():
    tex = i(f"block/{base}")
    t3 = {"bottom": tex, "top": tex, "side": tex}
    st, sl, wa = f"{shape_base}_stairs", f"{shape_base}_slab", f"{shape_base}_wall"
    for suffix, parent in (("", "stairs"), ("_inner", "inner_stairs"), ("_outer", "outer_stairs")):
        write_json(f"{ASSETS}/models/block/{st}{suffix}.json", {"parent": f"minecraft:block/{parent}", "textures": t3})
    write_json(f"{ASSETS}/blockstates/{st}.json", vanilla_states("brick_stairs", st))
    write_json(f"{ASSETS}/models/block/{sl}.json", {"parent": "minecraft:block/slab", "textures": t3})
    write_json(f"{ASSETS}/models/block/{sl}_top.json", {"parent": "minecraft:block/slab_top", "textures": t3})
    write_json(f"{ASSETS}/blockstates/{sl}.json", {"variants": {
        "type=bottom": {"model": i(f"block/{sl}")}, "type=top": {"model": i(f"block/{sl}_top")},
        "type=double": {"model": i(f"block/{base}")}}})
    for suffix, parent in (("_post", "template_wall_post"), ("_side", "template_wall_side"),
                           ("_side_tall", "template_wall_side_tall"), ("_inventory", "wall_inventory")):
        write_json(f"{ASSETS}/models/block/{wa}{suffix}.json", {"parent": f"minecraft:block/{parent}", "textures": {"wall": tex}})
    write_json(f"{ASSETS}/blockstates/{wa}.json", vanilla_states("brick_wall", wa))
    write_json(f"{ASSETS}/items/{st}.json", {"model": {"type": "minecraft:model", "model": i(f"block/{st}")}})
    write_json(f"{ASSETS}/items/{sl}.json", {"model": {"type": "minecraft:model", "model": i(f"block/{sl}")}})
    write_json(f"{ASSETS}/items/{wa}.json", {"model": {"type": "minecraft:model", "model": i(f"block/{wa}_inventory")}})
    loot(st)
    loot(wa)
    loot(sl, [{"function": "minecraft:set_count", "count": 2.0, "add": False, "conditions": [{
        "condition": "minecraft:block_state_property", "block": i(sl), "properties": {"type": "double"}}]},
        {"function": "minecraft:explosion_decay"}])


# ------------------------------------------------------------ recipes
def shaped(name, pattern, key, count=1, category="equipment", file=None):
    write_json(f"{DATA}/recipe/{file or name}.json", {"type": "minecraft:crafting_shaped", "category": category,
                                                      "key": key, "pattern": pattern, "result": {"count": count, "id": i(name)}})


def shapeless(name, ingredients, count=1, category="misc", file=None):
    write_json(f"{DATA}/recipe/{file or name}.json", {"type": "minecraft:crafting_shapeless", "category": category,
                                                      "ingredients": ingredients, "result": {"count": count, "id": i(name)}})


RQ, STICK = i("rose_quartz"), "minecraft:stick"
shapeless("rose_quartz", ["minecraft:amethyst_shard", "minecraft:quartz", "minecraft:pink_dye"], count=2)
shaped("rose_quartz_block", ["###", "###", "###"], {"#": RQ}, category="building")
shapeless("rose_quartz", [i("rose_quartz_block")], count=9, file="rose_quartz_from_block")
shaped("rose_quartz_bricks", ["##", "##"], {"#": i("rose_quartz_block")}, count=4, category="building")
for piece, pat in (("helmet", ["###", "# #"]), ("chestplate", ["# #", "###", "###"]),
                   ("leggings", ["###", "# #", "# #"]), ("boots", ["# #", "# #"])):
    shaped(f"rose_quartz_{piece}", pat, {"#": RQ})
for kind, pat in (("sword", ["#", "#", "S"]), ("pickaxe", ["###", " S ", " S "]), ("axe", ["##", "#S", " S"]),
                  ("shovel", ["#", "S", "S"]), ("hoe", ["##", " S", " S"]), ("spear", ["#", "S", "S"])):
    pattern = pat if kind != "spear" else ["  #", " S ", "S  "]
    shaped(f"rose_quartz_{kind}", pattern, {"#": RQ, "S": STICK})
for kind in ("axe", "shovel", "hoe"):
    shapeless(f"sparkly_{kind}", [f"minecraft:diamond_{kind}", i("pink_ribbon"), i("pink_ribbon")], category="equipment")
shaped("fih_slapper", ["C", "C", "S"], {"C": "minecraft:cod", "S": STICK})
shaped("blahaj_bat", ["B", "B", "S"], {"B": i("blahaj"), "S": STICK})
shapeless("blahaj_capsule", ["minecraft:light_blue_wool", "minecraft:white_wool", "minecraft:emerald"])
shapeless("fih_capsule", ["minecraft:cod", "minecraft:leather", "minecraft:emerald"])
DYES = {"pastel_blue_bricks": "light_blue", "pastel_lavender_bricks": "purple", "pastel_mint_bricks": "lime",
        "pastel_yellow_bricks": "yellow"}
for name, dye in DYES.items():
    shaped(name, ["BBB", "BDB", "BBB"], {"B": "minecraft:bricks", "D": f"minecraft:{dye}_dye"}, count=8, category="building")
for shape_base, base in SHAPE_BASES.items():
    shaped(f"{shape_base}_stairs", ["#  ", "## ", "###"], {"#": i(base)}, count=4, category="building")
    shaped(f"{shape_base}_slab", ["###"], {"#": i(base)}, count=6, category="building")
    shaped(f"{shape_base}_wall", ["###", "###"], {"#": i(base)}, count=6, category="misc")


# ------------------------------------------------------------ tags
def tag(path, values, base=MC):
    p = f"{base}/tags/{path}.json"
    existing = json.load(open(p))["values"] if os.path.exists(p) else []
    write_json(p, {"replace": False, "values": existing + [v for v in values if v not in existing]})


tag("item/rose_quartz_repair_materials", [RQ], DATA)
tag("item/head_armor", [i("rose_quartz_helmet")])
tag("item/chest_armor", [i("rose_quartz_chestplate")])
tag("item/leg_armor", [i("rose_quartz_leggings")])
tag("item/foot_armor", [i("rose_quartz_boots")])
tag("item/trimmable_armor", [i(f"rose_quartz_{p}") for p in ("helmet", "chestplate", "leggings", "boots")])
tag("item/swords", [i("rose_quartz_sword"), i("fih_slapper"), i("blahaj_bat")])
tag("item/pickaxes", [i("rose_quartz_pickaxe")])
tag("item/axes", [i("rose_quartz_axe"), i("sparkly_axe")])
tag("item/shovels", [i("rose_quartz_shovel"), i("sparkly_shovel")])
tag("item/hoes", [i("rose_quartz_hoe"), i("sparkly_hoe")])
tag("item/spears", [i("rose_quartz_spear")])
tag("block/mineable/pickaxe", [i(n) for n in FULL_BLOCKS] + [i(f"{b}_{s}") for b in SHAPE_BASES for s in ("stairs", "slab", "wall")])
tag("block/stairs", [i(f"{b}_stairs") for b in SHAPE_BASES])
tag("block/slabs", [i(f"{b}_slab") for b in SHAPE_BASES])
tag("block/walls", [i(f"{b}_wall") for b in SHAPE_BASES])
tag("item/stairs", [i(f"{b}_stairs") for b in SHAPE_BASES])
tag("item/slabs", [i(f"{b}_slab") for b in SHAPE_BASES])
tag("item/walls", [i(f"{b}_wall") for b in SHAPE_BASES])

# ------------------------------------------------------------ lang
def title(s):
    return " ".join(w.capitalize() for w in s.split("_"))


for name in ITEM_SPRITES:
    LANG[f"item.{NS}.{name}"] = title(name)
LANG[f"item.{NS}.fih_slapper"] = "Fih Slapper"
LANG[f"item.{NS}.blahaj_bat"] = "Blåhaj Bat"
LANG[f"item.{NS}.blahaj_capsule"] = "Blåhaj Capsule"
LANG[f"item.{NS}.fih_capsule"] = "Fih Capsule"
for name in FULL_BLOCKS:
    LANG[f"block.{NS}.{name}"] = title(name)
for b in SHAPE_BASES:
    for s in ("stairs", "slab", "wall"):
        LANG[f"block.{NS}.{b}_{s}"] = title(f"{b}_{s}")
LANG[f"message.{NS}.capsule"] = "✨ You got: %s!"
LANG["trinkets.slot.feet.socks"] = "Socks"

lang_path = f"{ASSETS}/lang/en_us.json"
lang = json.load(open(lang_path, encoding="utf-8"))
lang.update(LANG)
write_json(lang_path, lang)
print("gear done:", len(ITEM_SPRITES), "items,", len(FULL_BLOCKS) + 3 * len(SHAPE_BASES), "blocks")
