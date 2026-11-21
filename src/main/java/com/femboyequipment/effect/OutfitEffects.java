package com.femboyequipment.effect;

import com.femboyequipment.item.ModItems;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.core.Holder;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.Item;

/** Gives players buffs for wearing the outfit or holding accessories in their offhand. */
public final class OutfitEffects {
	private static final int CHECK_INTERVAL = 20;
	private static final int DURATION = 60;
	// Night vision starts flashing under 10 seconds, so keep it topped up above that.
	private static final int NIGHT_VISION_DURATION = 260;

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
		boolean ears = wearing(player, EquipmentSlot.HEAD, ModItems.CAT_EARS);
		boolean hoodie = wearing(player, EquipmentSlot.CHEST, ModItems.FEMBOY_HOODIE);
		boolean skirt = wearing(player, EquipmentSlot.LEGS, ModItems.PLEATED_SKIRT);
		boolean thighHighs = wearing(player, EquipmentSlot.FEET, ModItems.THIGH_HIGHS);

		if (ears) {
			give(player, MobEffects.NIGHT_VISION, 0, NIGHT_VISION_DURATION);
		}
		if (hoodie) {
			give(player, MobEffects.REGENERATION, 0);
		}
		if (skirt) {
			give(player, MobEffects.SPEED, 0);
		}
		if (ears && hoodie && skirt && thighHighs) {
			// Full outfit bonus~
			give(player, MobEffects.LUCK, 1);
			give(player, MobEffects.HERO_OF_THE_VILLAGE, 0);
		}
		if (thighHighs) {
			// OP as fuck, as requested.
			give(player, MobEffects.SPEED, 2);
			give(player, MobEffects.HASTE, 2);
			give(player, MobEffects.STRENGTH, 2);
			give(player, MobEffects.RESISTANCE, 2);
			give(player, MobEffects.JUMP_BOOST, 1);
			give(player, MobEffects.REGENERATION, 1);
			give(player, MobEffects.FIRE_RESISTANCE, 0);
			give(player, MobEffects.WATER_BREATHING, 0);
			give(player, MobEffects.DOLPHINS_GRACE, 0);
			give(player, MobEffects.SATURATION, 0);
			if (player.isShiftKeyDown() && !player.onGround()) {
				give(player, MobEffects.SLOW_FALLING, 0);
			}
			player.fallDistance = 0;
		}

		Item offhand = player.getItemBySlot(EquipmentSlot.OFFHAND).getItem();
		if (offhand == ModItems.PROGRAMMING_SOCKS) {
			give(player, MobEffects.HASTE, 1);
		} else if (offhand == ModItems.HAIR_CLIP) {
			give(player, MobEffects.LUCK, 0);
		} else if (offhand == ModItems.CHOKER) {
			give(player, MobEffects.STRENGTH, 0);
		}
	}

	private static boolean wearing(ServerPlayer player, EquipmentSlot slot, Item item) {
		return player.getItemBySlot(slot).is(item);
	}

	private static void give(ServerPlayer player, Holder<MobEffect> effect, int amplifier) {
		give(player, effect, amplifier, DURATION);
	}

	private static void give(ServerPlayer player, Holder<MobEffect> effect, int amplifier, int duration) {
		MobEffectInstance current = player.getEffect(effect);
		// Don't override a stronger effect from somewhere else (potions, beacons...).
		if (current != null && current.getAmplifier() > amplifier) {
			return;
		}
		player.addEffect(new MobEffectInstance(effect, duration, amplifier, true, false, true));
	}
}
