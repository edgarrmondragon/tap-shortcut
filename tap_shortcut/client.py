"""REST client handling, including ShortcutStream base class."""

from __future__ import annotations

import typing as t

from singer_sdk import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator

T = t.TypeVar("T", bound="ShortcutStream")


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
    def authenticator(self) -> APIKeyAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        token: str = self.config["token"]
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Shortcut-Token",
            value=token,
            location="header",
        )

    @property
    def http_headers(self) -> dict[str, str]:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {"User-Agent": f"{self.tap_name}/{self._tap.plugin_version}"}

    @classmethod
    def preprocess_schema(cls: type[T], schema: dict[str, t.Any]) -> None:
        """Preprocess the schema.

        Args:
            schema: A dictionary of the schema.

        Returns:
            A dictionary of the processed schema.
        """
        _handle_runtime_nullables(schema, cls.extra_nullable_fields)
