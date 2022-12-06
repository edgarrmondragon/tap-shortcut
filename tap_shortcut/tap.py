"""Shortcut tap class."""

from copy import deepcopy
from typing import Any, Dict, List, Type, Union

import requests
from singer_sdk import RESTStream, Stream, Tap
from singer_sdk import typing as th
from singer_sdk._singerlib import resolve_schema_references
from toolz.dicttoolz import get_in

from tap_shortcut.client import ShortcutStream
from tap_shortcut.streams import (
    Categories,
    Epics,
    Files,
    Groups,
    Iterations,
    Labels,
    Members,
    Milestones,
    Projects,
    ProjectStories,
    Repositories,
    Workflows,
)

STREAM_TYPES: List[Type[ShortcutStream]] = [
    Categories,
    Epics,
    Files,
    Groups,
    Iterations,
    Labels,
    Members,
    Milestones,
    Projects,
    ProjectStories,
    Repositories,
    Workflows,
]

OPENAPI_URL = "https://developer.shortcut.com/api/rest/v3/shortcut.swagger.json"


def handle_x_nullable(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Resolve x-nullable properties to standard JSON Schema nullable type.

    Args:
        schema: A JSON Schema dictionary.

    Returns:
        A new JSON Schema dictionary with 'x-nullable' resolved to [<type>, "null"].
    """
    result = deepcopy(schema)

    if "object" in result["type"]:
        for prop, prop_schema in result.get("properties", {}).items():
            prop_type: Union[str, List[str]] = prop_schema.get("type", [])
            types = [prop_type] if isinstance(prop_type, str) else prop_type
            nullable: bool = prop_schema.get("x-nullable", False)

            if nullable:
                prop_schema["type"] = [*types, "null"]

            result["properties"][prop] = handle_x_nullable(prop_schema)

    elif "array" in result["type"]:
        result["items"] = handle_x_nullable(result["items"])

    if "enum" in result and None not in result["enum"]:
        result["enum"].append(None)

    return result


class TapShortcut(Tap):
    """Singer tap for Shortcut."""

    name = "tap-shortcut"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "token",
            th.StringType,
            required=True,
            description="Shortcut Token",
        ),
    ).to_dict()

    def get_openapi_schema(self) -> dict:
        """Retrieve Swagger/OpenAPI schema for this API.

        Returns:
            OpenAPI schema.
        """
        return requests.get(OPENAPI_URL).json()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Shortcut streams.
        """
        openapi_schema = self.get_openapi_schema()
        streams: List[RESTStream] = []

        for stream_type in STREAM_TYPES:
            schema = get_in(
                keys=[
                    "paths",
                    stream_type.path,
                    "get",
                    "responses",
                    "200",
                    "schema",
                    "items",
                ],
                coll=openapi_schema,
            )
            schema["definitions"] = openapi_schema["definitions"]
            resolved_schema = resolve_schema_references(schema)
            clean_schema = handle_x_nullable(resolved_schema)
            streams.append(stream_type(tap=self, schema=clean_schema))

        return sorted(streams, key=lambda x: x.name)
