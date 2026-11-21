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
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.equipment.Equippable;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;

/** All the Blåhaj variants (the list lives in the generated BlahajVariants). */
public final class Blahaj {
	public static final List<String> VARIANTS = BlahajVariants.NAMES;

	private static final List<Block> BLOCKS = new ArrayList<>();
	private static final List<Item> ITEMS = new ArrayList<>();

	private Blahaj() {
	}

	public static void initialize() {
		for (String name : VARIANTS) {
			register(name);
		}
	}

	private static void register(String name) {
		BlockBehaviour.Properties props = BlockBehaviour.Properties.of()
				.mapColor(MapColor.COLOR_LIGHT_BLUE)
				.strength(0.3F)
				.sound(SoundType.WOOL)
				.noOcclusion();
		Integer light = BlahajVariants.LIGHT.get(name);
		if (light != null) {
			props = props.lightLevel(state -> light);
		}
		ResourceKey<Block> blockKey = ResourceKey.create(Registries.BLOCK, FemboyEquipment.id(name));
		Block block = Registry.register(BuiltInRegistries.BLOCK, blockKey, new BlahajBlock(props.setId(blockKey)));

		Item.Properties itemProps = new Item.Properties()
				.useBlockDescriptionPrefix()
				.stacksTo(16)
				// Wear it on your head as a shark hat!
				.component(DataComponents.EQUIPPABLE, Equippable.builder(EquipmentSlot.HEAD)
						.setEquipSound(SoundEvents.ARMOR_EQUIP_LEATHER)
						.setSwappable(true)
						.build());
		if (BlahajVariants.RARE.contains(name)) {
			itemProps = itemProps.rarity(Rarity.RARE);
		}
		if (BlahajVariants.FIRE_RESISTANT.contains(name)) {
			itemProps = itemProps.fireResistant();
		}
		Item item = ModItems.register(name, p -> new BlockItem(block, p), itemProps);
		BLOCKS.add(block);
		ITEMS.add(item);
	}

	public static List<Item> items() {
		return Collections.unmodifiableList(ITEMS);
	}

	public static boolean is(ItemStack stack) {
		return stack.getItem() instanceof BlockItem blockItem && blockItem.getBlock() instanceof BlahajBlock;
	}
}
