package com.femboyequipment.entity;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.item.ModItems;
import net.fabricmc.fabric.api.object.builder.v1.entity.FabricDefaultAttributeRegistry;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.animal.feline.CatVariant;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.SpawnEggItem;
import net.minecraft.world.item.component.TypedEntityData;

public final class ModEntities {
	private static final ResourceKey<EntityType<?>> FEMBOY_VILLAGER_KEY =
			ResourceKey.create(Registries.ENTITY_TYPE, FemboyEquipment.id("femboy_villager"));

	public static final EntityType<FemboyVillager> FEMBOY_VILLAGER = Registry.register(BuiltInRegistries.ENTITY_TYPE,
			FEMBOY_VILLAGER_KEY,
			EntityType.Builder.of(FemboyVillager::new, MobCategory.CREATURE)
					.sized(0.6F, 1.95F)
					.eyeHeight(1.62F)
					.clientTrackingRange(10)
					.build(FEMBOY_VILLAGER_KEY));

	/** The data-driven pink cat variant (data/femboyequipment/cat_variant/pink.json). */
	public static final ResourceKey<CatVariant> PINK_CAT = ResourceKey.create(Registries.CAT_VARIANT, FemboyEquipment.id("pink"));

	public static Item FEMBOY_VILLAGER_SPAWN_EGG;
	public static Item PINK_CAT_SPAWN_EGG;

	private ModEntities() {
	}

	public static void initialize() {
		FabricDefaultAttributeRegistry.register(FEMBOY_VILLAGER, FemboyVillager.createAttributes());
		FEMBOY_VILLAGER_SPAWN_EGG = ModItems.register("femboy_villager_spawn_egg", SpawnEggItem::new,
				new Item.Properties().spawnEgg(FEMBOY_VILLAGER));

		// A vanilla cat, but always the pink variant (the egg's entity data is applied after the random variant roll).
		CompoundTag pinkCat = new CompoundTag();
		pinkCat.putString("variant", PINK_CAT.identifier().toString());
		PINK_CAT_SPAWN_EGG = ModItems.register("pink_cat_spawn_egg", SpawnEggItem::new,
				new Item.Properties().component(DataComponents.ENTITY_DATA, TypedEntityData.of(EntityType.CAT, pinkCat)));
	}
}
