#!/usr/bin/env python
# /// script
# dependencies = [
#   # renovate: datasource=pypi depName=requests
#   "requests==2.32.4",
# ]
# ///

"""Update the OpenAPI schema from the Shortcut API.

Copyright (c) 2025 Edgar Ramírez-Mondragón
"""

from __future__ import annotations

import json
import pathlib

import requests

OPENAPI_URL = "https://developer.shortcut.com/api/rest/v3/shortcut.swagger.json"
PATH = "tap_shortcut/openapi.json"


def main() -> None:
    """Update the OpenAPI schema from the Shortcut API."""
    with pathlib.Path(PATH).open("w", encoding="utf-8") as file:
        response = requests.get(OPENAPI_URL, timeout=5)
        response.raise_for_status()
        spec = response.json()

        content = json.dumps(spec, indent=2) + "\n"
        file.write(content)


if __name__ == "__main__":
    main()
