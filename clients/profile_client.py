from clients.base_client import BaseClient


class ProfileClient(BaseClient):
    def get_profile(self, username: str):
        return self.get(f"/profiles/{username}")

    def follow(self, username: str):
        return self.post(f"/profiles/{username}/follow")

    def unfollow(self, username: str):
        return self.delete(f"/profiles/{username}/follow")
