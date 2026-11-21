package com.femboyequipment.compat;

import dev.emi.trinkets.api.TrinketsApi;
import java.util.function.Predicate;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;

/**
 * Optional Trinkets support. Only touch {@link TrinketsApi} through here, and only after checking
 * {@link #LOADED}, so the mod still runs when no Trinkets fork is installed.
 */
public final class TrinketsCompat {
	public static final boolean LOADED = FabricLoader.getInstance().isModLoaded("trinkets");

	private TrinketsCompat() {
	}

	/** Whether the entity has a matching item in any of its Trinkets slots. */
	public static boolean isEquipped(LivingEntity entity, Predicate<ItemStack> predicate) {
		return LOADED && Impl.isEquipped(entity, predicate);
	}

	/** Kept in a nested class so TrinketsApi is only loaded when Trinkets is actually present. */
	private static final class Impl {
		static boolean isEquipped(LivingEntity entity, Predicate<ItemStack> predicate) {
			return TrinketsApi.getTrinketComponent(entity).map(c -> c.isEquipped(predicate)).orElse(false);
		}
	}
}
