# 🌐 Ngrok Integration Guide for MC AI

## What is Ngrok?

Ngrok creates secure tunnels to expose local services to the public internet. Your authtoken is already configured in MC AI!

---

## 🎯 How to Use Your Ngrok Token

### **Scenario 1: Expose MC AI Publicly**

Make MC AI accessible from anywhere:

```bash
# In your terminal
ngrok http 5000 --authtoken=$Ngrok
```

This gives you a public URL like: `https://abc123.ngrok.io`

Share this URL with anyone to let them use MC AI!

---

### **Scenario 2: Connect Kaggle/Colab AI Services to MC AI**

#### **Step 1: In Your Kaggle/Colab Notebook**

Add this to the top of your notebook:

```python
# Install ngrok
!pip install pyngrok flask

# Import and setup
from pyngrok import ngrok
import os

# Your ngrok token (same one you added to MC AI)
ngrok.set_auth_token("33joexrK5OUiIo5QG5G5jDLG2h3_53sXKPddn14QWuTtU61eh")

# After creating your Flask API...
from flask import Flask
app = Flask(__name__)

@app.route('/generate-art', methods=['POST'])
def generate_art():
    # Your art generation code here
    pass

# Expose it publicly
public_url = ngrok.connect(5000)
print(f"🎨 Art Service URL: {public_url}")

# Run Flask
app.run(port=5000)
```

#### **Step 2: Copy the Public URL**

Your Kaggle/Colab will print something like:
```
🎨 Art Service URL: https://xyz789.ngrok.io
```

#### **Step 3: Add to MC AI**

In your Replit terminal:

```bash
# Add your Kaggle/Colab service URLs as secrets
export CUSTOM_ART_SERVICE_URL="https://xyz789.ngrok.io/generate-art"
export CUSTOM_MUSIC_SERVICE_URL="https://abc123.ngrok.io/generate-music"
export CUSTOM_VIDEO_SERVICE_URL="https://def456.ngrok.io/generate-video"
```

Or add them through Replit's Secrets panel:
- `CUSTOM_ART_SERVICE_URL`
- `CUSTOM_MUSIC_SERVICE_URL`
- `CUSTOM_VIDEO_SERVICE_URL`

---

## 🔧 Integration with MC AI

### **Option A: Quick Test (Manual)**

1. Run your Kaggle/Colab notebook
2. Get the ngrok URL
3. Test it directly:

```bash
curl -X POST https://your-ngrok-url.ngrok.io/generate-art \
  -H "Content-Type: application/json" \
  -d '{"prompt":"sunset", "style":"digital", "emotion":"joy"}'
```

### **Option B: Permanent Integration**

Modify MC AI to use your services:

1. Add service URLs to Replit Secrets
2. MC AI's `config/external_services.py` will automatically detect them
3. Art/Music/Video generators will use your services first, then fall back to external APIs

---

## 📋 Service Requirements

For each Kaggle/Colab service you build, make sure it:

### **Art Service** (`/generate-art`)
**Accepts:**
```json
{
  "prompt": "beautiful sunset",
  "style": "digital",
  "emotion": "joy"
}
```

**Returns:**
```json
{
  "success": true,
  "image_url": "data:image/png;base64,...",
  "provider": "KaggleArtService"
}
```

### **Music Service** (`/generate-music`)
**Accepts:**
```json
{
  "emotion": "calm",
  "style": "ambient",
  "duration": 30
}
```

**Returns:**
```json
{
  "success": true,
  "audio_url": "data:audio/wav;base64,...",
  "provider": "ColabMusicService"
}
```

### **Video Service** (`/generate-video`)
**Accepts:**
```json
{
  "prompt": "flowing water",
  "duration": 4
}
```

**Returns:**
```json
{
  "success": true,
  "video_url": "data:video/mp4;base64,...",
  "provider": "KaggleVideoService"
}
```

---

## ⚡ Quick Start Checklist

- [x] Ngrok token added to MC AI secrets ✅
- [ ] Build Kaggle/Colab notebook for art/music/video
- [ ] Add ngrok to your notebook
- [ ] Create Flask API endpoint
- [ ] Get public ngrok URL
- [ ] Add URL to MC AI secrets
- [ ] Test integration
- [ ] Enjoy self-hosted AI features!

---

## 🔒 Security Notes

- **Ngrok tokens are sensitive** - Keep them in environment variables only
- **Free ngrok tunnels change URLs** when you restart - You'll need to update MC AI each time
- **Paid ngrok** allows custom domains that don't change
- **Kaggle/Colab sessions expire** - Services will go down when the notebook stops

---

## 💡 Pro Tips

1. **Keep notebooks running**: Kaggle allows 9 hours/week, Colab allows ~12 hours/session
2. **Use both platforms**: Run music on Colab, art on Kaggle to maximize free GPU time
3. **Base64 encoding**: Return images/audio as base64 strings to avoid storage issues
4. **Error handling**: Add try/catch to handle when services are down

---

Need help building your first Kaggle/Colab service? Let me know which one to start with!
