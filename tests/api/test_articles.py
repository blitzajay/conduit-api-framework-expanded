import pytest

from schemas.article_schema import article_schema, articles_schema
from utils.data_generator import generate_article_data
from validators.format_validator import assert_status
from validators.schema_validator import assert_schema


@pytest.mark.smoke
def test_create_article(article_client):
    data = generate_article_data()
    response = article_client.create_article(**data)
    assert_status(response, 201)
    assert_schema(response.json(), article_schema)
    article = response.json()["article"]
    try:
        assert article["title"] == data["title"]
        assert article["tagList"] == data["tag_list"]
    finally:
        article_client.delete_article(article["slug"])


def test_get_article(article_client, created_article):
    response = article_client.get_article(created_article["slug"])
    assert_status(response, 200)
    assert_schema(response.json(), article_schema)
    assert response.json()["article"]["slug"] == created_article["slug"]


def test_update_article(article_client, created_article):
    updated_title = f"Updated {created_article['title']}"
    response = article_client.update_article(created_article["slug"], title=updated_title)
    assert_status(response, 200)
    assert response.json()["article"]["title"] == updated_title


def test_list_articles_supports_pagination(anonymous_article_client):
    response = anonymous_article_client.list_articles(limit=5, offset=0)
    assert_status(response, 200)
    assert_schema(response.json(), articles_schema)
    assert len(response.json()["articles"]) <= 5


def test_filter_articles_by_author(article_client, created_article):
    author = created_article["author"]["username"]
    response = article_client.list_articles(author=author)
    assert_status(response, 200)
    assert any(article["slug"] == created_article["slug"] for article in response.json()["articles"])


def test_favorite_and_unfavorite_article(article_client, created_article):
    favorite = article_client.favorite_article(created_article["slug"])
    assert_status(favorite, 200)
    assert favorite.json()["article"]["favorited"] is True

    unfavorite = article_client.unfavorite_article(created_article["slug"])
    assert_status(unfavorite, 200)
    assert unfavorite.json()["article"]["favorited"] is False


def test_get_tags(anonymous_article_client):
    response = anonymous_article_client.get_tags()
    assert_status(response, 200)
    assert isinstance(response.json()["tags"], list)


@pytest.mark.negative
def test_create_article_without_authentication(anonymous_article_client):
    response = anonymous_article_client.create_article(**generate_article_data())
    assert_status(response, {401, 403})


@pytest.mark.negative
def test_get_unknown_article(anonymous_article_client):
    response = anonymous_article_client.get_article("article-that-does-not-exist")
    assert_status(response, 404)
