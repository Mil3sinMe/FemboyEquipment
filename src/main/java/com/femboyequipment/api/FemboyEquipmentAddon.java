package com.femboyequipment.api;

/**
 * Entrypoint for FemboyEquipment addons. Declare it in your fabric.mod.json:
 *
 * <pre>{@code
 * "entrypoints": { "femboyequipment": ["com.example.MyAddon"] }
 * }</pre>
 *
 * It runs once, right after FemboyEquipment has registered all of its own content, so everything
 * in {@link FemboyEquipmentApi} is ready to use. Register your blocks/items here (or in your own
 * main entrypoint) - registries are still open at this point.
 */
@FunctionalInterface
public interface FemboyEquipmentAddon {
	void onFemboyEquipmentInit();
}
