#!/usr/bin/env bash
set -euo pipefail

UPSTREAM_REPO="https://github.com/absolutelyaya/ultracraft.git"
UPSTREAM_BRANCH="fabric-1.20.1"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$ROOT/.upstream-ultracraft"

rm -rf "$TMP"
git clone --depth 1 --branch "$UPSTREAM_BRANCH" "$UPSTREAM_REPO" "$TMP"

# Copy upstream working tree, but never overwrite this repository's Git metadata,
# port overlays, scripts, workflow, or port documentation.
rsync -a --delete \
  --exclude='.git/' \
  --exclude='port/' \
  --exclude='scripts/' \
  --exclude='.github/' \
  --exclude='PORTING.md' \
  --exclude='README.md' \
  "$TMP/" "$ROOT/"

cp "$ROOT/port/gradle.properties" "$ROOT/gradle.properties"
cp "$ROOT/port/settings.gradle" "$ROOT/settings.gradle"
cp "$ROOT/port/build.gradle" "$ROOT/build.gradle"
cp "$ROOT/port/fabric.mod.json" "$ROOT/src/main/resources/fabric.mod.json"

rm -rf "$TMP"
echo "Prepared ULTRACRAFT upstream source with the Fabric 1.21.1 port overlay."
echo "Next: ./gradlew compileJava --continue"
