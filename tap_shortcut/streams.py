"""Stream type classes for tap-shortcut."""

from __future__ import annotations

import typing as t

from tap_shortcut.client import ShortcutStream

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
    "Projects",
    "ProjectStories",
    "Repositories",
    "Workflows",
]


class Members(ShortcutStream):
    """Members stream."""

    name = "members"
    path = "/api/v3/members"
    extra_nullable_fields = ("replaced_by",)


class Projects(ShortcutStream):
    """Projects stream."""

    name = "projects"
    path = "/api/v3/projects"

    def get_child_context(
        self,
        record: Record,
        context: Context | None,  # noqa: ARG002
    ) -> dict[str, t.Any]:
        """Return a dictionary of child context.

        Args:
            record: A dictionary of the record.
            context: A dictionary of the context.

        Returns:
            A dictionary of the child context.
        """
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
    def preprocess_schema(cls: type[ProjectStories], schema: dict[str, t.Any]) -> None:
        """Return the schema of the stream."""
        super().preprocess_schema(schema)
        schema["properties"]["lead_time"]["type"] = ["number", "null"]
        schema["properties"]["cycle_time"]["type"] = ["number", "null"]


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


class Repositories(ShortcutStream):
    """Repositories stream."""

    name = "repositories"
    path = "/api/v3/repositories"
