#!/usr/bin/env python3
"""Repeatable, conservative API compatibility repairs for Minecraft 1.21.1."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1] / "src/main/java"
changed = 0

for path in root.rglob("*.java"):
    old = path.read_text(encoding="utf-8")
    new = old

    # EntityDimensions is a record in 1.21.
    new = re.sub(r"(getDimensions\([^()]*\))\.(width|height)\b(?!\s*\()", r"\1.\2()", new)

    # Attribute modifier operation enum renames.
    for before, after in (
        ("MULTIPLY_TOTAL", "ADD_MULTIPLIED_TOTAL"),
        ("MULTIPLY_BASE", "ADD_MULTIPLIED_BASE"),
        ("ADDITION", "ADD_VALUE"),
    ):
        new = new.replace("EntityAttributeModifier.Operation." + before,
                          "EntityAttributeModifier.Operation." + after)

    # Attribute instances now use registry entries.
    new = re.sub(r"Multimap\s*<\s*EntityAttribute\s*,",
                 "Multimap<net.minecraft.registry.entry.RegistryEntry<EntityAttribute>,", new)
    new = re.sub(r"Multimap\s*<\s*net\.minecraft\.entity\.attribute\.EntityAttribute\s*,",
                 "Multimap<net.minecraft.registry.entry.RegistryEntry<net.minecraft.entity.attribute.EntityAttribute>,", new)

    # Attribute modifiers are identified by namespaced identifiers in 1.21.
    new = re.sub(
        r'new EntityAttributeModifier\(\s*"([a-z0-9_./-]+)"\s*,',
        r'new EntityAttributeModifier(net.minecraft.util.Identifier.of("ultracraft", "\1"),',
        new,
    )

    if path.name == "UltraDimensions.java":
        new = new.replace("RegistryKey<DimensionType> key = world.getDimensionKey();",
                          "RegistryKey<World> key = world.getRegistryKey();")
        new = new.replace("LIMBO_MANAGER.world.getDimensionKey().equals(key)",
                          "LIMBO_MANAGER.world.getRegistryKey().equals(key)")

    # CCA 6 Component requires a WrapperLookup argument. Keep legacy overloads
    # for internal calls and add adapters for the updated interface.
    if "/components/" in str(path).replace("\\", "/"):
        has_read = re.search(r"\bvoid\s+readFromNbt\s*\(\s*NbtCompound\s+\w+\s*\)", new)
        has_write = re.search(r"\bvoid\s+writeToNbt\s*\(\s*NbtCompound\s+\w+\s*\)", new)
        if has_read and has_write:
            new = re.sub(
                r"(?m)^[ \t]*@Override\s*\n(?=[ \t]*public\s+void\s+(?:readFromNbt|writeToNbt)\s*\()",
                "", new)
            if "RegistryWrapper.WrapperLookup registryLookup" not in new:
                bridge = """
    @Override
    public void readFromNbt(net.minecraft.nbt.NbtCompound nbt,
            net.minecraft.registry.RegistryWrapper.WrapperLookup registryLookup) {
        readFromNbt(nbt);
    }

    @Override
    public void writeToNbt(net.minecraft.nbt.NbtCompound nbt,
            net.minecraft.registry.RegistryWrapper.WrapperLookup registryLookup) {
        writeToNbt(nbt);
    }
"""
                pos = new.rfind("}")
                if pos >= 0:
                    new = new[:pos] + bridge + new[pos:]

    if new != old:
        path.write_text(new, encoding="utf-8")
        changed += 1

print(f"Applied Minecraft 1.21.1 API repairs to {changed} Java files")
