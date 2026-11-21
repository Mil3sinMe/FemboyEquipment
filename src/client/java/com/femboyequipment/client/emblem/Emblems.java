package com.femboyequipment.client.emblem;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.client.mixin.AvatarAccessor;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import net.minecraft.client.Minecraft;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.FontDescription;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.network.chat.Style;
import net.minecraft.world.entity.player.Player;

/**
 * Lunar-style emblems: FemboyEquipment users can see each other on any server.
 *
 * <p>How it works: the client always sends its skin-layer settings (hat, jacket, sleeves...) to the
 * server as a bit mask, and the server shares that byte with every other player. Vanilla only uses
 * the lower 7 bits, so we set the unused top bit as a "has FemboyEquipment" flag. No server-side
 * support or external backend needed.
 */
public final class Emblems {
	/** Unused 8th bit of the skin-layer byte. */
	public static final int FLAG = 0x80;

	private static final FontDescription FONT = new FontDescription.Resource(FemboyEquipment.id("emblem"));
	private static final String NORMAL = "";
	private static final String SPECIAL = "";

	/** People who get the special crown emblem. */
	private static final Set<UUID> SPECIAL_PLAYERS = Set.of(
			UUID.fromString("9c06d07d-d8b3-47f7-aee0-3b571027d441"), // IShowAvoid
			UUID.fromString("8e6897f4-63f2-4068-8822-c38652ee8524"), // Mil3sinMe
			UUID.fromString("22ffc62a-47d7-4966-93a6-abb3184adada"), // Wxtrix
			UUID.fromString("7278262a-321a-4008-b904-cf3970b1caa9"), // MilesinMe562
			UUID.fromString("43a7ce2e-bab5-4ec4-a7c2-3370f3181f0b")); // xvD8

	/** Everyone we've seen with the flag this session, so the tab list still knows them when they're out of range. */
	private static final Set<UUID> KNOWN_USERS = ConcurrentHashMap.newKeySet();

	private Emblems() {
	}

	/** Checks a player entity for the flag and remembers them. */
	public static boolean check(Player player) {
		if (isSelf(player.getUUID())) {
			return true;
		}
		byte parts = player.getEntityData().get(AvatarAccessor.femboy$getModeCustomisation());
		if ((parts & FLAG) != 0) {
			KNOWN_USERS.add(player.getUUID());
			return true;
		}
		KNOWN_USERS.remove(player.getUUID());
		return false;
	}

	public static boolean isKnownUser(UUID uuid) {
		return isSelf(uuid) || KNOWN_USERS.contains(uuid);
	}

	private static boolean isSelf(UUID uuid) {
		Minecraft mc = Minecraft.getInstance();
		return mc.player != null && mc.player.getUUID().equals(uuid);
	}

	/** Returns the name with the right emblem in front. */
	public static Component decorate(UUID uuid, Component name) {
		String glyph = SPECIAL_PLAYERS.contains(uuid) ? SPECIAL : NORMAL;
		MutableComponent emblem = Component.literal(glyph).setStyle(Style.EMPTY.withFont(FONT));
		return Component.empty().append(emblem).append(" ").append(name);
	}

	public static void clear() {
		KNOWN_USERS.clear();
	}
}
