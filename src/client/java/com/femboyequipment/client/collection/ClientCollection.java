package com.femboyequipment.client.collection;

import com.femboyequipment.collection.CollectionPayloads;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayConnectionEvents;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.minecraft.client.Minecraft;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.ItemStack;

/** What the client knows about the Cute Collection (pages, progress, points, quests, everyone's titles). */
public final class ClientCollection {
	public static final class Page {
		public final Identifier id;
		public final Component title;
		public final ItemStack icon;
		public final List<CollectionPayloads.EntryDef> entries;
		public final List<ItemStack> icons = new ArrayList<>();
		public BitSet done;

		Page(CollectionPayloads.Page p) {
			this.id = p.id();
			this.title = p.title();
			this.icon = new ItemStack(p.icon());
			this.entries = p.entries();
			this.done = p.done();
			for (CollectionPayloads.EntryDef def : this.entries) {
				this.icons.add(new ItemStack(def.icon()));
			}
		}

		public int doneCount() {
			return this.done.cardinality();
		}
	}

	public static final List<Page> PAGES = new ArrayList<>();
	public static CollectionPayloads.Status status;
	public static long statusReceivedAt;
	public static final Map<UUID, Integer> TITLES = new HashMap<>();

	private ClientCollection() {
	}

	private static Page find(Identifier id) {
		for (Page page : PAGES) {
			if (page.id.equals(id)) {
				return page;
			}
		}
		return null;
	}

	public static void register() {
		ClientPlayNetworking.registerGlobalReceiver(CollectionPayloads.Reset.TYPE, (p, ctx) -> PAGES.clear());
		ClientPlayNetworking.registerGlobalReceiver(CollectionPayloads.Page.TYPE, (p, ctx) -> {
			Page old = find(p.id());
			if (old != null) {
				PAGES.set(PAGES.indexOf(old), new Page(p));
			} else {
				PAGES.add(new Page(p));
			}
		});
		ClientPlayNetworking.registerGlobalReceiver(CollectionPayloads.Progress.TYPE, (p, ctx) -> {
			Page page = find(p.page());
			if (page != null) {
				page.done = p.done();
			}
		});
		ClientPlayNetworking.registerGlobalReceiver(CollectionPayloads.EntryDone.TYPE, (p, ctx) -> {
			Page page = find(p.page());
			if (page != null) {
				page.done.set(p.index());
			}
		});
		ClientPlayNetworking.registerGlobalReceiver(CollectionPayloads.Status.TYPE, (p, ctx) -> {
			status = p;
			statusReceivedAt = System.currentTimeMillis();
		});
		ClientPlayNetworking.registerGlobalReceiver(CollectionPayloads.Notify.TYPE, (p, ctx) -> Minecraft.getInstance()
				.getToastManager().addToast(new CollectionToast(new ItemStack(p.icon()), p.title(), p.subtitle(), p.color())));
		ClientPlayNetworking.registerGlobalReceiver(CollectionPayloads.Titles.TYPE, (p, ctx) -> {
			TITLES.clear();
			TITLES.putAll(p.ranks());
		});
		ClientPlayConnectionEvents.DISCONNECT.register((handler, client) -> {
			PAGES.clear();
			TITLES.clear();
			status = null;
		});
	}
}
