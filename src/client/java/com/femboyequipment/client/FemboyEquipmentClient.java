package com.femboyequipment.client;

import com.femboyequipment.block.ModBlocks;
import com.femboyequipment.client.compat.TrinketsClientCompat;
import com.femboyequipment.client.emblem.EmblemCommand;
import com.femboyequipment.compat.TrinketsCompat;
import com.femboyequipment.client.model.AccessoryModels;
import com.femboyequipment.client.render.AccessoryLayer;
import com.femboyequipment.client.render.FemboyVillagerRenderer;
import com.femboyequipment.entity.ModEntities;
import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.api.client.AccessoryShape;
import com.femboyequipment.api.client.FemboyEquipmentClientAddon;
import com.femboyequipment.api.client.FemboyEquipmentClientApi;
import com.femboyequipment.item.ModItems;
import com.femboyequipment.item.OutfitColors;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.world.item.Item;
import net.fabricmc.fabric.api.client.rendering.v1.BlockRenderLayerMap;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.fabricmc.fabric.api.client.rendering.v1.LivingEntityFeatureRendererRegistrationCallback;
import net.minecraft.client.renderer.chunk.ChunkSectionLayer;
import net.minecraft.client.renderer.entity.player.AvatarRenderer;

public class FemboyEquipmentClient implements ClientModInitializer {
	@Override
	public void onInitializeClient() {
		AccessoryModels.register();
		registerBuiltInAccessories();
		EmblemCommand.register();
		com.femboyequipment.client.collection.CollectionClient.register();
		if (TrinketsCompat.LOADED) {
			TrinketsClientCompat.register();
		}
		EntityRendererRegistry.register(ModEntities.FEMBOY_VILLAGER, FemboyVillagerRenderer::new);
		BlockRenderLayerMap.putBlock(ModBlocks.PASTEL_BLOOM, ChunkSectionLayer.CUTOUT);

		// Let addons register their client stuff.
		for (var addon : FabricLoader.getInstance().getEntrypointContainers("femboyequipment-client", FemboyEquipmentClientAddon.class)) {
			addon.getEntrypoint().onFemboyEquipmentClientInit();
		}

		LivingEntityFeatureRendererRegistrationCallback.EVENT.register((entityType, renderer, helper, context) -> {
			if (renderer instanceof AvatarRenderer<?> avatarRenderer) {
				helper.register(new AccessoryLayer<>(avatarRenderer, context.getModelSet()));
			}
		});
	}

	private static void registerBuiltInAccessories() {
		accessory(ModItems.CAT_EARS, AccessoryShape.CAT_EARS, "cat_ears", OutfitColors.PINK);
		accessory(ModItems.CAT_EARS, AccessoryShape.CAT_TAIL, "cat_tail", OutfitColors.PINK);
		accessory(ModItems.BUNNY_EARS, AccessoryShape.BUNNY_EARS, "bunny_ears", OutfitColors.BUNNY);
		accessory(ModItems.BUNNY_EARS, AccessoryShape.BUNNY_TAIL, "bunny_tail", OutfitColors.BUNNY);
		accessory(ModItems.PLEATED_SKIRT, AccessoryShape.SKIRT, "pleated_skirt", OutfitColors.PINK);
		accessory(ModItems.MAID_APRON, AccessoryShape.SKIRT, "maid_skirt", OutfitColors.MAID);
	}

	private static void accessory(Item item, AccessoryShape shape, String texture, int color) {
		FemboyEquipmentClientApi.registerAccessory(item, shape,
				FemboyEquipment.id("textures/entity/accessory/" + texture + ".png"),
				FemboyEquipment.id("textures/entity/accessory/" + texture + "_overlay.png"), color);
	}
}
