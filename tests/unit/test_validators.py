from unittest.mock import Mock

import pytest

from schemas.user_schema import user_schema
from validators.format_validator import assert_status
from validators.schema_validator import assert_schema, validate_schema


def test_valid_user_schema_passes():
    payload = {
        "user": {
            "username": "ajay",
            "email": "ajay@example.test",
            "token": "token",
            "bio": None,
            "image": None,
        }
    }
    assert validate_schema(payload, user_schema) == (True, None)


def test_invalid_user_schema_returns_readable_path():
    valid, error = validate_schema({"user": {"username": "ajay"}}, user_schema)
    assert valid is False
    assert "user" in error


def test_assert_schema_raises_for_invalid_payload():
    with pytest.raises(AssertionError):
        assert_schema({}, user_schema)


def test_assert_status_includes_response_body():
    response = Mock(status_code=500, text="server exploded")
    with pytest.raises(AssertionError, match="server exploded"):
        assert_status(response, 200)
