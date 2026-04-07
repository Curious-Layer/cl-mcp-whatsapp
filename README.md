Send and manage WhatsApp messages via the WhatsApp Cloud API.

A Model Context Protocol (MCP) server that exposes the WhatsApp Cloud API for sending messages, managing media, and handling message workflows.

---

## Overview

The WhatsApp MCP Server provides stateless, multi-user messaging capabilities:

- **Text messaging** - Send plain text messages to WhatsApp contacts
- **Template messages** - Send pre-approved message templates for bulk messaging
- **Media sharing** - Send images, videos, audio, and documents
- **Connection testing** - Verify API credentials and phone number configuration
- **Media retrieval** - Fetch attachment URLs from received messages

Perfect for:

- Building WhatsApp bot integrations
- Automated customer notifications
- Bulk messaging campaigns with templates
- Media-rich customer communications
- AI agent-powered WhatsApp workflows

---

## Tools

<details>
<summary><code>health_check</code> — Server readiness verification</summary>

Returns the current health status of the MCP server.

**Inputs:**

None

**Output:**

```json
{
  "status": "ok",
  "server": "CL WhatsApp MCP Server"
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/health_check
```

</details>

<details>
<summary><code>send_text_message</code> — Send a text message</summary>

Send a plain text message to a WhatsApp contact using the 24-hour customer service window or an active conversation thread.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID
- `recipient_phone` (string, required) — Recipient's phone number with country code (e.g., `917823846641`)
- `message_text` (string, required) — Text content of the message

**Output:**

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{"input": "917823846641", "wa_id": "917823846641"}],
  "messages": [{"id": "wamid.xyz...", "message_status": "accepted"}]
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/send_text_message \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "recipient_phone": "917823846641",
    "message_text": "Hello from WhatsApp API!"
  }'
```

</details>

<details>
<summary><code>send_template_message</code> — Send a pre-approved template</summary>

Send a template message that has been pre-approved by WhatsApp. Templates have no delivery restrictions and work for cold outreach.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID
- `recipient_phone` (string, required) — Recipient's phone number with country code
- `template_name` (string, required) — Name of the approved template (e.g., `hello_world`)
- `template_language_code` (string, optional, default: `en_US`) — Template language code (e.g., `en_US`, `es_ES`)
- `parameters` (array, optional) — List of parameter values to populate template variables

**Output:**

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{"input": "917823846641", "wa_id": "917823846641"}],
  "messages": [{"id": "wamid.xyz...", "message_status": "accepted"}]
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/send_template_message \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "recipient_phone": "917823846641",
    "template_name": "hello_world",
    "template_language_code": "en_US"
  }'
```

</details>

<details>
<summary><code>send_media_message</code> — Send image, video, audio, or document</summary>

Send media files to a WhatsApp contact using direct URLs (within 24-hour window or active thread).

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID
- `recipient_phone` (string, required) — Recipient's phone number with country code
- `media_type` (string, required) — Type of media: `image`, `video`, `audio`, or `document`
- `media_url` (string, required) — Public URL of the media file
- `caption` (string, optional) — Caption text (image and video only)

**Output:**

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{"input": "917823846641", "wa_id": "917823846641"}],
  "messages": [{"id": "wamid.xyz...", "message_status": "accepted"}]
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/send_media_message \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "recipient_phone": "917823846641",
    "media_type": "image",
    "media_url": "https://example.com/image.jpg",
    "caption": "Check this out!"
  }'
```

</details>

<details>
<summary><code>send_marketing_template_message</code> — Send marketing template messages</summary>

Send pre-approved marketing template messages with optional policy controls and activity sharing settings. Marketing templates are not subject to the 24-hour message window restrictions.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID
- `recipient_phone` (string, required) — Recipient's phone number with country code (e.g., `917823846641`)
- `template_name` (string, required) — Name of the approved marketing template
- `template_language_code` (string, optional, default: `en_US`) — Template language code (e.g., `en_US`, `es_ES`)
- `components` (array, optional) — Array of template components containing parameter values
- `product_policy` (string, optional) — Product policy setting: `CLOUD_API_FALLBACK` or `STRICT`
- `message_activity_sharing` (boolean, optional) — Flag to control message activity sharing

**Output:**

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{"input": "917823846641", "wa_id": "917823846641"}],
  "messages": [
    {
      "id": "wamid.xyz...",
      "message_status": "accepted"
    }
  ]
}
```

Possible message statuses:
- `accepted` - Message has been accepted by WhatsApp and is being processed
- `held_for_quality_assessment` - Message is being held for quality assessment before delivery
- `paused` - Message delivery has been paused

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/send_marketing_template_message \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "recipient_phone": "917823846641",
    "template_name": "marketing_promotion",
    "template_language_code": "en_US",
    "product_policy": "CLOUD_API_FALLBACK"
  }'
```

</details>

<details>
<summary><code>test_connection</code> — Verify API credentials and phone number</summary>

Test your WhatsApp Cloud API connection and phone number configuration. Retrieves phone number details and quality rating.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID

**Output:**

```json
{
  "id": "1077755395418019",
  "display_phone_number": "+1 (555) 555-1234",
  "quality_rating": "GREEN"
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/test_connection \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019"
  }'
```

</details>

<details>
<summary><code>get_message_attachment</code> — Retrieve media URL</summary>

Fetch the download URL for media attachments from received messages (images, videos, documents, audio).

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `media_id` (string, required) — ID of the media attachment

**Output:**

```json
{
  "id": "media_id",
  "url": "https://media.graph.facebook.com/...",
  "media_product_type": "MESSAGES"
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/get_message_attachment \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "media_id": "12345"
  }'
```

</details>

<details>
<summary><code>get_message_history_events</code> — Query message delivery status events</summary>

Retrieve paginated delivery status events for messages using the WhatsApp Message History API. Supports filtering by status and pagination.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `message_history_id` (string, required) — WhatsApp Business Message History ID
- `status_filter` (string, optional) — Filter by status: `ACCEPTED`, `DELIVERED`, `ERROR`, `READ`, `SENT`
- `fields` (string, optional) — Comma-separated fields to include (e.g., `id,delivery_status,error_description,occurrence_timestamp,status_timestamp`)
- `limit` (integer, optional, default: 25) — Max events per page (1-100)
- `after` (string, optional) — Pagination cursor for next page
- `before` (string, optional) — Pagination cursor for previous page

**Output:**

```json
{
  "data": [
    {
      "id": "event_id",
      "delivery_status": "DELIVERED",
      "occurrence_timestamp": 1234567890,
      "status_timestamp": 1234567891
    }
  ],
  "paging": {
    "cursors": {
      "after": "next_cursor",
      "before": "prev_cursor"
    }
  }
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/get_message_history_events \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "message_history_id": "123456789",
    "status_filter": "DELIVERED",
    "limit": 50
  }'
```

</details>

<details>
<summary><code>configure_conversational_automation</code> — Configure bot automation settings</summary>

Configure conversational automation settings for a WhatsApp Business Account phone number, including welcome messages, conversation prompts, and bot commands.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID
- `enable_welcome_message` (boolean, optional) — Enable/disable welcome messages for new conversations
- `prompts` (array, optional) — List of conversation prompts (ice breakers) to guide customer interactions
- `commands` (array, optional) — List of bot commands with `command_name` and `command_description` keys

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/configure_conversational_automation \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "enable_welcome_message": true,
    "prompts": ["How can I help you?", "What do you need?"],
    "commands": [
      {
        "command_name": "help",
        "command_description": "Get help with your order"
      },
      {
        "command_name": "status",
        "command_description": "Check your order status"
      }
    ]
  }'
```

</details>

<details>
<summary><code>get_bot_details</code> — Retrieve bot configuration details</summary>

Fetch WhatsApp Business Bot configuration including id, prompts, commands, and welcome message settings.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `bot_id` (string, required) — WhatsApp Business Bot ID
- `fields` (string, optional) — Comma-separated fields to include (e.g., `id,prompts,commands,enable_welcome_message`)

**Output:**

```json
{
  "id": "123456789",
  "enable_welcome_message": true,
  "prompts": ["How can I help you?", "What do you need?"],
  "commands": [
    {
      "command_name": "help",
      "command_description": "Get help with your order"
    }
  ]
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/get_bot_details \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "bot_id": "123456789",
    "fields": "id,prompts,commands,enable_welcome_message"
  }'
```

</details>

<details>
<summary><code>check_call_permissions</code> — Check WhatsApp call permissions</summary>

Check whether you have permission to call a WhatsApp user and retrieve available actions and rate limits.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID
- `user_wa_id` (string, required) — The WhatsApp ID of the user to check call permissions for

**Output:**

```json
{
  "messaging_product": "whatsapp",
  "permission": {
    "status": "granted",
    "expiration_time": 1234567890
  },
  "actions": [
    {
      "action_name": "start_call",
      "can_perform_action": true,
      "limits": [
        {
          "time_period": "24h",
          "current_usage": 5,
          "max_allowed": 100,
          "limit_expiration_time": 1234567890
        }
      ]
    }
  ]
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/check_call_permissions \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "user_wa_id": "917823846641"
  }'
```

**Permission Statuses:**
- `granted` - You have active permission to call this user
- `pending` - A permission request has been sent but not yet approved
- `denied` - The user has denied call permissions
- `expired` - Previous permission has expired

</details>

<details>
<summary><code>manage_call</code> — Initiate, accept, reject, or terminate calls</summary>

Manage WhatsApp calls with actions to connect, accept, reject, or terminate. Supports session description protocol (SDP) for call setup.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID
- `action` (string, required) — Call action: `connect`, `pre_accept`, `accept`, `reject`, or `terminate`
- `to` (string, optional) — The WhatsApp number being called (required for connect/pre_accept/accept/reject)
- `call_id` (string, optional) — The WhatsApp call ID (required for terminate action)
- `session` (object, optional) — Session description protocol with `sdp_type` (offer/answer) and `sdp` string
- `biz_opaque_callback_data` (string, optional) — Arbitrary string for tracking (max 512 characters)

**Output:**

```json
{
  "messaging_product": "whatsapp",
  "calls": [
    {
      "id": "call_id_123"
    }
  ]
}
```

Or for terminate:

```json
{
  "success": true
}
```

**Usage Examples:**

Initiate a call:
```bash
curl -X POST http://localhost:8000/tools/manage_call \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "action": "connect",
    "to": "917823846641",
    "session": {
      "sdp_type": "offer",
      "sdp": "v=0\r\no=- ..."
    }
  }'
```

Terminate a call:
```bash
curl -X POST http://localhost:8000/tools/manage_call \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "action": "terminate",
    "call_id": "call_id_123"
  }'
```

**Available Actions:**
- `connect` - Initiate a new call to a user (requires `to` and session SDP)
- `pre_accept` - Pre-accept a call
- `accept` - Accept an incoming call (requires session SDP with type "answer")
- `reject` - Reject a call
- `terminate` - End an active call (requires `call_id`)

</details>

<details>
<summary><code>get_qr_code</code> — Retrieve QR code details and image</summary>

Retrieve details for a WhatsApp Message QR code including the image URL for use in marketing materials.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID
- `qr_code_id` (string, required) — The unique 14-character identifier of the QR code
- `fields` (string, optional) — Comma-separated fields to include (e.g., `code,prefilled_message,deep_link_url,qr_image_url.format(SVG)`)

**Output:**

```json
{
  "data": [
    {
      "code": "dcbf1f8edc4f6d",
      "prefilled_message": "Hello from WhatsApp!",
      "deep_link_url": "https://wa.me/...",
      "qr_image_url": "https://graph.facebook.com/v21.0/..."
    }
  ]
}
```

**Available Fields:**
- `code` - QR code identifier (always included)
- `prefilled_message` - Pre-filled message text (always included)
- `deep_link_url` - WhatsApp deep link URL (always included)
- `creation_time` - Unix timestamp when QR code was created (first-party apps only)
- `qr_image_url.format(SVG|PNG)` - QR code image URL in specified format

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/get_qr_code \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "qr_code_id": "dcbf1f8edc4f6d",
    "fields": "code,prefilled_message,qr_image_url.format(PNG)"
  }'
```

</details>

<details>
<summary><code>delete_qr_code</code> — Delete a QR code permanently</summary>

Permanently delete a WhatsApp Message QR code. Once deleted, the QR code and associated deep link become invalid. This action cannot be undone.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `phone_number_id` (string, required) — Your WhatsApp Business Account phone number ID
- `qr_code_id` (string, required) — The unique 14-character identifier of the QR code to delete

**Output:**

```json
{
  "success": true
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/delete_qr_code \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "phone_number_id": "1077755395418019",
    "qr_code_id": "dcbf1f8edc4f6d"
  }'
```

</details>

<details>
<summary><code>get_whatsapp_business_profile</code> — Retrieve business profile details</summary>

Retrieve comprehensive information about your WhatsApp Business Profile including account name, description, contact details, business vertical, websites, and profile picture.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `business_profile_id` (string, required) — Your WhatsApp Business Profile ID
- `fields` (string, optional) — Comma-separated fields to include (e.g., `id,account_name,description,email,about,address,vertical,websites,profile_picture_url`)

**Output:**

```json
{
  "id": "123456789",
  "account_name": "My Business",
  "description": "Business description",
  "email": "contact@business.com",
  "about": "About section text",
  "address": "123 Main Street, City, State",
  "vertical": "RETAIL",
  "websites": ["https://example.com"],
  "profile_picture_url": "https://graph.facebook.com/...",
  "messaging_product": "whatsapp"
}
```

**Available Verticals:**
UNDEFINED, OTHER, AUTO, BEAUTY, APPAREL, EDU, ENTERTAIN, EVENT_PLAN, FINANCE, GROCERY, GOVT, HOTEL, HEALTH, NONPROFIT, PROF_SERVICES, RETAIL, TRAVEL, RESTAURANT, NOT_A_BIZ

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/get_whatsapp_business_profile \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "business_profile_id": "123456789",
    "fields": "id,account_name,description,email,vertical,websites"
  }'
```

</details>

<details>
<summary><code>update_whatsapp_business_profile</code> — Update business profile information</summary>

Update your WhatsApp Business Profile with current business information, contact details, and configuration. All fields are optional.

**Inputs:**

- `api_key` (string, required) — WhatsApp Cloud API access token
- `business_profile_id` (string, required) — Your WhatsApp Business Profile ID
- `account_name` (string, optional) — Name of the business account
- `description` (string, optional) — Business description text
- `email` (string, optional) — Contact email address
- `about` (string, optional) — About section text
- `address` (string, optional) — Physical address of the business
- `vertical` (string, optional) — Industry vertical classification
- `websites` (array, optional) — List of website URLs associated with the business
- `profile_picture_handle` (string, optional) — Handle of profile picture from Resumable Upload API

**Output:**

```json
{
  "id": "123456789",
  "success": true
}
```

**Usage Example:**

```bash
curl -X POST http://localhost:8000/tools/update_whatsapp_business_profile \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "YOUR_API_KEY",
    "business_profile_id": "123456789",
    "account_name": "Updated Business Name",
    "description": "Updated business description",
    "email": "newemail@business.com",
    "address": "456 New Street, City, State",
    "vertical": "RETAIL",
    "websites": ["https://newsite.com", "https://shop.com"]
  }'
```

</details>

---

## API Parameters Reference

<details>
<summary><strong>Common Parameters</strong></summary>

- `api_key` (string, required) — System user access token used as `Authorization: Bearer <token>`.
- `phone_number_id` (string, required for send/test tools) — WhatsApp Business phone number ID used in Graph API paths.
- `recipient_phone` (string, required for send tools) — WhatsApp user phone number in international format, digits only, include country code (no `+`, spaces, or leading zero).
- `media_id` (string, required for attachment tool) — Media object ID returned by WhatsApp.
- `message_text` (string, required for text messages) — Text body to send.
- `template_name` (string, required for template messages) — Approved template name in your WhatsApp Business Account.
- `template_language_code` (string, optional, default `en_US`) — Template locale code.
- `parameters` (array, optional) — Template body parameters in WhatsApp template parameter format.
- `media_type` (string, required for media messages) — One of: `image`, `video`, `audio`, `document`.
- `media_url` (string, required for media messages) — Publicly accessible media URL.
- `caption` (string, optional) — Caption for `image` and `video` media types.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Phone Number ID:**

```
Numeric string
Example: 1077755395418019
```

**WhatsApp Business Account ID:**

```
Numeric string
Example: 215589313241560883
```

**Recipient Phone Number:**

```
Country code + subscriber number (digits only)
Example: 14155552671
```

**Media ID:**

```
Media object ID returned by WhatsApp
Example: 123456789012345
```

</details>

---

## Authentication Guide

<details>
<summary><strong>How to Get Required Credentials</strong></summary>

This server requires three values:

- `api_key` (system user access token)
- `phone_number_id`
- `whatsapp_business_account_id`

### Prerequisites

1. You have a Facebook account or a managed Meta account.
2. You are registered as a Meta developer.
3. You have access to a device with WhatsApp installed for test messaging.

If you are not registered as a developer, register at:
[https://developers.facebook.com/async/registration/](https://developers.facebook.com/async/registration/)

### Step 1: Create a Meta App with WhatsApp Use Case

1. Open the App Dashboard in [Meta for Developers](https://developers.facebook.com/).
2. If you already have an app:
  - Select the app.
  - Click **Add use cases**.
  - Choose **Connect with customers through WhatsApp**.
3. If you do not have an app:
  - Create a new app.
  - Choose **Connect with customers through WhatsApp** use case.
  - Select an existing Business Portfolio or create one.

### Step 2: Connect App to WhatsApp Business Account

1. In App Dashboard, open your app.
2. Click **Use cases** (pencil icon).
3. Under **Connect with customers through WhatsApp**, click **Customize**.
4. In **API Setup**, choose one:
  - Select an existing WhatsApp Business Account, or
  - Create a new WhatsApp Business Account.
5. Save your **WhatsApp Business Account ID** from the API Setup panel.

### Step 3: Capture Phone Number ID

1. In the same WhatsApp API setup flow / quickstart, send the `hello_world` template message.
2. Save your test business **Phone Number ID** from the setup panel.

### Step 4: Generate Permanent System User Access Token

1. Open **Business Settings**.
2. Go to **System users**.
3. Create a new system user.
4. Click **Assign Assets** and grant full control to:
  - Your app (`Manage app`)
  - Your WhatsApp account (`Manage WhatsApp Business Accounts`)
5. Click **Generate token**.
6. Add permissions:
  - `business_management`
  - `whatsapp_business_messaging`
  - `whatsapp_business_management`
7. Copy and securely store this token.

### Step 5: Use These Values in This MCP Server

Use the credentials in tool calls:

- `api_key` = system user access token
- `phone_number_id` = business phone number ID
- `whatsapp_business_account_id` = business account ID (store for your operational use and Graph API workflows)

Optional local env mapping:

```env
WHATSAPP_API_KEY=YOUR_SYSTEM_USER_ACCESS_TOKEN
PHONE_NUMBER_ID=YOUR_PHONE_NUMBER_ID
WHATSAPP_BUSINESS_ACCOUNT_ID=YOUR_BUSINESS_ACCOUNT_ID
```

Reference:
[https://developers.facebook.com/docs/whatsapp/cloud-api/get-started](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)

</details>

---

## Troubleshooting

<details>
<summary><strong>Common Issues & Solutions</strong></summary>

### **Error: "Object with ID does not exist"**

- **Cause:** Wrong `phone_number_id` or not linked to your access token
- **Solution:**
  1. Verify `phone_number_id` in WhatsApp Business Manager
  2. Confirm phone number is verified
  3. Check token has `whatsapp_business_messaging` scope

### **Message Accepted but Not Delivered**

- **Cause:** Outside 24-hour customer service window
- **Solution:**
  1. Ask user to message you first OR
  2. Use a template message instead
  3. Use `send_template_message` tool (unrestricted)

### **"Invalid Access Token" Error**

- **Cause:** Token expired or invalid
- **Solution:**
  1. Regenerate token in Business Manager
  2. Verify token has required scopes
  3. Check token is not revoked

### **"Invalid Recipient Phone Number"**

- **Cause:** Phone number format incorrect
- **Solution:**
  1. Use format: Country Code + Number (no + or 0)
  2. Example: `917823846641` (not `+917823846641`)
  3. Verify number is a valid WhatsApp user

### **Media URL Not Accessible**

- **Cause:** URL expired or requires authentication
- **Solution:**
  1. Ensure URL is publicly accessible
  2. Use direct media URLs (not requiring login)
  3. Check media file size is within limits

### **Rate Limit Exceeded**

- **Cause:** Too many API calls in short timeframe
- **Solution:**
  1. Implement exponential backoff retry logic
  2. Space out API calls
  3. Check rate limits in Meta Business settings

</details>

---

## Resources

<details>
<summary><strong>External Documentation</strong></summary>

- **[WhatsApp Cloud API Docs](https://developers.facebook.com/docs/whatsapp/cloud-api)** — Official API reference
- **[Getting Started Guide](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)** — Setup and first message
- **[Message Templates](https://developers.facebook.com/docs/whatsapp/message-templates/manage-templates)** — Template management
- **[Error Codes Reference](https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes)** — API error codes
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — MCP framework specification

</details>

---
