package com.femboyequipment.client.collection;

import com.femboyequipment.collection.CollectionPayloads;
import com.femboyequipment.collection.Ranks;
import com.femboyequipment.item.ModItems;
import java.util.ArrayList;
import java.util.List;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.ChatFormatting;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.input.MouseButtonEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.network.chat.TextColor;
import net.minecraft.util.Mth;
import net.minecraft.world.item.ItemStack;

/** The Cute Collection: collection pages, daily/weekly quests and ranks. */
public class CollectionScreen extends Screen {
	private static final int PINK = 0xFFFF8FC7;
	private static final int PINK_DARK = 0xFFB0507F;
	private static final int PANEL = 0xFFFFF4FA;
	private static final int PANEL_EDGE = 0xFFFFC2E0;
	private static final int TEXT = 0xFF5A4060;
	private static final int TEXT_SOFT = 0xFF9A7FA0;
	private static final int CELL = 18;
	private static final String[] TABS = {"collection", "quests", "ranks"};

	private static int tab;
	private static int selectedPage;
	private static int sideScroll;
	private int gridScroll;

	private int left;
	private int top;
	private int w;
	private int h;
	private final List<Runnable> clicks = new ArrayList<>();
	private final List<int[]> clickBoxes = new ArrayList<>();

	public CollectionScreen() {
		super(Component.translatable("collection.femboyequipment.title"));
	}

	@Override
	protected void init() {
		this.w = Math.min(this.width - 12, 420);
		this.h = Math.min(this.height - 12, 240);
		this.left = (this.width - this.w) / 2;
		this.top = (this.height - this.h) / 2;
		if (ClientPlayNetworking.canSend(CollectionPayloads.Request.TYPE)) {
			ClientPlayNetworking.send(new CollectionPayloads.Request());
		}
	}

	@Override
	public boolean isPauseScreen() {
		return false;
	}

	// ------------------------------------------------------------ rendering

	@Override
	public void render(GuiGraphics g, int mouseX, int mouseY, float partialTick) {
		super.render(g, mouseX, mouseY, partialTick);
		this.clicks.clear();
		this.clickBoxes.clear();
		int l = this.left;
		int t = this.top;
		g.fill(l - 2, t - 2, l + this.w + 2, t + this.h + 2, PINK);
		g.fill(l, t, l + this.w, t + this.h, PANEL);
		g.fill(l, t, l + this.w, t + 20, PANEL_EDGE);
		g.drawString(this.font, Component.literal("✿ ").append(this.title).append(" ✿"), l + 8, t + 6, PINK_DARK, false);

		// tabs
		int tx = l + this.w - 4;
		for (int i = TABS.length - 1; i >= 0; i--) {
			Component label = Component.translatable("collection.femboyequipment.tab." + TABS[i]);
			int tw = this.font.width(label) + 12;
			tx -= tw + 2;
			int x0 = tx;
			boolean active = tab == i;
			boolean hover = in(mouseX, mouseY, x0, t + 3, tw, 15);
			g.fill(x0, t + 3, x0 + tw, t + 18, active ? PINK : hover ? 0xFFFFB3D9 : 0xFFFFE0EF);
			g.drawString(this.font, label, x0 + 6, t + 7, active ? 0xFFFFFFFF : TEXT, false);
			int idx = i;
			this.button(x0, t + 3, tw, 15, () -> tab = idx);
		}

		if (ClientCollection.PAGES.isEmpty()) {
			g.drawCenteredString(this.font, Component.translatable("collection.femboyequipment.loading"), l + this.w / 2,
					t + this.h / 2, TEXT_SOFT);
			return;
		}
		switch (tab) {
			case 1 -> this.renderQuests(g, mouseX, mouseY);
			case 2 -> this.renderRanks(g, mouseX, mouseY);
			default -> this.renderCollection(g, mouseX, mouseY);
		}
	}

	private void renderCollection(GuiGraphics g, int mouseX, int mouseY) {
		List<ClientCollection.Page> pages = ClientCollection.PAGES;
		selectedPage = Mth.clamp(selectedPage, 0, pages.size() - 1);
		int sx = this.left + 4;
		int sy = this.top + 24;
		int sw = 124;
		int sh = this.h - 28;
		int rows = sh / 20;
		sideScroll = Mth.clamp(sideScroll, 0, Math.max(0, pages.size() - rows));

		// totals
		int done = 0;
		int all = 0;
		for (ClientCollection.Page p : pages) {
			done += p.doneCount();
			all += p.entries.size();
		}

		g.fill(sx, sy, sx + sw, sy + sh, 0xFFFFE8F3);
		g.enableScissor(sx, sy, sx + sw, sy + sh);
		for (int i = 0; i < rows + 1 && i + sideScroll < pages.size(); i++) {
			int pi = i + sideScroll;
			ClientCollection.Page p = pages.get(pi);
			int ry = sy + i * 20;
			boolean sel = pi == selectedPage;
			if (sel || in(mouseX, mouseY, sx, ry, sw, 20)) {
				g.fill(sx, ry, sx + sw, ry + 20, sel ? 0xFFFFC2E0 : 0xFFFFD6EA);
			}
			g.renderItem(p.icon, sx + 2, ry + 2);
			String name = this.font.plainSubstrByWidth(p.title.getString(), sw - 46);
			g.drawString(this.font, name, sx + 20, ry + 6, TEXT, false);
			boolean complete = p.doneCount() == p.entries.size();
			String pct = complete ? "✔" : (p.doneCount() * 100 / Math.max(1, p.entries.size())) + "%";
			g.drawString(this.font, pct, sx + sw - 4 - this.font.width(pct), ry + 6, complete ? 0xFF3FA060 : TEXT_SOFT, false);
			this.button(sx, ry, sw, 20, () -> {
				selectedPage = pi;
				this.gridScroll = 0;
			});
		}
		g.disableScissor();

		// selected page
		ClientCollection.Page page = pages.get(selectedPage);
		int gx = sx + sw + 6;
		int gw = this.left + this.w - 6 - gx;
		g.drawString(this.font, page.title, gx, sy + 1, PINK_DARK, false);
		String count = page.doneCount() + " / " + page.entries.size();
		g.drawString(this.font, count, gx + gw - this.font.width(count), sy + 1, TEXT, false);
		bar(g, gx, sy + 11, gw, 5, page.doneCount() / (float) Math.max(1, page.entries.size()), PINK);
		g.drawString(this.font, Component.translatable("collection.femboyequipment.total", done, all), gx, this.top + this.h - 11,
				TEXT_SOFT, false);

		int gy = sy + 20;
		int gh = this.top + this.h - 14 - gy;
		int cols = Math.max(1, gw / CELL);
		int visibleRows = Math.max(1, gh / CELL);
		int totalRows = (page.entries.size() + cols - 1) / cols;
		this.gridScroll = Mth.clamp(this.gridScroll, 0, Math.max(0, totalRows - visibleRows));
		CollectionPayloads.EntryDef hovered = null;
		boolean hoveredDone = false;
		g.enableScissor(gx, gy, gx + gw, gy + gh);
		for (int i = this.gridScroll * cols; i < page.entries.size() && i < (this.gridScroll + visibleRows + 1) * cols; i++) {
			int row = i / cols - this.gridScroll;
			int cx = gx + (i % cols) * CELL;
			int cy = gy + row * CELL;
			CollectionPayloads.EntryDef e = page.entries.get(i);
			boolean got = page.done.get(i);
			int frame = e.type() == 2 ? 0xFFB06CFF : e.type() == 1 ? 0xFFFFC94D : (got ? 0xFFFFB3D9 : 0xFF8C7A93);
			g.fill(cx, cy, cx + CELL - 1, cy + CELL - 1, frame);
			g.fill(cx + 1, cy + 1, cx + CELL - 2, cy + CELL - 2, got ? 0xFFFFF0F8 : 0xFF54465C);
			g.renderItem(page.icons.get(i), cx + 1, cy + 1);
			if (in(mouseX, mouseY, cx, cy, CELL - 1, CELL - 1) && mouseY < gy + gh) {
				hovered = e;
				hoveredDone = got;
			}
		}
		// dim everything not collected yet (drawn above the items)
		g.nextStratum();
		for (int i = this.gridScroll * cols; i < page.entries.size() && i < (this.gridScroll + visibleRows + 1) * cols; i++) {
			if (!page.done.get(i)) {
				int row = i / cols - this.gridScroll;
				int cx = gx + (i % cols) * CELL;
				int cy = gy + row * CELL;
				g.fill(cx + 1, cy + 1, cx + CELL - 2, cy + CELL - 2, 0xB8302838);
			}
		}
		g.disableScissor();
		if (totalRows > visibleRows) {
			int barH = Math.max(10, gh * visibleRows / totalRows);
			int barY = gy + (gh - barH) * this.gridScroll / Math.max(1, totalRows - visibleRows);
			g.fill(gx + gw + 1, barY, gx + gw + 3, barY + barH, PINK);
		}
		if (hovered != null) {
			List<Component> lines = new ArrayList<>();
			int color = hovered.type() == 2 ? 0xB06CFF : hovered.type() == 1 ? 0xFFC94D : 0xFF8FC7;
			lines.add(hovered.title().copy().withStyle(s -> s.withColor(TextColor.fromRgb(color))));
			lines.add(hovered.description().copy().withStyle(ChatFormatting.GRAY));
			lines.add(Component.translatable(hoveredDone ? "collection.femboyequipment.collected" : "collection.femboyequipment.missing")
					.withStyle(hoveredDone ? ChatFormatting.GREEN : ChatFormatting.DARK_GRAY));
			lines.add(Component.translatable("collection.femboyequipment.points",
					Ranks.points(net.minecraft.advancements.AdvancementType.values()[hovered.type()])).withStyle(ChatFormatting.LIGHT_PURPLE));
			g.setTooltipForNextFrame(this.font, lines, java.util.Optional.empty(), mouseX, mouseY);
		}
	}

	private void renderQuests(GuiGraphics g, int mouseX, int mouseY) {
		CollectionPayloads.Status s = ClientCollection.status;
		int x = this.left + 10;
		int y = this.top + 26;
		int qw = this.w - 20;
		if (s == null) {
			g.drawCenteredString(this.font, Component.translatable("collection.femboyequipment.loading"), this.left + this.w / 2,
					this.top + this.h / 2, TEXT_SOFT);
			return;
		}
		long elapsed = System.currentTimeMillis() - ClientCollection.statusReceivedAt;
		int dailyIndex = 0;
		int weeklyIndex = 0;
		boolean weeklyHeader = false;
		g.drawString(this.font, Component.translatable("collection.femboyequipment.daily", time(s.dailyResetMs() - elapsed)), x, y,
				PINK_DARK, false);
		y += 12;
		for (CollectionPayloads.QuestView q : s.quests()) {
			if (q.weekly() && !weeklyHeader) {
				weeklyHeader = true;
				y += 4;
				g.drawString(this.font, Component.translatable("collection.femboyequipment.weekly", time(s.weeklyResetMs() - elapsed)),
						x, y, PINK_DARK, false);
				y += 12;
			}
			int slot = q.weekly() ? weeklyIndex++ : dailyIndex++;
			boolean complete = q.progress() >= q.target();
			g.fill(x, y, x + qw, y + 30, q.claimed() ? 0xFFE6F6EA : 0xFFFFE8F3);
			g.drawString(this.font, Component.translatable("quest.femboyequipment." + q.type(), q.target()), x + 5, y + 4, TEXT, false);
			g.drawString(this.font, Component.translatable(q.weekly() ? "collection.femboyequipment.reward.weekly"
					: "collection.femboyequipment.reward.daily"), x + 5, y + 19, TEXT_SOFT, false);
			int bx = x + qw - 150;
			bar(g, bx, y + 6, 90, 6, q.progress() / (float) Math.max(1, q.target()), complete ? 0xFF6BD48A : PINK);
			String prog = q.progress() + "/" + q.target();
			g.drawString(this.font, prog, bx + 45 - this.font.width(prog) / 2, y + 16, TEXT_SOFT, false);
			int cbx = x + qw - 54;
			if (q.claimed()) {
				g.drawString(this.font, Component.translatable("collection.femboyequipment.claimed"), cbx + 2, y + 11, 0xFF3FA060, false);
			} else if (complete) {
				boolean hover = in(mouseX, mouseY, cbx, y + 7, 48, 16);
				g.fill(cbx, y + 7, cbx + 48, y + 23, hover ? 0xFFFF6FB5 : PINK);
				g.drawCenteredString(this.font, Component.translatable("collection.femboyequipment.claim"), cbx + 24, y + 11, 0xFFFFFFFF);
				boolean weekly = q.weekly();
				this.button(cbx, y + 7, 48, 16, () -> ClientPlayNetworking.send(new CollectionPayloads.Claim(weekly, slot)));
			}
			y += 33;
		}
	}

	private void renderRanks(GuiGraphics g, int mouseX, int mouseY) {
		CollectionPayloads.Status s = ClientCollection.status;
		if (s == null) {
			g.drawCenteredString(this.font, Component.translatable("collection.femboyequipment.loading"), this.left + this.w / 2,
					this.top + this.h / 2, TEXT_SOFT);
			return;
		}
		int x = this.left + 10;
		int y = this.top + 28;
		int half = this.w / 2 - 14;
		int rank = s.rank();
		g.drawString(this.font, Component.translatable("collection.femboyequipment.your_rank"), x, y, TEXT_SOFT, false);
		g.pose().pushMatrix();
		g.pose().translate(x, y + 12);
		g.pose().scale(2.0F, 2.0F);
		g.drawString(this.font, Ranks.name(rank), 0, 0, 0xFF000000 | darkenTitle(Ranks.COLORS[rank]), false);
		g.pose().popMatrix();
		y += 36;
		g.drawString(this.font, Component.translatable("collection.femboyequipment.cute_points", s.points(), s.totalPoints()), x, y,
				TEXT, false);
		y += 12;
		if (rank < Ranks.KEYS.length - 1) {
			int from = Ranks.threshold(rank, s.totalPoints());
			int to = Ranks.threshold(rank + 1, s.totalPoints());
			bar(g, x, y, half, 7, (s.points() - from) / (float) Math.max(1, to - from), PINK);
			y += 11;
			g.drawString(this.font, Component.translatable("collection.femboyequipment.next_rank", to - s.points(), Ranks.name(rank + 1)),
					x, y, TEXT_SOFT, false);
		} else {
			bar(g, x, y, half, 7, 1.0F, 0xFFFFE36E);
			y += 11;
			g.drawString(this.font, Component.translatable("collection.femboyequipment.max_rank"), x, y, TEXT_SOFT, false);
		}
		y += 18;
		for (String key : new String[] {"points_help", "rank_rewards"}) {
			for (var line : this.font.split(Component.translatable("collection.femboyequipment." + key), half)) {
				g.drawString(this.font, line, x, y, TEXT_SOFT, false);
				y += 10;
			}
			y += 2;
		}

		// title toggle
		int ty = this.top + this.h - 24;
		Component label = Component.translatable(s.showTitle() ? "collection.femboyequipment.title_on" : "collection.femboyequipment.title_off");
		int tw = this.font.width(label) + 12;
		boolean hover = in(mouseX, mouseY, x, ty, tw, 16);
		g.fill(x, ty, x + tw, ty + 16, hover ? 0xFFFF6FB5 : PINK);
		g.drawString(this.font, label, x + 6, ty + 4, 0xFFFFFFFF, false);
		boolean show = s.showTitle();
		this.button(x, ty, tw, 16, () -> ClientPlayNetworking.send(new CollectionPayloads.ShowTitle(!show)));

		// ladder
		int lx = this.left + this.w / 2 + 4;
		int ly = this.top + 26;
		int rowH = Math.min(22, (this.h - 30) / Ranks.KEYS.length);
		for (int r = 0; r < Ranks.KEYS.length; r++) {
			boolean reached = r <= rank;
			int ry = ly + r * rowH;
			g.fill(lx, ry, lx + half + 4, ry + rowH - 2, r == rank ? 0xFFFFC2E0 : reached ? 0xFFFFE8F3 : 0xFFF1E6F0);
			ItemStack icon = r == 0 ? new ItemStack(ModItems.PINK_RIBBON) : new ItemStack(ModItems.RANK_HATS.get(r - 1));
			g.renderItem(icon, lx + 2, ry + (rowH - 18) / 2 + 1);
			MutableComponent name = Ranks.name(r).copy();
			g.drawString(this.font, name, lx + 22, ry + (rowH - 10) / 2, reached ? 0xFF000000 | darkenTitle(Ranks.COLORS[r]) : TEXT_SOFT,
					false);
			String pts = reached ? "✔" : String.valueOf(Ranks.threshold(r, s.totalPoints()));
			g.drawString(this.font, pts, lx + half - this.font.width(pts), ry + (rowH - 10) / 2, reached ? 0xFF3FA060 : TEXT_SOFT, false);
			if (r > 0 && in(mouseX, mouseY, lx, ry, half + 4, rowH - 2)) {
				g.setTooltipForNextFrame(this.font, List.of(Ranks.name(r),
						Component.translatable("collection.femboyequipment.rank_reward_line", icon.getHoverName(), r, r * 3)
								.withStyle(ChatFormatting.GRAY)), java.util.Optional.empty(), mouseX, mouseY);
			}
		}
	}

	// ------------------------------------------------------------ helpers

	private static int darkenTitle(int rgb) {
		int r = (rgb >> 16) & 0xFF;
		int gr = (rgb >> 8) & 0xFF;
		int b = rgb & 0xFF;
		return ((r * 7 / 10) << 16) | ((gr * 7 / 10) << 8) | (b * 7 / 10);
	}

	private static void bar(GuiGraphics g, int x, int y, int width, int height, float fraction, int color) {
		g.fill(x, y, x + width, y + height, 0xFFE9D3E2);
		int fw = (int) (width * Mth.clamp(fraction, 0.0F, 1.0F));
		g.fill(x, y, x + fw, y + height, color);
		g.fill(x, y, x + fw, y + 1, 0x60FFFFFF);
	}

	private static Component time(long ms) {
		long minutes = Math.max(0, ms) / 60000;
		long days = minutes / 1440;
		long hours = (minutes / 60) % 24;
		long mins = minutes % 60;
		return Component.literal(days > 0 ? days + "d " + hours + "h" : hours + "h " + mins + "m");
	}

	private static boolean in(double mx, double my, int x, int y, int width, int height) {
		return mx >= x && mx < x + width && my >= y && my < y + height;
	}

	private void button(int x, int y, int width, int height, Runnable action) {
		this.clickBoxes.add(new int[] {x, y, width, height});
		this.clicks.add(action);
	}

	// ------------------------------------------------------------ input

	@Override
	public boolean mouseClicked(MouseButtonEvent event, boolean doubleClick) {
		if (event.button() == 0) {
			for (int i = this.clickBoxes.size() - 1; i >= 0; i--) {
				int[] b = this.clickBoxes.get(i);
				if (in(event.x(), event.y(), b[0], b[1], b[2], b[3])) {
					this.clicks.get(i).run();
					this.minecraft.getSoundManager().play(net.minecraft.client.resources.sounds.SimpleSoundInstance.forUI(
							net.minecraft.sounds.SoundEvents.UI_BUTTON_CLICK, 1.2F));
					return true;
				}
			}
		}
		return super.mouseClicked(event, doubleClick);
	}

	@Override
	public boolean mouseScrolled(double mouseX, double mouseY, double scrollX, double scrollY) {
		if (tab == 0) {
			int step = scrollY > 0 ? -1 : 1;
			if (mouseX < this.left + 128) {
				sideScroll += step;
			} else {
				this.gridScroll += step;
			}
			return true;
		}
		return super.mouseScrolled(mouseX, mouseY, scrollX, scrollY);
	}
}
