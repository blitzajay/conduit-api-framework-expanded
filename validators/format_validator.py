from __future__ import annotations

from requests import Response


def assert_status(response: Response, expected: int | set[int]) -> None:
    expected_values = {expected} if isinstance(expected, int) else expected
    assert response.status_code in expected_values, (
        f"Expected status {sorted(expected_values)}, got {response.status_code}. "
        f"Response: {response.text[:1000]}"
    )


def assert_json_content_type(response: Response) -> None:
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Unexpected Content-Type: {content_type}"
