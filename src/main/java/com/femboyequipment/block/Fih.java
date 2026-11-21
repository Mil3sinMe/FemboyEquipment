package com.femboyequipment.block;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.item.ModItems;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.equipment.Equippable;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;

/** All 1000 fih (40 fish x 25 sneakers). The list lives in the generated FihVariants. */
public final class Fih {
	private static final List<Item> ITEMS = new ArrayList<>();

	private Fih() {
	}

	public static void initialize() {
		for (String name : FihVariants.NAMES) {
			register(name);
		}
	}

	private static void register(String name) {
		BlockBehaviour.Properties props = BlockBehaviour.Properties.of()
				.mapColor(MapColor.COLOR_LIGHT_GRAY)
				.strength(0.3F)
				.sound(SoundType.WOOL)
				.noOcclusion();
		Integer light = FihVariants.LIGHT.get(name);
		if (light != null) {
			props = props.lightLevel(state -> light);
		}
		ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, FemboyEquipment.id(name));
		Block block = Registry.register(BuiltInRegistries.BLOCK, key, new FihBlock(props.setId(key)));
		Item.Properties itemProps = new Item.Properties()
				.useBlockDescriptionPrefix()
				.stacksTo(16)
				.component(DataComponents.EQUIPPABLE, Equippable.builder(EquipmentSlot.HEAD)
						.setEquipSound(SoundEvents.ARMOR_EQUIP_LEATHER)
						.setSwappable(true)
						.build());
		if (FihVariants.RARE.contains(name)) {
			itemProps = itemProps.rarity(Rarity.RARE);
		}
		ITEMS.add(ModItems.register(name, p -> new BlockItem(block, p), itemProps));
	}

	public static List<Item> items() {
		return Collections.unmodifiableList(ITEMS);
	}
}
