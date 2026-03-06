# Release Process

This document describes how to create a new release of the VLX Fast Access Alfred Workflow.

## Automated Release Process

The workflow automatically creates releases when changes are pushed to specific branches:
- **Production releases**: When pushed to `main` or `master` branch
- **Beta releases**: When pushed to `beta` branch

### Steps to Create a Production Release

1. **Update Version Number**
   ```bash
   # Update version in info.plist
   plutil -replace version -string "1.1.0" info.plist
   
   # Verify the change
   plutil -extract version raw info.plist
   ```

2. **Update README Badge (if present)**
   - Edit README.md and update any version badges to match

3. **Commit Version Changes**
   ```bash
   git add info.plist README.md
   git commit -m "Bump version to 1.1.0"
   ```

4. **Push to Main Branch**
   
   **Option A: Direct Push** (if you have permissions)
   ```bash
   git push origin main
   ```
   
   **Option B: Pull Request** (recommended)
   ```bash
   git push origin your-feature-branch
   # Create PR, get approval, merge to main
   ```

5. **Automatic Release Process**
   When code is pushed/merged to main/master:
   - GitHub Actions automatically builds `VLX.alfredworkflow`
   - Checks if version was already released
   - If version is new, creates a GitHub Release
   - Generates changelog from git commits
   - Attaches the `.alfredworkflow` file to the release

6. **Monitor Release**
   - Go to [Actions tab](../../actions)
   - Watch the "Production Release" workflow
   - Once complete, check [Releases page](../../releases)

### Steps to Create a Beta Release

Beta releases are useful for testing before production:

1. **Create/Switch to Beta Branch**
   ```bash
   git checkout -b beta
   # or
   git checkout beta
   ```

2. **Update Version (Optional)**
   ```bash
   plutil -replace version -string "1.1.0" info.plist
   ```

3. **Commit and Push**
   ```bash
   git add .
   git commit -m "Beta: New feature description"
   git push origin beta
   ```

4. **Automatic Beta Release**
   - GitHub Actions builds the workflow
   - Creates a pre-release with timestamp (e.g., `v1.1.0-beta-20260306123456`)
   - Marked as "Pre-release" on GitHub
   - Not shown as the latest release

## Manual Release Process

If the automated process fails, you can create a release manually:

1. **Build Locally**
   ```bash
   ./build.sh
   ```

2. **Verify Build**
   ```bash
   unzip -t VLX.alfredworkflow
   unzip -l VLX.alfredworkflow | head
   ```

3. **Create Release on GitHub**
   - Go to [Releases page](../../releases)
   - Click "Draft a new release"
   - Create/choose your tag (e.g., `v1.1.0`)
   - Title: "VLX Fast Access v1.1.0"
   - Upload the `VLX.alfredworkflow` file
   - Add release notes (describe changes)
   - Check "Set as the latest release" for production
   - Check "Pre-release" for beta versions
   - Publish release

## Version Numbering

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR** (1.x.x): Breaking changes, major rewrites
- **MINOR** (x.1.x): New features, non-breaking changes
- **PATCH** (x.x.1): Bug fixes, minor improvements

Examples:
- `1.0.0` - Initial release
- `1.1.0` - Added pagination support
- `1.1.1` - Fixed UTF-8 encoding bug
- `2.0.0` - Complete API v2 rewrite (breaking)

## Pre-release Checklist

Before creating a release:

- [ ] Build succeeds: `./build.sh`
- [ ] Workflow installs correctly in Alfred
- [ ] All features work as expected
- [ ] No API keys or sensitive data in code
- [ ] info.plist version updated
- [ ] README.md updated (if needed)
- [ ] All changes committed
- [ ] Scripts have proper error handling
- [ ] UTF-8 encoding handled correctly

## Post-release Tasks

After releasing:

1. **Test the Release**
   - Download the `.alfredworkflow` from the release
   - Install in Alfred
   - Test core functionality (search, report generation)

2. **Announce the Release** (if major)
   - Update documentation sites
   - Post in relevant communities
   - Share on social media

3. **Monitor Issues**
   - Watch for bug reports
   - Be ready to create a hotfix release if needed

## Hotfix Process

For critical bugs in production:

1. **Create Hotfix Branch**
   ```bash
   git checkout main
   git checkout -b hotfix/1.0.1
   ```

2. **Fix the Bug**
   ```bash
   # Make your fixes
   git add .
   git commit -m "Hotfix: Fix critical API error"
   ```

3. **Update Version**
   ```bash
   # Bump patch version
   plutil -replace version -string "1.0.1" info.plist
   git add info.plist
   git commit -m "Bump version to 1.0.1"
   ```

4. **Merge and Release**
   ```bash
   git checkout main
   git merge hotfix/1.0.1
   git push origin main
   # Automatic release will trigger
   ```

## Troubleshooting

### "Version Already Released" Message

The workflow won't create duplicate releases. To release:
1. Increment the version number in `info.plist`
2. Commit and push again

### Build Fails in GitHub Actions

Check the Actions logs for errors:
1. Go to [Actions tab](../../actions)
2. Click on the failed workflow run
3. Click on the "build" job
4. Review the error messages

Common issues:
- Syntax errors in Python scripts
- Invalid `info.plist` format
- Missing files referenced in `build.sh`

### Workflow Won't Install

If the built workflow won't install:
1. Test locally: `./build.sh && open VLX.alfredworkflow`
2. Verify zip structure: `unzip -l VLX.alfredworkflow | head`
3. Check `info.plist`: `plutil -lint info.plist`

## GitHub Actions Workflows

### production-release.yml
- Triggers: Push to `main` or `master`
- Creates: Production releases
- Tag format: `v1.0.0`

### beta-release.yml
- Triggers: Push to `beta`
- Creates: Pre-releases
- Tag format: `v1.0.0-beta-20260306123456`

### pr-build.yml
- Triggers: Pull requests
- Creates: Build artifacts (no release)
- Purpose: Verify builds succeed

### test.yml
- Triggers: Push/PR to any main branch
- Creates: Nothing
- Purpose: Run linting and tests

## Release History Example

```
v1.2.0 (2026-03-15) - Latest
  - Added pagination support
  - Improved error handling
  - Updated to VLX API v2

v1.1.0 (2026-02-10)
  - Added report generation
  - Menu navigation improvements

v1.0.1 (2026-01-20)
  - Fixed UTF-8 encoding issue
  - Better error messages

v1.0.0 (2026-01-01)
  - Initial release
```

## Tips

- **Test before releasing**: Always test the built workflow before pushing to main
- **Use beta releases**: For experimental features, use the beta branch first
- **Keep versions incremental**: Don't skip version numbers
- **Document changes**: Clear commit messages help with automatic changelogs
- **Check Actions**: Monitor GitHub Actions to catch issues early

