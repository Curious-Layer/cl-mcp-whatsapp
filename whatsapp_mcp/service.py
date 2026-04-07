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
    resource_path: str,
    api_key: str,
    body: Optional[Dict] = None,
    params: Optional[Dict] = None,
) -> Dict:
    """Generic request handler for WhatsApp Cloud API.

    Args:
        method: HTTP method (GET, POST, etc.)
        resource_path: API resource path (e.g., '/phone_number_id/messages')
        api_key: WhatsApp Cloud API access token
        body: Optional request body
        params: Optional query parameters
    """
    headers = get_headers(api_key)
    endpoint = f"/{WHATSAPP_API_VERSION}{resource_path}"
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
    resource_path = f"/{phone_number_id}/messages"
    return make_whatsapp_request("POST", resource_path, api_key, body=body)


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

    resource_path = f"/{phone_number_id}/messages"
    return make_whatsapp_request("POST", resource_path, api_key, body=body)


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

    resource_path = f"/{phone_number_id}/messages"
    return make_whatsapp_request("POST", resource_path, api_key, body=body)


def send_marketing_template_message(
    api_key: str,
    phone_number_id: str,
    recipient_phone: str,
    template_name: str,
    template_language_code: str = "en_US",
    components: Optional[list] = None,
    product_policy: Optional[str] = None,
    message_activity_sharing: Optional[bool] = None,
) -> Dict:
    """Send a marketing template message via WhatsApp Cloud API.

    Args:
        api_key: WhatsApp Cloud API access token
        phone_number_id: Your WhatsApp Business Account phone number ID
        recipient_phone: Recipient's phone number with country code
        template_name: Name of the approved marketing template
        template_language_code: Template language code (e.g., en_US, es_ES)
        components: Array of template components containing parameters
        product_policy: Optional product policy setting (CLOUD_API_FALLBACK, STRICT)
        message_activity_sharing: Optional flag to control message activity sharing
    """
    logger.info(
        f"[send_marketing_template_message] to={recipient_phone}, template={template_name}"
    )

    body = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_phone,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"language": template_language_code},
        },
    }

    if components:
        body["template"]["components"] = components
    if product_policy:
        body["product_policy"] = product_policy
    if message_activity_sharing is not None:
        body["message_activity_sharing"] = message_activity_sharing

    resource_path = f"/{phone_number_id}/marketing_messages"
    return make_whatsapp_request("POST", resource_path, api_key, body=body)


def test_connection(api_key: str, phone_number_id: str) -> Dict:
    """Test connection to WhatsApp Cloud API."""
    logger.info(f"[test_connection] phone_number_id={phone_number_id}")

    resource_path = f"/{phone_number_id}"
    params = {"fields": "id,display_phone_number,quality_rating"}
    return make_whatsapp_request("GET", resource_path, api_key, params=params)


def get_message_attachment(api_key: str, media_id: str) -> Dict:
    """Retrieve message media URL from WhatsApp Cloud API."""
    logger.info(f"[get_message_attachment] media_id={media_id}")

    resource_path = f"/{media_id}"
    params = {"fields": "id,media_product_type,url"}
    return make_whatsapp_request("GET", resource_path, api_key, params=params)


def get_message_history_events(
    api_key: str,
    message_history_id: str,
    status_filter: Optional[str] = None,
    fields: Optional[str] = None,
    limit: int = 25,
    after: Optional[str] = None,
    before: Optional[str] = None,
) -> Dict:
    """Retrieve paginated message delivery status events from WhatsApp Cloud API.

    Args:
        api_key: WhatsApp Cloud API access token
        message_history_id: WhatsApp Business Message History ID
        status_filter: Filter by delivery status (ACCEPTED, DELIVERED, ERROR, READ, SENT)
        fields: Comma-separated list of fields to include (id, delivery_status, error_description, occurrence_timestamp, status_timestamp, application)
        limit: Maximum number of events per page (1-100, default 25)
        after: Pagination cursor for next page
        before: Pagination cursor for previous page
    """
    logger.info(f"[get_message_history_events] message_history_id={message_history_id}")

    params = {"limit": limit}

    if status_filter:
        params["status_filter"] = status_filter
    if fields:
        params["fields"] = fields
    if after:
        params["after"] = after
    if before:
        params["before"] = before

    resource_path = f"/{message_history_id}/events"
    return make_whatsapp_request("GET", resource_path, api_key, params=params)


def configure_conversational_automation(
    api_key: str,
    phone_number_id: str,
    enable_welcome_message: Optional[bool] = None,
    prompts: Optional[list] = None,
    commands: Optional[list] = None,
) -> Dict:
    """Configure conversational automation settings for a WhatsApp Business Account phone number.

    Args:
        api_key: WhatsApp Cloud API access token
        phone_number_id: WhatsApp Business phone number ID
        enable_welcome_message: Whether to enable welcome messages for new conversations
        prompts: List of conversation prompts (ice breakers) to guide customer interactions
        commands: List of bot command dicts with 'command_name' and 'command_description' keys
    """
    logger.info(
        f"[configure_conversational_automation] phone_number_id={phone_number_id}"
    )

    body = {}

    if enable_welcome_message is not None:
        body["enable_welcome_message"] = enable_welcome_message
    if prompts is not None:
        body["prompts"] = prompts
    if commands is not None:
        body["commands"] = commands

    resource_path = f"/{phone_number_id}/conversational_automation"
    return make_whatsapp_request("POST", resource_path, api_key, body=body)


def get_bot_details(
    api_key: str,
    bot_id: str,
    fields: Optional[str] = None,
) -> Dict:
    """Retrieve WhatsApp Business Bot details from WhatsApp Cloud API.

    Args:
        api_key: WhatsApp Cloud API access token
        bot_id: WhatsApp Business Bot ID
        fields: Comma-separated list of fields to include (id, prompts, commands, enable_welcome_message)
    """
    logger.info(f"[get_bot_details] bot_id={bot_id}")

    params = {}
    if fields:
        params["fields"] = fields

    resource_path = f"/{bot_id}"
    return make_whatsapp_request("GET", resource_path, api_key, params=params)


def get_call_permissions(
    api_key: str,
    phone_number_id: str,
    user_wa_id: str,
) -> Dict:
    """Check whether you have permission to call a WhatsApp user.

    Args:
        api_key: WhatsApp Cloud API access token
        phone_number_id: Your WhatsApp Business Account phone number ID
        user_wa_id: The WhatsApp ID of the user to check call permissions for
    """
    logger.info(
        f"[get_call_permissions] phone_number_id={phone_number_id}, user_wa_id={user_wa_id}"
    )

    params = {"user_wa_id": user_wa_id}
    resource_path = f"/{phone_number_id}/call_permissions"
    return make_whatsapp_request("GET", resource_path, api_key, params=params)


def manage_call(
    api_key: str,
    phone_number_id: str,
    action: str,
    to: Optional[str] = None,
    call_id: Optional[str] = None,
    session: Optional[dict] = None,
    biz_opaque_callback_data: Optional[str] = None,
) -> Dict:
    """Manage WhatsApp calls - initiate, accept, reject, or terminate.

    Args:
        api_key: WhatsApp Cloud API access token
        phone_number_id: Your WhatsApp Business Account phone number ID
        action: Call action - one of: connect, pre_accept, accept, reject, terminate
        to: The number being called (required for connect/pre_accept/accept/reject)
        call_id: The WhatsApp call ID (required for terminate)
        session: Session description protocol (SDP) - dict with 'sdp_type' and 'sdp' (optional for connect/accept)
        biz_opaque_callback_data: Arbitrary string for tracking (max 512 chars)
    """
    logger.info(f"[manage_call] phone_number_id={phone_number_id}, action={action}")

    body = {
        "messaging_product": "whatsapp",
        "action": action,
    }

    if action == "terminate":
        body["call_id"] = call_id
    else:
        if to:
            body["to"] = to
        if session:
            body["session"] = session
        if biz_opaque_callback_data:
            body["biz_opaque_callback_data"] = biz_opaque_callback_data

    resource_path = f"/{phone_number_id}/calls"
    return make_whatsapp_request("POST", resource_path, api_key, body=body)


def get_qr_code(
    api_key: str,
    phone_number_id: str,
    qr_code_id: str,
    fields: Optional[str] = None,
) -> Dict:
    """Retrieve details for a specific WhatsApp Message QR code.

    Args:
        api_key: WhatsApp Cloud API access token
        phone_number_id: Your WhatsApp Business Account phone number ID that owns the QR code
        qr_code_id: The unique 14-character identifier of the QR code
        fields: Comma-separated list of fields to include (code, prefilled_message, deep_link_url, creation_time, qr_image_url.format(SVG|PNG))
    """
    logger.info(
        f"[get_qr_code] phone_number_id={phone_number_id}, qr_code_id={qr_code_id}"
    )

    params = {}
    if fields:
        params["fields"] = fields

    resource_path = f"/{phone_number_id}/message_qrdls/{qr_code_id}"
    return make_whatsapp_request("GET", resource_path, api_key, params=params)


def delete_qr_code(
    api_key: str,
    phone_number_id: str,
    qr_code_id: str,
) -> Dict:
    """Permanently delete a WhatsApp Message QR code.

    Args:
        api_key: WhatsApp Cloud API access token
        phone_number_id: Your WhatsApp Business Account phone number ID that owns the QR code
        qr_code_id: The unique 14-character identifier of the QR code to delete
    """
    logger.info(
        f"[delete_qr_code] phone_number_id={phone_number_id}, qr_code_id={qr_code_id}"
    )

    resource_path = f"/{phone_number_id}/message_qrdls/{qr_code_id}"
    return make_whatsapp_request("DELETE", resource_path, api_key)


def get_whatsapp_business_profile(
    api_key: str,
    business_profile_id: str,
    fields: Optional[str] = None,
) -> Dict:
    """Retrieve WhatsApp Business Profile details.

    Args:
        api_key: WhatsApp Cloud API access token
        business_profile_id: Your WhatsApp Business Profile ID
        fields: Comma-separated list of fields to include (id, account_name, description, email, about, address, vertical, websites, profile_picture_url, messaging_product)
    """
    logger.info(
        f"[get_whatsapp_business_profile] business_profile_id={business_profile_id}"
    )

    params = {}
    if fields:
        params["fields"] = fields

    resource_path = f"/{business_profile_id}"
    return make_whatsapp_request("GET", resource_path, api_key, params=params)


def update_whatsapp_business_profile(
    api_key: str,
    business_profile_id: str,
    account_name: Optional[str] = None,
    description: Optional[str] = None,
    email: Optional[str] = None,
    about: Optional[str] = None,
    address: Optional[str] = None,
    vertical: Optional[str] = None,
    websites: Optional[list] = None,
    profile_picture_handle: Optional[str] = None,
) -> Dict:
    """Update WhatsApp Business Profile information.

    Args:
        api_key: WhatsApp Cloud API access token
        business_profile_id: Your WhatsApp Business Profile ID
        account_name: Name of the business account
        description: Business description text
        email: Contact email address
        about: About section text
        address: Physical address of the business
        vertical: Industry vertical classification (UNDEFINED, OTHER, AUTO, BEAUTY, APPAREL, EDU, ENTERTAIN, EVENT_PLAN, FINANCE, GROCERY, GOVT, HOTEL, HEALTH, NONPROFIT, PROF_SERVICES, RETAIL, TRAVEL, RESTAURANT, NOT_A_BIZ)
        websites: List of website URLs
        profile_picture_handle: Handle of profile picture from Resumable Upload API
    """
    logger.info(
        f"[update_whatsapp_business_profile] business_profile_id={business_profile_id}"
    )

    body = {"messaging_product": "whatsapp"}

    if account_name is not None:
        body["account_name"] = account_name
    if description is not None:
        body["description"] = description
    if email is not None:
        body["email"] = email
    if about is not None:
        body["about"] = about
    if address is not None:
        body["address"] = address
    if vertical is not None:
        body["vertical"] = vertical
    if websites is not None:
        body["websites"] = websites
    if profile_picture_handle is not None:
        body["profile_picture_handle"] = profile_picture_handle

    resource_path = f"/{business_profile_id}"
    return make_whatsapp_request("POST", resource_path, api_key, body=body)


def parse_graph_response(response_data: dict[str, Any]) -> dict[str, Any]:
    """Parse WhatsApp Graph API response."""
    return response_data
