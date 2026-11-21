package com.example.femboyaddon.client;

import com.example.femboyaddon.ExampleAddon;
import com.femboyequipment.api.client.AccessoryShape;
import com.femboyequipment.api.client.FemboyEquipmentClientAddon;
import com.femboyequipment.api.client.FemboyEquipmentClientApi;

public class ExampleAddonClient implements FemboyEquipmentClientAddon {
	@Override
	public void onFemboyEquipmentClientInit() {
		// Reuse FemboyEquipment's 3D cat ears + tail shapes with fox textures (no tint: 0xFFFFFF).
		FemboyEquipmentClientApi.registerAccessory(ExampleAddon.FOX_EARS, AccessoryShape.CAT_EARS,
				ExampleAddon.id("textures/entity/accessory/fox_ears.png"),
				ExampleAddon.id("textures/entity/accessory/fox_ears_overlay.png"), 0xFFFFFF);
		FemboyEquipmentClientApi.registerAccessory(ExampleAddon.FOX_EARS, AccessoryShape.CAT_TAIL,
				ExampleAddon.id("textures/entity/accessory/fox_tail.png"),
				ExampleAddon.id("textures/entity/accessory/fox_tail_overlay.png"), 0xFFFFFF);
	}
}
