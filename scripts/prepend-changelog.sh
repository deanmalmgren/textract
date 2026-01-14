#!/bin/bash
# Non-destructive changelog update using commitizen
# Generates new entries and prepends them to the existing changelog
#
# Usage:
#   ./scripts/prepend-changelog.sh        # After cz bump, adds the new version section
#   ./scripts/prepend-changelog.sh --preview  # Preview unreleased changes before bumping

set -e

PREVIEW_MODE=false
if [ "$1" = "--preview" ] || [ "$1" = "-p" ]; then
    PREVIEW_MODE=true
fi

CHANGELOG="docs/changelog.rst"
BACKUP="docs/changelog.rst.backup"
TEMP_FULL="/tmp/cz-changelog-full.rst"
TEMP_NEW="/tmp/cz-changelog-new.rst"
TEMP_MERGED="/tmp/cz-changelog-merged.rst"

# Get current version from pyproject.toml
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | head -1 | sed 's/version = "\(.*\)"/\1/')

# Find the latest version in existing changelog (first version number found after "next release")
LATEST_IN_CHANGELOG=$(grep -E '^[0-9]+\.[0-9]+\.[0-9]+' "$CHANGELOG" | head -1 | tr -d '[:space:]')

if $PREVIEW_MODE; then
    echo "=== Preview Mode: Unreleased Changes ==="
    echo ""
    uv run cz changelog --dry-run | head -50
    echo ""
    echo "To add these to changelog after bumping:"
    echo "  uv run cz bump --increment PATCH  # or MINOR, MAJOR"
    echo "  ./scripts/prepend-changelog.sh"
    exit 0
fi

echo "Current version (pyproject.toml): $CURRENT_VERSION"
echo "Latest version in changelog: $LATEST_IN_CHANGELOG"

# Check if we just bumped (current version not in changelog yet)
if [ "$CURRENT_VERSION" = "$LATEST_IN_CHANGELOG" ]; then
    echo ""
    echo "Warning: Current version $CURRENT_VERSION is already in changelog."
    echo "Did you forget to run 'cz bump' first?"
    echo ""
    echo "To preview unreleased changes: $0 --preview"
    exit 1
fi

echo "Backing up $CHANGELOG to $BACKUP..."
cp "$CHANGELOG" "$BACKUP"

echo "Generating full changelog with commitizen..."
uv run cz changelog --file-name "$TEMP_FULL"

echo "Extracting new version section ($CURRENT_VERSION)..."
# Extract everything from start until we hit the latest version that's already in the changelog
awk "/^$LATEST_IN_CHANGELOG/,0 {exit} 1" "$TEMP_FULL" > "$TEMP_NEW"

# Check if we actually got new content
if [ ! -s "$TEMP_NEW" ]; then
    echo "Error: No new content generated. This shouldn't happen."
    rm -f "$TEMP_FULL" "$TEMP_NEW"
    exit 1
fi

echo "Merging new entries with original changelog..."
{
    cat "$TEMP_NEW"
    cat "$BACKUP"
} > "$TEMP_MERGED"

echo "Updating $CHANGELOG..."
mv "$TEMP_MERGED" "$CHANGELOG"

# Cleanup
rm -f "$TEMP_FULL" "$TEMP_NEW"

echo ""
echo "✓ Successfully updated changelog!"
echo "  - Added version $CURRENT_VERSION to $CHANGELOG"
echo "  - Original backed up to $BACKUP"
echo ""
echo "Review the changes:"
echo "  diff $BACKUP $CHANGELOG | head -50"
echo ""
echo "If satisfied, commit and remove backup:"
echo "  git add $CHANGELOG"
echo "  rm $BACKUP"
