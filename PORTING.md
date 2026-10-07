# ULTRACRAFT 1.21.1 Port Status

Target: **Minecraft 1.21.1 / Fabric / Java 21**.

Intended secondary runtime: **NeoForge 1.21.1 through Sinytra Connector**, if the finished Fabric build is compatible.

## Upstream

- Repository: https://github.com/absolutelyaya/ultracraft
- Source branch: `fabric-1.20.1`
- Starting source version: `1.20.1-2.2.2`

## Bootstrap completed

- [x] Target Minecraft 1.21.1
- [x] Target Java 21
- [x] Fabric Loom 1.7.4
- [x] Yarn 1.21.1 mappings
- [x] Fabric API 1.21.1
- [x] Cardinal Components 1.21.1 dependency line prepared
- [x] Player Animation Library 1.21.1 dependency line prepared
- [x] Trinkets 1.21.1 dependency line prepared
- [x] `fabric.mod.json` overlay updated to Minecraft 1.21.1 / Java 21
- [x] Windows and Linux upstream-sync scripts
- [x] GitHub Actions Java 21 compile workflow

## Expected migration areas

1. Minecraft 1.20.1 -> 1.21.1 API/mapping changes.
2. ItemStack/NBT -> data component changes introduced after 1.20.1.
3. Fabric networking API changes to custom payloads/codecs.
4. Rendering and client API changes.
5. Mixins whose target methods changed between 1.20.1 and 1.21.1.
6. Fabric-ASM / ClassTinkerers early-riser compatibility.
7. AzureLib and GOOP dependency migration.
8. Optional integrations: REI, Better Combat, Carry On, YIGD, dynamic lights.
9. Datagen/advancement/resource format changes.
10. Final test under Sinytra Connector + Forgified Fabric API on NeoForge 1.21.1.

## Local workflow

Windows:

```powershell
.\scripts\prepare-port.ps1
.\gradlew.bat compileJava --continue
```

Linux/macOS:

```bash
bash scripts/prepare-port.sh
./gradlew compileJava --continue
```

The preparation script clones the untouched upstream `fabric-1.20.1` branch into the working directory, then applies the files in `port/` on top. This keeps upstream source separate while the 1.21.1 migration is developed.

## Current status

**Bootstrap / first compile-error collection.** The project is not playable yet. The next milestone is getting the upstream source through dependency resolution and collecting the first complete 1.21.1 Java compile error set.
