package com.femboyequipment.effect;

import com.femboyequipment.block.Blahaj;
import com.femboyequipment.compat.TrinketsCompat;
import com.femboyequipment.entity.ModEntities;
import net.minecraft.world.entity.animal.feline.Cat;
import com.femboyequipment.item.ModItems;
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
import net.minecraft.world.item.Item;

/** Gives players buffs for wearing outfit pieces, full sets, or holding accessories in their offhand. */
public final class OutfitEffects {
	private static final int CHECK_INTERVAL = 20;
	private static final int DURATION = 60;
	// Night vision starts flashing under 10 seconds, so keep it topped up above that.
	private static final int NIGHT_VISION_DURATION = 260;

	private record Buff(Holder<MobEffect> effect, int amplifier) {
	}

	private record OutfitSet(List<Item> pieces, List<Buff> bonus) {
	}

	private static Buff buff(Holder<MobEffect> effect, int amplifier) {
		return new Buff(effect, amplifier);
	}

	/** Effects for wearing a single piece. */
	private static final Map<Item, List<Buff>> WORN = Map.ofEntries(
			Map.entry(ModItems.CAT_EARS, List.of(buff(MobEffects.NIGHT_VISION, 0))),
			Map.entry(ModItems.FEMBOY_HOODIE, List.of(buff(MobEffects.REGENERATION, 0))),
			Map.entry(ModItems.PLEATED_SKIRT, List.of(buff(MobEffects.SPEED, 0))),
			// OP as fuck, as requested.
			Map.entry(ModItems.THIGH_HIGHS, List.of(
					buff(MobEffects.SPEED, 2), buff(MobEffects.HASTE, 2), buff(MobEffects.STRENGTH, 2),
					buff(MobEffects.RESISTANCE, 2), buff(MobEffects.JUMP_BOOST, 1), buff(MobEffects.REGENERATION, 1),
					buff(MobEffects.FIRE_RESISTANCE, 0), buff(MobEffects.WATER_BREATHING, 0),
					buff(MobEffects.DOLPHINS_GRACE, 0), buff(MobEffects.SATURATION, 0))),
			Map.entry(ModItems.MAID_HEADBAND, List.of(buff(MobEffects.HASTE, 0))),
			Map.entry(ModItems.MAID_DRESS, List.of(buff(MobEffects.RESISTANCE, 0))),
			Map.entry(ModItems.MAID_APRON, List.of(buff(MobEffects.FIRE_RESISTANCE, 0))),
			Map.entry(ModItems.MARY_JANES, List.of(buff(MobEffects.SPEED, 0))),
			Map.entry(ModItems.BUNNY_EARS, List.of(buff(MobEffects.JUMP_BOOST, 0))),
			Map.entry(ModItems.BUNNY_HOODIE, List.of(buff(MobEffects.REGENERATION, 0))),
			Map.entry(ModItems.FLUFFY_SLIPPERS, List.of(buff(MobEffects.JUMP_BOOST, 1))));

	private static final List<OutfitSet> SETS = List.of(
			new OutfitSet(List.of(ModItems.CAT_EARS, ModItems.FEMBOY_HOODIE, ModItems.PLEATED_SKIRT, ModItems.THIGH_HIGHS),
					List.of(buff(MobEffects.LUCK, 1), buff(MobEffects.HERO_OF_THE_VILLAGE, 0))),
			new OutfitSet(List.of(ModItems.MAID_HEADBAND, ModItems.MAID_DRESS, ModItems.MAID_APRON, ModItems.MARY_JANES),
					List.of(buff(MobEffects.HASTE, 1), buff(MobEffects.STRENGTH, 0))),
			new OutfitSet(List.of(ModItems.BUNNY_EARS, ModItems.BUNNY_HOODIE, ModItems.FLUFFY_SLIPPERS),
					List.of(buff(MobEffects.SPEED, 1), buff(MobEffects.JUMP_BOOST, 2))));

	/** Hold one of these in your offhand (or wear it in a Trinkets slot) for a little buff. */
	private static final Map<Item, Buff> OFFHAND = Map.of(
			ModItems.PROGRAMMING_SOCKS, buff(MobEffects.HASTE, 1),
			ModItems.HAIR_CLIP, buff(MobEffects.LUCK, 0),
			ModItems.CHOKER, buff(MobEffects.STRENGTH, 0));

	private static final EquipmentSlot[] ARMOR_SLOTS = {
			EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET};

	private OutfitEffects() {
	}

	public static void initialize() {
		ServerTickEvents.END_SERVER_TICK.register(OutfitEffects::tick);
	}

	private static void tick(MinecraftServer server) {
		if (server.getTickCount() % CHECK_INTERVAL != 0) {
			return;
		}
		for (ServerPlayer player : server.getPlayerList().getPlayers()) {
			apply(player);
		}
	}

	private static void apply(ServerPlayer player) {
		for (EquipmentSlot slot : ARMOR_SLOTS) {
			List<Buff> buffs = WORN.get(player.getItemBySlot(slot).getItem());
			if (buffs != null) {
				buffs.forEach(b -> give(player, b));
			}
		}

		for (OutfitSet set : SETS) {
			if (set.pieces().stream().allMatch(piece -> isWearing(player, piece))) {
				set.bonus().forEach(b -> give(player, b));
			}
		}

		// Accessories work held in your offhand, or worn in a Trinkets slot if Trinkets is installed.
		Item offhandItem = player.getItemBySlot(EquipmentSlot.OFFHAND).getItem();
		OFFHAND.forEach((item, buff) -> {
			if (offhandItem == item || TrinketsCompat.isEquipped(player, stack -> stack.is(item))) {
				give(player, buff);
			}
		});

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

	private static void give(ServerPlayer player, Buff buff) {
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
