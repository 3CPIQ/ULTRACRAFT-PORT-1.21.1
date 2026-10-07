#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "src/main/java/absolutelyaya/ultracraft/registry/ItemRegistry.java"

SONGS = {
    "clair_de_lune": ("ultracraft:music.clair_de_lune", 231.0, "Clair de Lune"),
    "fire_is_gone": ("ultracraft:music.the_fire_is_gone", 109.0, "The Fire Is Gone"),
    "prelude1": ("ultracraft:music.prelude1", 197.0, "Prelude I"),
    "prelude1_calm": ("ultracraft:music.prelude1_calm", 197.0, "Prelude I (Calm)"),
    "prelude2": ("ultracraft:music.prelude2", 181.0, "Prelude II"),
    "prelude2_calm": ("ultracraft:music.prelude2_calm", 181.0, "Prelude II (Calm)"),
    "cerberus": ("ultracraft:music.cerberus", 135.0, "Cerberus"),
    "cerberus_calm": ("ultracraft:music.cerberus_calm", 135.0, "Cerberus (Calm)"),
    "limbo1_illusion": ("ultracraft:music.limbo1_illusion", 116.0, "Into the Fire (Illusion)"),
    "limbo1": ("ultracraft:music.limbo1", 114.0, "Into the Fire"),
    "limbo1_calm": ("ultracraft:music.limbo1_calm", 114.0, "Into the Fire (Calm)"),
    "limbo2": ("ultracraft:music.limbo2", 176.0, "Unstoppable Force"),
    "limbo2_calm": ("ultracraft:music.limbo2_calm", 176.0, "Unstoppable Force (Calm)"),
    "versus": ("ultracraft:music.versus", 128.0, "Versus"),
    "counterfeit": ("ultracraft:music.counterfeit", 196.0, "Counterfeit"),
    "cybergrind": ("ultracraft:music.efefski_cybergrind", 269.0, "The Cyber Grind"),
}

text = ITEMS.read_text(encoding="utf-8")
pattern = re.compile(
    r'public static final MusicDiscItem\s+(\w+)\s*=\s*Registry\.register\(Registries\.ITEM,\s*'
    r'Ultracraft\.identifier\("disc/([^"\\]+)"\),\s*'
    r'new MusicDiscItem\(15,\s*SoundRegistry\.[A-Z0-9_]+\.value\(\),\s*'
    r'(new net\.minecraft\.item\.Item\.Settings\(\)\.maxCount\(1\)\.rarity\(Rarity\.RARE\)),\s*\d+\)\);',
    re.MULTILINE,
)

def replace(match):
    field, song_id, settings = match.groups()
    return (
        f'public static final Item {field} = Registry.register(Registries.ITEM,\n'
        f'\t\t\tUltracraft.identifier("disc/{song_id}"),\n'
        f'\t\t\tnew Item({settings}.jukeboxPlayable('
        f'RegistryKey.of(RegistryKeys.JUKEBOX_SONG, Ultracraft.identifier("disc/{song_id}")))));'
    )

text, count = pattern.subn(replace, text)
ITEMS.write_text(text, encoding="utf-8")

base = ROOT / "src/main/resources/data/ultracraft/jukebox_song/disc"
base.mkdir(parents=True, exist_ok=True)
for song_id, (sound_id, length, title) in SONGS.items():
    payload = {
        "comparator_output": 15,
        "description": {"text": title},
        "length_in_seconds": length,
        "sound_event": {"sound_id": sound_id},
    }
    (base / f"{song_id}.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

print(f"Ported {count} legacy MusicDiscItem declarations and generated {len(SONGS)} jukebox songs.")
