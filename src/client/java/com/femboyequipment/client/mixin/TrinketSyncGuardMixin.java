package com.femboyequipment.client.mixin;

import com.femboyequipment.FemboyEquipment;
import com.llamalad7.mixinextras.injector.wrapmethod.WrapMethod;
import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import dev.emi.trinkets.api.LivingEntityTrinketComponent;
import net.minecraft.network.RegistryFriendlyByteBuf;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;

/**
 * Keeps a broken Trinkets slot-sync packet from kicking you. Some mods (e.g. replay recorders) read the packet's
 * data before Trinkets does, which leaves it empty ("fieldSize is too long! Length is 1, but maximum is 0").
 * The broken update is skipped instead; the slots catch up on the next sync.
 */
@Mixin(value = LivingEntityTrinketComponent.class, remap = false)
public abstract class TrinketSyncGuardMixin {
	@Unique
	private static boolean femboy$warned;

	@WrapMethod(method = "applySyncPacket")
	private void femboy$guard(RegistryFriendlyByteBuf buf, Operation<Void> original) {
		try {
			original.call(buf);
		} catch (RuntimeException e) {
			if (!femboy$warned) {
				femboy$warned = true;
				FemboyEquipment.LOGGER.warn("Skipped a broken Trinkets sync packet instead of disconnecting "
						+ "(another mod probably read it first, e.g. a replay recorder)", e);
			}
		}
	}
}
