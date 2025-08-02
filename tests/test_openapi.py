"""Test OpenAPI handling."""

from __future__ import annotations

import typing as t

import pytest

from tap_shortcut.client import handle_x_nullable


@pytest.mark.parametrize(
    ("input_schema", "expected"),
    [
        (
            {
                "type": "object",
                "required": ["id"],
                "properties": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {
                        "type": "string",
                        "x-nullable": True,
                    },
                },
            },
            {
                "type": "object",
                "required": ["id"],
                "properties": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {
                        "type": ["string", "null"],
                        "x-nullable": True,
                    },
                },
            },
        ),
        (
            {
                "type": "object",
                "required": ["id"],
                "properties": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {
                        "type": "string",
                        "x-nullable": True,
                    },
                    "object_prop": {
                        "type": "object",
                        "properties": {
                            "nested": {
                                "type": "string",
                                "x-nullable": True,
                            },
                        },
                        "x-nullable": True,
                    },
                },
            },
            {
                "type": "object",
                "required": ["id"],
                "properties": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {
                        "type": ["string", "null"],
                        "x-nullable": True,
                    },
                    "object_prop": {
                        "type": ["object", "null"],
                        "properties": {
                            "nested": {
                                "type": ["string", "null"],
                                "x-nullable": True,
                            },
                        },
                        "x-nullable": True,
                    },
                },
            },
        ),
        (
            {
                "type": "object",
                "required": ["id", "array_prop"],
                "properties": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {
                        "type": "string",
                        "x-nullable": True,
                    },
                    "array_prop": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["id"],
                            "properties": {
                                "id": {
                                    "type": "integer",
                                },
                                "nested": {
                                    "type": "string",
                                    "x-nullable": True,
                                },
                            },
                        },
                    },
                },
            },
            {
                "type": "object",
                "required": ["id", "array_prop"],
                "properties": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {
                        "type": ["string", "null"],
                        "x-nullable": True,
                    },
                    "array_prop": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["id"],
                            "properties": {
                                "id": {
                                    "type": "integer",
                                },
                                "nested": {
                                    "type": ["string", "null"],
                                    "x-nullable": True,
                                },
                            },
                        },
                    },
                },
            },
        ),
    ],
    ids=["simple_object", "nested_object", "nested_array"],
)
def test_handle_x_nullable(
    input_schema: dict[str, t.Any],
    expected: dict[str, t.Any],
) -> None:
    """Test handling of x-nullable."""
    assert handle_x_nullable(input_schema) == expected
