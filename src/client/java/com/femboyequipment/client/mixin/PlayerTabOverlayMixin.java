package com.femboyequipment.client.mixin;

import com.femboyequipment.client.emblem.Emblems;
import net.minecraft.client.gui.components.PlayerTabOverlay;
import net.minecraft.client.multiplayer.PlayerInfo;
import net.minecraft.network.chat.Component;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Puts the emblem in front of FemboyEquipment users in the tab list. */
@Mixin(PlayerTabOverlay.class)
public abstract class PlayerTabOverlayMixin {
	@Inject(method = "getNameForDisplay", at = @At("RETURN"), cancellable = true)
	private void femboy$addEmblem(PlayerInfo info, CallbackInfoReturnable<Component> cir) {
		if (Emblems.shouldShow(info.getProfile().id())) {
			cir.setReturnValue(Emblems.decorate(info.getProfile().id(), info.getProfile().name(), cir.getReturnValue()));
		}
	}
}
