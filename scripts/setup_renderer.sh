#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/tools" "$ROOT/assets" "$ROOT/output"
sudo apt-get update -qq
sudo apt-get install -y -qq curl wget unzip zip git ffmpeg xz-utils libegl1 libgl1 libxi6 libxxf86vm1 libxfixes3 libxrender1 libxkbcommon0 libsm6 >/dev/null

BLENDER_RELEASE="https://download.blender.org/release/Blender4.2/blender-4.2.3-linux-x64.tar.xz"
curl -fL --retry 3 --connect-timeout 30 "$BLENDER_RELEASE" -o "$ROOT/tools/blender.tar.xz"
tar -xf "$ROOT/tools/blender.tar.xz" -C "$ROOT/tools"
BLENDER="$ROOT/tools/blender-4.2.3-linux-x64/blender"
"$BLENDER" --version | head -2

git clone --depth 1 --branch master https://github.com/makehumancommunity/mpfb2.git "$ROOT/tools/mpfb2"
(cd "$ROOT/tools/mpfb2/src/mpfb" && zip -qr "$ROOT/tools/mpfb.zip" .)
"$BLENDER" -b --command extension install-file -r user_default -e "$ROOT/tools/mpfb.zip"

ASSET_ZIP="$ROOT/tools/makehuman_system_assets_cc0.zip"
PRIMARY="https://files2.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip"
MIRROR="https://files.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip"
if ! curl -fL --retry 2 --speed-time 120 --speed-limit 8192 --max-time 1200 "$PRIMARY" -o "$ASSET_ZIP"; then
  echo "Primary MakeHuman asset mirror unavailable; trying alternate mirror"
  curl -fL --retry 2 --speed-time 120 --speed-limit 8192 --max-time 1200 "$MIRROR" -o "$ASSET_ZIP"
fi
unzip -t "$ASSET_ZIP" >/dev/null
unzip -qo "$ASSET_ZIP" -d "$ROOT/assets"
for file in young_caucasian_female.mhmat high-poly.mhclo eyebrow001.mhclo eyelashes01.mhclo long01.mhclo female_casualsuit01.mhclo; do
  if ! find "$ROOT/assets" -type f -name "$file" | grep -q .; then
    echo "Required original MakeHuman asset missing: $file" >&2
    exit 1
  fi
done
echo "Blender + real MPFB2 + actual CC0 assets installed"