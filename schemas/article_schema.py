author_schema = {
    "type": "object",
    "required": ["username", "bio", "image", "following"],
    "properties": {
        "username": {"type": "string"},
        "bio": {"type": ["string", "null"]},
        "image": {"type": ["string", "null"]},
        "following": {"type": "boolean"},
    },
}

article_object_schema = {
    "type": "object",
    "required": [
        "slug", "title", "description", "body", "tagList", "createdAt", "updatedAt",
        "favorited", "favoritesCount", "author",
    ],
    "properties": {
        "slug": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "body": {"type": "string"},
        "tagList": {"type": "array", "items": {"type": "string"}},
        "createdAt": {"type": "string"},
        "updatedAt": {"type": "string"},
        "favorited": {"type": "boolean"},
        "favoritesCount": {"type": "integer", "minimum": 0},
        "author": author_schema,
    },
}

article_schema = {
    "type": "object",
    "required": ["article"],
    "properties": {"article": article_object_schema},
}

articles_schema = {
    "type": "object",
    "required": ["articles", "articlesCount"],
    "properties": {
        "articles": {"type": "array", "items": article_object_schema},
        "articlesCount": {"type": "integer", "minimum": 0},
    },
}
