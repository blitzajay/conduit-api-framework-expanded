import pytest

from config.settings import TEST_PASSWORD
from schemas.error_schema import error_schema
from schemas.user_schema import user_schema
from utils.data_generator import generate_unique_email, generate_unique_username
from validators.format_validator import assert_json_content_type, assert_status
from validators.schema_validator import assert_schema


@pytest.mark.smoke
def test_register_user(auth_client):
    username = generate_unique_username()
    email = generate_unique_email()
    response = auth_client.register(username, email, TEST_PASSWORD)

    assert_status(response, 201)
    assert_json_content_type(response)
    assert_schema(response.json(), user_schema)
    assert response.json()["user"]["username"] == username
    assert response.json()["user"]["email"] == email


@pytest.mark.smoke
def test_login_with_valid_credentials(auth_client, registered_user):
    response = auth_client.login(registered_user["email"], registered_user["password"])

    assert_status(response, 200)
    assert_schema(response.json(), user_schema)
    assert response.json()["user"]["username"] == registered_user["username"]


@pytest.mark.negative
@pytest.mark.parametrize("email,password", [("missing@example.test", "bad"), ("", "")])
def test_login_with_invalid_credentials(auth_client, email, password):
    response = auth_client.login(email, password)
    assert_status(response, {400, 401, 403, 422})


@pytest.mark.negative
def test_register_duplicate_email(auth_client, registered_user):
    response = auth_client.register(generate_unique_username(), registered_user["email"], TEST_PASSWORD)
    assert_status(response, 422)
    assert_schema(response.json(), error_schema)


def test_get_current_user(auth_token):
    from clients.auth_client import AuthClient

    client = AuthClient(auth_token)
    response = client.get_current_user()
    client.close()

    assert_status(response, 200)
    assert_schema(response.json(), user_schema)


def test_update_user_bio(auth_token):
    from clients.auth_client import AuthClient

    client = AuthClient(auth_token)
    response = client.update_user(bio="Principal-level API automation practice")
    client.close()

    assert_status(response, 200)
    assert response.json()["user"]["bio"] == "Principal-level API automation practice"
