"""REST client handling, including ShortcutStream base class."""

from __future__ import annotations

import sys
import typing as t

from singer_sdk import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


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


class ShortcutStream(RESTStream[None]):
    """Shortcut stream class."""

    url_base = "https://api.app.shortcut.com"
    records_jsonpath = "$[*]"
    primary_keys: t.ClassVar[list[str]] = ["id"]

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
