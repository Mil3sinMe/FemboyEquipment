package com.femboyequipment.collection;

/** Lets common code (the Collection Book) open the client-only screen without loading client classes. */
public final class CollectionHooks {
	public static Runnable openScreen = () -> {
	};

	private CollectionHooks() {
	}
}
