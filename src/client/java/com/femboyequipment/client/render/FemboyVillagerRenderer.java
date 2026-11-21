package com.femboyequipment.client.render;

import com.femboyequipment.FemboyEquipment;
import com.femboyequipment.client.model.AccessoryModels;
import com.femboyequipment.entity.FemboyVillager;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.ArmorModelSet;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.client.renderer.entity.layers.HumanoidArmorLayer;
import net.minecraft.client.renderer.entity.state.HumanoidRenderState;
import net.minecraft.resources.Identifier;

public class FemboyVillagerRenderer extends HumanoidMobRenderer<FemboyVillager, HumanoidRenderState, HumanoidModel<HumanoidRenderState>> {
	private static final Identifier TEXTURE = FemboyEquipment.id("textures/entity/femboy_villager.png");

	public FemboyVillagerRenderer(EntityRendererProvider.Context context) {
		super(context, new HumanoidModel<>(context.bakeLayer(AccessoryModels.FEMBOY_VILLAGER)), 0.5F);
		this.addLayer(new HumanoidArmorLayer<>(this,
				ArmorModelSet.bake(ModelLayers.ZOMBIE_ARMOR, context.getModelSet(), HumanoidModel::new),
				context.getEquipmentRenderer()));
		this.addLayer(new AccessoryLayer<>(this, context.getModelSet()));
	}

	@Override
	public Identifier getTextureLocation(HumanoidRenderState state) {
		return TEXTURE;
	}

	@Override
	public HumanoidRenderState createRenderState() {
		return new HumanoidRenderState();
	}
}
