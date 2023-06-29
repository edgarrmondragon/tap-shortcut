"""Stream type classes for tap-shortcut."""

from __future__ import annotations

from tap_shortcut.client import ShortcutStream

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


class Projects(ShortcutStream):
    """Projects stream."""

    name = "projects"
    path = "/api/v3/projects"

    def get_child_context(
        self,
        record: dict,
        context: dict | None,  # noqa: ARG002
    ) -> dict:
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


class Epics(ShortcutStream):
    """Epics stream."""

    name = "epics"
    path = "/api/v3/epics"


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
