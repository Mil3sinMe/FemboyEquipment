package com.femboyequipment.client.model;

import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.renderer.entity.state.HumanoidRenderState;
import net.minecraft.util.Mth;

/**
 * A player-shaped model whose only cubes are the accessory (ears, tail, skirt).
 * It copies the player's pose, so the accessory follows the head and body.
 */
public class AccessoryModel extends HumanoidModel<HumanoidRenderState> {
	private final ModelPart tail;

	public AccessoryModel(ModelPart root) {
		super(root);
		this.tail = this.body.hasChild(AccessoryModels.TAIL) ? this.body.getChild(AccessoryModels.TAIL) : null;
	}

	@Override
	public void setupAnim(HumanoidRenderState state) {
		super.setupAnim(state);
		if (this.tail != null) {
			// Lazy swish, faster while walking.
			float swish = Mth.sin(state.ageInTicks * 0.08F) * 0.25F + Mth.sin(state.walkAnimationPos * 0.6F) * 0.3F * state.walkAnimationSpeed;
			this.tail.yRot = swish;
			if (state.isCrouching) {
				this.tail.xRot += 0.4F;
			}
		}
	}
}
