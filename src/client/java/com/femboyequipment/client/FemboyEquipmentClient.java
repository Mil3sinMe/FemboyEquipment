package com.femboyequipment.client;

import com.femboyequipment.client.model.AccessoryModels;
import com.femboyequipment.client.render.AccessoryLayer;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.rendering.v1.LivingEntityFeatureRendererRegistrationCallback;
import net.minecraft.client.renderer.entity.player.AvatarRenderer;

public class FemboyEquipmentClient implements ClientModInitializer {
	@Override
	public void onInitializeClient() {
		AccessoryModels.register();

		LivingEntityFeatureRendererRegistrationCallback.EVENT.register((entityType, renderer, helper, context) -> {
			if (renderer instanceof AvatarRenderer<?> avatarRenderer) {
				helper.register(new AccessoryLayer(avatarRenderer, context.getModelSet()));
			}
		});
	}
}
