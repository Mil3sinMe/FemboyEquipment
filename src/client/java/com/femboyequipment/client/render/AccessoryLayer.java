package com.femboyequipment.client.render;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.client.model.AccessoryModel;
import com.femboyequipment.client.model.AccessoryModels;
import com.femboyequipment.item.ModItems;
import com.femboyequipment.item.OutfitColors;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.model.geom.EntityModelSet;
import net.minecraft.client.model.player.PlayerModel;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.entity.state.AvatarRenderState;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.Identifier;
import net.minecraft.util.ARGB;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.DyedItemColor;

/** Draws 3D ears, tails and skirts on players wearing the matching outfit pieces. */
public class AccessoryLayer extends RenderLayer<AvatarRenderState, PlayerModel> {
	private final AccessoryModel catEars;
	private final AccessoryModel catTail;
	private final AccessoryModel bunnyEars;
	private final AccessoryModel bunnyTail;
	private final AccessoryModel skirt;

	public AccessoryLayer(RenderLayerParent<AvatarRenderState, PlayerModel> parent, EntityModelSet models) {
		super(parent);
		this.catEars = new AccessoryModel(models.bakeLayer(AccessoryModels.CAT_EARS));
		this.catTail = new AccessoryModel(models.bakeLayer(AccessoryModels.CAT_TAIL));
		this.bunnyEars = new AccessoryModel(models.bakeLayer(AccessoryModels.BUNNY_EARS));
		this.bunnyTail = new AccessoryModel(models.bakeLayer(AccessoryModels.BUNNY_TAIL));
		this.skirt = new AccessoryModel(models.bakeLayer(AccessoryModels.SKIRT));
	}

	@Override
	public void submit(PoseStack poseStack, SubmitNodeCollector collector, int light, AvatarRenderState state, float yRot, float xRot) {
		if (state.isInvisible) {
			return;
		}

		ItemStack head = state.headEquipment;
		if (head.is(ModItems.CAT_EARS)) {
			int color = color(head, OutfitColors.PINK);
			draw(this.catEars, "cat_ears", color, poseStack, collector, light, state);
			draw(this.catTail, "cat_tail", color, poseStack, collector, light, state);
		} else if (head.is(ModItems.BUNNY_EARS)) {
			int color = color(head, OutfitColors.BUNNY);
			draw(this.bunnyEars, "bunny_ears", color, poseStack, collector, light, state);
			draw(this.bunnyTail, "bunny_tail", color, poseStack, collector, light, state);
		}

		ItemStack legs = state.legsEquipment;
		if (legs.is(ModItems.PLEATED_SKIRT)) {
			draw(this.skirt, "pleated_skirt", color(legs, OutfitColors.PINK), poseStack, collector, light, state);
		} else if (legs.is(ModItems.MAID_APRON)) {
			draw(this.skirt, "maid_skirt", color(legs, OutfitColors.MAID), poseStack, collector, light, state);
		}
	}

	private static int color(ItemStack stack, int undyed) {
		return ARGB.opaque(DyedItemColor.getOrDefault(stack, undyed));
	}

	/** Draws the dyeable base texture tinted, then the fixed-color overlay on top. */
	private static void draw(AccessoryModel model, String texture, int color, PoseStack poseStack,
			SubmitNodeCollector collector, int light, AvatarRenderState state) {
		collector.order(0).submitModel(model, state, poseStack, RenderTypes.armorCutoutNoCull(texture(texture)),
				light, OverlayTexture.NO_OVERLAY, color, null, state.outlineColor, null);
		collector.order(1).submitModel(model, state, poseStack, RenderTypes.armorCutoutNoCull(texture(texture + "_overlay")),
				light, OverlayTexture.NO_OVERLAY, -1, null, state.outlineColor, null);
	}

	private static Identifier texture(String name) {
		return FemboyEquipment.id("textures/entity/accessory/" + name + ".png");
	}
}
