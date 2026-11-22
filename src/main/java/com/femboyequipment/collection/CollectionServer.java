package com.femboyequipment.collection;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.item.ModItems;
import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.temporal.IsoFields;
import java.time.temporal.TemporalAdjusters;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.UUID;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.advancements.AdvancementHolder;
import net.minecraft.advancements.AdvancementNode;
import net.minecraft.advancements.AdvancementType;
import net.minecraft.advancements.DisplayInfo;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.storage.loot.LootParams;
import net.minecraft.world.level.storage.loot.LootTable;
import net.minecraft.world.level.storage.loot.parameters.LootContextParamSets;

/**
 * Server side of the Cute Collection: FemboyEquipment's and addons' advancements become collection pages
 * (hidden from the vanilla advancement screen), plus Cute Points, ranks with rewards, and daily/weekly quests.
 */
public final class CollectionServer {
	public static final AttachmentType<CollectionData> DATA = AttachmentRegistry.create(FemboyEquipment.id("collection"),
			builder -> builder.persistent(CollectionData.CODEC).copyOnDeath().initializer(CollectionData::new));

	public static final TagKey<Item> SNACKS = QuestType.itemTag("collection_snacks");
	public static final TagKey<Block> ORES = QuestType.blockTag("collection_ores");

	private static final Set<String> NAMESPACES = Collections.synchronizedSet(new LinkedHashSet<>(List.of(FemboyEquipment.MOD_ID)));
	private static final List<String> MAIN_ORDER = List.of("main", "blahaj", "fih", "mystery");

	private static Index index;
	private static List<Item> ourItems;
	private static final Set<UUID> DIRTY_STATUS = new HashSet<>();
	private static final Set<UUID> DIRTY_PROGRESS = new HashSet<>();
	private static final Map<UUID, Integer> RANKS = new HashMap<>();
	private static boolean titlesDirty;

	private CollectionServer() {
	}

	/** Advancements in these namespaces become collection pages (AddonKit addons are added automatically). */
	public static void addNamespace(String namespace) {
		NAMESPACES.add(namespace);
	}

	public static boolean isOurs(Identifier id) {
		return NAMESPACES.contains(id.getNamespace());
	}

	// ------------------------------------------------------------ index of pages

	record PageInfo(AdvancementHolder root, List<AdvancementHolder> entries) {
	}

	record Index(Object source, List<PageInfo> pages, Map<Identifier, int[]> where, int totalPoints) {
	}

	private static Index index(MinecraftServer server) {
		var manager = server.getAdvancements();
		if (index != null && index.source() == manager) {
			return index;
		}
		List<AdvancementNode> roots = new ArrayList<>();
		for (AdvancementNode root : manager.tree().roots()) {
			if (isOurs(root.holder().id()) && root.advancement().display().isPresent()) {
				roots.add(root);
			}
		}
		roots.sort(Comparator.comparing((AdvancementNode n) -> !n.holder().id().getNamespace().equals(FemboyEquipment.MOD_ID))
				.thenComparing(n -> n.holder().id().getNamespace())
				.thenComparing(n -> {
					int k = MAIN_ORDER.indexOf(n.holder().id().getPath().split("/")[0]);
					return k < 0 ? 99 : k;
				})
				.thenComparing(n -> n.holder().id().getPath()));
		List<PageInfo> pages = new ArrayList<>();
		Map<Identifier, int[]> where = new HashMap<>();
		int total = 0;
		for (AdvancementNode root : roots) {
			List<AdvancementHolder> entries = new ArrayList<>();
			collect(root, entries);
			for (int i = 0; i < entries.size(); i++) {
				where.put(entries.get(i).id(), new int[] {pages.size(), i});
				total += Ranks.points(entries.get(i).value().display().orElseThrow().getType());
			}
			pages.add(new PageInfo(root.holder(), entries));
		}
		index = new Index(manager, pages, where, total);
		return index;
	}

	private static void collect(AdvancementNode node, List<AdvancementHolder> out) {
		if (node.advancement().display().isPresent()) {
			out.add(node.holder());
		}
		for (AdvancementNode child : node.children()) {
			collect(child, out);
		}
	}

	static List<Item> ourItems() {
		if (ourItems == null) {
			List<Item> items = new ArrayList<>();
			for (Item item : BuiltInRegistries.ITEM) {
				if (isOurs(BuiltInRegistries.ITEM.getKey(item))) {
					items.add(item);
				}
			}
			ourItems = items;
		}
		return ourItems;
	}

	// ------------------------------------------------------------ progress, points

	private static boolean done(ServerPlayer player, AdvancementHolder holder) {
		return player.getAdvancements().getOrStartProgress(holder).isDone();
	}

	private static BitSet doneBits(ServerPlayer player, PageInfo page) {
		BitSet bits = new BitSet(page.entries().size());
		for (int i = 0; i < page.entries().size(); i++) {
			if (done(player, page.entries().get(i))) {
				bits.set(i);
			}
		}
		return bits;
	}

	static long doneCount(ServerPlayer player) {
		long count = 0;
		for (PageInfo page : index(player.level().getServer()).pages()) {
			for (AdvancementHolder holder : page.entries()) {
				if (done(player, holder)) {
					count++;
				}
			}
		}
		return count;
	}

	public static int points(ServerPlayer player) {
		int points = 0;
		for (PageInfo page : index(player.level().getServer()).pages()) {
			for (AdvancementHolder holder : page.entries()) {
				if (done(player, holder)) {
					points += Ranks.points(holder.value().display().orElseThrow().getType());
				}
			}
		}
		return points;
	}

	// ------------------------------------------------------------ hooks (PlayerAdvancementsMixin)

	/** Called the moment an advancement becomes complete. */
	public static void onCompleted(ServerPlayer player, AdvancementHolder holder) {
		if (!isOurs(holder.id()) || player.connection == null) {
			return;
		}
		Index idx = index(player.level().getServer());
		int[] at = idx.where().get(holder.id());
		if (at != null && ServerPlayNetworking.canSend(player, CollectionPayloads.EntryDone.TYPE)) {
			ServerPlayNetworking.send(player, new CollectionPayloads.EntryDone(idx.pages().get(at[0]).root().id(), at[1]));
		}
		DisplayInfo display = holder.value().display().orElse(null);
		if (display != null && holder.value().parent().isPresent()) {
			String ns = holder.id().getNamespace();
			if (display.getType() == AdvancementType.GOAL) {
				give(player, new ItemStack(player.getRandom().nextBoolean() ? ModItems.BLAHAJ_CAPSULE : ModItems.FIH_CAPSULE));
				rollLoot(player, ns, "collection/goal");
				notify(player, display.getIcon().getItem(), Component.translatable("collection.femboyequipment.toast.goal"),
						display.getTitle(), 0xFF8FC7);
			} else if (display.getType() == AdvancementType.CHALLENGE) {
				give(player, new ItemStack(ModItems.BLAHAJ_CAPSULE, 3));
				give(player, new ItemStack(ModItems.FIH_CAPSULE, 3));
				rollLoot(player, ns, "collection/challenge");
				notify(player, display.getIcon().getItem(), Component.translatable("collection.femboyequipment.toast.challenge"),
						display.getTitle(), 0xC77DFF);
			}
		}
		DIRTY_STATUS.add(player.getUUID());
	}

	public static void onRevoked(ServerPlayer player, AdvancementHolder holder) {
		if (isOurs(holder.id())) {
			DIRTY_PROGRESS.add(player.getUUID());
			DIRTY_STATUS.add(player.getUUID());
		}
	}

	// ------------------------------------------------------------ syncing

	public static void sendAll(ServerPlayer player) {
		if (!ServerPlayNetworking.canSend(player, CollectionPayloads.Page.TYPE)) {
			return;
		}
		Index idx = index(player.level().getServer());
		ServerPlayNetworking.send(player, new CollectionPayloads.Reset(idx.pages().size()));
		for (PageInfo page : idx.pages()) {
			DisplayInfo root = page.root().value().display().orElseThrow();
			List<CollectionPayloads.EntryDef> defs = new ArrayList<>(page.entries().size());
			for (AdvancementHolder holder : page.entries()) {
				DisplayInfo d = holder.value().display().orElseThrow();
				defs.add(new CollectionPayloads.EntryDef(holder.id(), d.getIcon().getItem(), d.getTitle(), d.getDescription(),
						d.getType().ordinal()));
			}
			ServerPlayNetworking.send(player, new CollectionPayloads.Page(page.root().id(), root.getTitle(), root.getIcon().getItem(),
					defs, doneBits(player, page)));
		}
		DIRTY_STATUS.add(player.getUUID());
		titlesDirty = true;
	}

	private static void sendProgress(ServerPlayer player) {
		if (!ServerPlayNetworking.canSend(player, CollectionPayloads.Progress.TYPE)) {
			return;
		}
		for (PageInfo page : index(player.level().getServer()).pages()) {
			ServerPlayNetworking.send(player, new CollectionPayloads.Progress(page.root().id(), doneBits(player, page)));
		}
	}

	private static void sendStatus(ServerPlayer player) {
		CollectionData data = player.getAttachedOrCreate(DATA);
		ensureQuests(player, data);
		int total = index(player.level().getServer()).totalPoints();
		int points = points(player);
		int rank = Ranks.rankFor(points, total);
		Integer old = RANKS.put(player.getUUID(), rank);
		if (old == null || old != rank) {
			titlesDirty = true;
		}
		// Rank rewards for every rank reached but not rewarded yet (works for old worlds too).
		while (data.rewardedRank < rank) {
			data.rewardedRank++;
			rankReward(player, data.rewardedRank);
		}
		if (!ServerPlayNetworking.canSend(player, CollectionPayloads.Status.TYPE)) {
			return;
		}
		List<CollectionPayloads.QuestView> views = new ArrayList<>();
		for (CollectionData.Quest q : data.daily) {
			views.add(view(player, q, false));
		}
		for (CollectionData.Quest q : data.weekly) {
			views.add(view(player, q, true));
		}
		ServerPlayNetworking.send(player, new CollectionPayloads.Status(points, total, rank, data.showTitle, views,
				millisUntilTomorrow(), millisUntilMonday()));
	}

	private static CollectionPayloads.QuestView view(ServerPlayer player, CollectionData.Quest q, boolean weekly) {
		return new CollectionPayloads.QuestView(q.type.key, weekly, progress(player, q), q.target, q.claimed);
	}

	private static void broadcastTitles(MinecraftServer server) {
		Map<UUID, Integer> titles = new HashMap<>();
		for (ServerPlayer player : server.getPlayerList().getPlayers()) {
			Integer rank = RANKS.get(player.getUUID());
			if (rank != null && player.getAttachedOrCreate(DATA).showTitle) {
				titles.put(player.getUUID(), rank);
			}
		}
		for (ServerPlayer player : server.getPlayerList().getPlayers()) {
			if (ServerPlayNetworking.canSend(player, CollectionPayloads.Titles.TYPE)) {
				ServerPlayNetworking.send(player, new CollectionPayloads.Titles(titles));
			}
		}
	}

	// ------------------------------------------------------------ rewards

	private static void rankReward(ServerPlayer player, int rank) {
		if (rank >= 1 && rank <= ModItems.RANK_HATS.size()) {
			give(player, new ItemStack(ModItems.RANK_HATS.get(rank - 1)));
		}
		give(player, new ItemStack(ModItems.BLAHAJ_CAPSULE, rank));
		give(player, new ItemStack(ModItems.FIH_CAPSULE, rank));
		player.giveExperienceLevels(rank * 3);
		notify(player, rank >= 1 && rank <= ModItems.RANK_HATS.size() ? ModItems.RANK_HATS.get(rank - 1) : ModItems.PINK_RIBBON,
				Component.translatable("collection.femboyequipment.toast.rank", Ranks.name(rank)),
				Component.translatable("collection.femboyequipment.toast.rank_reward"), Ranks.COLORS[rank]);
	}

	private static void rollLoot(ServerPlayer player, String namespace, String path) {
		ResourceKey<LootTable> key = ResourceKey.create(Registries.LOOT_TABLE, Identifier.fromNamespaceAndPath(namespace, path));
		LootTable table = player.level().getServer().reloadableRegistries().getLootTable(key);
		if (table != LootTable.EMPTY) {
			table.getRandomItems(new LootParams.Builder(player.level()).create(LootContextParamSets.EMPTY)).forEach(s -> give(player, s));
		}
	}

	private static void give(ServerPlayer player, ItemStack stack) {
		if (!stack.isEmpty() && !player.getInventory().add(stack)) {
			player.drop(stack, false);
		}
	}

	private static void notify(ServerPlayer player, Item icon, Component title, Component subtitle, int color) {
		if (ServerPlayNetworking.canSend(player, CollectionPayloads.Notify.TYPE)) {
			ServerPlayNetworking.send(player, new CollectionPayloads.Notify(icon, title, subtitle, color));
		}
	}

	// ------------------------------------------------------------ quests

	private static String dailyKey() {
		return LocalDate.now().toString();
	}

	private static String weeklyKey() {
		LocalDate now = LocalDate.now();
		return now.get(IsoFields.WEEK_BASED_YEAR) + "-W" + now.get(IsoFields.WEEK_OF_WEEK_BASED_YEAR);
	}

	private static long millisUntilTomorrow() {
		LocalDateTime next = LocalDate.now().plusDays(1).atStartOfDay();
		return Math.max(0, next.atZone(ZoneId.systemDefault()).toInstant().toEpochMilli() - System.currentTimeMillis());
	}

	private static long millisUntilMonday() {
		LocalDateTime next = LocalDate.now().with(TemporalAdjusters.next(DayOfWeek.MONDAY)).atStartOfDay();
		return Math.max(0, next.atZone(ZoneId.systemDefault()).toInstant().toEpochMilli() - System.currentTimeMillis());
	}

	private static void ensureQuests(ServerPlayer player, CollectionData data) {
		String day = dailyKey();
		if (!day.equals(data.dailyKey)) {
			data.dailyKey = day;
			data.daily = pick(player, day, 3, false);
		}
		String week = weeklyKey();
		if (!week.equals(data.weeklyKey)) {
			data.weeklyKey = week;
			data.weekly = pick(player, week, 2, true);
		}
	}

	private static List<CollectionData.Quest> pick(ServerPlayer player, String key, int count, boolean weekly) {
		List<QuestType> types = new ArrayList<>(List.of(QuestType.values()));
		Collections.shuffle(types, new Random(player.getUUID().getMostSignificantBits() ^ key.hashCode() * 31L));
		List<CollectionData.Quest> quests = new ArrayList<>();
		for (QuestType type : types.subList(0, count)) {
			quests.add(new CollectionData.Quest(type, type.current(player), weekly ? type.weeklyTarget : type.dailyTarget, false, false));
		}
		return quests;
	}

	private static int progress(ServerPlayer player, CollectionData.Quest q) {
		return (int) Math.max(0, Math.min(q.target, q.type.current(player) - q.baseline));
	}

	private static void checkQuests(ServerPlayer player) {
		CollectionData data = player.getAttachedOrCreate(DATA);
		String oldDay = data.dailyKey;
		String oldWeek = data.weeklyKey;
		ensureQuests(player, data);
		boolean changed = !oldDay.equals(data.dailyKey) || !oldWeek.equals(data.weeklyKey);
		for (List<CollectionData.Quest> list : List.of(data.daily, data.weekly)) {
			for (CollectionData.Quest q : list) {
				if (!q.claimed && !q.notified && progress(player, q) >= q.target) {
					q.notified = true;
					changed = true;
					notify(player, Items.WRITABLE_BOOK, Component.translatable("collection.femboyequipment.toast.quest"),
							Component.translatable("quest.femboyequipment." + q.type.key, q.target), 0x7FD7FF);
				}
			}
		}
		if (changed) {
			DIRTY_STATUS.add(player.getUUID());
		}
	}

	private static void claim(ServerPlayer player, boolean weekly, int slot) {
		CollectionData data = player.getAttachedOrCreate(DATA);
		ensureQuests(player, data);
		List<CollectionData.Quest> list = weekly ? data.weekly : data.daily;
		if (slot < 0 || slot >= list.size()) {
			return;
		}
		CollectionData.Quest q = list.get(slot);
		if (q.claimed || progress(player, q) < q.target) {
			return;
		}
		q.claimed = true;
		if (weekly) {
			give(player, new ItemStack(ModItems.BLAHAJ_CAPSULE, 2));
			give(player, new ItemStack(ModItems.FIH_CAPSULE, 2));
			player.giveExperiencePoints(500);
		} else {
			give(player, new ItemStack(player.getRandom().nextBoolean() ? ModItems.BLAHAJ_CAPSULE : ModItems.FIH_CAPSULE));
			player.giveExperiencePoints(100);
		}
		notify(player, ModItems.COLLECTION_BOOK, Component.translatable("collection.femboyequipment.toast.claimed"),
				Component.translatable("quest.femboyequipment." + q.type.key, q.target), 0x7FD7FF);
		DIRTY_STATUS.add(player.getUUID());
	}

	// ------------------------------------------------------------ setup

	public static void initialize() {
		CollectionPayloads.register();

		ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> sendAll(handler.getPlayer()));
		ServerPlayConnectionEvents.DISCONNECT.register((handler, server) -> {
			RANKS.remove(handler.getPlayer().getUUID());
			titlesDirty = true;
		});
		ServerLifecycleEvents.END_DATA_PACK_RELOAD.register((server, resources, success) -> {
			index = null;
			server.getPlayerList().getPlayers().forEach(CollectionServer::sendAll);
		});
		ServerLifecycleEvents.SERVER_STOPPED.register(server -> {
			index = null;
			RANKS.clear();
			DIRTY_STATUS.clear();
			DIRTY_PROGRESS.clear();
		});

		ServerPlayNetworking.registerGlobalReceiver(CollectionPayloads.Request.TYPE,
				(payload, context) -> DIRTY_STATUS.add(context.player().getUUID()));
		ServerPlayNetworking.registerGlobalReceiver(CollectionPayloads.Claim.TYPE,
				(payload, context) -> claim(context.player(), payload.weekly(), payload.index()));
		ServerPlayNetworking.registerGlobalReceiver(CollectionPayloads.ShowTitle.TYPE, (payload, context) -> {
			context.player().getAttachedOrCreate(DATA).showTitle = payload.show();
			DIRTY_STATUS.add(context.player().getUUID());
			titlesDirty = true;
		});

		ServerTickEvents.END_SERVER_TICK.register(server -> {
			if (server.getTickCount() % 100 == 0) {
				server.getPlayerList().getPlayers().forEach(CollectionServer::checkQuests);
			}
			for (ServerPlayer player : server.getPlayerList().getPlayers()) {
				UUID id = player.getUUID();
				if (DIRTY_PROGRESS.remove(id)) {
					sendProgress(player);
				}
				if (DIRTY_STATUS.remove(id)) {
					sendStatus(player);
				}
			}
			DIRTY_STATUS.clear();
			DIRTY_PROGRESS.clear();
			if (titlesDirty) {
				titlesDirty = false;
				broadcastTitles(server);
			}
		});
	}
}
