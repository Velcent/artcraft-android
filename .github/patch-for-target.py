#!/usr/bin/env python3
"""Patch build-common.sh to support --target for non-aarch64 ABIs."""
import sys

path = "lib/build-common.sh"
target = sys.argv[1] if len(sys.argv) > 1 else ""

if not target:
    print("No target specified, skipping patch")
    sys.exit(0)

with open(path, "r") as f:
    content = f.read()

# Patch 1: release build command
old_release = '"${APK_CMD[@]}" --release 2>&1'
new_release = '"${APK_CMD[@]}" --release --target "' + target + '" 2>&1'
content = content.replace(old_release, new_release)

# Patch 2: debug build command
old_debug = '"${APK_CMD[@]}" 2>&1'
new_debug = '"${APK_CMD[@]}" --target "' + target + '" 2>&1'
content = content.replace(old_debug, new_debug)

# Patch 3: skip the aarch64-only rustup check so x86_64 builds also work
old_check = """if command -v rustup >/dev/null 2>&1 && ! rustup target list --installed | grep -qx 'aarch64-linux-android'; then
    fail "Rust target is missing. Install it once with: rustup target add aarch64-linux-android"
fi"""
new_check = """# Target check disabled for CI multi-ABI builds.
# if command -v rustup >/dev/null 2>&1 && ! rustup target list --installed | grep -qx 'aarch64-linux-android'; then
#     fail "Rust target is missing."
# fi
"""
content = content.replace(old_check, new_check)

with open(path, "w") as f:
    f.write(content)

print(f"Patched {path} for target: {target}")
print("Changes made:")
print("  1. cargo apk build now passes --target")
print("  2. aarch64-only rustup check disabled")
