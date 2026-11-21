package com.femboyequipment.item;

import com.femboyequipment.FemboyEquipment;
import java.util.List;
import java.util.function.Function;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.Unit;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.HoeItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ShovelItem;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.item.component.Consumables;
import net.minecraft.world.item.consume_effects.ApplyStatusEffectsConsumeEffect;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;

public final class ModItems {
	public static final ToolMaterial SPARKLY = new ToolMaterial(BlockTags.INCORRECT_FOR_DIAMOND_TOOL,
			1800, 10.0F, 3.5F, 22, ModArmorMaterials.CUTE_REPAIR_MATERIALS);

	public static final ToolMaterial ROSE_QUARTZ_TOOLS = new ToolMaterial(BlockTags.INCORRECT_FOR_DIAMOND_TOOL,
			1900, 8.5F, 3.5F, 18, ModArmorMaterials.ROSE_QUARTZ_REPAIR_MATERIALS);

	// Accessories (hold one in your offhand for a little buff)
	public static final Item PINK_RIBBON = register("pink_ribbon", Item::new, new Item.Properties().stacksTo(16));
	public static final Item PROGRAMMING_SOCKS = register("programming_socks", Item::new, new Item.Properties().stacksTo(1));
	public static final Item HAIR_CLIP = register("hair_clip", Item::new, new Item.Properties().stacksTo(16));
	public static final Item CHOKER = register("choker", Item::new, new Item.Properties().stacksTo(1));

	// Food
	public static final Item STRAWBERRY_MILK = register("strawberry_milk", Item::new, new Item.Properties()
			.stacksTo(16)
			.usingConvertsTo(Items.GLASS_BOTTLE)
			.food(new FoodProperties(4, 0.6F, true), Consumables.defaultDrink()
					.onConsume(new ApplyStatusEffectsConsumeEffect(List.of(
							new MobEffectInstance(MobEffects.SPEED, 600, 1),
							new MobEffectInstance(MobEffects.REGENERATION, 200, 0))))
					.build()));

	// Wearable outfit
	public static final Item CAT_EARS = register("cat_ears", Item::new,
			new Item.Properties().humanoidArmor(ModArmorMaterials.CAT_EARS, ArmorType.HELMET));
	public static final Item FEMBOY_HOODIE = register("femboy_hoodie", Item::new,
			new Item.Properties().humanoidArmor(ModArmorMaterials.FEMBOY_HOODIE, ArmorType.CHESTPLATE));
	public static final Item PLEATED_SKIRT = register("pleated_skirt", Item::new,
			new Item.Properties().humanoidArmor(ModArmorMaterials.PLEATED_SKIRT, ArmorType.LEGGINGS));
	public static final Item THIGH_HIGHS = register("thigh_highs", Item::new,
			new Item.Properties().humanoidArmor(ModArmorMaterials.THIGH_HIGHS, ArmorType.BOOTS)
					.rarity(Rarity.EPIC)
					.fireResistant()
					.component(DataComponents.UNBREAKABLE, Unit.INSTANCE)
					.component(DataComponents.ENCHANTMENT_GLINT_OVERRIDE, true));

	// Maid outfit
	public static final Item MAID_HEADBAND = armor("maid_headband", ModArmorMaterials.MAID_HEADBAND, ArmorType.HELMET);
	public static final Item MAID_DRESS = armor("maid_dress", ModArmorMaterials.MAID_DRESS, ArmorType.CHESTPLATE);
	public static final Item MAID_APRON = armor("maid_apron", ModArmorMaterials.MAID_APRON, ArmorType.LEGGINGS);
	public static final Item MARY_JANES = armor("mary_janes", ModArmorMaterials.MARY_JANES, ArmorType.BOOTS);

	// Bunny outfit
	public static final Item BUNNY_EARS = armor("bunny_ears", ModArmorMaterials.BUNNY_EARS, ArmorType.HELMET);
	public static final Item BUNNY_HOODIE = armor("bunny_hoodie", ModArmorMaterials.BUNNY_HOODIE, ArmorType.CHESTPLATE);
	public static final Item FLUFFY_SLIPPERS = armor("fluffy_slippers", ModArmorMaterials.FLUFFY_SLIPPERS, ArmorType.BOOTS);

	// Tools & weapons
	public static final Item SPARKLY_SWORD = register("sparkly_sword", Item::new,
			new Item.Properties().sword(SPARKLY, 3.0F, -2.4F).rarity(Rarity.RARE));
	public static final Item SPARKLY_PICKAXE = register("sparkly_pickaxe", Item::new,
			new Item.Properties().pickaxe(SPARKLY, 1.0F, -2.8F).rarity(Rarity.RARE));

	public static final Item SPARKLY_AXE = register("sparkly_axe",
			p -> new AxeItem(SPARKLY, 5.0F, -3.0F, p), new Item.Properties().rarity(Rarity.RARE));
	public static final Item SPARKLY_SHOVEL = register("sparkly_shovel",
			p -> new ShovelItem(SPARKLY, 1.5F, -3.0F, p), new Item.Properties().rarity(Rarity.RARE));
	public static final Item SPARKLY_HOE = register("sparkly_hoe",
			p -> new HoeItem(SPARKLY, -3.0F, 0.0F, p), new Item.Properties().rarity(Rarity.RARE));

	// Rose Quartz: material, armor, tools and a spear
	public static final Item ROSE_QUARTZ = register("rose_quartz", Item::new, new Item.Properties());
	public static final Item ROSE_QUARTZ_HELMET = armor("rose_quartz_helmet", ModArmorMaterials.ROSE_QUARTZ, ArmorType.HELMET);
	public static final Item ROSE_QUARTZ_CHESTPLATE = armor("rose_quartz_chestplate", ModArmorMaterials.ROSE_QUARTZ, ArmorType.CHESTPLATE);
	public static final Item ROSE_QUARTZ_LEGGINGS = armor("rose_quartz_leggings", ModArmorMaterials.ROSE_QUARTZ, ArmorType.LEGGINGS);
	public static final Item ROSE_QUARTZ_BOOTS = armor("rose_quartz_boots", ModArmorMaterials.ROSE_QUARTZ, ArmorType.BOOTS);
	public static final Item ROSE_QUARTZ_SWORD = register("rose_quartz_sword", Item::new,
			new Item.Properties().sword(ROSE_QUARTZ_TOOLS, 3.0F, -2.4F));
	public static final Item ROSE_QUARTZ_PICKAXE = register("rose_quartz_pickaxe", Item::new,
			new Item.Properties().pickaxe(ROSE_QUARTZ_TOOLS, 1.0F, -2.8F));
	public static final Item ROSE_QUARTZ_AXE = register("rose_quartz_axe",
			p -> new AxeItem(ROSE_QUARTZ_TOOLS, 5.0F, -3.0F, p), new Item.Properties());
	public static final Item ROSE_QUARTZ_SHOVEL = register("rose_quartz_shovel",
			p -> new ShovelItem(ROSE_QUARTZ_TOOLS, 1.5F, -3.0F, p), new Item.Properties());
	public static final Item ROSE_QUARTZ_HOE = register("rose_quartz_hoe",
			p -> new HoeItem(ROSE_QUARTZ_TOOLS, -3.0F, 0.0F, p), new Item.Properties());
	public static final Item ROSE_QUARTZ_SPEAR = register("rose_quartz_spear", Item::new,
			new Item.Properties().spear(ROSE_QUARTZ_TOOLS, 1.05F, 1.075F, 0.5F, 3.0F, 7.5F, 6.5F, 5.1F, 10.0F, 4.6F));

	// Joke weapons that send things flying
	public static final Item FIH_SLAPPER = register("fih_slapper",
			p -> new KnockbackWeaponItem(1.5F, SoundEvents.COD_FLOP, p),
			new Item.Properties().sword(ToolMaterial.IRON, 2.0F, -2.2F).rarity(Rarity.UNCOMMON));
	public static final Item BLAHAJ_BAT = register("blahaj_bat",
			p -> new KnockbackWeaponItem(3.0F, SoundEvents.WOOL_HIT, p),
			new Item.Properties().sword(ToolMaterial.DIAMOND, 4.0F, -3.0F).rarity(Rarity.RARE));

	// Gacha capsules
	public static final Item BLAHAJ_CAPSULE = register("blahaj_capsule",
			p -> new CapsuleItem(com.femboyequipment.block.Blahaj::items, p), new Item.Properties().stacksTo(64));
	public static final Item FIH_CAPSULE = register("fih_capsule",
			p -> new CapsuleItem(com.femboyequipment.block.Fih::items, p), new Item.Properties().stacksTo(64));

	private ModItems() {
	}

	private static Item armor(String name, ArmorMaterial material, ArmorType type) {
		return register(name, Item::new, new Item.Properties().humanoidArmor(material, type));
	}

	public static Item register(String name, Function<Item.Properties, Item> factory, Item.Properties properties) {
		ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, FemboyEquipment.id(name));
		Item item = factory.apply(properties.setId(key));
		return Registry.register(BuiltInRegistries.ITEM, key, item);
	}

	public static void initialize() {
		// Loading this class registers the items above.
	}
}
