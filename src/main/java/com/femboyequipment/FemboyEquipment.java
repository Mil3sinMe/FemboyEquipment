package com.femboyequipment;

import com.femboyequipment.block.Blahaj;
import com.femboyequipment.block.ModBlocks;
import com.femboyequipment.effect.OutfitEffects;
import com.femboyequipment.entity.ModEntities;
import com.femboyequipment.world.ModWorldGen;
import com.femboyequipment.item.ModItemGroups;
import com.femboyequipment.item.ModItems;
import net.fabricmc.api.ModInitializer;
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
		ModEntities.initialize();
		ModItemGroups.initialize();
		OutfitEffects.initialize();
		ModWorldGen.initialize();

		LOGGER.info("FemboyEquipment loaded~ time to get cute! <3");
	}

	public static Identifier id(String path) {
		return Identifier.fromNamespaceAndPath(MOD_ID, path);
	}
}
