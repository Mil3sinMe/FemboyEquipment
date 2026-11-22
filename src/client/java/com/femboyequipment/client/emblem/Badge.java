package com.femboyequipment.client.emblem;

import java.util.Locale;

/** Badges from the badge list, in display order (best first). Each one has its own emblem glyph. */
public enum Badge {
	OWNER("owner", "Owner", "", 0xFFD040),
	DEVELOPER("developer", "Developer", "", 0x7FD7FF),
	MODERATOR("moderator", "Moderator", "", 0x6BD48A),
	CONTRIBUTOR("contributor", "Contributor", "", 0xFF8FC7),
	ARTIST("artist", "Artist", "", 0xC77DFF),
	TRANSLATOR("translator", "Translator", "", 0x8FB8FF),
	MEDIA("media", "Media", "", 0xFF5A5A),
	BUG_HUNTER("bug_hunter", "Bug Hunter", "", 0x9BE05A),
	TESTER("tester", "Tester", "", 0x5AE0D0),
	SUPPORTER("supporter", "Supporter", "", 0xFF6FB5),
	PARTNER("partner", "Partner", "", 0xFFB347),
	OG("og", "OG", "", 0xFFE36E),
	FRIEND("friend", "Friend", "", 0xFFB3D9);

	public final String id;
	public final String displayName;
	public final String glyph;
	public final int color;

	Badge(String id, String displayName, String glyph, int color) {
		this.id = id;
		this.displayName = displayName;
		this.glyph = glyph;
		this.color = color;
	}

	/** Accepts "bug_hunter", "Bug Hunter", "bug-hunter", "contributer" (common typo)... */
	public static Badge byId(String text) {
		String id = text.trim().toLowerCase(Locale.ROOT).replace(' ', '_').replace('-', '_');
		if (id.equals("contributer")) {
			id = "contributor";
		}
		for (Badge badge : values()) {
			if (badge.id.equals(id)) {
				return badge;
			}
		}
		return null;
	}
}
