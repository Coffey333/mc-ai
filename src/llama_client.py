"""
Llama Integration for MC AI
Free, local LLM via Ollama
"""

import requests
import json
import os
import time
from typing import Dict, List, Optional, Generator
from enum import Enum

class LlamaModel(Enum):
    """Available Llama models"""
    LLAMA_3_3_70B = "llama3.3:70b"  # Best quality, slowest
    LLAMA_3_2_7B = "llama3.2:7b"    # Good balance
    LLAMA_3_2_3B = "llama3.2:3b"    # Fastest, smallest
    LLAMA_3_2_1B = "llama3.2:1b"    # Ultra-fast, minimal

class LlamaClient:
    """
    Client for local Llama models via Ollama
    """
    
    def __init__(self, 
                 model: Optional[str] = None,
                 base_url: str = "http://localhost:11434",
                 timeout: int = 120):
        """
        Initialize Llama client
        
        Args:
            model: Llama model to use (default: llama3.2:3b for speed)
            base_url: Ollama server URL
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        
        # Determine model (default to 3B for Replit - faster, less memory)
        if model:
            self.model = model
        else:
            # Try to get from environment, default to 3B (best for Replit)
            self.model = os.getenv('LLAMA_MODEL', LlamaModel.LLAMA_3_2_3B.value)
        
        # Check if Ollama is available
        self.available = self._check_availability()
        
        if not self.available:
            print("⚠️  Ollama not running. Install with: curl -fsSL https://ollama.ai/install.sh | sh")
            print("⚠️  Then run: ollama serve")
    
    def _check_availability(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def complete(self, 
                 system_prompt: str,
                 messages: List[Dict],
                 max_tokens: int = 500,
                 temperature: float = 0.7) -> Dict:
        """
        Get completion from Llama
        
        Args:
            system_prompt: System instructions
            messages: Conversation history
            max_tokens: Max response length
            temperature: Sampling temperature (0-1)
        
        Returns:
            Dict with text and metadata
        """
        if not self.available:
            raise Exception("Ollama server not available. Run: ollama serve")
        
        # Format messages for Llama
        formatted_messages = self._format_messages(system_prompt, messages)
        
        # Make request
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    'model': self.model,
                    'messages': formatted_messages,
                    'stream': False,
                    'options': {
                        'num_predict': max_tokens,
                        'temperature': temperature
                    }
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                elapsed = time.time() - start_time
                
                return {
                    'text': data['message']['content'],
                    'model': self.model,
                    'provider': 'llama_local',
                    'tokens': data.get('eval_count', 0),
                    'response_time': round(elapsed, 2),
                    'done': data.get('done', True)
                }
            else:
                raise Exception(f"Ollama error: {response.status_code} - {response.text}")
        
        except requests.exceptions.Timeout:
            raise Exception(f"Llama request timed out after {self.timeout}s")
        except Exception as e:
            raise Exception(f"Llama completion failed: {e}")
    
    def stream_complete(self,
                       system_prompt: str,
                       messages: List[Dict],
                       max_tokens: int = 500,
                       temperature: float = 0.7) -> Generator[str, None, None]:
        """
        Stream completion from Llama (for real-time responses)
        
        Args:
            system_prompt: System instructions
            messages: Conversation history
            max_tokens: Max response length
            temperature: Sampling temperature
        
        Yields:
            Text chunks as they're generated
        """
        if not self.available:
            raise Exception("Ollama server not available")
        
        formatted_messages = self._format_messages(system_prompt, messages)
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    'model': self.model,
                    'messages': formatted_messages,
                    'stream': True,
                    'options': {
                        'num_predict': max_tokens,
                        'temperature': temperature
                    }
                },
                stream=True,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if 'message' in data:
                            chunk = data['message'].get('content', '')
                            if chunk:
                                yield chunk
                        
                        if data.get('done', False):
                            break
            else:
                raise Exception(f"Ollama error: {response.status_code}")
        
        except Exception as e:
            raise Exception(f"Streaming failed: {e}")
    
    def _format_messages(self, system_prompt: str, messages: List[Dict]) -> List[Dict]:
        """Format messages for Llama"""
        formatted = []
        
        # Add system message
        if system_prompt:
            formatted.append({
                'role': 'system',
                'content': system_prompt
            })
        
        # Add conversation messages
        for msg in messages:
            formatted.append({
                'role': msg.get('role', 'user'),
                'content': msg.get('content', '')
            })
        
        return formatted
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        if not self.available:
            return []
        
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return [m['name'] for m in data.get('models', [])]
        except:
            pass
        
        return []
    
    def get_model_info(self) -> Dict:
        """Get information about current model"""
        if not self.available:
            return {'available': False, 'model': self.model}
        
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={'name': self.model},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'available': True,
                    'model': self.model,
                    'parameters': data.get('details', {}).get('parameter_size', 'unknown'),
                    'family': data.get('details', {}).get('family', 'llama'),
                    'quantization': data.get('details', {}).get('quantization_level', 'unknown')
                }
        except:
            pass
        
        return {'available': False, 'model': self.model}
    
    def pull_model(self, model_name: Optional[str] = None) -> bool:
        """
        Pull a model from Ollama registry
        
        Args:
            model_name: Model to pull (default: self.model)
        
        Returns:
            Success status
        """
        if not self.available:
            return False
        
        model = model_name or self.model
        
        print(f"📥 Pulling {model}... This may take a while.")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={'name': model},
                timeout=600  # 10 minutes for large models
            )
            
            if response.status_code == 200:
                print(f"✅ Model {model} ready")
                return True
            else:
                print(f"❌ Failed to pull model: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Failed to pull model: {e}")
            return False
