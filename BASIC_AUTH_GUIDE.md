# HTTP Basic Authentication Guide

This API now uses **HTTP Basic Authentication** with username and password. No tokens needed!

## How It Works

Simply send your **username and password** with each request using HTTP Basic Authentication.

## Default Users

- **Username:** `admin`
- **Password:** `admin123`

- **Username:** `user`
- **Password:** `user123`

⚠️ **Change these passwords in production!**

## Using in Postman

### Step 1: Set Up Basic Auth

1. Create a new request (e.g., `GET /api/jasdatadaily`)
2. Go to **Authorization** tab
3. Select **Type:** `Basic Auth`
4. Enter:
   - **Username:** `admin`
   - **Password:** `admin123`
5. Click **Send**

That's it! Postman will automatically encode and send the credentials.

### Step 2: Use Environment Variables (Recommended)

1. Create/Select Environment (top right)
2. Add variables:
   - `username`: `admin`
   - `password`: `admin123`
3. In Authorization tab:
   - **Username:** `{{username}}`
   - **Password:** `{{password}}`

## Using with curl

```bash
curl -u admin:admin123 \
  "http://localhost:8000/api/jasdatadaily?date_from=2025-01-01&date_to=2025-01-31"
```

Or with explicit Basic Auth header:
```bash
curl -H "Authorization: Basic $(echo -n 'admin:admin123' | base64)" \
  "http://localhost:8000/api/jasdatadaily"
```

## Using with Python requests

```python
import requests

# Method 1: Using auth parameter (recommended)
response = requests.get(
    "http://localhost:8000/api/jasdatadaily",
    params={"date_from": "2025-01-01", "date_to": "2025-01-31"},
    auth=("admin", "admin123")
)

# Method 2: Using headers
import base64
credentials = base64.b64encode(b"admin:admin123").decode("utf-8")
response = requests.get(
    "http://localhost:8000/api/jasdatadaily",
    params={"date_from": "2025-01-01", "date_to": "2025-01-31"},
    headers={"Authorization": f"Basic {credentials}"}
)

print(response.json())
```

## Using in JavaScript/Fetch

```javascript
// Method 1: Using btoa (browser)
const username = 'admin';
const password = 'admin123';
const credentials = btoa(`${username}:${password}`);

fetch('http://localhost:8000/api/jasdatadaily?date_from=2025-01-01&date_to=2025-01-31', {
  headers: {
    'Authorization': `Basic ${credentials}`
  }
})
.then(response => response.json())
.then(data => console.log(data));

// Method 2: Using Buffer (Node.js)
const credentials = Buffer.from('admin:admin123').toString('base64');
fetch('http://localhost:8000/api/jasdatadaily', {
  headers: {
    'Authorization': `Basic ${credentials}`
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

## Using in FastAPI Docs (Swagger UI)

1. Go to http://localhost:8000/docs
2. Click **Authorize** button (top right)
3. Enter:
   - **Username:** `admin`
   - **Password:** `admin123`
4. Click **Authorize**
5. Now you can test protected endpoints!

## Protected Endpoints

These endpoints require username and password:

- `GET /api/jasdatadaily` - Get data with date filtering
- `GET /api/jasdatadaily/count` - Get count with date filtering
- `GET /api/auth/me` - Get current user info

## Public Endpoints

These endpoints don't require authentication:

- `GET /` - Welcome message
- `GET /health` - Health check

## How Basic Auth Works

HTTP Basic Authentication works by:
1. Combining username and password: `username:password`
2. Encoding it in Base64: `YWRtaW46YWRtaW4xMjM=`
3. Sending in Authorization header: `Authorization: Basic YWRtaW46YWRtaW4xMjM=`
4. Server decodes and validates credentials

## Security Notes

⚠️ **Important:**
- Always use **HTTPS** in production (Basic Auth sends credentials in base64, which is easily decoded)
- Change default passwords
- Consider rate limiting
- Use strong passwords

## Troubleshooting

### Error: "Incorrect username or password"
- Check username and password are correct
- Verify credentials are being sent (check Authorization header)
- Make sure you're using Basic Auth, not Bearer Token

### Error: 401 Unauthorized
- Verify credentials are correct
- Check Authorization header format: `Basic <base64_encoded_credentials>`
- Ensure endpoint requires authentication

### Not Working in Postman
- Make sure **Type** is set to `Basic Auth` (not Bearer Token)
- Check username and password fields are filled
- Try clearing and re-entering credentials

## Example: Complete Request Flow

**Request:**
```
GET /api/jasdatadaily?date_from=2025-01-01&date_to=2025-01-31
Authorization: Basic YWRtaW46YWRtaW4xMjM=
```

**Response:**
```json
{
  "total": 100,
  "count": 100,
  "date_from": "2025-01-01",
  "date_to": "2025-01-31",
  "data": [...]
}
```

## Benefits of Basic Auth

✅ **Simple** - No token management  
✅ **No expiration** - Credentials work until changed  
✅ **Standard** - Supported by all HTTP clients  
✅ **Easy to use** - Just username and password  

## Migration from Token Auth

If you were using tokens before:
- ❌ No need to login first
- ❌ No token to store/manage
- ❌ No token expiration to handle
- ✅ Just use username/password directly
