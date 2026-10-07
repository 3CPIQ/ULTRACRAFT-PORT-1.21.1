#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
JAVA = ROOT / "src" / "main" / "java"

REPLACEMENTS = {
    # Cardinal Components moved packages for the 1.21.x line.
    "dev.onyxstudios.cca": "org.ladysnake.cca",
}

changed = 0
for path in JAVA.rglob("*.java"):
    text = path.read_text(encoding="utf-8")
    new = text
    for old, replacement in REPLACEMENTS.items():
        new = new.replace(old, replacement)
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

print(f"Applied 1.21.1 source migrations to {changed} Java files.")
