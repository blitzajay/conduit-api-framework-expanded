from unittest.mock import Mock

from clients.article_client import ArticleClient
from clients.auth_client import AuthClient
from clients.comment_client import CommentClient
from clients.profile_client import ProfileClient


def test_article_client_maps_python_names_to_api_payload(monkeypatch):
    client = ArticleClient()
    post = Mock()
    monkeypatch.setattr(client, "post", post)

    client.create_article("Title", "Description", "Body", ["python"])

    post.assert_called_once_with(
        "/articles",
        json={
            "article": {
                "title": "Title",
                "description": "Description",
                "body": "Body",
                "tagList": ["python"],
            }
        },
    )
    client.close()


def test_auth_client_login_payload(monkeypatch):
    client = AuthClient()
    post = Mock()
    monkeypatch.setattr(client, "post", post)
    client.login("a@example.test", "password")
    post.assert_called_once_with(
        "/users/login",
        json={"user": {"email": "a@example.test", "password": "password"}},
    )
    client.close()


def test_comment_client_uses_article_scoped_endpoint(monkeypatch):
    client = CommentClient()
    post = Mock()
    monkeypatch.setattr(client, "post", post)
    client.create_comment("my-slug", "hello")
    post.assert_called_once_with(
        "/articles/my-slug/comments",
        json={"comment": {"body": "hello"}},
    )
    client.close()


def test_profile_client_follow_endpoint(monkeypatch):
    client = ProfileClient()
    post = Mock()
    monkeypatch.setattr(client, "post", post)
    client.follow("ajay")
    post.assert_called_once_with("/profiles/ajay/follow")
    client.close()
