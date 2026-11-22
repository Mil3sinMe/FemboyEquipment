"""Generates the 30 official addons in official-addons/<theme>/ (see addon_themes.py).

Each addon is its own small Fabric mod (Gradle subproject) with exactly 100 items/blocks, its own creative tab,
102 advancements, worldgen ore, recipes, loot tables, tags, textures, models and lang.

Usage: python3 official_addons.py <repo root>   (needs Pillow; run ./gradlew build once first so Loom's
Minecraft client jar is cached, it is used for vanilla stair/wall blockstate templates)
"""
import json
import math
import os
import random
import re
import shutil
import sys
import zipfile

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from addon_themes import THEMES  # noqa: E402

ROOT = sys.argv[1]
OUT = os.path.join(ROOT, "official-addons")
CLIENT = zipfile.ZipFile(os.path.expanduser("~/.gradle/caches/fabric-loom/1.21.11/minecraft-client.jar"))
ADDON_VERSION = "1.0.0"
MIN_FE = "1.13.0"


# ============================================================ helpers
def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent="\t", ensure_ascii=False)
        f.write("\n")


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def slug(s):
    s = s.replace("å", "a").replace("é", "e").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def hx(h):
    return tuple(int(h[k:k + 2], 16) for k in (0, 2, 4))


def mix(a, b, t):
    return tuple(int(a[k] * (1 - t) + b[k] * t) for k in range(3))


def clamp(c):
    return tuple(max(0, min(255, int(v))) for v in c)


def ramp(rgb):
    """5 shades: dark outline .. highlight."""
    lum = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
    if lum < 60:  # very dark colors: lift the ramp so shading still shows
        return [clamp(mix(rgb, (0, 0, 0), 0.5)), rgb, clamp(mix(rgb, (255, 255, 255), 0.12)),
                clamp(mix(rgb, (255, 255, 255), 0.25)), clamp(mix(rgb, (255, 255, 255), 0.45))]
    return [clamp(tuple(v * f for v in rgb)) for f in (0.55, 0.75, 0.88, 1.0)] + [clamp(mix(rgb, (255, 255, 255), 0.5))]


BASE_RAMPS = {
    "h": [(50, 30, 25), (85, 55, 40), (115, 78, 55), (140, 100, 70), (170, 130, 95)],     # handle wood
    "o": [(110, 70, 35), (160, 110, 60), (195, 145, 85), (220, 175, 115), (240, 210, 160)],  # baked dough
    "w": [(150, 145, 160), (200, 196, 208), (232, 228, 238), (248, 246, 252), (255, 255, 255)],
    "k": [(10, 8, 12), (30, 24, 34), (48, 40, 54), (70, 60, 78), (100, 90, 110)],
    "g": [(120, 80, 20), (200, 140, 40), (240, 190, 60), (255, 220, 100), (255, 245, 180)],
    "x": [(60, 60, 66), (100, 100, 108), (140, 140, 148), (175, 175, 182), (210, 210, 216)],
}
FLAT = {"W": (255, 255, 255, 255), "E": (20, 20, 24, 255), "Y": (255, 250, 200, 255)}


class Pal:
    def __init__(self, t):
        self.p, self.s, self.a = hx(t["p"]), hx(t["s"]), hx(t["a"])
        self.ramps = dict(BASE_RAMPS, p=ramp(self.p), s=ramp(self.s), a=ramp(self.a))


def sprite(px, pal, size=16):
    """px: dict (x, y) -> material key. Outlines + simple top-left lighting."""
    R = pal.ramps
    solid = lambda x, y: (x, y) in px and px[(x, y)] not in FLAT  # noqa: E731
    im = Image.new("RGBA", (size, size))
    for y in range(size):
        for x in range(size):
            m = px.get((x, y))
            if m is None:
                for nx, ny in ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)):
                    if solid(nx, ny):
                        im.putpixel((x, y), R[px[(nx, ny)]][0] + (255,))
                        break
                continue
            if m in FLAT:
                im.putpixel((x, y), FLAT[m])
                continue
            up, left, down, right = solid(x, y - 1), solid(x - 1, y), solid(x, y + 1), solid(x + 1, y)
            shade = 4 if not up and not left else 3 if not up or not left else 1 if not down or not right else 2
            im.putpixel((x, y), R[m][shade] + (255,))
    return im


def grid(rows, mp=None, ox=0, oy=0):
    px = {}
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == ".":
                continue
            m = (mp or {}).get(ch, ch)
            if m:
                px[(x + ox, y + oy)] = m
    return px


def line(px, a, b, m, w=1):
    (x0, y0), (x1, y1) = a, b
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for k in range(n + 1):
        x, y = round(x0 + (x1 - x0) * k / n), round(y0 + (y1 - y0) * k / n)
        for d in range(w):
            px[(x + d, y)] = m


def disk(px, cx, cy, r, m, ry=None):
    ry = ry or r
    for y in range(16):
        for x in range(16):
            if ((x - cx) / r) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                px[(x, y)] = m(x, y) if callable(m) else m


def inside_poly(x, y, pts):
    c = False
    j = len(pts) - 1
    for k in range(len(pts)):
        xi, yi = pts[k]
        xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            c = not c
        j = k
    return c


def star_pts(cx, cy, r1, r2, n=5, rot=-math.pi / 2):
    return [(cx + (r1 if k % 2 == 0 else r2) * math.cos(rot + k * math.pi / n),
             cy + (r1 if k % 2 == 0 else r2) * math.sin(rot + k * math.pi / n)) for k in range(2 * n)]


def star(px, cx, cy, r1, r2, m):
    pts = star_pts(cx, cy, r1, r2)
    for y in range(16):
        for x in range(16):
            if inside_poly(x + 0.5, y + 0.5, pts):
                px[(x, y)] = m


def heart(px, cx, cy, s, m):
    for y in range(16):
        for x in range(16):
            u, v = (x + 0.5 - cx) / s, -(y + 0.5 - cy) / s
            if (u * u + v * v - 1) ** 3 - u * u * v ** 3 <= 0:
                px[(x, y)] = m


# ============================================================ item sprites
GEM = ["", "", "......pppp......", ".....ppWppp.....", "....ppWppppp....", "...pppppppppp...",
       "....pppppppp....", ".....pppppp.....", "......pppp......", ".......pp......."]
RAW = ["", "", "", ".....ppp........", "....ppppp.pp....", "...pppppppppp...", "...ppppxxppppp..",
       "..pppppxxpppp...", "..ppppppppppp...", "...ppppppppp....", "....ppp..pp....."]
NUGGET = ["", "", "", "", "", "......pp........", ".....pWpp.......", "....pppppp.pp...", "....pppppppppp..",
          ".....ppp.pppp...", "..........pp...."]
DUST = ["", "", "", "", "", "", "", ".......p........", "......ppp...p...", ".....ppWpp......", "..p.ppppppp.....",
        "...ppppppppp....", "..ppppppppppp..."]
SWORD = ["", ".............pp.", "............ppp.", "...........ppp..", "..........ppp...", ".........ppp....",
         "........ppp.....", ".......ppp......", "......ppp.......", "..ss.ppp........", "...ssppp........",
         "....sss.........", "....h.ss........", "...h............", "..h............."]
PICKAXE = ["", "....ppppp.......", "...ppppppaa.....", "....ppp..pp.....", "........hpppa...", ".......h.ss.pp..",
           "......h......pp.", ".....h.......pp.", "....h.........p.", "...h..........p.", "..h.............",
           ".h.............."]
HELMET = ["", "", "", "....pppppppp....", "...ppppppppppp..", "...pppWppppppp..", "...ppp....ppp...",
          "...pp......pp...", "...pp......pp..."]
CHEST = ["", "..ppp......ppp..", "..pppp....pppp..", "..pppppppppppp..", "...ppppWppppp...", "....pppsspppp...",
         "....pppppppp....", "....pppppppp....", "....pppppppp....", "....pppppppp....", "....pppppppp....",
         "....pppppppp...."]
LEGS = ["", "", "...ssssssssss...", "...pppppppppp...", "...pppp..pppp...", "...ppp....ppp...", "...ppp....ppp...",
        "...ppp....ppp...", "...ppp....ppp...", "...ppp....ppp...", "...ppp....ppp..."]
BOOTS = ["", "", "", "", "", "", "...ppp....ppp...", "...ppp....ppp...", "...sss....sss...", ".ppppp....ppppp.",
         ".ppppp....ppppp."]


def tool(kind):
    px = {}
    line(px, (2, 13), (10, 5), "h")
    if kind == "spear":
        line(px, (2, 13), (10, 5), "h")
        for p in ((11, 4), (12, 3), (13, 2), (12, 2), (13, 3), (11, 3), (12, 4), (14, 1)):
            px[p] = "p"
        px[(10, 6)] = px[(9, 5)] = "s"
        return px
    heads = {
        "axe": [(10, 1), (11, 1), (12, 1), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (9, 3), (10, 3), (11, 3),
                (12, 3), (13, 3), (12, 4), (13, 4), (13, 5), (11, 4)],
        "shovel": [(11, 1), (12, 1), (10, 2), (11, 2), (12, 2), (13, 2), (10, 3), (11, 3), (12, 3), (13, 3),
                   (11, 4), (12, 4)],
        "hoe": [(7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (11, 4)],
    }
    for p in heads[kind]:
        px[p] = "p"
    px[(11, 2)] = "a" if kind != "hoe" else "p"
    return px


def weapon(kind):
    px = {}
    if kind == "bat":
        for k in range(12):
            x, y = 2 + k, 13 - k
            width = 1 + k // 4
            for d in range(-width, width + 1):
                px[(x + d, y)] = "p" if d < width else "s"
        line(px, (1, 14), (3, 12), "h")
        px[(12, 3)] = "a"
    elif kind == "hammer":
        line(px, (2, 14), (9, 7), "h")
        for y in range(1, 8):
            for x in range(8, 15):
                if abs((x - 11) - (y - 4)) <= 3 and abs((x - 11) + (y - 4)) <= 5:
                    px[(x, y)] = "p"
        for k in range(-2, 3):
            px[(11 + k, 4 + k)] = "s"
    elif kind == "scythe":
        line(px, (3, 14), (11, 2), "h")
        for x in range(2, 12):
            y = 2 + int(((11 - x) / 9) ** 2 * 5)
            px[(x, y)] = "p"
            px[(x, y + 1)] = "p"
            px[(x, y - 1)] = "a" if x < 11 else "p"
    elif kind == "wand":
        line(px, (2, 14), (9, 7), "s")
        star(px, 11.5, 4.5, 4.2, 1.9, "a")
        px[(11, 4)] = "W"
        px[(2, 14)] = px[(3, 13)] = "p"
    return px


def food(slot):
    px = {}
    if slot == 0:  # soda bottle
        px = grid(["", "......oo........", "......ww........", ".....wwww.......", "....wwwwww......", "....wppppw......",
                   "....wpWppw......", "....wppppw......", "....wsssww......", "....wppppw......", "....wwwwww......"],
                  ox=2, oy=2)
    elif slot == 1:  # cookie
        disk(px, 7.5, 8, 5.5, "o")
        for p in ((6, 5), (9, 7), (5, 9), (8, 10), (10, 11), (4, 7), (11, 9)):
            px[p] = "p"
    elif slot == 2:  # cupcake
        px = grid(["", "", ".......a........", "......pap.......", ".....ppppp......", "....pppWppp.....",
                   "...ppppppppp....", "...ppppppppp....", "....sssssss.....", "....s.s.s.s.....", ".....sssss......",
                   ".....s.s.s......", "......sss......."], oy=1)
    elif slot == 3:  # wrapped candy
        disk(px, 7.5, 7.5, 3.6, lambda x, y: "w" if (x + y) % 3 == 0 else "p")
        for k in range(3):
            for d in range(-k, k + 1):
                px[(2 - k + 2, 7 + d)] = "s"
                px[(13 + k - 2, 7 + d)] = "s"
    elif slot == 4:  # soup bowl
        for y in range(7, 13):
            for x in range(2, 14):
                if ((x - 7.5) / 6) ** 2 + ((y - 7) / 6) ** 2 <= 1:
                    px[(x, y)] = "o"
        for x in range(3, 13):
            px[(x, 7)] = "p"
            px[(x, 6)] = "p" if 4 <= x <= 11 else px.get((x, 6))
        px = {k: v for k, v in px.items() if v}
        px[(6, 6)] = "a"
        px[(9, 6)] = "a"
    elif slot == 5:  # donut
        for y in range(16):
            for x in range(16):
                d = ((x - 7.5) ** 2 + (y - 8) ** 2) ** 0.5
                if 2.0 <= d <= 6.0:
                    px[(x, y)] = "p" if y < 9 or d < 4.5 else "o"
        for p in ((5, 4), (9, 3), (11, 6), (4, 7), (10, 9)):
            px[p] = "a" if p[0] % 2 else "s"
    elif slot == 6:  # popsicle
        for y in range(1, 11):
            for x in range(5, 11):
                if not (y == 1 and x in (5, 10)):
                    px[(x, y)] = "p" if y > 3 else "s"
        px[(6, 4)] = "W"
        for y in range(11, 15):
            px[(7, y)] = px[(8, y)] = "o"
    elif slot == 7:  # lollipop
        disk(px, 9.5, 5.5, 4.2, lambda x, y: "p" if int(math.atan2(y - 5.5, x - 9.5) * 2 + ((x - 9.5) ** 2 + (y - 5.5) ** 2) ** 0.5) % 2 else "w")
        line(px, (7, 9), (2, 14), "w")
    elif slot == 8:  # macaron
        disk(px, 7.5, 5.5, 5.5, "p", 2.4)
        disk(px, 7.5, 10.5, 5.5, "p", 2.4)
        for x in range(3, 13):
            px[(x, 8)] = "s"
    elif slot == 9:  # pie slice
        for y in range(16):
            for x in range(16):
                if inside_poly(x + 0.5, y + 0.5, [(2, 12), (14, 12), (14, 6), (3, 10)]) or (y in (12, 13) and 2 <= x <= 14):
                    px[(x, y)] = "o" if y >= 12 or x >= 13 or y <= 6 else "p"
        for x in range(4, 14, 3):
            px[(x, 11 - (x - 2) // 3)] = "o"
    elif slot == 10:  # steamed bun
        disk(px, 7.5, 9, 6, "w", 4.6)
        disk(px, 7.5, 6, 1.6, "p")
        px[(5, 9)] = px[(10, 9)] = "a"
    elif slot == 11:  # jelly
        for y in range(4, 12):
            for x in range(4, 12):
                if not (y == 4 and x in (4, 11)):
                    px[(x, y)] = "p"
        px[(5, 5)] = px[(6, 5)] = px[(5, 6)] = "W"
        for x in range(2, 14):
            px[(x, 12)] = "w"
        px[(8, 3)] = "a"
    return px


CHARMS = ["Ribbon Charm", "Heart Locket", "Bell Collar", "Star Pin", "Moon Pendant", "Bow Clip", "Friendship Bracelet",
          "Lucky Coin", "Anklet", "Earrings", "Bead Necklace", "Keychain"]


def bow(px, cx, cy, m, knot):
    for dx in range(-4, 5):
        for dy in range(-3, 4):
            if abs(dy) <= abs(dx) * 0.8 + 0.6 and abs(dx) >= 1:
                px[(cx + dx, cy + dy)] = m
    px[(cx, cy)] = knot
    px[(cx - 1, cy + 4)] = px[(cx + 1, cy + 4)] = m


def charm(slot):
    px = {}
    chain = lambda: [px.__setitem__((x, int(1 + ((x - 7.5) ** 2) / 12)), "g") for x in range(2, 14)]  # noqa: E731
    if slot == 0:
        bow(px, 7, 6, "p", "s")
        px[(5, 11)] = px[(9, 11)] = "p"
    elif slot == 1:
        chain()
        heart(px, 7.6, 9, 4.2, "g")
        heart(px, 7.6, 9, 3.0, "p")
    elif slot == 2:
        for x in range(1, 15):
            px[(x, 4)] = px[(x, 5)] = "s"
        disk(px, 7.5, 9, 3, "g")
        px[(7, 12)] = px[(8, 12)] = "k"
    elif slot == 3:
        star(px, 7.5, 7.5, 6.5, 2.9, "a")
        star(px, 7.5, 7.5, 3.5, 1.5, "p")
    elif slot == 4:
        chain()
        disk(px, 7.5, 9, 4.5, "p")
        for y in range(16):
            for x in range(16):
                if ((x - 9.5) ** 2 + (y - 7.8) ** 2) < 12:
                    px.pop((x, y), None)
    elif slot == 5:
        for x in range(1, 15):
            px[(x, 11)] = "x"
        bow(px, 7, 7, "p", "a")
    elif slot == 6:
        cols = "psa"
        for k in range(16):
            ang = k * math.pi * 2 / 16
            px[(round(7.5 + 5.5 * math.cos(ang)), round(7.5 + 4.5 * math.sin(ang)))] = cols[k % 3]
    elif slot == 7:
        disk(px, 7.5, 7.5, 6, "g")
        heart(px, 6.5, 6.5, 1.7, "p")
        heart(px, 9, 6.5, 1.7, "p")
        heart(px, 7.8, 9.2, 1.7, "p")
    elif slot == 8:
        for k in range(20):
            ang = k * math.pi * 2 / 20
            px[(round(7.5 + 6 * math.cos(ang)), round(9 + 3 * math.sin(ang)))] = "g"
        heart(px, 7.6, 13, 1.8, "p")
        px[(4, 11)] = px[(11, 11)] = "a"
    elif slot == 9:
        for cx in (4, 11):
            px[(cx, 2)] = px[(cx, 3)] = "g"
            disk(px, cx, 7, 2.2, "p", 3.2)
            px[(cx, 6)] = "W"
    elif slot == 10:
        for k in range(15):
            ang = math.pi * k / 14
            px[(round(7.5 + 6 * math.cos(ang)), round(3 + 9 * math.sin(ang)))] = "p" if k % 2 else "s"
        disk(px, 7.5, 12.5, 1.6, "a")
    elif slot == 11:
        for k in range(12):
            ang = k * math.pi * 2 / 12
            px[(round(4 + 2.5 * math.cos(ang)), round(4 + 2.5 * math.sin(ang)))] = "x"
        disk(px, 10, 10, 3.8, "p")
        px[(9, 9)] = px[(11, 9)] = "E"
        px[(7, 7)] = "x"
    return px


STICKERS = ["Heart", "Star", "Moon", "Flower", "Paw", "Bow", "Cloud", "Sparkle", "Smiley", "Music Note", "Crown",
            "Rainbow", "Butterfly", "Mushroom"]


def sticker(slot):
    px = {}
    if slot == 0:
        heart(px, 7.6, 8, 5.4, "p")
    elif slot == 1:
        star(px, 7.5, 8, 6.8, 3.0, "a")
    elif slot == 2:
        disk(px, 7.5, 7.5, 6, "a")
        for y in range(16):
            for x in range(16):
                if (x - 10.5) ** 2 + (y - 5.5) ** 2 < 22:
                    px.pop((x, y), None)
    elif slot == 3:
        for k in range(5):
            ang = k * 2 * math.pi / 5 - math.pi / 2
            disk(px, 7.5 + 3.4 * math.cos(ang), 7.5 + 3.4 * math.sin(ang), 2.6, "p")
        disk(px, 7.5, 7.5, 1.8, "a")
    elif slot == 4:
        disk(px, 7.5, 10, 3.6, "p", 3)
        for cx, cy in ((3.5, 5.5), (6, 3.5), (9, 3.5), (11.5, 5.5)):
            disk(px, cx, cy, 1.4, "p")
    elif slot == 5:
        bow(px, 7, 7, "p", "s")
    elif slot == 6:
        for cx, cy, r in ((5, 9, 3.2), (8.5, 7, 4), (11.5, 9.5, 2.8)):
            disk(px, cx, cy, r, "w")
        for x in range(3, 13):
            px[(x, 11)] = "w"
        px[(6, 8)] = px[(10, 8)] = "E"
    elif slot == 7:
        star(px, 7.5, 7.5, 7, 1.6, "a")
        px[(7, 7)] = "W"
    elif slot == 8:
        disk(px, 7.5, 7.5, 6, "a")
        px[(5, 5)] = px[(5, 6)] = px[(10, 5)] = px[(10, 6)] = "E"
        for x in range(5, 11):
            px[(x, 10 if 6 <= x <= 9 else 9)] = "E"
    elif slot == 9:
        disk(px, 5, 11, 2.2, "p", 1.7)
        disk(px, 11, 10, 2.2, "p", 1.7)
        for y in range(3, 11):
            px[(6, y)] = "p"
        for y in range(2, 10):
            px[(12, y)] = "p"
        line(px, (6, 3), (12, 2), "p")
        line(px, (6, 4), (12, 3), "p")
    elif slot == 10:
        for y in range(6, 12):
            for x in range(2, 14):
                px[(x, y)] = "g"
        for cx in (2, 7, 13):
            for y in range(2, 6):
                if abs(y - 5) <= 3:
                    px[(cx, y)] = px[(cx + (1 if cx < 13 else -1), y + 1)] = "g"
        px[(5, 8)] = "p"
        px[(8, 8)] = "a"
        px[(11, 8)] = "s"
    elif slot == 11:
        cols = ["p", "s", "a", "p"]
        for y in range(16):
            for x in range(16):
                d = ((x - 7.5) ** 2 + (y - 12) ** 2) ** 0.5
                if 3 <= d <= 7 and y <= 12:
                    px[(x, y)] = cols[min(3, int(7 - d))]
    elif slot == 12:
        for sx in (-1, 1):
            disk(px, 7.5 + sx * 3.5, 5.5, 3, "p")
            disk(px, 7.5 + sx * 3, 10, 2.2, "s")
        for y in range(4, 13):
            px[(7, y)] = px[(8, y)] = "k"
    elif slot == 13:
        disk(px, 7.5, 6.5, 6, lambda x, y: "W" if (x, y) in ((5, 4), (9, 3), (10, 6), (4, 7)) else "p", 4)
        for y in range(16):
            for x in range(16):
                if y > 7:
                    px.pop((x, y), None)
        for y in range(8, 14):
            for x in range(6, 10):
                px[(x, y)] = "w"
    return px


def sticker_image(px, pal):
    """Sticker: the shape with a thick white die-cut border and a faint shadow."""
    im = sprite(px, pal)
    out = Image.new("RGBA", (16, 16))
    border = set()
    for (x, y) in px:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                border.add((x + dx, y + dy))
    for (x, y) in border:
        if 0 <= x < 16 and 0 <= y < 16:
            if (x, y + 1) not in border and y + 1 < 16:
                out.putpixel((x, y + 1), (120, 110, 130, 255))
            out.putpixel((x, y), (255, 255, 255, 255))
    for (x, y) in px:
        if 0 <= x < 16 and 0 <= y < 16:
            out.putpixel((x, y), im.getpixel((x, y)))
    return out


# ============================================================ block textures
def noise_tex(base_fn, seed):
    rnd = random.Random(seed)
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            c = base_fn(x, y, rnd)
            im.putpixel((x, y), clamp(c) + (255,))
    return im


def stone_base(x, y, rnd, deep=False):
    g = [(116, 116, 116), (128, 128, 128), (140, 140, 140), (104, 104, 104)] if not deep else \
        [(70, 70, 76), (80, 80, 86), (60, 60, 66), (90, 90, 96)]
    return g[(x * 7 + y * 13 + rnd.randint(0, 3)) % 4]


def ore(pal, seed, deep):
    R = pal.ramps["p"]
    rnd = random.Random(seed)
    spots = [(3, 3), (10, 2), (12, 9), (5, 10), (8, 6), (2, 13), (11, 13)]
    gem = set()
    for (cx, cy) in spots:
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            if rnd.random() < 0.85:
                gem.add((cx + dx, cy + dy))

    def f(x, y, r):
        if (x, y) in gem:
            return R[4] if (x - 1, y) not in gem and (x, y - 1) not in gem else R[2] if (x + 1, y) in gem else R[1]
        return stone_base(x, y, r, deep)
    return noise_tex(f, seed)


def faceted(pal, seed, key="p"):
    R = pal.ramps[key]

    def f(x, y, r):
        if x in (0, 15) or y in (0, 15):
            return R[1] if x == 15 or y == 15 else R[4]
        facet = ((x // 4) + (y // 4) * 3) % 5
        s = [2, 3, 4, 3, 1][facet]
        if (x + y) % 7 == 0:
            s = 4
        return tuple(v * (1 + r.uniform(-0.04, 0.04)) for v in R[s])
    return noise_tex(f, seed)


def raw_block(pal, seed):
    R = pal.ramps["p"]
    return noise_tex(lambda x, y, r: R[[1, 2, 2, 3, 3, 1, 4][(x * 3 + y * 5 + r.randint(0, 6)) % 7]]
                     if r.random() > 0.1 else BASE_RAMPS["x"][2], seed)


def bricks(pal, seed, key="p", mortar_key="s"):
    R = pal.ramps[key]
    mortar = [mix(pal.ramps[mortar_key][4], (255, 255, 255), 0.3), pal.ramps[mortar_key][3]]
    rnd = random.Random(seed)
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            im.putpixel((x, y), clamp(mortar[(x + y) % 2]) + (255,))
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
                        im.putpixel((x, y), R[s] + (255,))
    return im


def tiles(pal, seed):
    P, S = pal.ramps["p"], pal.ramps["s"]

    def f(x, y, r):
        lx, ly = x % 8, y % 8
        if lx == 7 or ly == 7:
            return S[1]
        if lx == 0 or ly == 0:
            return P[4]
        checker = ((x // 8) + (y // 8)) % 2
        return (P if checker else S)[3 if (lx + ly) % 5 else 2]
    return noise_tex(f, seed)


def polished(pal, seed):
    P = pal.ramps["p"]

    def f(x, y, r):
        if x == 0 or y == 0:
            return P[4]
        if x == 15 or y == 15:
            return P[1]
        if x == 1 or y == 1:
            return P[3]
        return tuple(v * (1 + r.uniform(-0.025, 0.025)) for v in P[3 if (x + y) % 11 else 4])
    return noise_tex(f, seed)


def cobbled(pal, seed):
    P = pal.ramps["p"]
    rnd = random.Random(seed)
    pts = [(rnd.uniform(0, 16), rnd.uniform(0, 16), rnd.choice([2, 3, 3, 4])) for _ in range(9)]

    def f(x, y, r):
        best = sorted(((min(abs(x - px_), 16 - abs(x - px_)) ** 2 + min(abs(y - py_), 16 - abs(y - py_)) ** 2, s)
                       for px_, py_, s in pts))
        if best[1][0] - best[0][0] < 6:
            return P[0]
        return P[best[0][1]]
    return noise_tex(f, seed)


def mosaic(pal, seed):
    cols = [pal.ramps["p"][3], pal.ramps["s"][3], pal.ramps["a"][3], pal.ramps["p"][2], pal.ramps["s"][4]]
    rnd = random.Random(seed)
    cell = {(cx, cy): rnd.choice(cols) for cx in range(8) for cy in range(8)}

    def f(x, y, r):
        if x % 2 == 1 and y % 2 == 1:
            return mix(cell[(x // 2, y // 2)], (40, 40, 40), 0.35)
        return cell[(x // 2, y // 2)]
    return noise_tex(f, seed)


def lamp(pal, seed):
    A, P = pal.ramps["a"], pal.ramps["p"]

    def f(x, y, r):
        if x in (0, 15) or y in (0, 15):
            return P[1]
        if x in (1, 14) or y in (1, 14):
            return P[3]
        d = ((x - 7.5) ** 2 + (y - 7.5) ** 2) ** 0.5
        return mix(A[4], (255, 255, 240), max(0.0, 1 - d / 6))
    return noise_tex(f, seed)


def cushion(pal, seed):
    S, P = pal.ramps["s"], pal.ramps["p"]

    def f(x, y, r):
        u, v = (x + y) % 8, (x - y) % 8
        if (x % 8 == 4 and y % 8 == 4) or (x % 8 == 0 and y % 8 == 0):
            return P[1]
        if u == 0 or v == 0:
            return S[2]
        return S[3 if (u + v) % 3 else 4]
    return noise_tex(f, seed)


def crate(pal, seed):
    H, P = BASE_RAMPS["o"], pal.ramps["p"]

    def f(x, y, r):
        if x in (0, 15) or y in (0, 15) or x in (1, 14) or y in (1, 14):
            return P[2] if (x + y) % 2 else P[3]
        if abs(x - y) <= 1:
            return H[1]
        return H[2 if y % 4 == 0 else 3]
    return noise_tex(f, seed)


def pillar(pal, seed):
    P = pal.ramps["p"]

    def f(x, y, r):
        if y in (0, 1, 14, 15):
            return P[4] if y in (0, 14) else P[1]
        return P[[1, 3, 4, 3][x % 4]]
    return noise_tex(f, seed)


def chiseled(pal, seed):
    P, A = pal.ramps["p"], pal.ramps["a"]
    hp = {}
    heart(hp, 7.9, 8, 3.8, "x")

    def f(x, y, r):
        if x in (0, 15) or y in (0, 15):
            return P[1]
        if x in (1, 14) or y in (1, 14):
            return P[4]
        if (x, y) in hp:
            return A[3] if (x - 1, y - 1) in hp else A[4]
        return P[3]
    return noise_tex(f, seed)


def shingles(pal, seed):
    P = pal.ramps["p"]

    def f(x, y, r):
        row = y // 4
        lx = (x + (2 if row % 2 else 0)) % 4
        ly = y % 4
        if ly == 3 or (lx == 0 and ly >= 1):
            return P[1]
        return P[4 if ly == 0 else 3 if ly == 1 else 2]
    return noise_tex(f, seed)


def quilt(pal, seed):
    cols = [pal.ramps["p"], pal.ramps["s"], pal.ramps["a"]]
    rnd = random.Random(seed)
    patch = {(cx, cy): rnd.randrange(3) for cx in range(4) for cy in range(4)}

    def f(x, y, r):
        R = cols[patch[(x // 4, y // 4)]]
        if (x % 4 == 0 or y % 4 == 0) and (x + y) % 2 == 0:
            return (255, 250, 245)
        return R[3 if (x + y) % 3 else 4]
    return noise_tex(f, seed)


def glazed(pal, seed):
    P, S = pal.ramps["p"], pal.ramps["s"]

    def f(x, y, r):
        ang = math.atan2(y - 7.5, x - 7.5)
        d = ((x - 7.5) ** 2 + (y - 7.5) ** 2) ** 0.5
        band = int((ang / math.pi * 2 + d / 2.5) * 1.0) % 3
        return [P[4], S[3], P[2]][band]
    return noise_tex(f, seed)


def starry(pal, seed):
    dark = mix(pal.p, (10, 10, 30), 0.75)
    rnd = random.Random(seed)
    stars = {(rnd.randrange(16), rnd.randrange(16)) for _ in range(9)}

    def f(x, y, r):
        if (x, y) in stars:
            return (255, 250, 210)
        if any((x + dx, y) in stars or (x, y + dx) in stars for dx in (-1, 1)):
            return mix(dark, pal.a, 0.5)
        return tuple(v * (1 + r.uniform(-0.08, 0.08)) for v in dark)
    return noise_tex(f, seed)


def sparkling(pal, seed):
    P = pal.ramps["p"]

    def f(x, y, r):
        v = r.random()
        if v < 0.07:
            return (255, 255, 255)
        if v < 0.15:
            return P[4]
        return P[2 + ((x * 5 + y * 3) % 2)]
    return noise_tex(f, seed)


# ============================================================ armor + plushie textures
def faces(u, v, w, h, d):
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + d + w + d, v + d, w, h)}


HEAD, BODY, ARM, LEG = faces(0, 0, 8, 8, 8), faces(16, 16, 8, 12, 4), faces(40, 16, 4, 12, 4), faces(0, 16, 4, 12, 4)


def armor_layers(pal):
    P, S = pal.ramps["p"], pal.ramps["s"]

    def paint(im, rect, fn):
        x0, y0, w, h = rect
        for dy in range(h):
            for dx in range(w):
                c = fn(dx, dy, w, h)
                if c is not None:
                    im.putpixel((x0 + dx, y0 + dy), c + (255,))

    def plate(dx, dy, w, h):
        if dy == 0 or dx == 0:
            return P[4]
        if dy == h - 1 or dx == w - 1:
            return S[2]
        return P[3] if (dx + dy) % 4 == 0 else P[2]

    main = Image.new("RGBA", (64, 32))
    for side, rect in HEAD.items():
        if side == "front":
            paint(main, rect, lambda x, y, w, h: None if (2 <= x <= 5 and 3 <= y <= 6) else plate(x, y, w, h))
        elif side != "bottom":
            paint(main, rect, plate)
    for rect in BODY.values():
        paint(main, rect, plate)
    for rect in ARM.values():
        paint(main, rect, lambda x, y, w, h: plate(x, y, w, h) if y <= 8 else None)
    for side, rect in LEG.items():
        paint(main, rect, lambda x, y, w, h: plate(x, y, w, h) if y >= 8 or side == "bottom" else None)
    legs = Image.new("RGBA", (64, 32))
    for side in ("right", "front", "left", "back"):
        paint(legs, BODY[side], lambda x, y, w, h: plate(x, y, w, h) if y >= 8 else None)
        paint(legs, LEG[side], lambda x, y, w, h: plate(x, y, w, h) if y <= 9 else None)
    paint(legs, BODY["bottom"], plate)
    return main, legs


WHITE_P = (246, 242, 240)


def blahaj_tex(colors, seed, sparkle):
    """Same UV layout as FemboyEquipment's blahaj_base model (32x32)."""
    rnd = random.Random(seed)
    im = Image.new("RGBA", (32, 32))

    def px(x, y, c, n=0.06):
        im.putpixel((x, y), clamp(tuple(v * (1 + rnd.uniform(-n, n)) for v in c)) + (255,))

    def stripes(n):
        return [colors[min(len(colors) - 1, k * len(colors) // n)] for k in range(n)]
    rows, top, erows = stripes(10), stripes(16), stripes(5)
    for y in range(16):
        for x in range(16):
            px(x, y, rows[y] if y < 10 else WHITE_P)
            px(16 + x, y, tuple(v * 1.05 for v in top[x]))
            px(x, 16 + y, WHITE_P)
    for y in range(8):
        for x in range(8):
            px(16 + x, 16 + y, tuple(v * 0.82 for v in colors[0]))
            px(24 + x, 16 + y, erows[y] if y < 5 else WHITE_P)
            px(16 + x, 24 + y, rows[min(9, y * 10 // 8)])
            c = erows[y] if y < 4 else WHITE_P
            if y == 5 and 1 <= x <= 6:
                c = (232, 130, 150)
            px(24 + x, 24 + y, c, 0.03)
    for x, y in ((26, 18), (26, 19), (27, 18), (27, 19)):
        im.putpixel((x, y), (24, 20, 28, 255))
    im.putpixel((26, 18), (230, 230, 240, 255))
    for x in (26, 28, 30):
        im.putpixel((x, 29), (255, 255, 255, 255))
    if sparkle:
        for x, y in ((19, 3), (26, 9), (4, 2), (12, 6), (29, 5), (8, 11)):
            im.putpixel((x, y), (255, 255, 240, 255))
    return im


def fih_tex(body, back, belly, canvas, sole, seed, sparkle):
    """Same UV layout as FemboyEquipment's fih_base model (32x32)."""
    rnd = random.Random(seed)
    im = Image.new("RGBA", (32, 32))

    def px(x, y, c, n=0.05):
        im.putpixel((x, y), clamp(tuple(v * (1 + rnd.uniform(-n, n)) for v in c)) + (255,))
    W = (255, 255, 255)
    for y in range(16):  # fish side
        for x in range(16):
            c = back if y < 3 else belly if y >= 12 else body
            if 3 <= y < 12 and (x + (y % 2) * 2) % 4 == 0:
                c = mix(c, W, 0.3)
            if sparkle and rnd.random() < 0.06:
                c = (255, 255, 235)
            px(x, y, c)
    for y in range(8):  # top strip
        for x in range(16):
            px(16 + x, y, back)
    for y in range(8):  # head side + front
        for x in range(8):
            px(16 + x, 8 + y, back if y < 2 else belly if y >= 6 else body)
            px(24 + x, 8 + y, mix(body, (0, 0, 0), 0.5) if y == 5 and 2 <= x <= 5 else body if y < 5 else belly)
    for (dx, dy, c) in ((3, 2, W), (4, 2, W), (3, 3, W), (4, 3, (20, 20, 24)), (2, 2, W), (2, 3, W)):
        im.putpixel((16 + dx, 8 + dy), c + (255,))
    fin = mix(back, body, 0.4)
    for y in range(8):
        for x in range(8):
            px(x, 16 + y, mix(fin, (0, 0, 0), 0.15) if x % 2 == 0 else fin)
    for y in range(8):  # shoe side (16x8) + top (8x8)
        for x in range(16):
            c = sole if y >= 6 else mix(sole, (0, 0, 0), 0.2) if y == 5 else sole if x < 3 else canvas
            px(8 + x, 16 + y, c, 0.03)
        for x in range(8):
            px(24 + x, 16 + y, W if (y % 2 == 0 and 1 <= x <= 6) else canvas, 0.03)
    for y in range(8):  # ankle, sole, toe
        for x in range(16):
            c = (200, 200, 205) if x in (2, 13) and y % 3 == 1 else mix(canvas, W, 0.4) if y == 0 else canvas
            px(x, 24 + y, c, 0.03)
        for x in range(8):
            px(16 + x, 24 + y, mix(sole, (0, 0, 0), 0.15) if (x + y) % 3 == 0 else sole, 0.03)
            px(24 + x, 24 + y, W if y in (4, 5) and 1 <= x <= 6 else sole if y >= 2 else canvas, 0.03)
    return im


def background(pal, seed):
    rnd = random.Random(seed)
    base, accent = pal.ramps["p"][3], pal.ramps["p"][4]
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            c = accent if (x + y) % 8 == 0 or (x - y) % 8 == 0 else base
            im.putpixel((x, y), clamp(tuple(v * (1 + rnd.uniform(-0.04, 0.04)) for v in c)) + (255,))
    return im


# ============================================================ content
BENEFITS = ["SPEED", "REGENERATION", "JUMP_BOOST", "HASTE", "NIGHT_VISION", "ABSORPTION", "LUCK", "FIRE_RESISTANCE",
            "WATER_BREATHING", "SLOW_FALLING", "RESISTANCE", "STRENGTH", "DOLPHINS_GRACE", "HEALTH_BOOST",
            "CONDUIT_POWER", "HERO_OF_THE_VILLAGE"]
FOOD_NOUNS = ["Soda", "Cookie", "Cupcake", "Candy", "Soup", "Donut", "Popsicle", "Lollipop", "Macaron", "Pie", "Bun",
              "Jelly"]
# (nutrition, saturation, effect seconds, recipe ingredients besides the dust, count)
FOOD_STATS = [(3, 0.6, 30, ["minecraft:glass_bottle", "minecraft:sugar"], 1),
              (2, 0.2, 10, ["minecraft:wheat", "minecraft:wheat"], 4),
              (5, 0.6, 30, ["minecraft:wheat", "minecraft:egg", "minecraft:sugar"], 2),
              (2, 0.1, 10, ["minecraft:sugar", "minecraft:sugar"], 4),
              (7, 0.7, 45, ["minecraft:bowl", "minecraft:carrot"], 1),
              (5, 0.5, 30, ["minecraft:bread", "minecraft:sugar"], 2),
              (3, 0.3, 20, ["minecraft:stick", "minecraft:snowball"], 1),
              (2, 0.3, 20, ["minecraft:stick", "minecraft:sugar"], 1),
              (4, 0.4, 20, ["minecraft:egg", "minecraft:sugar", "minecraft:sugar"], 2),
              (8, 0.6, 60, ["minecraft:wheat", "minecraft:egg", "minecraft:apple"], 1),
              (6, 0.8, 30, ["minecraft:bread"], 1),
              (3, 0.4, 20, ["minecraft:sugar", "minecraft:apple"], 2)]
CHARM_ITEMS = ["minecraft:string", "minecraft:gold_ingot", "minecraft:iron_ingot", "minecraft:glowstone_dust",
               "minecraft:amethyst_shard", "minecraft:feather", "minecraft:leather", "minecraft:emerald",
               "minecraft:rabbit_hide", "minecraft:copper_ingot", "minecraft:prismarine_shard", "minecraft:lapis_lazuli"]
DYES = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple",
        "blue", "brown", "green"]
WOOLS = ["light_blue", "pink", "white", "purple", "yellow"]
TIERS = {
    1: dict(incorrect="INCORRECT_FOR_IRON_TOOL", dur=650, speed=7.0, attack=2.5, ench=16, armor_dur=22,
            defense=(2, 5, 6, 2), armor_ench=16, sound="ARMOR_EQUIP_IRON", tough=0.5, kb=0.0, needs="needs_stone_tool"),
    2: dict(incorrect="INCORRECT_FOR_DIAMOND_TOOL", dur=1600, speed=8.5, attack=3.0, ench=18, armor_dur=33,
            defense=(3, 6, 8, 3), armor_ench=18, sound="ARMOR_EQUIP_DIAMOND", tough=2.0, kb=0.0, needs="needs_iron_tool"),
    3: dict(incorrect="INCORRECT_FOR_NETHERITE_TOOL", dur=2100, speed=9.5, attack=4.0, ench=20, armor_dur=37,
            defense=(3, 6, 8, 3), armor_ench=20, sound="ARMOR_EQUIP_NETHERITE", tough=3.0, kb=0.1, needs="needs_iron_tool"),
}
WEAPON_KINDS = [("bat", 4.0, -3.0, 2.5, "WOOL_HIT", "UNCOMMON"), ("hammer", 6.0, -3.3, 3.5, "ANVIL_LAND", "RARE"),
                ("scythe", 5.0, -2.8, 1.5, "CHAIN_HIT", "RARE"), ("wand", 2.0, -2.0, 4.0, "AMETHYST_BLOCK_CHIME", "EPIC")]


class Entry:
    def __init__(self, id, name, cat, kind, java=None, tex=None, **kw):
        self.id, self.name, self.cat, self.kind, self.java, self.tex = id, name, cat, kind, java, tex
        self.__dict__.update(kw)


def camel(s):
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def build(t, index):
    m, M, S = t["mat"], t["mat_name"], t["short"]
    s = slug(S)
    sound = f"SoundType.{t['sound']}"
    color = f"MapColor.{t['map']}"
    C = []
    add = lambda *a, **k: C.append(Entry(*a, **k))  # noqa: E731

    # materials (4)
    add(m, M, "materials", "item", f'k.item("{m}")', ("gem",))
    add(f"raw_{m}", f"Raw {M}", "materials", "item", f'k.item("raw_{m}")', ("raw",))
    add(f"{m}_nugget", f"{M} Nugget", "materials", "item", f'k.item("{m}_nugget")', ("nugget",))
    add(f"{m}_dust", f"{M} Dust", "materials", "item", f'k.item("{m}_dust")', ("dust",))
    # ores + storage (4)
    add(f"{m}_ore", f"{M} Ore", "building", "cube", f'k.cube("{m}_ore", MapColor.STONE, 3.0F, SoundType.STONE, 0, true)',
        ("ore", False), tool="pickaxe", needs=True)
    add(f"deepslate_{m}_ore", f"Deepslate {M} Ore", "building", "cube",
        f'k.cube("deepslate_{m}_ore", MapColor.DEEPSLATE, 4.5F, SoundType.DEEPSLATE, 0, true)', ("ore", True),
        tool="pickaxe", needs=True)
    add(f"{m}_block", f"Block of {M}", "building", "cube", f'k.cube("{m}_block", {color}, 5.0F, {sound}, 0, true)',
        ("faceted",), tool="pickaxe", needs=True)
    add(f"raw_{m}_block", f"Block of Raw {M}", "building", "cube",
        f'k.cube("raw_{m}_block", {color}, 5.0F, SoundType.STONE, 0, true)', ("raw_block",), tool="pickaxe", needs=True)
    # decor families (5 x 4)
    for fam, base, name, prefix in (("bricks", f"{m}_bricks", f"{M} Bricks", f"{m}_brick"),
                                    ("tiles", f"{m}_tiles", f"{M} Tiles", f"{m}_tile"),
                                    ("polished", f"polished_{m}", f"Polished {M}", f"polished_{m}"),
                                    ("cobbled", f"cobbled_{m}", f"Cobbled {M}", f"cobbled_{m}"),
                                    ("mosaic", f"{m}_mosaic", f"{M} Mosaic", f"{m}_mosaic")):
        add(base, name, "building", "cube",
            f'k.cube("{base}", {color}, 2.0F, {sound}, 0, true)', (fam,), tool="pickaxe", family=fam, prefix=prefix)
        C[-1].java_after = f'k.shapes("{prefix}", {camel(base)});'
        pname = name[:-1] if name.endswith("Bricks") or name.endswith("Tiles") else name
        for shp in ("stairs", "slab", "wall"):
            add(f"{prefix}_{shp}", f"{pname} {shp.capitalize()}", "building", shp, None, None, tool="pickaxe", base=base)
    # 10 fun blocks
    for bid, name, tex, snd, strength, light, needs, tl in (
            (f"{m}_lamp", f"{M} Lamp", "lamp", "SoundType.GLASS", 0.3, 15, False, "pickaxe"),
            (f"{s}_cushion", f"{S} Cushion", "cushion", "SoundType.WOOL", 0.8, 0, False, None),
            (f"{s}_crate", f"{S} Crate", "crate", "SoundType.WOOD", 2.0, 0, False, "axe"),
            (f"{m}_pillar", f"{M} Pillar", "pillar", sound, 2.0, 0, True, "pickaxe"),
            (f"chiseled_{m}", f"Chiseled {M}", "chiseled", sound, 2.0, 0, True, "pickaxe"),
            (f"{m}_shingles", f"{M} Shingles", "shingles", sound, 2.0, 0, True, "pickaxe"),
            (f"{s}_quilt_block", f"{S} Quilt Block", "quilt", "SoundType.WOOL", 0.8, 0, False, None),
            (f"glazed_{m}", f"Glazed {M}", "glazed", sound, 1.4, 0, True, "pickaxe"),
            (f"starry_{m}", f"Starry {M}", "starry", sound, 2.0, 6, True, "pickaxe"),
            (f"sparkling_{m}", f"Sparkling {M}", "sparkling", "SoundType.AMETHYST", 2.0, 10, True, "pickaxe")):
        add(bid, name, "building", "cube", f'k.cube("{bid}", {color}, {strength}F, {snd}, {light}, {str(needs).lower()})',
            (tex,), tool=tl, fun=tex)
    # tools (6)
    for kind in ("sword", "pickaxe", "axe", "shovel", "hoe", "spear"):
        add(f"{m}_{kind}", f"{M} {kind.capitalize()}", "tools", "handheld", f'k.{kind}("{m}_{kind}", tools)', ("tool", kind),
            tool_kind=kind)
    # weapons (4)
    for (kind, dmg, spd, kb, snd, rar), wname in zip(WEAPON_KINDS, t["weapons"]):
        wid = slug(wname)
        add(wid, wname, "weapons", "handheld",
            f'k.knockbackWeapon("{wid}", tools, {dmg}F, {spd}F, {kb}F, SoundEvents.{snd}, Rarity.{rar})', ("weapon", kind),
            weapon_kind=kind)
    # armor (4)
    for piece, typ in (("helmet", "HELMET"), ("chestplate", "CHESTPLATE"), ("leggings", "LEGGINGS"), ("boots", "BOOTS")):
        add(f"{m}_{piece}", f"{M} {piece.capitalize()}", "armor", "item", f'k.armor("{m}_{piece}", armor, ArmorType.{typ})',
            ("armor", piece), piece=piece)
    # food (12)
    for k, noun in enumerate(FOOD_NOUNS):
        flavor = t["flavors"][k % 3]
        fname = f"{flavor} {noun}"
        fid = slug(fname)
        nut, sat, secs, _, _ = FOOD_STATS[k]
        eff = BENEFITS[(index * 5 + k) % len(BENEFITS)]
        amp = 1 if k in (4, 9) else 0
        add(fid, fname, "food", "item",
            f'k.food("{fid}", {nut}, {sat}F, {str(k == 0).lower()}, new MobEffectInstance(MobEffects.{eff}, {secs * 20}, {amp}))',
            ("food", k), slot=k, effect=eff)
    # charms (12)
    for k, cname in enumerate(CHARMS):
        cid = f"{s}_{slug(cname)}"
        eff = BENEFITS[(index * 3 + k) % len(BENEFITS)]
        rar = "RARE" if k in (1, 7) else "UNCOMMON"
        add(cid, f"{S} {cname}", "charms", "item", f'k.charm("{cid}", Rarity.{rar}, OutfitEffect.of(MobEffects.{eff}, 0))',
            ("charm", k), slot=k, effect=eff)
    # plushies (10)
    for k, adj in enumerate(t["adj"]):
        bid = f"{slug(adj)}_{s}_blahaj"
        add(bid, f"{adj} {S} Blåhaj", "plushies", "blahaj", f'k.blahaj("{bid}", {7 if k == 4 else 0})', ("blahaj", k),
            slot=k)
    for k, adj in enumerate(t["adj"]):
        fid = f"{slug(adj)}_{s}_fih"
        add(fid, f"{adj} {S} Fih", "plushies", "fih", f'k.fih("{fid}", {7 if k == 4 else 0})', ("fih", k), slot=k)
    # stickers (14)
    for k, kind in enumerate(STICKERS):
        sid = f"{s}_{slug(kind)}_sticker"
        add(sid, f"{S} {kind} Sticker", "stickers", "item", f'k.item("{sid}")', ("sticker", k), slot=k)

    ids = [e.id for e in C]
    assert len(C) == 100, (t["id"], len(C))
    assert len(set(ids)) == 100, (t["id"], [x for x in ids if ids.count(x) > 1])
    return C


# ============================================================ writers
def item_model(ns, e):
    if e.kind in ("item", "handheld"):
        parent = "minecraft:item/handheld" if e.kind == "handheld" else "minecraft:item/generated"
        return {"parent": parent, "textures": {"layer0": f"{ns}:item/{e.id}"}}
    return None


def vanilla_states(vanilla, ns, ours):
    text = CLIENT.read(f"assets/minecraft/blockstates/{vanilla}.json").decode()
    return json.loads(text.replace(f"minecraft:block/{vanilla}", f"{ns}:block/{ours}"))


def facing_states(ns, name):
    return {"variants": {f"facing={f}": dict({"model": f"{ns}:block/{name}"}, **({"y": r} if r else {}))
                         for f, r in (("north", 0), ("east", 90), ("south", 180), ("west", 270))}}


def loot_simple(ns, name):
    return {"type": "minecraft:block", "pools": [{"bonus_rolls": 0.0, "conditions": [{"condition": "minecraft:survives_explosion"}],
                                                  "entries": [{"type": "minecraft:item", "name": f"{ns}:{name}"}], "rolls": 1.0}],
            "random_sequence": f"{ns}:blocks/{name}"}


def loot_slab(ns, name):
    return {"type": "minecraft:block", "pools": [{"bonus_rolls": 0.0, "entries": [{"type": "minecraft:item", "name": f"{ns}:{name}",
            "functions": [{"function": "minecraft:set_count", "count": 2.0, "add": False, "conditions": [{
                "condition": "minecraft:block_state_property", "block": f"{ns}:{name}", "properties": {"type": "double"}}]},
                {"function": "minecraft:explosion_decay"}]}], "rolls": 1.0}], "random_sequence": f"{ns}:blocks/{name}"}


def loot_ore(ns, ore, drop):
    silk = {"condition": "minecraft:match_tool", "predicate": {"predicates": {"minecraft:enchantments": [
        {"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}}}
    return {"type": "minecraft:block", "pools": [{"bonus_rolls": 0.0, "entries": [{"type": "minecraft:alternatives", "children": [
        {"type": "minecraft:item", "conditions": [silk], "name": f"{ns}:{ore}"},
        {"type": "minecraft:item", "name": f"{ns}:{drop}", "functions": [
            {"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune", "formula": "minecraft:ore_drops"},
            {"function": "minecraft:explosion_decay"}]}]}], "rolls": 1.0}], "random_sequence": f"{ns}:blocks/{ore}"}


ADV_TITLES = {
    "materials": ["Ooh, Shiny~", "Pocket Sparkles", "Rock Collector", "Treasure Goblin", "Dig Dig Dig!", "Pretty Pebbles"],
    "building": ["Interior Decorator", "Home Sweet Home", "Aesthetic Builder", "Block Party!", "Cozy Construction",
                 "Designer Era", "Room Makeover", "Pinterest Board", "Build It Cute", "Moodboard Material"],
    "tools": ["Cute but Useful", "Tool Time~", "Work Smarter, Cuter", "Pretty Productive"],
    "weapons": ["Bonk!", "Pretty Dangerous", "Cute Aggression", "Yeet!"],
    "armor": ["Dressed to Impress", "Fashion Armor", "Outfit Check!", "Slay (Literally)"],
    "food": ["Snack Attack", "Nom Nom Nom", "Sweet Tooth", "Treat Yourself", "Om Nom", "Tasty~"],
    "charms": ["Lucky Charm", "Accessorize!", "Bling Bling", "Jewelry Box", "Extra Sparkle"],
    "plushies": ["Squish!", "New Best Friend", "Plush Pile", "Hug Time", "Cuddle Buddy", "Adopted!"],
    "stickers": ["Sticker Bomb", "Stick It Everywhere", "Scrapbook Mode", "Collector's Binder", "Peel & Stick"],
}
ADV_DESC = {
    "materials": "Get your paws on {name}",
    "building": "Get {name} for your cute build",
    "tools": "Get {name}",
    "weapons": "Get {name} and send things flying",
    "armor": "Get {name}",
    "food": "Get {name} (now eat it!)",
    "charms": "Get {name} (hold it in your offhand or wear it as a necklace)",
    "plushies": "Adopt {name}",
    "stickers": "Collect {name}",
}
CAT_ORDER = ["materials", "building", "tools", "weapons", "armor", "food", "charms", "plushies", "stickers"]


def generate(t, index):
    ns = f"fe_{t['id']}"
    pkg = f"com.femboyequipment.official.{t['id'].replace('_', '')}"
    cls = "".join(p.capitalize() for p in t["id"].split("_")) + "Addon"
    base = os.path.join(OUT, t["id"])
    if os.path.isdir(base):
        shutil.rmtree(base)
    res = os.path.join(base, "src/main/resources")
    A, D = os.path.join(res, "assets", ns), os.path.join(res, "data", ns)
    pal = Pal(t)
    C = build(t, index)
    tier = TIERS[t["tier"]]
    m, M, S = t["mat"], t["mat_name"], t["short"]
    lang = {f"itemGroup.{ns}.main": f"{t['name']} (FemboyEquipment)",
            f"tag.item.{ns}.repair_materials": f"{t['mat_name']} Repair Materials"}

    def tex_save(im, rel):
        p = os.path.join(A, "textures", rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        im.save(p)

    seed = index * 1000
    for n, e in enumerate(C):
        sd = seed + n
        is_block = e.kind in ("cube", "stairs", "slab", "wall", "blahaj", "fih")
        lang[f"{'block' if is_block else 'item'}.{ns}.{e.id}"] = e.name
        # ---- textures + models
        if e.kind == "cube":
            kind = e.tex[0]
            im = {"ore": lambda: ore(pal, sd, e.tex[1]), "faceted": lambda: faceted(pal, sd),
                  "raw_block": lambda: raw_block(pal, sd), "bricks": lambda: bricks(pal, sd), "tiles": lambda: tiles(pal, sd),
                  "polished": lambda: polished(pal, sd), "cobbled": lambda: cobbled(pal, sd),
                  "mosaic": lambda: mosaic(pal, sd), "lamp": lambda: lamp(pal, sd), "cushion": lambda: cushion(pal, sd),
                  "crate": lambda: crate(pal, sd), "pillar": lambda: pillar(pal, sd), "chiseled": lambda: chiseled(pal, sd),
                  "shingles": lambda: shingles(pal, sd), "quilt": lambda: quilt(pal, sd), "glazed": lambda: glazed(pal, sd),
                  "starry": lambda: starry(pal, sd), "sparkling": lambda: sparkling(pal, sd)}[kind]()
            tex_save(im, f"block/{e.id}.png")
            if kind == "pillar":
                write_json(f"{A}/models/block/{e.id}.json", {"parent": "minecraft:block/cube_column", "textures": {
                    "end": f"{ns}:block/polished_{m}", "side": f"{ns}:block/{e.id}"}})
            else:
                write_json(f"{A}/models/block/{e.id}.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"{ns}:block/{e.id}"}})
            write_json(f"{A}/blockstates/{e.id}.json", {"variants": {"": {"model": f"{ns}:block/{e.id}"}}})
            write_json(f"{A}/items/{e.id}.json", {"model": {"type": "minecraft:model", "model": f"{ns}:block/{e.id}"}})
        elif e.kind in ("stairs", "slab", "wall"):
            tex = f"{ns}:block/{e.base}"
            t3 = {"bottom": tex, "top": tex, "side": tex}
            if e.kind == "stairs":
                for suffix, parent in (("", "stairs"), ("_inner", "inner_stairs"), ("_outer", "outer_stairs")):
                    write_json(f"{A}/models/block/{e.id}{suffix}.json", {"parent": f"minecraft:block/{parent}", "textures": t3})
                write_json(f"{A}/blockstates/{e.id}.json", vanilla_states("brick_stairs", ns, e.id))
                item_model_ref = f"{ns}:block/{e.id}"
            elif e.kind == "slab":
                write_json(f"{A}/models/block/{e.id}.json", {"parent": "minecraft:block/slab", "textures": t3})
                write_json(f"{A}/models/block/{e.id}_top.json", {"parent": "minecraft:block/slab_top", "textures": t3})
                write_json(f"{A}/blockstates/{e.id}.json", {"variants": {
                    "type=bottom": {"model": f"{ns}:block/{e.id}"}, "type=top": {"model": f"{ns}:block/{e.id}_top"},
                    "type=double": {"model": f"{ns}:block/{e.base}"}}})
                item_model_ref = f"{ns}:block/{e.id}"
            else:
                for suffix, parent in (("_post", "template_wall_post"), ("_side", "template_wall_side"),
                                       ("_side_tall", "template_wall_side_tall"), ("_inventory", "wall_inventory")):
                    write_json(f"{A}/models/block/{e.id}{suffix}.json", {"parent": f"minecraft:block/{parent}", "textures": {"wall": tex}})
                write_json(f"{A}/blockstates/{e.id}.json", vanilla_states("brick_wall", ns, e.id))
                item_model_ref = f"{ns}:block/{e.id}_inventory"
            write_json(f"{A}/items/{e.id}.json", {"model": {"type": "minecraft:model", "model": item_model_ref}})
        elif e.kind in ("blahaj", "fih"):
            k = e.slot
            P, Sx, Ax = pal.p, pal.s, pal.a
            if e.kind == "blahaj":
                schemes = [[P], [P, mix(P, (255, 255, 255), 0.45)] * 3, [Sx, Ax] if Sx != (255, 255, 255) else [Ax, P],
                           [mix(P, (255, 255, 255), 0.4), P, mix(P, (0, 0, 0), 0.3)], [Ax, P, Sx]]
                im = blahaj_tex([clamp(c) for c in schemes[k]], sd, k == 4)
                tex_save(im, f"block/{e.id}.png")
                write_json(f"{A}/models/block/{e.id}.json", {"parent": "femboyequipment:block/blahaj_base",
                                                             "textures": {"shark": f"{ns}:block/{e.id}"}})
            else:
                bodies = [(P, mix(P, (0, 0, 0), 0.3), (250, 248, 245), Sx, (245, 245, 245)),
                          (Sx, P, (255, 255, 255), P, (240, 240, 240)),
                          (Ax, mix(Ax, (0, 0, 0), 0.3), P, P, (60, 60, 64)),
                          (mix(P, (255, 255, 255), 0.4), P, (255, 255, 255), Ax, (245, 245, 245)),
                          (P, Ax, Sx, mix(Sx, Ax, 0.5), (250, 250, 250))]
                body, back, belly, canvas, sole = [clamp(c) for c in bodies[k]]
                im = fih_tex(body, back, belly, canvas, sole, sd, k == 4)
                tex_save(im, f"block/{e.id}.png")
                write_json(f"{A}/models/block/{e.id}.json", {"parent": "femboyequipment:block/fih_base",
                                                             "textures": {"fih": f"{ns}:block/{e.id}"}})
            write_json(f"{A}/blockstates/{e.id}.json", facing_states(ns, e.id))
            write_json(f"{A}/items/{e.id}.json", {"model": {"type": "minecraft:model", "model": f"{ns}:block/{e.id}"}})
        else:
            kind = e.tex[0]
            if kind == "gem":
                px = grid(GEM)
            elif kind == "raw":
                px = grid(RAW)
            elif kind == "nugget":
                px = grid(NUGGET)
            elif kind == "dust":
                px = grid(DUST)
            elif kind == "tool":
                px = grid(SWORD) if e.tex[1] == "sword" else grid(PICKAXE) if e.tex[1] == "pickaxe" else tool(e.tex[1])
            elif kind == "weapon":
                px = weapon(e.tex[1])
            elif kind == "armor":
                px = grid({"helmet": HELMET, "chestplate": CHEST, "leggings": LEGS, "boots": BOOTS}[e.tex[1]])
            elif kind == "food":
                px = food(e.tex[1])
            elif kind == "charm":
                px = charm(e.tex[1])
            else:
                px = None
            px = {k2: v for k2, v in (px or {}).items() if 0 <= k2[0] < 16 and 0 <= k2[1] < 16}
            im = sticker_image(sticker(e.tex[1]), pal) if kind == "sticker" else sprite(px, pal)
            tex_save(im, f"item/{e.id}.png")
            write_json(f"{A}/models/item/{e.id}.json", item_model(ns, e))
            write_json(f"{A}/items/{e.id}.json", {"model": {"type": "minecraft:model", "model": f"{ns}:item/{e.id}"}})

    # ---- armor look
    main, legs = armor_layers(pal)
    tex_save(main, f"entity/equipment/humanoid/{m}.png")
    tex_save(legs, f"entity/equipment/humanoid_leggings/{m}.png")
    write_json(f"{A}/equipment/{m}.json", {"layers": {"humanoid": [{"texture": f"{ns}:{m}"}],
                                                       "humanoid_leggings": [{"texture": f"{ns}:{m}"}]}})
    tex_save(background(pal, seed), "gui/advancements/backgrounds/main.png")

    # ---- loot tables
    for e in C:
        if e.kind == "slab":
            write_json(f"{D}/loot_table/blocks/{e.id}.json", loot_slab(ns, e.id))
        elif e.kind in ("cube", "stairs", "wall", "blahaj", "fih"):
            if e.id in (f"{m}_ore", f"deepslate_{m}_ore"):
                write_json(f"{D}/loot_table/blocks/{e.id}.json", loot_ore(ns, e.id, f"raw_{m}"))
            else:
                write_json(f"{D}/loot_table/blocks/{e.id}.json", loot_simple(ns, e.id))

    # ---- recipes
    I = lambda n: n if ":" in n else f"{ns}:{n}"  # noqa: E731
    rec = {}

    def shaped(name, pattern, key, count=1, category="building", file=None):
        rec[file or name] = {"type": "minecraft:crafting_shaped", "category": category,
                             "key": {k2: I(v) for k2, v in key.items()}, "pattern": pattern,
                             "result": {"count": count, "id": I(name)}}

    def shapeless(name, ingredients, count=1, category="misc", file=None):
        rec[file or name] = {"type": "minecraft:crafting_shapeless", "category": category,
                             "ingredients": [I(x) for x in ingredients], "result": {"count": count, "id": I(name)}}

    def cook(name, ingredient, file, xp=0.7):
        for typ, time in (("smelting", 200), ("blasting", 100)):
            rec[f"{file}_{typ}"] = {"type": f"minecraft:{typ}", "category": "misc", "cookingtime": time, "experience": xp,
                                    "ingredient": I(ingredient), "result": {"id": I(name)}}

    def cut(name, ingredient, count=1):
        rec[f"{name}_from_{ingredient.split(':')[-1]}_stonecutting"] = {
            "type": "minecraft:stonecutting", "ingredient": I(ingredient), "result": {"count": count, "id": I(name)}}

    gem, dust, nug, raw = m, f"{m}_dust", f"{m}_nugget", f"raw_{m}"
    shaped(f"{m}_block", ["###", "###", "###"], {"#": gem})
    shapeless(gem, [f"{m}_block"], 9, file=f"{m}_from_block")
    shaped(f"raw_{m}_block", ["###", "###", "###"], {"#": raw})
    shapeless(raw, [f"raw_{m}_block"], 9, file=f"raw_{m}_from_block")
    shaped(gem, ["###", "###", "###"], {"#": nug}, file=f"{m}_from_nuggets", category="misc")
    shapeless(nug, [gem], 9)
    shapeless(dust, [gem, "minecraft:flint"], 4)
    cook(gem, raw, f"{m}_from_raw")
    cook(gem, f"{m}_ore", f"{m}_from_ore", 1.0)
    cook(gem, f"deepslate_{m}_ore", f"{m}_from_deepslate_ore", 1.0)
    fam_from = {"bricks": "minecraft:stone_bricks", "tiles": "minecraft:smooth_stone", "polished": "minecraft:polished_andesite",
                "cobbled": "minecraft:cobblestone", "mosaic": "minecraft:terracotta"}
    for e in C:
        if getattr(e, "family", None):
            shaped(e.id, ["###", "#D#", "###"], {"#": fam_from[e.family], "D": dust}, 8)
            p = e.prefix
            shaped(f"{p}_stairs", ["#  ", "## ", "###"], {"#": e.id}, 4)
            shaped(f"{p}_slab", ["###"], {"#": e.id}, 6)
            shaped(f"{p}_wall", ["###", "###"], {"#": e.id}, 6, "misc")
            cut(f"{p}_stairs", e.id)
            cut(f"{p}_slab", e.id, 2)
            cut(f"{p}_wall", e.id)
    s = slug(S)
    pol, bri, til, cob = f"polished_{m}", f"{m}_bricks", f"{m}_tiles", f"cobbled_{m}"
    shaped(f"{m}_lamp", [" D ", "DGD", " D "], {"D": dust, "G": "minecraft:glowstone"})
    shapeless(f"{s}_cushion", ["minecraft:white_wool", dust])
    shaped(f"{s}_crate", ["###", "#D#", "###"], {"#": "#minecraft:planks", "D": dust}, 4)
    rec[f"{s}_crate"]["key"]["#"] = "#minecraft:planks"
    shaped(f"{m}_pillar", ["#", "#"], {"#": pol}, 2)
    shaped(f"chiseled_{m}", ["#", "#"], {"#": f"{m}_brick_slab"})
    shaped(f"{m}_shingles", ["##", "##"], {"#": til}, 4)
    shaped(f"{s}_quilt_block", ["##", "##"], {"#": f"{s}_cushion"}, 4)
    cook(f"glazed_{m}", pol, f"glazed_{m}_from_polished", 0.1)
    shaped(f"starry_{m}", ["###", "#G#", "###"], {"#": cob, "G": "minecraft:glowstone_dust"}, 8)
    shapeless(f"sparkling_{m}", [pol, dust, "minecraft:glowstone_dust"])
    cut(f"{m}_pillar", pol)
    cut(f"chiseled_{m}", bri)
    cut(f"{m}_shingles", til)
    for kind, pat in (("sword", ["#", "#", "S"]), ("pickaxe", ["###", " S ", " S "]), ("axe", ["##", "#S", " S"]),
                      ("shovel", ["#", "S", "S"]), ("hoe", ["##", " S", " S"]), ("spear", ["  #", " S ", "S  "])):
        shaped(f"{m}_{kind}", pat, {"#": gem, "S": "minecraft:stick"}, category="equipment")
    wpat = {"bat": (["B", "S"], {"B": f"{m}_block", "S": "minecraft:stick"}),
            "hammer": (["BBB", " S ", " S "], {"B": f"{m}_block", "S": "minecraft:stick"}),
            "scythe": (["###", "  S", " S "], {"#": gem, "S": "minecraft:stick"}),
            "wand": (["  D", " S ", "S  "], {"D": dust, "S": "minecraft:blaze_rod"})}
    for e in C:
        if e.cat == "weapons":
            pat, key = wpat[e.weapon_kind]
            shaped(e.id, pat, key, category="equipment")
        elif e.cat == "food":
            _, _, _, ingr, cnt = FOOD_STATS[e.slot]
            shapeless(e.id, ingr + [dust], cnt, "misc")
        elif e.cat == "charms":
            shapeless(e.id, [gem, CHARM_ITEMS[e.slot]], 1, "misc")
        elif e.cat == "stickers":
            shapeless(e.id, ["minecraft:paper", dust, f"minecraft:{DYES[e.slot]}_dye"], 4, "misc")
        elif e.kind == "blahaj":
            shapeless(e.id, [f"minecraft:{WOOLS[e.slot]}_wool", "minecraft:white_wool", gem], 1, "misc")
        elif e.kind == "fih":
            shapeless(e.id, ["minecraft:cod", f"minecraft:{WOOLS[e.slot]}_wool", gem], 1, "misc")
    for piece, pat in (("helmet", ["###", "# #"]), ("chestplate", ["# #", "###", "###"]),
                       ("leggings", ["###", "# #", "# #"]), ("boots", ["# #", "# #"])):
        shaped(f"{m}_{piece}", pat, {"#": gem}, category="equipment")
    for name, r in rec.items():
        write_json(f"{D}/recipe/{name}.json", r)
    crafted = {r["result"]["id"] for r in rec.values()}
    missing = [e.id for e in C if f"{ns}:{e.id}" not in crafted and e.id not in (f"{m}_ore", f"deepslate_{m}_ore", raw)]
    assert not missing, (t["id"], missing)

    # ---- worldgen
    write_json(f"{D}/worldgen/configured_feature/{m}_ore.json", {"type": "minecraft:ore", "config": {
        "discard_chance_on_air_exposure": 0.0, "size": 7, "targets": [
            {"state": {"Name": f"{ns}:{m}_ore"}, "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"}},
            {"state": {"Name": f"{ns}:deepslate_{m}_ore"}, "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:deepslate_ore_replaceables"}}]}})
    write_json(f"{D}/worldgen/placed_feature/{m}_ore.json", {"feature": f"{ns}:{m}_ore", "placement": [
        {"type": "minecraft:count", "count": 3}, {"type": "minecraft:in_square"},
        {"type": "minecraft:height_range", "height": {"type": "minecraft:trapezoid", "min_inclusive": {"absolute": -48},
                                                      "max_inclusive": {"absolute": 64}}},
        {"type": "minecraft:biome"}]})

    # ---- tags
    def tag(path, values, nsp="minecraft"):
        write_json(f"{res}/data/{nsp}/tags/{path}.json", {"replace": False, "values": values})

    pick = [I(e.id) for e in C if getattr(e, "tool", None) == "pickaxe"]
    tag("block/mineable/pickaxe", pick)
    tag("block/mineable/axe", [I(f"{s}_crate")])
    tag(f"block/{tier['needs']}", [I(f"{m}_ore"), I(f"deepslate_{m}_ore"), I(f"{m}_block"), I(f"raw_{m}_block")])
    for shp in ("stairs", "slabs", "walls"):
        vals = [I(e.id) for e in C if e.kind == shp[:-1] or (shp == "stairs" and e.kind == "stairs")]
        tag(f"block/{shp}", vals)
        tag(f"item/{shp}", vals)
    tag("item/swords", [I(f"{m}_sword")] + [I(e.id) for e in C if e.cat == "weapons"])
    for kind in ("pickaxe", "axe", "shovel", "hoe", "spear"):
        tag(f"item/{kind}s", [I(f"{m}_{kind}")])
    for piece, tg in (("helmet", "head_armor"), ("chestplate", "chest_armor"), ("leggings", "leg_armor"), ("boots", "foot_armor")):
        tag(f"item/{tg}", [I(f"{m}_{piece}")])
    tag("item/trimmable_armor", [I(f"{m}_{p}") for p in ("helmet", "chestplate", "leggings", "boots")])
    write_json(f"{D}/tags/item/repair_materials.json", {"values": [I(gem)]})
    tag("item/blahaj", [I(e.id) for e in C if e.kind == "blahaj"], "femboyequipment")
    tag("item/fih", [I(e.id) for e in C if e.kind == "fih"], "femboyequipment")
    tag("item/chest/necklace", [I(e.id) for e in C if e.cat == "charms"], "trinkets")

    # ---- advancements
    adv = os.path.join(D, "advancement")

    def advancement(path, title, desc, icon, criteria, parent=None, frame="task", bg=False, toast=True, xp=0):
        key = path.replace("/", ".")
        lang[f"advancements.{ns}.{key}.title"] = title
        lang[f"advancements.{ns}.{key}.description"] = desc
        display = {"icon": {"id": I(icon), "count": 1}, "title": {"translate": f"advancements.{ns}.{key}.title"},
                   "description": {"translate": f"advancements.{ns}.{key}.description"}, "frame": frame,
                   "show_toast": toast, "announce_to_chat": toast, "hidden": False}
        if bg:
            display["background"] = f"{ns}:gui/advancements/backgrounds/main"
        obj = {}
        if parent:
            obj["parent"] = f"{ns}:{parent}"
        obj["display"] = display
        obj["criteria"] = criteria
        obj["requirements"] = [list(criteria)] if frame == "challenge" else [[k2] for k2 in criteria]
        if xp:
            obj["rewards"] = {"experience": xp}
        write_json(f"{adv}/{path}.json", obj)

    got = lambda iid: {"trigger": "minecraft:inventory_changed", "conditions": {"items": [{"items": I(iid)}]}}  # noqa: E731
    advancement("main/root", t["name"], t["desc"], gem, {"tick": {"trigger": "minecraft:tick"}}, bg=True, toast=False)
    rnd = random.Random(t["id"])
    for cat in CAT_ORDER:
        group = [e for e in C if e.cat == cat]
        parent = "main/root"
        titles = ADV_TITLES[cat][:]
        rnd.shuffle(titles)
        for n, e in enumerate(group):
            last = n == len(group) - 1
            pool = titles[n % len(titles)]
            title = f"{pool}: {e.name}" if n >= len(titles) or rnd.random() < 0.5 else pool
            # make every title unique within the addon
            title = title if not any(v == title for k2, v in lang.items() if k2.endswith(".title")) else f"{pool}: {e.name}"
            advancement(f"main/{e.id}", title, ADV_DESC[cat].format(name=e.name), e.id, {"got": got(e.id)}, parent,
                        "goal" if last else "task", xp=25 if last else 0)
            parent = f"main/{e.id}"
    advancement("main/complete_collection", f"{S} Completionist", f"Collect all 100 things from {t['name']}!",
                f"{m}_block", {e.id: got(e.id) for e in C}, "main/root", "challenge", xp=500)

    # ---- lang
    write_json(f"{A}/lang/en_us.json", dict(sorted(lang.items())))

    # ---- Java
    lines = []
    for e in C:
        if e.java is None:
            continue
        var = camel(e.id)
        typ = "Block" if e.kind in ("cube", "blahaj", "fih") else "Item"
        lines.append(f"\t\t{typ} {var} = {e.java};")
        if getattr(e, "java_after", None):
            lines.append(f"\t\t{e.java_after}")
    set_effects = ", ".join(f"OutfitEffect.of(MobEffects.{eff}, {amp})" for eff, amp in t["set"])
    defense = tier["defense"]
    java = f"""package {pkg};

import com.femboyequipment.api.AddonKit;
import com.femboyequipment.api.FemboyEquipmentAddon;
import com.femboyequipment.api.FemboyEquipmentApi;
import com.femboyequipment.api.OutfitEffect;
import java.util.List;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.material.MapColor;

/**
 * {t['name']}: an official FemboyEquipment addon. {t['desc']}
 * Generated by tools/generators/official_addons.py (edit the generator, not this file).
 */
public class {cls} implements FemboyEquipmentAddon {{
	public static final String MOD_ID = "{ns}";
	public static final AddonKit KIT = new AddonKit(MOD_ID);

	@Override
	public void onFemboyEquipmentInit() {{
		AddonKit k = KIT;
		TagKey<Item> repair = k.itemTag("repair_materials");
		ToolMaterial tools = AddonKit.toolMaterial(BlockTags.{tier['incorrect']}, {tier['dur']}, {tier['speed']}F,
				{tier['attack']}F, {tier['ench']}, repair);
		ArmorMaterial armor = k.armorMaterial("{m}", {tier['armor_dur']}, {defense[0]}, {defense[2]}, {defense[1]}, {defense[3]},
				{tier['armor_ench']}, SoundEvents.{tier['sound']}, {tier['tough']}F, {tier['kb']}F, repair);

{chr(10).join(lines)}

		// Full set bonus, a world ore and the creative tab.
		FemboyEquipmentApi.addOutfitSet(List.of({camel(m)}Helmet, {camel(m)}Chestplate, {camel(m)}Leggings, {camel(m)}Boots),
				{set_effects});
		FemboyEquipmentApi.addCapsulePrize(FemboyEquipmentApi.Capsule.BLAHAJ, {camel(C[-20].id)});
		FemboyEquipmentApi.addCapsulePrize(FemboyEquipmentApi.Capsule.FIH, {camel(C[-15].id)});
		k.overworldOre("{m}_ore");
		k.creativeTab("main", () -> new ItemStack({camel(m)}));
	}}
}}
"""
    write_text(os.path.join(base, "src/main/java", pkg.replace(".", "/"), f"{cls}.java"), java)

    # ---- mod metadata + gradle
    write_json(f"{res}/fabric.mod.json", {
        "schemaVersion": 1, "id": ns, "version": "${version}",
        "name": f"FemboyEquipment: {t['name']}",
        "description": f"Official FemboyEquipment addon. {t['desc']} 100 new things: {M} ore, tools, armor, "
                       f"weapons, building blocks, snacks, charms, plushies and stickers, with its own creative tab "
                       f"and 102 advancements.",
        "authors": ["Mil3sinMe"], "license": "MIT", "icon": f"assets/{ns}/icon.png", "environment": "*",
        "entrypoints": {"femboyequipment": [f"{pkg}.{cls}"]},
        "depends": {"femboyequipment": f">={MIN_FE}", "fabric-api": "*", "fabricloader": ">=0.18.4", "minecraft": "~1.21.11"}})
    icon = Image.open(os.path.join(A, "textures/item", f"{m}.png")).resize((64, 64), Image.NEAREST)
    icon.save(os.path.join(A, "icon.png"))
    write_text(os.path.join(base, "build.gradle"),
               f"// {t['name']} - generated by tools/generators/official_addons.py\n"
               "plugins {\n\tid 'net.fabricmc.fabric-loom-remap'\n}\n\n"
               f"version = \"{ADDON_VERSION}\"\n"
               f"ext.addonModId = \"{ns}\"\n\n"
               "apply from: rootProject.file('official-addons/addon.gradle')\n")
    return ns, C


def main():
    os.makedirs(OUT, exist_ok=True)
    summary = []
    for index, t in enumerate(THEMES):
        ns, C = generate(t, index)
        summary.append((t, ns, C))
    # README table for the folder
    rows = "\n".join(f"| {t['name']} | `{ns}` | {t['mat_name']} | {t['desc']} |" for t, ns, C in summary)
    write_text(os.path.join(OUT, "LIST.md"),
               "# Official addon list\n\n(generated by `tools/generators/official_addons.py`)\n\n"
               "| Addon | Mod id | Material | Vibe |\n|---|---|---|---|\n" + rows + "\n")
    print(f"official addons: {len(summary)} addons, {sum(len(C) for _, _, C in summary)} things")


main()
