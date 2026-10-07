from clients.base_client import BaseClient


class AuthClient(BaseClient):
    def register(self, username: str, email: str, password: str):
        return self.post(
            "/users",
            json={"user": {"username": username, "email": email, "password": password}},
        )

    def login(self, email: str, password: str):
        return self.post("/users/login", json={"user": {"email": email, "password": password}})

    def get_current_user(self):
        return self.get("/user")

    def update_user(self, **fields):
        return self.put("/user", json={"user": fields})
