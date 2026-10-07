user_schema = {
    "type": "object",
    "required": ["user"],
    "properties": {
        "user": {
            "type": "object",
            "required": ["username", "email", "token", "bio", "image"],
            "properties": {
                "username": {"type": "string", "minLength": 1},
                "email": {"type": "string", "minLength": 3},
                "token": {"type": "string", "minLength": 1},
                "bio": {"type": ["string", "null"]},
                "image": {"type": ["string", "null"]},
            },
        }
    },
}
