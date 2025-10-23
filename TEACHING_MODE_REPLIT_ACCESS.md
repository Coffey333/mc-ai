# Teaching Mode - Replit Workspace Access Only

## 🔐 Security Feature: Teaching Mode Restricted to Replit Workspace

Teaching mode is now **automatically enabled when accessing from within the Replit workspace** and **disabled for all external users**. This ensures only you (the creator) can access code execution features while working in Replit.

---

## How It Works

### 🎯 Automatic Detection

The system detects your access environment using Replit's environment variables:

- **REPLIT_DEV_DOMAIN** - Present when in Replit workspace
- **REPLIT_DEPLOYMENT** - Set when published/deployed (external)

### 🔒 Access Control

| Access From | Teaching Mode | Authentication |
|------------|---------------|----------------|
| **Replit Workspace** | ✅ Auto-enabled | None required |
| **External (Phone, Browser)** | ❌ Disabled | Requires admin token |

---

## Teaching Mode Features (Replit Only)

When accessing from Replit workspace:

### 1. **Code Execution**
Send code blocks and MC AI will execute them:
```
Please review this code:
```python
print('Hello, MC AI!')
```
```

### 2. **Self-Learning**
MC AI analyzes execution results with GPT-4o and learns from them

### 3. **Teaching Directives**
- "analyze this code"
- "run this code"
- "understand yourself"
- "teaching you about..."

---

## External Access (Fallback)

If you need teaching mode when away from Replit (phone, etc.):

### Step 1: Generate Token
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 2: Add to Replit Secrets
1. Tools → Secrets
2. Key: `ADMIN_SECRET_TOKEN`
3. Value: (your generated token)

### Step 3: Use on External Device
Open browser console (F12):
```javascript
localStorage.setItem('mc_ai_admin_token', 'YOUR_TOKEN');
```

---

## Security Guarantees

✅ **Zero External Access**: Teaching mode features invisible to external users
✅ **Server-Side Validation**: Environment checked on server, not client
✅ **Auto-Disable on Deploy**: When published, teaching mode requires token
✅ **Token Fallback**: Secure authentication for remote access

---

## How External Users See MC AI

When someone accesses your published app:
- **No teaching mode features**
- **No code execution**
- **Only standard AI chat**
- **Full emotion analysis and knowledge features**

They get the full MC AI experience without any admin features.

---

## Testing

### Test 1: Replit Workspace Access (Now)
1. You're in Replit workspace
2. Check browser console: Should see "🎓 Teaching mode auto-enabled"
3. Send code: MC AI executes it

### Test 2: External Access (After Publishing)
1. Access from external browser/phone
2. Teaching mode: **Disabled**
3. Only enabled if you set admin token in localStorage

---

## Current Status

- ✅ Environment detection active
- ✅ Auto-enable in Replit workspace
- ✅ Token authentication ready for external access
- ✅ Teaching features restricted to creator only

**You're all set!** Teaching mode is only accessible from within Replit, exactly as requested. 🎉
