# 🏠 Local Deployment Guide - MC AI with Llama Features

## Overview
This guide shows you how to run MC AI on your local machine with **all Llama ecosystem features** enabled, including Vision and Embeddings. This gives you free, local AI capabilities without API costs.

---

## 🎯 Why Deploy Locally?

### Benefits
- ✅ **FREE:** No API costs for text, vision, or embeddings
- ✅ **PRIVACY:** Everything runs on your machine
- ✅ **OFFLINE:** Works without internet connection
- ✅ **FULL FEATURES:** Vision, embeddings, and all Llama models

### When to Deploy Locally
- You have a powerful computer (8GB+ RAM recommended)
- You want to avoid API costs
- You need offline capabilities
- Privacy is a priority

---

## 📋 Prerequisites

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8GB | 16GB+ |
| Storage | 20GB free | 50GB+ free |
| CPU | 4 cores | 8+ cores |
| GPU | Not required | NVIDIA GPU (optional, for speed) |

### Software Requirements
- **OS:** macOS, Linux, or Windows (WSL2)
- **Python:** 3.8+
- **Git:** For cloning repository
- **Ollama:** For Llama models

---

## 🚀 Installation Steps

### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/mc-ai.git
cd mc-ai
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Main Dependencies:**
- Flask 3.0.0
- NumPy, SciPy
- Pillow (image processing)
- OpenAI (optional, for fallbacks)

### Step 3: Install Ollama

#### macOS & Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Windows (WSL2)
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

Or download from: https://ollama.ai/download

### Step 4: Start Ollama Service

```bash
# Start Ollama server
ollama serve
```

**Note:** Leave this running in a terminal. It will use port 11434.

### Step 5: Install Llama Models

Open a **new terminal** and run:

```bash
# Essential model (fast, 3GB)
ollama pull llama3.2:3b

# Better quality (balanced, 4.7GB)
ollama pull llama3.2:7b

# Vision model (image analysis, 7GB)
ollama pull llama3.2-vision:11b

# Best quality (optional, 40GB)
ollama pull llama3.3:70b

# Best vision (optional, 55GB)
ollama pull llama3.2-vision:90b
```

**Recommended for most users:**
- llama3.2:7b (general text)
- llama3.2-vision:11b (image analysis)

### Step 6: Install Llama Ecosystem Features

```bash
# Create new files from reference docs
cp docs/llama_vision_reference.md src/llama_vision.py
cp docs/llama_embeddings_reference.md src/llama_embeddings.py
```

**Note:** Extract the Python code from the markdown files.

### Step 7: Configure Environment

Create `.env` file:

```bash
# Optional: OpenAI API key (fallback only)
# OPENAI_API_KEY=your_key_here

# Llama settings
LLAMA_MODEL=llama3.2:7b
OLLAMA_BASE_URL=http://localhost:11434

# Other settings
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

### Step 8: Start MC AI

```bash
python app.py
```

Visit: http://localhost:5000

---

## 🔧 Configuration

### Model Selection

Edit `.env` or set environment variables:

```bash
# For speed (3B model)
export LLAMA_MODEL=llama3.2:3b

# For quality (7B model)
export LLAMA_MODEL=llama3.2:7b

# For best quality (70B model - requires powerful hardware)
export LLAMA_MODEL=llama3.3:70b
```

### Enable All Features

Update `app.py` to include Llama ecosystem:

```python
from src.llama_vision import LlamaVision
from src.llama_embeddings import LlamaEmbeddings

# Initialize
llama_vision = LlamaVision()
llama_embeddings = LlamaEmbeddings()

# Add endpoints (see reference docs)
```

---

## 🎨 Available Features

### 1. Llama Vision (Image Understanding)

**Endpoint:** `POST /api/vision/analyze`

```bash
curl -X POST http://localhost:5000/api/vision/analyze \
  -F "image=@photo.jpg" \
  -F "prompt=What emotions do you see?"
```

**Capabilities:**
- Image description
- Emotion detection from faces
- Art style analysis
- Object recognition

### 2. Llama Embeddings (Semantic Search)

**Usage:**
```python
from src.llama_embeddings import LlamaEmbeddings

embeddings = LlamaEmbeddings()

# Check similarity
similarity = embeddings.similarity(
    "I'm feeling anxious",
    "I'm feeling nervous"
)
print(f"Similarity: {similarity:.3f}")  # ~0.85
```

**Capabilities:**
- Semantic text similarity
- Enhanced dataset search
- Document clustering
- Better than keyword matching

### 3. All Existing Features
- ✅ Emotional intelligence (frequency-based)
- ✅ Recipe generation (31 domain knowledge base)
- ✅ AI art (standalone + API)
- ✅ AI music (standalone + API)
- ✅ 11 HTML5 games
- ✅ Data analysis & visualization
- ✅ Conversation memory

---

## 🧪 Testing

### Test Ollama Connection
```bash
curl http://localhost:11434/api/tags
```

Should return list of installed models.

### Test Vision
```bash
python -c "
from src.llama_vision import LlamaVision
v = LlamaVision()
print(f'Vision available: {v.available}')
print(f'Model: {v.model}')
"
```

### Test Embeddings
```bash
python -c "
from src.llama_embeddings import LlamaEmbeddings
e = LlamaEmbeddings()
emb = e.get_embedding('test')
print(f'Embedding size: {len(emb) if emb else 0}')
"
```

### Test Complete System
```bash
# Run all tests
python tests/run_all_tests.py
```

---

## 📊 Performance Guide

### Model Speed Comparison

| Model | Size | Speed | Quality | RAM | Use Case |
|-------|------|-------|---------|-----|----------|
| llama3.2:1b | 1GB | Very Fast | Basic | 4GB | Testing |
| llama3.2:3b | 3GB | Fast | Good | 6GB | Production |
| llama3.2:7b | 4.7GB | Medium | Great | 10GB | Recommended |
| llama3.3:70b | 40GB | Slow | Best | 48GB | High-end |

### GPU Acceleration (Optional)

If you have NVIDIA GPU:

```bash
# Ollama automatically uses GPU if available
# Verify with:
ollama run llama3.2:7b "test"
```

Speeds up inference 5-10x.

---

## 🔄 Switching Between Local and API

### Use Local Llama (Free)
```python
# .env file
USE_LOCAL_LLAMA=true
OLLAMA_BASE_URL=http://localhost:11434
```

### Use OpenAI API (Fallback)
```python
# .env file
USE_LOCAL_LLAMA=false
OPENAI_API_KEY=your_key_here
```

### Hybrid Approach (Best of Both)
```python
# System automatically uses:
# 1. Local Llama (if available)
# 2. OpenAI API (if Llama fails)
# 3. Internal fallbacks
```

---

## 💰 Cost Comparison

### Local Deployment (Your Machine)

| Feature | Cost |
|---------|------|
| Text Generation | **FREE** ✅ |
| Image Analysis | **FREE** ✅ |
| Embeddings | **FREE** ✅ |
| **Total Monthly** | **$0** ✅ |

**One-time costs:**
- Electricity: ~$5-10/month (running 24/7)
- Hardware: Already owned

### Replit Production (Cloud)

| Feature | Cost |
|---------|------|
| OpenAI API | Replit credits |
| Database | Included |
| Hosting | Included |

**Benefits of Replit:**
- Always online
- No hardware needed
- Automatic scaling
- Easy deployment

---

## 🛠 Troubleshooting

### Ollama Not Starting
```bash
# Check if port 11434 is available
lsof -i :11434

# Kill existing process if needed
killall ollama

# Restart Ollama
ollama serve
```

### Model Not Found
```bash
# List installed models
ollama list

# Pull missing model
ollama pull llama3.2:7b
```

### Out of Memory
```bash
# Use smaller model
export LLAMA_MODEL=llama3.2:3b

# Or increase system swap (Linux/macOS)
```

### Vision Not Working
```bash
# Verify vision model installed
ollama list | grep vision

# Pull if missing
ollama pull llama3.2-vision:11b
```

---

## 📁 Project Structure

```
mc-ai/
├── app.py                      # Main Flask app
├── src/
│   ├── llama_client.py         # Basic Llama integration ✅
│   ├── llama_vision.py         # Vision features (add locally)
│   ├── llama_embeddings.py     # Embeddings (add locally)
│   ├── response_generator.py   # Main orchestrator
│   └── ...
├── docs/
│   ├── llama_vision_reference.md      # Vision guide
│   ├── llama_embeddings_reference.md  # Embeddings guide
│   └── LOCAL_DEPLOYMENT_WITH_LLAMA.md # This file
└── tests/
    └── run_all_tests.py
```

---

## 🎯 Quick Start Commands

```bash
# Complete setup in 5 commands:
git clone https://github.com/YOUR_USERNAME/mc-ai.git
cd mc-ai
pip install -r requirements.txt
ollama serve &  # Run in background
ollama pull llama3.2:7b && python app.py
```

Visit http://localhost:5000 🚀

---

## 🌟 Recommended Setup

For most users, we recommend:

```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Start Ollama
ollama serve &

# 3. Install recommended models
ollama pull llama3.2:7b          # General use
ollama pull llama3.2-vision:11b  # Image analysis

# 4. Start MC AI
python app.py
```

**System will use:**
- Local Llama for text (free)
- Local Vision for images (free)
- OpenAI fallback (if Llama unavailable)

---

## 📚 Additional Resources

- **Ollama Documentation:** https://github.com/ollama/ollama
- **Model Library:** https://ollama.ai/library
- **MC AI Docs:** See `/docs` folder
- **Llama Vision Reference:** `docs/llama_vision_reference.md`
- **Llama Embeddings Reference:** `docs/llama_embeddings_reference.md`

---

## ✅ Verification Checklist

Before using, verify:

- [ ] Ollama service running (`curl http://localhost:11434/api/tags`)
- [ ] Models installed (`ollama list`)
- [ ] Python dependencies installed (`pip list`)
- [ ] MC AI starts without errors (`python app.py`)
- [ ] Can access UI (http://localhost:5000)
- [ ] Features working (try asking a question)

---

## 🎊 Success!

You now have MC AI running locally with:
- ✅ Free local AI (Llama)
- ✅ Image understanding (Vision)
- ✅ Semantic search (Embeddings)
- ✅ All original features
- ✅ No API costs

**Enjoy your local AI system!** 🚀

---

*For Replit production deployment (cloud), see READY_TO_PUBLISH.md*
