package com.femboyequipment.entity;

import com.femboyequipment.block.Blahaj;
import com.femboyequipment.item.ModItems;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.stats.Stats;
import net.minecraft.util.RandomSource;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ExperienceOrb;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.AvoidEntityGoal;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.InteractGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.LookAtTradingPlayerGoal;
import net.minecraft.world.entity.ai.goal.PanicGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.TradeWithPlayerGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.monster.zombie.Zombie;
import net.minecraft.world.entity.npc.villager.AbstractVillager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.trading.ItemCost;
import net.minecraft.world.item.trading.MerchantOffer;
import net.minecraft.world.item.trading.MerchantOffers;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import org.jspecify.annotations.Nullable;

/** A cute trader who sells outfit pieces, Blåhaj and snacks. Lives in cute houses. */
public class FemboyVillager extends AbstractVillager {
	public FemboyVillager(EntityType<? extends FemboyVillager> type, Level level) {
		super(type, level);
	}

	public static AttributeSupplier.Builder createAttributes() {
		return Mob.createMobAttributes().add(Attributes.MOVEMENT_SPEED, 0.5).add(Attributes.MAX_HEALTH, 20.0);
	}

	@Override
	protected void registerGoals() {
		this.goalSelector.addGoal(0, new FloatGoal(this));
		this.goalSelector.addGoal(1, new TradeWithPlayerGoal(this));
		this.goalSelector.addGoal(1, new AvoidEntityGoal<>(this, Zombie.class, 8.0F, 0.5, 0.5));
		this.goalSelector.addGoal(1, new PanicGoal(this, 0.5));
		this.goalSelector.addGoal(1, new LookAtTradingPlayerGoal(this));
		this.goalSelector.addGoal(8, new WaterAvoidingRandomStrollGoal(this, 0.35));
		this.goalSelector.addGoal(9, new InteractGoal(this, Player.class, 3.0F, 1.0F));
		this.goalSelector.addGoal(10, new LookAtPlayerGoal(this, Mob.class, 8.0F));
		this.goalSelector.addGoal(11, new RandomLookAroundGoal(this));
	}

	@Override
	public SpawnGroupData finalizeSpawn(ServerLevelAccessor level, DifficultyInstance difficulty, EntitySpawnReason reason,
			@Nullable SpawnGroupData data) {
		this.setPersistenceRequired();
		this.dressUp(level.getRandom());
		return super.finalizeSpawn(level, difficulty, reason, data);
	}

	/** Puts on one of the three outfits. They're just for show, so they never drop. */
	private void dressUp(RandomSource random) {
		Item[] outfit = switch (random.nextInt(3)) {
			case 0 -> new Item[] {ModItems.CAT_EARS, ModItems.FEMBOY_HOODIE, ModItems.PLEATED_SKIRT, ModItems.PROGRAMMING_SOCKS};
			case 1 -> new Item[] {ModItems.MAID_HEADBAND, ModItems.MAID_DRESS, ModItems.MAID_APRON, ModItems.MARY_JANES};
			default -> new Item[] {ModItems.BUNNY_EARS, ModItems.BUNNY_HOODIE, null, ModItems.FLUFFY_SLIPPERS};
		};
		EquipmentSlot[] slots = {EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET};
		for (int i = 0; i < slots.length; i++) {
			// programming socks aren't wearable, so the cat outfit keeps bare feet
			if (outfit[i] != null && outfit[i] != ModItems.PROGRAMMING_SOCKS) {
				this.setItemSlot(slots[i], new ItemStack(outfit[i]));
				this.setDropChance(slots[i], 0.0F);
			}
		}
		// hugging a shark, of course
		List<Item> sharks = Blahaj.items();
		this.setItemSlot(EquipmentSlot.OFFHAND, new ItemStack(sharks.get(random.nextInt(16))));
		this.setDropChance(EquipmentSlot.OFFHAND, 0.0F);
	}

	@Override
	public boolean removeWhenFarAway(double distance) {
		return false;
	}

	@Override
	public InteractionResult mobInteract(Player player, InteractionHand hand) {
		if (this.isAlive() && !this.isTrading() && !this.isBaby()) {
			if (hand == InteractionHand.MAIN_HAND) {
				player.awardStat(Stats.TALKED_TO_VILLAGER);
			}
			if (!this.level().isClientSide()) {
				if (this.getOffers().isEmpty()) {
					return InteractionResult.CONSUME;
				}
				this.setTradingPlayer(player);
				this.openTradingScreen(player, this.getDisplayName(), 1);
			}
			return InteractionResult.SUCCESS;
		}
		return super.mobInteract(player, hand);
	}

	@Override
	protected void updateTrades(ServerLevel level) {
		MerchantOffers offers = this.getOffers();
		RandomSource random = this.random;

		// Always in stock
		offers.add(sell(1, new ItemStack(ModItems.PINK_RIBBON, 4), 16));
		offers.add(sell(1, new ItemStack(ModItems.STRAWBERRY_MILK, 2), 12));
		offers.add(new MerchantOffer(new ItemCost(Items.PINK_WOOL, 8), new ItemStack(Items.EMERALD), 16, 2, 0.05F));
		offers.add(sell(3, new ItemStack(ModItems.BLAHAJ_CAPSULE), 12));
		offers.add(sell(3, new ItemStack(ModItems.FIH_CAPSULE), 12));

		// A few random goodies
		List<MerchantOffer> extras = new ArrayList<>(List.of(
				sell(3, new ItemStack(ModItems.HAIR_CLIP, 2), 8),
				sell(4, new ItemStack(ModItems.CHOKER), 6),
				sell(6, new ItemStack(ModItems.PROGRAMMING_SOCKS), 4),
				sell(8, new ItemStack(Blahaj.items().get(random.nextInt(26))), 3),
				sell(12, new ItemStack(randomOutfitPiece(random)), 3),
				sell(12, new ItemStack(randomOutfitPiece(random)), 3),
				sell(10, new ItemStack(ModItems.SPARKLY_SWORD), 2)));
		java.util.Collections.shuffle(extras, new java.util.Random(random.nextLong()));
		offers.addAll(extras.subList(0, 4));

		// Very rarely: the legendary thigh highs
		if (random.nextInt(5) == 0) {
			offers.add(new MerchantOffer(new ItemCost(Items.EMERALD, 64), java.util.Optional.of(new ItemCost(Items.DIAMOND, 8)),
					new ItemStack(ModItems.THIGH_HIGHS), 1, 30, 0.0F));
		}
	}

	private static MerchantOffer sell(int emeralds, ItemStack result, int maxUses) {
		return new MerchantOffer(new ItemCost(Items.EMERALD, emeralds), result, maxUses, 5, 0.05F);
	}

	private static Item randomOutfitPiece(RandomSource random) {
		Item[] pieces = {ModItems.CAT_EARS, ModItems.FEMBOY_HOODIE, ModItems.PLEATED_SKIRT,
				ModItems.MAID_HEADBAND, ModItems.MAID_DRESS, ModItems.MAID_APRON, ModItems.MARY_JANES,
				ModItems.BUNNY_EARS, ModItems.BUNNY_HOODIE, ModItems.FLUFFY_SLIPPERS};
		return pieces[random.nextInt(pieces.length)];
	}

	@Override
	protected void rewardTradeXp(MerchantOffer offer) {
		if (offer.shouldRewardExp()) {
			int xp = 3 + this.random.nextInt(4);
			this.level().addFreshEntity(new ExperienceOrb(this.level(), this.getX(), this.getY() + 0.5, this.getZ(), xp));
		}
	}

	@Override
	public @Nullable AgeableMob getBreedOffspring(ServerLevel level, AgeableMob partner) {
		return null;
	}

	@Override
	public boolean showProgressBar() {
		return false;
	}

	@Override
	protected SoundEvent getAmbientSound() {
		return this.isTrading() ? SoundEvents.WANDERING_TRADER_TRADE : SoundEvents.WANDERING_TRADER_AMBIENT;
	}

	@Override
	protected SoundEvent getHurtSound(DamageSource source) {
		return SoundEvents.WANDERING_TRADER_HURT;
	}

	@Override
	protected SoundEvent getDeathSound() {
		return SoundEvents.WANDERING_TRADER_DEATH;
	}

	@Override
	protected SoundEvent getTradeUpdatedSound(boolean accepted) {
		return accepted ? SoundEvents.WANDERING_TRADER_YES : SoundEvents.WANDERING_TRADER_NO;
	}

	@Override
	public SoundEvent getNotifyTradeSound() {
		return SoundEvents.WANDERING_TRADER_YES;
	}

	@Override
	public float getVoicePitch() {
		return super.getVoicePitch() * 1.25F; // cuter
	}
}
