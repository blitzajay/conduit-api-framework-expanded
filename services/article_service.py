from clients.article_client import ArticleClient
from clients.comment_client import CommentClient
from validators.format_validator import assert_status


class ArticleService:
    """Composes endpoint calls into reusable business operations."""

    def __init__(self, article_client: ArticleClient, comment_client: CommentClient) -> None:
        self.article_client = article_client
        self.comment_client = comment_client

    def create_article(self, article_data: dict) -> dict:
        response = self.article_client.create_article(**article_data)
        assert_status(response, 201)
        return response.json()["article"]

    def create_article_with_comment(self, article_data: dict, comment_body: str) -> dict:
        article = self.create_article(article_data)
        response = self.comment_client.create_comment(article["slug"], comment_body)
        assert_status(response, 200)
        return {"article": article, "comment": response.json()["comment"]}

    def cleanup_article(self, slug: str) -> None:
        response = self.article_client.delete_article(slug)
        assert_status(response, {200, 204, 404})
