import logging

GRAPH_API_BASE_URL = "https://graph.facebook.com"
AUTH_MODE = "system_user_access_token"


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
