package com.femboyequipment.client.collection;

import static net.fabricmc.fabric.api.client.command.v2.ClientCommandManager.literal;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.client.mixin.AbstractContainerScreenAccessor;
import com.femboyequipment.collection.CollectionHooks;
import com.mojang.blaze3d.platform.InputConstants;
import net.fabricmc.fabric.api.client.command.v2.ClientCommandRegistrationCallback;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.fabricmc.fabric.api.client.screen.v1.ScreenEvents;
import net.fabricmc.fabric.api.client.screen.v1.Screens;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.network.chat.Component;
import org.lwjgl.glfw.GLFW;

/** Ways to open the Cute Collection: K, the Collection Book, a heart button in the inventory, /collection. */
public final class CollectionClient {
	public static final KeyMapping.Category CATEGORY = KeyMapping.Category.register(FemboyEquipment.id("main"));
	public static final KeyMapping OPEN = KeyBindingHelper.registerKeyBinding(new KeyMapping("key.femboyequipment.collection",
			InputConstants.Type.KEYSYM, GLFW.GLFW_KEY_K, CATEGORY));
	private static boolean pendingOpen;

	private CollectionClient() {
	}

	public static void open() {
		Minecraft.getInstance().setScreen(new CollectionScreen());
	}

	public static void register() {
		ClientCollection.register();
		CollectionHooks.openScreen = CollectionClient::open;

		ClientTickEvents.END_CLIENT_TICK.register(client -> {
			while (OPEN.consumeClick()) {
				if (client.screen == null) {
					open();
				}
			}
			if (pendingOpen && client.screen == null) {
				pendingOpen = false;
				open();
			}
		});

		ClientCommandRegistrationCallback.EVENT.register((dispatcher, registryAccess) -> dispatcher.register(
				literal("collection").executes(ctx -> {
					pendingOpen = true;
					return 1;
				})));

		ScreenEvents.AFTER_INIT.register((client, screen, scaledWidth, scaledHeight) -> {
			if (screen instanceof InventoryScreen inventory) {
				Button button = Button.builder(Component.literal("♥"), b -> open())
						.bounds(0, 0, 14, 14)
						.tooltip(Tooltip.create(Component.translatable("collection.femboyequipment.title")))
						.build();
				Screens.getButtons(screen).add(button);
				// Follow the inventory when the recipe book pushes it sideways.
				ScreenEvents.beforeRender(screen).register((s, graphics, mouseX, mouseY, tickDelta) -> {
					AbstractContainerScreenAccessor acc = (AbstractContainerScreenAccessor) inventory;
					button.setX(acc.femboy$leftPos() + acc.femboy$imageWidth() - 16);
					button.setY(acc.femboy$topPos() - 15);
				});
			}
		});
	}
}
