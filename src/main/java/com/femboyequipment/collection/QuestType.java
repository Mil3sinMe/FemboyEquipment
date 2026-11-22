package com.femboyequipment.collection;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.item.ModItems;
import java.util.function.ToLongFunction;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.stats.ServerStatsCounter;
import net.minecraft.stats.Stats;
import net.minecraft.tags.TagKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;

/**
 * Daily/weekly quest kinds. Progress is "stat now minus stat when the quest was handed out", using vanilla stats,
 * so nothing extra has to be tracked.
 */
public enum QuestType {
	SNACKS("snacks", 4, 24, p -> sumUsed(p, CollectionServer.SNACKS)),
	ORES("ores", 8, 48, p -> sumMined(p, CollectionServer.ORES)),
	CRAFT("craft", 16, 128, p -> sumOurItems(p, false)),
	PLACE("place", 48, 320, p -> sumOurItems(p, true)),
	CAPSULES("capsules", 2, 12, p -> used(p, ModItems.BLAHAJ_CAPSULE) + used(p, ModItems.FIH_CAPSULE)),
	COLLECT("collect", 5, 30, p -> CollectionServer.doneCount(p)),
	MOBS("mobs", 20, 120, p -> custom(p, Stats.MOB_KILLS)),
	WALK("walk", 1500, 12000, p -> custom(p, Stats.WALK_ONE_CM) / 100),
	JUMP("jump", 200, 1500, p -> custom(p, Stats.JUMP)),
	FISH("fish", 3, 20, p -> custom(p, Stats.FISH_CAUGHT)),
	TRADE("trade", 2, 12, p -> custom(p, Stats.TRADED_WITH_VILLAGER)),
	SLEEP("sleep", 1, 5, p -> custom(p, Stats.SLEEP_IN_BED));

	public final String key;
	public final int dailyTarget;
	public final int weeklyTarget;
	private final ToLongFunction<ServerPlayer> value;

	QuestType(String key, int dailyTarget, int weeklyTarget, ToLongFunction<ServerPlayer> value) {
		this.key = key;
		this.dailyTarget = dailyTarget;
		this.weeklyTarget = weeklyTarget;
		this.value = value;
	}

	public long current(ServerPlayer player) {
		return this.value.applyAsLong(player);
	}

	public static QuestType byKey(String key) {
		for (QuestType type : values()) {
			if (type.key.equals(key)) {
				return type;
			}
		}
		return SNACKS;
	}

	// ------------------------------------------------------------ stat helpers

	private static long custom(ServerPlayer player, Identifier stat) {
		return player.getStats().getValue(Stats.CUSTOM.get(stat));
	}

	private static long used(ServerPlayer player, Item item) {
		return player.getStats().getValue(Stats.ITEM_USED.get(item));
	}

	private static long sumUsed(ServerPlayer player, TagKey<Item> tag) {
		ServerStatsCounter stats = player.getStats();
		long sum = 0;
		for (Holder<Item> holder : BuiltInRegistries.ITEM.getTagOrEmpty(tag)) {
			sum += stats.getValue(Stats.ITEM_USED.get(holder.value()));
		}
		return sum;
	}

	private static long sumMined(ServerPlayer player, TagKey<Block> tag) {
		ServerStatsCounter stats = player.getStats();
		long sum = 0;
		for (Holder<Block> holder : BuiltInRegistries.BLOCK.getTagOrEmpty(tag)) {
			sum += stats.getValue(Stats.BLOCK_MINED.get(holder.value()));
		}
		return sum;
	}

	/** Crafted count of every FemboyEquipment/addon item, or "used" count of every block item (= placed). */
	private static long sumOurItems(ServerPlayer player, boolean placedBlocks) {
		ServerStatsCounter stats = player.getStats();
		long sum = 0;
		for (Item item : CollectionServer.ourItems()) {
			if (placedBlocks) {
				if (item instanceof BlockItem) {
					sum += stats.getValue(Stats.ITEM_USED.get(item));
				}
			} else {
				sum += stats.getValue(Stats.ITEM_CRAFTED.get(item));
			}
		}
		return sum;
	}

	static TagKey<Item> itemTag(String path) {
		return TagKey.create(Registries.ITEM, FemboyEquipment.id(path));
	}

	static TagKey<Block> blockTag(String path) {
		return TagKey.create(Registries.BLOCK, FemboyEquipment.id(path));
	}
}
