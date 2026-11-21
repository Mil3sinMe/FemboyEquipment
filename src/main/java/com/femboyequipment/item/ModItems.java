package com.femboyequipment.item;

import com.femboyequipment.FemboyEquipment;
import java.util.function.Function;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;

public final class ModItems {
	public static final Item PINK_RIBBON = register("pink_ribbon", Item::new, new Item.Properties().stacksTo(16));
	public static final Item PROGRAMMING_SOCKS = register("programming_socks", Item::new, new Item.Properties().stacksTo(1));

	private ModItems() {
	}

	private static Item register(String name, Function<Item.Properties, Item> factory, Item.Properties properties) {
		ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, FemboyEquipment.id(name));
		Item item = factory.apply(properties.setId(key));
		return Registry.register(BuiltInRegistries.ITEM, key, item);
	}

	public static void initialize() {
		// Loading this class registers the items above.
	}
}
