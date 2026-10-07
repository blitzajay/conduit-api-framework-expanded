import logging

import pytest

from clients.article_client import ArticleClient
from clients.auth_client import AuthClient
from clients.comment_client import CommentClient
from clients.profile_client import ProfileClient
from config.settings import RUN_UI_TESTS, TEST_PASSWORD, UI_BASE_URL
from services.article_service import ArticleService
from utils.data_generator import generate_article_data, generate_unique_email, generate_unique_username
from validators.format_validator import assert_status

logger = logging.getLogger(__name__)


@pytest.fixture
def auth_client():
    client = AuthClient()
    yield client
    client.close()


@pytest.fixture
def registered_user(auth_client):
    user = {
        "username": generate_unique_username(),
        "email": generate_unique_email(),
        "password": TEST_PASSWORD,
    }
    response = auth_client.register(**user)
    assert_status(response, 201)
    response_user = response.json()["user"]
    yield {**user, "token": response_user["token"]}
    # The RealWorld API does not expose user deletion. Unique users prevent test coupling.


@pytest.fixture
def auth_token(registered_user):
    return registered_user["token"]


@pytest.fixture
def article_client(auth_token):
    client = ArticleClient(auth_token)
    yield client
    client.close()


@pytest.fixture
def comment_client(auth_token):
    client = CommentClient(auth_token)
    yield client
    client.close()


@pytest.fixture
def profile_client(auth_token):
    client = ProfileClient(auth_token)
    yield client
    client.close()


@pytest.fixture
def anonymous_article_client():
    client = ArticleClient()
    yield client
    client.close()


@pytest.fixture
def article_service(article_client, comment_client):
    return ArticleService(article_client, comment_client)


@pytest.fixture
def created_article(article_service):
    article = article_service.create_article(generate_article_data())
    yield article
    try:
        article_service.cleanup_article(article["slug"])
    except AssertionError as exc:
        logger.warning("Article cleanup failed for %s: %s", article["slug"], exc)


@pytest.fixture
def second_registered_user():
    client = AuthClient()
    user = {
        "username": generate_unique_username("second"),
        "email": generate_unique_email(),
        "password": TEST_PASSWORD,
    }
    response = client.register(**user)
    assert_status(response, 201)
    body = response.json()["user"]
    yield {**user, "token": body["token"]}
    client.close()


@pytest.fixture(scope="session")
def ui_base_url():
    return UI_BASE_URL


def pytest_collection_modifyitems(config, items):
    if RUN_UI_TESTS:
        return
    skip_ui = pytest.mark.skip(reason="Set RUN_UI_TESTS=true to execute browser tests")
    for item in items:
        if "ui" in item.keywords:
            item.add_marker(skip_ui)
