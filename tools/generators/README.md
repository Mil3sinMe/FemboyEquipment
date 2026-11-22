# Content generators

Python scripts (need Pillow) that generate most of FemboyEquipment's assets and data: textures, models, blockstates,
recipes, loot tables, tags, lang entries, the cute house structure, `BlahajVariants.java`, `FihVariants.java` and all
advancements. Run them from the repo root, **in this order** (later ones merge into `en_us.json` and tags):

```bash
G=tools/generators
python3 $G/content.py .        # outfits, accessories, tools, bricks, base lang/tags/recipes
python3 $G/blahaj.py .         # 1000 Blåhaj (uses blahaj_more.py, blahaj_proc.py) -> BlahajVariants.java
python3 $G/phase3.py .         # villager, pink cat, Pastel Bloom, cute house (+ chest loot)
python3 $G/emblem.py .         # emblem font glyphs
python3 $G/gear.py .           # Rose Quartz, sparkly tools, weapons, capsules, pastel bricks + stairs/slabs/walls
python3 $G/fih.py .            # 1000 fih -> FihVariants.java
python3 $G/advancements.py .   # every advancement (uses blahaj_jokes.py, adv_lines.py); asserts full coverage
python3 $G/collection.py .     # Cute Collection: book + rank hats, quest/rank lang, tags
git checkout src/main/resources/data/femboyequipment/structure/cute_house.nbt  # phase3 rewrites it with a new gzip timestamp
```

Notes:
- `content.py` rewrites `en_us.json` from scratch, so always run the whole chain after it.
- `gear.py` reads vanilla blockstate templates from Loom's cache (`~/.gradle/caches/fabric-loom/1.21.11/minecraft-client.jar`);
  run `./gradlew build` once first so it exists.
- `blahaj.py` and `fih.py` write `blahaj_meta.json` / `fih_meta.json` next to the scripts; `advancements.py` reads them.
- `preview.py <outdir>` renders contact sheets of the item/armor textures for a quick visual check.
- `official_addons.py` (+ `addon_themes.py`) is separate from the chain above: it regenerates all 30 addons in
  `official-addons/` (wipes and rewrites each addon folder; doesn't touch the main mod). Run it any time:
  `python3 $G/official_addons.py .`
- The example addon's assets were made by hand (recolored copies of these textures).
