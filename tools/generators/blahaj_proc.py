# 870 procedural Blåhaj: 29 colors x 30 patterns. name -> (display, stripe colors, pattern, color hex)
import colorsys

COLORS = [
    ("lavender", "Lavender", "b57edc"), ("peach", "Peach", "ffbf94"), ("sky", "Sky", "7ec8eb"),
    ("teal", "Teal", "2a9d8f"), ("coral", "Coral", "ff7f50"), ("cherry", "Cherry", "d2042d"),
    ("lilac", "Lilac", "c8a2c8"), ("rose", "Rose", "ff66cc"), ("sapphire", "Sapphire", "1f5fd6"),
    ("ruby", "Ruby", "e0115f"), ("jade", "Jade", "00a86b"), ("honey", "Honey", "ffc30b"),
    ("mango", "Mango", "ffa53f"), ("plum", "Plum", "8e4585"), ("cobalt", "Cobalt", "0047ab"),
    ("seafoam", "Seafoam", "93e9be"), ("bubblegum", "Bubblegum", "ffa6c9"), ("slate", "Slate", "708090"),
    ("sand", "Sand", "e2c290"), ("forest", "Forest", "2e8b3a"), ("crimson", "Crimson", "dc143c"),
    ("periwinkle", "Periwinkle", "a8a8ff"), ("aqua", "Aqua", "22e0e0"), ("tangerine", "Tangerine", "f28500"),
    ("blush", "Blush", "de5d83"), ("charcoal", "Charcoal", "36454f"), ("cream", "Cream", "f5ecc8"),
    ("olive", "Olive", "8a8a1a"), ("berry", "Berry", "990f4b"),
]
PATTERNS = [
    ("plain", "Plain"), ("striped", "Striped"), ("two_tone", "Two-Tone"), ("gradient", "Gradient"),
    ("ombre", "Ombré"), ("sunset", "Sunset"), ("frosted", "Frosted"), ("shadow", "Shadow"),
    ("banded", "Banded"), ("neon", "Neon"), ("pastel", "Pastel"), ("metallic", "Metallic"),
    ("spotted", "Spotted"), ("polka", "Polka Dot"), ("starry", "Starry"), ("speckled", "Speckled"),
    ("checkered", "Checkered"), ("zigzag", "Zigzag"), ("camo", "Camo"), ("marble", "Marble"),
    ("glitter", "Glitter"), ("galaxy", "Galaxy"), ("tie_dye", "Tie-Dye"), ("plaid", "Plaid"),
    ("hearts", "Heart Print"), ("holographic", "Holographic"), ("ringed", "Ringed"), ("split", "Split"),
    ("cursed", "Cursed"), ("royal", "Royal"),
]
assert len(COLORS) == 29 and len(PATTERNS) == 30


def hx(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(c):
    return "%02x%02x%02x" % tuple(max(0, min(255, int(v))) for v in c)


def mix(a, b, t):
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


WHITE, BLACK = (255, 255, 255), (0, 0, 0)


def stripe_colors(pattern, base):
    c = hx(base)
    light, dark = mix(c, WHITE, 0.45), mix(c, BLACK, 0.35)
    table = {
        "striped": [c, light, c, light, c, light],
        "two_tone": [c, c, dark, dark],
        "gradient": [light, c, dark],
        "ombre": [c, mix(c, WHITE, 0.3), mix(c, WHITE, 0.6)],
        "sunset": [c, mix(c, (255, 140, 60), 0.5), (255, 190, 90)],
        "frosted": [WHITE, mix(c, WHITE, 0.5), c, c],
        "shadow": [mix(c, BLACK, 0.55), c],
        "banded": [c, WHITE, c, WHITE, c],
        "neon": [mix(c, WHITE, 0.15)],
        "pastel": [mix(c, WHITE, 0.55)],
        "metallic": [light, c, dark, c, light],
        "starry": [mix(c, BLACK, 0.5)],
        "galaxy": [mix(c, (20, 0, 50), 0.6), mix(c, (90, 30, 140), 0.5), mix(c, (20, 0, 50), 0.6)],
        "cursed": [tuple(255 - v for v in c)],
        "royal": [c, (255, 205, 60), c],
        "holographic": [mix(c, h, 0.45) for h in ((255, 150, 220), (150, 220, 255), (190, 255, 190), (255, 245, 170))],
        "split": [c, c, mix(c, WHITE, 0.6), mix(c, WHITE, 0.6)],
    }
    return [to_hex(x) for x in table.get(pattern, [c])]


PROC = {}
for pid, pdisp in PATTERNS:
    for cid, cdisp, chex in COLORS:
        PROC[f"{pid}_{cid}_blahaj"] = (f"{pdisp} {cdisp} Blåhaj", stripe_colors(pid, chex), pid, chex)
assert len(PROC) == 870

PROC_LIGHT = {n: 7 for n, v in PROC.items() if v[2] == "neon"}
PROC_RARE = {n for n, v in PROC.items() if v[2] in ("holographic", "royal", "galaxy")}
PROC_SPARKLY = {n for n, v in PROC.items() if v[2] in ("glitter", "galaxy", "starry", "holographic", "royal")}


def overlay(im, name, rnd):
    """Pattern details painted over the striped base (side 0..16 x 0..10, top 16..32 x 0..16)."""
    disp, cols, pattern, chex = PROC[name]
    c = hx(chex)
    light, dark = mix(c, WHITE, 0.5), mix(c, BLACK, 0.4)

    def put(x, y, col):
        im.putpixel((x, y), tuple(int(v) for v in col) + (255,))

    regions = [(0, 0, 16, 10), (16, 0, 16, 16)]  # side (colored part), top
    for x0, y0, w, h in regions:
        for y in range(h):
            for x in range(w):
                X, Y = x0 + x, y0 + y
                if pattern == "spotted" and (x * 7 + y * 13) % 11 == 0:
                    put(X, Y, dark)
                elif pattern == "polka" and x % 4 == 1 and y % 4 == 1:
                    put(X, Y, WHITE)
                elif pattern == "speckled" and rnd.random() < 0.18:
                    put(X, Y, light if rnd.random() < 0.5 else dark)
                elif pattern == "checkered" and ((x // 2) + (y // 2)) % 2 == 0:
                    put(X, Y, light)
                elif pattern == "zigzag" and (y + abs((x % 6) - 3)) % 5 == 0:
                    put(X, Y, light)
                elif pattern == "camo" and rnd.random() < 0.35:
                    put(X, Y, [dark, mix(c, (80, 110, 50), 0.5), light][rnd.randrange(3)])
                elif pattern == "marble" and (x + 2 * y + rnd.randrange(2)) % 7 == 0:
                    put(X, Y, WHITE)
                elif pattern == "plaid" and (x % 5 == 0 or y % 5 == 0):
                    put(X, Y, dark if (x % 5 == 0 and y % 5 == 0) else mix(c, BLACK, 0.2))
                elif pattern == "ringed" and x % 4 == 0:
                    put(X, Y, light)
                elif pattern == "tie_dye":
                    hue = ((x * 0.07 + y * 0.05 + ((x - 8) ** 2 + (y - 5) ** 2) ** 0.5 * 0.06) % 1.0)
                    r, g, b = colorsys.hsv_to_rgb(hue, 0.55, 1.0)
                    put(X, Y, mix(c, (r * 255, g * 255, b * 255), 0.6))
                elif pattern == "hearts" and (x % 6, y % 5) in ((1, 1), (3, 1), (1, 2), (2, 2), (3, 2), (2, 3)):
                    put(X, Y, (255, 90, 150) if sum(c) > 380 else (255, 200, 225))
                elif pattern in ("glitter", "galaxy", "starry") and rnd.random() < (0.06 if pattern == "glitter" else 0.05):
                    put(X, Y, (255, 250, 200) if pattern == "starry" else WHITE)
