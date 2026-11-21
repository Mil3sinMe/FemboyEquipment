"""Generates FemboyEquipment textures, models, recipes, tags and loot tables.

Usage: python3 content.py <repo root>

Sprites are drawn as material maps; outlines and lighting are added automatically.
Dyeable materials ('p', 'k') on dyeable items go to a grayscale base layer that the
game tints, everything else goes to a fixed-color overlay layer.
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
MC_DATA = os.path.join(RES, "data/minecraft")
NS = "femboyequipment"

# Undyed outfit color (ARGB as a signed int, like vanilla's leather default).
# Undyed outfit colors (ARGB as signed ints, like vanilla's leather default).
# Keep in sync with OutfitColors.java.
def argb(rgb):
    return ((0xFF << 24) | (rgb[0] << 16) | (rgb[1] << 8) | rgb[2]) - (1 << 32)


PINK_RGB, MAID_RGB, BUNNY_RGB = (0xF0, 0x70, 0xB0), (0x34, 0x2C, 0x40), (0xF6, 0xF0, 0xF6)
UNDYED = {}
for _n in ("cat_ears", "femboy_hoodie", "pleated_skirt", "thigh_highs"):
    UNDYED[_n] = PINK_RGB
for _n in ("maid_headband", "maid_dress", "maid_apron", "mary_janes"):
    UNDYED[_n] = MAID_RGB
for _n in ("bunny_ears", "bunny_hoodie", "fluffy_slippers"):
    UNDYED[_n] = BUNNY_RGB

# Five-step ramps, darkest (outline) to lightest (highlight).
RAMPS = {
    "p": [(122, 32, 82), (184, 58, 120), (232, 108, 166), (246, 150, 196), (255, 200, 226)],
    "w": [(120, 110, 130), (190, 182, 198), (228, 222, 234), (246, 242, 250), (255, 255, 255)],
    "s": [(70, 70, 90), (140, 140, 160), (190, 190, 205), (220, 220, 232), (250, 250, 255)],
    "y": [(120, 80, 20), (200, 140, 40), (240, 190, 60), (255, 220, 100), (255, 245, 180)],
    "b": [(10, 8, 12), (30, 24, 34), (48, 40, 54), (70, 60, 78), (100, 90, 110)],
    "r": [(100, 10, 30), (170, 25, 55), (220, 45, 80), (240, 90, 120), (255, 150, 170)],
    "h": [(50, 25, 40), (80, 40, 65), (110, 60, 90), (140, 85, 115), (170, 110, 140)],
    "c": [(150, 40, 110), (220, 100, 170), (250, 160, 210), (255, 205, 235), (255, 240, 250)],
    "g": [(90, 110, 130), (150, 175, 195), (200, 220, 235), (225, 240, 250), (245, 252, 255)],
    "m": [(200, 120, 150), (240, 170, 195), (255, 205, 222), (255, 222, 234), (255, 240, 246)],
    "l": [(190, 90, 140), (235, 150, 190), (255, 190, 215), (255, 210, 228), (255, 230, 240)],
    "e": [(20, 70, 30), (40, 120, 50), (70, 170, 70), (110, 200, 100), (160, 230, 140)],
}
RAMPS["k"] = [RAMPS["p"][0]] + RAMPS["p"][:4]           # darker fabric
GRAY = [(120, 120, 120), (178, 178, 178), (222, 222, 222), (242, 242, 242), (255, 255, 255)]
GRAY_K = [GRAY[0]] + GRAY[:4]
FLAT = {"Y": (255, 240, 150, 255)}                       # sparkles: no outline, no shading
DYED = {"p", "k"}


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent="\t")
        f.write("\n")


def save(im, rel):
    path = os.path.join(ASSETS, "textures", rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)


def color(mat, shade, dyed):
    if mat in FLAT:
        return FLAT[mat]
    if dyed and mat in DYED:
        rgb = (GRAY_K if mat == "k" else GRAY)[shade]
    else:
        rgb = RAMPS[mat][shade]
    return rgb + (255,)


# ---------------------------------------------------------------- item sprites
def grid(rows, mirror):
    if mirror:
        rows = [r.ljust(8, ".")[:8] + r.ljust(8, ".")[:8][::-1] for r in rows]
    for r in rows:
        assert len(r) <= 16, r
    rows = [r.ljust(16, ".") for r in rows] + ["." * 16] * (16 - len(rows))
    return [list(r) for r in rows[:16]]


def render_item(rows, mirror=False, dyeable=False):
    """Returns (base, overlay). For non-dyeable items everything is in base."""
    g = grid(rows, mirror)
    solid = lambda x, y: 0 <= x < 16 and 0 <= y < 16 and g[y][x] not in "." and g[y][x] not in FLAT
    base = Image.new("RGBA", (16, 16))
    over = Image.new("RGBA", (16, 16))

    def put(x, y, mat, shade):
        target = base if (not dyeable or mat in DYED) else over
        target.putpixel((x, y), color(mat, shade, dyeable))

    for y in range(16):
        for x in range(16):
            mat = g[y][x]
            if mat == ".":
                # outline: take the darkest shade of a neighbouring material
                for nx, ny in ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)):
                    if solid(nx, ny):
                        put(x, y, g[ny][nx], 0)
                        break
                continue
            if mat in FLAT:
                (over if dyeable else base).putpixel((x, y), FLAT[mat])
                continue
            up, left = solid(x, y - 1), solid(x - 1, y)
            down, right = solid(x, y + 1), solid(x + 1, y)
            if not up and not left:
                shade = 4
            elif not up or not left:
                shade = 3
            elif not down or not right:
                shade = 1
            else:
                shade = 2
            put(x, y, mat, shade)
    return base, over


ITEMS = {
    # name: (mirror, dyeable, rows)
    "cat_ears": (True, True, [
        "", "",
        ".pp",
        ".ppp",
        ".plpp",
        ".pllpp",
        ".pllppp",
        ".plllppp",
        ".ppppppp",
        "pkkkkkkk",
        "pkkkkkkk",
        ".kkkkkkk",
        ".......y",
        ".......y",
    ]),
    "femboy_hoodie": (True, True, [
        "",
        "....pppp",
        "..pppppp",
        ".pppkkkk",
        ".ppkkkkk",
        "pppppwrp",
        "pppppwrr",
        "pppppwpr",
        "pkpppppp",
        "pkpppppp",
        "pkppkkkk",
        "pkppkppp",
        "pkppkppp",
        "wwpppppp",
        "..kkkkkk",
    ]),
    "pleated_skirt": (True, True, [
        "", "",
        "...kkkkk",
        "...wwwww",
        "...kkkkk",
        "..pkppkp",
        "..pkppkp",
        ".ppkppkp",
        ".ppkppkp",
        "ppkppkpp",
        "ppkppkpp",
        "wwwwwwww",
        "w.w.w.w.",
    ]),
    "thigh_highs": (True, True, [
        ".yyyy",
        ".wwww",
        ".pppp",
        ".wwww",
        ".pppp",
        ".wwww",
        ".pppp",
        ".wwww",
        ".pppp",
        ".wwww",
        ".pppp",
        "ppppp",
        "wwwww",
        ".kkkk",
    ]),
    "pink_ribbon": (True, False, [
        "", "",
        ".pp",
        ".plp",
        ".pllp",
        ".plllp",
        ".pllllpk",
        ".pllllkk",
        ".ppplpkk",
        ".pppppkk",
        ".....pk",
        "....pp",
        "...pp",
        "..pp",
    ]),
    "programming_socks": (False, False, [
        "",
        "....wwwww",
        "....ppppp",
        "....wwwww",
        "....ppppp",
        "....wwwww",
        "....ppppp",
        "....wwwww",
        "....ppppp",
        "....pppppp",
        "....wwwwwwww",
        "....pppppppppp",
        "....wwwwwwwwww",
        ".....kkkkkkkk",
    ]),
    "hair_clip": (True, False, [
        "", "", "", "",
        "..pp",
        ".pllp",
        ".pllpp",
        ".plpppss",
        ".ppppkss",
        ".pkkp",
        "..pp",
    ]),
    "choker": (True, False, [
        "", "", "",
        "...bbbbb",
        ".bb",
        ".b",
        "b",
        "b",
        "b",
        ".b",
        ".bb",
        "...bbbbs",
        "......p.",
        "......pp",
        ".......p",
    ]),
    "strawberry_milk": (True, False, [
        "......pp",
        "......gg",
        "......gm",
        ".....gmm",
        "...ggmmm",
        "...gmmmm",
        "...gmmme",
        "...gmmmr",
        "...gmmrr",
        "...gmmrr",
        "...gmmmr",
        "...gmmmm",
        "...gmmmm",
        "...ggggg",
    ]),
    "sparkly_sword": (False, False, [
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
        "..p.............",
    ]),
    "sparkly_pickaxe": (False, False, [
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
        ".p..............",
    ]),
    "maid_headband": (True, True, [
        "", "", "", "",
        "..w.w.w.",
        ".wwwwwww",
        ".wpppppp",
        "wppppppp",
        ".p",
    ]),
    "maid_dress": (True, True, [
        "",
        "...pwwww",
        "..pppwww",
        ".ppppppw",
        "wwpppppp",
        "..pppppw",
        "..pppppp",
        "..pppppw",
        "..pppppp",
        ".ppppppp",
        ".ppppppp",
        "pppppppp",
        "wwwwwwww",
        "w.w.w.w.",
    ]),
    "maid_apron": (True, True, [
        "", "",
        "....p...",
        "....wwww",
        "....wwww",
        "....wwww",
        "pppppppp",
        "...wwwww",
        "..wwwwww",
        "..wwwwww",
        ".wwwwwww",
        ".wwwwwww",
        "wwwwwwww",
        "w.w.w.w.",
    ]),
    "mary_janes": (True, True, [
        "", "", "", "", "", "",
        "...ww",
        "...ww",
        "...ww",
        ".ppppy",
        "pppppp",
        "pppppp",
        "kkkkkk",
    ]),
    "bunny_ears": (True, True, [
        "..pp",
        ".plp",
        ".plp",
        ".plp",
        ".plp",
        ".plp",
        "..plp",
        "..plp",
        "...pp",
        "..kkkkkk",
        ".kkkkkkk",
        ".kkkkkkk",
    ]),
    "bunny_hoodie": (True, True, [
        "..pp",
        "..plpppp",
        "..pppppp",
        ".pppkkkk",
        ".ppkkkkk",
        "ppppplpp",
        "ppppplpp",
        "ppppplpp",
        "pkpppppp",
        "pkpppppp",
        "pkppkkkk",
        "pkppkppp",
        "pkppkppp",
        "wwpppppp",
        "..kkkkkk",
    ]),
    "fluffy_slippers": (True, True, [
        "", "", "", "", "", "",
        "..p.p",
        "..plp",
        ".ppppp",
        "pbppbp",
        "ppplpp",
        "pppppp",
        "kkkkkk",
    ]),
}

DYEABLE_ITEMS = [n for n, (_, d, _) in ITEMS.items() if d]

for name, (mirror, dyeable, rows) in ITEMS.items():
    base, over = render_item(rows, mirror, dyeable)
    save(base, f"item/{name}.png")
    if dyeable:
        save(over, f"item/{name}_overlay.png")


# --------------------------------------------------------------- block textures
def bricks():
    rnd = random.Random(7)
    mortar = [(255, 214, 230), (246, 200, 218)]
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            im.putpixel((x, y), mortar[(x + y) % 2] + (255,))
    ramp = RAMPS["p"]
    for row in range(4):
        y0 = row * 4
        offset = 0 if row % 2 == 0 else 4
        for x0 in range(-offset, 16, 8):
            tone = rnd.choice([0, 0, 1])
            for y in range(y0, y0 + 3):
                for x in range(x0, x0 + 7):
                    if not 0 <= x < 16:
                        continue
                    if y == y0:
                        shade = 4
                    elif x == x0 + 6 or y == y0 + 2:
                        shade = 2
                    else:
                        shade = 3
                    shade -= tone
                    if rnd.random() < 0.12:
                        shade = max(1, shade - 1)
                    im.putpixel((x, y), ramp[shade] + (255,))
    return im


def ribbon_block():
    rnd = random.Random(3)
    im = Image.new("RGBA", (16, 16))
    p, w = RAMPS["p"], RAMPS["w"]
    for y in range(16):
        for x in range(16):
            # quilted fabric: diagonal stitching every 4 pixels
            shade = 2 if (x + y) % 4 == 0 or (x - y) % 4 == 0 else 3
            if rnd.random() < 0.1:
                shade += 1
            im.putpixel((x, y), p[shade] + (255,))
    for i in range(16):
        for j, shade in ((6, 1), (7, 4), (8, 3), (9, 1)):
            im.putpixel((i, j), w[shade] + (255,))
            im.putpixel((j, i), w[shade] + (255,))
        im.putpixel((i, 0), p[4] + (255,))
        im.putpixel((0, i), p[4] + (255,))
        im.putpixel((i, 15), p[1] + (255,))
        im.putpixel((15, i), p[1] + (255,))
    # little bow in the middle
    bow = {(5, 6): 2, (5, 9): 2, (4, 5): 3, (4, 10): 3, (10, 6): 2, (10, 9): 2, (11, 5): 3, (11, 10): 3,
           (6, 7): 4, (6, 8): 3, (9, 7): 4, (9, 8): 3}
    for (x, y), shade in bow.items():
        im.putpixel((x, y), w[shade] + (255,))
    for x in (7, 8):
        for y in (7, 8):
            im.putpixel((x, y), RAMPS["r"][3 if y == 7 else 2] + (255,))
    return im


save(bricks(), "block/pastel_pink_bricks.png")
save(ribbon_block(), "block/ribbon_block.png")


# ------------------------------------------------------------ worn armor layers
def faces(u, v, w, h, d):
    """Texture rectangles (x, y, width, height) of a model box, Minecraft UV layout."""
    return {
        "top": (u + d, v, w, d),
        "bottom": (u + d + w, v, w, d),
        "right": (u, v + d, d, h),
        "front": (u + d, v + d, w, h),
        "left": (u + d + w, v + d, d, h),
        "back": (u + d + w + d, v + d, w, h),
    }


HEAD = faces(0, 0, 8, 8, 8)
BODY = faces(16, 16, 8, 12, 4)
ARM = faces(40, 16, 4, 12, 4)
LEG = faces(0, 16, 4, 12, 4)
SIDES = ("right", "front", "left", "back")


class Layer:
    """A worn texture split into a dyeable grayscale base and a fixed-color overlay."""

    def __init__(self):
        self.base = Image.new("RGBA", (64, 32))
        self.over = Image.new("RGBA", (64, 32))

    def paint(self, rect, fn, shading=True):
        x0, y0, w, h = rect
        for dy in range(h):
            for dx in range(w):
                mat = fn(dx, dy, w, h)
                if mat is None:
                    continue
                if mat in FLAT:
                    self.over.putpixel((x0 + dx, y0 + dy), FLAT[mat])
                    continue
                shade = 2
                if shading:
                    if dy == 0:
                        shade = 3
                    elif dy == h - 1:
                        shade = 1
                    if (dx + dy) % 5 == 0 and 0 < dy < h - 1:
                        shade = 3  # soft fabric texture
                target = self.base if mat in DYED else self.over
                target.putpixel((x0 + dx, y0 + dy), color(mat, shade, True))


def cat_ears_layer():
    L = Layer()
    L.paint(HEAD["top"], lambda x, y, w, h: "p" if y in (3, 4) else None, shading=False)
    for side in ("left", "right"):
        L.paint(HEAD[side], lambda x, y, w, h: "p" if y == 0 and 3 <= x <= 4 else None, shading=False)

    # the ears themselves are a 3D model (AccessoryModels.catEars)
    return L


def hoodie_layer():
    L = Layer()

    def front(x, y, w, h):
        if x in (2, 5) and 1 <= y <= 4:
            return "w"
        if 7 <= y <= 9 and 1 <= x <= 6:
            return "k"
        if y == h - 1:
            return "k"
        return "p"
    L.paint(BODY["front"], front)
    # little heart print
    L.paint((BODY["front"][0] + 3, BODY["front"][1] + 2, 2, 2), lambda x, y, w, h: "r", shading=False)
    L.paint(BODY["back"], lambda x, y, w, h: "k" if y <= 3 and (x in (0, 7) or y == 3) else ("p" if y < h - 1 else "k"))
    for side in ("left", "right", "top", "bottom"):
        L.paint(BODY[side], lambda x, y, w, h: "p" if y < h - 1 else "k")
    for side in ARM:
        L.paint(ARM[side], lambda x, y, w, h: "k" if y >= h - 2 else "p")
    return L


def skirt_layer():
    L = Layer()
    for side in SIDES:
        L.paint(BODY[side], lambda x, y, w, h: ("k" if y == h - 2 else "p") if y >= h - 2 else None)
    L.paint(BODY["bottom"], lambda x, y, w, h: "p")
    # the flared skirt itself is a 3D model (AccessoryModels.skirt)
    return L


def thigh_highs_layer():
    L = Layer()

    def stripes(x, y, w, h):
        if y == 0:
            return "Y"  # sparkly lace trim
        if y == 1:
            return "w"
        return "p" if (y // 2) % 2 == 0 else "w"
    for side in SIDES:
        L.paint(LEG[side], stripes)
    L.paint(LEG["bottom"], lambda x, y, w, h: "k")
    return L


def maid_headband_layer():
    L = Layer()
    L.paint(HEAD["top"], lambda x, y, w, h: "p" if y in (2, 3) else None, shading=False)
    for side in ("left", "right"):
        L.paint(HEAD[side], lambda x, y, w, h: "p" if y <= 1 and 2 <= x <= 3 else None, shading=False)
    # white frills along the forehead
    L.paint(HEAD["front"], lambda x, y, w, h: "w" if y == 0 or (y == 1 and x % 2 == 0) else None, shading=False)
    return L


def maid_dress_layer():
    L = Layer()

    def front(x, y, w, h):
        if y <= 1 and 2 <= x <= 5:
            return "w"  # collar
        if x in (3, 4) and y in (3, 5, 7):
            return "w"  # buttons
        return "p"
    L.paint(BODY["front"], front)
    for side in ("left", "right", "back", "top", "bottom"):
        L.paint(BODY[side], lambda x, y, w, h: "p")
    for side in ARM:
        # puffy short sleeves with white cuffs
        L.paint(ARM[side], lambda x, y, w, h: "p" if y <= 3 else ("w" if y == 4 else None))
    L.paint(ARM["top"], lambda x, y, w, h: "p")
    return L


def maid_apron_layer():
    L = Layer()
    for side in SIDES:
        L.paint(BODY[side], lambda x, y, w, h: "p" if y >= h - 2 else None)
    # apron bib + waist ties
    L.paint(BODY["front"], lambda x, y, w, h: "w" if y >= 6 and 1 <= x <= 6 else None)
    L.paint(BODY["back"], lambda x, y, w, h: "w" if y == h - 2 and 2 <= x <= 5 else None, shading=False)
    # the skirt and apron front are a 3D model (AccessoryModels.skirt)
    return L


def mary_janes_layer():
    L = Layer()

    def shoe(x, y, w, h):
        if y == 2:
            return "w"  # lace top of the socks
        if 3 <= y <= 8:
            return "w"
        if y >= 9:
            return "p"
        return None
    for side in SIDES:
        L.paint(LEG[side], shoe)
    # strap with a gold buckle across the front
    L.paint(LEG["front"], lambda x, y, w, h: ("y" if x == 2 else "p") if y == 8 else None, shading=False)
    L.paint(LEG["bottom"], lambda x, y, w, h: "k")
    return L


def bunny_ears_layer():
    L = Layer()
    L.paint(HEAD["top"], lambda x, y, w, h: "p" if y in (3, 4) else None, shading=False)
    for side in ("left", "right"):
        L.paint(HEAD[side], lambda x, y, w, h: "p" if y == 0 and 3 <= x <= 4 else None, shading=False)
    return L


def bunny_hoodie_layer():
    L = Layer()

    def front(x, y, w, h):
        if x in (2, 5) and 1 <= y <= 4:
            return "l"
        if 7 <= y <= 9 and 1 <= x <= 6:
            return "k"
        if y == h - 1:
            return "k"
        return "p"
    L.paint(BODY["front"], front)
    L.paint(BODY["back"], lambda x, y, w, h: "k" if y <= 3 and (x in (0, 7) or y == 3) else ("p" if y < h - 1 else "k"))
    for side in ("left", "right", "top", "bottom"):
        L.paint(BODY[side], lambda x, y, w, h: "p" if y < h - 1 else "k")
    for side in ARM:
        L.paint(ARM[side], lambda x, y, w, h: "w" if y >= h - 2 else "p")
    return L


def fluffy_slippers_layer():
    L = Layer()
    for side in SIDES:
        L.paint(LEG[side], lambda x, y, w, h: ("k" if (x + y) % 3 == 0 else "p") if y >= 8 else None)

    def face(x, y, w, h):
        if y == 9 and x in (0, 3):
            return "b"  # eyes
        if y == 10 and x in (1, 2):
            return "l"  # nose
        return None
    L.paint(LEG["front"], face, shading=False)
    L.paint(LEG["bottom"], lambda x, y, w, h: "k")
    return L


WEARABLES = [
    ("cat_ears", cat_ears_layer, "humanoid"),
    ("femboy_hoodie", hoodie_layer, "humanoid"),
    ("pleated_skirt", skirt_layer, "humanoid_leggings"),
    ("thigh_highs", thigh_highs_layer, "humanoid"),
    ("maid_headband", maid_headband_layer, "humanoid"),
    ("maid_dress", maid_dress_layer, "humanoid"),
    ("maid_apron", maid_apron_layer, "humanoid_leggings"),
    ("mary_janes", mary_janes_layer, "humanoid"),
    ("bunny_ears", bunny_ears_layer, "humanoid"),
    ("bunny_hoodie", bunny_hoodie_layer, "humanoid"),
    ("fluffy_slippers", fluffy_slippers_layer, "humanoid"),
]
for name, fn, layer in WEARABLES:
    L = fn()
    save(L.base, f"entity/equipment/{layer}/{name}.png")
    save(L.over, f"entity/equipment/{layer}/{name}_overlay.png")
    write_json(f"{ASSETS}/equipment/{name}.json", {"layers": {layer: [
        {"texture": f"{NS}:{name}", "dyeable": {"color_when_undyed": argb(UNDYED[name])}},
        {"texture": f"{NS}:{name}_overlay"},
    ]}})


# ------------------------------------------------------- 3D accessory textures
class Accessory(Layer):
    def __init__(self, w, h):
        self.base = Image.new("RGBA", (w, h))
        self.over = Image.new("RGBA", (w, h))

    def box(self, u, v, w, h, d, fn=lambda x, y, fw, fh, side: "p"):
        for side, rect in faces(u, v, w, h, d).items():
            self.paint(rect, lambda x, y, fw, fh: fn(x, y, fw, fh, side))


def save_accessory(acc, name):
    save(acc.base, f"entity/accessory/{name}.png")
    save(acc.over, f"entity/accessory/{name}_overlay.png")


def inner_ear(x, y, w, h, side):
    if side == "front" and 0 < x < w - 1 or (side == "front" and w <= 2 and y > 0):
        return "l"
    return "p"


acc = Accessory(16, 16)
acc.box(0, 0, 3, 3, 1, lambda x, y, w, h, side: "l" if side == "front" and x == 1 and y >= 1 else "p")
acc.box(0, 4, 2, 2, 1, lambda x, y, w, h, side: "l" if side == "front" and y == 1 else "p")
acc.box(0, 8, 1, 1, 1)
save_accessory(acc, "cat_ears")

acc = Accessory(16, 16)
acc.box(0, 0, 1, 1, 4)
acc.box(0, 6, 1, 1, 3, lambda x, y, w, h, side: "w" if side != "top" or y >= 1 else "p")
save_accessory(acc, "cat_tail")

acc = Accessory(16, 16)
acc.box(0, 0, 2, 8, 1, lambda x, y, w, h, side: "l" if side == "front" and 1 <= y <= 6 else "p")
save_accessory(acc, "bunny_ears")

acc = Accessory(16, 16)
acc.box(0, 10, 3, 3, 2, lambda x, y, w, h, side: "k" if (x + y) % 3 == 0 else "p")
save_accessory(acc, "bunny_tail")


def skirt(apron):
    acc = Accessory(64, 32)

    def waist(x, y, w, h, side):
        if apron and side == "front" and 2 <= x <= 6:
            return "w"
        return "k"
    acc.box(0, 0, 9, 2, 5, waist)

    def panel(name):
        def fn(x, y, w, h, side):
            if side in ("top", "bottom"):
                return "p"
            if y == h - 1:
                return "w"  # lace hem
            if apron and name == "front" and side == "front" and 2 <= x <= 7:
                return "w"
            return "k" if x % 2 == 1 else "p"  # pleats
        return fn
    acc.box(0, 8, 10, 6, 1, panel("front"))
    acc.box(0, 16, 10, 6, 1, panel("back"))
    acc.box(24, 8, 1, 6, 6, panel("right"))
    acc.box(40, 8, 1, 6, 6, panel("left"))
    return acc


save_accessory(skirt(False), "pleated_skirt")
save_accessory(skirt(True), "maid_skirt")


# ------------------------------------------------------------ models / item defs
HANDHELD = {"sparkly_sword", "sparkly_pickaxe"}
for name in ITEMS:
    model = {"type": "minecraft:model", "model": f"{NS}:item/{name}"}
    textures = {"layer0": f"{NS}:item/{name}"}
    if name in DYEABLE_ITEMS:
        model["tints"] = [{"type": "minecraft:dye", "default": argb(UNDYED[name])}]
        textures["layer1"] = f"{NS}:item/{name}_overlay"
    write_json(f"{ASSETS}/items/{name}.json", {"model": model})
    write_json(f"{ASSETS}/models/item/{name}.json", {
        "parent": "minecraft:item/handheld" if name in HANDHELD else "minecraft:item/generated",
        "textures": textures,
    })

BLOCKS = ["pastel_pink_bricks", "ribbon_block"]
for name in BLOCKS:
    write_json(f"{ASSETS}/blockstates/{name}.json", {"variants": {"": {"model": f"{NS}:block/{name}"}}})
    write_json(f"{ASSETS}/models/block/{name}.json",
               {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/{name}"}})
    write_json(f"{ASSETS}/items/{name}.json",
               {"model": {"type": "minecraft:model", "model": f"{NS}:block/{name}"}})
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

# ----------------------------------------------------------------------- lang
write_json(f"{ASSETS}/lang/en_us.json", {
    "itemGroup.femboyequipment.main": "Femboy Equipment",
    "item.femboyequipment.pink_ribbon": "Pink Ribbon",
    "item.femboyequipment.programming_socks": "Programming Socks",
    "item.femboyequipment.hair_clip": "Hair Clip",
    "item.femboyequipment.choker": "Choker",
    "item.femboyequipment.strawberry_milk": "Strawberry Milk",
    "item.femboyequipment.cat_ears": "Cat Ears",
    "item.femboyequipment.femboy_hoodie": "Femboy Hoodie",
    "item.femboyequipment.pleated_skirt": "Pleated Skirt",
    "item.femboyequipment.thigh_highs": "Thigh Highs",
    "item.femboyequipment.maid_headband": "Maid Headband",
    "item.femboyequipment.maid_dress": "Maid Dress",
    "item.femboyequipment.maid_apron": "Maid Apron",
    "item.femboyequipment.mary_janes": "Mary Janes",
    "item.femboyequipment.bunny_ears": "Bunny Ears",
    "item.femboyequipment.bunny_hoodie": "Bunny Hoodie",
    "item.femboyequipment.fluffy_slippers": "Fluffy Slippers",
    "item.femboyequipment.sparkly_sword": "Sparkly Sword",
    "item.femboyequipment.sparkly_pickaxe": "Sparkly Pickaxe",
    "block.femboyequipment.pastel_pink_bricks": "Pastel Pink Bricks",
    "block.femboyequipment.ribbon_block": "Block of Ribbons",
})


# ----------------------------------------------------------------------- tags
def tag(base, path, values):
    write_json(f"{base}/tags/{path}.json", {"replace": False, "values": values})


def i(name):
    return f"{NS}:{name}"


OUTFIT = list(UNDYED)
tag(DATA, "item/cute_repair_materials", ["minecraft:pink_wool", i("pink_ribbon")])
tag(MC_DATA, "item/dyeable", [i(n) for n in OUTFIT])
tag(MC_DATA, "item/head_armor", [i("cat_ears"), i("maid_headband"), i("bunny_ears")])
tag(MC_DATA, "item/chest_armor", [i("femboy_hoodie"), i("maid_dress"), i("bunny_hoodie")])
tag(MC_DATA, "item/leg_armor", [i("pleated_skirt"), i("maid_apron")])
tag(MC_DATA, "item/foot_armor", [i("thigh_highs"), i("mary_janes"), i("fluffy_slippers")])
tag(MC_DATA, "item/swords", [i("sparkly_sword")])
tag(MC_DATA, "item/pickaxes", [i("sparkly_pickaxe")])
tag(MC_DATA, "block/mineable/pickaxe", [i("pastel_pink_bricks")])


# -------------------------------------------------------------------- recipes
def shaped(name, pattern, key, count=1, category="equipment"):
    write_json(f"{DATA}/recipe/{name}.json", {
        "type": "minecraft:crafting_shaped",
        "category": category,
        "key": key,
        "pattern": pattern,
        "result": {"count": count, "id": i(name)},
    })


def shapeless(name, ingredients, count=1, category="misc", file=None):
    write_json(f"{DATA}/recipe/{file or name}.json", {
        "type": "minecraft:crafting_shapeless",
        "category": category,
        "ingredients": ingredients,
        "result": {"count": count, "id": i(name)},
    })


PINK = "minecraft:pink_wool"
RIBBON = i("pink_ribbon")
shapeless("pink_ribbon", ["minecraft:string", "minecraft:string", "minecraft:pink_dye"], count=2)
shaped("programming_socks", ["W W", "P P", "W W"], {"W": "minecraft:white_wool", "P": PINK})
shapeless("hair_clip", [RIBBON, "minecraft:iron_ingot"], count=2)
shaped("choker", ["SSS", "S S", " D "], {"S": "minecraft:string", "D": "minecraft:pink_dye"})
shapeless("strawberry_milk", ["minecraft:milk_bucket", "minecraft:sweet_berries", "minecraft:sugar",
                              "minecraft:glass_bottle", "minecraft:glass_bottle", "minecraft:glass_bottle"],
          count=3, category="misc")
shaped("cat_ears", ["P P", "RHR"], {"P": PINK, "R": RIBBON, "H": i("hair_clip")})
shaped("femboy_hoodie", ["P P", "PCP", "PPP"], {"P": PINK, "C": i("choker")})
shaped("pleated_skirt", ["PRP", "P P", "P P"], {"P": PINK, "R": RIBBON})
shaped("thigh_highs", ["RNR", "S S"], {
    "N": "minecraft:netherite_ingot", "R": RIBBON, "S": i("programming_socks")})
BLACK, WHITE = "minecraft:black_wool", "minecraft:white_wool"
shaped("maid_headband", ["WWW", "S S"], {"W": WHITE, "S": "minecraft:string"})
shaped("maid_dress", ["B B", "BWB", "BBB"], {"B": BLACK, "W": WHITE})
shaped("maid_apron", ["BRB", "W W", "W W"], {"B": BLACK, "R": RIBBON, "W": WHITE})
shaped("mary_janes", ["R R", "L L"], {"R": RIBBON, "L": "minecraft:leather"})
shaped("bunny_ears", ["H H", "WRW"], {"H": "minecraft:rabbit_hide", "W": WHITE, "R": RIBBON})
shaped("bunny_hoodie", ["W W", "WFW", "WWW"], {"W": WHITE, "F": "minecraft:rabbit_foot"})
shaped("fluffy_slippers", ["W W", "H H"], {"W": WHITE, "H": "minecraft:rabbit_hide"})
shaped("sparkly_sword", ["RDR", " D ", " S "], {"R": RIBBON, "D": "minecraft:diamond", "S": "minecraft:stick"})
shaped("sparkly_pickaxe", ["DDD", "RSR", " S "], {"R": RIBBON, "D": "minecraft:diamond", "S": "minecraft:stick"})
shaped("pastel_pink_bricks", ["BBB", "BDB", "BBB"], {"B": "minecraft:bricks", "D": "minecraft:pink_dye"},
       count=8, category="building")
shaped("ribbon_block", ["RRR", "RRR", "RRR"], {"R": RIBBON}, category="building")
shapeless("pink_ribbon", [i("ribbon_block")], count=9, file="pink_ribbon_from_ribbon_block")

# ---------------------------------------------------------------------- icon
icon = Image.new("RGBA", (128, 128), (255, 228, 240, 255))
ribbon = Image.open(os.path.join(ASSETS, "textures/item/pink_ribbon.png"))
icon.alpha_composite(ribbon.resize((112, 112), Image.NEAREST), (8, 8))
icon.save(os.path.join(ASSETS, "icon.png"))
print("done")
