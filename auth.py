def validate_token(token: str):
    if not token or not isinstance(token, str):
        raise ValueError("Invalid or missing access token")
    return True
