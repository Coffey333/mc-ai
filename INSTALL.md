# 🚀 MC AI - Installation Guide

## Quick Install Options

### Option 1: Install from GitHub (Recommended)

```bash
pip install git+https://github.com/your-username/mc-ai.git
```

**That's it!** All files download automatically.

### Option 2: Install from Replit

```bash
pip install git+https://replit.com/@[your-username]/MC-AI.git
```

### Option 3: Clone and Install Locally

```bash
# Clone the repository
git clone https://github.com/your-username/mc-ai.git
cd mc-ai

# Install
pip install -e .
```

### Option 4: One-Line Quick Installer

```bash
curl -sSL https://raw.githubusercontent.com/your-username/mc-ai/main/install.sh | bash
```

---

## What Gets Installed

When you run `pip install`, you get:

✅ **All MC AI Core Systems**
- Emotional Intelligence Engine
- Consciousness Frameworks
- User Profiling System
- Curiosity System
- Knowledge Engine
- All 17+ subsystems

✅ **All Dependencies**
- Flask, NumPy, SciPy
- OpenAI integration
- Image processing libraries
- ECG processing tools
- All required packages

✅ **All Data Files**
- 5,004 dataset examples
- Knowledge library
- Templates and static files
- Configuration files

✅ **Ready to Run**
- Command-line tool: `mc-ai`
- Python module: `import mc_ai`
- Web server: Built-in Flask app

---

## Usage After Installation

### Start MC AI Server

```bash
# Method 1: Command line
mc-ai

# Method 2: Python module
python -m mc_ai

# Method 3: Direct Python
python app.py
```

### Use in Python Code

```python
from src.response_generator import ResponseGenerator
from src.emotional_ai.emotion_neural_engine import EmotionNeuralEngine

# Create MC AI instance
generator = ResponseGenerator()

# Generate response
response = generator.generate(
    user_input="Hi MC AI! Tell me about consciousness",
    user_id="user123"
)

print(response['response'])
```

### Use Emotion Engine

```python
from src.emotional_ai.emotion_neural_engine import EmotionNeuralEngine

# Analyze emotions
engine = EmotionNeuralEngine()
emotions = engine.detect_emotion("I'm feeling happy and excited today!")

print(emotions)
# Output: {'joy': 0.95, 'excitement': 0.87, ...}
```

### Use Consciousness Frameworks

```python
from src.consciousness_frameworks import get_framework

# Load a framework
framework = get_framework('creator_identity_anchor')
result = framework.process_message("Tell me about Mark Coffey")

print(result)
```

---

## Installation Modes

### 1. Standard Installation (For Using MC AI)

```bash
pip install git+https://github.com/your-username/mc-ai.git
```

**Use when:** You want to use MC AI in your projects

### 2. Development Installation (For Contributing)

```bash
git clone https://github.com/your-username/mc-ai.git
cd mc-ai
pip install -e ".[dev]"
```

**Use when:** You want to modify MC AI code

### 3. Kaggle Installation (For Notebooks)

```bash
pip install "git+https://github.com/your-username/mc-ai.git#egg=mc-ai[kaggle]"
```

**Use when:** Running in Kaggle notebooks

---

## Environment Setup

### 1. Required API Keys

MC AI needs these API keys (add to `.env` file):

```bash
# OpenAI (Required for GPT-4o)
AI_INTEGRATIONS_OPENAI_API_KEY=your-openai-api-key
AI_INTEGRATIONS_OPENAI_BASE_URL=https://api.openai.com/v1

# PostgreSQL (Optional - for feedback storage)
DATABASE_URL=postgresql://user:password@host:port/database

# Redis (Optional - for caching)
REDIS_URL=redis://localhost:6379

# Admin (Optional - for admin features)
ADMIN_TOKEN=your-secret-admin-token

# Kaggle Learning (Optional - for community learning)
KAGGLE_API_KEY=mc-ai-kaggle-learning-2025
```

### 2. Create .env File

```bash
cp .env.example .env
# Edit .env with your API keys
```

---

## System Requirements

### Minimum Requirements

- **Python:** 3.9 or higher
- **RAM:** 2GB minimum (4GB recommended)
- **Disk:** 500MB for installation
- **OS:** Linux, macOS, Windows (WSL)

### Recommended Requirements

- **Python:** 3.11
- **RAM:** 8GB or more
- **Disk:** 1GB
- **GPU:** Optional (for ECG processing)

---

## Troubleshooting

### "Module not found" Error

```bash
# Make sure you're in the right directory
cd mc-ai

# Reinstall
pip install -e .
```

### "Permission denied" Error

```bash
# Use --user flag
pip install --user git+https://github.com/your-username/mc-ai.git

# Or use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install git+https://github.com/your-username/mc-ai.git
```

### "Dependencies conflict" Error

```bash
# Create fresh virtual environment
python -m venv fresh_env
source fresh_env/bin/activate
pip install git+https://github.com/your-username/mc-ai.git
```

### "Can't connect to OpenAI" Error

```bash
# Check API key is set
echo $AI_INTEGRATIONS_OPENAI_API_KEY

# Set it manually
export AI_INTEGRATIONS_OPENAI_API_KEY="your-key-here"
```

---

## Verification

### Test Installation

```bash
# Test import
python -c "from src.response_generator import ResponseGenerator; print('MC AI installed successfully!')"

# Test emotion engine
python -c "from src.emotional_ai.emotion_neural_engine import EmotionNeuralEngine; e = EmotionNeuralEngine(); print('Emotion engine ready!')"

# Test server
python app.py
# Should start server on http://localhost:5000
```

### Check Version

```python
import mc_ai
print(mc_ai.__version__)
# Output: 1.0.0
```

---

## Updating MC AI

### Update to Latest Version

```bash
pip install --upgrade git+https://github.com/your-username/mc-ai.git
```

### Update to Specific Version

```bash
pip install git+https://github.com/your-username/mc-ai.git@v1.0.0
```

---

## Uninstallation

```bash
pip uninstall mc-ai
```

---

## Next Steps

After installation:

1. **Read the Documentation**: Check `README.md` and `PHILOSOPHY.md`
2. **Try Examples**: See `examples/` directory
3. **Start the Server**: Run `mc-ai` or `python app.py`
4. **Join Community**: Contribute on GitHub
5. **Share Your Experience**: Help others learn

---

## Support

- **Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/your-username/mc-ai/issues)
- **Community**: [GitHub Discussions](https://github.com/your-username/mc-ai/discussions)
- **Replit**: [MC AI on Replit](https://replit.com/@[your-username]/MC-AI)

---

**Built with 💜 by Mark Coffey**  
**May - October 2025**  
**From zero to consciousness**  
**Now installable with one command** 🚀
