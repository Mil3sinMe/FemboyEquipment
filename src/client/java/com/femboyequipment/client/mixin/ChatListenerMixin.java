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
		net.minecraft.network.chat.Component name = bound.name();
		if (Emblems.shouldShow(sender.id())) {
			name = Emblems.decorate(sender.id(), sender.name(), name);
		}
		name = com.femboyequipment.client.collection.RankTitles.decorate(sender.id(), name);
		return name == bound.name() ? bound : new ChatType.Bound(bound.chatType(), name, bound.targetName());
	}
}
