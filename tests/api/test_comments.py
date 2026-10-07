import pytest

from schemas.comment_schema import comment_schema, comments_schema
from validators.format_validator import assert_status
from validators.schema_validator import assert_schema


@pytest.mark.smoke
def test_create_comment(comment_client, created_article):
    response = comment_client.create_comment(created_article["slug"], "Useful framework explanation")
    assert_status(response, 200)
    assert_schema(response.json(), comment_schema)
    comment = response.json()["comment"]
    try:
        assert comment["body"] == "Useful framework explanation"
    finally:
        comment_client.delete_comment(created_article["slug"], comment["id"])


def test_list_comments(comment_client, created_article):
    create_response = comment_client.create_comment(created_article["slug"], "List me")
    assert_status(create_response, 200)
    comment = create_response.json()["comment"]
    try:
        response = comment_client.list_comments(created_article["slug"])
        assert_status(response, 200)
        assert_schema(response.json(), comments_schema)
        assert any(item["id"] == comment["id"] for item in response.json()["comments"])
    finally:
        comment_client.delete_comment(created_article["slug"], comment["id"])


def test_delete_comment(comment_client, created_article):
    create_response = comment_client.create_comment(created_article["slug"], "Delete me")
    comment_id = create_response.json()["comment"]["id"]
    delete_response = comment_client.delete_comment(created_article["slug"], comment_id)
    assert_status(delete_response, {200, 204})

    list_response = comment_client.list_comments(created_article["slug"])
    assert all(item["id"] != comment_id for item in list_response.json()["comments"])
