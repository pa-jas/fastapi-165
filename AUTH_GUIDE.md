# Authentication Guide

This FastAPI application uses JWT (JSON Web Tokens) for authentication.

## How to Use Authentication

### Step 1: Login to Get Token

**Endpoint:** `POST /api/auth/login`

**Request Format:**
- Content-Type: `application/x-www-form-urlencoded`
- Body:
  - `username`: Your username
  - `password`: Your password

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Example using Python requests:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/auth/login",
    data={"username": "admin", "password": "admin123"}
)
token_data = response.json()
access_token = token_data["access_token"]
print(f"Token: {access_token}")
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Step 2: Use Token to Access Protected Endpoints

**Add Authorization Header:**
```
Authorization: Bearer <your_access_token>
```

**Example using curl:**
```bash
curl -X GET "http://localhost:8000/api/jasdatadaily?date_from=2025-01-01&date_to=2025-01-31" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Example using Python requests:**
```python
import requests

token = "your_access_token_here"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(
    "http://localhost:8000/api/jasdatadaily",
    params={"date_from": "2025-01-01", "date_to": "2025-01-31"},
    headers=headers
)
data = response.json()
print(data)
```

### Step 3: Get Current User Info

**Endpoint:** `GET /api/auth/me`

**Example:**
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer <your_access_token>"
```

## Default Users

The application comes with two default users:

1. **Username:** `admin`
   - **Password:** `admin123`
   - ⚠️ **Change this in production!**

2. **Username:** `user`
   - **Password:** `user123`
   - ⚠️ **Change this in production!**

## Using in FastAPI Docs (Swagger UI)

1. Go to http://localhost:8000/docs
2. Click on the **Authorize** button (top right)
3. Click on `/api/auth/login` endpoint
4. Click "Try it out"
5. Enter username and password
6. Execute and copy the `access_token` from response
7. Click **Authorize** button again
8. Paste token in the "Value" field (format: `Bearer <token>`)
9. Click "Authorize" and "Close"
10. Now you can test protected endpoints!

## Protected Endpoints

The following endpoints require authentication:
- `GET /api/jasdatadaily` - Get data with date filtering
- `GET /api/jasdatadaily/count` - Get count with date filtering

## Public Endpoints

These endpoints don't require authentication:
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/auth/login` - Login endpoint

## Token Expiration

Tokens expire after **30 minutes** by default. You need to login again to get a new token.

## Security Notes

⚠️ **Important for Production:**

1. Change the `SECRET_KEY` in `config/auth.py` or use environment variable
2. Store users in a database instead of in-memory
3. Use strong passwords
4. Enable HTTPS in production
5. Consider adding rate limiting
6. Store passwords securely (already using bcrypt)

## Environment Variables

You can set the secret key using environment variable:

```bash
export SECRET_KEY="your-super-secret-key-here"
```

Or in Docker:
```bash
docker run -d -p 8000:8000 \
  -e SECRET_KEY="your-super-secret-key-here" \
  --name fastapi-container fastapi-app
```
