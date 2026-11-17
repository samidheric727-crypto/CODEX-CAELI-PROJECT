#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/tools" "$ROOT/assets" "$ROOT/output"
sudo apt-get update -qq
sudo apt-get install -y -qq curl unzip zip git ffmpeg libegl1 libgl1 libxi6 libxxf86vm1 libxfixes3 libxrender1 libxkbcommon0 libsm6 > /dev/null
echo "[INFO] Using Blender installed by cached setup-blender action"
blender --version | head -2

echo "[INFO] Fetching real MPFB2 human generator"
git clone --depth 1 --branch master https://github.com/makehumancommunity/mpfb2.git "$ROOT/tools/mpfb2"
(cd "$ROOT/tools/mpfb2/src/mpfb" && zip -qr "$ROOT/tools/mpfb.zip" .)
blender -b --command extension install-file -r user_default -e "$ROOT/tools/mpfb.zip"

echo "[INFO] Downloading official 267MB CC0 MakeHuman assets (hard 4-minute limit per mirror)"
ASSET_ZIP="$ROOT/tools/makehuman_system_assets_cc0.zip"
PRIMARY="https://files.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip"
MIRROR="https://files2.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip"
fetch_asset () {
  curl --fail --location --show-error --retry 0 --connect-timeout 15 \
       --speed-time 40 --speed-limit 16384 --max-time 240 \
       --output "$ASSET_ZIP" "$1"
}
if ! fetch_asset "$PRIMARY"; then
  echo "::warning::Primary asset host failed; attempting official secondary mirror"
  rm -f "$ASSET_ZIP"
  fetch_asset "$MIRROR"
fi
echo "[INFO] Download finished; verifying ZIP and unpacking"
unzip -t "$ASSET_ZIP" >/dev/null
unzip -qo "$ASSET_ZIP" -d "$ROOT/assets"
for file in young_caucasian_female.mhmat low-poly.mhclo eyebrow001.mhclo long01.mhclo female_casualsuit01.mhclo; do
  if ! find "$ROOT/assets" -type f -name "$file" -print -quit | grep -q .; then
    echo "::error::Missing CC0 MPFB asset: $file"
    exit 1
  fi
done
echo "[OK] Actual Blender and MPFB2 assets installed"
