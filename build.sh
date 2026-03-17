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

# Copy workflow library (for Keychain support)
if [ -d "workflow" ]; then
    rsync -a --exclude='__pycache__' --exclude='*.pyc' workflow/ "$BUILD_DIR/workflow/"
    echo "  Copied workflow library"
fi

# Copy images
cp *.png "$BUILD_DIR/" 2>/dev/null || true

# Copy documentation files
cp README.md "$BUILD_DIR/" 2>/dev/null || true

# Copy info.plist
cp info.plist "$BUILD_DIR/"

# Replace version placeholder
sed -i '' "s|REPLACE_VERSION_HERE|$VERSION|g" "$BUILD_DIR/info.plist"
echo "  Set version to $VERSION"

# Inject about.md content into info.plist (replacing REPLACE_README_HERE placeholder)
if [ -f "about.md" ]; then
    # Read about.md and escape special XML characters
    ABOUT_CONTENT=$(cat about.md | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g' | tr '\n' '\r' | sed 's/\r/\\n/g' | sed 's/\\n$//')
    # Replace the placeholder in info.plist
    sed -i '' "s|REPLACE_README_HERE|$ABOUT_CONTENT|g" "$BUILD_DIR/info.plist"
    echo "  Injected about.md content into info.plist"
fi


# Copy List Filter Images directory
rsync -a --exclude='.DS_Store' "List Filter Images/" "$BUILD_DIR/List Filter Images/" 2>/dev/null || true

# Create the .alfredworkflow file (just a zip)
cd "$BUILD_DIR"
zip -r "$OLDPWD/$WORKFLOW_NAME.alfredworkflow" .

# Keep build directory for inspection
BUILD_OUTPUT_DIR="$OLDPWD/.build_output"
rm -rf "$BUILD_OUTPUT_DIR"
cp -r "$BUILD_DIR" "$BUILD_OUTPUT_DIR"

# Cleanup temp directory (but keep our inspection copy)
rm -rf "$TEMP_DIR"

echo "✓ Built $WORKFLOW_NAME.alfredworkflow"
echo "  Version: $VERSION"
echo "  Location: $OLDPWD/$WORKFLOW_NAME.alfredworkflow"
echo ""
echo "DEBUG: Build contents preserved in: $BUILD_OUTPUT_DIR"
echo "Contents:"
ls -lah "$BUILD_OUTPUT_DIR/" | grep -v "^total" | awk '{print "  " $0}'

