import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger("whatsapp-mcp-server")

GRAPH_API_BASE = "https://graph.facebook.com"
WHATSAPP_API_VERSION = "v21.0"


def get_headers(api_key: str) -> Dict[str, str]:
    """Build headers for WhatsApp Cloud API requests."""
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


#################### WhatsApp API Request Handler ###################
def make_whatsapp_request(
    method: str,
    endpoint: str,
    api_key: str,
    body: Optional[Dict] = None,
    params: Optional[Dict] = None,
) -> Dict:
    """Generic request handler for WhatsApp Cloud API."""
    headers = get_headers(api_key)
    url = f"{GRAPH_API_BASE}{endpoint}"

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body,
            params=params,
            timeout=10,
        )
        result = response.json()

        if not (200 <= response.status_code < 300):
            logger.error(f"WhatsApp API error: {result}")
            return {
                "error": result.get("error", {}).get("message", "Unknown error"),
                "code": result.get("error", {}).get("code"),
                "status": response.status_code,
            }
        return result

    except Exception as e:
        logger.error(f"Request error: {e}")
        return {"error": str(e)}


################### WhatsApp API Service Functions ###################


def send_text_message(
    api_key: str, phone_number_id: str, recipient_phone: str, message_text: str
) -> Dict:
    """Send a text message via WhatsApp Cloud API."""
    logger.info(f"[send_text_message] to={recipient_phone}")

    body = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_phone,
        "type": "text",
        "text": {"body": message_text},
    }
    endpoint = f"/{WHATSAPP_API_VERSION}/{phone_number_id}/messages"
    return make_whatsapp_request("POST", endpoint, api_key, body=body)


def send_template_message(
    api_key: str,
    phone_number_id: str,
    recipient_phone: str,
    template_name: str,
    template_language_code: str = "en_US",
    parameters: Optional[list] = None,
) -> Dict:
    """Send a template message via WhatsApp Cloud API."""
    logger.info(
        f"[send_template_message] to={recipient_phone}, template={template_name}"
    )

    body = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_phone,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": template_language_code},
        },
    }

    if parameters:
        body["template"]["components"] = [{"type": "body", "parameters": parameters}]

    endpoint = f"/{WHATSAPP_API_VERSION}/{phone_number_id}/messages"
    return make_whatsapp_request("POST", endpoint, api_key, body=body)


def send_media_message(
    api_key: str,
    phone_number_id: str,
    recipient_phone: str,
    media_type: str,
    media_url: str,
    caption: Optional[str] = None,
) -> Dict:
    """Send a media message (image, video, audio, document) via WhatsApp Cloud API."""
    logger.info(f"[send_media_message] to={recipient_phone}, type={media_type}")

    media_object = {"link": media_url}
    if caption and media_type in ["image", "video"]:
        media_object["caption"] = caption

    body = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_phone,
        "type": media_type,
        media_type: media_object,
    }

    endpoint = f"/{WHATSAPP_API_VERSION}/{phone_number_id}/messages"
    return make_whatsapp_request("POST", endpoint, api_key, body=body)


def test_connection(api_key: str, phone_number_id: str) -> Dict:
    """Test connection to WhatsApp Cloud API."""
    logger.info(f"[test_connection] phone_number_id={phone_number_id}")

    endpoint = f"/{WHATSAPP_API_VERSION}/{phone_number_id}"
    params = {"fields": "id,display_phone_number,quality_rating"}
    return make_whatsapp_request("GET", endpoint, api_key, params=params)


def get_message_attachment(api_key: str, media_id: str) -> Dict:
    """Retrieve message media URL from WhatsApp Cloud API."""
    logger.info(f"[get_message_attachment] media_id={media_id}")

    endpoint = f"/{WHATSAPP_API_VERSION}/{media_id}"
    params = {"fields": "id,media_product_type,url"}
    return make_whatsapp_request("GET", endpoint, api_key, params=params)


def parse_graph_response(response_data: dict[str, Any]) -> dict[str, Any]:
    """Parse WhatsApp Graph API response."""
    return response_data
