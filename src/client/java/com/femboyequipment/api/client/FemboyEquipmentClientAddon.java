package com.femboyequipment.api.client;

/**
 * Client entrypoint for FemboyEquipment addons:
 *
 * <pre>{@code
 * "entrypoints": { "femboyequipment-client": ["com.example.MyAddonClient"] }
 * }</pre>
 */
@FunctionalInterface
public interface FemboyEquipmentClientAddon {
	void onFemboyEquipmentClientInit();
}
