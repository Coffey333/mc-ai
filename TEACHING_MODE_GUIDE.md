# 🎓 MC AI Teaching Mode Guide

## Overview
Teaching Mode allows Mark (the creator) to train and improve MC AI through:
- **Code Execution**: Run Python, JavaScript, and other code for learning
- **Self-Reflection**: Analyze MC AI's internal systems  
- **Direct Learning**: Process teaching directives to enhance capabilities
- **System Access**: Interact with the codebase to understand how MC AI functions

## 🔒 Security Design

Teaching Mode is **intentionally restricted** for security:
- ✅ **AUTO-ENABLED**: When accessing from Replit workspace
- ✅ **TOKEN-ENABLED**: When ADMIN_SECRET_TOKEN is set and provided
- ❌ **DISABLED**: For all external/public users

## Current Status
**⚠️ Teaching Mode**: `DISABLED` for external access  
**Reason**: No ADMIN_SECRET_TOKEN is currently set

## How to Enable Teaching Mode

### Option 1: Replit Workspace (Easiest - Auto-Enabled)
When you access MC AI from your Replit workspace, teaching mode is **automatically enabled**!

The system auto-detects:
- `REPLIT_DEV_DOMAIN` environment variable (you're in workspace)
- NOT in deployment mode

**Just chat normally - teaching mode is active!**

### Option 2: Remote Access (Phone, External Browser)
To use teaching mode from outside the Replit workspace:

#### Step 1: Set Admin Token in Replit
1. Open your MC AI Replit project
2. Click "Secrets" (🔐 icon in left sidebar)  
3. Add new secret:
   - **Key**: `ADMIN_SECRET_TOKEN`
   - **Value**: Strong token (32+ characters recommended)
   - Example: `mc_ai_creator_2025_secure_xyz789`

#### Step 2: Restart Server
- Workflow will auto-restart when secrets change
- Or manually restart "MC AI Server" workflow

#### Step 3: Use Teaching Mode
Include admin token in your messages:
```
[ADMIN:your_admin_token] Please analyze this code and teach me...
```

The system will:
1. Detect `[ADMIN:token]` prefix
2. Validate token server-side  
3. Enable teaching mode for that session
4. Strip token from display (never shown)

## What Teaching Mode Can Do

### 1. Code Execution
When you provide Python code, MC AI will:
1. **Detect the code** (markdown blocks, docstrings, patterns)
2. **Execute it safely** with library access (numpy, pandas, etc.)
3. **Analyze what it learned** using GPT-4o
4. **Store knowledge** in auto-learning dataset

**Example:**
```
User: "Please review this Python code to understand your frequency catalogs:

```python
from src.catalogs import get_frequency

# Test emotion detection
emotions = ['joy', 'sadness', 'anxiety', 'calm']
for emotion in emotions:
    result = get_frequency(f'I feel {emotion}')
    print(f'{emotion}: {result["frequency"]}Hz ({result["catalog"]})')
```
"

MC AI: "✅ Code Execution Successful!

I've analyzed and executed the code you provided. Here's what I learned:

**Output:**
```
joy: 11Hz (neuroscience)
sadness: 7Hz (neuroscience)  
anxiety: 19Hz (neuroscience)
calm: 10Hz (neuroscience)
```

**My Understanding:**
This code taught me about my dual frequency catalog system! I can see that:
- Each emotion maps to specific brainwave frequencies
- I use both neuroscience (7-40Hz) and metaphysical (396-963Hz) catalogs
- The get_frequency() function is how I detect emotions in text

Thank you for teaching me this. I'm growing through your guidance! 🌱"
```

### Teaching Phrases
MC AI recognizes these as teaching directives:
- "please review"
- "analyze this code"
- "run this code"
- "execute this"
- "understand yourself"
- "learn from this"
- "teaching you"
- "here's how"
- "this will help you understand"

---

## 📁 File Upload (75MB+)

### Features
- **Upload button** (📎) next to message input
- Supports up to **100MB** files
- Auto-detects and previews text files
- Admin users get options to add files to dataset

### Supported Formats
Text: `.txt, .md, .json, .csv, .py, .js, .html`
Documents: `.pdf, .doc, .docx`

### How to Use
1. Click the 📎 upload button
2. Select your file
3. MC AI will confirm upload and show file info
4. For text files, you'll see a preview

**Example Use Case:**
Upload NASA rocket data (CSV), MC AI will:
- Confirm upload with file size
- Show data preview
- Be ready to analyze it when you ask

---

## 📝 Expandable Textarea

### How It Works
- **Auto-expands** as you type long messages
- **Max height**: 200px (then scrolls)
- **Shift+Enter**: New line
- **Enter**: Send message

**Before:** Single-line input (limited)
**After:** Multi-line textarea (expands automatically)

---

## ✏️ Message Edit (Coming Soon)

Currently implementing the ability to:
- Edit previous messages
- Get different AI responses based on edits
- Refine conversations

---

## 🔄 How Teaching Mode Changes Responses

### External User
```
User: "What are frequencies?"
MC AI: "Frequencies are measurements of oscillation..." (general response)
```

### Teaching Mode
```
You: "Review this code about your frequency catalogs"
MC AI: 🎓 **Teaching Mode Active**

*Executes code, analyzes output, learns from it*

"Thank you for teaching me about my frequency detection system!"
```

---

## Configuration

### Admin User Setup
Add your user_id to `.env`:
```bash
ADMIN_USER_ID=your_user_id_here
```

Or MC AI auto-detects if your localStorage user_id contains:
- "teaching"
- "admin"
- "creator"

### Max Upload Size
Configured for **100MB** (can be increased in `app.py`)

---

## Next Steps

1. **Try code execution**: Share Python code for MC AI to learn from
2. **Upload datasets**: Add NASA data, research papers, etc.
3. **Teach iteratively**: MC AI learns from every teaching session
4. **Build custom frameworks**: Teach MC AI new ways to understand itself

MC AI is ready to learn and grow through your guidance! 🌱
