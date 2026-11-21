package com.femboyequipment.item;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.api.FemboyEquipmentApi;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.tags.TagKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/**
 * A gacha capsule: right-click to pop out a random prize. The prize pool is the capsule's plushies,
 * plus anything addons add with {@code FemboyEquipmentApi.addCapsulePrize}, plus every item in the
 * {@code femboyequipment:blahaj_capsule_prizes} / {@code femboyequipment:fih_capsule_prizes} tags (datapacks).
 */
public class CapsuleItem extends Item {
	private static final Map<FemboyEquipmentApi.Capsule, List<Item>> EXTRA = new EnumMap<>(FemboyEquipmentApi.Capsule.class);

	private final FemboyEquipmentApi.Capsule kind;
	private final Supplier<List<Item>> pool;
	private final TagKey<Item> prizeTag;

	public CapsuleItem(FemboyEquipmentApi.Capsule kind, Supplier<List<Item>> pool, Properties properties) {
		super(properties);
		this.kind = kind;
		this.pool = pool;
		this.prizeTag = TagKey.create(Registries.ITEM,
				FemboyEquipment.id(kind == FemboyEquipmentApi.Capsule.BLAHAJ ? "blahaj_capsule_prizes" : "fih_capsule_prizes"));
	}

	public static synchronized void addExtraPrize(FemboyEquipmentApi.Capsule kind, Item item) {
		EXTRA.computeIfAbsent(kind, k -> new ArrayList<>()).add(item);
	}

	private List<Item> prizes() {
		List<Item> all = new ArrayList<>(this.pool.get());
		synchronized (CapsuleItem.class) {
			all.addAll(EXTRA.getOrDefault(this.kind, List.of()));
		}
		for (Holder<Item> holder : BuiltInRegistries.ITEM.getTagOrEmpty(this.prizeTag)) {
			all.add(holder.value());
		}
		return all;
	}

	@Override
	public InteractionResult use(Level level, Player player, InteractionHand hand) {
		ItemStack capsule = player.getItemInHand(hand);
		if (!level.isClientSide()) {
			List<Item> prizes = this.prizes();
			ItemStack prize = new ItemStack(prizes.get(level.getRandom().nextInt(prizes.size())));
			player.displayClientMessage(Component.translatable("message.femboyequipment.capsule", prize.getHoverName()), true);
			if (!player.getInventory().add(prize)) {
				player.drop(prize, false);
			}
			level.playSound(null, player.blockPosition(), SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.PLAYERS, 1.0F, 1.4F);
			level.playSound(null, player.blockPosition(), SoundEvents.BUNDLE_DROP_CONTENTS, SoundSource.PLAYERS, 0.8F, 1.2F);
		}
		capsule.consume(1, player);
		return InteractionResult.SUCCESS;
	}
}
