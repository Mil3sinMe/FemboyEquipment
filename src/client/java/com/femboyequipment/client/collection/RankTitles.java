package com.femboyequipment.client.collection;

import com.femboyequipment.collection.Ranks;
import java.util.UUID;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.network.chat.TextColor;

/** Shows a player's collection rank as a little title before their name (chat, tab list, name tag). */
public final class RankTitles {
	private RankTitles() {
	}

	public static Component decorate(UUID uuid, Component name) {
		Integer rank = ClientCollection.TITLES.get(uuid);
		if (rank == null || rank <= 0) {
			return name;
		}
		MutableComponent title = Component.literal("[").append(Ranks.name(rank)).append("]")
				.withStyle(style -> style.withColor(TextColor.fromRgb(Ranks.COLORS[rank])));
		return Component.empty().append(title).append(" ").append(name);
	}
}
