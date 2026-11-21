package com.femboyequipment.client.model;

import com.femboyequipment.FemboyEquipment;
import net.fabricmc.fabric.api.client.rendering.v1.EntityModelLayerRegistry;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * 3D accessory geometry. Texture layouts are mirrored by the texture generator, so keep
 * texOffs / box sizes in sync with it.
 */
public final class AccessoryModels {
	public static final String TAIL = "tail";

	public static final ModelLayerLocation CAT_EARS = layer("cat_ears");
	public static final ModelLayerLocation CAT_TAIL = layer("cat_tail");
	public static final ModelLayerLocation BUNNY_EARS = layer("bunny_ears");
	public static final ModelLayerLocation BUNNY_TAIL = layer("bunny_tail");
	public static final ModelLayerLocation SKIRT = layer("skirt");
	public static final ModelLayerLocation FEMBOY_VILLAGER = layer("femboy_villager");

	private AccessoryModels() {
	}

	private static ModelLayerLocation layer(String name) {
		return new ModelLayerLocation(FemboyEquipment.id(name), "main");
	}

	public static void register() {
		EntityModelLayerRegistry.registerModelLayer(CAT_EARS, AccessoryModels::catEars);
		EntityModelLayerRegistry.registerModelLayer(CAT_TAIL, AccessoryModels::catTail);
		EntityModelLayerRegistry.registerModelLayer(BUNNY_EARS, AccessoryModels::bunnyEars);
		EntityModelLayerRegistry.registerModelLayer(BUNNY_TAIL, AccessoryModels::bunnyTail);
		EntityModelLayerRegistry.registerModelLayer(SKIRT, AccessoryModels::skirt);
		EntityModelLayerRegistry.registerModelLayer(FEMBOY_VILLAGER,
				() -> LayerDefinition.create(HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F), 64, 32));
	}

	/** An empty humanoid skeleton to hang accessories on. */
	private static MeshDefinition emptyHumanoid() {
		MeshDefinition mesh = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
		mesh.getRoot().clearRecursively();
		return mesh;
	}

	private static LayerDefinition catEars() {
		MeshDefinition mesh = emptyHumanoid();
		PartDefinition head = mesh.getRoot().getChild("head");
		for (int side = -1; side <= 1; side += 2) {
			// Pointy ears: a 3x3 base, a 2x2 middle and a 1x1 tip, tilted outwards.
			CubeListBuilder ear = CubeListBuilder.create()
					.texOffs(0, 0).addBox(-1.5F, -3.0F, -0.5F, 3.0F, 3.0F, 1.0F)
					.texOffs(0, 4).addBox(-1.0F, -5.0F, -0.5F, 2.0F, 2.0F, 1.0F)
					.texOffs(0, 8).addBox(-0.5F, -6.0F, -0.5F, 1.0F, 1.0F, 1.0F);
			head.addOrReplaceChild(side < 0 ? "left_ear" : "right_ear", ear,
					PartPose.offsetAndRotation(side * 2.5F, -8.0F, -1.0F, 0.0F, 0.0F, side * 0.3F));
		}
		return LayerDefinition.create(mesh, 16, 16);
	}

	private static LayerDefinition bunnyEars() {
		MeshDefinition mesh = emptyHumanoid();
		PartDefinition head = mesh.getRoot().getChild("head");
		for (int side = -1; side <= 1; side += 2) {
			CubeListBuilder ear = CubeListBuilder.create().texOffs(0, 0).addBox(-1.0F, -8.0F, -0.5F, 2.0F, 8.0F, 1.0F);
			head.addOrReplaceChild(side < 0 ? "left_ear" : "right_ear", ear,
					PartPose.offsetAndRotation(side * 2.0F, -7.5F, 0.0F, -0.15F, 0.0F, side * 0.15F));
		}
		return LayerDefinition.create(mesh, 16, 16);
	}

	private static LayerDefinition catTail() {
		MeshDefinition mesh = emptyHumanoid();
		PartDefinition body = mesh.getRoot().getChild("body");
		// Three segments curling upwards; the root segment is animated in AccessoryModel.
		PartDefinition seg1 = body.addOrReplaceChild(TAIL,
				CubeListBuilder.create().texOffs(0, 0).addBox(-0.5F, -0.5F, 0.0F, 1.0F, 1.0F, 4.0F),
				PartPose.offsetAndRotation(0.0F, 10.5F, 2.0F, 0.35F, 0.0F, 0.0F));
		PartDefinition seg2 = seg1.addOrReplaceChild("segment_2",
				CubeListBuilder.create().texOffs(0, 0).addBox(-0.5F, -0.5F, 0.0F, 1.0F, 1.0F, 4.0F),
				PartPose.offsetAndRotation(0.0F, 0.0F, 3.8F, 0.55F, 0.0F, 0.0F));
		seg2.addOrReplaceChild("tip",
				CubeListBuilder.create().texOffs(0, 6).addBox(-0.5F, -0.5F, 0.0F, 1.0F, 1.0F, 3.0F),
				PartPose.offsetAndRotation(0.0F, 0.0F, 3.8F, 0.55F, 0.0F, 0.0F));
		return LayerDefinition.create(mesh, 16, 16);
	}

	private static LayerDefinition bunnyTail() {
		MeshDefinition mesh = emptyHumanoid();
		mesh.getRoot().getChild("body").addOrReplaceChild(TAIL,
				CubeListBuilder.create().texOffs(0, 10).addBox(-1.5F, -1.5F, 0.0F, 3.0F, 3.0F, 2.0F),
				PartPose.offset(0.0F, 10.5F, 2.0F));
		return LayerDefinition.create(mesh, 16, 16);
	}

	private static LayerDefinition skirt() {
		MeshDefinition mesh = emptyHumanoid();
		PartDefinition body = mesh.getRoot().getChild("body");
		float flare = 0.35F;
		body.addOrReplaceChild("waist",
				CubeListBuilder.create().texOffs(0, 0).addBox(-4.5F, -1.0F, -2.5F, 9.0F, 2.0F, 5.0F),
				PartPose.offset(0.0F, 11.0F, 0.0F));
		body.addOrReplaceChild("front",
				CubeListBuilder.create().texOffs(0, 8).addBox(-5.0F, 0.0F, -0.5F, 10.0F, 6.0F, 1.0F),
				PartPose.offsetAndRotation(0.0F, 11.5F, -2.5F, -flare, 0.0F, 0.0F));
		body.addOrReplaceChild("back",
				CubeListBuilder.create().texOffs(0, 16).addBox(-5.0F, 0.0F, -0.5F, 10.0F, 6.0F, 1.0F),
				PartPose.offsetAndRotation(0.0F, 11.5F, 2.5F, flare, 0.0F, 0.0F));
		body.addOrReplaceChild("right",
				CubeListBuilder.create().texOffs(24, 8).addBox(-0.5F, 0.0F, -3.0F, 1.0F, 6.0F, 6.0F),
				PartPose.offsetAndRotation(-4.5F, 11.5F, 0.0F, 0.0F, 0.0F, flare));
		body.addOrReplaceChild("left",
				CubeListBuilder.create().texOffs(40, 8).addBox(-0.5F, 0.0F, -3.0F, 1.0F, 6.0F, 6.0F),
				PartPose.offsetAndRotation(4.5F, 11.5F, 0.0F, 0.0F, 0.0F, -flare));
		return LayerDefinition.create(mesh, 64, 32);
	}
}
