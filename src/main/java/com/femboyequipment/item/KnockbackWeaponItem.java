package com.femboyequipment.item;

import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

/** A silly melee weapon that sends whatever it hits flying, with a sound to match. */
public class KnockbackWeaponItem extends Item {
	private final float knockback;
	private final SoundEvent hitSound;

	public KnockbackWeaponItem(float knockback, SoundEvent hitSound, Properties properties) {
		super(properties);
		this.knockback = knockback;
		this.hitSound = hitSound;
	}

	@Override
	public void hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
		super.hurtEnemy(stack, target, attacker);
		target.knockback(this.knockback, attacker.getX() - target.getX(), attacker.getZ() - target.getZ());
		target.level().playSound(null, target.blockPosition(), this.hitSound, SoundSource.PLAYERS, 1.0F, 1.0F);
	}
}
