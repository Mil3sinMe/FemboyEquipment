package com.femboyequipment.world;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.block.Blahaj;
import com.femboyequipment.block.ModBlocks;
import com.femboyequipment.item.ModItems;
import java.util.Set;
import net.fabricmc.fabric.api.biome.v1.BiomeModifications;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectors;
import net.fabricmc.fabric.api.loot.v3.LootTableEvents;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.levelgen.GenerationStep;
import net.minecraft.world.level.levelgen.placement.PlacedFeature;
import net.minecraft.world.level.storage.loot.BuiltInLootTables;
import net.minecraft.world.level.storage.loot.LootPool;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.level.storage.loot.entries.LootItem;
import net.minecraft.world.level.storage.loot.entries.LootPoolEntryContainer;
import net.minecraft.world.level.storage.loot.functions.SetItemCountFunction;
import net.minecraft.world.level.storage.loot.providers.number.UniformGenerator;

/** Pastel Bloom flower patches and outfit loot in vanilla chests. The cute house itself is pure data. */
public final class ModWorldGen {
	public static final ResourceKey<PlacedFeature> PASTEL_BLOOM_PATCH =
			ResourceKey.create(Registries.PLACED_FEATURE, FemboyEquipment.id("pastel_bloom_patch"));

	private static final Set<ResourceKey<LootTable>> LOOT_TARGETS = Set.of(
			BuiltInLootTables.VILLAGE_PLAINS_HOUSE,
			BuiltInLootTables.VILLAGE_TAIGA_HOUSE,
			BuiltInLootTables.VILLAGE_SAVANNA_HOUSE,
			BuiltInLootTables.VILLAGE_SNOWY_HOUSE,
			BuiltInLootTables.VILLAGE_DESERT_HOUSE,
			BuiltInLootTables.SIMPLE_DUNGEON,
			BuiltInLootTables.ABANDONED_MINESHAFT,
			BuiltInLootTables.WOODLAND_MANSION,
			BuiltInLootTables.SHIPWRECK_SUPPLY);

	private ModWorldGen() {
	}

	public static void initialize() {
		BiomeModifications.addFeature(
				BiomeSelectors.includeByKey(Biomes.MEADOW, Biomes.FLOWER_FOREST, Biomes.CHERRY_GROVE, Biomes.PLAINS, Biomes.SUNFLOWER_PLAINS),
				GenerationStep.Decoration.VEGETAL_DECORATION,
				PASTEL_BLOOM_PATCH);

		LootTableEvents.MODIFY.register((key, tableBuilder, source, registries) -> {
			if (source.isBuiltin() && LOOT_TARGETS.contains(key)) {
				tableBuilder.withPool(cuteLoot());
			}
		});
	}

	private static LootPool.Builder cuteLoot() {
		return LootPool.lootPool()
				.setRolls(UniformGenerator.between(0.0F, 2.0F))
				.add(entry(ModItems.PINK_RIBBON, 12, 1, 4))
				.add(entry(ModItems.STRAWBERRY_MILK, 8, 1, 3))
				.add(entry(ModItems.HAIR_CLIP, 6, 1, 2))
				.add(entry(ModItems.CHOKER, 4, 1, 1))
				.add(entry(ModItems.PROGRAMMING_SOCKS, 4, 1, 1))
				.add(entry(ModBlocks.PASTEL_BLOOM.asItem(), 6, 1, 3))
				.add(entry(Blahaj.items().get(0), 3, 1, 1))
				.add(entry(Blahaj.items().get(1), 2, 1, 1))
				.add(entry(ModItems.CAT_EARS, 1, 1, 1))
				.add(entry(ModItems.MAID_HEADBAND, 1, 1, 1))
				.add(entry(ModItems.BUNNY_EARS, 1, 1, 1));
	}

	private static LootPoolEntryContainer.Builder<?> entry(Item item, int weight, int min, int max) {
		return LootItem.lootTableItem(item)
				.setWeight(weight)
				.apply(SetItemCountFunction.setCount(UniformGenerator.between(min, max)));
	}
}
