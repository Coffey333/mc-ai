"""
Advanced AI Art Generation for MC AI
Integrates with multiple AI image generation APIs
PRIORITY: Standalone generator (no API keys needed)
"""

import os
import requests
import base64
from typing import Dict, Optional, List
from io import BytesIO
from PIL import Image
from src.standalone_art_generator import StandaloneArtGenerator

class ArtGenerator:
    """
    Multi-provider AI art generation system
    Supports: Standalone (no API), OpenAI DALL-E, Stability AI, Replicate
    """
    
    def __init__(self):
        # Initialize standalone generator (always available)
        self.standalone = StandaloneArtGenerator()
        
        # API keys from environment variables
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        self.stability_key = os.environ.get('STABILITY_API_KEY')
        self.replicate_key = os.environ.get('REPLICATE_API_KEY')
        
        # Track which services are available
        self.available_services = []
        if self.openai_key:
            self.available_services.append('dalle')
        if self.stability_key:
            self.available_services.append('stability')
        if self.replicate_key:
            self.available_services.append('replicate')
    
    def generate_art(self, user_request: str, style: str = "auto", emotion: str = "neutral") -> Dict:
        """
        Generate artwork based on user request
        
        Args:
            user_request: What user wants to see
            style: Art style (realistic, abstract, anime, oil_painting, digital, etc.)
            emotion: Emotional tone to incorporate
        
        Returns:
            Dict with image_url, prompt_used, style, provider
        """
        # PRIORITY 1: Use standalone generator (no API needed)
        try:
            # Map style to standalone style
            style_map = {
                'abstract': 'abstract',
                'realistic': 'landscape',
                'auto': 'abstract',
                'surreal': 'fractal',
                'digital': 'geometric',
                'watercolor': 'organic',
                'cyberpunk': 'galaxy',
                'anime': 'particles',
                'oil_painting': 'waves'
            }
            
            standalone_style = style_map.get(style, 'abstract')
            result = self.standalone.generate_art(
                prompt=user_request,
                style=standalone_style,
                emotion=emotion
            )
            
            if result.get('success'):
                return {
                    'success': True,
                    'image_url': result['image_url'],
                    'prompt': user_request,
                    'provider': 'MC AI Standalone Generator',
                    'style': style,
                    'emotion': emotion
                }
        except Exception as e:
            print(f"Standalone generator failed: {e}")
        
        # PRIORITY 2: Try external API services if standalone fails
        enhanced_prompt = self._enhance_prompt(user_request, style, emotion)
        
        for service in self.available_services:
            try:
                if service == 'dalle':
                    return self._generate_dalle(enhanced_prompt)
                elif service == 'stability':
                    return self._generate_stability(enhanced_prompt)
                elif service == 'replicate':
                    return self._generate_replicate(enhanced_prompt)
            except Exception as e:
                print(f"Failed with {service}: {e}")
                continue
        
        # If all fail, return fallback
        return self._generate_fallback(user_request)
    
    def _enhance_prompt(self, user_request: str, style: str, emotion: str) -> str:
        """
        Enhance user prompt with MC AI's emotional intelligence
        """
        # Map emotions to visual qualities
        emotion_qualities = {
            'anxiety': 'chaotic energy, swirling patterns, intense colors',
            'calm': 'peaceful, serene, soft lighting, gentle colors',
            'focus': 'sharp, clear, geometric precision, vibrant focus point',
            'love': 'warm glowing light, harmonious colors, embracing forms',
            'transcendence': 'ethereal, cosmic, luminous, ascending energy',
            'curiosity': 'intricate details, mysterious elements, discovery theme',
            'neutral': 'balanced composition, natural lighting'
        }
        
        # Map styles to art techniques
        style_prompts = {
            'realistic': 'photorealistic, highly detailed, professional photography',
            'abstract': 'abstract expressionism, non-representational, emotional forms',
            'anime': 'anime style, manga art, vibrant cel-shading',
            'oil_painting': 'oil painting, classical art style, textured brushstrokes',
            'digital': 'digital art, modern illustration, clean design',
            'surreal': 'surrealistic, dreamlike, Salvador Dali inspired',
            'cyberpunk': 'cyberpunk aesthetic, neon lights, futuristic dystopia',
            'watercolor': 'watercolor painting, soft edges, flowing colors',
            'auto': ''  # Let AI decide
        }
        
        emotion_quality = emotion_qualities.get(emotion, emotion_qualities['neutral'])
        style_prompt = style_prompts.get(style, '')
        
        # Construct enhanced prompt
        prompt_parts = [user_request]
        
        if style_prompt:
            prompt_parts.append(style_prompt)
        
        prompt_parts.append(emotion_quality)
        prompt_parts.append("high quality, professional, detailed")
        
        return ", ".join(prompt_parts)
    
    def _generate_dalle(self, prompt: str) -> Dict:
        """Generate using OpenAI DALL-E"""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            return {
                'success': True,
                'image_url': response.data[0].url,
                'prompt': prompt,
                'provider': 'DALL-E 3 (OpenAI)',
                'style': 'AI-generated digital art'
            }
        except Exception as e:
            raise Exception(f"DALL-E error: {e}")
    
    def _generate_stability(self, prompt: str) -> Dict:
        """Generate using Stability AI"""
        api_host = 'https://api.stability.ai'
        
        response = requests.post(
            f"{api_host}/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.stability_key}"
            },
            json={
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )
        
        if response.status_code != 200:
            raise Exception(f"Stability AI error: {response.text}")
        
        data = response.json()
        
        # Save image
        image_data = base64.b64decode(data["artifacts"][0]["base64"])
        image_path = f"/tmp/art_{hash(prompt) % 10000}.png"
        
        with open(image_path, 'wb') as f:
            f.write(image_data)
        
        return {
            'success': True,
            'image_url': f'file://{image_path}',
            'prompt': prompt,
            'provider': 'Stable Diffusion XL (Stability AI)',
            'style': 'AI-generated digital art'
        }
    
    def _generate_replicate(self, prompt: str) -> Dict:
        """Generate using Replicate API"""
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers={
                "Authorization": f"Token {self.replicate_key}",
                "Content-Type": "application/json"
            },
            json={
                "version": "stability-ai/sdxl",
                "input": {"prompt": prompt}
            }
        )
        
        if response.status_code != 201:
            raise Exception(f"Replicate error: {response.text}")
        
        prediction = response.json()
        
        return {
            'success': True,
            'image_url': prediction.get('output', [''])[0],
            'prompt': prompt,
            'provider': 'SDXL (Replicate)',
            'style': 'AI-generated digital art'
        }
    
    def _generate_fallback(self, user_request: str) -> Dict:
        """
        Fallback: Generate cymatic pattern visualization
        When no API keys available
        """
        return {
            'success': False,
            'error': 'No AI art API keys configured',
            'message': 'To generate advanced AI artwork, add API keys to environment variables: OPENAI_API_KEY, STABILITY_API_KEY, or REPLICATE_API_KEY',
            'prompt': user_request,
            'provider': 'none',
            'fallback': 'cymatic_pattern'
        }
    
    def get_style_suggestions(self, emotion: str) -> List[str]:
        """Suggest art styles based on emotional state"""
        style_map = {
            'anxiety': ['abstract', 'surreal', 'expressionist'],
            'calm': ['watercolor', 'realistic', 'minimalist'],
            'focus': ['digital', 'geometric', 'modern'],
            'love': ['oil_painting', 'romantic', 'soft_focus'],
            'transcendence': ['surreal', 'cosmic', 'ethereal'],
            'curiosity': ['detailed', 'fantasy', 'exploratory']
        }
        return style_map.get(emotion, ['realistic', 'digital', 'abstract'])
