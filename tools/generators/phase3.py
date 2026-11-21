"""Phase 3 content: femboy villager skin + spawn egg, pink cat variant, Pastel Bloom flower,
the cute house structure (NBT template + jigsaw worldgen) and its loot.

Usage: python3 phase3.py <repo root>   (run after content.py and blahaj.py; it merges into en_us.json)
"""
import gzip
import json
import os
import random
import struct
import sys

from PIL import Image

ROOT = sys.argv[1]
RES = os.path.join(ROOT, "src/main/resources")
ASSETS = os.path.join(RES, "assets/femboyequipment")
DATA = os.path.join(RES, "data/femboyequipment")
NS = "femboyequipment"
DATA_VERSION = 4671  # Minecraft 1.21.11


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent="\t", ensure_ascii=False)
        f.write("\n")


def save(im, rel):
    path = os.path.join(ASSETS, "textures", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (255,)


def faces(u, v, w, h, d):
    return {
        "top": (u + d, v, w, d),
        "bottom": (u + d + w, v, w, d),
        "right": (u, v + d, d, h),
        "front": (u + d, v + d, w, h),
        "left": (u + d + w, v + d, d, h),
        "back": (u + d + w + d, v + d, w, h),
    }


def fill(im, rect, fn, rnd, noise=0.05):
    x0, y0, w, h = rect
    for y in range(h):
        for x in range(w):
            c = fn(x, y, w, h)
            if c is not None:
                im.putpixel((x0 + x, y0 + y), shade(c, 1 + rnd.uniform(-noise, noise)))


def box(im, u, v, w, h, d, fn, rnd, noise=0.05):
    for side, rect in faces(u, v, w, h, d).items():
        fill(im, rect, lambda x, y, fw, fh: fn(side, x, y, fw, fh), rnd, noise)


# ------------------------------------------------------------ villager skin
SKIN = (243, 207, 185)
HAIR = (247, 160, 205)
HAIR_DARK = (222, 118, 172)
WHITE = (248, 246, 250)
IRIS = (95, 175, 238)
LASH = (70, 40, 70)
BLUSH = (246, 150, 165)
MOUTH = (205, 105, 125)


def villager_skin():
    rnd = random.Random(1)
    im = Image.new("RGBA", (64, 32))

    def hair(x, y):
        return HAIR_DARK if (x + 2 * y) % 5 == 0 else HAIR

    def head(side, x, y, w, h):
        if side in ("top", "back", "left", "right"):
            return hair(x, y)
        if side == "bottom":
            return SKIN
        # face
        if y <= 1 or (y == 2 and x in (0, 1, 3, 6, 7)):
            return hair(x, y)  # bangs
        if x in (0, 7) and y <= 5:
            return hair(x, y)  # side locks
        if y == 3 and x in (1, 2, 5, 6):
            return LASH
        if y == 4:
            return {1: WHITE, 2: IRIS, 5: IRIS, 6: WHITE}.get(x, SKIN)
        if y == 5 and x in (1, 6):
            return BLUSH
        if y == 6 and x in (3, 4):
            return MOUTH
        return SKIN
    box(im, 0, 0, 8, 8, 8, head, rnd, 0.03)

    # a little ribbon bow on the hat layer, on the back of the head
    def bow(side, x, y, w, h):
        if side == "back" and y in (1, 2) and x in (2, 3, 4, 5):
            return (235, 70, 140) if x in (3, 4) and y == 1 else (250, 120, 180)
        return None
    box(im, 32, 0, 8, 8, 8, bow, rnd, 0.0)

    def body(side, x, y, w, h):
        if side == "front" and y == 0 and 2 <= x <= 5:
            return (240, 120, 175)  # collar
        return WHITE
    box(im, 16, 16, 8, 12, 4, body, rnd, 0.03)
    box(im, 40, 16, 4, 12, 4, lambda side, x, y, w, h: WHITE if side != "bottom" and y <= 3 else SKIN, rnd, 0.03)
    box(im, 0, 16, 4, 12, 4, lambda side, x, y, w, h: (240, 120, 175) if y >= 11 or side == "bottom" else SKIN, rnd, 0.03)
    save(im, "entity/femboy_villager.png")


# ------------------------------------------------------------ spawn egg
def spawn_egg():
    egg = [
        "......dddd......",
        ".....dppppd.....",
        "....dppwwppd....",
        "...dppwwpppkd...",
        "...dpppppppkd...",
        "..dppppwwppppd..",
        "..dpppwwwwpppd..",
        "..dppppwwppppd..",
        "..dpwwpppppkkd..",
        "..dpwwppppppkd..",
        "..dppppppwwpkd..",
        "...dppppwwwpd...",
        "...dkppppppkd...",
        "....dkkppkkd....",
        ".....dddddd.....",
        "................",
    ]
    eggs = {
        # trader egg: pink with white spots
        "femboy_villager_spawn_egg": {"d": (150, 50, 110), "p": (245, 160, 200), "k": (220, 120, 170), "w": (255, 240, 248)},
        # pink cat egg: soft pink fur with darker tabby spots
        "pink_cat_spawn_egg": {"d": (170, 70, 120), "p": (255, 200, 222), "k": (240, 160, 195), "w": (226, 128, 176)},
    }
    for name, pal in eggs.items():
        im = Image.new("RGBA", (16, 16))
        for y, row in enumerate(egg):
            for x, c in enumerate(row):
                if c != ".":
                    im.putpixel((x, y), pal[c] + (255,))
        save(im, f"item/{name}.png")
        write_json(f"{ASSETS}/items/{name}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:item/{name}"}})
        write_json(f"{ASSETS}/models/item/{name}.json",
                   {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{name}"}})


# ------------------------------------------------------------ pink cat
FUR = (246, 172, 205)
FUR_DARK = (226, 128, 176)
FUR_WHITE = (252, 238, 245)
CAT_EYE = (110, 205, 235)


def pink_cat():
    rnd = random.Random(2)
    im = Image.new("RGBA", (64, 32))

    def tabby(x, y):
        return FUR_DARK if (x + y) % 4 == 0 else FUR

    def head(side, x, y, w, h):
        if side == "front":
            if y == 1 and x in (0, 4):
                return CAT_EYE
            if y == 1 and x in (1, 3):
                return (40, 30, 50)
            return FUR if y < 3 else FUR_WHITE
        if side == "top":
            return FUR_DARK if x in (1, 3) else FUR
        return tabby(x, y)
    box(im, 0, 0, 5, 4, 5, head, rnd)
    box(im, 0, 24, 3, 2, 2, lambda side, x, y, w, h: (240, 110, 150) if side == "front" and y == 0 and x == 1 else FUR_WHITE, rnd)
    for u in (0, 6):
        box(im, u, 10, 1, 1, 2, lambda side, x, y, w, h: (255, 200, 220) if side == "front" else FUR_DARK, rnd)
    # body: "front" faces down after the model's rotation, so it is the belly
    box(im, 20, 0, 4, 16, 6, lambda side, x, y, w, h: FUR_WHITE if side == "front" else (FUR_DARK if y % 4 == 1 else FUR), rnd)
    box(im, 0, 15, 1, 8, 1, lambda side, x, y, w, h: FUR_DARK if y % 3 == 0 else FUR, rnd)
    box(im, 4, 15, 1, 8, 1, lambda side, x, y, w, h: FUR_WHITE if y >= 5 else (FUR_DARK if y % 3 == 0 else FUR), rnd)
    box(im, 8, 13, 2, 6, 2, lambda side, x, y, w, h: FUR_WHITE if y >= 4 or side == "bottom" else FUR, rnd)
    box(im, 40, 0, 2, 10, 2, lambda side, x, y, w, h: FUR_WHITE if y >= 8 or side == "bottom" else FUR, rnd)
    save(im, "entity/cat/pink.png")
    write_json(f"{DATA}/cat_variant/pink.json", {
        "asset_id": f"{NS}:entity/cat/pink",
        "spawn_conditions": [
            {"condition": {"type": "minecraft:structure", "structures": f"#{NS}:cats_spawn_as_pink"}, "priority": 1},
            {"priority": 0},
        ],
    })
    write_json(f"{DATA}/tags/worldgen/structure/cats_spawn_as_pink.json", {"values": [f"{NS}:cute_house"]})


# ------------------------------------------------------------ pastel bloom
def pastel_bloom():
    rows = [
        "................",
        "......pp........",
        ".....pllp.pp....",
        "....pllllpllp...",
        "....plyylllllp..",
        ".....plyylllp...",
        "....pllllpp.....",
        ".....pppgp......",
        "........g..pp...",
        "...pp...g.pllp..",
        "..pllp..g.plyp..",
        "..plyp.gg..pp...",
        "...pp..g..g.....",
        ".....g.g.g......",
        "......ggg.......",
        ".......g........",
    ]
    pal = {"p": (232, 110, 170), "l": (255, 185, 220), "y": (255, 230, 120), "g": (80, 160, 70)}
    im = Image.new("RGBA", (16, 16))
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c != ".":
                im.putpixel((x, y), pal[c] + (255,))
    save(im, "block/pastel_bloom.png")
    write_json(f"{ASSETS}/blockstates/pastel_bloom.json", {"variants": {"": {"model": f"{NS}:block/pastel_bloom"}}})
    write_json(f"{ASSETS}/models/block/pastel_bloom.json",
               {"parent": "minecraft:block/cross", "textures": {"cross": f"{NS}:block/pastel_bloom"}})
    write_json(f"{ASSETS}/items/pastel_bloom.json",
               {"model": {"type": "minecraft:model", "model": f"{NS}:item/pastel_bloom"}})
    write_json(f"{ASSETS}/models/item/pastel_bloom.json",
               {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:block/pastel_bloom"}})
    write_json(f"{DATA}/loot_table/blocks/pastel_bloom.json", {
        "type": "minecraft:block",
        "pools": [{"bonus_rolls": 0.0, "conditions": [{"condition": "minecraft:survives_explosion"}],
                   "entries": [{"type": "minecraft:item", "name": f"{NS}:pastel_bloom"}], "rolls": 1.0}],
        "random_sequence": f"{NS}:blocks/pastel_bloom",
    })
    write_json(f"{DATA}/recipe/pink_dye_from_pastel_bloom.json", {
        "type": "minecraft:crafting_shapeless", "category": "misc", "group": "pink_dye",
        "ingredients": [f"{NS}:pastel_bloom"], "result": {"count": 2, "id": "minecraft:pink_dye"},
    })
    write_json(f"{RES}/data/minecraft/tags/block/small_flowers.json", {"replace": False, "values": [f"{NS}:pastel_bloom"]})
    write_json(f"{RES}/data/minecraft/tags/item/small_flowers.json", {"replace": False, "values": [f"{NS}:pastel_bloom"]})
    write_json(f"{DATA}/worldgen/configured_feature/pastel_bloom_patch.json", {
        "type": "minecraft:flower",
        "config": {
            "feature": {
                "feature": {"type": "minecraft:simple_block", "config": {
                    "to_place": {"type": "minecraft:simple_state_provider", "state": {"Name": f"{NS}:pastel_bloom"}}}},
                "placement": [{"type": "minecraft:block_predicate_filter",
                               "predicate": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"}}],
            },
            "tries": 48, "xz_spread": 6, "y_spread": 2,
        },
    })
    write_json(f"{DATA}/worldgen/placed_feature/pastel_bloom_patch.json", {
        "feature": f"{NS}:pastel_bloom_patch",
        "placement": [{"type": "minecraft:rarity_filter", "chance": 24}, {"type": "minecraft:in_square"},
                      {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"}],
    })


# ------------------------------------------------------------ NBT writer
class Int(int):
    pass


class Byte(int):
    pass


class Double(float):
    pass


def nbt_payload(v):
    if isinstance(v, Byte):
        return 1, struct.pack(">b", v)
    if isinstance(v, Int):
        return 3, struct.pack(">i", v)
    if isinstance(v, Double):
        return 6, struct.pack(">d", v)
    if isinstance(v, str):
        b = v.encode("utf-8")
        return 8, struct.pack(">H", len(b)) + b
    if isinstance(v, list):
        if not v:
            return 9, struct.pack(">bi", 0, 0)
        items = [nbt_payload(x) for x in v]
        t = items[0][0]
        assert all(i[0] == t for i in items)
        return 9, struct.pack(">bi", t, len(v)) + b"".join(i[1] for i in items)
    if isinstance(v, dict):
        out = b""
        for k, x in v.items():
            t, p = nbt_payload(x)
            kb = k.encode("utf-8")
            out += struct.pack(">bH", t, len(kb)) + kb + p
        return 10, out + b"\x00"
    raise TypeError(type(v))


def write_nbt(path, root):
    t, payload = nbt_payload(root)
    data = struct.pack(">bH", 10, 0) + payload
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with gzip.open(path, "wb") as f:
        f.write(data)


# ------------------------------------------------------------ cute house
def cute_house():
    W, H, D = 9, 10, 9
    palette, index = [], {}
    blocks = {}

    def state(name, **props):
        key = (name, tuple(sorted(props.items())))
        if key not in index:
            entry = {"Name": name}
            if props:
                entry["Properties"] = {k: str(v) for k, v in props.items()}
            index[key] = len(palette)
            palette.append(entry)
        return index[key]

    def put(x, y, z, name, nbt=None, **props):
        blocks[(x, y, z)] = (state(name, **props), nbt)

    # clear the inside
    for x in range(W):
        for y in range(1, H):
            for z in range(D):
                put(x, y, z, "minecraft:air")
    # floor
    for x in range(W):
        for z in range(D):
            put(x, 0, z, "minecraft:cherry_planks")
    # walls with cherry log corners
    for y in range(1, 5):
        for i in range(W):
            for x, z in ((i, 0), (i, D - 1), (0, i), (W - 1, i)):
                corner = x in (0, W - 1) and z in (0, D - 1)
                put(x, y, z, "minecraft:cherry_log" if corner else f"{NS}:pastel_pink_bricks",
                    **({"axis": "y"} if corner else {}))
    # windows
    for y in (2, 3):
        for a in (2, 6):
            put(a, y, D - 1, "minecraft:pink_stained_glass")
            put(0, y, a, "minecraft:pink_stained_glass")
            put(W - 1, y, a, "minecraft:pink_stained_glass")
        put(2, y, 0, "minecraft:pink_stained_glass")
        put(6, y, 0, "minecraft:pink_stained_glass")
    # door in the middle of the front (z = 0)
    put(4, 1, 0, "minecraft:cherry_door", facing="south", half="lower", hinge="left", open="false", powered="false")
    put(4, 2, 0, "minecraft:cherry_door", facing="south", half="upper", hinge="left", open="false", powered="false")
    # stepped roof
    roof = ["minecraft:pink_wool", "minecraft:white_wool", "minecraft:pink_wool", "minecraft:white_wool", "minecraft:magenta_wool"]
    for level, inset in enumerate(range(0, 5)):
        y = 5 + level
        for x in range(inset, W - inset):
            for z in range(inset, D - inset):
                put(x, y, z, roof[level])
    # furniture
    put(1, 1, 7, "minecraft:chest", nbt={"LootTable": f"{NS}:chests/cute_house"},
        facing="east", type="single", waterlogged="false")
    put(3, 1, 6, "minecraft:pink_bed", facing="south", part="foot", occupied="false")
    put(3, 1, 7, "minecraft:pink_bed", facing="south", part="head", occupied="false")
    put(6, 1, 7, f"{NS}:trans_blahaj", facing="north")
    put(7, 1, 7, f"{NS}:blahaj", facing="west")
    put(7, 1, 1, f"{NS}:glow_blahaj", facing="west")
    put(1, 1, 1, f"{NS}:ribbon_block")
    for x in range(3, 6):
        for z in range(3, 6):
            put(x, 1, z, "minecraft:pink_carpet")

    block_list = []
    for (x, y, z), (s, nbt) in sorted(blocks.items()):
        entry = {"pos": [Int(x), Int(y), Int(z)], "state": Int(s)}
        if nbt:
            entry["nbt"] = nbt
        block_list.append(entry)

    def entity(x, y, z, nbt):
        return {"pos": [Double(x), Double(y), Double(z)], "blockPos": [Int(int(x)), Int(int(y)), Int(int(z))], "nbt": nbt}

    root = {
        "DataVersion": Int(DATA_VERSION),
        "size": [Int(W), Int(H), Int(D)],
        "palette": palette,
        "blocks": block_list,
        "entities": [
            entity(4.5, 2.0, 4.5, {"id": f"{NS}:femboy_villager", "PersistenceRequired": Byte(1)}),
            entity(5.5, 2.0, 2.5, {"id": "minecraft:cat", "PersistenceRequired": Byte(1)}),
        ],
    }
    write_nbt(f"{DATA}/structure/cute_house.nbt", root)

    write_json(f"{DATA}/worldgen/template_pool/cute_house.json", {
        "elements": [{"element": {"element_type": "minecraft:single_pool_element", "location": f"{NS}:cute_house",
                                  "processors": {"processors": []}, "projection": "rigid"}, "weight": 1}],
        "fallback": "minecraft:empty",
    })
    write_json(f"{DATA}/worldgen/structure/cute_house.json", {
        "type": "minecraft:jigsaw",
        "biomes": f"#{NS}:has_cute_house",
        "max_distance_from_center": 80,
        "project_start_to_heightmap": "WORLD_SURFACE_WG",
        "size": 1,
        "spawn_overrides": {},
        "start_height": {"absolute": 0},
        "start_pool": f"{NS}:cute_house",
        "step": "surface_structures",
        "terrain_adaptation": "beard_thin",
        "use_expansion_hack": False,
    })
    write_json(f"{DATA}/worldgen/structure_set/cute_house.json", {
        "placement": {"type": "minecraft:random_spread", "salt": 20051210, "separation": 8, "spacing": 20},
        "structures": [{"structure": f"{NS}:cute_house", "weight": 1}],
    })
    write_json(f"{DATA}/tags/worldgen/biome/has_cute_house.json", {"values": [
        "minecraft:plains", "minecraft:sunflower_plains", "minecraft:meadow", "minecraft:flower_forest", "minecraft:cherry_grove"]})

    def item(name, weight, lo=1, hi=1):
        e = {"type": "minecraft:item", "name": name, "weight": weight}
        if hi > 1:
            e["functions"] = [{"function": "minecraft:set_count",
                               "count": {"type": "minecraft:uniform", "min": lo, "max": hi}, "add": False}]
        return e
    write_json(f"{DATA}/loot_table/chests/cute_house.json", {
        "type": "minecraft:chest",
        "pools": [
            {"rolls": {"type": "minecraft:uniform", "min": 4, "max": 7}, "bonus_rolls": 0.0, "entries": [
                item(f"{NS}:pink_ribbon", 15, 2, 6), item(f"{NS}:strawberry_milk", 10, 1, 3),
                item(f"{NS}:hair_clip", 8, 1, 2), item(f"{NS}:pastel_bloom", 8, 2, 5),
                item("minecraft:emerald", 8, 2, 7), item(f"{NS}:choker", 4), item(f"{NS}:programming_socks", 4),
                item("minecraft:cherry_sapling", 4, 1, 2), item("minecraft:cake", 2),
            ]},
            {"rolls": 1.0, "bonus_rolls": 0.0, "entries": [
                item(f"{NS}:cat_ears", 2), item(f"{NS}:femboy_hoodie", 2), item(f"{NS}:pleated_skirt", 2),
                item(f"{NS}:maid_headband", 2), item(f"{NS}:mary_janes", 2), item(f"{NS}:bunny_ears", 2),
                item(f"{NS}:fluffy_slippers", 2), item(f"{NS}:pink_blahaj", 2), item(f"{NS}:trans_blahaj", 2),
                item(f"{NS}:femboy_villager_spawn_egg", 1),
            ]},
        ],
        "random_sequence": f"{NS}:chests/cute_house",
    })


villager_skin()
spawn_egg()
pink_cat()
pastel_bloom()
cute_house()

lang_path = f"{ASSETS}/lang/en_us.json"
lang = json.load(open(lang_path, encoding="utf-8"))
lang.update({
    "entity.femboyequipment.femboy_villager": "Femboy Trader",
    "item.femboyequipment.femboy_villager_spawn_egg": "Femboy Trader Spawn Egg",
    "item.femboyequipment.pink_cat_spawn_egg": "Pink Cat Spawn Egg",
    "block.femboyequipment.pastel_bloom": "Pastel Bloom",
})
write_json(lang_path, lang)
print("phase 3 done")
