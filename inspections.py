#!/usr/bin/env python3
# encoding: utf-8
#
# VLX Fast Access - Alfred Workflow
# Script Filter: Search inspections via VLX API
#

import sys
import json
import os
import urllib.request
import urllib.parse
import urllib.error


def get_env(key, default=""):
    return os.environ.get(key, default)


def main():
    query = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    api_key = get_env("API_KEY")

    if not api_key:
        output = {
            "items": [
                {
                    "title": "API Key not configured",
                    "subtitle": "Set API_KEY in Alfred workflow configuration",
                    "valid": False,
                    "icon": {"path": "icon.png"},
                }
            ]
        }
        print(json.dumps(output))
        return

    url = "https://api.visualogyx.com/v1/inspections?page=1&page_size=10"
    headers = {
        "access-token": api_key,
        "Content-Type": "application/json",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        output = {
            "items": [
                {
                    "title": "API Error: " + str(e.code),
                    "subtitle": "Check your API key and try again",
                    "valid": False,
                }
            ]
        }
        print(json.dumps(output))
        return
    except Exception as e:
        output = {
            "items": [
                {
                    "title": "Error connecting to VLX",
                    "subtitle": str(e),
                    "valid": False,
                }
            ]
        }
        print(json.dumps(output))
        return

    inspections = data if isinstance(data, list) else data.get("inspections", data.get("data", []))

    items = []
    for inspection in inspections:
        inspection_id = str(inspection.get("id", ""))
        title = inspection.get("name", inspection.get("title", "Untitled Inspection"))
        status = inspection.get("status", "")
        location = inspection.get("location", inspection.get("address", ""))
        description = inspection.get("description", "")
        created_by = inspection.get("created_by", inspection.get("inspector", ""))
        if isinstance(created_by, dict):
            created_by = created_by.get("name", created_by.get("email", ""))
        date = inspection.get("created_at", inspection.get("date", ""))
        if date and "T" in date:
            date = date.split("T")[0]

        subtitle_parts = []
        if status:
            subtitle_parts.append("Status: " + status)
        if created_by:
            subtitle_parts.append("By: " + created_by)
        if date:
            subtitle_parts.append("Date: " + date)
        if location:
            subtitle_parts.append("Location: " + location)
        if description:
            subtitle_parts.append("Desc: " + description[:80])
        subtitle = " | ".join(subtitle_parts) if subtitle_parts else "VLX Inspection"

        match_text = " ".join(filter(None, [title, description, location, status]))

        if query and query.lower() not in match_text.lower():
            continue

        item = {
            "title": title,
            "subtitle": subtitle,
            "arg": inspection_id,
            "valid": True,
            "variables": {
                "id": inspection_id,
                "title": title,
                "status": status,
                "date": date,
                "location": location,
                "description": description,
            },
        }
        items.append(item)

    if not items:
        items.append(
            {
                "title": "No inspections found",
                "subtitle": "Try a different search query or check your API key",
                "valid": False,
            }
        )

    output = {"items": items}
    print(json.dumps(output))


if __name__ == "__main__":
    main()
