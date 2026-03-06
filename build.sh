#!/bin/bash
# Build script for VLX Alfred Workflow

WORKFLOW_NAME="VLX"
BUNDLE_ID="net.cdoug.vlx"
VERSION="0.0.1"

echo "Building $WORKFLOW_NAME v$VERSION..."

# Create temp directory
TEMP_DIR=$(mktemp -d)
BUILD_DIR="$TEMP_DIR/$WORKFLOW_NAME"

# Copy all necessary files
mkdir -p "$BUILD_DIR"

# Copy Python files
cp *.py "$BUILD_DIR/" 2>/dev/null || true

# Copy images
cp *.png "$BUILD_DIR/" 2>/dev/null || true

# Copy info.plist
cp info.plist "$BUILD_DIR/"

# Update version in info.plist on line 841 (the <string> after <key>version</key>)
sed -i '' '841s/<string>.*<\/string>/<string>'"$VERSION"'<\/string>/' "$BUILD_DIR/info.plist"

# Copy List Filter Images directory
rsync -a --exclude='.DS_Store' "List Filter Images/" "$BUILD_DIR/List Filter Images/" 2>/dev/null || true

# Create the .alfredworkflow file (just a zip)
cd "$BUILD_DIR"
zip -r "$OLDPWD/$WORKFLOW_NAME.alfredworkflow" .

# Cleanup
rm -rf "$TEMP_DIR"

echo "✓ Built $WORKFLOW_NAME.alfredworkflow"
echo "  Version: $VERSION"
echo "  Location: $OLDPWD/$WORKFLOW_NAME.alfredworkflow"

