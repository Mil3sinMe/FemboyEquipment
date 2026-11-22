# Changelog 🎀

All versions need **Minecraft 1.21.11**, **Fabric Loader 0.18.4+** and **[Fabric API](https://modrinth.com/mod/fabric-api)**.
Downloads are on the [Releases page](../../releases).

## 1.16.0: All addons included 🎁

### Changed
- **All 30 official addons are now bundled inside the FemboyEquipment jar** (jar-in-jar), so one download has
  everything: 3000 more items and blocks, 30 more Cute Collection pages. Same item IDs as the separate jars, so
  existing worlds keep everything. The separate addon jars are still attached to each release
- Official addons 1.1.1

### Fixed
- The 30 addon *Completionist* challenges finished as soon as you collected **any one** item of that addon (they
  needed one of the 100 items instead of all 100). They now need all 100. The main mod's challenges were already
  correct

## 1.15.1: Fix

### Fixed
- A broken Trinkets slot-sync packet no longer disconnects you ("Packet handling error ... fieldSize is too long!
  Length is 1, but maximum is 0"). This happens when another mod (e.g. a replay recorder like Flashback) reads the
  packet before Trinkets does; the broken update is now skipped with a warning in the log, and the slots catch up
  on the next sync

## 1.15.0: Badges 🏅

### Added
- **Badges**: players listed in [FemboyEquipment-Badge-Users](https://github.com/NeonWardonmc/FemboyEquipment-Badge-Users)
  get badge emblems in front of their name (chat, tab list, name tags): owner, developer, moderator, contributor,
  artist, translator, media, bug hunter, tester, supporter, partner, OG and friend
  - `badges.txt` format: `uuid | badge[,badge...] | backup-username` (the username is used on offline-mode servers)
  - Downloaded on startup and every 30 minutes, cached in `config/femboyequipment-badges-cache.txt` for offline play
  - Up to 3 emblems per player (best first); hover a name in chat to see all badges
- **12 new emblems** (one per badge); the pink bow and the owner crown stay the same
- `/emblem` now also lists your own badges

### Changed
- The people who already had the crown keep it: they're `owner` in the list, and still hardcoded as a fallback

## 1.14.0: Cute Collection 📖

### Added
- **Cute Collection**, a custom advancement system. FemboyEquipment's and all addons' advancements moved out of the
  vanilla advancement screen (no more 30+ tabs, toast floods or chat spam) into their own screen:
  - **Collection** tab: a page per tab/addon, progress bars, every collectible as a grid with tooltips
  - **Ranks** tab: Cute Points (entry 1, group goal 5, full page 25) and 9 ranks from *Smol Bean* to *Ultimate Femboy*;
    thresholds scale with how much content is installed
  - **Quests** tab: 3 daily + 2 weekly quests (real-life reset) built on vanilla stats, with claimable rewards
- Open it with **K** (rebindable), the new **Collection Book** (book + pink dye), a **♥ button** in the inventory, or `/collection`
- **Rewards**: group goal = capsule + material bundle, full page = 6 capsules + big bundle, rank-up = an exclusive hat +
  capsules + XP levels, quests = capsules + XP
- **8 rank-exclusive hats** (head or Trinkets hat slot): Cutie Bow, Sweetheart Halo, Darling Flower Crown,
  Sparkle Star Circlet, Pastel Tiara, Blåhaj Crown, Legendary Rainbow Halo, Ultimate Femboy Crown
- **Rank titles** before your name in chat, the tab list and name tags (can be hidden in the Ranks tab)
- Custom pastel toasts for goals, completions, rank-ups and quests
- API: `FemboyEquipmentApi.addCollectionNamespace(ns)` (AddonKit addons are added automatically), plus optional
  `data/<ns>/loot_table/collection/goal.json` / `challenge.json` reward bundles and the
  `femboyequipment:collection_snacks` / `femboyequipment:collection_ores` quest tags

### Changed
- Official addons 1.1.0: material-bundle rewards and quest tags

## 1.13.0: 30 Official Addons 🎁

### Added
- **30 official addons** in [`official-addons/`](official-addons), each its own mod jar (install any you like) with
  **100 new things**, its own creative tab and its own advancement tab. **3000 things in total**:
  - a new gem with ore + deepslate ore that generates in the Overworld (Fortune and Silk Touch work), raw chunk,
    nugget, dust and storage blocks
  - 20 building blocks (bricks, tiles, polished, cobbled, mosaic + stairs, slabs, walls) and 10 fun blocks
    (lamp, cushion, crate, pillar, chiseled heart, shingles, quilt, glazed, glowing starry and sparkling blocks)
  - sword, pickaxe, axe, shovel, hoe and spear (iron, diamond or netherite tier) and 4 knockback weapons
  - armor with a full set bonus, 12 snacks with effects, 12 charms (offhand or Trinkets necklace slot)
  - 5 Blåhaj + 5 fih plushies (also in the plushie tabs and capsules) and 14 stickers
  - **102 advancements per addon** (3060 total) including a *Completionist* challenge for all 100
  - themes: Strawberry Shortcake, Ocean Dreams, Starlight Sky, Cottagecore Garden, Bubblegum Pop, Lavender Fields,
    Kitty Café, Frosted Winter, Pumpkin Spice, Cherry Blossom, Pastel Goth, Rainbow Pride, Trans Pride, Honey Bee,
    Mushroom Forest, Bunny Meadow, Neon Arcade, Witchy Moon, Dragon Hoard, Cloud Kingdom, Lemonade Summer,
    Mint Chocolate, Space Cadet, Fairy Ring, Boba Tea Shop, Sunset Beach, Axolotl Pond, Royal Ball, Cozy Sleepover,
    Cyber Kitten
- **`AddonKit`** in the addon API: register items, blocks (+ stairs/slab/wall), tools, knockback weapons, armor, food,
  charms, plushies, an Overworld ore and a creative tab in one line each
- Generator scripts `tools/generators/official_addons.py` + `addon_themes.py`; the addon jars are attached to
  releases and kept in `dist/official-addons/`

## 1.12.2: Addons Update 🧩

### Added
- **Addon API** (`com.femboyequipment.api`) for Fabric mods:
  - `FemboyEquipmentApi`: worn effects, accessory effects, outfit set bonuses, register Blåhaj and fih plushies,
    capsule prizes, creative tab keys
  - `FemboyEquipmentClientApi`: reuse the 3D cat ears/tail, bunny ears/tail and skirt with your own textures
  - `femboyequipment` / `femboyequipment-client` entrypoints that run once FemboyEquipment is ready
- **Datapack addons**: `data/<ns>/femboyequipment/outfit_effects/*.json` (`worn`, `accessory`, `set`) for any item,
  plus `femboyequipment:blahaj_capsule_prizes` / `fih_capsule_prizes` tags. Reloads with `/reload`
- **Example addon** (`example-addon/`): Fox Ears with 3D fox ears + tail, a Fox Blåhaj, a Fox Fih, and a datapack effect
  (carved pumpkin = Night Vision)
- **ADDONS.md** guide. Releases now also include the sources jar and the example addon jar

### Changed
- FemboyEquipment's own outfit effects and 3D accessories now go through the same API addons use

## 1.12.1: Advancements for everything 🏆

### Added
- **An advancement for every single item and block**: 2091 in total (up from 187)
  - **fih. tab**: all 1000 fih as a grid (one row per fish, 25 kicks per row) plus *Fih Collector* (all 1000)
  - **New Mystery Blåhaj tab**: all 870 capsule Blåhaj as a grid (one row per pattern) plus *Gacha Legend* (all 870)
  - Every plushie gets its own two-part joke description, e.g. *"Will fight its own reflection. Galaxy kicks, out of this world."*
  - Main tab: every Rose Quartz piece and tool, every brick, stair, slab and wall, and both spawn eggs
- Plushie advancements show a toast but don't spam chat

## 1.12.0: fih. 🐟👟

### Added
- **1000 fih**: a fish standing in high-top sneakers. 40 fish × 25 kicks, own creative and advancement tab
- **870 new Blåhaj (1000 total)**: 29 colors × 30 patterns (striped, polka dot, galaxy, tie-dye, holographic, cursed…)
- **Gacha capsules**: Blåhaj Capsule and Fih Capsule pop out a random plushie (also sold by Femboy Traders)
- **Rose Quartz**: material, block, bricks, full diamond-tier armor (set bonus: Resistance + Haste), sword, pickaxe,
  axe, shovel, hoe and spear
- **Sparkly Axe, Shovel & Hoe**
- **Fih Slapper** and **Blåhaj Bat**: joke weapons with huge knockback
- **Pastel bricks** in blue, lavender, mint and yellow, and stairs, slabs and walls for all pastel and Rose Quartz bricks
- 22 new advancements (gacha pulls, Rose Quartz, the fih. tab…)

## 1.11.0: Trinkets built in 📦

### Changed
- **Trinkets Canary is now bundled inside the mod.** Accessory slots work out of the box with just FemboyEquipment +
  Fabric API, so there's no separate Trinkets download anymore. If you install a newer Trinkets fork yourself, Fabric
  Loader uses the newer one.

## 1.10.0: Accessory slots 🎒

### Added
- **Trinkets support** (optional, works with Trinkets Canary / Trinkets Updated for 1.21.11):
  - **Hat**: Hair Clip, Pink Ribbon
  - **Necklace**: Choker
  - **Back**: any Blåhaj, which shows riding on your back 🦈
  - **Socks** (a new slot): Programming Socks
- Accessory buffs (Luck, Strength, Haste II, Blåhaj cuddle Regeneration) work from Trinkets slots as well as your offhand

## 1.9.0: Pink kitties on demand 🐱

### Added
- **Pink Cat Spawn Egg**: always hatches a pink kitty (in the Femboy Equipment creative tab)
- **A joke for every Blåhaj advancement**: all 95 plain "Get a ___ Blåhaj" descriptions were rewritten, e.g.
  *Swims both ways* (Bi), *Would rather have garlic bread* (Ace), *Orange you glad you found it?* (Orange),
  *A fun guy* (Mushroom), *Touch grass. Hug moss* (Moss), *RAWR XD means I love you in dinosaur. And shark* (Scene)

## 1.8.0: Emblem controls & 100 new Blåhaj 🦈

### Added
- **Emblems in chat**: the 🎀 / 👑 emblem now also shows in front of the sender's name in chat
- **`/emblem` command**: `/emblem share on|off` hides your own emblem, `/emblem display on|off` hides other
  people's. Settings are saved in `config/femboyequipment-client.json`
- **100 new Blåhaj (130 total)**: more pride flags, food, minerals, mobs, nature, sky, aesthetics, elements and
  holidays, each crafted from a classic Blåhaj plus something themed. Star, Sun, Fire and Blaze glow; Fire, Blaze
  and Magma are fire-proof
- **Advancements for every new Blåhaj** (165 total), grouped by theme, plus *The Original 30* and
  *Gotta Hug 'Em All* (all 130)

### Fixed
- Advancement descriptions said "Get **a** Emerald Blåhaj" instead of "an"

## 1.7.1

### Fixed
- The special 👑 crown emblem didn't show on offline-mode ("cracked") servers. It now falls back to the username
  when the server doesn't use real Mojang UUIDs

## 1.7.0: Advancements 🏆

### Added
- **64 advancements** in two tabs:
  - **Femboy Equipment**: one per item, wearing each full outfit, the thigh highs, dyeing, strawberry milk, finding a
    cute house, trading with a Femboy Trader, taming a pink cat, and *Fully Equipped*
  - **Blåhaj Collection**: one per Blåhaj, *Shark Hat*, *Shark Week* and a collect-them-all challenge
- Custom pink quilt and ocean advancement backgrounds

## 1.6.0: Emblems 🎀

### Added
- **Lunar-style emblems**: players who both have FemboyEquipment see a pink bow 🎀 next to each other's names, above
  their heads and in the tab list, **on any server**, with no backend needed
- Special 👑 gold crown emblem for friends of the mod

## 1.5.0: Cute houses, traders & kitties 🏠

### Added
- **Cute houses**: pastel pink houses in plains, meadows, flower forests and cherry groves, with a loot chest
- **Femboy Traders**: dressed in a random outfit, hugging a Blåhaj, trading outfit goodies (and *very* rarely the
  thigh highs). Femboy Trader Spawn Egg
- **Pink cats**: a new cat variant (always in cute houses, sometimes in villages). A tamed one nearby gives
  Regeneration + Luck
- **Pastel Bloom**: a new pink flower that grows in the wild and crafts into pink dye
- Outfit loot in village, dungeon, mineshaft, mansion and shipwreck chests
- Traders show 3D ears, tails and skirts too

## 1.4.0: Blåhaj 🦈

### Added
- **30 Blåhaj shark plushies**: classic, 15 pride flags, 10 colors, Golden, Diamond, Netherite and a glowing Glow
  Blåhaj
- Place them (they look at you), wear one as a hat, or hug one for Regeneration
- Their own Blåhaj creative tab

## 1.3.0: Maid & bunny outfits, 3D accessories 🐰

### Added
- **Maid outfit**: Maid Headband, Maid Dress, Maid Apron, Mary Janes (+ set bonus)
- **Bunny outfit**: Bunny Ears, Bunny Hoodie, Fluffy Slippers (+ set bonus)
- **Real 3D models**: pointy cat ears with a swishing cat tail, floppy bunny ears with a fluffy tail, and flared
  skirts
- Every outfit piece is dyeable

## 1.2.0: Glow-up ✨

### Changed
- Redrew every texture with outlines and shading
- Cheaper Thigh Highs recipe (1 Netherite Ingot, 2 Ribbons, 2 Programming Socks)

### Added
- The cat outfit is dyeable like leather armor

## 1.1.0: The outfit update 👗

### Added
- **Cat outfit**: Cat Ears, Femboy Hoodie, Pleated Skirt and the absurdly OP **Thigh Highs**, each with effects
  while worn, plus a full-set bonus
- Hair Clip, Choker and Programming Socks give buffs in your offhand
- Strawberry Milk, Sparkly Sword, Sparkly Pickaxe, Pastel Pink Bricks and Block of Ribbons
- Crafting recipes for everything
- GitHub Actions builds every version and publishes releases automatically

### Changed
- Fabric Loader requirement lowered to 0.18.4

## 1.0.0: First release 🎀

### Added
- Pink Ribbon and Programming Socks
- Femboy Equipment creative tab
