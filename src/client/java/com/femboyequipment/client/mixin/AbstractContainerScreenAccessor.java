package com.femboyequipment.client.mixin;

import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Accessor;

@Mixin(AbstractContainerScreen.class)
public interface AbstractContainerScreenAccessor {
	@Accessor("leftPos")
	int femboy$leftPos();

	@Accessor("topPos")
	int femboy$topPos();

	@Accessor("imageWidth")
	int femboy$imageWidth();
}
