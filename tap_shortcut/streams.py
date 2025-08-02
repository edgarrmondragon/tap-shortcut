"""Stream type classes for tap-shortcut."""

from __future__ import annotations

import sys
import typing as t

from tap_shortcut.client import ShortcutStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context, Record


__all__ = [
    "Categories",
    "Epics",
    "Files",
    "Groups",
    "Iterations",
    "Labels",
    "Members",
    "Milestones",
    "ProjectStories",
    "Projects",
    "Repositories",
    "Workflows",
]


class Members(ShortcutStream):
    """Members stream."""

    name = "members"
    path = "/api/v3/members"
    extra_nullable_fields = ("replaced_by", "installation_id")


class Projects(ShortcutStream):
    """Projects stream."""

    name = "projects"
    path = "/api/v3/projects"

    @override
    def get_child_context(
        self,
        record: Record,
        context: Context | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of child context."""
        return {"project-public-id": record["id"]}


class ProjectStories(ShortcutStream):
    """Project stories stream."""

    name = "project_stories"
    path = "/api/v3/projects/{project-public-id}/stories"
    parent_stream_type = Projects
    ignore_parent_replication_key = True
    extra_nullable_fields = (
        "description",
        "synced_item",
        "unresolved_blocker_comments",
        "lead_time",
        "cycle_time",
    )

    @classmethod
    @override
    def preprocess_schema(cls, schema: dict[str, t.Any]) -> None:
        """Return the schema of the stream."""
        ShortcutStream.preprocess_schema(schema)
        schema["properties"]["lead_time"]["type"] = ["number", "null"]
        schema["properties"]["cycle_time"]["type"] = ["number", "null"]
        schema["properties"]["parent_story_id"]["type"] = ["integer", "null"]
        schema["properties"]["sub_task_story_ids"]["type"] = ["array", "null"]


class Epics(ShortcutStream):
    """Epics stream."""

    name = "epics"
    path = "/api/v3/epics"
    extra_nullable_fields = ("description",)


class Workflows(ShortcutStream):
    """Workflows stream."""

    name = "workflows"
    path = "/api/v3/workflows"


class Milestones(ShortcutStream):
    """Milestones stream."""

    name = "milestones"
    path = "/api/v3/milestones"


class Labels(ShortcutStream):
    """Labels stream."""

    name = "labels"
    path = "/api/v3/labels"


class Categories(ShortcutStream):
    """Categories stream."""

    name = "categories"
    path = "/api/v3/categories"


class Files(ShortcutStream):
    """Files stream."""

    name = "files"
    path = "/api/v3/files"


class Groups(ShortcutStream):
    """Groups stream."""

    name = "groups"
    path = "/api/v3/groups"


class Iterations(ShortcutStream):
    """Iterations stream."""

    name = "iterations"
    path = "/api/v3/iterations"

    @classmethod
    @override
    def preprocess_schema(cls, schema: dict[str, t.Any]) -> None:
        """Return the schema of the stream."""
        ShortcutStream.preprocess_schema(schema)
        schema["properties"]["associated_groups"]["type"] = ["array", "null"]


class Repositories(ShortcutStream):
    """Repositories stream."""

    name = "repositories"
    path = "/api/v3/repositories"
