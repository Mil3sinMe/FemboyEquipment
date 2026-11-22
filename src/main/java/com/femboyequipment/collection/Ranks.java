package com.femboyequipment.collection;

import net.minecraft.advancements.AdvancementType;
import net.minecraft.network.chat.Component;

/**
 * Cute Points and the rank ladder. Thresholds are a share of every point available in the installed
 * FemboyEquipment content, so the ladder works the same with 1 addon or 30.
 */
public final class Ranks {
	public static final String[] KEYS = {"smol_bean", "cutie", "sweetheart", "darling", "sparkle_star",
			"pastel_prince", "plushie_royalty", "femboy_legend", "ultimate_femboy"};
	private static final double[] SHARE = {0.0, 0.005, 0.02, 0.05, 0.10, 0.20, 0.35, 0.55, 0.80};
	/** Title colors (RGB), one per rank. */
	public static final int[] COLORS = {0xC8B8C8, 0xFFB3D9, 0xFF8FC7, 0xE07BE0, 0xFFE36E, 0xB9A4FF, 0x7FD7FF, 0xFF6FB5,
			0xFFFFFF};

	private Ranks() {
	}

	public static int points(AdvancementType type) {
		return switch (type) {
			case TASK -> 1;
			case GOAL -> 5;
			case CHALLENGE -> 25;
		};
	}

	public static int threshold(int rank, int totalPoints) {
		return rank <= 0 ? 0 : Math.max(rank * 5, (int) Math.ceil(SHARE[rank] * totalPoints));
	}

	public static int rankFor(int points, int totalPoints) {
		int rank = 0;
		for (int r = 1; r < KEYS.length; r++) {
			if (points >= threshold(r, totalPoints)) {
				rank = r;
			}
		}
		return rank;
	}

	public static Component name(int rank) {
		return Component.translatable("rank.femboyequipment." + KEYS[Math.max(0, Math.min(KEYS.length - 1, rank))]);
	}
}
