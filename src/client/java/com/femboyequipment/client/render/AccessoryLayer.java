package com.femboyequipment.client.render;

import com.femboyequipment.api.client.AccessoryShape;
import com.femboyequipment.client.model.AccessoryModel;
import com.femboyequipment.client.model.AccessoryModels;
import com.mojang.blaze3d.vertex.PoseStack;
import java.util.ArrayList;
import java.util.EnumMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.EntityModelSet;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.entity.state.HumanoidRenderState;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.Identifier;
import net.minecraft.util.ARGB;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.DyedItemColor;
import org.jspecify.annotations.Nullable;

/**
 * Draws 3D accessories (ears, tails, skirts) on humanoids wearing items registered for them,
 * by FemboyEquipment itself or by addons via {@code FemboyEquipmentClientApi.registerAccessory}.
 */
public class AccessoryLayer<S extends HumanoidRenderState, M extends HumanoidModel<S>> extends RenderLayer<S, M> {
	private record Entry(AccessoryShape shape, Identifier texture, @Nullable Identifier overlay, int undyedColor) {
	}

	private static final Map<Item, List<Entry>> ACCESSORIES = new LinkedHashMap<>();

	private final Map<AccessoryShape, AccessoryModel> models = new EnumMap<>(AccessoryShape.class);

	public AccessoryLayer(RenderLayerParent<S, M> parent, EntityModelSet modelSet) {
		super(parent);
		this.models.put(AccessoryShape.CAT_EARS, new AccessoryModel(modelSet.bakeLayer(AccessoryModels.CAT_EARS)));
		this.models.put(AccessoryShape.CAT_TAIL, new AccessoryModel(modelSet.bakeLayer(AccessoryModels.CAT_TAIL)));
		this.models.put(AccessoryShape.BUNNY_EARS, new AccessoryModel(modelSet.bakeLayer(AccessoryModels.BUNNY_EARS)));
		this.models.put(AccessoryShape.BUNNY_TAIL, new AccessoryModel(modelSet.bakeLayer(AccessoryModels.BUNNY_TAIL)));
		this.models.put(AccessoryShape.SKIRT, new AccessoryModel(modelSet.bakeLayer(AccessoryModels.SKIRT)));
	}

	public static synchronized void register(Item item, AccessoryShape shape, Identifier texture,
			@Nullable Identifier overlay, int undyedColor) {
		ACCESSORIES.computeIfAbsent(item, k -> new ArrayList<>()).add(new Entry(shape, texture, overlay, undyedColor));
	}

	@Override
	public void submit(PoseStack poseStack, SubmitNodeCollector collector, int light, S state, float yRot, float xRot) {
		if (state.isInvisible) {
			return;
		}
		for (ItemStack stack : new ItemStack[] {state.headEquipment, state.chestEquipment, state.legsEquipment, state.feetEquipment}) {
			if (stack.isEmpty()) {
				continue;
			}
			List<Entry> entries = ACCESSORIES.get(stack.getItem());
			if (entries == null) {
				continue;
			}
			for (Entry entry : entries) {
				int color = ARGB.opaque(DyedItemColor.getOrDefault(stack, entry.undyedColor()));
				draw(this.models.get(entry.shape()), entry, color, poseStack, collector, light, state);
			}
		}
	}

	/** Draws the dyeable base texture tinted, then the fixed-color overlay on top. */
	private static void draw(AccessoryModel model, Entry entry, int color, PoseStack poseStack,
			SubmitNodeCollector collector, int light, HumanoidRenderState state) {
		collector.order(0).submitModel(model, state, poseStack, RenderTypes.armorCutoutNoCull(entry.texture()),
				light, OverlayTexture.NO_OVERLAY, color, null, state.outlineColor, null);
		if (entry.overlay() != null) {
			collector.order(1).submitModel(model, state, poseStack, RenderTypes.armorCutoutNoCull(entry.overlay()),
					light, OverlayTexture.NO_OVERLAY, -1, null, state.outlineColor, null);
		}
	}
}
