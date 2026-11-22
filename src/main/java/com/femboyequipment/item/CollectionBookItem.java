package com.femboyequipment.item;

import com.femboyequipment.collection.CollectionHooks;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;

/** Right-click to open the Cute Collection. */
public class CollectionBookItem extends Item {
	public CollectionBookItem(Properties properties) {
		super(properties);
	}

	@Override
	public InteractionResult use(Level level, Player player, InteractionHand hand) {
		if (level.isClientSide()) {
			CollectionHooks.openScreen.run();
		}
		return InteractionResult.SUCCESS;
	}
}
