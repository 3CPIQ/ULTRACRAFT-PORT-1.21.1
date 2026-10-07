#!/usr/bin/env python3
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1] / "src/main/java"
for path in root.rglob("*.java"):
    old = path.read_text(encoding="utf-8")
    new = re.sub(r"(getDimensions\([^()]*\))\.(width|height)\b(?!\s*\()", r"\1.\2()", old)
    new = new.replace("EntityAttributeModifier.Operation.MULTIPLY_TOTAL", "EntityAttributeModifier.Operation.ADD_MULTIPLIED_TOTAL")
    new = new.replace("EntityAttributeModifier.Operation.MULTIPLY_BASE", "EntityAttributeModifier.Operation.ADD_MULTIPLIED_BASE")
    new = new.replace("EntityAttributeModifier.Operation.ADDITION", "EntityAttributeModifier.Operation.ADD_VALUE")
    if new != old:
        path.write_text(new, encoding="utf-8")
