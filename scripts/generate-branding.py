#!/usr/bin/env python3
"""
Generate branding files from branding.env configuration.

This script reads branding.env and generates:
- firefox/additions/browser/branding/{dir}/configure.sh
- firefox/additions/browser/branding/{dir}/locales/en-US/brand.ftl
- firefox/additions/browser/branding/{dir}/locales/en-US/brand.properties
- firefox/patches/camoufox-branding.patch

Usage:
    python3 scripts/generate-branding.py
"""

import os
import sys
from pathlib import Path


def load_branding_config(config_path: str = "branding.env") -> dict[str, str]:
    """Load branding configuration from branding.env file."""
    config = {}
    
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    # Validate required keys
    required = [
        'BRAND_SHORT_NAME', 'BRAND_FULL_NAME', 'BRAND_VENDOR',
        'APP_NAME', 'APP_PROFILE', 'BRANDING_DIR'
    ]
    missing = [k for k in required if k not in config]
    if missing:
        print(f"Error: Missing required config keys: {', '.join(missing)}")
        sys.exit(1)
    
    return config


def generate_configure_sh(config: dict[str, str], output_path: str):
    """Generate configure.sh for the branding directory."""
    content = f"""# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Note: MOZ_APP_VENDOR and MOZ_APP_PROFILE are set in patches/camoufox-branding.patch
# Firefox 142+ requires them to be set via imply_option() in browser/moz.configure

MOZ_APP_NAME={config['APP_NAME']}
MOZ_APP_BASENAME={config['BRAND_SHORT_NAME']}
MOZ_APP_DISPLAYNAME={config['BRAND_SHORT_NAME']}
MOZ_APP_REMOTINGNAME={config['APP_NAME']}
"""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"Generated: {output_path}")


def generate_brand_ftl(config: dict[str, str], output_path: str):
    """Generate brand.ftl localization file."""
    short = config['BRAND_SHORT_NAME']
    full = config['BRAND_FULL_NAME']
    vendor = config['BRAND_VENDOR']
    
    content = f"""# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

## Firefox Brand
##
## Firefox must be treated as a brand, and kept in English.
## It cannot be:
## - Declined to adapt to grammatical case.
## - Transliterated.
## - Translated.
##
## Reference: https://www.mozilla.org/styleguide/communications/translation/

-brand-shorter-name = {short}
-brand-short-name = {short}
-brand-full-name = {full}
-brand-shortcut-name = {short}
# This brand name can be used in messages where the product name needs to
# remain unchanged across different versions (Nightly, Beta, etc.).
-brand-product-name = {short}
-vendor-short-name = {vendor}
trademarkInfo = {{ " " }}
"""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"Generated: {output_path}")


def generate_brand_properties(config: dict[str, str], output_path: str):
    """Generate brand.properties localization file."""
    short = config['BRAND_SHORT_NAME']
    full = config['BRAND_FULL_NAME']
    vendor = config['BRAND_VENDOR']
    
    content = f"""# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

brandShorterName={short}
brandShortName={short}
brandFullName={full}
# LOCALIZATION NOTE(brandProductName):
# This brand name can be used in messages where the product name needs to
# remain unchanged across different versions (Nightly, Beta, etc.).
brandProductName={short}
vendorShortName={vendor}

syncBrandShortName={short} Sync
"""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"Generated: {output_path}")


def generate_branding_patch(config: dict[str, str], output_path: str):
    """Generate the camoufox-branding.patch file."""
    vendor = config['BRAND_VENDOR']
    profile = config['APP_PROFILE']
    
    content = f"""diff --git a/browser/moz.configure b/browser/moz.configure
index e8b401a7dfb2..b29b95e4fbda 100644
--- a/browser/moz.configure
+++ b/browser/moz.configure
@@ -13,7 +13,8 @@ imply_option("MOZ_NORMANDY", True)
 imply_option("MOZ_PROFILE_MIGRATOR", True)
 
 
-imply_option("MOZ_APP_VENDOR", "Mozilla")
+imply_option("MOZ_APP_VENDOR", "{vendor}")
+imply_option("MOZ_APP_PROFILE", "{profile}")
 imply_option("MOZ_APP_ID", "{{ec8030f7-c20a-464f-9b0e-13a3a9e97384}}")
 # Include the DevTools client, not just the server (which is the default)
 imply_option("MOZ_DEVTOOLS", "all")
"""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"Generated: {output_path}")


def generate_base_mozconfig(config: dict[str, str], output_path: str):
    """Update base.mozconfig with correct app-name and branding path."""
    
    # Read the existing mozconfig
    with open(output_path, 'r') as f:
        lines = f.readlines()
    
    # Update the relevant lines
    new_lines = []
    for line in lines:
        if line.strip().startswith('ac_add_options --with-app-name='):
            new_lines.append(f"ac_add_options --with-app-name={config['APP_NAME']}\n")
        elif line.strip().startswith('ac_add_options --with-branding='):
            new_lines.append(f"ac_add_options --with-branding=browser/branding/{config['BRANDING_DIR']}\n")
        else:
            new_lines.append(line)
    
    with open(output_path, 'w') as f:
        f.writelines(new_lines)
    print(f"Updated: {output_path}")


def main():
    # Change to repo root
    repo_root = Path(__file__).parent.parent
    os.chdir(repo_root)
    
    print("Loading branding configuration from branding.env...")
    config = load_branding_config()
    
    print(f"\nGenerating branding files for: {config['BRAND_SHORT_NAME']}")
    print(f"  Vendor: {config['BRAND_VENDOR']}")
    print(f"  App Name: {config['APP_NAME']}")
    print(f"  Branding Dir: {config['BRANDING_DIR']}")
    print()
    
    branding_dir = config['BRANDING_DIR']
    branding_path = f"firefox/additions/browser/branding/{branding_dir}"
    
    # Generate all branding files
    generate_configure_sh(config, f"{branding_path}/configure.sh")
    generate_brand_ftl(config, f"{branding_path}/locales/en-US/brand.ftl")
    generate_brand_properties(config, f"{branding_path}/locales/en-US/brand.properties")
    generate_branding_patch(config, "firefox/patches/camoufox-branding.patch")
    generate_base_mozconfig(config, "firefox/assets/base.mozconfig")
    
    print("\n✓ All branding files generated successfully!")
    print("\nNext steps:")
    print("  1. If in git workflow: run 'make copy-additions' to sync to source")
    print("  2. If updating baseline: run 'make retag-baseline' to update git tags")
    print("  3. Build with 'make build'")


if __name__ == "__main__":
    main()
