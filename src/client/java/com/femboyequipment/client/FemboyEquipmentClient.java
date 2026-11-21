package com.femboyequipment.client;

import com.femboyequipment.block.ModBlocks;
import com.femboyequipment.client.compat.TrinketsClientCompat;
import com.femboyequipment.client.emblem.EmblemCommand;
import com.femboyequipment.compat.TrinketsCompat;
import com.femboyequipment.client.model.AccessoryModels;
import com.femboyequipment.client.render.AccessoryLayer;
import com.femboyequipment.client.render.FemboyVillagerRenderer;
import com.femboyequipment.entity.ModEntities;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.rendering.v1.BlockRenderLayerMap;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.LivingEntityFeatureRendererRegistrationCallback;
import net.minecraft.client.renderer.chunk.ChunkSectionLayer;
import net.minecraft.client.renderer.entity.player.AvatarRenderer;

public class FemboyEquipmentClient implements ClientModInitializer {
	@Override
	public void onInitializeClient() {
		AccessoryModels.register();
		EmblemCommand.register();
		if (TrinketsCompat.LOADED) {
			TrinketsClientCompat.register();
		}
		EntityRendererRegistry.register(ModEntities.FEMBOY_VILLAGER, FemboyVillagerRenderer::new);
		BlockRenderLayerMap.putBlock(ModBlocks.PASTEL_BLOOM, ChunkSectionLayer.CUTOUT);

		LivingEntityFeatureRendererRegistrationCallback.EVENT.register((entityType, renderer, helper, context) -> {
			if (renderer instanceof AvatarRenderer<?> avatarRenderer) {
				helper.register(new AccessoryLayer<>(avatarRenderer, context.getModelSet()));
			}
		});
	}
}
