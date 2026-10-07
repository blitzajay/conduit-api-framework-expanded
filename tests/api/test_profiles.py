from clients.profile_client import ProfileClient
from validators.format_validator import assert_status


def test_get_profile(profile_client, second_registered_user):
    response = profile_client.get_profile(second_registered_user["username"])
    assert_status(response, 200)
    assert response.json()["profile"]["username"] == second_registered_user["username"]
    assert response.json()["profile"]["following"] is False


def test_follow_and_unfollow_profile(profile_client, second_registered_user):
    username = second_registered_user["username"]
    follow = profile_client.follow(username)
    assert_status(follow, 200)
    assert follow.json()["profile"]["following"] is True

    unfollow = profile_client.unfollow(username)
    assert_status(unfollow, 200)
    assert unfollow.json()["profile"]["following"] is False


def test_followed_user_appears_in_feed(article_client, profile_client, second_registered_user):
    second_articles = __import__("clients.article_client", fromlist=["ArticleClient"]).ArticleClient(
        second_registered_user["token"]
    )
    article_response = second_articles.create_article(
        title=f"Feed article by {second_registered_user['username']}",
        description="Feed validation",
        body="Follower should see this",
        tag_list=["feed"],
    )
    article = article_response.json()["article"]
    try:
        assert_status(profile_client.follow(second_registered_user["username"]), 200)
        feed = article_client.feed()
        assert_status(feed, 200)
        assert any(item["slug"] == article["slug"] for item in feed.json()["articles"])
    finally:
        profile_client.unfollow(second_registered_user["username"])
        second_articles.delete_article(article["slug"])
        second_articles.close()
