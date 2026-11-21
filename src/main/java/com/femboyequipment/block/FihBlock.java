package com.femboyequipment.block;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/** fih. (a fish standing in a pair of sneakers) */
public class FihBlock extends BlahajBlock {
	public static final MapCodec<FihBlock> CODEC = simpleCodec(FihBlock::new);
	private static final VoxelShape SHAPE = Block.box(3.0, 0.0, 1.0, 13.0, 12.0, 15.0);

	public FihBlock(Properties properties) {
		super(properties);
	}

	@Override
	protected MapCodec<? extends HorizontalDirectionalBlock> codec() {
		return CODEC;
	}

	@Override
	protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
		return SHAPE;
	}
}
