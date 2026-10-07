#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
JAVA = ROOT / "src" / "main" / "java"

REPLACEMENTS = {
    "dev.onyxstudios.cca": "org.ladysnake.cca",
    "import net.minecraft.client.item.TooltipContext;": "import net.minecraft.item.tooltip.TooltipType;",
    "TooltipContext": "net.minecraft.item.Item.TooltipContext",
    "MinecraftClient.getInstance().renderTickCounter.lastFrameDuration": "MinecraftClient.getInstance().getRenderTickCounter().getLastFrameDuration()",
    "import net.fabricmc.fabric.api.item.v1.FabricItemSettings;\n": "",
    "new FabricItemSettings()": "new net.minecraft.item.Item.Settings()",
    "DefaultParticleType": "SimpleParticleType",
    "import net.bettercombat.utils.MathHelper;": "import net.minecraft.util.math.MathHelper;",
    "import net.minecraft.client.sound.MusicType;": "import net.minecraft.sound.MusicType;",
    "import net.minecraft.block.AbstractGlassBlock;": "import net.minecraft.block.TransparentBlock;",
    "extends AbstractGlassBlock": "extends TransparentBlock",
    "import absolutelyaya.goop.api.WaterHandling;\n": "",
    "import absolutelyaya.goop.particles.GoopDropParticleEffect;": "import absolutelyaya.goop.particle.DripParticleEffect;",
    "import absolutelyaya.goop.particles.GoopStringParticleEffect;": "import absolutelyaya.goop.particle.DripParticleEffect;",
    "mod.azure.azurelib.animatable.GeoEntity": "mod.azure.azurelib.common.api.common.animatable.GeoEntity",
    "mod.azure.azurelib.animatable.GeoItem": "mod.azure.azurelib.common.api.common.animatable.GeoItem",
    "mod.azure.azurelib.animatable.GeoBlockEntity": "mod.azure.azurelib.common.api.common.animatable.GeoBlockEntity",
    "mod.azure.azurelib.animatable.SingletonGeoAnimatable": "mod.azure.azurelib.common.internal.common.animatable.SingletonGeoAnimatable",
    "mod.azure.azurelib.animatable.client.RenderProvider": "mod.azure.azurelib.common.internal.client.RenderProvider",
    "mod.azure.azurelib.util.AzureLibUtil": "mod.azure.azurelib.common.internal.common.util.AzureLibUtil",
    "mod.azure.azurelib.constant.DataTickets": "mod.azure.azurelib.common.internal.common.constant.DataTickets",
    "mod.azure.azurelib.model.data.EntityModelData": "mod.azure.azurelib.common.internal.client.model.data.EntityModelData",
    "mod.azure.azurelib.cache.object.GeoBone": "mod.azure.azurelib.common.internal.common.cache.object.GeoBone",
    "mod.azure.azurelib.cache.object.BakedGeoModel": "mod.azure.azurelib.common.internal.common.cache.object.BakedGeoModel",
    "mod.azure.azurelib.model.GeoModel": "mod.azure.azurelib.common.api.client.model.GeoModel",
    "mod.azure.azurelib.model.DefaultedItemGeoModel": "mod.azure.azurelib.common.api.client.model.DefaultedItemGeoModel",
    "mod.azure.azurelib.model.DefaultedBlockGeoModel": "mod.azure.azurelib.common.api.client.model.DefaultedBlockGeoModel",
    "mod.azure.azurelib.renderer.GeoEntityRenderer": "mod.azure.azurelib.common.api.client.renderer.GeoEntityRenderer",
    "mod.azure.azurelib.renderer.GeoItemRenderer": "mod.azure.azurelib.common.api.client.renderer.GeoItemRenderer",
    "mod.azure.azurelib.renderer.GeoBlockRenderer": "mod.azure.azurelib.common.api.client.renderer.GeoBlockRenderer",
    "mod.azure.azurelib.renderer.GeoArmorRenderer": "mod.azure.azurelib.common.api.client.renderer.GeoArmorRenderer",
    "mod.azure.azurelib.renderer.GeoRenderer": "mod.azure.azurelib.common.internal.client.renderer.GeoRenderer",
    "mod.azure.azurelib.renderer.layer.GeoRenderLayer": "mod.azure.azurelib.common.api.client.renderer.layer.GeoRenderLayer",
    "mod.azure.azurelib.renderer.layer.BlockAndItemGeoLayer": "mod.azure.azurelib.common.api.client.renderer.layer.BlockAndItemGeoLayer",
}

changed = 0
for path in JAVA.rglob("*.java"):
    text = path.read_text(encoding="utf-8")
    new = text
    for old, replacement in REPLACEMENTS.items():
        new = new.replace(old, replacement)

    new = re.sub(
        r"appendTooltip\(ItemStack stack,\s*(?:@Nullable\s+)?World world,\s*List<Text> tooltip,\s*net\.minecraft\.item\.Item\.TooltipContext context\)",
        "appendTooltip(ItemStack stack, net.minecraft.item.Item.TooltipContext context, List<Text> tooltip, TooltipType type)",
        new,
    )
    new = new.replace("super.appendTooltip(stack, world, tooltip, context);", "super.appendTooltip(stack, context, tooltip, type);")
    new = new.replace("context.isAdvanced()", "type.isAdvanced()")

    new = re.sub(
        r"new GoopDropParticleEffect\(new Vec3d\(0\.56,\s*0\.09,\s*0\.01\),\s*([^,\n]+),\s*true,\s*WaterHandling\.REPLACE_WITH_CLOUD_PARTICLE\)",
        r"new DripParticleEffect(0xFF8F1703, \1, true)",
        new,
    )
    new = re.sub(
        r"new GoopStringParticleEffect\(new Vec3d\(0\.56,\s*0\.09,\s*0\.01\),\s*([^,\n]+),\s*true\)",
        r"new DripParticleEffect(0xFF8F1703, \1, true)",
        new,
    )

    if new != text:
        path.write_text(new, encoding="utf-8")
        changed += 1

teleport_files = {
    JAVA / "absolutelyaya/ultracraft/dimension/LevelManager.java": [
        (
            r"FabricDimensions\.teleport\(player, overworld, new TeleportTarget\(overworld\.getSpawnPos\(\)\.toCenterPos\(\), Vec3d\.ZERO, player\.getYaw\(\), player\.getPitch\(\)\)\);",
            "player.teleport(overworld, overworld.getSpawnPos().getX() + 0.5, overworld.getSpawnPos().getY() + 0.5, overworld.getSpawnPos().getZ() + 0.5, player.getYaw(), player.getPitch());",
        ),
        (
            r"FabricDimensions\.teleport\(player, world\.getServer\(\)\.getWorld\(spawnDimension\),\s*new TeleportTarget\(spawnPoint\.toCenterPos\(\), Vec3d\.ZERO, player\.getYaw\(\), player\.getPitch\(\)\)\);",
            "player.teleport(world.getServer().getWorld(spawnDimension), spawnPoint.getX() + 0.5, spawnPoint.getY() + 0.5, spawnPoint.getZ() + 0.5, player.getYaw(), player.getPitch());",
        ),
        (
            r"FabricDimensions\.teleport\(player, world, new TeleportTarget\(spawnPos\.toCenterPos\(\), Vec3d\.ZERO,\s*LevelDataManager\.getLevelData\(levelIdForInstanceId\.get\(id\)\)\.getSpawnRot\(\), 0f\)\);",
            "player.teleport(world, spawnPos.getX() + 0.5, spawnPos.getY() + 0.5, spawnPos.getZ() + 0.5, LevelDataManager.getLevelData(levelIdForInstanceId.get(id)).getSpawnRot(), 0f);",
        ),
    ],
    JAVA / "absolutelyaya/ultracraft/command/Commands.java": [
        (
            r"FabricDimensions\.teleport\(context\.getSource\(\)\.getPlayer\(\), LevelManager\.Instance\.getWorld\(\),\s*new TeleportTarget\(new Vec3d\(0, 64, 0\), Vec3d\.ZERO, 0f, 0f\)\);",
            "context.getSource().getPlayer().teleport(LevelManager.Instance.getWorld(), 0.0, 64.0, 0.0, 0f, 0f);",
        ),
    ],
    JAVA / "absolutelyaya/ultracraft/registry/PacketRegistry.java": [
        (
            r"FabricDimensions\.teleport\(player, world, new TeleportTarget\(pos\.toCenterPos\(\), Vec3d\.ZERO, world\.getSpawnAngle\(\), 0f\)\);",
            "player.teleport(world, pos.getX() + 0.5, pos.getY() + 0.5, pos.getZ() + 0.5, world.getSpawnAngle(), 0f);",
        ),
    ],
}

for path, rules in teleport_files.items():
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    new = text.replace("import net.fabricmc.fabric.api.dimension.v1.FabricDimensions;\n", "")
    for pattern, replacement in rules:
        new = re.sub(pattern, replacement, new, flags=re.MULTILINE)
    if new != text:
        path.write_text(new, encoding="utf-8")
        changed += 1

# Optional integrations can be restored after the core 1.21.1 port is stable.
for relative in (
    "absolutelyaya/ultracraft/mixin/compat/carryon/PickupHandlerMixin.java",
    "absolutelyaya/ultracraft/mixin/compat/carryon/PlacementHandlerMixin.java",
    "absolutelyaya/ultracraft/mixin/compat/yigd/DeathHandlerMixin.java",
    "absolutelyaya/ultracraft/compat/REIClientPlugin.java",
):
    (JAVA / relative).unlink(missing_ok=True)

mixins = ROOT / "src/main/resources/ultracraft.mixins.json"
if mixins.exists():
    text = mixins.read_text(encoding="utf-8")
    for name in (
        "compat.carryon.PickupHandlerMixin",
        "compat.carryon.PlacementHandlerMixin",
        "compat.yigd.DeathHandlerMixin",
    ):
        text = re.sub(rf'\s*"{re.escape(name)}",?', "", text)
    text = re.sub(r',\s*]', '\n  ]', text)
    mixins.write_text(text, encoding="utf-8")

mod_json = ROOT / "src/main/resources/fabric.mod.json"
if mod_json.exists():
    text = mod_json.read_text(encoding="utf-8")
    text = re.sub(r'\s*"rei_client"\s*:\s*\[\s*"absolutelyaya\.ultracraft\.compat\.REIClientPlugin"\s*]\s*,?', "", text)
    text = re.sub(r'}\s*"cardinal-components-entity"', '},\n    "cardinal-components-entity"', text)
    mod_json.write_text(text, encoding="utf-8")

aw = ROOT / "src/main/resources/ultracraft.accesswidener"
if aw.exists():
    text = aw.read_text(encoding="utf-8")
    text = text.replace(
        "accessible field net/minecraft/client/MinecraftClient renderTickCounter Lnet/minecraft/client/render/RenderTickCounter;\n",
        "",
    )
    aw.write_text(text, encoding="utf-8")

print(f"Applied 1.21.1 source migrations to {changed} Java files.")
