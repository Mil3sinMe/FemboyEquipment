package com.femboyequipment.client.collection;

import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.toasts.Toast;
import net.minecraft.client.gui.components.toasts.ToastManager;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;

/** A pastel toast for collection goals, challenges, rank-ups and quests. */
public class CollectionToast implements Toast {
	private final ItemStack icon;
	private final Component title;
	private final Component subtitle;
	private final int color;
	private Toast.Visibility visibility = Toast.Visibility.SHOW;

	public CollectionToast(ItemStack icon, Component title, Component subtitle, int color) {
		this.icon = icon;
		this.title = title;
		this.subtitle = subtitle;
		this.color = 0xFF000000 | color;
	}

	@Override
	public Toast.Visibility getWantedVisibility() {
		return this.visibility;
	}

	@Override
	public void update(ToastManager manager, long time) {
		this.visibility = time >= 6000.0 * manager.getNotificationDisplayTimeMultiplier() ? Toast.Visibility.HIDE : Toast.Visibility.SHOW;
	}

	@Override
	public void render(GuiGraphics g, Font font, long time) {
		int w = this.width();
		int h = this.height();
		g.fill(0, 0, w, h, this.color);
		g.fill(1, 1, w - 1, h - 1, 0xFFFFF4FA);
		g.fill(1, 1, 4, h - 1, this.color);
		g.drawString(font, this.title, 30, 7, darken(this.color), false);
		g.drawString(font, font.plainSubstrByWidth(this.subtitle.getString(), w - 34), 30, 18, 0xFF5A4060, false);
		g.renderFakeItem(this.icon, 8, 8);
		// a few sparkles
		long t = time / 200;
		for (int i = 0; i < 3; i++) {
			if ((t + i) % 3 == 0) {
				g.fill(w - 8 - i * 7, 4 + i * 8, w - 7 - i * 7, 5 + i * 8, this.color);
			}
		}
	}

	private static int darken(int argb) {
		int r = ((argb >> 16) & 0xFF) * 3 / 5;
		int gr = ((argb >> 8) & 0xFF) * 3 / 5;
		int b = (argb & 0xFF) * 3 / 5;
		return 0xFF000000 | (r << 16) | (gr << 8) | b;
	}
}
