# Getting TickTick Access Token

This guide explains how to obtain an OAuth2 access token for the TickTick API.

## Prerequisites

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get TickTick Developer Credentials:**
   - Register at [TickTick Developer Center](https://developer.ticktick.com/)
   - Create a new application
   - Note your `client_id` and `client_secret`

## Setup

1. **Configure credentials:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your TickTick application credentials:**
   - `TICKTICK_CLIENT_ID`: Your application's client ID
   - `TICKTICK_CLIENT_SECRET`: Your application's client secret  
   - `TICKTICK_REDIRECT_URI`: Your configured redirect URI (e.g., `http://localhost:8080/callback`)
   - `TICKTICK_SCOPE`: Permission scope (e.g., `tasks:read`)

3. **Important:** In the TickTick Developer Center, you must add your `redirect_uri` to the allowed redirect URIs list for your application.

## Get Access Token

Run the OAuth flow to get your access token:

```bash
python3 get_access_token.py
```

The script will:
1. Display the TickTick authorization URL
2. Wait for you to paste the authorization code from the redirect URL
3. Exchange it for an access token
4. Display the access token for use in API requests

## Troubleshooting

### "invalid_request" - redirect_uri error

If you get an error like:
```
OAuth Error: error="invalid_request", error_description="At least one redirect_uri must be registered with the client."
```

This means you need to register your redirect URI in the TickTick Developer Center:

1. Go to [TickTick Developer Center](https://developer.ticktick.com/)
2. Edit your application settings
3. Add your redirect URI (e.g., `http://localhost:8080/callback`) to the allowed redirect URIs list
4. Save the changes and try again

## Environment Variables Reference

Required variables (set in `.env` file):
- `TICKTICK_CLIENT_ID`: Your application's client ID
- `TICKTICK_CLIENT_SECRET`: Your application's client secret  
- `TICKTICK_REDIRECT_URI`: Your configured redirect URI
- `TICKTICK_SCOPE`: Permission scope (space-separated)

## API Endpoints

Based on the TickTick Open API OAuth2 flow:
- Authorization endpoint: `https://ticktick.com/oauth/authorize`
- Token endpoint: `https://ticktick.com/oauth/token`
- Available scopes: `tasks:read`, `tasks:write`
