package com.femboyequipment.api;

import com.femboyequipment.item.KnockbackWeaponItem;
import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.function.Supplier;
import net.fabricmc.fabric.api.biome.v1.BiomeModifications;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectors;
import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.minecraft.core.Holder;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.tags.TagKey;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.HoeItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.ShovelItem;
import net.minecraft.world.item.ToolMaterial;
import net.minecraft.world.item.component.Consumable;
import net.minecraft.world.item.component.Consumables;
import net.minecraft.world.item.consume_effects.ApplyStatusEffectsConsumeEffect;
import net.minecraft.world.item.equipment.ArmorMaterial;
import net.minecraft.world.item.equipment.ArmorType;
import net.minecraft.world.item.equipment.EquipmentAssets;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.WallBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.levelgen.GenerationStep;
import net.minecraft.world.level.material.MapColor;

/**
 * Small helpers for content addons: register items, blocks, tools, armor, food and charms in one line each,
 * and collect everything into the addon's own creative tab. The 30 official addons are built with this.
 *
 * <pre>{@code
 * AddonKit kit = new AddonKit("myaddon");
 * Item gem = kit.item("sparkle_gem");
 * Block bricks = kit.cube("sparkle_bricks", MapColor.COLOR_PINK, 2.0F, SoundType.STONE, 0, true);
 * kit.shapes("sparkle_brick", bricks);   // sparkle_brick_stairs, _slab, _wall
 * kit.creativeTab("main", () -> new ItemStack(gem));
 * }</pre>
 * Everything a kit registers is added to its tab, in registration order. Models, textures, recipes and loot
 * tables are normal resources in your mod.
 */
public final class AddonKit {
	private final String modId;
	private final List<ItemLike> entries = new ArrayList<>();

	public AddonKit(String modId) {
		this.modId = modId;
	}

	public Identifier id(String path) {
		return Identifier.fromNamespaceAndPath(this.modId, path);
	}

	/** Everything registered so far, in order. */
	public List<ItemLike> entries() {
		return Collections.unmodifiableList(this.entries);
	}

	public TagKey<Item> itemTag(String path) {
		return TagKey.create(Registries.ITEM, id(path));
	}

	// ------------------------------------------------------------ items

	public <T extends Item> T item(String name, Function<Item.Properties, T> factory, Item.Properties properties) {
		ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, id(name));
		T item = Registry.register(BuiltInRegistries.ITEM, key, factory.apply(properties.setId(key)));
		this.entries.add(item);
		return item;
	}

	public Item item(String name, Item.Properties properties) {
		return item(name, Item::new, properties);
	}

	public Item item(String name) {
		return item(name, new Item.Properties());
	}

	/** Food (or a drink) that applies the given effects when eaten. */
	public Item food(String name, int nutrition, float saturation, boolean drink, MobEffectInstance... effects) {
		Consumable.Builder consumable = drink ? Consumables.defaultDrink() : Consumables.defaultFood();
		if (effects.length > 0) {
			consumable.onConsume(new ApplyStatusEffectsConsumeEffect(List.of(effects)));
		}
		Item.Properties properties = new Item.Properties()
				.food(new FoodProperties(nutrition, saturation, effects.length > 0), consumable.build());
		if (drink) {
			properties.stacksTo(16).usingConvertsTo(Items.GLASS_BOTTLE);
		}
		return item(name, properties);
	}

	/** An accessory: effects while held in the offhand or worn in a Trinkets slot (tag it for the slot you want). */
	public Item charm(String name, Rarity rarity, OutfitEffect... effects) {
		Item item = item(name, new Item.Properties().stacksTo(1).rarity(rarity));
		FemboyEquipmentApi.addAccessoryEffect(item, effects);
		return item;
	}

	// ------------------------------------------------------------ tools & weapons

	public static ToolMaterial toolMaterial(TagKey<net.minecraft.world.level.block.Block> incorrectForDrops,
			int durability, float speed, float attackBonus, int enchantability, TagKey<Item> repairItems) {
		return new ToolMaterial(incorrectForDrops, durability, speed, attackBonus, enchantability, repairItems);
	}

	public Item sword(String name, ToolMaterial material) {
		return item(name, new Item.Properties().sword(material, 3.0F, -2.4F));
	}

	public Item pickaxe(String name, ToolMaterial material) {
		return item(name, new Item.Properties().pickaxe(material, 1.0F, -2.8F));
	}

	public Item axe(String name, ToolMaterial material) {
		return item(name, p -> new AxeItem(material, 5.0F, -3.0F, p), new Item.Properties());
	}

	public Item shovel(String name, ToolMaterial material) {
		return item(name, p -> new ShovelItem(material, 1.5F, -3.0F, p), new Item.Properties());
	}

	public Item hoe(String name, ToolMaterial material) {
		return item(name, p -> new HoeItem(material, -3.0F, 0.0F, p), new Item.Properties());
	}

	public Item spear(String name, ToolMaterial material) {
		return item(name, new Item.Properties().spear(material, 1.05F, 1.075F, 0.5F, 3.0F, 7.5F, 6.5F, 5.1F, 10.0F, 4.6F));
	}

	/** A melee weapon that sends whatever it hits flying, playing {@code sound}. */
	public Item knockbackWeapon(String name, ToolMaterial material, float damage, float speed, float knockback,
			SoundEvent sound, Rarity rarity) {
		return item(name, p -> new KnockbackWeaponItem(knockback, sound, p),
				new Item.Properties().sword(material, damage, speed).rarity(rarity));
	}

	// ------------------------------------------------------------ armor

	/** An armor material whose look is {@code assets/<modid>/equipment/<asset>.json}. */
	public ArmorMaterial armorMaterial(String asset, int durability, int boots, int leggings, int chestplate,
			int helmet, int enchantability, Holder<SoundEvent> equipSound, float toughness, float knockbackResistance,
			TagKey<Item> repairItems) {
		Map<ArmorType, Integer> defense = new EnumMap<>(ArmorType.class);
		defense.put(ArmorType.BOOTS, boots);
		defense.put(ArmorType.LEGGINGS, leggings);
		defense.put(ArmorType.CHESTPLATE, chestplate);
		defense.put(ArmorType.HELMET, helmet);
		defense.put(ArmorType.BODY, chestplate);
		return new ArmorMaterial(durability, defense, enchantability, equipSound, toughness, knockbackResistance,
				repairItems, ResourceKey.create(EquipmentAssets.ROOT_ID, id(asset)));
	}

	public Item armor(String name, ArmorMaterial material, ArmorType type) {
		return item(name, new Item.Properties().humanoidArmor(material, type));
	}

	// ------------------------------------------------------------ blocks

	/** Registers a block and its block item. */
	public Block block(String name, Function<BlockBehaviour.Properties, Block> factory,
			BlockBehaviour.Properties properties) {
		ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, id(name));
		Block block = Registry.register(BuiltInRegistries.BLOCK, key, factory.apply(properties.setId(key)));
		item(name, p -> new BlockItem(block, p), new Item.Properties().useBlockDescriptionPrefix());
		return block;
	}

	/** A plain full block. {@code needsTool}: only drops when mined with the right tool. */
	public Block cube(String name, MapColor color, float strength, SoundType sound, int light, boolean needsTool) {
		BlockBehaviour.Properties properties = BlockBehaviour.Properties.of().mapColor(color)
				.strength(strength, Math.max(strength, 6.0F)).sound(sound).lightLevel(state -> light);
		if (needsTool) {
			properties.requiresCorrectToolForDrops();
		}
		return block(name, Block::new, properties);
	}

	/** Registers {@code <prefix>_stairs}, {@code <prefix>_slab} and {@code <prefix>_wall} copying {@code base}. */
	public List<Block> shapes(String prefix, Block base) {
		return List.of(
				block(prefix + "_stairs", p -> new StairBlock(base.defaultBlockState(), p),
						BlockBehaviour.Properties.ofFullCopy(base)),
				block(prefix + "_slab", SlabBlock::new, BlockBehaviour.Properties.ofFullCopy(base)),
				block(prefix + "_wall", WallBlock::new, BlockBehaviour.Properties.ofFullCopy(base).forceSolidOn()));
	}

	/** A Blåhaj plushie (see {@link FemboyEquipmentApi#registerBlahaj}); also added to this kit's tab. */
	public Block blahaj(String name, int light) {
		Block block = FemboyEquipmentApi.registerBlahaj(id(name), light);
		this.entries.add(block);
		return block;
	}

	/** A fih plushie (see {@link FemboyEquipmentApi#registerFih}); also added to this kit's tab. */
	public Block fih(String name, int light) {
		Block block = FemboyEquipmentApi.registerFih(id(name), light);
		this.entries.add(block);
		return block;
	}

	// ------------------------------------------------------------ world & tabs

	/** Adds {@code data/<modid>/worldgen/placed_feature/<placedFeature>.json} to every Overworld biome. */
	public void overworldOre(String placedFeature) {
		BiomeModifications.addFeature(BiomeSelectors.foundInOverworld(), GenerationStep.Decoration.UNDERGROUND_ORES,
				ResourceKey.create(Registries.PLACED_FEATURE, id(placedFeature)));
	}

	/**
	 * Registers a creative tab titled {@code itemGroup.<modid>.<name>} with everything this kit registered
	 * (including things registered after this call).
	 */
	public ResourceKey<CreativeModeTab> creativeTab(String name, Supplier<ItemStack> icon) {
		ResourceKey<CreativeModeTab> key = ResourceKey.create(Registries.CREATIVE_MODE_TAB, id(name));
		CreativeModeTab tab = FabricItemGroup.builder()
				.icon(icon)
				.title(Component.translatable("itemGroup." + this.modId + "." + name))
				.displayItems((parameters, output) -> this.entries.forEach(output::accept))
				.build();
		Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, key, tab);
		return key;
	}
}
