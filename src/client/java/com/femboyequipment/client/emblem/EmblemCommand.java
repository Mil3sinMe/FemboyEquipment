package com.femboyequipment.client.emblem;

import static net.fabricmc.fabric.api.client.command.v2.ClientCommandManager.literal;

import com.mojang.brigadier.context.CommandContext;
import net.fabricmc.fabric.api.client.command.v2.ClientCommandRegistrationCallback;
import net.fabricmc.fabric.api.client.command.v2.FabricClientCommandSource;
import net.minecraft.ChatFormatting;
import net.minecraft.client.Minecraft;
import net.minecraft.network.chat.Component;

/**
 * /emblem                - show current settings
 * /emblem share on|off   - let other mod users see your emblem
 * /emblem display on|off - show other people's emblems
 */
public final class EmblemCommand {
	private EmblemCommand() {
	}

	public static void register() {
		ClientCommandRegistrationCallback.EVENT.register((dispatcher, registryAccess) -> dispatcher.register(
				literal("emblem")
						.executes(EmblemCommand::status)
						.then(literal("share")
								.then(literal("on").executes(ctx -> setShare(ctx, true)))
								.then(literal("off").executes(ctx -> setShare(ctx, false))))
						.then(literal("display")
								.then(literal("on").executes(ctx -> setDisplay(ctx, true)))
								.then(literal("off").executes(ctx -> setDisplay(ctx, false))))));
	}

	private static int status(CommandContext<FabricClientCommandSource> ctx) {
		EmblemConfig config = EmblemConfig.get();
		ctx.getSource().sendFeedback(msg("Emblem settings"));
		ctx.getSource().sendFeedback(line("Share my emblem", config.shareEmblem, "/emblem share on|off"));
		ctx.getSource().sendFeedback(line("Show other emblems", config.showEmblems, "/emblem display on|off"));
		return 1;
	}

	private static Component msg(String text) {
		return Component.empty().append(Emblems.icon()).append(" ")
				.append(Component.literal(text).withStyle(ChatFormatting.LIGHT_PURPLE));
	}

	private static Component line(String label, boolean on, String hint) {
		return Component.literal(" " + label + ": ")
				.append(Component.literal(on ? "ON" : "OFF").withStyle(on ? ChatFormatting.GREEN : ChatFormatting.RED))
				.append(Component.literal("  " + hint).withStyle(ChatFormatting.GRAY));
	}

	private static int setShare(CommandContext<FabricClientCommandSource> ctx, boolean on) {
		EmblemConfig config = EmblemConfig.get();
		config.shareEmblem = on;
		config.save();
		// Re-send our client settings so the server updates the flag right away.
		Minecraft.getInstance().options.broadcastOptions();
		ctx.getSource().sendFeedback(msg(on
				? "Other FemboyEquipment users can see your emblem again"
				: "Your emblem is now hidden; you'll look like a normal player"));
		return 1;
	}

	private static int setDisplay(CommandContext<FabricClientCommandSource> ctx, boolean on) {
		EmblemConfig config = EmblemConfig.get();
		config.showEmblems = on;
		config.save();
		ctx.getSource().sendFeedback(msg(on
				? "Showing emblems in name tags, tab and chat"
				: "Emblems hidden"));
		return 1;
	}
}
