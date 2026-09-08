#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXT_DIR="$ROOT_DIR/extension"
DIST_DIR="$ROOT_DIR/dist"

# Generate and validate snippets before changing the package version.
python3 "$EXT_DIR/tools/build_snippets.py"

# Make sure dist/ exists.
mkdir -p "$DIST_DIR"

pushd "$EXT_DIR" > /dev/null

# Bump the patch version (for example 0.0.14 -> 0.0.15).
npm version patch --no-git-tag-version

# Build the VSIX package.
vsce package --no-yarn

# Move the package to dist/.
mv ./*.vsix "$DIST_DIR/"

popd > /dev/null

echo "Done. The package is in $DIST_DIR/"
