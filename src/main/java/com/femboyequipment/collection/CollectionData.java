package com.femboyequipment.collection;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.ArrayList;
import java.util.List;

/** Per-player, per-world Cute Collection save data (rank rewards given, title setting, quests). */
public final class CollectionData {
	public static final Codec<CollectionData> CODEC = RecordCodecBuilder.create(i -> i.group(
			Codec.INT.optionalFieldOf("rewarded_rank", 0).forGetter(d -> d.rewardedRank),
			Codec.BOOL.optionalFieldOf("show_title", true).forGetter(d -> d.showTitle),
			Codec.STRING.optionalFieldOf("daily_key", "").forGetter(d -> d.dailyKey),
			Codec.STRING.optionalFieldOf("weekly_key", "").forGetter(d -> d.weeklyKey),
			Quest.CODEC.listOf().optionalFieldOf("daily", List.of()).forGetter(d -> d.daily),
			Quest.CODEC.listOf().optionalFieldOf("weekly", List.of()).forGetter(d -> d.weekly)
	).apply(i, CollectionData::new));

	public int rewardedRank;
	public boolean showTitle;
	public String dailyKey;
	public String weeklyKey;
	public List<Quest> daily;
	public List<Quest> weekly;

	public CollectionData() {
		this(0, true, "", "", List.of(), List.of());
	}

	private CollectionData(int rewardedRank, boolean showTitle, String dailyKey, String weeklyKey, List<Quest> daily,
			List<Quest> weekly) {
		this.rewardedRank = rewardedRank;
		this.showTitle = showTitle;
		this.dailyKey = dailyKey;
		this.weeklyKey = weeklyKey;
		this.daily = new ArrayList<>(daily);
		this.weekly = new ArrayList<>(weekly);
	}

	public static final class Quest {
		public static final Codec<Quest> CODEC = RecordCodecBuilder.create(i -> i.group(
				Codec.STRING.fieldOf("type").forGetter(q -> q.type.key),
				Codec.LONG.fieldOf("baseline").forGetter(q -> q.baseline),
				Codec.INT.fieldOf("target").forGetter(q -> q.target),
				Codec.BOOL.optionalFieldOf("claimed", false).forGetter(q -> q.claimed),
				Codec.BOOL.optionalFieldOf("notified", false).forGetter(q -> q.notified)
		).apply(i, (type, baseline, target, claimed, notified) -> new Quest(QuestType.byKey(type), baseline, target, claimed, notified)));

		public final QuestType type;
		public final long baseline;
		public final int target;
		public boolean claimed;
		public boolean notified;

		public Quest(QuestType type, long baseline, int target, boolean claimed, boolean notified) {
			this.type = type;
			this.baseline = baseline;
			this.target = target;
			this.claimed = claimed;
			this.notified = notified;
		}
	}
}
