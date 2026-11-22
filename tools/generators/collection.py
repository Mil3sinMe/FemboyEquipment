"""Cute Collection assets: Collection Book + 8 rank-exclusive hats (item + head textures), lang, tags, recipe.

Usage: python3 collection.py <repo root>   (run after advancements.py; merges into en_us.json and tags)
"""
import json
import math
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import official_addons as oa  # noqa: E402  (pixel-art helpers)

ROOT = sys.argv[1]
RES = os.path.join(ROOT, "src/main/resources")
ASSETS = os.path.join(RES, "assets/femboyequipment")
DATA = os.path.join(RES, "data/femboyequipment")
NS = "femboyequipment"


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent="\t", ensure_ascii=False)
        f.write("\n")


def merge_tag(path, values):
    existing = json.load(open(path))["values"] if os.path.exists(path) else []
    write_json(path, {"replace": False, "values": existing + [v for v in values if v not in existing]})


class P:
    """Palette for oa.sprite: p primary, s secondary, a accent."""

    def __init__(self, p, s, a):
        self.ramps = dict(oa.BASE_RAMPS, p=oa.ramp(p), s=oa.ramp(s), a=oa.ramp(a))


def save(im, rel):
    path = os.path.join(ASSETS, "textures", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)


# ------------------------------------------------------------ item sprites
def ring(px, cx, cy, rx, ry, m, thick=1.0):
    for y in range(16):
        for x in range(16):
            d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
            if abs(math.sqrt(d) - 1.0) * min(rx, ry) <= thick * 0.75:
                px[(x, y)] = m(x, y) if callable(m) else m


def book():
    px = oa.grid(["", "..pppppppppp....", "..pwwwwwwwwwp...", "..pwwwwwwwwwp...", "..pwwsssswwwp...",
                  "..pwwsssswwwp...", "..pwwwwwwwwwp...", "..pwwwwwwwwwp...", "..pwwwwwwwwwp...", "..pwwwwwwwwwp...",
                  "..pwwwwwwwwwp...", "..pwwwwwwwwwp...", "..pppppppppppa..", "...........aa..."])
    heart = {}
    oa.heart(heart, 7.6, 7.2, 2.6, "a")
    px.update({k: v for k, v in heart.items() if px.get(k) == "w"})
    return px


def hats():
    out = {}
    # 1 Cutie Bow
    px = {}
    oa.bow(px, 7, 7, "p", "a")
    out["cutie_bow"] = (px, ((255, 150, 200), (255, 220, 235), (255, 240, 120)))
    # 2 Sweetheart Halo
    px = {}
    ring(px, 7.5, 6.5, 6.2, 2.6, "a", 1.2)
    oa.heart(px, 7.6, 11, 2.6, "p")
    out["sweetheart_halo"] = (px, ((255, 110, 170), (255, 255, 255), (255, 230, 120)))
    # 3 Darling Flower Crown
    px = {}
    ring(px, 7.5, 8.5, 6.2, 3.2, "s", 1.0)
    for k, (fx, fy) in enumerate(((2, 8), (5, 5), (8, 5), (11, 6), (13, 9), (8, 12), (4, 11))):
        oa.disk(px, fx, fy, 1.3, "pa"[k % 2])
    out["darling_flower_crown"] = (px, ((255, 160, 200), (110, 190, 90), (190, 160, 255)))
    # 4 Sparkle Star Circlet
    px = {}
    ring(px, 7.5, 9.5, 6.4, 2.8, "g", 1.0)
    oa.star(px, 7.5, 5.5, 4.4, 2.0, "p")
    px[(7, 5)] = "W"
    out["sparkle_star_circlet"] = (px, ((255, 225, 110), (255, 255, 255), (255, 255, 200)))
    # 5 Pastel Tiara
    px = oa.grid(["", "", "", "", ".......a........", "......ppp.......", "...a..pWp..a....", "..ppp.ppp.ppp...",
                  ".pppppppppppppp.", ".pssppsspppsspp.", ".pppppppppppppp."])
    out["pastel_tiara"] = (px, ((200, 200, 225), (190, 160, 255), (255, 150, 200)))
    # 6 Blåhaj Crown
    px = oa.grid(["", "", "", ".......p........", "......pp........", ".....ppp........", "....pppp........",
                  ".g..g..g..g..g..", ".ggggggggggggggg", ".gsgggsgggsgggs.", ".ggggggggggggggg"])
    out["blahaj_crown"] = (px, ((90, 140, 190), (120, 200, 255), (255, 255, 255)))
    # 7 Legendary Rainbow Halo
    rainbow = ["p", "g", "s", "a"]
    px = {}
    ring(px, 7.5, 7.5, 6.5, 3.0, lambda x, y: rainbow[(x // 3) % 4], 1.4)
    out["legendary_rainbow_halo"] = (px, ((240, 70, 90), (90, 210, 120), (110, 150, 255)))
    # 8 Ultimate Femboy Crown
    px = oa.grid(["", "", "..a....a....a...", "..g...ggg...g...", ".ggg..ggg..ggg..", ".ggg.ggggg.ggg..",
                  ".ggggggggggggg..", ".gpggggsggggpg..", ".ggggggggggggg..", ".ggggggggggggg..", "..ggggggggggg..."],
                 ox=1)
    out["ultimate_femboy_crown"] = (px, ((255, 110, 190), (130, 220, 255), (255, 255, 255)))
    return out


# ------------------------------------------------------------ head layers
def head_layer(colors, style):
    """64x32 armor texture: a band around the head (and a ring on top for halos)."""
    p, s, a = (oa.clamp(c) for c in colors)
    im = Image.new("RGBA", (64, 32))
    HEAD = oa.HEAD

    def put(x, y, c):
        im.putpixel((x, y), tuple(oa.clamp(c)) + (255,))
    rainbow = [(240, 70, 90), (255, 170, 60), (255, 230, 90), (90, 210, 120), (110, 150, 255), (180, 120, 255)]
    for side in ("front", "right", "left", "back"):
        x0, y0, w, h = HEAD[side]
        for dx in range(w):
            if style == "halo":
                continue
            for dy in range(3):
                c = s if dy == 1 else p
                if style == "flowers":
                    c = s if (dx + dy) % 3 else (a if dx % 2 else p)
                if style == "rainbow":
                    c = rainbow[(dx + dy) % 6]
                if style in ("crown", "tiara") and dy == 0 and dx % 3 == 1:
                    c = a
                put(x0 + dx, y0 + dy, c)
        if style == "bow" and side == "front":
            for dx, dy in ((2, 0), (3, 1), (5, 1), (6, 0), (2, 1), (6, 1), (4, 1)):
                put(x0 + dx - 1, y0 + dy, a if (dx, dy) == (4, 1) else p)
        if style == "star" and side == "front":
            for dx, dy in ((3, 0), (4, 0), (3, 1), (4, 1)):
                put(x0 + dx, y0 + dy, (255, 255, 255))
    x0, y0, w, h = HEAD["top"]
    for dx in range(w):
        for dy in range(h):
            edge = dx in (0, w - 1) or dy in (0, h - 1)
            if style in ("halo", "rainbow") and edge:
                put(x0 + dx, y0 + dy, rainbow[(dx + dy) % 6] if style == "rainbow" else a)
            elif style in ("crown", "tiara", "flowers", "bow", "star") and edge:
                put(x0 + dx, y0 + dy, p)
    if style == "halo":
        for dx, dy in ((3, 3), (4, 3), (3, 4), (4, 4)):
            put(x0 + dx, y0 + dy, p)
    return im


STYLES = {"cutie_bow": "bow", "sweetheart_halo": "halo", "darling_flower_crown": "flowers",
          "sparkle_star_circlet": "star", "pastel_tiara": "tiara", "blahaj_crown": "crown",
          "legendary_rainbow_halo": "rainbow", "ultimate_femboy_crown": "crown"}
NAMES = {"cutie_bow": "Cutie Bow", "sweetheart_halo": "Sweetheart Halo", "darling_flower_crown": "Darling Flower Crown",
         "sparkle_star_circlet": "Sparkle Star Circlet", "pastel_tiara": "Pastel Tiara", "blahaj_crown": "Blåhaj Crown",
         "legendary_rainbow_halo": "Legendary Rainbow Halo", "ultimate_femboy_crown": "Ultimate Femboy Crown"}


def main():
    lang = {}
    # book
    save(oa.sprite(book(), P((235, 110, 170), (255, 200, 225), (255, 90, 160))), "item/collection_book.png")
    write_json(f"{ASSETS}/models/item/collection_book.json", {"parent": "minecraft:item/generated",
                                                              "textures": {"layer0": f"{NS}:item/collection_book"}})
    write_json(f"{ASSETS}/items/collection_book.json", {"model": {"type": "minecraft:model", "model": f"{NS}:item/collection_book"}})
    lang[f"item.{NS}.collection_book"] = "Collection Book"
    write_json(f"{DATA}/recipe/collection_book.json", {"type": "minecraft:crafting_shapeless", "category": "misc",
                                                       "ingredients": ["minecraft:book", "minecraft:pink_dye"],
                                                       "result": {"count": 1, "id": f"{NS}:collection_book"}})
    # hats
    for name, (px, colors) in hats().items():
        px = {k: v for k, v in px.items() if 0 <= k[0] < 16 and 0 <= k[1] < 16}
        save(oa.sprite(px, P(*colors)), f"item/{name}.png")
        write_json(f"{ASSETS}/models/item/{name}.json", {"parent": "minecraft:item/generated",
                                                         "textures": {"layer0": f"{NS}:item/{name}"}})
        write_json(f"{ASSETS}/items/{name}.json", {"model": {"type": "minecraft:model", "model": f"{NS}:item/{name}"}})
        save(head_layer(colors, STYLES[name]), f"entity/equipment/humanoid/{name}.png")
        write_json(f"{ASSETS}/equipment/{name}.json", {"layers": {"humanoid": [{"texture": f"{NS}:{name}"}]}})
        lang[f"item.{NS}.{name}"] = NAMES[name]
    hat_ids = [f"{NS}:{n}" for n in NAMES]
    merge_tag(f"{RES}/data/trinkets/tags/item/head/hat.json", hat_ids)
    merge_tag(f"{RES}/data/minecraft/tags/item/head_armor.json", hat_ids)
    merge_tag(f"{DATA}/tags/item/collection_snacks.json", [f"{NS}:strawberry_milk"])
    merge_tag(f"{DATA}/tags/block/collection_ores.json", [])

    # ranks, screen, quests, toasts
    ranks = {"smol_bean": "Smol Bean", "cutie": "Cutie", "sweetheart": "Sweetheart", "darling": "Darling",
             "sparkle_star": "Sparkle Star", "pastel_prince": "Pastel Prince(ss)", "plushie_royalty": "Plushie Royalty",
             "femboy_legend": "Femboy Legend", "ultimate_femboy": "Ultimate Femboy"}
    for k, v in ranks.items():
        lang[f"rank.{NS}.{k}"] = v
    quests = {"snacks": "Eat %s cute snacks", "ores": "Mine %s addon ores", "craft": "Craft %s cute items",
              "place": "Place %s cute blocks", "capsules": "Open %s gacha capsules", "collect": "Collect %s new entries",
              "mobs": "Defeat %s mobs", "walk": "Walk %s blocks", "jump": "Do %s bunny hops (jumps!)",
              "fish": "Catch %s fish", "trade": "Trade with villagers (%s trades)", "sleep": "Sleep in a bed (%s nights, cozy~)"}
    for k, v in quests.items():
        lang[f"quest.{NS}.{k}"] = v
    C = f"collection.{NS}"
    lang.update({
        f"{C}.title": "Cute Collection",
        f"{C}.tab.collection": "Collection",
        f"{C}.tab.quests": "Quests",
        f"{C}.tab.ranks": "Ranks",
        f"{C}.loading": "Loading your collection...",
        f"{C}.total": "Total: %s / %s collected",
        f"{C}.collected": "✔ Collected!",
        f"{C}.missing": "✖ Not collected yet",
        f"{C}.points": "+%s Cute Points",
        f"{C}.daily": "Daily Quests (new ones in %s)",
        f"{C}.weekly": "Weekly Quests (new ones in %s)",
        f"{C}.reward.daily": "Reward: a capsule + 100 XP",
        f"{C}.reward.weekly": "Reward: 4 capsules + 500 XP",
        f"{C}.claim": "Claim!",
        f"{C}.claimed": "✔ Claimed",
        f"{C}.your_rank": "Your rank",
        f"{C}.cute_points": "%s / %s Cute Points",
        f"{C}.next_rank": "%s more points to %s",
        f"{C}.max_rank": "You reached the top! Ultimate cutie~",
        f"{C}.points_help": "Entry +1 · group goal +5 · full collection +25",
        f"{C}.rank_rewards": "Every rank: an exclusive hat, capsules, XP",
        f"{C}.rank_reward_line": "Rewards: %1$s, %2$s Blåhaj + %2$s fih capsules, %3$s XP levels",
        f"{C}.title_on": "My title: shown",
        f"{C}.title_off": "My title: hidden",
        f"{C}.toast.goal": "Group complete! ✿",
        f"{C}.toast.challenge": "Collection complete!! ★",
        f"{C}.toast.rank": "Rank up: %s!",
        f"{C}.toast.rank_reward": "New hat + capsules in your inventory~",
        f"{C}.toast.quest": "Quest complete! Claim it ♥",
        f"{C}.toast.claimed": "Quest reward claimed!",
        f"key.{NS}.collection": "Open Cute Collection",
        f"key.category.{NS}.main": "FemboyEquipment",
    })
    lang_path = f"{ASSETS}/lang/en_us.json"
    data = json.load(open(lang_path, encoding="utf-8"))
    data.update(lang)
    write_json(lang_path, data)
    print("collection done:", len(lang), "lang keys")


main()
