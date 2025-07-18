#!/usr/bin/env python3
"""
TickTick OAuth2 Access Token Generator

This script implements the TickTick OAuth2 flow to obtain an access token.
It requires the following environment variables or .env file:
- TICKTICK_CLIENT_ID: Your TickTick application client ID
- TICKTICK_CLIENT_SECRET: Your TickTick application client secret
- TICKTICK_REDIRECT_URI: Your configured redirect URI
- TICKTICK_SCOPE: Permission scope (e.g., "tasks:read tasks:write")

Usage:
    1. Copy .env.example to .env and fill in your credentials
    2. Run: python get_access_token.py
"""

import os
import sys
import urllib.parse
import requests
import base64
import time
from dotenv import load_dotenv


def get_config_from_env():
    """Get configuration from environment variables or .env file"""
    # Load environment variables from .env file
    load_dotenv()
    
    config = {}
    required_vars = [
        'TICKTICK_CLIENT_ID',
        'TICKTICK_CLIENT_SECRET', 
        'TICKTICK_REDIRECT_URI',
        'TICKTICK_SCOPE'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            print(f"Error: Environment variable {var} is required but not set")
            print("Please check your .env file or environment variables")
            sys.exit(1)
        config[var.lower().replace('ticktick_', '')] = value
    
    return config


def build_authorization_url(config, state):
    """Build the authorization URL for step 1"""
    base_url = "https://ticktick.com/oauth/authorize"
    params = {
        'client_id': config['client_id'],
        'scope': config['scope'],
        'state': state,
        'redirect_uri': config['redirect_uri'],
        'response_type': 'code'
    }
    
    return f"{base_url}?{urllib.parse.urlencode(params)}"


def exchange_code_for_token(config, auth_code):
    """Exchange authorization code for access token (step 3)"""
    token_url = "https://ticktick.com/oauth/token"
    
    # Prepare Basic Auth header
    credentials = f"{config['client_id']}:{config['client_secret']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'code': auth_code,
        'grant_type': 'authorization_code',
        'scope': config['scope'],
        'redirect_uri': config['redirect_uri']
    }
    
    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        return token_data
    
    except requests.RequestException as e:
        print(f"Error exchanging code for token: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None


def main():
    """Main function to orchestrate the OAuth flow"""
    print("TickTick OAuth2 Access Token Generator")
    print("=" * 40)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✓ Found .env file")
    else:
        print("⚠ No .env file found. Make sure to set environment variables or copy .env.example to .env")
    
    # Get configuration from environment
    config = get_config_from_env()
    
    print(f"Client ID: {config['client_id']}")
    print(f"Scope: {config['scope']}")
    print(f"Redirect URI: {config['redirect_uri']}")
    print()
    
    # Generate a simple state parameter
    state = f"ticktick_oauth_{int(time.time())}"
    
    # Step 1: Build authorization URL
    auth_url = build_authorization_url(config, state)
    
    print("Step 1: Authorization")
    print(f"Please visit the following URL to authorize the application:")
    print(f"\n{auth_url}\n")
    
    print("After authorizing, you will be redirected to your redirect URI.")
    print("Please copy the 'code' parameter from the redirect URL and paste it below:")
    
    # Get authorization code from user
    auth_code = input("Authorization code: ").strip()
    
    if not auth_code:
        print("Error: No authorization code provided")
        sys.exit(1)
    
    print(f"\nStep 2: Received authorization code: {auth_code[:10]}...")
    
    # Step 3: Exchange code for token
    print("\nStep 3: Exchanging authorization code for access token...")
    
    token_data = exchange_code_for_token(config, auth_code)
    
    if token_data and 'access_token' in token_data:
        print("\n" + "=" * 50)
        print("SUCCESS! Access token obtained:")
        print("=" * 50)
        print(f"Access Token: {token_data['access_token']}")
        
        if 'expires_in' in token_data:
            print(f"Expires in: {token_data['expires_in']} seconds")
        
        if 'refresh_token' in token_data:
            print(f"Refresh Token: {token_data['refresh_token']}")
        
        if 'scope' in token_data:
            print(f"Granted Scope: {token_data['scope']}")
        
        print("\nYou can now use this access token to make API requests to TickTick.")
        print("Set it as an environment variable:")
        print(f"export TICKTICK_ACCESS_TOKEN='{token_data['access_token']}'")
        
    else:
        print("\nError: Failed to obtain access token")
        sys.exit(1)


if __name__ == "__main__":
    main()
