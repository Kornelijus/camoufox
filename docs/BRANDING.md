# Branding Configuration Guide

This guide explains how to customize Camoufox's browser branding for different use cases.

## Overview

Camoufox's branding is centralized in the `branding.env` configuration file. This makes it easy to:
1. **Reduce fingerprinting** by keeping Firefox branding when needed
2. **Create private forks** with custom branding
3. **Contribute improvements** back upstream without merge conflicts

## Configuration File: branding.env

All branding settings are in the root-level `branding.env` file:

```bash
# Product Names
BRAND_SHORT_NAME=Camoufox        # Short product name for UI
BRAND_FULL_NAME=Camoufox         # Full product name for about dialog
BRAND_VENDOR=Camoufox            # Vendor/Organization name

# Application Settings  
APP_NAME=camoufox                # Lowercase app identifier (binary name)
APP_PROFILE=camoufox             # Profile directory name (~/.APP_PROFILE)

# Branding Directory
BRANDING_DIR=camoufox            # Directory under browser/branding/
```

## Use Cases

### 1. Keep Firefox Branding (Stealth Mode)

To reduce fingerprinting surface area by appearing as standard Firefox:

```bash
# branding.env
BRAND_SHORT_NAME=Firefox
BRAND_FULL_NAME=Mozilla Firefox
BRAND_VENDOR=Mozilla

# Keep unique profile/app names to avoid conflicts
APP_NAME=camoufox
APP_PROFILE=camoufox
BRANDING_DIR=camoufox
```

**Result:**
- Browser window title: "Firefox" 
- About dialog: "Mozilla Firefox"
- Binary/profile: still `camoufox` (no conflict with real Firefox)
- WAF detection: Harder to distinguish from real Firefox

**Note:** User-Agent header is controlled separately via MaskConfig at runtime, not by these branding settings.

### 2. Custom Fork Branding

For private forks with unique branding:

```bash
# branding.env
BRAND_SHORT_NAME=MyBrowser
BRAND_FULL_NAME=MyBrowser Pro
BRAND_VENDOR=MyCompany

APP_NAME=mybrowser
APP_PROFILE=mybrowser
BRANDING_DIR=mybrowser
```

**Important:** You'll also need to:
1. Create `firefox/additions/browser/branding/mybrowser/` directory
2. Copy icon assets from `camoufox/` directory (or create custom ones)

## Applying Branding Changes

After editing `branding.env`, regenerate the branding files:

```bash
# Standalone generation
make generate-branding

# For git workflow (automatic during copy)
make copy-additions

# For updating baseline tag
make retag-baseline
```

The `generate-branding` target creates/updates:
- `firefox/additions/browser/branding/{dir}/configure.sh`
- `firefox/additions/browser/branding/{dir}/locales/en-US/brand.ftl`
- `firefox/additions/browser/branding/{dir}/locales/en-US/brand.properties`
- `firefox/patches/camoufox-branding.patch`
- `firefox/assets/base.mozconfig`

## What Gets Branded?

These settings affect:
- **Window title** and taskbar name
- **About dialog** text
- **Executable name** (binary filename)
- **Profile directory** location (e.g., `~/.camoufox/`)
- **MOZ_APP_VENDOR** (internal Firefox setting)

These settings do NOT affect:
- **User-Agent header**: Controlled by MaskConfig at runtime
- **navigator.userAgent**: Controlled by MaskConfig at runtime
- **Icon assets**: Stored in `firefox/additions/browser/branding/{dir}/`

## Advanced: Creating Custom Branding Assets

To create a completely new brand with custom icons:

1. Create new branding directory:
   ```bash
   mkdir -p firefox/additions/browser/branding/mybrowser/locales/en-US
   ```

2. Copy icon assets from camoufox:
   ```bash
   cp -r firefox/additions/browser/branding/camoufox/*.png \
         firefox/additions/browser/branding/camoufox/*.ico \
         firefox/additions/browser/branding/camoufox/*.icns \
         firefox/additions/browser/branding/mybrowser/
   ```

3. Copy required build files:
   ```bash
   cp firefox/additions/browser/branding/camoufox/moz.build \
      firefox/additions/browser/branding/camoufox/content \
      firefox/additions/browser/branding/mybrowser/
   ```

4. Update `branding.env`:
   ```bash
   BRANDING_DIR=mybrowser
   BRAND_SHORT_NAME=MyBrowser
   # ... etc
   ```

5. Generate branding files:
   ```bash
   make generate-branding
   ```

## Troubleshooting

### Running tests

To verify the branding system works correctly:
```bash
python3 tests/test_branding.py
```

This tests:
- Default Camoufox branding generation
- Firefox stealth branding generation
- All generated files contain correct values

### "Directory not found" errors

If you change `BRANDING_DIR`, ensure the directory exists:
```bash
ls firefox/additions/browser/branding/$BRANDING_DIR/
```

### Profile conflicts

If using `APP_PROFILE=firefox`, Firefox and Camoufox would share profiles. Keep unique profile names to avoid this.

### Changes not taking effect

After changing `branding.env`:
1. Run `make generate-branding`
2. Run `make copy-additions` (if using git workflow)
3. Rebuild: `make build`

## Contributing Back Upstream

When contributing from a private fork:
1. Keep local changes to `branding.env` only
2. Don't commit generated files in `firefox/additions/` and `firefox/patches/`
3. Contributors can regenerate branding from your `branding.env`
4. Focus pull requests on functional improvements, not branding

This allows forks to maintain unique branding while still contributing code improvements back to Camoufox.

## Real-World Examples

### Example 1: Reduce Fingerprinting (Issue #1 from RFC)

**Problem:** When Firefox forks upgraded from Firefox 135 → 140, the User-Agent header exposed custom branding like "Camoufox" instead of "Firefox", making them trivial to detect by WAFs like DataDome and Cloudflare.

**Solution:** Use Firefox branding in UI while keeping unique internal app paths:

```bash
# branding.env
BRAND_SHORT_NAME=Firefox
BRAND_FULL_NAME=Mozilla Firefox  
BRAND_VENDOR=Mozilla

# Keep unique to avoid conflicts
APP_NAME=camoufox
APP_PROFILE=camoufox
BRANDING_DIR=camoufox
```

Then regenerate:
```bash
make generate-branding
make copy-additions  # If using git workflow
make build
```

**Result:** 
- Window title shows "Firefox"
- About dialog shows "Mozilla Firefox"
- Binary remains `camoufox` (no conflict with real Firefox)
- Profile stored in `~/.camoufox/` (no conflict)
- WAFs see standard Firefox branding, reducing detection surface

**Note:** Runtime User-Agent is controlled separately via MaskConfig, not by branding files.

### Example 2: Private Fork Collaboration (Issue #2 from RFC)

**Problem:** Multiple teams fork Camoufox for internal use with custom branding. When they improve the codebase, contributing back creates merge conflicts in hardcoded branding files.

**Solution:** Each fork customizes only `branding.env`:

```bash
# Fork A's branding.env
BRAND_SHORT_NAME=InternalBrowser
BRAND_FULL_NAME=InternalBrowser Pro
BRAND_VENDOR=CompanyA
APP_NAME=internalbrowser
APP_PROFILE=internalbrowser
BRANDING_DIR=internalbrowser
```

When Fork A fixes a bug or adds a feature:
1. They commit functional changes (patches, code, etc.)
2. They DON'T commit generated branding files
3. They open a PR to upstream Camoufox
4. Upstream maintainers merge without conflicts (branding.env differs but that's expected)
5. Fork A can later pull upstream updates without branding conflicts

**Workflow:**
```bash
# Fork maintainer
git checkout -b fix-webgl-leak
# ... make fixes to patches/webgl-spoofing.patch ...
git add patches/webgl-spoofing.patch
git commit -m "Fix WebGL parameter leak in headless mode"
git push origin fix-webgl-leak
# Open PR to upstream

# Upstream can merge cleanly because branding.env isn't changed
# Fork can pull updates and regenerate their branding
git pull upstream main
make generate-branding  # Regenerates fork's branding
```

This pattern enables a healthy ecosystem of forks that contribute improvements back upstream.
