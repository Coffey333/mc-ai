"""
AI Music & Audio Generation for MC AI
Creates original music, sound effects, and audio based on emotions
PRIORITY: Standalone generator (no API keys needed)
"""

import os
import requests
import json
from typing import Dict
from src.standalone_music_generator import StandaloneMusicGenerator

class MusicGenerator:
    """
    Generate music and audio using AI
    Supports: Standalone (no API), MusicGen (Replicate), ElevenLabs (voice)
    """
    
    def __init__(self):
        # Initialize standalone generator (always available)
        self.standalone = StandaloneMusicGenerator()
        
        self.elevenlabs_key = os.environ.get('ELEVENLABS_API_KEY')
        self.replicate_key = os.environ.get('REPLICATE_API_KEY')
    
    def generate_music(self, emotion: str, style: str = "ambient", duration: int = 30) -> Dict:
        """
        Generate original music based on emotion
        
        Args:
            emotion: Emotional state (calm, energetic, melancholic, etc.)
            style: Music style (ambient, electronic, orchestral, lofi, etc.)
            duration: Length in seconds
        
        Returns:
            Dict with audio_url, style, emotion, bpm
        """
        # PRIORITY 1: Use standalone generator (no API needed)
        try:
            result = self.standalone.generate_music(
                emotion=emotion,
                style=style,
                duration=duration
            )
            
            if result.get('success'):
                return {
                    'success': True,
                    'audio_url': result['audio_url'],
                    'emotion': emotion,
                    'style': style,
                    'duration': duration,
                    'provider': 'MC AI Standalone Generator',
                    'tempo': result.get('tempo', 120)
                }
        except Exception as e:
            print(f"Standalone generator failed: {e}")
        
        # PRIORITY 2: Try external API services if standalone fails
        music_params = self._get_music_params(emotion, style)
        
        # Generate using MusicGen via Replicate
        if self.replicate_key:
            return self._generate_musicgen(music_params, duration)
        
        return {
            'success': False,
            'message': 'Add REPLICATE_API_KEY to generate music',
            'fallback': 'cymatic_audio_pattern',
            'emotion': emotion,
            'style': style
        }
    
    def generate_voice(self, text: str, emotion: str = "neutral", voice: str = "default") -> Dict:
        """
        Convert text to speech with emotional inflection
        
        Args:
            text: What to say
            emotion: How to say it (happy, sad, excited, calm)
            voice: Voice ID to use
        
        Returns:
            Dict with audio_url, text, emotion
        """
        if not self.elevenlabs_key:
            return {
                'success': False,
                'message': 'Add ELEVENLABS_API_KEY for voice generation',
                'text': text,
                'emotion': emotion
            }
        
        # Map emotion to voice settings
        voice_settings = self._get_voice_settings(emotion)
        
        try:
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{self._get_voice_id(voice)}",
                headers={
                    "xi-api-key": self.elevenlabs_key,
                    "Content-Type": "application/json"
                },
                json={
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": voice_settings
                },
                timeout=30
            )
            
            if response.status_code == 200:
                # Save audio
                os.makedirs("/tmp/audio_outputs", exist_ok=True)
                audio_path = f"/tmp/audio_outputs/voice_{hash(text) % 10000}.mp3"
                with open(audio_path, 'wb') as f:
                    f.write(response.content)
                
                return {
                    'success': True,
                    'audio_url': audio_path,
                    'text': text,
                    'emotion': emotion,
                    'provider': 'ElevenLabs'
                }
            
            return {'success': False, 'error': f'API error: {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_sound_effect(self, description: str) -> Dict:
        """
        Generate custom sound effects
        
        Args:
            description: What sound to create (e.g., "ocean waves", "thunderstorm")
        
        Returns:
            Dict with audio_url
        """
        # Use AudioCraft via Replicate
        prompt = f"High quality sound effect: {description}"
        
        if self.replicate_key:
            try:
                response = requests.post(
                    "https://api.replicate.com/v1/predictions",
                    headers={
                        "Authorization": f"Token {self.replicate_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "version": "facebook/musicgen:7a76a8258b23fae65c5a22debb8841d1d7e816063ee6441d97d942a4c51d6d2b",
                        "input": {
                            "prompt": prompt,
                            "duration": 10
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
                        'description': description,
                        'provider': 'MusicGen'
                    }
            except Exception as e:
                return {'success': False, 'error': str(e)}
        
        return {
            'success': False,
            'message': 'Add REPLICATE_API_KEY for sound effects'
        }
    
    def create_binaural_beats(self, target_frequency: float, base_frequency: float = 200) -> Dict:
        """
        Generate binaural beats for brain entrainment
        
        Args:
            target_frequency: Desired brain wave frequency (e.g., 10Hz for alpha)
            base_frequency: Carrier frequency
        
        Returns:
            Dict with audio file for left/right channels
        """
        # Create two tones slightly offset
        left_freq = base_frequency
        right_freq = base_frequency + target_frequency
        
        return {
            'success': True,
            'type': 'binaural_beats',
            'target_frequency': f'{target_frequency}Hz',
            'left_frequency': f'{left_freq}Hz',
            'right_frequency': f'{right_freq}Hz',
            'description': f'Binaural beat for {self._frequency_to_state(target_frequency)}',
            'instructions': 'Use headphones for best effect',
            'brain_state': self._frequency_to_state(target_frequency)
        }
    
    def _get_music_params(self, emotion: str, style: str) -> Dict:
        """Map emotion to musical parameters"""
        emotion_map = {
            'calm': {'tempo': 'slow', 'mood': 'peaceful', 'instruments': 'piano, strings'},
            'anxiety': {'tempo': 'fast', 'mood': 'tense', 'instruments': 'synthesizer, percussion'},
            'focus': {'tempo': 'moderate', 'mood': 'steady', 'instruments': 'electronic, minimal'},
            'love': {'tempo': 'moderate', 'mood': 'warm', 'instruments': 'acoustic guitar, violin'},
            'energetic': {'tempo': 'fast', 'mood': 'uplifting', 'instruments': 'drums, bass, synth'},
            'neutral': {'tempo': 'moderate', 'mood': 'ambient', 'instruments': 'synthesizer, pads'}
        }
        
        return {
            'emotion': emotion,
            'style': style,
            **emotion_map.get(emotion, emotion_map['neutral'])
        }
    
    def _get_voice_settings(self, emotion: str) -> Dict:
        """Map emotion to voice parameters"""
        settings = {
            'neutral': {'stability': 0.5, 'similarity_boost': 0.75},
            'happy': {'stability': 0.7, 'similarity_boost': 0.8},
            'sad': {'stability': 0.3, 'similarity_boost': 0.6},
            'excited': {'stability': 0.8, 'similarity_boost': 0.9},
            'calm': {'stability': 0.4, 'similarity_boost': 0.7}
        }
        return settings.get(emotion, settings['neutral'])
    
    def _get_voice_id(self, voice: str) -> str:
        """Get ElevenLabs voice ID"""
        voices = {
            'default': '21m00Tcm4TlvDq8ikWAM',  # Rachel
            'male': 'VR6AewLTigWG4xSOukaG',      # Arnold
            'female': 'EXAVITQu4vr4xnSDxMaL'     # Bella
        }
        return voices.get(voice, voices['default'])
    
    def _frequency_to_state(self, freq: float) -> str:
        """Convert frequency to brain state"""
        if freq < 4:
            return 'deep sleep (delta)'
        elif freq < 8:
            return 'meditation (theta)'
        elif freq < 13:
            return 'relaxed focus (alpha)'
        elif freq < 30:
            return 'active thinking (beta)'
        else:
            return 'peak cognition (gamma)'
    
    def _generate_musicgen(self, params: Dict, duration: int) -> Dict:
        """Generate music using MusicGen"""
        prompt = f"{params['mood']} {params['style']} music with {params['instruments']}, {params['tempo']} tempo"
        
        try:
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Token {self.replicate_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": "facebook/musicgen:7a76a8258b23fae65c5a22debb8841d1d7e816063ee6441d97d942a4c51d6d2b",
                    "input": {
                        "prompt": prompt,
                        "duration": duration
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
                    'prompt': prompt,
                    'emotion': params['emotion'],
                    'style': params['style'],
                    'provider': 'MusicGen'
                }
            
            return {'success': False, 'error': f'API error: {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
