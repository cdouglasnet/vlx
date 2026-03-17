#!/usr/bin/env python3
# encoding: utf-8
#
# VLX Fast Access - Alfred Workflow
# Configuration management
#

import sys
import json
import subprocess
import re

# Service name for Keychain storage (must match configStore.py)
KEYCHAIN_SERVICE = "net.cdoug.vlx"
KEYCHAIN_ACCOUNT = "vlxAPI"

# Configuration names mapping
confNames = {
    'confApi': 'apiKey',
}


def get_password(account, service=KEYCHAIN_SERVICE):
    """Get password from macOS Keychain using security command."""
    result = subprocess.run(
        ['security', 'find-generic-password', '-s', service, '-a', account, '-g'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None

    # Parse the output - password is in stderr in format: password: "value"
    match = re.search(r'password:\s*(?:0x[0-9A-F]+\s*)?"(.+)"', result.stderr)
    if match:
        return match.group(1)

    # Try hex format
    match = re.search(r'password:\s*0x([0-9A-F]+)', result.stderr)
    if match:
        try:
            return bytes.fromhex(match.group(1)).decode('utf-8')
        except Exception:
            pass

    return None


def maskApiKey(apiKey):
    """Masks an API key for security display, showing only first 4 and last 4 characters.

    Args:
        apiKey (str): The API key to mask

    Returns:
        str: Masked API key (e.g., "pk_3****MD3G" for short keys)
    """
    if not apiKey:
        return ''

    if len(apiKey) <= 8:
        # For very short keys, show first 2 and last 2 with asterisks
        return apiKey[:2] + '****' + apiKey[-2:]
    elif len(apiKey) <= 12:
        # For short keys, show first 4 and last 4 with asterisks
        return apiKey[:4] + '****' + apiKey[-4:]
    else:
        # For long keys, show first 8, asterisks, and last 4
        return apiKey[:8] + '*' * 16 + apiKey[-4:]


def getConfigValue(configName):
    """Gets a configuration value from Keychain.

    Args:
        configName (str): The name of the configuration item

    Returns:
        str: The configuration value or None if not found
    """
    if configName == confNames['confApi']:
        return get_password(KEYCHAIN_ACCOUNT)
    return None


def main():
    """Main configuration interface."""

    # Get query from command line args
    query = sys.argv[1].strip() if len(sys.argv) > 1 else ""

    items = []

    if not query:
        # Show main config menu
        apiKeyValue = getConfigValue(confNames['confApi'])
        maskedApiKey = maskApiKey(apiKeyValue)

        items.append({
            "title": ('*' if not apiKeyValue else '') + 'Set API key' + (' (' + maskedApiKey + ')' if maskedApiKey else ''),
            "subtitle": "Your VLX API key/token. (Required)",
            "valid": False,
            "autocomplete": confNames['confApi'] + ' ',
            "icon": {"path": "icon.png" if apiKeyValue else "List Filter Images/question.png"}
        })

    elif query.startswith(confNames['confApi'] + ' ') or query == confNames['confApi']:
        # User is entering API key
        userInput = query.replace(confNames['confApi'] + ' ', '').replace(confNames['confApi'], '')
        maskedInput = maskApiKey(userInput) if userInput else ''

        if userInput:
            items.append({
                "title": "Save API key: " + maskedInput,
                "subtitle": "Press Enter to save to keychain",
                "valid": True,
                "arg": userInput,
                "variables": {
                    "config_action": "save_api_key"
                }
            })
        else:
            items.append({
                "title": "Enter your VLX API key...",
                "subtitle": "Type your API key and press Enter to save",
                "valid": False
            })
    else:
        # Unknown query
        items.append({
            "title": "Unknown configuration option",
            "subtitle": "Type 'vlx:config' to see available options",
            "valid": False
        })

    output = {"items": items}
    print(json.dumps(output))


if __name__ == "__main__":
    main()


