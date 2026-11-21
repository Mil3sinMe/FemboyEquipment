package com.femboyequipment.item;

import com.femboyequipment.FemboyEquipment;
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
				output.accept(ModItems.PINK_RIBBON);
				output.accept(ModItems.PROGRAMMING_SOCKS);
			})
			.build();

	private ModItemGroups() {
	}

	public static void initialize() {
		Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, MAIN_KEY, MAIN);
	}
}
