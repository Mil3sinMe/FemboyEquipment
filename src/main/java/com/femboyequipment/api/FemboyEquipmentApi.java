package com.femboyequipment.api;

import com.femboyequipment.block.Blahaj;
import com.femboyequipment.block.Fih;
import com.femboyequipment.effect.OutfitEffects;
import com.femboyequipment.item.CapsuleItem;
import com.femboyequipment.item.ModItemGroups;
import java.util.List;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.block.Block;

/**
 * The public API for FemboyEquipment addons. Everything here is stable: if it changes in a
 * breaking way, {@link #API_VERSION} goes up.
 *
 * <p>Most things can also be done with a plain datapack, no code needed: see ADDONS.md.
 */
public final class FemboyEquipmentApi {
	/** Bumped on breaking API changes. */
	public static final int API_VERSION = 1;

	/** The main "Femboy Equipment" creative tab (add entries with Fabric's ItemGroupEvents). */
	public static final ResourceKey<CreativeModeTab> MAIN_TAB = ModItemGroups.MAIN_KEY;
	/** The Blåhaj creative tab. Plushies registered with {@link #registerBlahaj} show up here automatically. */
	public static final ResourceKey<CreativeModeTab> BLAHAJ_TAB = ModItemGroups.BLAHAJ_KEY;
	/** The fih. creative tab. Plushies registered with {@link #registerFih} show up here automatically. */
	public static final ResourceKey<CreativeModeTab> FIH_TAB = ModItemGroups.FIH_KEY;

	public enum Capsule {
		BLAHAJ,
		FIH
	}

	private FemboyEquipmentApi() {
	}

	// ------------------------------------------------------------ effects

	/** Effects given while {@code item} is worn in an armor slot. */
	public static void addWornEffect(Item item, OutfitEffect... effects) {
		OutfitEffects.addWorn(item, List.of(effects));
	}

	/** Effects given while {@code item} is held in the offhand or worn in a Trinkets slot (accessories). */
	public static void addAccessoryEffect(Item item, OutfitEffect... effects) {
		OutfitEffects.addAccessory(item, List.of(effects));
	}

	/** Bonus effects for wearing every item in {@code pieces} at once (in any armor slots). */
	public static void addOutfitSet(List<Item> pieces, OutfitEffect... effects) {
		OutfitEffects.addSet(List.copyOf(pieces), List.of(effects));
	}

	// ------------------------------------------------------------ plushies

	/**
	 * Registers a Blåhaj plushie block + item with the given id (use your own namespace!).
	 * It is placeable, wearable as a hat, gives cuddle Regeneration, fits the Trinkets back slot
	 * (add it to the {@code femboyequipment:blahaj} item tag for that), appears in the Blåhaj tab
	 * and can be pulled from Blåhaj Capsules.
	 *
	 * <p>Assets you provide: {@code blockstates/<name>.json}, {@code items/<name>.json} and a block
	 * model with {@code "parent": "femboyequipment:block/blahaj_base"} and a {@code "shark"} texture.
	 */
	public static Block registerBlahaj(Identifier id) {
		return registerBlahaj(id, 0);
	}

	/** Same as {@link #registerBlahaj(Identifier)}, glowing with the given light level (0-15). */
	public static Block registerBlahaj(Identifier id, int lightLevel) {
		return Blahaj.register(id, lightLevel, false, false);
	}

	/**
	 * Registers a fih (fish in sneakers) plushie. Like {@link #registerBlahaj}, but your block model
	 * uses {@code "parent": "femboyequipment:block/fih_base"} with a {@code "fih"} texture.
	 */
	public static Block registerFih(Identifier id) {
		return registerFih(id, 0);
	}

	public static Block registerFih(Identifier id, int lightLevel) {
		return Fih.register(id, lightLevel, false);
	}

	/** Adds any item as an extra prize to a gacha capsule. */
	public static void addCapsulePrize(Capsule capsule, ItemLike prize) {
		CapsuleItem.addExtraPrize(capsule, prize.asItem());
	}

	/**
	 * Moves this namespace's advancements into the Cute Collection (their own page per advancement tab, Cute Points,
	 * hidden from the vanilla advancement screen). {@link AddonKit} does this automatically for its mod id.
	 */
	public static void addCollectionNamespace(String namespace) {
		com.femboyequipment.collection.CollectionServer.addNamespace(namespace);
	}

	/** True for any Blåhaj or fih plushie, including ones from addons. */
	public static boolean isPlushie(ItemStack stack) {
		return Blahaj.is(stack);
	}
}
