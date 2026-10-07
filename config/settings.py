import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://conduit-realworld-example-app.fly.dev/api").rstrip("/")
UI_BASE_URL = os.getenv("UI_BASE_URL", BASE_URL.removesuffix("/api")).rstrip("/")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "15"))
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "Test@123")
RUN_UI_TESTS = os.getenv("RUN_UI_TESTS", "false").lower() == "true"
