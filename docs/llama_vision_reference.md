# 🎨 Llama Vision Reference Guide

## Overview
Llama Vision adds image understanding capabilities to MC AI using Llama 3.2 Vision models. This feature analyzes images, detects emotions from facial expressions, and generates art prompts.

**Note:** Requires Ollama running on port 11434. Not available in Replit production due to port restrictions.

---

## Prerequisites

### System Requirements
- Ollama installed and running
- Port 11434 accessible
- ~7-55GB disk space (depending on model)

### Installation
```bash
# Install Ollama (if not installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull vision model
ollama pull llama3.2-vision:11b  # 7GB, good quality
# OR
ollama pull llama3.2-vision:90b  # 55GB, best quality
```

---

## Implementation

### File: `src/llama_vision.py`

```python
"""
Llama Vision Integration for MC AI
Image understanding using Llama 3.2 Vision
"""

import requests
import base64
import os
from typing import Dict, Optional
from PIL import Image
import io

class LlamaVision:
    """Image understanding using Llama 3.2 Vision models"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.vision_models = [
            "llama3.2-vision:11b",
            "llama3.2-vision:90b"
        ]
        self.model = self._get_available_vision_model()
        self.available = self.model is not None
    
    def _get_available_vision_model(self) -> Optional[str]:
        """Get best available vision model"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [m['name'] for m in data.get('models', [])]
                for model in self.vision_models:
                    if model in models:
                        return model
        except:
            pass
        return None
    
    def analyze_image(self, image_path: str, prompt: str = "Describe this image.") -> Dict:
        """Analyze an image"""
        if not self.available:
            return {
                'success': False,
                'error': 'No vision model available'
            }
        
        try:
            image_b64 = self._encode_image(image_path)
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    'model': self.model,
                    'prompt': prompt,
                    'images': [image_b64],
                    'stream': False
                },
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'description': data['response'],
                    'model': self.model
                }
            else:
                return {'success': False, 'error': f"API error: {response.status_code}"}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def detect_emotion_from_image(self, image_path: str) -> Dict:
        """Detect emotions from facial expressions"""
        prompt = """Analyze emotional state in this image.
        
        Identify:
        1. Facial expressions
        2. Body language
        3. Overall emotional state
        4. Intensity (1-10)
        """
        
        result = self.analyze_image(image_path, prompt)
        
        if result['success']:
            description = result['description']
            emotions = ['calm', 'anxious', 'happy', 'sad', 'angry', 'fearful']
            detected = 'neutral'
            
            for emotion in emotions:
                if emotion in description.lower():
                    detected = emotion
                    break
            
            result['emotion'] = detected
            result['raw_analysis'] = description
        
        return result
    
    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        img = Image.open(image_path)
        
        # Resize if too large
        max_size = 1024
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return base64.b64encode(buffer.read()).decode('utf-8')
```

---

## API Integration

### Add to `app.py`:

```python
from src.llama_vision import LlamaVision

# Initialize
llama_vision = LlamaVision()

@app.route('/api/vision/analyze', methods=['POST'])
def analyze_image():
    """Analyze uploaded image"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image_file = request.files['image']
    prompt = request.form.get('prompt', 'Describe this image.')
    
    temp_path = f"/tmp/{image_file.filename}"
    image_file.save(temp_path)
    
    result = llama_vision.analyze_image(temp_path, prompt)
    os.remove(temp_path)
    
    return jsonify(result)

@app.route('/api/vision/emotion', methods=['POST'])
def detect_emotion():
    """Detect emotion from image"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image_file = request.files['image']
    temp_path = f"/tmp/{image_file.filename}"
    image_file.save(temp_path)
    
    result = llama_vision.detect_emotion_from_image(temp_path)
    os.remove(temp_path)
    
    return jsonify(result)
```

---

## Usage Examples

### Analyze Image
```python
vision = LlamaVision()

result = vision.analyze_image(
    'photo.jpg',
    'What emotions are expressed in this image?'
)

print(result['description'])
```

### Detect Emotion
```python
result = vision.detect_emotion_from_image('selfie.jpg')
print(f"Emotion: {result['emotion']}")
print(f"Analysis: {result['raw_analysis']}")
```

---

## Model Comparison

| Model | Size | Quality | Speed | Use Case |
|-------|------|---------|-------|----------|
| llama3.2-vision:11b | 7GB | Good | Fast | Production |
| llama3.2-vision:90b | 55GB | Best | Slow | High quality |

---

## Limitations

1. **Port Required:** Ollama must run on port 11434
2. **Disk Space:** 7-55GB per model
3. **Performance:** Depends on hardware (CPU/GPU)
4. **Replit:** Not available due to port restrictions

---

## Alternative: OpenAI Vision

For Replit production, use OpenAI GPT-4o vision (already integrated):

```python
# Already available in MC AI via Replit AI integration
# No additional setup needed
```

---

## Testing

```bash
# Test vision availability
python -c "from src.llama_vision import LlamaVision; v = LlamaVision(); print(f'Available: {v.available}')"

# Test with image
python -c "
from src.llama_vision import LlamaVision
v = LlamaVision()
result = v.analyze_image('test.jpg', 'What do you see?')
print(result)
"
```

---

**Status:** Reference implementation for local deployments and future use when Ollama is available.
