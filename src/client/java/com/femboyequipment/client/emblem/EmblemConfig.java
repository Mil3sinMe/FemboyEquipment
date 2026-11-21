package com.femboyequipment.client.emblem;

import com.femboyequipment.FemboyEquipment;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import net.fabricmc.loader.api.FabricLoader;

/** Client-side emblem settings, saved to config/femboyequipment-client.json. */
public final class EmblemConfig {
	private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
	private static final Path FILE = FabricLoader.getInstance().getConfigDir().resolve("femboyequipment-client.json");

	/** Let other FemboyEquipment users see your emblem. */
	public boolean shareEmblem = true;
	/** Show other people's emblems (name tags, tab list, chat). */
	public boolean showEmblems = true;

	private static EmblemConfig instance;

	public static EmblemConfig get() {
		if (instance == null) {
			instance = load();
		}
		return instance;
	}

	private static EmblemConfig load() {
		try {
			if (Files.exists(FILE)) {
				EmblemConfig config = GSON.fromJson(Files.readString(FILE), EmblemConfig.class);
				if (config != null) {
					return config;
				}
			}
		} catch (IOException | RuntimeException e) {
			FemboyEquipment.LOGGER.warn("Couldn't read {}, using defaults", FILE, e);
		}
		return new EmblemConfig();
	}

	public void save() {
		try {
			Files.createDirectories(FILE.getParent());
			Files.writeString(FILE, GSON.toJson(this));
		} catch (IOException e) {
			FemboyEquipment.LOGGER.warn("Couldn't save {}", FILE, e);
		}
	}
}
