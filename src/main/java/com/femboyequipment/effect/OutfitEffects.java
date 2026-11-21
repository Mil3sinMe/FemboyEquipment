package com.femboyequipment.effect;

import com.femboyequipment.api.OutfitEffect;
import com.femboyequipment.block.Blahaj;
import com.femboyequipment.compat.TrinketsCompat;
import com.femboyequipment.entity.ModEntities;
import com.femboyequipment.item.ModItems;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.Holder;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.animal.feline.Cat;
import net.minecraft.world.item.Item;

/**
 * Gives players buffs for wearing outfit pieces, full sets, or holding/wearing accessories.
 *
 * <p>There are two layers of effect tables: the ones registered in code (FemboyEquipment itself and
 * addon mods, via {@code FemboyEquipmentApi}) and the ones loaded from datapacks
 * ({@link OutfitEffectsData}), which are cleared and reloaded with {@code /reload}.
 */
public final class OutfitEffects {
	private static final int CHECK_INTERVAL = 20;
	private static final int DURATION = 60;
	// Night vision starts flashing under 10 seconds, so keep it topped up above that.
	private static final int NIGHT_VISION_DURATION = 260;

	private record OutfitSet(List<Item> pieces, List<OutfitEffect> bonus) {
	}

	// registered in code (built-in + addon mods)
	private static final Map<Item, List<OutfitEffect>> WORN = new LinkedHashMap<>();
	private static final Map<Item, List<OutfitEffect>> ACCESSORY = new LinkedHashMap<>();
	private static final List<OutfitSet> SETS = new ArrayList<>();
	// loaded from datapacks
	private static final Map<Item, List<OutfitEffect>> DATA_WORN = new LinkedHashMap<>();
	private static final Map<Item, List<OutfitEffect>> DATA_ACCESSORY = new LinkedHashMap<>();
	private static final List<OutfitSet> DATA_SETS = new ArrayList<>();

	private static final EquipmentSlot[] ARMOR_SLOTS = {
			EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET};

	private OutfitEffects() {
	}

	private static OutfitEffect buff(Holder<MobEffect> effect, int amplifier) {
		return new OutfitEffect(effect, amplifier);
	}

	public static void initialize() {
		registerBuiltIns();
		ServerTickEvents.END_SERVER_TICK.register(OutfitEffects::tick);
	}

	private static void registerBuiltIns() {
		addWorn(ModItems.CAT_EARS, List.of(buff(MobEffects.NIGHT_VISION, 0)));
		addWorn(ModItems.FEMBOY_HOODIE, List.of(buff(MobEffects.REGENERATION, 0)));
		addWorn(ModItems.PLEATED_SKIRT, List.of(buff(MobEffects.SPEED, 0)));
		// OP as fuck, as requested.
		addWorn(ModItems.THIGH_HIGHS, List.of(
				buff(MobEffects.SPEED, 2), buff(MobEffects.HASTE, 2), buff(MobEffects.STRENGTH, 2),
				buff(MobEffects.RESISTANCE, 2), buff(MobEffects.JUMP_BOOST, 1), buff(MobEffects.REGENERATION, 1),
				buff(MobEffects.FIRE_RESISTANCE, 0), buff(MobEffects.WATER_BREATHING, 0),
				buff(MobEffects.DOLPHINS_GRACE, 0), buff(MobEffects.SATURATION, 0)));
		addWorn(ModItems.MAID_HEADBAND, List.of(buff(MobEffects.HASTE, 0)));
		addWorn(ModItems.MAID_DRESS, List.of(buff(MobEffects.RESISTANCE, 0)));
		addWorn(ModItems.MAID_APRON, List.of(buff(MobEffects.FIRE_RESISTANCE, 0)));
		addWorn(ModItems.MARY_JANES, List.of(buff(MobEffects.SPEED, 0)));
		addWorn(ModItems.BUNNY_EARS, List.of(buff(MobEffects.JUMP_BOOST, 0)));
		addWorn(ModItems.BUNNY_HOODIE, List.of(buff(MobEffects.REGENERATION, 0)));
		addWorn(ModItems.FLUFFY_SLIPPERS, List.of(buff(MobEffects.JUMP_BOOST, 1)));

		addSet(List.of(ModItems.CAT_EARS, ModItems.FEMBOY_HOODIE, ModItems.PLEATED_SKIRT, ModItems.THIGH_HIGHS),
				List.of(buff(MobEffects.LUCK, 1), buff(MobEffects.HERO_OF_THE_VILLAGE, 0)));
		addSet(List.of(ModItems.MAID_HEADBAND, ModItems.MAID_DRESS, ModItems.MAID_APRON, ModItems.MARY_JANES),
				List.of(buff(MobEffects.HASTE, 1), buff(MobEffects.STRENGTH, 0)));
		addSet(List.of(ModItems.BUNNY_EARS, ModItems.BUNNY_HOODIE, ModItems.FLUFFY_SLIPPERS),
				List.of(buff(MobEffects.SPEED, 1), buff(MobEffects.JUMP_BOOST, 2)));
		addSet(List.of(ModItems.ROSE_QUARTZ_HELMET, ModItems.ROSE_QUARTZ_CHESTPLATE, ModItems.ROSE_QUARTZ_LEGGINGS,
				ModItems.ROSE_QUARTZ_BOOTS), List.of(buff(MobEffects.RESISTANCE, 0), buff(MobEffects.HASTE, 0)));

		// Hold one of these in your offhand (or wear it in a Trinkets slot) for a little buff.
		addAccessory(ModItems.PROGRAMMING_SOCKS, List.of(buff(MobEffects.HASTE, 1)));
		addAccessory(ModItems.HAIR_CLIP, List.of(buff(MobEffects.LUCK, 0)));
		addAccessory(ModItems.CHOKER, List.of(buff(MobEffects.STRENGTH, 0)));
	}

	// ------------------------------------------------------------ registration (code)

	public static synchronized void addWorn(Item item, List<OutfitEffect> effects) {
		WORN.computeIfAbsent(item, k -> new ArrayList<>()).addAll(effects);
	}

	public static synchronized void addAccessory(Item item, List<OutfitEffect> effects) {
		ACCESSORY.computeIfAbsent(item, k -> new ArrayList<>()).addAll(effects);
	}

	public static synchronized void addSet(List<Item> pieces, List<OutfitEffect> effects) {
		SETS.add(new OutfitSet(List.copyOf(pieces), List.copyOf(effects)));
	}

	// ------------------------------------------------------------ registration (datapacks)

	static synchronized void clearData() {
		DATA_WORN.clear();
		DATA_ACCESSORY.clear();
		DATA_SETS.clear();
	}

	static synchronized void addWornData(Item item, List<OutfitEffect> effects) {
		DATA_WORN.computeIfAbsent(item, k -> new ArrayList<>()).addAll(effects);
	}

	static synchronized void addAccessoryData(Item item, List<OutfitEffect> effects) {
		DATA_ACCESSORY.computeIfAbsent(item, k -> new ArrayList<>()).addAll(effects);
	}

	static synchronized void addSetData(List<Item> pieces, List<OutfitEffect> effects) {
		DATA_SETS.add(new OutfitSet(List.copyOf(pieces), List.copyOf(effects)));
	}

	// ------------------------------------------------------------ ticking

	private static void tick(MinecraftServer server) {
		if (server.getTickCount() % CHECK_INTERVAL != 0) {
			return;
		}
		for (ServerPlayer player : server.getPlayerList().getPlayers()) {
			apply(player);
		}
	}

	private static synchronized void apply(ServerPlayer player) {
		for (EquipmentSlot slot : ARMOR_SLOTS) {
			Item worn = player.getItemBySlot(slot).getItem();
			giveAll(player, WORN.get(worn));
			giveAll(player, DATA_WORN.get(worn));
		}

		for (List<OutfitSet> sets : List.of(SETS, DATA_SETS)) {
			for (OutfitSet set : sets) {
				if (set.pieces().stream().allMatch(piece -> isWearing(player, piece))) {
					giveAll(player, set.bonus());
				}
			}
		}

		// Accessories work held in your offhand, or worn in a Trinkets slot.
		Item offhandItem = player.getItemBySlot(EquipmentSlot.OFFHAND).getItem();
		for (Map<Item, List<OutfitEffect>> table : List.of(ACCESSORY, DATA_ACCESSORY)) {
			table.forEach((item, effects) -> {
				if (offhandItem == item || TrinketsCompat.isEquipped(player, stack -> stack.is(item))) {
					giveAll(player, effects);
				}
			});
		}

		// Hugging a Blåhaj (in either hand, or wearing one as a hat) is very comforting.
		if (Blahaj.is(player.getMainHandItem()) || Blahaj.is(player.getOffhandItem())
				|| Blahaj.is(player.getItemBySlot(EquipmentSlot.HEAD)) || TrinketsCompat.isEquipped(player, Blahaj::is)) {
			give(player, buff(MobEffects.REGENERATION, 0));
		}

		// A tamed pink kitty nearby purrs you back to health.
		boolean kitty = !player.level().getEntitiesOfClass(Cat.class, player.getBoundingBox().inflate(8.0),
				cat -> cat.isTame() && cat.isOwnedBy(player) && cat.getVariant().is(ModEntities.PINK_CAT)).isEmpty();
		if (kitty) {
			give(player, buff(MobEffects.REGENERATION, 0));
			give(player, buff(MobEffects.LUCK, 0));
		}

		// Soft landings: thigh highs and bunny slippers cancel fall damage.
		Item feet = player.getItemBySlot(EquipmentSlot.FEET).getItem();
		if (feet == ModItems.THIGH_HIGHS || feet == ModItems.FLUFFY_SLIPPERS) {
			player.fallDistance = 0;
		}
		if (feet == ModItems.THIGH_HIGHS && player.isShiftKeyDown() && !player.onGround()) {
			give(player, buff(MobEffects.SLOW_FALLING, 0));
		}
	}

	private static boolean isWearing(ServerPlayer player, Item item) {
		for (EquipmentSlot slot : ARMOR_SLOTS) {
			if (player.getItemBySlot(slot).is(item)) {
				return true;
			}
		}
		return false;
	}

	private static void giveAll(ServerPlayer player, List<OutfitEffect> effects) {
		if (effects != null) {
			effects.forEach(e -> give(player, e));
		}
	}

	private static void give(ServerPlayer player, OutfitEffect buff) {
		Holder<MobEffect> effect = buff.effect();
		MobEffectInstance current = player.getEffect(effect);
		// Don't override a stronger effect from somewhere else (potions, beacons, another piece...).
		if (current != null && current.getAmplifier() > buff.amplifier()) {
			return;
		}
		int duration = effect.equals(MobEffects.NIGHT_VISION) ? NIGHT_VISION_DURATION : DURATION;
		player.addEffect(new MobEffectInstance(effect, duration, buff.amplifier(), true, false, true));
	}
}
