error_schema = {
    "type": "object",
    "required": ["errors"],
    "properties": {
        "errors": {
            "type": "object",
            "additionalProperties": {
                "oneOf": [
                    {"type": "array", "items": {"type": "string"}},
                    {"type": "string"},
                ]
            },
        }
    },
}
