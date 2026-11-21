package com.femboyequipment.effect;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.api.OutfitEffect;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.Reader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.ResourceManagerReloadListener;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;

/**
 * Datapack addons: loads {@code data/<namespace>/femboyequipment/outfit_effects/*.json}.
 *
 * <pre>{@code
 * {
 *   "type": "worn",                         // "worn", "accessory" or "set"
 *   "items": ["minecraft:carved_pumpkin"],  // for "set": all of these must be worn at once
 *   "effects": [{ "id": "minecraft:night_vision", "amplifier": 0 }]
 * }
 * }</pre>
 */
public final class OutfitEffectsData implements ResourceManagerReloadListener {
	public static final Identifier ID = FemboyEquipment.id("outfit_effects");
	private static final String FOLDER = "femboyequipment/outfit_effects";

	@Override
	public void onResourceManagerReload(ResourceManager manager) {
		OutfitEffects.clearData();
		int loaded = 0;
		for (Map.Entry<Identifier, Resource> entry : manager.listResources(FOLDER, id -> id.getPath().endsWith(".json")).entrySet()) {
			try (Reader reader = entry.getValue().openAsReader()) {
				JsonObject json = JsonParser.parseReader(reader).getAsJsonObject();
				apply(json);
				loaded++;
			} catch (Exception e) {
				FemboyEquipment.LOGGER.error("Couldn't load outfit effect {}: {}", entry.getKey(), e.getMessage());
			}
		}
		if (loaded > 0) {
			FemboyEquipment.LOGGER.info("Loaded {} datapack outfit effect file(s)", loaded);
		}
	}

	private static void apply(JsonObject json) {
		String type = json.has("type") ? json.get("type").getAsString() : "worn";
		List<Item> items = new ArrayList<>();
		for (JsonElement e : array(json, "items")) {
			Identifier id = Identifier.parse(e.getAsString());
			Item item = BuiltInRegistries.ITEM.getValue(id);
			if (item == Items.AIR) {
				throw new IllegalArgumentException("unknown item " + id);
			}
			items.add(item);
		}
		List<OutfitEffect> effects = new ArrayList<>();
		for (JsonElement e : array(json, "effects")) {
			JsonObject o = e.getAsJsonObject();
			Identifier id = Identifier.parse(o.get("id").getAsString());
			Optional<Holder.Reference<MobEffect>> effect = BuiltInRegistries.MOB_EFFECT.get(id);
			int amplifier = o.has("amplifier") ? o.get("amplifier").getAsInt() : 0;
			effects.add(new OutfitEffect(effect.orElseThrow(() -> new IllegalArgumentException("unknown effect " + id)), amplifier));
		}
		switch (type) {
			case "worn" -> items.forEach(item -> OutfitEffects.addWornData(item, effects));
			case "accessory" -> items.forEach(item -> OutfitEffects.addAccessoryData(item, effects));
			case "set" -> OutfitEffects.addSetData(items, effects);
			default -> throw new IllegalArgumentException("unknown type " + type + " (use worn, accessory or set)");
		}
	}

	private static JsonArray array(JsonObject json, String key) {
		if (!json.has(key) || !json.get(key).isJsonArray()) {
			throw new IllegalArgumentException("missing \"" + key + "\" array");
		}
		return json.getAsJsonArray(key);
	}
}
