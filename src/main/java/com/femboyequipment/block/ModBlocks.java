package com.femboyequipment.block;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.item.ModItems;
import java.util.function.Function;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.FlowerBlock;
import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.WallBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;

public final class ModBlocks {
	public static final Block PASTEL_PINK_BRICKS = register("pastel_pink_bricks", Block::new,
			BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PINK).strength(2.0F, 6.0F)
					.requiresCorrectToolForDrops().sound(SoundType.MUD_BRICKS));
	public static final Block RIBBON_BLOCK = register("ribbon_block", Block::new,
			BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PINK).strength(0.8F).sound(SoundType.WOOL));

	public static final Block PASTEL_BLOOM = register("pastel_bloom",
			props -> new FlowerBlock(MobEffects.REGENERATION, 7.0F, props),
			BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PINK).noCollision().instabreak()
					.sound(SoundType.GRASS).offsetType(BlockBehaviour.OffsetType.XZ).pushReaction(PushReaction.DESTROY));

	public static final Block PASTEL_BLUE_BRICKS = bricks("pastel_blue_bricks", MapColor.COLOR_LIGHT_BLUE);
	public static final Block PASTEL_LAVENDER_BRICKS = bricks("pastel_lavender_bricks", MapColor.COLOR_PURPLE);
	public static final Block PASTEL_MINT_BRICKS = bricks("pastel_mint_bricks", MapColor.COLOR_LIGHT_GREEN);
	public static final Block PASTEL_YELLOW_BRICKS = bricks("pastel_yellow_bricks", MapColor.COLOR_YELLOW);
	public static final Block ROSE_QUARTZ_BLOCK = register("rose_quartz_block", Block::new,
			BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PINK).strength(3.0F, 6.0F)
					.requiresCorrectToolForDrops().sound(SoundType.AMETHYST));
	public static final Block ROSE_QUARTZ_BRICKS = register("rose_quartz_bricks", Block::new,
			BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PINK).strength(3.0F, 6.0F)
					.requiresCorrectToolForDrops().sound(SoundType.AMETHYST));

	/** Every brick-ish block gets stairs, a slab and a wall. Names: <base minus "s">_stairs etc. */
	public static final java.util.List<Block> BRICK_BASES = java.util.List.of(PASTEL_PINK_BRICKS, PASTEL_BLUE_BRICKS,
			PASTEL_LAVENDER_BRICKS, PASTEL_MINT_BRICKS, PASTEL_YELLOW_BRICKS, ROSE_QUARTZ_BRICKS);
	public static final java.util.List<Block> BRICK_SHAPES = new java.util.ArrayList<>();

	static {
		String[] names = {"pastel_pink_brick", "pastel_blue_brick", "pastel_lavender_brick", "pastel_mint_brick",
				"pastel_yellow_brick", "rose_quartz_brick"};
		for (int i = 0; i < names.length; i++) {
			Block base = BRICK_BASES.get(i);
			BRICK_SHAPES.add(register(names[i] + "_stairs", p -> new StairBlock(base.defaultBlockState(), p),
					BlockBehaviour.Properties.ofFullCopy(base)));
			BRICK_SHAPES.add(register(names[i] + "_slab", SlabBlock::new, BlockBehaviour.Properties.ofFullCopy(base)));
			BRICK_SHAPES.add(register(names[i] + "_wall", WallBlock::new,
					BlockBehaviour.Properties.ofFullCopy(base).forceSolidOn()));
		}
	}

	private static Block bricks(String name, MapColor color) {
		return register(name, Block::new, BlockBehaviour.Properties.of().mapColor(color).strength(2.0F, 6.0F)
				.requiresCorrectToolForDrops().sound(SoundType.MUD_BRICKS));
	}

	private ModBlocks() {
	}

	private static Block register(String name, Function<BlockBehaviour.Properties, Block> factory,
			BlockBehaviour.Properties properties) {
		ResourceKey<Block> blockKey = ResourceKey.create(Registries.BLOCK, FemboyEquipment.id(name));
		Block block = Registry.register(BuiltInRegistries.BLOCK, blockKey, factory.apply(properties.setId(blockKey)));
		ModItems.register(name, props -> new BlockItem(block, props), new Item.Properties().useBlockDescriptionPrefix());
		return block;
	}

	public static void initialize() {
		// Loading this class registers the blocks above.
	}
}
