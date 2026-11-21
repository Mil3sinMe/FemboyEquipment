# Making FemboyEquipment addons 🎀

FemboyEquipment (1.12.2+) can be extended in two ways:

1. **Datapack addons** (no coding): give items outfit effects, add set bonuses, add capsule prizes, tag plushies.
2. **Mod addons** (Java, Fabric): register new Blåhaj and fih plushies, outfit pieces with effects and set
   bonuses, and reuse FemboyEquipment's 3D ears, tails and skirts with your own textures.

A complete working example lives in [`example-addon/`](example-addon). It adds Fox Ears (3D fox ears + tail,
Speed, a set bonus), a Fox Blåhaj, a Fox Fih, and a datapack effect: wearing a carved pumpkin gives Night Vision.

## Installing addons (players)

Put the addon's `.jar` in your `mods` folder next to FemboyEquipment and Fabric API. Datapack addons go in your world's
`datapacks` folder (or inside a mod).

---

## 1. Datapack addons

### Outfit effects

`data/<your_namespace>/femboyequipment/outfit_effects/<anything>.json`

```json
{
  "type": "worn",
  "items": ["minecraft:carved_pumpkin"],
  "effects": [
    { "id": "minecraft:night_vision", "amplifier": 0 }
  ]
}
```

| `type` | When the effects apply |
|---|---|
| `worn` | While any listed item is worn in an armor slot |
| `accessory` | While any listed item is held in the offhand or worn in a Trinkets slot |
| `set` | While **all** listed items are worn at the same time |

`amplifier` 0 = level I, 1 = level II, … Works with any item from any mod, including vanilla. Reloads with `/reload`.

### Capsule prizes

Add items to these item tags to make them extra gacha prizes:

- `femboyequipment:blahaj_capsule_prizes`
- `femboyequipment:fih_capsule_prizes`

```json
// data/femboyequipment/tags/item/fih_capsule_prizes.json
{ "replace": false, "values": ["minecraft:tropical_fish"] }
```

### Other useful tags

| Tag | Meaning |
|---|---|
| `femboyequipment:blahaj` | Fits the Trinkets back slot, counts for the *Shark Hat* advancement |
| `femboyequipment:fih` | Counts for the fih. advancements |
| `minecraft:dyeable` | Works for your armor items too (FemboyEquipment's outfit uses it) |

---

## 2. Mod addons (Java)

### Setup

Start from [`example-addon/`](example-addon) or a normal [Fabric template mod](https://fabricmc.net/develop/template/)
for **Minecraft 1.21.11** (Fabric Loader 0.18.4+, Loom 1.19, Java 25 to build). Then:

1. Download the FemboyEquipment jar (and, optionally, the `-sources.jar` for docs in your IDE) from the
   [Releases page](../../releases) into a `libs/` folder.
2. In `build.gradle`:
   ```groovy
   dependencies {
       modImplementation files("libs/femboyequipment-1.12.2.jar")
   }
   ```
3. In `fabric.mod.json`:
   ```json
   "depends": { "femboyequipment": ">=1.12.2" },
   "entrypoints": {
     "femboyequipment": ["com.example.MyAddon"],
     "femboyequipment-client": ["com.example.MyAddonClient"]
   }
   ```

The `femboyequipment` entrypoint runs right after FemboyEquipment has registered everything, so the API is ready
and registries are still open. You can register your own items and blocks there.

### The API (`com.femboyequipment.api.FemboyEquipmentApi`)

```java
public class MyAddon implements FemboyEquipmentAddon {
    @Override
    public void onFemboyEquipmentInit() {
        // effects for your own (or anyone's) items
        FemboyEquipmentApi.addWornEffect(MY_EARS, OutfitEffect.of(MobEffects.SPEED, 0));
        FemboyEquipmentApi.addAccessoryEffect(MY_NECKLACE, OutfitEffect.of(MobEffects.LUCK, 0));
        FemboyEquipmentApi.addOutfitSet(List.of(MY_EARS, ModItems.FEMBOY_HOODIE), OutfitEffect.of(MobEffects.JUMP_BOOST, 1));

        // plushies: placeable, wearable as hats, cuddle Regeneration, in the creative tabs and capsules
        Block fox = FemboyEquipmentApi.registerBlahaj(Identifier.fromNamespaceAndPath("myaddon", "fox_blahaj"));
        Block fih = FemboyEquipmentApi.registerFih(Identifier.fromNamespaceAndPath("myaddon", "fox_fih"), 8); // glows

        // extra capsule prizes, creative tab keys
        FemboyEquipmentApi.addCapsulePrize(FemboyEquipmentApi.Capsule.BLAHAJ, MY_EARS);
        ItemGroupEvents.modifyEntriesEvent(FemboyEquipmentApi.MAIN_TAB).register(e -> e.accept(MY_EARS));
    }
}
```

| Method | What it does |
|---|---|
| `addWornEffect(item, effects...)` | Effects while the item is worn in an armor slot |
| `addAccessoryEffect(item, effects...)` | Effects while held in the offhand or worn in a Trinkets slot |
| `addOutfitSet(pieces, effects...)` | Bonus while all pieces are worn |
| `registerBlahaj(id[, light])` / `registerFih(id[, light])` | Register a plushie block + item |
| `addCapsulePrize(capsule, item)` | Extra gacha prize |
| `isPlushie(stack)` | True for any Blåhaj/fih (yours too) |
| `MAIN_TAB`, `BLAHAJ_TAB`, `FIH_TAB` | Creative tab keys |
| `API_VERSION` | Bumped on breaking changes (currently `1`) |

### Plushie assets

For a plushie with id `myaddon:fox_blahaj`, provide:

- `assets/myaddon/models/block/fox_blahaj.json`:
  ```json
  { "parent": "femboyequipment:block/blahaj_base", "textures": { "shark": "myaddon:block/fox_blahaj" } }
  ```
  (for fih: `"parent": "femboyequipment:block/fih_base"` with a `"fih"` texture)
- `assets/myaddon/textures/block/fox_blahaj.png`: a 32×32 texture. Easiest is to copy one of FemboyEquipment's
  (`textures/block/blahaj/*.png` or `textures/block/fih/*.png`) and recolor it, since the layout must match.
- `assets/myaddon/blockstates/fox_blahaj.json` with `facing=north|east|south|west` variants (y = 0/90/180/270)
- `assets/myaddon/items/fox_blahaj.json` pointing at the block model
- `data/myaddon/loot_table/blocks/fox_blahaj.json`
- a translation `block.myaddon.fox_blahaj`

### 3D accessories (client, `com.femboyequipment.api.client.FemboyEquipmentClientApi`)

Reuse FemboyEquipment's 3D models on players, mannequins and Femboy Traders while your item is worn:

```java
public class MyAddonClient implements FemboyEquipmentClientAddon {
    @Override
    public void onFemboyEquipmentClientInit() {
        FemboyEquipmentClientApi.registerAccessory(MY_EARS, AccessoryShape.CAT_EARS,
                Identifier.fromNamespaceAndPath("myaddon", "textures/entity/accessory/fox_ears.png"),
                Identifier.fromNamespaceAndPath("myaddon", "textures/entity/accessory/fox_ears_overlay.png"), // or null
                0xFFFFFF); // tint when undyed; 0xFFFFFF = no tint
    }
}
```

Shapes: `CAT_EARS`, `CAT_TAIL`, `BUNNY_EARS`, `BUNNY_TAIL` (16×16 textures) and `SKIRT` (64×32). Copy the matching
texture from `femboyequipment:textures/entity/accessory/` to get the UV layout. The base texture is tinted with the
item's dye color, and the optional overlay is drawn on top untinted. Register several shapes for one item to combine
them (e.g. ears + tail).

### Building the example addon in this repo

```bash
./gradlew :example-addon:build        # jar in example-addon/build/libs
./gradlew :example-addon:runClient    # game with FemboyEquipment + the example addon
```
