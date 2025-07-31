"""Shortcut tap class."""

from __future__ import annotations

import sys

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_shortcut import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


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

    @override
    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams."""
        return [
            streams.Categories(tap=self),
            streams.Epics(tap=self),
            streams.Files(tap=self),
            streams.Groups(tap=self),
            streams.Iterations(tap=self),
            streams.Labels(tap=self),
            streams.Members(tap=self),
            streams.Milestones(tap=self),
            streams.Projects(tap=self),
            streams.ProjectStories(tap=self),
            streams.Repositories(tap=self),
            streams.Workflows(tap=self),
        ]
