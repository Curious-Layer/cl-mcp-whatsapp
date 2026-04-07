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
