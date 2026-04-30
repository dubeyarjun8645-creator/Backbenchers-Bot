import json
import base64
import requests
import jwt
import os
import re
from datetime import datetime, timezone

class SecureAPIClient:
    def __init__(self):
        self.html_url = "https://xindex.netlify.app/xindex"
        # Secret handle through env or default
        self.jwt_secret = os.getenv('JWT_SECRET', 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpc3MiOiAic2VjdXJlLWFwaS1zeXN0ZW0iLCAiYXVkIjogImFwaS1kYXNoYm9hcmQiLCAiaWF0IjogMTc1MzIzNjY0MywgImV4cCI6IDE3ODkyMTUwNDMsICJjdXN0b21fZGF0YSI6IHsidXNlcl9yb2xlIjogImFkbWluIn19._O30-nacUDNahkYgBCZp9ZnL0_7itDsHx5W9cnVxiQ0')
        self.apis = {}

    def generate_token(self):
        """Generate JWT token for secure API access"""
        payload = {
            'user_id': 'api_client',
            'exp': datetime.now(timezone.utc).timestamp() + 3600,
            'iat': datetime.now(timezone.utc).timestamp(),
            'authorized': True
        }
        # Fixed: Ensuring the secret is handled correctly as a string
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')

    def decode_apis(self, encoded):
        """Decode base64 encoded API endpoints"""
        decoded = {}
        for k, v in encoded.items():
            try:
                decoded[k] = base64.b64decode(v).decode('utf-8')
            except Exception:
                decoded[k] = None
        return decoded

    def fetch_apis(self):
        """Fetch and parse APIs from the secure HTML data script"""
        token = self.generate_token()
        url = f"{self.html_url}?view_apis=true&auth={token}"

        headers = {
            'User-Agent': 'SecureClient',
            'X-API-Key': 'XUGKEYPRO',
            'Referer': 'https://xindex.netlify.app'
        }

        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code != 200:
                print(f"Server returned status: {res.status_code}")
                return False

            # Search for the hidden JSON data in script tag
            match = re.search(r'<script id="secure-data"[^>]*>(.*?)</script>', res.text, re.DOTALL)
            if not match:
                print("Security Error: No secure-data script found.")
                return False

            raw_json = match.group(1).strip()
            encoded_apis = json.loads(raw_json)

            self.apis = self.decode_apis(encoded_apis)
            return True

        except Exception as e:
            print(f"Fatal Error fetching APIs: {e}")
            return False

    def get_apis(self):
        """Public method to retrieve the API dictionary"""
        if not self.apis:
            self.fetch_apis()
        return self.apis
