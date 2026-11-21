package com.example.femboyaddon;

import com.femboyequipment.api.FemboyEquipmentAddon;
import com.femboyequipment.api.FemboyEquipmentApi;
import com.femboyequipment.api.OutfitEffect;
import com.femboyequipment.item.ModItems;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.TagKey;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.equipment.EquipmentAssets;
import net.minecraft.world.level.block.Block;

/** An example FemboyEquipment addon: fox ears, a fox Blåhaj and a fox fih. */
public class ExampleAddon implements FemboyEquipmentAddon {
	public static final String MOD_ID = "fe_example_addon";

	public static Item FOX_EARS;
	public static Block FOX_BLAHAJ;
	public static Block FOX_FIH;

	public static Identifier id(String path) {
		return Identifier.fromNamespaceAndPath(MOD_ID, path);
	}

	@Override
	public void onFemboyEquipmentInit() {
		// 1. A normal armor item (a helmet) with its own look.
		Map<ArmorType, Integer> defense = new EnumMap<>(ArmorType.class);
		for (ArmorType type : ArmorType.values()) {
			defense.put(type, 2);
		}
		ArmorMaterial fox = new ArmorMaterial(20, defense, 15, SoundEvents.ARMOR_EQUIP_LEATHER, 0.0F, 0.0F,
				TagKey.create(Registries.ITEM, id("fox_repair")), ResourceKey.create(EquipmentAssets.ROOT_ID, id("fox_ears")));
		ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, id("fox_ears"));
		FOX_EARS = Registry.register(BuiltInRegistries.ITEM, key,
				new Item(new Item.Properties().humanoidArmor(fox, ArmorType.HELMET).setId(key)));

		// 2. Effects: Speed while worn, and a set bonus together with FemboyEquipment's hoodie + skirt.
		FemboyEquipmentApi.addWornEffect(FOX_EARS, OutfitEffect.of(MobEffects.SPEED, 0));
		FemboyEquipmentApi.addOutfitSet(List.of(FOX_EARS, ModItems.FEMBOY_HOODIE, ModItems.PLEATED_SKIRT),
				OutfitEffect.of(MobEffects.JUMP_BOOST, 1), OutfitEffect.of(MobEffects.LUCK, 0));

		// 3. Plushies: they join the Blåhaj / fih. creative tabs and capsules automatically.
		FOX_BLAHAJ = FemboyEquipmentApi.registerBlahaj(id("fox_blahaj"));
		FOX_FIH = FemboyEquipmentApi.registerFih(id("fox_fih"));

		// 4. Fox ears are also a (rare-ish) Blåhaj Capsule prize, and show up in the main tab.
		FemboyEquipmentApi.addCapsulePrize(FemboyEquipmentApi.Capsule.BLAHAJ, FOX_EARS);
		ItemGroupEvents.modifyEntriesEvent(FemboyEquipmentApi.MAIN_TAB).register(entries -> entries.accept(FOX_EARS));
	}
}
