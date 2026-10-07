import pytest

from utils.data_generator import generate_article_data
from validators.format_validator import assert_status


@pytest.mark.integration
def test_complete_article_lifecycle(article_service, article_client, comment_client):
    result = article_service.create_article_with_comment(
        generate_article_data("Lifecycle"),
        "Created as part of a business workflow",
    )
    article = result["article"]
    comment = result["comment"]

    try:
        favorite = article_client.favorite_article(article["slug"])
        assert_status(favorite, 200)
        assert favorite.json()["article"]["favoritesCount"] >= 1

        update = article_client.update_article(article["slug"], description="Updated in lifecycle")
        assert_status(update, 200)
        assert update.json()["article"]["description"] == "Updated in lifecycle"

        comments = comment_client.list_comments(article["slug"])
        assert any(item["id"] == comment["id"] for item in comments.json()["comments"])
    finally:
        comment_client.delete_comment(article["slug"], comment["id"])
        article_service.cleanup_article(article["slug"])
