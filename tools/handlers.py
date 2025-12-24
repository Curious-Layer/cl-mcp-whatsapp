import os
import uuid
from datetime import datetime
from auth import validate_token

MOCK_MODE = os.getenv("MOCK_WHATSAPP", "true").lower() == "true"


def send_whatsapp_message(data):
    validate_token(data.access_token)

    if MOCK_MODE:
        return {
            "mock": True,
            "type": "text",
            "to": data.to,
            "message": {
                "id": f"mock-{uuid.uuid4()}"
            },
            "status": "sent",
            "timestamp": datetime.utcnow().isoformat()
        }

    import requests

    url = f"https://graph.facebook.com/v19.0/{data.phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {data.access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": data.to,
        "type": "text",
        "text": {"body": data.message}
    }

    response = requests.post(url, headers=headers, json=payload, timeout=10)
    return response.json()


def send_whatsapp_template(data):
    validate_token(data.access_token)

    if MOCK_MODE:
        return {
            "mock": True,
            "type": "template",
            "to": data.to,
            "template": data.template_name,
            "status": "sent",
            "timestamp": datetime.utcnow().isoformat()
        }

    import requests

    url = f"https://graph.facebook.com/v19.0/{data.phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {data.access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": data.to,
        "type": "template",
        "template": {
            "name": data.template_name,
            "language": {"code": data.language_code}
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=10)
    return response.json()
