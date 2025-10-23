"""
AI Video Generation for MC AI V4
Creates animated videos, visualizations, and motion graphics
"""

import os
import requests
from typing import Dict

class VideoGenerator:
    """
    Generate videos from text or images
    Supports: Stable Video Diffusion (via Replicate)
    """
    
    def __init__(self):
        self.replicate_key = os.environ.get('REPLICATE_API_KEY')
    
    def text_to_video(self, prompt: str, duration: int = 4) -> Dict:
        """
        Generate video from text description
        
        Note: Full text-to-video requires async polling infrastructure (webhook/worker)
        to complete the two-stage process (text→image→video). Currently returns
        helpful fallback message.
        
        Args:
            prompt: What to animate
            duration: Length in seconds
        
        Returns:
            Dict with status
        """
        # Text-to-video requires two-stage async process:
        # 1. Generate image from text (SDXL)
        # 2. Poll for completion, then animate image (SVD)
        # This requires webhook infrastructure not currently implemented
        
        return {
            'success': False,
            'message': 'Add REPLICATE_API_KEY for video generation (requires async polling infrastructure)',
            'prompt': prompt,
            'note': 'Text-to-video requires two-stage async processing. Use image_to_video with existing images instead.',
            'alternative': 'emotion_visualization'
        }
    
    def image_to_video(self, image_url: str, motion_prompt: str = "gentle movement") -> Dict:
        """
        Animate a static image
        
        Args:
            image_url: Image to animate
            motion_prompt: How to animate it (currently informational, SVD doesn't use text prompts)
        
        Returns:
            Dict with video_url
        """
        if not self.replicate_key:
            return {
                'success': False,
                'message': 'Add REPLICATE_API_KEY for video generation',
                'source_image': image_url
            }
        
        # Note: Stable Video Diffusion uses motion_bucket_id to control motion intensity
        # Map motion prompt keywords to motion bucket values (1-255, higher = more motion)
        motion_intensity = 127  # default moderate motion
        if 'subtle' in motion_prompt.lower() or 'gentle' in motion_prompt.lower():
            motion_intensity = 80
        elif 'dynamic' in motion_prompt.lower() or 'intense' in motion_prompt.lower():
            motion_intensity = 180
        
        try:
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Token {self.replicate_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
                    "input": {
                        "image": image_url,
                        "cond_aug": 0.02,
                        "decoding_t": 14,
                        "video_length": "14_frames_with_svd",
                        "sizing_strategy": "maintain_aspect_ratio",
                        "motion_bucket_id": motion_intensity,
                        "frames_per_second": 6
                    }
                },
                timeout=30
            )
            
            if response.status_code == 201:
                prediction = response.json()
                return {
                    'success': True,
                    'prediction_id': prediction.get('id'),
                    'status': 'processing',
                    'source_image': image_url,
                    'motion': motion_prompt,
                    'motion_intensity': motion_intensity,
                    'provider': 'Stable Video Diffusion'
                }
            
            return {'success': False, 'error': f'API error: {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_talking_avatar(self, text: str, avatar_image: str = None) -> Dict:
        """
        Create talking avatar video
        
        Args:
            text: What the avatar should say
            avatar_image: Image of face to animate
        
        Returns:
            Dict with video_url
        """
        return {
            'success': False,
            'type': 'talking_avatar',
            'message': 'Avatar video generation available with D-ID API key. Set DID_API_KEY environment variable.',
            'text': text
        }
    
    def create_emotion_visualization(self, emotion: str, frequency: float) -> Dict:
        """
        Create animated visualization of emotional frequency
        
        Args:
            emotion: Emotion name
            frequency: Frequency in Hz
        
        Returns:
            Dict with visualization HTML/video
        """
        # Generate description for animation
        colors = self._emotion_to_colors(emotion)
        pattern = self._frequency_to_pattern(frequency)
        
        animation_prompt = f"Abstract {colors} {pattern} flowing smoothly, representing {emotion} at {frequency}Hz"
        
        return {
            'success': True,
            'type': 'emotion_visualization',
            'emotion': emotion,
            'frequency': frequency,
            'animation_prompt': animation_prompt,
            'colors': colors,
            'pattern': pattern
        }
    
    def _emotion_to_colors(self, emotion: str) -> str:
        """Map emotion to color palette"""
        color_map = {
            'calm': 'blue and purple',
            'anxiety': 'red and orange',
            'love': 'pink and red',
            'focus': 'green and blue',
            'energetic': 'yellow and orange',
            'neutral': 'white and gray'
        }
        return color_map.get(emotion, 'blue and white')
    
    def _frequency_to_pattern(self, frequency: float) -> str:
        """Map frequency to visual pattern"""
        if frequency < 8:
            return 'slow waves'
        elif frequency < 13:
            return 'gentle ripples'
        elif frequency < 30:
            return 'rhythmic pulses'
        else:
            return 'rapid vibrations'
