# Using FastAPI Authentication with Postman

This guide shows you how to use JWT authentication in Postman to test the FastAPI endpoints.

## Step 1: Login to Get Access Token

### Create Login Request

1. **Create a new request** in Postman
2. **Set method to:** `POST`
3. **Set URL to:** `http://localhost:8000/api/auth/login`
4. **Go to Body tab:**
   - Select `x-www-form-urlencoded`
   - Add two key-value pairs:
     - Key: `username`, Value: `admin`
     - Key: `password`, Value: `admin123`
5. **Click Send**

### Expected Response

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcw...",
    "token_type": "bearer"
}
```

### Save Token to Environment Variable (Recommended)

1. **Create/Select Environment** (top right corner)
2. **After login response, add this script in Tests tab:**
   ```javascript
   if (pm.response.code === 200) {
       var jsonData = pm.response.json();
       pm.environment.set("access_token", jsonData.access_token);
       console.log("Token saved to environment variable");
   }
   ```
3. **Run the login request again** - Token will be automatically saved

## Step 2: Use Token in Protected Endpoints

### Method 1: Manual Authorization Header

1. **Create a new request** (e.g., GET `/api/jasdatadaily`)
2. **Go to Authorization tab:**
   - Type: Select `Bearer Token`
   - Token: Paste your access token (or use `{{access_token}}` if saved in environment)
3. **Add query parameters** (if needed):
   - Go to Params tab
   - Add `date_from`: `2025-01-01`
   - Add `date_to`: `2025-01-31`
4. **Click Send**

### Method 2: Using Environment Variable

If you saved the token to an environment variable:

1. **Go to Authorization tab:**
   - Type: `Bearer Token`
   - Token: `{{access_token}}`
2. Postman will automatically use the token from your environment

## Step 3: Complete Postman Collection Setup

### Create a Collection

1. **Create New Collection** (e.g., "FastAPI")
2. **Add requests:**
   - `Login` - POST `/api/auth/login`
   - `Get JasDataDaily` - GET `/api/jasdatadaily`
   - `Get Count` - GET `/api/jasdatadaily/count`
   - `Get Current User` - GET `/api/auth/me`
   - `Health Check` - GET `/health`

### Collection-Level Authorization

1. **Select your Collection**
2. **Go to Authorization tab**
3. **Type:** `Bearer Token`
4. **Token:** `{{access_token}}`
5. All requests in the collection will use this token automatically

## Example Requests

### 1. Login Request

**Method:** `POST`  
**URL:** `http://localhost:8000/api/auth/login`  
**Body (x-www-form-urlencoded):**
```
username: admin
password: admin123
```

### 2. Get JasDataDaily (Protected)

**Method:** `GET`  
**URL:** `http://localhost:8000/api/jasdatadaily`  
**Authorization:** Bearer Token `{{access_token}}`  
**Params:**
```
date_from: 2025-01-01
date_to: 2025-01-31
```

### 3. Get Count (Protected)

**Method:** `GET`  
**URL:** `http://localhost:8000/api/jasdatadaily/count`  
**Authorization:** Bearer Token `{{access_token}}`  
**Params (optional):**
```
date_from: 2025-01-01
date_to: 2025-01-31
```

### 4. Get Current User (Protected)

**Method:** `GET`  
**URL:** `http://localhost:8000/api/auth/me`  
**Authorization:** Bearer Token `{{access_token}}`

### 5. Health Check (Public - No Auth)

**Method:** `GET`  
**URL:** `http://localhost:8000/health`  
**Authorization:** None needed

## Postman Environment Setup

### Create Environment Variables

1. **Click Environment icon** (top right)
2. **Click + to create new environment**
3. **Name it:** "FastAPI Local"
4. **Add variables:**
   - `base_url`: `http://localhost:8000`
   - `access_token`: (leave empty, will be set by login script)
   - `username`: `admin`
   - `password`: `admin123`

### Use Environment Variables in URLs

Instead of hardcoding URLs, use:
- `{{base_url}}/api/auth/login`
- `{{base_url}}/api/jasdatadaily`

## Automatic Token Refresh Script

Add this to your Login request's **Tests** tab to automatically save token:

```javascript
// Save token to environment
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access_token);
    pm.environment.set("token_type", jsonData.token_type);
    
    console.log("✅ Login successful");
    console.log("Token saved to environment");
} else {
    console.log("❌ Login failed");
    pm.environment.unset("access_token");
}
```

## Testing Token Expiration

Tokens expire after 30 minutes. If you get a 401 error:

1. **Run the Login request again** to get a new token
2. The token will be automatically updated in your environment

## Troubleshooting

### Error: "Could not validate credentials"
- **Solution:** Token expired or invalid. Login again to get a new token.

### Error: "Incorrect username or password"
- **Solution:** Check username/password. Default: `admin`/`admin123`

### Token not being sent
- **Solution:** 
  1. Check Authorization tab is set to "Bearer Token"
  2. Verify environment variable `{{access_token}}` is set
  3. Make sure you're using the correct environment

### 401 Unauthorized
- **Solution:** 
  1. Verify token is in Authorization header
  2. Check token hasn't expired (login again)
  3. Ensure endpoint requires authentication

## Quick Test Flow

1. **Login** → Get token
2. **Save token** to environment (via script)
3. **Test protected endpoint** → Should work with `{{access_token}}`
4. **Test without token** → Should get 401 error
5. **Test public endpoint** → Should work without token

## Postman Collection JSON (Import Ready)

You can import this collection to get started quickly:

```json
{
    "info": {
        "name": "FastAPI Authentication",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "auth": {
        "type": "bearer",
        "bearer": [
            {
                "key": "token",
                "value": "{{access_token}}",
                "type": "string"
            }
        ]
    },
    "item": [
        {
            "name": "Login",
            "request": {
                "method": "POST",
                "header": [],
                "body": {
                    "mode": "urlencoded",
                    "urlencoded": [
                        {"key": "username", "value": "admin"},
                        {"key": "password", "value": "admin123"}
                    ]
                },
                "url": {
                    "raw": "{{base_url}}/api/auth/login",
                    "host": ["{{base_url}}"],
                    "path": ["api", "auth", "login"]
                }
            },
            "event": [
                {
                    "listen": "test",
                    "script": {
                        "exec": [
                            "if (pm.response.code === 200) {",
                            "    var jsonData = pm.response.json();",
                            "    pm.environment.set('access_token', jsonData.access_token);",
                            "}"
                        ]
                    }
                }
            ]
        },
        {
            "name": "Get JasDataDaily",
            "request": {
                "method": "GET",
                "header": [],
                "url": {
                    "raw": "{{base_url}}/api/jasdatadaily?date_from=2025-01-01&date_to=2025-01-31",
                    "host": ["{{base_url}}"],
                    "path": ["api", "jasdatadaily"],
                    "query": [
                        {"key": "date_from", "value": "2025-01-01"},
                        {"key": "date_to", "value": "2025-01-31"}
                    ]
                }
            }
        }
    ]
}
```

Save this as a `.json` file and import it into Postman!
