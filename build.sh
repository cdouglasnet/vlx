#!/bin/bash
# Build script for VLX Alfred Workflow

WORKFLOW_NAME="VLX"
BUNDLE_ID="net.cdoug.vlx"

echo "Building $WORKFLOW_NAME..."

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

# Copy List Filter Images directory
rsync -a --exclude='.DS_Store' "List Filter Images/" "$BUILD_DIR/List Filter Images/" 2>/dev/null || true

# Create the .alfredworkflow file (just a zip)
cd "$BUILD_DIR"
zip -r "$OLDPWD/$WORKFLOW_NAME.alfredworkflow" .

# Cleanup
rm -rf "$TEMP_DIR"

echo "✓ Built $WORKFLOW_NAME.alfredworkflow"
echo "  Location: $OLDPWD/$WORKFLOW_NAME.alfredworkflow"

