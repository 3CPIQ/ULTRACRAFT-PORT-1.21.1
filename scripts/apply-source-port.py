#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JAVA = ROOT / "src" / "main" / "java"

REPLACEMENTS = {
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

print(f"Applied 1.21.1 source migrations to {changed} Java files.")
