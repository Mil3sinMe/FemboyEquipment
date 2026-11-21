package com.femboyequipment.item;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.block.ModBlocks;
import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;

public final class ModItemGroups {
	public static final ResourceKey<CreativeModeTab> MAIN_KEY =
			ResourceKey.create(Registries.CREATIVE_MODE_TAB, FemboyEquipment.id("main"));

	public static final CreativeModeTab MAIN = FabricItemGroup.builder()
			.icon(() -> new ItemStack(ModItems.PINK_RIBBON))
			.title(Component.translatable("itemGroup.femboyequipment.main"))
			.displayItems((parameters, output) -> {
				output.accept(ModItems.CAT_EARS);
				output.accept(ModItems.FEMBOY_HOODIE);
				output.accept(ModItems.PLEATED_SKIRT);
				output.accept(ModItems.THIGH_HIGHS);
				output.accept(ModItems.MAID_HEADBAND);
				output.accept(ModItems.MAID_DRESS);
				output.accept(ModItems.MAID_APRON);
				output.accept(ModItems.MARY_JANES);
				output.accept(ModItems.BUNNY_EARS);
				output.accept(ModItems.BUNNY_HOODIE);
				output.accept(ModItems.FLUFFY_SLIPPERS);
				output.accept(ModItems.SPARKLY_SWORD);
				output.accept(ModItems.SPARKLY_PICKAXE);
				output.accept(ModItems.PINK_RIBBON);
				output.accept(ModItems.PROGRAMMING_SOCKS);
				output.accept(ModItems.HAIR_CLIP);
				output.accept(ModItems.CHOKER);
				output.accept(ModItems.STRAWBERRY_MILK);
				output.accept(ModBlocks.PASTEL_PINK_BRICKS);
				output.accept(ModBlocks.RIBBON_BLOCK);
			})
			.build();

	private ModItemGroups() {
	}

	public static void initialize() {
		Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, MAIN_KEY, MAIN);
	}
}
