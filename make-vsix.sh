#!/usr/bin/env bash
set -euo pipefail

# directories
EXT_DIR="extension"
DIST_DIR="dist"

# make sure dist/ exists
mkdir -p "$DIST_DIR"

# bump patch version (0.0.1 -> 0.0.2)
pushd "$EXT_DIR" > /dev/null
npm version patch --no-git-tag-version

# build package
vsce package --no-yarn

# move .vsix to dist/
mv ./*.vsix "../$DIST_DIR/"
popd > /dev/null

echo "✅ Done! The package is in $DIST_DIR/"
