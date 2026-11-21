package com.femboyequipment.api;

import net.minecraft.core.Holder;
import net.minecraft.world.effect.MobEffect;

/**
 * A status effect FemboyEquipment keeps topped up while something is worn or held.
 *
 * @param effect    the effect, e.g. {@code MobEffects.SPEED}
 * @param amplifier 0 = level I, 1 = level II, ...
 */
public record OutfitEffect(Holder<MobEffect> effect, int amplifier) {
	public static OutfitEffect of(Holder<MobEffect> effect, int amplifier) {
		return new OutfitEffect(effect, amplifier);
	}
}
