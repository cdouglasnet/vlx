#!/usr/bin/env python3
# encoding: utf-8
#
# VLX Fast Access - Alfred Workflow
# Configuration storage - saves API key to macOS Keychain
#

import sys
import os
import subprocess

# Service name for Keychain storage
KEYCHAIN_SERVICE = "net.cdoug.vlx"
KEYCHAIN_ACCOUNT = "vlxAPI"


def save_password(account, password, service=KEYCHAIN_SERVICE):
    """Save password to macOS Keychain using security command."""
    # First try to delete any existing password
    try:
        subprocess.run(
            ['security', 'delete-generic-password', '-s', service, '-a', account],
            capture_output=True,
            check=False
        )
    except Exception:
        pass

    # Add the new password
    result = subprocess.run(
        ['security', 'add-generic-password', '-s', service, '-a', account, '-w', password],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(result.stderr.strip() or "Failed to save to Keychain")


def main():
    """Main entry point - saves API key to Keychain."""
    # Get the API key from the argument (passed from config.py)
    api_key = sys.argv[1].strip() if len(sys.argv) > 1 else ""

    # Also check for environment variable set by Alfred
    if not api_key:
        api_key = os.environ.get('api_key', '').strip()

    if not api_key:
        print("No API key provided")
        return

    try:
        # Save the new API key to Keychain
        save_password(KEYCHAIN_ACCOUNT, api_key)
        print("API Key saved successfully")

    except Exception as e:
        print("Error saving API key: " + str(e))


if __name__ == "__main__":
    main()


