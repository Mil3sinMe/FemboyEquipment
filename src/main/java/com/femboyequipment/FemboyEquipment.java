package com.femboyequipment;

import com.femboyequipment.block.Blahaj;
import com.femboyequipment.block.ModBlocks;
import com.femboyequipment.effect.OutfitEffects;
import com.femboyequipment.entity.ModEntities;
import com.femboyequipment.world.ModWorldGen;
import com.femboyequipment.item.ModItemGroups;
import com.femboyequipment.item.ModItems;
import com.femboyequipment.api.FemboyEquipmentAddon;
import com.femboyequipment.effect.OutfitEffectsData;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.resource.v1.ResourceLoader;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.server.packs.PackType;
import net.minecraft.resources.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FemboyEquipment implements ModInitializer {
	public static final String MOD_ID = "femboyequipment";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	@Override
	public void onInitialize() {
		ModItems.initialize();
		ModBlocks.initialize();
		Blahaj.initialize();
		com.femboyequipment.block.Fih.initialize();
		ModEntities.initialize();
		ModItemGroups.initialize();
		OutfitEffects.initialize();
		ModWorldGen.initialize();

		ResourceLoader.get(PackType.SERVER_DATA).registerReloader(OutfitEffectsData.ID, new OutfitEffectsData());

		// Let addons know we're ready.
		var addons = FabricLoader.getInstance().getEntrypointContainers("femboyequipment", FemboyEquipmentAddon.class);
		for (var addon : addons) {
			try {
				addon.getEntrypoint().onFemboyEquipmentInit();
			} catch (Throwable t) {
				throw new RuntimeException("FemboyEquipment addon " + addon.getProvider().getMetadata().getId() + " failed to initialize", t);
			}
		}

		LOGGER.info("FemboyEquipment loaded~ time to get cute! <3 ({} addon(s))", addons.size());
	}

	public static Identifier id(String path) {
		return Identifier.fromNamespaceAndPath(MOD_ID, path);
	}
}
