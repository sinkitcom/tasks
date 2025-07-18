# ticktick-export

A tool to export data from TickTick using their API.

## Getting Started

### Step 1: Obtain Access Token

Before you can export your TickTick data, you need to get an OAuth2 access token.

#### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure credentials:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your TickTick application credentials:
   - Get your `client_id` and `client_secret` from [TickTick Developer Center](https://developer.ticktick.com/)
   - **Important:** In the TickTick Developer Center, you must add your `redirect_uri` to the allowed redirect URIs list for your application
   - Set your `redirect_uri` in `.env` (e.g., `http://localhost:8080/callback` or `https://example.com/callback`)
   - Configure `scope` (e.g., `tasks:read`)

#### Get Access Token

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

### Step 2: Export Your Data

*Coming soon - scripts to export tasks, projects, and other TickTick data*

## Development

### OAuth2 Flow Details

#### Environment Variables

Required variables (set in `.env` file):
- `TICKTICK_CLIENT_ID`: Your application's client ID
- `TICKTICK_CLIENT_SECRET`: Your application's client secret  
- `TICKTICK_REDIRECT_URI`: Your configured redirect URI
- `TICKTICK_SCOPE`: Permission scope (space-separated)

#### API Endpoints

Based on the TickTick Open API OAuth2 flow:
- Authorization endpoint: `https://ticktick.com/oauth/authorize`
- Token endpoint: `https://ticktick.com/oauth/token`
- Available scopes: `tasks:read`, `tasks:write`
