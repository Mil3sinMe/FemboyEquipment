package com.femboyequipment.item;

import java.util.List;
import java.util.function.Supplier;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/** A gacha capsule: right-click to pop out a random plushie from its pool. */
public class CapsuleItem extends Item {
	private final Supplier<List<Item>> pool;

	public CapsuleItem(Supplier<List<Item>> pool, Properties properties) {
		super(properties);
		this.pool = pool;
	}

	@Override
	public InteractionResult use(Level level, Player player, InteractionHand hand) {
		ItemStack capsule = player.getItemInHand(hand);
		if (!level.isClientSide()) {
			List<Item> prizes = this.pool.get();
			ItemStack prize = new ItemStack(prizes.get(level.getRandom().nextInt(prizes.size())));
			player.displayClientMessage(Component.translatable("message.femboyequipment.capsule", prize.getHoverName()), true);
			if (!player.getInventory().add(prize)) {
				player.drop(prize, false);
			}
			level.playSound(null, player.blockPosition(), SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.PLAYERS, 1.0F, 1.4F);
			level.playSound(null, player.blockPosition(), SoundEvents.BUNDLE_DROP_CONTENTS, SoundSource.PLAYERS, 0.8F, 1.2F);
		}
		capsule.consume(1, player);
		return InteractionResult.SUCCESS;
	}
}
