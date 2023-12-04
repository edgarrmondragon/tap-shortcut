"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

from typing import Any

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_shortcut.tap import TapShortcut

SAMPLE_CONFIG: dict[str, Any] = {}


TestTapShortcut = get_tap_test_class(
    TapShortcut,
    config=SAMPLE_CONFIG,
    suite_config=SuiteConfig(
        ignore_no_records_for_streams=[
            "categories",
            "files",
            "iterations",
            "milestones",
        ]
    ),
)
