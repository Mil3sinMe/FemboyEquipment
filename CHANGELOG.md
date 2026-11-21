# Changelog 🎀

All versions need **Minecraft 1.21.11**, **Fabric Loader 0.18.4+** and **[Fabric API](https://modrinth.com/mod/fabric-api)**.
Downloads are on the [Releases page](../../releases).

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
