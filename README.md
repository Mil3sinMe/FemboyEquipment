# FemboyEquipment 🎀

A cute little [Fabric](https://fabricmc.net/) mod for **Minecraft 1.21.11**.

![Outfits in game: cat set (back and front), maid set, bunny set](docs/showcase.png)

## Download

Grab the latest jar from the [Releases page](../../releases/latest) and drop it into your `mods`
folder together with [Fabric API](https://modrinth.com/mod/fabric-api).

## Features

### Cat outfit 🐱

| Piece | Slot | Effect while worn |
|---|---|---|
| **Cat Ears** | Head | Night Vision |
| **Femboy Hoodie** | Chest | Regeneration I |
| **Pleated Skirt** | Legs | Speed I |
| **Thigh Highs** ✨ | Feet | Absolutely broken: Speed III, Haste III, Strength III, Resistance III, Jump Boost II, Regeneration II, Fire Resistance, Water Breathing, Dolphin's Grace, Saturation, no fall damage, slow falling while sneaking mid-air. Unbreakable, fire-proof, 8 armor, 6 toughness. |

Wear all four for a set bonus: **Luck II** + **Hero of the Village** (cheap villager trades~).

### Maid outfit 🖤

| Piece | Slot | Effect while worn |
|---|---|---|
| **Maid Headband** | Head | Haste I |
| **Maid Dress** | Chest | Resistance I |
| **Maid Apron** | Legs | Fire Resistance |
| **Mary Janes** | Feet | Speed I |

Full set bonus: **Haste II** + **Strength I**.

### Bunny outfit 🐰

| Piece | Slot | Effect while worn |
|---|---|---|
| **Bunny Ears** | Head | Jump Boost I |
| **Bunny Hoodie** | Chest | Regeneration I |
| **Fluffy Slippers** | Feet | Jump Boost II, no fall damage |

Full set bonus (all three): **Speed II** + **Jump Boost III**.

### 3D accessories & dyeing

- Cat Ears and Bunny Ears render as real 3D ears, and come with a swishing cat tail / fluffy bunny tail
- The Pleated Skirt and Maid Apron render as flared 3D skirts
- **Every outfit piece is dyeable** like leather armor. Craft it with any dye to recolor it (ears and tails included).

### Blåhaj 🦈

30 squishy shark plushies! Place them on the floor (they look at you), **wear one as a hat**, or **hug one**
(hold it in either hand or wear it) for Regeneration. They have their own creative tab.

- **Classic Blåhaj**: craft with `" C "` · `"CBC"` · `"WWB"` (Cyan Wool, Light Blue Wool, White Wool)
- **Pride flags**: craft a classic Blåhaj with the flag's dyes (shapeless):

| Variant | Extra ingredients |
|---|---|
| Trans | Light Blue, Pink, White dye |
| Pride | Red, Orange, Yellow, Green, Blue, Purple dye |
| Bi | Magenta, Purple, Blue dye |
| Pan | Pink, Yellow, Light Blue dye |
| Lesbian | Orange, White, Magenta dye |
| Gay | Cyan, White, Blue dye |
| Nonbinary | Yellow, White, Purple, Black dye |
| Ace | Black, Gray, White, Purple dye |
| Aro | Green, Lime, White, Gray, Black dye |
| Genderfluid | Pink, White, Purple, Black, Blue dye |
| Agender | Black, Light Gray, White, Lime dye |
| Intersex | Yellow, Purple dye |
| Demiboy | Gray, Light Blue, White dye |
| Demigirl | Gray, Pink, White dye |
| Femboy | Pink, White, Light Blue, Blue dye |

- **Solid colors**: Classic Blåhaj + one dye: Pink, Red, Orange, Yellow, Mint (lime), Purple, Goth (black), Ghost (white), Chocolate (brown), Magenta
- **Fancy**: Classic Blåhaj + Gold Ingot (Golden), Diamond (Diamond), Netherite Scrap (Netherite, fire-proof), Glow Ink Sac (**Glow Blåhaj** glows in the dark!)

### Cute houses, traders & kitties 🏠

![A Femboy Trader in a Pastel Bloom patch next to a cute house, and the house interior](docs/cute_house.png)

- **Cute houses** generate in plains, meadows, flower forests and cherry groves (`/locate structure femboyequipment:cute_house`).
  Pastel pink brick walls, a cherry wood floor, a bed, Blåhajs and a loot chest full of goodies.
- **Femboy Traders** live inside, dressed in a random outfit (cat, maid or bunny) and hugging a Blåhaj.
  Right-click to trade emeralds for ribbons, strawberry milk, outfit pieces, Blåhajs… and, very rarely, *the thigh highs*.
  There's also a Femboy Trader spawn egg.
- **Pink cats**: a new cat variant. Every cute house comes with one, and village cats can be pink too.
  Tame one with fish: while your pink kitty is within 8 blocks it purrs you Regeneration + Luck.
- **Pastel Bloom**: a new pink flower in meadows, plains, flower forests and cherry groves. Craft it into 2 pink dye.
- **Chest loot**: village houses, dungeons, mineshafts, mansions and shipwreck supply chests sometimes hold ribbons,
  strawberry milk, accessories, Blåhajs and the odd outfit piece.

### Emblems 🎀

![Bob's name tag and the tab list showing the FemboyEquipment emblem](docs/emblems.png)

Like Lunar Client's emblem: **players who both have FemboyEquipment see a little pink bow next to each other's
names**, above their heads and in the tab list. It works on **any server**, even vanilla servers without the mod
(you just can't use the mod's items there). Friends of the mod get a special 👑 crown emblem.

How it works: your client sends the server which skin layers you show (hat, jacket, sleeves…) as a byte, and the
server shares it with everyone. Vanilla only uses 7 of those 8 bits, so the mod sets the spare one as a
"has FemboyEquipment" flag. There's no backend server. The tab list remembers players once you've seen them nearby.

### Accessories (hold in your offhand)

- **Programming Socks** – Haste II
- **Hair Clip** – Luck
- **Choker** – Strength I
- **Pink Ribbon** – crafting material

### Other goodies

- **Strawberry Milk** – drink it for Speed II (30s) + Regeneration (10s)
- **Sparkly Sword** & **Sparkly Pickaxe** – diamond-tier, more durable, very enchantable
- **Pastel Pink Bricks** & **Block of Ribbons** – decoration
- A **Femboy Equipment** creative tab holding everything

## Crafting

| Item | Recipe |
|---|---|
| Pink Ribbon ×2 | 2 String + Pink Dye (shapeless) |
| Programming Socks | White Wool / Pink Wool stripes: `W W` · `P P` · `W W` |
| Hair Clip ×2 | Pink Ribbon + Iron Ingot (shapeless) |
| Choker | `SSS` · `S S` · ` D ` (String, Pink Dye) |
| Strawberry Milk ×3 | Milk Bucket + Sweet Berries + Sugar + 3 Glass Bottles (shapeless) |
| Cat Ears | `P P` · `RHR` (Pink Wool, Ribbon, Hair Clip) |
| Femboy Hoodie | `P P` · `PCP` · `PPP` (Pink Wool, Choker) |
| Pleated Skirt | `PRP` · `P P` · `P P` (Pink Wool, Ribbon) |
| Thigh Highs | `RNR` · `S S` (Ribbon, Netherite Ingot, Programming Socks) |
| Maid Headband | `WWW` · `S S` (White Wool, String) |
| Maid Dress | `B B` · `BWB` · `BBB` (Black Wool, White Wool) |
| Maid Apron | `BRB` · `W W` · `W W` (Black Wool, Ribbon, White Wool) |
| Mary Janes | `R R` · `L L` (Ribbon, Leather) |
| Bunny Ears | `H H` · `WRW` (Rabbit Hide, White Wool, Ribbon) |
| Bunny Hoodie | `W W` · `WFW` · `WWW` (White Wool, Rabbit's Foot) |
| Fluffy Slippers | `W W` · `H H` (White Wool, Rabbit Hide) |
| Sparkly Sword | `RDR` · ` D ` · ` S ` (Ribbon, Diamond, Stick) |
| Sparkly Pickaxe | `DDD` · `RSR` · ` S ` (Diamond, Ribbon, Stick) |
| Pastel Pink Bricks ×8 | 8 Bricks around a Pink Dye |
| Block of Ribbons | 9 Pink Ribbons (and back) |

All outfits and the sparkly tools are repaired with Pink Wool or Pink Ribbons.

## Requirements

| Thing | Version |
|---|---|
| Minecraft | 1.21.11 |
| Fabric Loader | ≥ 0.18.4 |
| Fabric API | 0.141.6+1.21.11 |
| Java (to play) | 21+ |
| Java (to build) | 25+ (needed by Fabric Loom 1.19) |

## Building

    ./gradlew build

The mod jar ends up in `build/libs/`. Drop it (plus Fabric API) into your `mods` folder.

## Running in dev

    ./gradlew runClient

## License

MIT
