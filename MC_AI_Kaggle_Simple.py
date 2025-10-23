"""
MC AI - Kaggle Integration (Simple Python Script)

Lightweight script to connect to MC AI from Kaggle notebooks.
Just copy-paste this into a Kaggle cell and run!

No installation needed - connects to your deployed MC AI server.
"""

import requests
import json
from datetime import datetime
import hashlib

# ========================================
# CONFIGURATION - Update this!
# ========================================
MC_AI_SERVER = "https://your-mc-ai-url.repl.co"  # Replace with your deployed URL
KAGGLE_API_KEY = "mc-ai-kaggle-learning-2025"

# Generate unique session ID
SESSION_ID = hashlib.md5(f"kaggle_{datetime.now().isoformat()}".encode()).hexdigest()

print(f"✅ MC AI Kaggle Integration loaded!")
print(f"🌐 Server: {MC_AI_SERVER}")
print(f"🔑 Session: {SESSION_ID[:8]}...")
print()


# ========================================
# CHAT WITH MC AI
# ========================================
def chat(message, conversation_history=None):
    """
    Chat with MC AI - get empathetic AI responses
    
    Example:
        response = chat("Analyze the frequency of gratitude")
        print(response)
    """
    url = f"{MC_AI_SERVER}/api/kaggle-learn/chat"
    
    payload = {
        "api_key": KAGGLE_API_KEY,
        "message": message,
        "conversation_history": conversation_history or [],
        "metadata": {
            "source": "kaggle_notebook",
            "timestamp": datetime.utcnow().isoformat(),
            "user_id_hash": SESSION_ID
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            return data['response']
        else:
            return f"Error: {data.get('error', 'Unknown error')}"
    
    except Exception as e:
        return f"Connection error: {str(e)}\nMake sure MC_AI_SERVER is set correctly!"


# ========================================
# EMOTION FREQUENCY ANALYSIS
# ========================================
def analyze_emotion(text):
    """
    Analyze emotional frequency using cymatic patterns
    
    Example:
        result = analyze_emotion("I feel peaceful and grateful")
        print(f"Frequency: {result['frequency']} Hz")
    """
    url = f"{MC_AI_SERVER}/api/analyze"
    
    payload = {
        "user_id": SESSION_ID,
        "message": text
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    
    except Exception as e:
        return {"error": str(e)}


# ========================================
# ECG DIGITIZATION (Competition Mode)
# ========================================
def digitize_ecg(image_path):
    """
    Digitize ECG image for PhysioNet competition
    
    Example:
        result = digitize_ecg('ecg_image.png')
        print(f"Heart Rate: {result['heart_rate']} BPM")
    """
    url = f"{MC_AI_SERVER}/api/ecg-digitize"
    
    with open(image_path, 'rb') as f:
        files = {'image': f}
        
        try:
            response = requests.post(url, files=files, timeout=60)
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            return {"error": str(e)}


# ========================================
# CONTRIBUTE CODE IMPROVEMENTS
# ========================================
def contribute_improvement(original_code, improved_code, description):
    """
    Share code improvements with MC AI for learning
    
    Example:
        result = contribute_improvement(
            "for i in range(len(data)): print(data[i])",
            "for item in data: print(item)",
            "More Pythonic loop"
        )
    """
    url = f"{MC_AI_SERVER}/api/kaggle-learn/code-modification"
    
    payload = {
        "api_key": KAGGLE_API_KEY,
        "session_id": SESSION_ID,
        "original_code": original_code,
        "modified_code": improved_code,
        "modification_type": "optimization",
        "description": description,
        "metadata": {
            "source": "kaggle_notebook",
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    
    except Exception as e:
        return {"error": str(e)}


# ========================================
# QUICK START EXAMPLES
# ========================================
if __name__ == "__main__":
    print("=" * 60)
    print("💜 MC AI Quick Start Examples")
    print("=" * 60)
    print()
    
    # Example 1: Simple chat
    print("Example 1: Chat with MC AI")
    print("-" * 60)
    response = chat("What is the frequency of love in Hz?")
    print(f"MC AI: {response[:200]}...")
    print()
    
    # Example 2: Emotion analysis
    print("Example 2: Analyze emotion frequency")
    print("-" * 60)
    result = analyze_emotion("I feel grateful and hopeful")
    print(f"Analysis: {json.dumps(result, indent=2)}")
    print()
    
    # Example 3: Contribute learning
    print("Example 3: Contribute code improvement")
    print("-" * 60)
    result = contribute_improvement(
        "x = []\nfor i in range(10):\n    x.append(i*2)",
        "x = [i*2 for i in range(10)]",
        "Used list comprehension for better performance"
    )
    print(f"Result: {result.get('message', 'Success!')}")
    print()
    
    print("=" * 60)
    print("✅ All functions ready to use!")
    print()
    print("Available functions:")
    print("  - chat(message)")
    print("  - analyze_emotion(text)")
    print("  - digitize_ecg(image_path)")
    print("  - contribute_improvement(original, improved, description)")
    print("=" * 60)
