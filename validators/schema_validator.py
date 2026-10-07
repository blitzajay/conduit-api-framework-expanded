from jsonschema import Draft7Validator


def validate_schema(instance, schema) -> tuple[bool, str | None]:
    errors = sorted(Draft7Validator(schema).iter_errors(instance), key=lambda error: list(error.path))
    if not errors:
        return True, None
    error = errors[0]
    path = ".".join(str(part) for part in error.absolute_path) or "<root>"
    return False, f"{path}: {error.message}"


def assert_schema(instance, schema) -> None:
    is_valid, error = validate_schema(instance, schema)
    assert is_valid, error
