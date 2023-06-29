"""REST client handling, including ShortcutStream base class."""
from __future__ import annotations

import typing as t

from singer_sdk import RESTStream
from singer_sdk.authenticators import APIKeyAuthenticator


class ShortcutStream(RESTStream):
    """Shortcut stream class."""

    url_base = "https://api.app.shortcut.com"
    records_jsonpath = "$[*]"
    primary_keys: t.ClassVar[list[str]] = ["id"]

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
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {"User-Agent": f"{self.tap_name}/{self._tap.plugin_version}"}
