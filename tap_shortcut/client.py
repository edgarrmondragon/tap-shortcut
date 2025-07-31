"""REST client handling, including ShortcutStream base class."""

from __future__ import annotations

import importlib.resources
import sys
import typing as t
from copy import deepcopy

from singer_sdk import OpenAPISchema, RESTStream, StreamSchema
from singer_sdk.authenticators import APIKeyAuthenticator
from toolz.dicttoolz import get_in

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

SPEC = importlib.resources.files("tap_shortcut") / "openapi.json"


def handle_x_nullable(schema: dict[str, t.Any]) -> dict[str, t.Any]:
    """Resolve x-nullable properties to standard JSON Schema nullable type.

    Args:
        schema: A JSON Schema dictionary.

    Returns:
        A new JSON Schema dictionary with 'x-nullable' resolved to [<type>, "null"].
    """
    result = deepcopy(schema)

    if "object" in result["type"]:
        for prop, prop_schema in result.get("properties", {}).items():
            if prop_schema.get("x-nullable", False):
                prop_type: str | list[str] = prop_schema.get("type", [])
                types = [prop_type] if isinstance(prop_type, str) else prop_type
                prop_schema["type"] = [*types, "null"]

            result["properties"][prop] = handle_x_nullable(prop_schema)

    elif "array" in result["type"]:
        result["items"] = handle_x_nullable(result["items"])

    if "enum" in result and None not in result["enum"]:
        result["enum"].append(None)

    return result


def _handle_runtime_nullables(
    schema: dict[str, t.Any],
    fields: t.Iterable[str],
) -> None:
    """Force fields to be nullable at runtime."""
    for field in fields:
        if field in schema["properties"]:
            prop_type: str | list[str] = schema["type"]
            types = [prop_type] if isinstance(prop_type, str) else prop_type
            schema["properties"][field]["type"] = [*types, "null"]


class ResponseKey(t.NamedTuple):
    """Response key."""

    path: str
    http_method: str
    expected_status: int = 200


class ShortcutOpenAPISchema(OpenAPISchema[ResponseKey]):
    """Shortcut OpenAPI schema."""

    @override
    def get_unresolved_schema(self, key: ResponseKey) -> dict[str, t.Any]:
        return get_in(  # type: ignore[no-any-return]
            keys=(
                "paths",
                key.path,
                key.http_method.lower(),
                "responses",
                str(key.expected_status),
                "schema",
                "items",
            ),
            coll=self.spec,
        )


class ShortcutSchema(StreamSchema[ResponseKey]):
    """Shortcut schema."""

    @override
    def get_stream_schema(
        self,
        stream: ShortcutStream,  # type: ignore[override]
        stream_class: type[ShortcutStream],  # type: ignore[override]
    ) -> dict[str, t.Any]:
        key = ResponseKey(stream.path, stream.http_method)
        schema = handle_x_nullable(self.schema_source.fetch_schema(key))
        _handle_runtime_nullables(schema, stream.extra_nullable_fields)
        stream_class.preprocess_schema(schema)
        return schema


class ShortcutStream(RESTStream[None]):
    """Shortcut stream class."""

    url_base = "https://api.app.shortcut.com"
    records_jsonpath = "$[*]"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    schema: t.ClassVar[ShortcutSchema] = ShortcutSchema(ShortcutOpenAPISchema(SPEC))

    # Abstract fields
    extra_nullable_fields: tuple[str, ...] = ()

    @property
    @override
    def authenticator(self) -> APIKeyAuthenticator:
        """Request authenticator."""
        token: str = self.config["token"]
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Shortcut-Token",
            value=token,
            location="header",
        )

    @classmethod
    def preprocess_schema(cls, schema: dict[str, t.Any]) -> None:
        """Preprocess the schema.

        Args:
            schema: A dictionary of the schema.

        Returns:
            A dictionary of the processed schema.
        """
        _handle_runtime_nullables(schema, cls.extra_nullable_fields)
