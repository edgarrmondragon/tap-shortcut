"""Stream type classes for tap-shortcut."""

from tap_shortcut.client import ShortcutStream


class Members(ShortcutStream):
    """Members stream."""

    name = "members"
    path = "/api/v3/members"
    primary_keys = ["id"]


class Projects(ShortcutStream):
    """Projects stream."""

    name = "projects"
    path = "/api/v3/projects"
    primary_keys = ["id"]


class Epics(ShortcutStream):
    """Epics stream."""

    name = "epics"
    path = "/api/v3/epics"
    primary_keys = ["id"]


class Workflows(ShortcutStream):
    """Workflows stream."""

    name = "workflows"
    path = "/api/v3/workflows"
    primary_keys = ["id"]


class Milestones(ShortcutStream):
    """Milestones stream."""

    name = "milestones"
    path = "/api/v3/milestones"
    primary_keys = ["id"]


class Labels(ShortcutStream):
    """Labels stream."""

    name = "labels"
    path = "/api/v3/labels"
    primary_keys = ["id"]


class Categories(ShortcutStream):
    """Categories stream."""

    name = "categories"
    path = "/api/v3/categories"
    primary_keys = ["id"]


class Files(ShortcutStream):
    """Files stream."""

    name = "files"
    path = "/api/v3/files"
    primary_keys = ["id"]


class Groups(ShortcutStream):
    """Groups stream."""

    name = "groups"
    path = "/api/v3/groups"
    primary_keys = ["id"]


class Iterations(ShortcutStream):
    """Iterations stream."""

    name = "iterations"
    path = "/api/v3/iterations"
    primary_keys = ["id"]


class Repositories(ShortcutStream):
    """Repositories stream."""

    name = "repositories"
    path = "/api/v3/repositories"
    primary_keys = ["id"]
