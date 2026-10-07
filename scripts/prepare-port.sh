#!/usr/bin/env bash
set -euo pipefail

UPSTREAM_REPO="https://github.com/absolutelyaya/ultracraft.git"
UPSTREAM_BRANCH="fabric-1.20.1"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP"
}
trap cleanup EXIT

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

# Loom 1.7.x requires Gradle 8.8+. Upstream 1.20.1 still uses 8.6.
sed -i 's/gradle-8\.6-bin\.zip/gradle-8.8-bin.zip/' "$ROOT/gradle/wrapper/gradle-wrapper.properties"

# Apply repeatable mechanical source migrations after copying upstream.
python3 "$ROOT/scripts/apply-source-port.py"

# Overlay files that need a semantic rewrite instead of a mechanical migration.
if [ -d "$ROOT/port/src" ]; then
  rsync -a "$ROOT/port/src/" "$ROOT/src/"
fi

echo "Prepared ULTRACRAFT upstream source with the Fabric 1.21.1 port overlay."
echo "Next: ./gradlew clean build --continue"
