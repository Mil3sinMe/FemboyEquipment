package com.femboyequipment.api.client;

import com.femboyequipment.client.render.AccessoryLayer;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.Item;
import org.jspecify.annotations.Nullable;

/** Client-side API for FemboyEquipment addons. */
public final class FemboyEquipmentClientApi {
	private FemboyEquipmentClientApi() {
	}

	/**
	 * Draws one of FemboyEquipment's 3D accessory models on players, mannequins and Femboy Traders
	 * while they wear {@code item} (in any armor slot). Call it several times to attach more than one
	 * shape to the same item (e.g. ears and a tail).
	 *
	 * @param texture      full texture path, e.g. {@code mymod:textures/entity/accessory/fox_ears.png}.
	 *                     It is tinted with the item's dye color (or {@code undyedColor}).
	 * @param overlay      optional untinted texture drawn on top (inner ears, lace, ...), or null
	 * @param undyedColor  RGB tint when the item isn't dyed; use 0xFFFFFF for "no tint"
	 */
	public static void registerAccessory(Item item, AccessoryShape shape, Identifier texture,
			@Nullable Identifier overlay, int undyedColor) {
		AccessoryLayer.register(item, shape, texture, overlay, undyedColor);
	}
}
