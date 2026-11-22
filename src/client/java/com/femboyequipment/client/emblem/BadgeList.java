package com.femboyequipment.client.emblem;

import com.femboyequipment.FemboyEquipment;
import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.URLConnection;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import net.fabricmc.loader.api.FabricLoader;

/**
 * Badges for certain players (owner, contributor, media, bug hunter, tester...), read from
 * <a href="https://github.com/NeonWardonmc/FemboyEquipment-Badge-Users">FemboyEquipment-Badge-Users</a>.
 *
 * <p>File format ({@code badges.txt}), one player per line, {@code #} starts a comment:
 * <pre>uuid | badge[,badge...] | backup-username</pre>
 * The backup username is used on offline-mode servers, where players don't have their real UUIDs.
 * The list is downloaded on startup and every 30 minutes, and cached so badges still show offline.
 */
public final class BadgeList {
	private static final String URL = System.getProperty("femboyequipment.badgeUrl",
			"https://raw.githubusercontent.com/NeonWardonmc/FemboyEquipment-Badge-Users/main/badges.txt");
	private static final Path CACHE = FabricLoader.getInstance().getConfigDir().resolve("femboyequipment-badges-cache.txt");
	private static final int MAX_BYTES = 1 << 20;

	private static volatile Map<UUID, Set<Badge>> byUuid = Map.of();
	private static volatile Map<String, Set<Badge>> byName = Map.of();
	private static boolean started;

	private BadgeList() {
	}

	/** Loads the cache right away and starts downloading the list in the background (once). */
	public static synchronized void start() {
		if (started) {
			return;
		}
		started = true;
		try {
			if (Files.exists(CACHE)) {
				parse(Files.readString(CACHE, StandardCharsets.UTF_8));
			}
		} catch (IOException | RuntimeException e) {
			FemboyEquipment.LOGGER.warn("Couldn't read the badge cache", e);
		}
		ScheduledExecutorService executor = Executors.newSingleThreadScheduledExecutor(r -> {
			Thread thread = new Thread(r, "FemboyEquipment badge list");
			thread.setDaemon(true);
			return thread;
		});
		executor.scheduleWithFixedDelay(BadgeList::download, 0, 30, TimeUnit.MINUTES);
	}

	private static void download() {
		try {
			URLConnection connection = URI.create(URL).toURL().openConnection();
			connection.setConnectTimeout(10_000);
			connection.setReadTimeout(10_000);
			connection.setRequestProperty("User-Agent", "FemboyEquipment");
			String text;
			try (InputStream in = connection.getInputStream()) {
				text = new String(in.readNBytes(MAX_BYTES), StandardCharsets.UTF_8);
			}
			int count = parse(text);
			Files.createDirectories(CACHE.getParent());
			Files.writeString(CACHE, text, StandardCharsets.UTF_8);
			FemboyEquipment.LOGGER.info("Loaded {} badge user(s)", count);
		} catch (IOException | RuntimeException e) {
			FemboyEquipment.LOGGER.warn("Couldn't download the badge list ({}), using the cached one", e.toString());
		}
	}

	/** Parses the list and swaps it in. Returns how many players got at least one badge. */
	static int parse(String text) {
		Map<UUID, Set<Badge>> uuids = new HashMap<>();
		Map<String, Set<Badge>> names = new HashMap<>();
		for (String raw : text.split("\\R")) {
			int hash = raw.indexOf('#');
			String line = (hash >= 0 ? raw.substring(0, hash) : raw).trim();
			if (line.isEmpty()) {
				continue;
			}
			String[] parts = line.split("\\|");
			if (parts.length < 2) {
				continue;
			}
			Set<Badge> badges = EnumSet.noneOf(Badge.class);
			for (String id : parts[1].split(",")) {
				Badge badge = Badge.byId(id);
				if (badge != null) {
					badges.add(badge);
				}
			}
			if (badges.isEmpty()) {
				continue;
			}
			String uuid = parts[0].trim();
			if (!uuid.isEmpty()) {
				try {
					uuids.computeIfAbsent(UUID.fromString(uuid), k -> EnumSet.noneOf(Badge.class)).addAll(badges);
				} catch (IllegalArgumentException ignored) {
					// not a UUID, the username column can still match
				}
			}
			if (parts.length >= 3 && !parts[2].trim().isEmpty()) {
				names.computeIfAbsent(parts[2].trim().toLowerCase(Locale.ROOT), k -> EnumSet.noneOf(Badge.class)).addAll(badges);
			}
		}
		byUuid = uuids;
		byName = names;
		return Math.max(uuids.size(), names.size());
	}

	/**
	 * The player's badges, best first. Real Mojang accounts always have version 4 UUIDs; anything else comes from
	 * an offline-mode server (made up from the name), so the backup username is used there instead.
	 */
	public static List<Badge> get(UUID uuid, String username) {
		Set<Badge> badges = byUuid.get(uuid);
		if (badges == null && uuid.version() != 4 && username != null) {
			badges = byName.get(username.toLowerCase(Locale.ROOT));
		}
		if (badges == null) {
			return List.of();
		}
		List<Badge> sorted = new ArrayList<>(badges);
		Collections.sort(sorted);
		return sorted;
	}
}
