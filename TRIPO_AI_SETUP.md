# Tripo AI 3D Model Generator - Setup Guide

## Overview
MC AI now includes an **AI-powered Image-to-3D Model Generator** using Tripo AI's advanced API. Upload your 2D robot drawing and get back a 3D model file!

## Features
- 📸 Upload any 2D drawing (PNG, JPG, JPEG)
- 🤖 AI generates a 3D model in 2-5 minutes
- 🎨 View and interact with the generated 3D model in real-time
- 💾 Download the model as .GLB file for use in Blender, Unity, etc.

## Setup Instructions

### Step 1: Get Tripo AI API Key

1. Visit [Tripo AI Platform](https://platform.tripo3d.ai/)
2. Sign up for a free account
3. Navigate to **API Keys** section in your dashboard
4. Click "Create New Key"
5. Copy your API key (starts with `tsk_...`)

### Step 2: Add API Key to Replit Secrets

1. In your Replit workspace, click the **🔒 Secrets** tab (lock icon in left sidebar)
2. Click "+ New Secret"
3. Enter:
   - **Key**: `TRIPO_API_KEY`
   - **Value**: Paste your Tripo AI key (e.g., `tsk_...`)
4. Click "Add Secret"

### Step 3: Start the Tripo Server

The Tripo server runs automatically in the background when MC AI starts. To manually start it, run:

```bash
node tripo-server.js &
```

You should see:
```
🎨 Tripo AI Server listening on port 3001
API Key configured: YES ✅
```

**Note**: The Flask app proxies requests from `/api/generate-model` to the Tripo server on port 3001.

### Step 4: Access the Generator

1. Open MC AI's main page
2. Click the 🤖 Live icon (or go to `/autonomous`)
3. Then navigate to `/generate-3d`
4. Or directly visit: `https://your-replit-url.dev/generate-3d`

## How to Use

1. **Upload Image**
   - Click the "Choose File" button
   - Select your robot drawing (PNG/JPG)
   - Click upload

2. **Wait for Generation** (2-5 minutes)
   - The AI will process your image
   - You'll see progress updates
   - The 3D model will appear when ready

3. **Interact with Model**
   - Rotate: Click and drag
   - Zoom: Scroll wheel
   - Pan: Right-click and drag

## How It Works

### Backend (tripo-server.js)
1. **Receives** your uploaded image
2. **Uploads** it to Tripo AI's servers
3. **Creates** a 3D generation task
4. **Polls** Tripo AI every 5 seconds for results
5. **Returns** the final model URL

### Frontend (ImageTo3D.jsx)
1. **Sends** image to our backend server
2. **Displays** loading progress
3. **Loads** the generated .GLB file
4. **Renders** the 3D model using Three.js

## Tech Stack

- **Backend**: Node.js + Express
- **AI Service**: Tripo AI API
- **Frontend**: React + React Three Fiber
- **3D Rendering**: Three.js
- **File Format**: GLB (GLTF Binary)

## Pricing

Tripo AI offers:
- **Free Tier**: ~10-20 generations per month
- **Pro Tier**: More generations + faster processing
- Check [Tripo Pricing](https://tripo3d.ai/pricing) for latest info

## Troubleshooting

### "API Key configured: NO ❌"
- Make sure you added `TRIPO_API_KEY` to Replit Secrets (exact spelling)
- Restart the tripo-server.js

### "Failed to generate model"
- Check if you have API credits remaining
- Ensure image is a clear drawing (not too complex)
- Try a smaller image file (<5MB)

### "Timeout after 5 minutes"
- This is normal for very complex images
- Try again with a simpler drawing
- The AI works best with clear, single-subject drawings

## Next Steps

### Using the Generated Model
1. The model URL is temporary - download it within 24 hours
2. Use the .GLB file in:
   - **Blender**: Import → glTF (.glb)
   - **Unity**: Drag and drop into Assets
   - **Three.js**: Load with `useGLTF(url)`
   - **Any 3D software** that supports GLTF

### Improving Quality
- AI-generated models are "base meshes" - not game-ready
- For PS4/Xbox quality:
  1. Generate base model with Tripo AI
  2. Import into Blender
  3. Clean up geometry (remove lumps, add details)
  4. Add proper rigging for animation
  5. Create PBR textures (Normal maps, Metallic, Roughness)

## Files Added

- `tripo-server.js` - Backend API server
- `frontend/src/components/ImageTo3D.jsx` - Upload UI
- `TRIPO_AI_SETUP.md` - This documentation
- `CLAUDE_3D_CHARACTER_REQUEST.md` - Character design specs

## Security

✅ **Your API key is safe**:
- Stored in Replit Secrets (encrypted)
- Never exposed to the frontend
- Backend handles all API calls

## Support

For issues with:
- **Tripo AI**: Contact [Tripo Support](https://platform.tripo3d.ai/)
- **MC AI Integration**: Check Replit console logs
- **3D Rendering**: Test in different browsers

---

**Ready to generate your first 3D model!** 🎨✨
