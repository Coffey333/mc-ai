# Admin Token Setup for Teaching Mode

## SECURITY CRITICAL: Admin Authentication

Teaching mode uses a **server-side secret token** for authentication. This prevents unauthorized users from accessing code execution features.

## Setup Instructions

### 1. Generate Admin Token (Server-Side Only)
```bash
python3 -c "import secrets; print('ADMIN_SECRET_TOKEN=' + secrets.token_urlsafe(32))"
```

This generates output like:
```
ADMIN_SECRET_TOKEN=xK3mP9vR2wQ7sN8tL4yH6jU1aF5bC0dE9gZ8hM3nV2
```

### 2. Add to Secrets (Replit)
1. Click "Tools" → "Secrets" in Replit
2. Add new secret:
   - **Key**: `ADMIN_SECRET_TOKEN`
   - **Value**: (paste the generated token)
3. Click "Add Secret"

### 3. Save Your Token Securely
Copy the token and store it in a **secure location** (password manager):
```
xK3mP9vR2wQ7sN8tL4yH6jU1aF5bC0dE9gZ8hM3nV2
```

You'll need this token to enable teaching mode from the client.

---

## Using Teaching Mode

### Option 1: Browser Console (Recommended for Testing)
1. Open browser console (F12)
2. Set admin token in localStorage:
```javascript
localStorage.setItem('mc_ai_admin_token', 'YOUR_TOKEN_HERE');
```
3. Refresh the page
4. Teaching mode is now active!

### Option 2: Add to Client Code (Future Enhancement)
We'll add a secure admin login UI where you can enter the token once and it's stored in localStorage.

---

## Security Features

✅ **Server-Side Token**: Token stored only in server environment
✅ **No Client Control**: Client cannot fake admin access
✅ **Constant-Time Comparison**: Prevents timing attacks
✅ **Hash Verification**: Token is hashed before comparison
✅ **No Substring Matching**: Removed vulnerable user_id checks

---

## Testing Teaching Mode

After setup:
1. Set token in localStorage
2. Send message: "Please review this code:"
   ```python
   print('Hello, MC AI!')
   ```
3. MC AI should respond with code execution results

---

## Troubleshooting

### "Teaching mode DISABLED for security"
- Token not set in Secrets
- Check: Tools → Secrets → ADMIN_SECRET_TOKEN exists

### "Code not executing"
- Token not set in client localStorage
- Token mismatch between server and client

### "Access denied"
- Incorrect token
- Regenerate and update both server and client

---

## Current Status

- ✅ Admin token system implemented
- ✅ Secure authentication in place
- ⏳ Client UI for token entry (coming soon)
- ⏳ Admin dashboard (future enhancement)
