#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1] / "src/main/java"
changed = 0
for path in root.rglob("*.java"):
    old = path.read_text(encoding="utf-8")
    new = re.sub(
        r"(?m)^(\s*)(protected|public)\s+void\s+initDataTracker\s*\(\s*\)\s*\{",
        r"\1\2 void initDataTracker(net.minecraft.entity.data.DataTracker.Builder builder) {",
        old,
    )
    new = new.replace("super.initDataTracker();", "super.initDataTracker(builder);")
    new = re.sub(r"\b(?:this\.)?dataTracker\.startTracking\(", "builder.add(", new)
    new = re.sub(r"new Identifier\(\s*(\"[^\"]+\")\s*,\s*(\"[^\"]+\")\s*\)", r"Identifier.of(\1, \2)", new)
    new = re.sub(r"new Identifier\(\s*(\"[^\"]+\")\s*\)", r"Identifier.of(\1)", new)
    if new != old:
        path.write_text(new, encoding="utf-8")
        changed += 1
print(f"Applied corrected 1.21.1 migrations to {changed} files")
