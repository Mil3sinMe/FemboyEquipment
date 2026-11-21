"""Emblem glyphs for FemboyEquipment users (usage: python3 emblem.py <repo root>)."""
import json, os, sys
from PIL import Image
A = os.path.join(sys.argv[1], "src/main/resources/assets/femboyequipment")
PAL = {"d": (176, 48, 112), "p": (240, 120, 176), "l": (255, 190, 222), "k": (214, 82, 148),
       "y": (255, 208, 64), "o": (190, 128, 30), "g": (240, 90, 170), "b": (110, 200, 255), "w": (255, 255, 255)}
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
    ]}, f, indent="\t")
    f.write("\n")
print("emblems done")
