#!/usr/bin/env python3

"""
Centralized constants for Camoufox build scripts.
"""

from enum import StrEnum
from pathlib import Path
import os

SCRIPTS_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = SCRIPTS_DIR.parent

BUNDLE_DIR = ROOT_DIR / "firefox" / "bundle"
ASSETS_DIR = ROOT_DIR / "firefox" / "assets"
PATCHES_DIR = ROOT_DIR / "firefox" / "patches"

FIREFOX_VERSION = os.getenv("FIREFOX_VERSION")
CAMOUFOX_RELEASE = os.getenv("CAMOUFOX_RELEASE", "dev")

CAMOUFOX_BUILD_NAME = f"camoufox-{FIREFOX_VERSION}-{CAMOUFOX_RELEASE}"
CAMOUFOX_SRC_DIR = ROOT_DIR / CAMOUFOX_BUILD_NAME


class BuildTarget(StrEnum):
    LINUX = "linux"
    WINDOWS = "windows"
    MACOS = "macos"


class BuildArch(StrEnum):
    X86_64 = "x86_64"
    ARM64 = "arm64"
    I686 = "i686"


AVAILABLE_TARGETS = [target.value for target in BuildTarget]
AVAILABLE_ARCHS = [arch.value for arch in BuildArch]

# Package configuration
PACKAGE_FILE_EXTENSIONS = {
    BuildTarget.LINUX: "tar.xz",
    BuildTarget.MACOS: "dmg",
    BuildTarget.WINDOWS: "zip",
}
PACKAGE_REMOVE_PATHS = {
    "uninstall",
    "pingsender.exe",
    "pingsender",
    "vaapitest",
    "glxtest",
}
