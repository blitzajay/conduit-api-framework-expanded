import uuid


def unique_suffix() -> str:
    return uuid.uuid4().hex[:10]


def generate_unique_username(prefix: str = "user") -> str:
    return f"{prefix}_{unique_suffix()}"


def generate_unique_email() -> str:
    return f"{unique_suffix()}@example.test"


def generate_article_data(prefix: str = "API Automation") -> dict:
    suffix = unique_suffix()
    return {
        "title": f"{prefix} {suffix}",
        "description": f"Description {suffix}",
        "body": f"Body created by automated test {suffix}",
        "tag_list": ["pytest", "api", suffix[:5]],
    }
