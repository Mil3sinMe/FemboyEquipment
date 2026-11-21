package com.femboyequipment.client.mixin;

import com.femboyequipment.client.emblem.Emblems;
import net.minecraft.client.renderer.entity.player.AvatarRenderer;
import net.minecraft.client.renderer.entity.state.AvatarRenderState;
import net.minecraft.world.entity.Avatar;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Puts the emblem in front of name tags above FemboyEquipment users' heads. */
@Mixin(AvatarRenderer.class)
public abstract class AvatarRendererMixin {
	@Inject(method = "extractRenderState(Lnet/minecraft/world/entity/Avatar;Lnet/minecraft/client/renderer/entity/state/AvatarRenderState;F)V",
			at = @At("TAIL"))
	private void femboy$addEmblem(Avatar avatar, AvatarRenderState state, float partialTick, CallbackInfo ci) {
		if (avatar instanceof Player player && Emblems.check(player) && Emblems.shouldShow(player.getUUID()) && state.nameTag != null) {
			state.nameTag = Emblems.decorate(player.getUUID(), player.getGameProfile().name(), state.nameTag);
		}
	}
}
