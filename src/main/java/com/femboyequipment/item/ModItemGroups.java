package com.femboyequipment.item;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.block.Blahaj;
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
				output.accept(ModItems.SPARKLY_AXE);
				output.accept(ModItems.SPARKLY_SHOVEL);
				output.accept(ModItems.SPARKLY_HOE);
				output.accept(ModItems.ROSE_QUARTZ);
				output.accept(ModItems.ROSE_QUARTZ_HELMET);
				output.accept(ModItems.ROSE_QUARTZ_CHESTPLATE);
				output.accept(ModItems.ROSE_QUARTZ_LEGGINGS);
				output.accept(ModItems.ROSE_QUARTZ_BOOTS);
				output.accept(ModItems.ROSE_QUARTZ_SWORD);
				output.accept(ModItems.ROSE_QUARTZ_PICKAXE);
				output.accept(ModItems.ROSE_QUARTZ_AXE);
				output.accept(ModItems.ROSE_QUARTZ_SHOVEL);
				output.accept(ModItems.ROSE_QUARTZ_HOE);
				output.accept(ModItems.ROSE_QUARTZ_SPEAR);
				output.accept(ModItems.FIH_SLAPPER);
				output.accept(ModItems.BLAHAJ_BAT);
				output.accept(ModItems.PINK_RIBBON);
				output.accept(ModItems.PROGRAMMING_SOCKS);
				output.accept(ModItems.HAIR_CLIP);
				output.accept(ModItems.CHOKER);
				output.accept(ModItems.STRAWBERRY_MILK);
				output.accept(ModItems.COLLECTION_BOOK);
				ModItems.RANK_HATS.forEach(output::accept);
				output.accept(ModBlocks.PASTEL_PINK_BRICKS);
				output.accept(ModBlocks.RIBBON_BLOCK);
				output.accept(ModBlocks.PASTEL_BLUE_BRICKS);
				output.accept(ModBlocks.PASTEL_LAVENDER_BRICKS);
				output.accept(ModBlocks.PASTEL_MINT_BRICKS);
				output.accept(ModBlocks.PASTEL_YELLOW_BRICKS);
				output.accept(ModBlocks.ROSE_QUARTZ_BLOCK);
				output.accept(ModBlocks.ROSE_QUARTZ_BRICKS);
				ModBlocks.BRICK_SHAPES.forEach(output::accept);
				output.accept(ModBlocks.PASTEL_BLOOM);
				output.accept(com.femboyequipment.entity.ModEntities.FEMBOY_VILLAGER_SPAWN_EGG);
				output.accept(com.femboyequipment.entity.ModEntities.PINK_CAT_SPAWN_EGG);
			})
			.build();

	public static final ResourceKey<CreativeModeTab> BLAHAJ_KEY =
			ResourceKey.create(Registries.CREATIVE_MODE_TAB, FemboyEquipment.id("blahaj"));

	public static final CreativeModeTab BLAHAJ = FabricItemGroup.builder()
			.icon(() -> new ItemStack(Blahaj.items().get(1)))
			.title(Component.translatable("itemGroup.femboyequipment.blahaj"))
			.displayItems((parameters, output) -> {
				output.accept(ModItems.BLAHAJ_CAPSULE);
				Blahaj.items().forEach(output::accept);
			})
			.build();

	public static final ResourceKey<CreativeModeTab> FIH_KEY =
			ResourceKey.create(Registries.CREATIVE_MODE_TAB, FemboyEquipment.id("fih"));

	public static final CreativeModeTab FIH = FabricItemGroup.builder()
			.icon(() -> new ItemStack(com.femboyequipment.block.Fih.items().get(0)))
			.title(Component.translatable("itemGroup.femboyequipment.fih"))
			.displayItems((parameters, output) -> {
				output.accept(ModItems.FIH_CAPSULE);
				com.femboyequipment.block.Fih.items().forEach(output::accept);
			})
			.build();

	private ModItemGroups() {
	}

	public static void initialize() {
		Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, MAIN_KEY, MAIN);
		Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, BLAHAJ_KEY, BLAHAJ);
		Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, FIH_KEY, FIH);
	}
}
