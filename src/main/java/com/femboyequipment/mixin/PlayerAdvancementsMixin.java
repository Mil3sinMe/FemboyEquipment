package com.femboyequipment.mixin;

import com.femboyequipment.collection.CollectionServer;
import com.llamalad7.mixinextras.injector.wrapoperation.Operation;
import com.llamalad7.mixinextras.injector.wrapoperation.WrapOperation;
import java.util.Optional;
import java.util.Set;
import net.minecraft.advancements.Advancement;
import net.minecraft.advancements.AdvancementHolder;
import net.minecraft.advancements.AdvancementNode;
import net.minecraft.advancements.DisplayInfo;
import net.minecraft.resources.Identifier;
import net.minecraft.server.PlayerAdvancements;
import net.minecraft.server.level.ServerPlayer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * Moves FemboyEquipment's (and addons') advancements into the Cute Collection: they still work and save as normal,
 * but are never sent to the vanilla advancement screen, never toast, never spam chat.
 */
@Mixin(PlayerAdvancements.class)
public abstract class PlayerAdvancementsMixin {
	@Shadow
	private ServerPlayer player;

	/** Our trees stay invisible to the vanilla screen (and so no vanilla toasts either). */
	@Inject(method = "updateTreeVisibility", at = @At("HEAD"), cancellable = true)
	private void femboy$hideOurTrees(AdvancementNode root, Set<AdvancementHolder> added, Set<Identifier> removed, CallbackInfo ci) {
		if (CollectionServer.isOurs(root.holder().id())) {
			ci.cancel();
		}
	}

	/** No chat announcement for ours (the collection shows its own toast instead). */
	@WrapOperation(method = "award", at = @At(value = "INVOKE", target = "Lnet/minecraft/advancements/Advancement;display()Ljava/util/Optional;"))
	private Optional<DisplayInfo> femboy$noChat(Advancement advancement, Operation<Optional<DisplayInfo>> original, AdvancementHolder holder, String criterion) {
		return CollectionServer.isOurs(holder.id()) ? Optional.empty() : original.call(advancement);
	}

	/** Fires exactly when an advancement becomes complete (right where vanilla grants its rewards). */
	@Inject(method = "award", at = @At(value = "INVOKE", target = "Lnet/minecraft/advancements/AdvancementRewards;grant(Lnet/minecraft/server/level/ServerPlayer;)V"))
	private void femboy$completed(AdvancementHolder holder, String criterion, CallbackInfoReturnable<Boolean> cir) {
		CollectionServer.onCompleted(this.player, holder);
	}

	@Inject(method = "revoke", at = @At("RETURN"))
	private void femboy$revoked(AdvancementHolder holder, String criterion, CallbackInfoReturnable<Boolean> cir) {
		if (cir.getReturnValueZ()) {
			CollectionServer.onRevoked(this.player, holder);
		}
	}
}
