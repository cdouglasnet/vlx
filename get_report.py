#!/usr/bin/env python3
# encoding: utf-8
#
# VLX Fast Access - Alfred Workflow
# Run Script: Generate and retrieve inspection report URL
#

import sys
import json
import os
import urllib.request
import urllib.error


def get_env(key, default=""):
    return os.environ.get(key, default)


def main():
    inspection_id = get_env("id", "")
    if not inspection_id:
        inspection_id = sys.argv[1].strip() if len(sys.argv) > 1 else ""

    api_key = get_env("API_KEY")

    if not api_key:
        sys.stderr.write("API Key not configured. Set API_KEY in Alfred workflow configuration.\n")
        sys.exit(1)

    if not inspection_id:
        sys.stderr.write("No inspection ID provided.\n")
        sys.exit(1)

    url = "https://api.visualogyx.com/v1/inspection/report"
    headers = {
        "access-token": api_key,
        "Content-Type": "application/json",
    }
    payload = json.dumps({"inspection_id": inspection_id}).encode("utf-8")

    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.stderr.write("API Error: " + str(e.code) + "\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write("Error connecting to VLX: " + str(e) + "\n")
        sys.exit(1)

    report_url = data.get("report_url", data.get("url", ""))
    if not report_url:
        sys.stderr.write("No report URL found in response.\n")
        sys.exit(1)

    print(report_url)


if __name__ == "__main__":
    main()
