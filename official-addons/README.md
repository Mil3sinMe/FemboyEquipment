# Official addons 🧩

30 official FemboyEquipment addons. Each one is its own small Fabric mod (its own jar) with **exactly 100 new things**
and its **own creative tab** and **advancement tab**. **Since FemboyEquipment 1.16.0 all 30 ship inside the main jar**
(jar-in-jar), so players don't need to install them separately. The single addon jars are still attached to each
release if someone wants only some of them (next to FemboyEquipment 1.13.0+ and Fabric API).
The full list is in [LIST.md](LIST.md).

## What's in every addon (100 things)

| Group | Count | What |
|---|---|---|
| Materials | 4 | the gem, raw chunk, nugget, dust |
| Ore & storage | 4 | ore + deepslate ore (generates in the Overworld, Fortune/Silk Touch work), block of gem, block of raw gem |
| Building | 20 | bricks, tiles, polished, cobbled and mosaic blocks, each with stairs, slab and wall |
| Fun blocks | 10 | lamp (light 15), cushion, crate, pillar, chiseled (heart), shingles, quilt block, glazed, starry (glows), sparkling (glows) |
| Tools | 6 | sword, pickaxe, axe, shovel, hoe, spear (iron, diamond or netherite tier depending on the addon) |
| Weapons | 4 | knockback weapons (a bat, a hammer, a scythe and a wand), each with its own name and hit sound |
| Armor | 4 | helmet, chestplate, leggings, boots, plus a **full set bonus** |
| Food | 12 | soda, cookie, cupcake, candy, soup, donut, popsicle, lollipop, macaron, pie, bun, jelly, each with an effect |
| Charms | 12 | hold in your offhand or wear in the Trinkets **necklace** slot for an effect |
| Plushies | 10 | 5 Blåhaj + 5 fih (they also join FemboyEquipment's plushie tabs, and one of each is a capsule prize) |
| Stickers | 14 | collectible stickers |

Plus **102 advancements per addon**: one per thing (in one row per group), the tab root, and a
*Completionist* challenge for collecting all 100. Everything has a crafting recipe (ore and raw drops come from mining).

## Building

```bash
./gradlew build                                       # everything; addon jars land in official-addons/<name>/build/libs
./gradlew :official-addons:strawberry_shortcake:build # just one
./gradlew -PaddonTestbed :official-addons:testbed:runClient   # dev game with all 30 addons loaded
```

## Editing / regenerating

Everything here (Java, textures, models, recipes, loot, tags, worldgen, advancements, lang) is **generated** by
[`tools/generators/official_addons.py`](../tools/generators/official_addons.py) from the themes in
[`tools/generators/addon_themes.py`](../tools/generators/addon_themes.py). Change those and rerun:

```bash
python3 tools/generators/official_addons.py .
```

Each addon uses `com.femboyequipment.api.AddonKit` (see [ADDONS.md](../ADDONS.md)), so its Java is a list of one-liners.
