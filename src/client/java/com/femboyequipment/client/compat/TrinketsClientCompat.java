package com.femboyequipment.client.compat;

import com.femboyequipment.block.Blahaj;
import com.mojang.blaze3d.vertex.PoseStack;
import dev.emi.trinkets.api.client.TrinketRenderer;
import dev.emi.trinkets.api.client.TrinketRendererRegistry;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.renderer.entity.state.HumanoidRenderState;
import net.minecraft.client.renderer.item.ItemStackRenderState;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemDisplayContext;
import org.joml.Quaternionf;

/** Draws a Blåhaj worn in the Trinkets back slot, riding on the player's back. Only loaded when Trinkets is installed. */
public final class TrinketsClientCompat {
	private static final float INV_SQRT2 = (float) (1.0 / Math.sqrt(2.0));

	private TrinketsClientCompat() {
	}

	public static void register() {
		TrinketRenderer backShark = (stack, slot, model, poseStack, collector, light, state, limbAngle, limbDistance) -> {
			if (!(model instanceof HumanoidModel<?> humanoid) || !(state instanceof HumanoidRenderState humanoidState)) {
				return;
			}
			if (!slot.inventory().getSlotType().getName().equals("back")) {
				return; // only draw it when it's in the back slot
			}
			poseStack.pushPose();
			// Trinkets puts us at the front of the chest (entity model space: +y is down, +z is towards the back).
			TrinketRenderer.translateToChest(poseStack, humanoid, humanoidState);
			// Block-model shark: head towards -z, fin up (+y). On the back we want head up (-y),
			// fin pointing away from the player (+z) and belly against the back. That's a 180° turn
			// around the (0, 1, 1) axis. The belly sits 0.25 blocks below the rotated origin, so push
			// the origin that far behind the back surface (0.285 behind the chest front).
			poseStack.translate(0.0F, 0.0F, 0.285F + 0.25F);
			poseStack.mulPose(new Quaternionf().rotationAxis((float) Math.PI, 0.0F, INV_SQRT2, INV_SQRT2));
			poseStack.scale(0.5F, 0.5F, 0.5F);
			ItemStackRenderState item = new ItemStackRenderState();
			Minecraft.getInstance().getItemModelResolver().updateForTopItem(item, stack, ItemDisplayContext.NONE, null, null, 0);
			item.submit(poseStack, collector, light, OverlayTexture.NO_OVERLAY, 0);
			poseStack.popPose();
		};
		for (Item shark : Blahaj.items()) {
			TrinketRendererRegistry.registerRenderer(shark, backShark);
		}
	}
}
