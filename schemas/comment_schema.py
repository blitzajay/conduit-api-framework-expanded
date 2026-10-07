from schemas.article_schema import author_schema

comment_object_schema = {
    "type": "object",
    "required": ["id", "createdAt", "updatedAt", "body", "author"],
    "properties": {
        "id": {"type": "integer"},
        "createdAt": {"type": "string"},
        "updatedAt": {"type": "string"},
        "body": {"type": "string"},
        "author": author_schema,
    },
}

comment_schema = {
    "type": "object",
    "required": ["comment"],
    "properties": {"comment": comment_object_schema},
}

comments_schema = {
    "type": "object",
    "required": ["comments"],
    "properties": {"comments": {"type": "array", "items": comment_object_schema}},
}
