# How to Check/Verify JWT Tokens

This guide shows you different ways to check and verify your JWT tokens.

## Method 1: Using the API Endpoint (Recommended)

### Endpoint: `GET /api/auth/verify`

This endpoint verifies your token and returns detailed information.

### Option A: Using Query Parameter

**Request:**
```
GET http://localhost:8000/api/auth/verify?token=YOUR_TOKEN_HERE
```

**Example with curl:**
```bash
curl "http://localhost:8000/api/auth/verify?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Option B: Using Authorization Header

**Request:**
```
GET http://localhost:8000/api/auth/verify
Authorization: Bearer YOUR_TOKEN_HERE
```

**Example with curl:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  "http://localhost:8000/api/auth/verify"
```

### Response Example

**Valid Token:**
```json
{
  "valid": true,
  "expired": false,
  "username": "admin",
  "issued_at": "2025-01-15T10:30:00",
  "expires_at": "2025-01-15T11:00:00",
  "time_remaining": "25m 30s",
  "payload": {
    "sub": "admin",
    "exp": 1737028800,
    "iat": 1737027000
  },
  "error": null
}
```

**Expired Token:**
```json
{
  "valid": false,
  "expired": true,
  "username": "admin",
  "issued_at": "2025-01-15T10:00:00",
  "expires_at": "2025-01-15T10:30:00",
  "time_remaining": "Expired",
  "payload": {
    "sub": "admin",
    "exp": 1737027000,
    "iat": 1737025200
  },
  "error": "Token has expired"
}
```

**Invalid Token:**
```json
{
  "valid": false,
  "expired": false,
  "username": null,
  "issued_at": null,
  "expires_at": null,
  "time_remaining": null,
  "payload": null,
  "error": "Invalid token: ..."
}
```

## Method 2: Using Postman

### Step 1: Create Verify Request

1. **Method:** `GET`
2. **URL:** `http://localhost:8000/api/auth/verify`
3. **Option A - Query Parameter:**
   - Go to **Params** tab
   - Add: `token` = `{{access_token}}` (or paste token directly)
4. **Option B - Authorization Header:**
   - Go to **Authorization** tab
   - Type: `Bearer Token`
   - Token: `{{access_token}}`
5. **Click Send**

### Step 2: View Response

The response will show:
- ✅ **valid**: true/false
- ⏰ **expired**: true/false
- 👤 **username**: The user associated with the token
- 📅 **expires_at**: When the token expires
- ⏱️ **time_remaining**: How much time is left
- 📦 **payload**: Full JWT payload

## Method 3: Using Python

```python
import requests

# Your token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Check token
response = requests.get(
    "http://localhost:8000/api/auth/verify",
    params={"token": token}
    # OR use header:
    # headers={"Authorization": f"Bearer {token}"}
)

result = response.json()

print(f"Valid: {result['valid']}")
print(f"Expired: {result['expired']}")
print(f"Username: {result.get('username')}")
print(f"Time Remaining: {result.get('time_remaining')}")
print(f"Expires At: {result.get('expires_at')}")
```

## Method 4: Manual JWT Decoding (Online Tools)

You can decode JWT tokens (without verification) using online tools:

1. **jwt.io** - https://jwt.io
2. Paste your token
3. See the decoded payload

⚠️ **Note:** These tools only decode the token, they don't verify it. Use the API endpoint for proper verification.

## Method 5: Using the `/api/auth/me` Endpoint

This endpoint automatically verifies your token:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/auth/me"
```

**If token is valid:**
```json
{
  "username": "admin"
}
```

**If token is invalid/expired:**
```json
{
  "detail": "Could not validate credentials"
}
```

## Understanding Token Information

### Token Fields Explained

- **valid**: `true` if token signature is valid and not expired
- **expired**: `true` if token has passed its expiration time
- **username**: The username (from `sub` claim) in the token
- **issued_at**: When the token was created
- **expires_at**: When the token will expire (30 minutes after issue by default)
- **time_remaining**: Human-readable time until expiration
- **payload**: Complete JWT payload including all claims
- **error**: Error message if token is invalid

### Token Expiration

- Default expiration: **30 minutes**
- After expiration, you need to login again
- Check `time_remaining` to see how much time is left

## Quick Test Script

Save this as `check_token.py`:

```python
import requests
import sys

if len(sys.argv) < 2:
    print("Usage: python check_token.py <token>")
    sys.exit(1)

token = sys.argv[1]
base_url = "http://localhost:8000"

# Check token
response = requests.get(
    f"{base_url}/api/auth/verify",
    params={"token": token}
)

if response.status_code == 200:
    result = response.json()
    print("\n" + "="*50)
    print("TOKEN VERIFICATION RESULT")
    print("="*50)
    print(f"Valid:        {result['valid']}")
    print(f"Expired:      {result['expired']}")
    print(f"Username:     {result.get('username', 'N/A')}")
    print(f"Time Left:    {result.get('time_remaining', 'N/A')}")
    print(f"Expires At:   {result.get('expires_at', 'N/A')}")
    print(f"Error:        {result.get('error', 'None')}")
    print("="*50)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

**Usage:**
```bash
python check_token.py "your_token_here"
```

## Troubleshooting

### Token Always Shows Invalid

1. **Check token format:** Should be `eyJ...` (base64 encoded)
2. **Check if token is complete:** Tokens have 3 parts separated by dots
3. **Verify secret key:** Token must be signed with the same secret key

### Token Shows Expired

1. **Login again** to get a new token
2. **Check expiration time** in the response
3. **Default expiration is 30 minutes** - tokens expire quickly for security

### Can't Decode Token

1. **Verify token is complete** - no missing characters
2. **Check for extra spaces** in the token
3. **Ensure token starts with "Bearer "** if using Authorization header

## Best Practices

1. ✅ **Use `/api/auth/verify`** to check token validity
2. ✅ **Check `time_remaining`** before making requests
3. ✅ **Handle expired tokens** by logging in again
4. ✅ **Store tokens securely** - don't log or expose them
5. ✅ **Use environment variables** for tokens in scripts
