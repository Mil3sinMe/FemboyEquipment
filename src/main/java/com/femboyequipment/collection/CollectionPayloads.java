package com.femboyequipment.collection;

import com.femboyequipment.FemboyEquipment;
import io.netty.buffer.ByteBuf;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.minecraft.core.UUIDUtil;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.ComponentSerialization;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.Item;

/** Packets for the Cute Collection screen. */
public final class CollectionPayloads {
	private static final StreamCodec<RegistryFriendlyByteBuf, Item> ITEM = ByteBufCodecs.registry(Registries.ITEM);
	private static final StreamCodec<RegistryFriendlyByteBuf, Component> TEXT = ComponentSerialization.TRUSTED_STREAM_CODEC;

	private CollectionPayloads() {
	}

	private static <T extends CustomPacketPayload> CustomPacketPayload.Type<T> payloadType(String path) {
		return new CustomPacketPayload.Type<>(FemboyEquipment.id("collection/" + path));
	}

	// ------------------------------------------------------------ server -> client

	/** One collectible: an advancement shown in the collection grid. type: 0 task, 1 goal, 2 challenge. */
	public record EntryDef(Identifier id, Item icon, Component title, Component description, int type) {
		public static final StreamCodec<RegistryFriendlyByteBuf, EntryDef> CODEC = StreamCodec.composite(
				Identifier.STREAM_CODEC, EntryDef::id, ITEM, EntryDef::icon, TEXT, EntryDef::title, TEXT, EntryDef::description,
				ByteBufCodecs.VAR_INT, EntryDef::type, EntryDef::new);
	}

	/** Clears the client's collection before pages are (re)sent. */
	public record Reset(int pageCount) implements CustomPacketPayload {
		public static final Type<Reset> TYPE = CollectionPayloads.payloadType("reset");
		public static final StreamCodec<RegistryFriendlyByteBuf, Reset> CODEC = ByteBufCodecs.VAR_INT.map(Reset::new, Reset::pageCount).cast();

		@Override
		public Type<Reset> type() {
			return TYPE;
		}
	}

	/** A page (one advancement tab: the main mod's tabs and one per addon) and its progress. */
	public record Page(Identifier id, Component title, Item icon, List<EntryDef> entries, BitSet done) implements CustomPacketPayload {
		public static final Type<Page> TYPE = CollectionPayloads.payloadType("page");
		public static final StreamCodec<RegistryFriendlyByteBuf, Page> CODEC = StreamCodec.composite(
				Identifier.STREAM_CODEC, Page::id, TEXT, Page::title, ITEM, Page::icon,
				EntryDef.CODEC.apply(ByteBufCodecs.list()), Page::entries, bitSet(), Page::done, Page::new);

		@Override
		public Type<Page> type() {
			return TYPE;
		}
	}

	/** Fresh progress for one page (after a revoke etc.). */
	public record Progress(Identifier page, BitSet done) implements CustomPacketPayload {
		public static final Type<Progress> TYPE = CollectionPayloads.payloadType("progress");
		public static final StreamCodec<RegistryFriendlyByteBuf, Progress> CODEC = StreamCodec.composite(
				Identifier.STREAM_CODEC, Progress::page, bitSet(), Progress::done, Progress::new);

		@Override
		public Type<Progress> type() {
			return TYPE;
		}
	}

	public record EntryDone(Identifier page, int index) implements CustomPacketPayload {
		public static final Type<EntryDone> TYPE = CollectionPayloads.payloadType("entry_done");
		public static final StreamCodec<RegistryFriendlyByteBuf, EntryDone> CODEC = StreamCodec.composite(
				Identifier.STREAM_CODEC, EntryDone::page, ByteBufCodecs.VAR_INT, EntryDone::index, EntryDone::new);

		@Override
		public Type<EntryDone> type() {
			return TYPE;
		}
	}

	public record QuestView(String type, boolean weekly, int progress, int target, boolean claimed) {
		public static final StreamCodec<RegistryFriendlyByteBuf, QuestView> CODEC = StreamCodec.composite(
				ByteBufCodecs.STRING_UTF8, QuestView::type, ByteBufCodecs.BOOL, QuestView::weekly, ByteBufCodecs.VAR_INT,
				QuestView::progress, ByteBufCodecs.VAR_INT, QuestView::target, ByteBufCodecs.BOOL, QuestView::claimed, QuestView::new);
	}

	/** Points, rank and quests. */
	public record Status(int points, int totalPoints, int rank, boolean showTitle, List<QuestView> quests, long dailyResetMs,
			long weeklyResetMs) implements CustomPacketPayload {
		public static final Type<Status> TYPE = CollectionPayloads.payloadType("status");
		public static final StreamCodec<RegistryFriendlyByteBuf, Status> CODEC = StreamCodec.composite(
				ByteBufCodecs.VAR_INT, Status::points, ByteBufCodecs.VAR_INT, Status::totalPoints, ByteBufCodecs.VAR_INT, Status::rank,
				ByteBufCodecs.BOOL, Status::showTitle, QuestView.CODEC.apply(ByteBufCodecs.list()), Status::quests,
				ByteBufCodecs.VAR_LONG, Status::dailyResetMs, ByteBufCodecs.VAR_LONG, Status::weeklyResetMs, Status::new);

		@Override
		public Type<Status> type() {
			return TYPE;
		}
	}

	/** A cute toast. */
	public record Notify(Item icon, Component title, Component subtitle, int color) implements CustomPacketPayload {
		public static final Type<Notify> TYPE = CollectionPayloads.payloadType("notify");
		public static final StreamCodec<RegistryFriendlyByteBuf, Notify> CODEC = StreamCodec.composite(
				ITEM, Notify::icon, TEXT, Notify::title, TEXT, Notify::subtitle, ByteBufCodecs.INT, Notify::color, Notify::new);

		@Override
		public Type<Notify> type() {
			return TYPE;
		}
	}

	/** Rank titles of online players (only those who show theirs). */
	public record Titles(Map<UUID, Integer> ranks) implements CustomPacketPayload {
		public static final Type<Titles> TYPE = CollectionPayloads.payloadType("titles");
		public static final StreamCodec<RegistryFriendlyByteBuf, Titles> CODEC = ByteBufCodecs.<ByteBuf, UUID, Integer, Map<UUID, Integer>>map(
				HashMap::new, UUIDUtil.STREAM_CODEC, ByteBufCodecs.VAR_INT).map(Titles::new, Titles::ranks).cast();

		@Override
		public Type<Titles> type() {
			return TYPE;
		}
	}

	// ------------------------------------------------------------ client -> server

	/** Ask for fresh status (sent when the screen opens). */
	public record Request() implements CustomPacketPayload {
		public static final Type<Request> TYPE = CollectionPayloads.payloadType("request");
		public static final StreamCodec<RegistryFriendlyByteBuf, Request> CODEC = StreamCodec.unit(new Request());

		@Override
		public Type<Request> type() {
			return TYPE;
		}
	}

	public record Claim(boolean weekly, int index) implements CustomPacketPayload {
		public static final Type<Claim> TYPE = CollectionPayloads.payloadType("claim");
		public static final StreamCodec<RegistryFriendlyByteBuf, Claim> CODEC = StreamCodec.composite(
				ByteBufCodecs.BOOL, Claim::weekly, ByteBufCodecs.VAR_INT, Claim::index, Claim::new);

		@Override
		public Type<Claim> type() {
			return TYPE;
		}
	}

	public record ShowTitle(boolean show) implements CustomPacketPayload {
		public static final Type<ShowTitle> TYPE = CollectionPayloads.payloadType("show_title");
		public static final StreamCodec<RegistryFriendlyByteBuf, ShowTitle> CODEC = ByteBufCodecs.BOOL.map(ShowTitle::new, ShowTitle::show).cast();

		@Override
		public Type<ShowTitle> type() {
			return TYPE;
		}
	}

	private static StreamCodec<RegistryFriendlyByteBuf, BitSet> bitSet() {
		return StreamCodec.of((RegistryFriendlyByteBuf buf, BitSet bits) -> buf.writeBitSet(bits), buf -> buf.readBitSet());
	}

	public static void register() {
		PayloadTypeRegistry.playS2C().register(Reset.TYPE, Reset.CODEC);
		PayloadTypeRegistry.playS2C().register(Page.TYPE, Page.CODEC);
		PayloadTypeRegistry.playS2C().register(Progress.TYPE, Progress.CODEC);
		PayloadTypeRegistry.playS2C().register(EntryDone.TYPE, EntryDone.CODEC);
		PayloadTypeRegistry.playS2C().register(Status.TYPE, Status.CODEC);
		PayloadTypeRegistry.playS2C().register(Notify.TYPE, Notify.CODEC);
		PayloadTypeRegistry.playS2C().register(Titles.TYPE, Titles.CODEC);
		PayloadTypeRegistry.playC2S().register(Request.TYPE, Request.CODEC);
		PayloadTypeRegistry.playC2S().register(Claim.TYPE, Claim.CODEC);
		PayloadTypeRegistry.playC2S().register(ShowTitle.TYPE, ShowTitle.CODEC);
	}

	static List<EntryDef> list() {
		return new ArrayList<>();
	}
}
