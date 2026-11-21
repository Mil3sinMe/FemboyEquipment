package com.femboyequipment.item;

import com.femboyequipment.FemboyEquipment;
import java.util.EnumMap;
import java.util.Map;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.equipment.EquipmentAsset;
import net.minecraft.world.item.equipment.EquipmentAssets;

public final class ModArmorMaterials {
	public static final TagKey<Item> CUTE_REPAIR_MATERIALS =
			TagKey.create(Registries.ITEM, FemboyEquipment.id("cute_repair_materials"));

	// Each wearable piece has its own look, so each gets its own material/equipment asset.
	public static final ArmorMaterial CAT_EARS = cute("cat_ears");
	public static final ArmorMaterial FEMBOY_HOODIE = cute("femboy_hoodie");
	public static final ArmorMaterial PLEATED_SKIRT = cute("pleated_skirt");
	public static final ArmorMaterial MAID_HEADBAND = cute("maid_headband");
	public static final ArmorMaterial MAID_DRESS = cute("maid_dress");
	public static final ArmorMaterial MAID_APRON = cute("maid_apron");
	public static final ArmorMaterial MARY_JANES = cute("mary_janes");
	public static final ArmorMaterial BUNNY_EARS = cute("bunny_ears");
	public static final ArmorMaterial BUNNY_HOODIE = cute("bunny_hoodie");
	public static final ArmorMaterial FLUFFY_SLIPPERS = cute("fluffy_slippers");

	// The thigh highs are intentionally absurd.
	public static final ArmorMaterial THIGH_HIGHS = new ArmorMaterial(
			100,
			defense(8, 12, 10, 8),
			30,
			SoundEvents.ARMOR_EQUIP_NETHERITE,
			6.0F,
			0.5F,
			CUTE_REPAIR_MATERIALS,
			asset("thigh_highs"));

	private ModArmorMaterials() {
	}

	private static ArmorMaterial cute(String name) {
		// Roughly iron-tier protection with diamond-ish durability and gold-level enchantability.
		return new ArmorMaterial(25, defense(2, 6, 5, 2), 22, SoundEvents.ARMOR_EQUIP_LEATHER,
				1.0F, 0.0F, CUTE_REPAIR_MATERIALS, asset(name));
	}

	private static Map<ArmorType, Integer> defense(int boots, int chest, int legs, int helmet) {
		Map<ArmorType, Integer> map = new EnumMap<>(ArmorType.class);
		map.put(ArmorType.BOOTS, boots);
		map.put(ArmorType.LEGGINGS, legs);
		map.put(ArmorType.CHESTPLATE, chest);
		map.put(ArmorType.HELMET, helmet);
		map.put(ArmorType.BODY, chest);
		return map;
	}

	private static ResourceKey<EquipmentAsset> asset(String name) {
		return ResourceKey.create(EquipmentAssets.ROOT_ID, FemboyEquipment.id(name));
	}
}
