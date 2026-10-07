#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
JAVA = ROOT / "src" / "main" / "java"

REPLACEMENTS = {
    # Cardinal Components moved Java packages for the 1.21.x line.
    "dev.onyxstudios.cca": "org.ladysnake.cca",
    # TooltipContext became Item.TooltipContext in 1.21.
    "import net.minecraft.client.item.TooltipContext;": "import net.minecraft.item.tooltip.TooltipType;",
    "TooltipContext": "net.minecraft.item.Item.TooltipContext",
    # MinecraftClient now exposes the render tick counter through a getter.
    "MinecraftClient.getInstance().renderTickCounter.lastFrameDuration": "MinecraftClient.getInstance().getRenderTickCounter().getLastFrameDuration()",
    # FabricItemSettings was removed; vanilla Item.Settings is used directly now.
    "import net.fabricmc.fabric.api.item.v1.FabricItemSettings;\n": "",
    "new FabricItemSettings()": "new net.minecraft.item.Item.Settings()",
    # Yarn renamed DefaultParticleType to SimpleParticleType.
    "DefaultParticleType": "SimpleParticleType",
    # This file only needs clamp; avoid depending on Better Combat internals.
    "import net.bettercombat.utils.MathHelper;": "import net.minecraft.util.math.MathHelper;",
    # Goop 1.21.1 reorganized particles under absolutelyaya.goop.particle.
    "import absolutelyaya.goop.api.WaterHandling;\n": "",
    "import absolutelyaya.goop.particles.GoopDropParticleEffect;": "import absolutelyaya.goop.particle.DripParticleEffect;",
    "import absolutelyaya.goop.particles.GoopStringParticleEffect;": "import absolutelyaya.goop.particle.DripParticleEffect;",
}

changed = 0
for path in JAVA.rglob("*.java"):
    text = path.read_text(encoding="utf-8")
    new = text
    for old, replacement in REPLACEMENTS.items():
        new = new.replace(old, replacement)

    # 1.20.x Item/Block tooltip override -> 1.21.1 signature.
    new = re.sub(
        r"appendTooltip\(ItemStack stack,\s*(?:@Nullable\s+)?World world,\s*List<Text> tooltip,\s*net\.minecraft\.item\.Item\.TooltipContext context\)",
        "appendTooltip(ItemStack stack, net.minecraft.item.Item.TooltipContext context, List<Text> tooltip, TooltipType type)",
        new,
    )
    new = new.replace("super.appendTooltip(stack, world, tooltip, context);", "super.appendTooltip(stack, context, tooltip, type);")
    new = new.replace("context.isAdvanced()", "type.isAdvanced()")

    # Goop 1.21.1 replaced the old Vec3d + WaterHandling drip/string effects
    # with a compact ARGB DripParticleEffect. Preserve ULTRACRAFT's blood color.
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

# FabricDimensions was removed in Fabric API for 1.21; ServerPlayerEntity has
# native cross-dimension teleport methods now.
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

# The old direct MinecraftClient.renderTickCounter access is no longer needed
# after switching to MinecraftClient#getRenderTickCounter(). Remove the obsolete
# access widener entry so Loom can validate the 1.21.1 mappings.
aw = ROOT / "src" / "main" / "resources" / "ultracraft.accesswidener"
if aw.exists():
    text = aw.read_text(encoding="utf-8")
    new = text.replace(
        "accessible field net/minecraft/client/MinecraftClient renderTickCounter Lnet/minecraft/client/render/RenderTickCounter;\n",
        "",
    )
    if new != text:
        aw.write_text(new, encoding="utf-8")

print(f"Applied 1.21.1 source migrations to {changed} Java files.")
