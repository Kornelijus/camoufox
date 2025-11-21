# Quick Start: Branding Configuration

This guide shows how to quickly customize Camoufox branding for common scenarios.

## Use Case 1: Stealth Mode (Keep Firefox Branding)

**Why:** Reduce fingerprinting surface by appearing as standard Firefox. Some WAFs detect custom browser names in User-Agent strings.

**How:**
```bash
# Edit branding.env
cat > branding.env << 'EOF'
BRAND_SHORT_NAME=Firefox
BRAND_FULL_NAME=Mozilla Firefox
BRAND_VENDOR=Mozilla
APP_NAME=camoufox
APP_PROFILE=camoufox
BRANDING_DIR=camoufox
EOF

# Generate branding files
make generate-branding

# Apply to source tree (if using git workflow)
make copy-additions

# Build
make build
```

**Result:** Browser appears as "Firefox" in UI, but uses separate profile directory to avoid conflicts.

## Use Case 2: Custom Fork Branding

**Why:** Create a distinct brand for internal use or private distribution.

**How:**
```bash
# Edit branding.env
cat > branding.env << 'EOF'
BRAND_SHORT_NAME=MyBrowser
BRAND_FULL_NAME=MyBrowser Enterprise
BRAND_VENDOR=MyCompany
APP_NAME=mybrowser
APP_PROFILE=mybrowser
BRANDING_DIR=mybrowser
EOF

# Create branding directory with icons
mkdir -p firefox/additions/browser/branding/mybrowser
cp -r firefox/additions/browser/branding/camoufox/* \
      firefox/additions/browser/branding/mybrowser/

# Generate branding files
make generate-branding

# Apply and build
make copy-additions
make build
```

## Use Case 3: Restore Default Camoufox Branding

**How:**
```bash
cat > branding.env << 'EOF'
BRAND_SHORT_NAME=Camoufox
BRAND_FULL_NAME=Camoufox
BRAND_VENDOR=Camoufox
APP_NAME=camoufox
APP_PROFILE=camoufox
BRANDING_DIR=camoufox
EOF

make generate-branding
```

## Testing Your Changes

```bash
# Run automated tests
python3 tests/test_branding.py

# Verify generated files
cat firefox/additions/browser/branding/camoufox/configure.sh
cat firefox/additions/browser/branding/camoufox/locales/en-US/brand.ftl
```

## What Gets Changed?

The branding configuration affects:
- Window title and taskbar name
- About dialog text
- Binary executable name
- Profile directory location
- MOZ_APP_VENDOR (internal Firefox setting)

It does NOT affect:
- User-Agent header (controlled by MaskConfig at runtime)
- navigator.userAgent (controlled by MaskConfig at runtime)

## Full Documentation

See [BRANDING.md](BRANDING.md) for complete documentation including:
- All configuration options
- Advanced customization
- Real-world examples
- Troubleshooting
- Contributing guidelines
