from typing import Any


def build_auth_headers(system_user_access_token: str) -> dict[str, str]:
    if not system_user_access_token or not isinstance(system_user_access_token, str):
        raise ValueError("Invalid or missing system user access token")

    return {
        "Authorization": f"Bearer {system_user_access_token}",
        "Content-Type": "application/json",
    }


def parse_graph_response(response_data: dict[str, Any]) -> dict[str, Any]:
    return response_data
