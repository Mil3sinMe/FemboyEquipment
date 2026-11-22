"""Emblem glyphs for FemboyEquipment users (usage: python3 emblem.py <repo root>)."""
import json, os, sys
from PIL import Image
A = os.path.join(sys.argv[1], "src/main/resources/assets/femboyequipment")
PAL = {"d": (176, 48, 112), "p": (240, 120, 176), "l": (255, 190, 222), "k": (214, 82, 148),
       "y": (255, 208, 64), "o": (190, 128, 30), "g": (240, 90, 170), "b": (110, 200, 255), "w": (255, 255, 255),
       # badge colors
       "D": (24, 22, 32), "N": (40, 140, 70), "M": (130, 220, 140), "R": (230, 50, 60), "C": (90, 224, 208),
       "V": (170, 90, 230), "H": (130, 85, 50), "S": (205, 205, 215), "O": (255, 150, 50), "Q": (70, 120, 230),
       "L": (255, 205, 225)}
GLYPHS = {
    "emblem": [  # pink bow
        "........",
        "dd....dd",
        "dpd..dpd",
        "dlpddpld",
        "dlpkkpld",
        "dpddddpd",
        "dd.dd.dd",
        "..d..d..",
    ],
    "emblem_special": [  # gold crown with trans-colored gems
        "........",
        "w..y..w.",
        "yy.y.yy.",
        "yyyyyyy.",
        "ybygbyy.",
        "yyyyyyy.",
        "ooooooo.",
        "........",
    ],
    # badge emblems (Badge.java), U+E002 onwards
    "badge_developer": ["........", "SSSSSSSS", "SDDDDDDS", "SDbDDDDS", "SDDbDDDS", "SDbDbbDS", "SSSSSSSS", "...SS..."],
    "badge_moderator": ["........", ".NNNNNN.", ".NMMMMN.", ".NMwMMN.", ".NMMMMN.", "..NMMN..", "...NN...", "........"],
    "badge_contributor": ["........", ".dd.dd..", "dlpdppd.", "dpppppd.", ".dpppd..", "..dpd...", "...d....", "........"],
    "badge_artist": ["........", "......HH", ".....HH.", "....HH..", "...SS...", "..VS....", ".VV.....", "VV......"],
    "badge_translator": ["........", ".QQQQQQ.", "QQQQQQQQ", "QwQQwQQw", "QQQQQQQQ", ".QQQQQQ.", ".Q......", "Q......."],
    "badge_media": ["........", ".RRRRRR.", "RRRwRRRR", "RRRwwRRR", "RRRwwwRR", "RRRwwRRR", "RRRwRRRR", ".RRRRRR."],
    "badge_bug_hunter": ["........", ".D....D.", "..DDDD..", "DNMDDNND", ".NNDDNN.", "DNNDDNND", ".NNDDNN.", "..NNNN.."],
    "badge_tester": ["........", "...HH...", "...ww...", "..wCCw..", ".wCCwCw.", ".wCCCCw.", ".wCCCCw.", "..wwww.."],
    "badge_supporter": ["........", "..y..y..", "...yy...", "pppyyppp", "pppyyppp", "LLLyyLLL", "pppyyppp", "pppyyppp"],
    "badge_partner": ["........", ".OOO....", "O...O...", "O...yyy.", ".OOy...y", "...y...y", "....yyy.", "........"],
    "badge_og": ["........", "...yy...", "...yy...", "yyyyyyyy", ".yyyyyy.", "..yyyy..", ".yy..yy.", "yy....yy"],
    "badge_friend": ["........", "..LLLL..", ".LLLLLL.", "LLDLLDLL", "LLLLLLLL", "LDLLLLDL", ".LDDDDL.", "..LLLL.."],
}
for name, rows in GLYPHS.items():
    im = Image.new("RGBA", (8, 8))
    for y, r in enumerate(rows):
        for x, c in enumerate(r[:8]):
            if c != ".":
                im.putpixel((x, y), PAL[c] + (255,))
    os.makedirs(f"{A}/textures/font", exist_ok=True)
    im.save(f"{A}/textures/font/{name}.png")
os.makedirs(f"{A}/font", exist_ok=True)
with open(f"{A}/font/emblem.json", "w") as f:
    json.dump({"providers": [
        {"type": "bitmap", "file": "femboyequipment:font/emblem.png", "ascent": 7, "height": 8, "chars": [""]},
        {"type": "bitmap", "file": "femboyequipment:font/emblem_special.png", "ascent": 7, "height": 8, "chars": [""]},
    ] + [{"type": "bitmap", "file": f"femboyequipment:font/{name}.png", "ascent": 7, "height": 8, "chars": [chr(0xE002 + k)]}
         for k, name in enumerate(n for n in GLYPHS if n.startswith("badge_"))]}, f, indent="\t")
    f.write("\n")
print("emblems done")
