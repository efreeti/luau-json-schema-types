#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .tools
luau_version=0.741
wally_version=0.3.2
case "$(uname -s)" in
  Linux) platform=linux; luau_platform=ubuntu ;;
  Darwin) platform=macos; luau_platform=macos ;;
  *) echo 'Use the official Luau and Wally Windows releases.' >&2; exit 1 ;;
esac
if [[ "$platform" == macos && "$(uname -m)" == x86_64 ]]; then
  # Luau's 0.741 macOS binaries target ARM; build the CLI tools for Intel Macs.
  curl -fsSL "https://github.com/luau-lang/luau/archive/refs/tags/$luau_version.tar.gz" -o .tools/luau.tar.gz
  mkdir -p .tools/source
  tar -xzf .tools/luau.tar.gz -C .tools/source --strip-components=1
  cmake -S .tools/source -B .tools/build -DCMAKE_BUILD_TYPE=Release -DLUAU_BUILD_TESTS=OFF
  cmake --build .tools/build --target Luau.Repl.CLI Luau.Analyze.CLI -j 4
  cp .tools/build/luau .tools/build/luau-analyze .tools/
else
  curl -fsSL "https://github.com/luau-lang/luau/releases/download/$luau_version/luau-$luau_platform.zip" -o .tools/luau.zip
  unzip -oq .tools/luau.zip -d .tools
fi
curl -fsSL "https://github.com/UpliftGames/wally/releases/download/v$wally_version/wally-v$wally_version-$platform.zip" -o .tools/wally.zip
unzip -oq .tools/wally.zip -d .tools
chmod +x .tools/luau .tools/luau-analyze .tools/wally
