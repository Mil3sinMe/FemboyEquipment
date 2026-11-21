package com.femboyequipment.client.mixin;

import com.femboyequipment.client.emblem.EmblemConfig;
import com.femboyequipment.client.emblem.Emblems;
import net.minecraft.client.Options;
import net.minecraft.server.level.ClientInformation;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Unless turned off with /emblem share off, sets the "has FemboyEquipment" bit in the skin-layer settings the client sends to the server. */
@Mixin(Options.class)
public abstract class OptionsMixin {
	@Inject(method = "buildPlayerInformation", at = @At("RETURN"), cancellable = true)
	private void femboy$flagModUser(CallbackInfoReturnable<ClientInformation> cir) {
		if (!EmblemConfig.get().shareEmblem) {
			return;
		}
		ClientInformation info = cir.getReturnValue();
		cir.setReturnValue(new ClientInformation(info.language(), info.viewDistance(), info.chatVisibility(),
				info.chatColors(), info.modelCustomisation() | Emblems.FLAG, info.mainHand(),
				info.textFilteringEnabled(), info.allowsListing(), info.particleStatus()));
	}
}
