from clients.base_client import BaseClient


class CommentClient(BaseClient):
    def list_comments(self, slug: str):
        return self.get(f"/articles/{slug}/comments")

    def create_comment(self, slug: str, body: str):
        return self.post(f"/articles/{slug}/comments", json={"comment": {"body": body}})

    def delete_comment(self, slug: str, comment_id: int):
        return self.delete(f"/articles/{slug}/comments/{comment_id}")
