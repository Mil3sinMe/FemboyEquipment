package com.femboyequipment.client.mixin;

import com.femboyequipment.client.emblem.Emblems;
import com.llamalad7.mixinextras.sugar.Local;
import com.mojang.authlib.GameProfile;
import net.minecraft.client.multiplayer.chat.ChatListener;
import net.minecraft.network.chat.ChatType;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyVariable;

/** Puts the emblem in front of FemboyEquipment users' names in chat. */
@Mixin(ChatListener.class)
public abstract class ChatListenerMixin {
	@ModifyVariable(method = "handlePlayerChatMessage", at = @At("HEAD"), argsOnly = true)
	private ChatType.Bound femboy$addEmblem(ChatType.Bound bound, @Local(argsOnly = true) GameProfile sender) {
		Emblems.refresh(sender.id());
		if (Emblems.shouldShow(sender.id())) {
			return new ChatType.Bound(bound.chatType(), Emblems.decorate(sender.id(), sender.name(), bound.name()), bound.targetName());
		}
		return bound;
	}
}
