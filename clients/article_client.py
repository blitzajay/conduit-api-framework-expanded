from clients.base_client import BaseClient


class ArticleClient(BaseClient):
    def list_articles(self, *, tag=None, author=None, favorited=None, limit=20, offset=0):
        params = {"limit": limit, "offset": offset}
        optional = {"tag": tag, "author": author, "favorited": favorited}
        params.update({key: value for key, value in optional.items() if value is not None})
        return self.get("/articles", params=params)

    def feed(self, *, limit=20, offset=0):
        return self.get("/articles/feed", params={"limit": limit, "offset": offset})

    def get_article(self, slug: str):
        return self.get(f"/articles/{slug}")

    def create_article(self, title: str, description: str, body: str, tag_list: list[str] | None = None):
        payload = {
            "article": {
                "title": title,
                "description": description,
                "body": body,
                "tagList": tag_list or [],
            }
        }
        return self.post("/articles", json=payload)

    def update_article(self, slug: str, **fields):
        return self.put(f"/articles/{slug}", json={"article": fields})

    def delete_article(self, slug: str):
        return self.delete(f"/articles/{slug}")

    def favorite_article(self, slug: str):
        return self.post(f"/articles/{slug}/favorite")

    def unfavorite_article(self, slug: str):
        return self.delete(f"/articles/{slug}/favorite")

    def get_tags(self):
        return self.get("/tags")
