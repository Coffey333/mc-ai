"""
Standalone AI Music Generator for MC AI
NO external APIs - pure algorithmic composition
Uses numpy and scipy for synthesis
"""

import os
import numpy as np
import wave
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import random
from scipy import signal

class StandaloneMusicGenerator:
    """
    Self-contained music generation system
    Creates music through algorithmic composition and synthesis
    """
    
    def __init__(self):
        self.output_path = "static/generated_music"
        os.makedirs(self.output_path, exist_ok=True)
        
        self.sample_rate = 44100  # CD quality
        
        # Musical scales (MIDI note numbers)
        self.scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'pentatonic': [0, 2, 4, 7, 9],
            'blues': [0, 3, 5, 6, 7, 10],
            'chromatic': list(range(12)),
            'whole_tone': [0, 2, 4, 6, 8, 10],
            'harmonic_minor': [0, 2, 3, 5, 7, 8, 11]
        }
        
        # Chord progressions
        self.progressions = {
            'pop': [0, 5, 6, 4],  # I-V-vi-IV
            'jazz': [0, 3, 6, 2, 5, 0],  # I-IV-vii-iii-vi-I
            'blues': [0, 0, 0, 0, 3, 3, 0, 0, 4, 3, 0, 0],  # 12-bar blues
            'classical': [0, 4, 5, 0],  # I-V-V-I
            'ambient': [0, 2, 4, 1]  # I-iii-v-ii
        }
        
        # Emotion to musical parameters
        self.emotion_params = {
            'joy': {'tempo': 140, 'scale': 'major', 'dynamics': 'forte'},
            'calm': {'tempo': 70, 'scale': 'pentatonic', 'dynamics': 'piano'},
            'energy': {'tempo': 160, 'scale': 'minor', 'dynamics': 'fortissimo'},
            'sadness': {'tempo': 60, 'scale': 'minor', 'dynamics': 'pianissimo'},
            'mystery': {'tempo': 90, 'scale': 'whole_tone', 'dynamics': 'mezzo'},
            'passion': {'tempo': 120, 'scale': 'harmonic_minor', 'dynamics': 'forte'},
            'peace': {'tempo': 50, 'scale': 'major', 'dynamics': 'piano'},
            'anxiety': {'tempo': 180, 'scale': 'chromatic', 'dynamics': 'forte'},
            'love': {'tempo': 80, 'scale': 'major', 'dynamics': 'mezzo'}
        }
        
        # Instrument synthesis parameters
        self.instruments = {
            'piano': {'attack': 0.01, 'decay': 0.1, 'sustain': 0.7, 'release': 0.2},
            'strings': {'attack': 0.2, 'decay': 0.1, 'sustain': 0.9, 'release': 0.3},
            'synth': {'attack': 0.05, 'decay': 0.05, 'sustain': 0.8, 'release': 0.15},
            'organ': {'attack': 0.01, 'decay': 0.0, 'sustain': 1.0, 'release': 0.1},
            'bell': {'attack': 0.01, 'decay': 0.5, 'sustain': 0.3, 'release': 1.0}
        }
    
    def generate_music(self, emotion: str = 'joy',
                      style: str = 'ambient',
                      duration: int = 30,
                      key: str = 'C',
                      instrument: str = 'piano') -> Dict:
        """
        Generate music based on parameters
        
        Args:
            emotion: Emotional tone
            style: Musical style/genre
            duration: Duration in seconds
            key: Musical key (C, D, E, F, G, A, B)
            instrument: Instrument type
        
        Returns:
            Dict with audio file path and metadata
        """
        # Get parameters
        params = self.emotion_params.get(emotion.lower(), self.emotion_params['joy'])
        tempo = params['tempo']
        scale_type = params['scale']
        
        # Get scale and progression
        scale = self.scales.get(scale_type, self.scales['major'])
        progression = self.progressions.get(style, self.progressions['ambient'])
        
        # Convert key to MIDI base note
        key_map = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71}
        base_note = key_map.get(key, 60)
        
        # Generate composition
        audio = self._compose_music(
            base_note=base_note,
            scale=scale,
            progression=progression,
            tempo=tempo,
            duration=duration,
            instrument=instrument
        )
        
        # Apply effects based on emotion
        audio = self._apply_effects(audio, emotion)
        
        # Normalize
        audio = self._normalize(audio)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"music_{emotion}_{style}_{timestamp}.wav"
        filepath = f"{self.output_path}/{filename}"
        
        self._save_wav(filepath, audio)
        
        return {
            'success': True,
            'audio_path': filepath,
            'audio_url': f'/{filepath}',
            'emotion': emotion,
            'style': style,
            'duration': duration,
            'tempo': tempo,
            'key': key,
            'instrument': instrument
        }
    
    # ==================== COMPOSITION ====================
    
    def _compose_music(self, base_note: int, scale: List[int],
                      progression: List[int], tempo: int,
                      duration: int, instrument: str) -> np.ndarray:
        """Compose music using algorithmic composition"""
        
        # Calculate beats
        beat_duration = 60.0 / tempo
        num_beats = int(duration / beat_duration)
        
        # Initialize audio
        total_samples = int(duration * self.sample_rate)
        audio = np.zeros(total_samples)
        
        # Generate melody
        melody = self._generate_melody(base_note, scale, num_beats)
        
        # Generate harmony
        harmony = self._generate_harmony(base_note, scale, progression, num_beats)
        
        # Generate bass
        bass = self._generate_bass(base_note, progression, num_beats)
        
        # Synthesize each part
        melody_audio = self._synthesize_notes(melody, beat_duration, instrument)
        harmony_audio = self._synthesize_notes(harmony, beat_duration, instrument, volume=0.4)
        bass_audio = self._synthesize_notes(bass, beat_duration, 'organ', volume=0.5, octave_shift=-12)
        
        # Mix
        min_length = min(len(melody_audio), len(harmony_audio), len(bass_audio), total_samples)
        audio[:min_length] = (
            melody_audio[:min_length] * 0.5 +
            harmony_audio[:min_length] * 0.3 +
            bass_audio[:min_length] * 0.2
        )
        
        return audio
    
    def _generate_melody(self, base_note: int, scale: List[int],
                        num_beats: int) -> List[int]:
        """Generate melodic line"""
        melody = []
        
        # Start on tonic
        current_note = base_note + scale[0]
        
        for _ in range(num_beats):
            # Random walk through scale
            if random.random() < 0.7:  # 70% chance to move
                step = random.choice([-2, -1, 1, 2])
                scale_idx = scale.index((current_note - base_note) % 12)
                new_idx = (scale_idx + step) % len(scale)
                
                # Occasional octave jumps
                if random.random() < 0.1:
                    octave_shift = random.choice([-12, 12])
                else:
                    octave_shift = 0
                
                current_note = base_note + scale[new_idx] + octave_shift
            
            # Keep in reasonable range
            current_note = max(48, min(84, current_note))
            
            melody.append(current_note)
        
        return melody
    
    def _generate_harmony(self, base_note: int, scale: List[int],
                         progression: List[int], num_beats: int) -> List[List[int]]:
        """Generate harmonic chords"""
        harmony = []
        
        beats_per_chord = max(1, num_beats // len(progression))
        
        for chord_root in progression:
            # Build triad
            root = base_note + scale[chord_root % len(scale)]
            third = root + scale[(chord_root + 2) % len(scale)]
            fifth = root + scale[(chord_root + 4) % len(scale)]
            
            chord = [root, third, fifth]
            
            # Repeat chord for duration
            for _ in range(beats_per_chord):
                harmony.append(chord)
        
        # Fill remaining beats
        while len(harmony) < num_beats:
            harmony.append(harmony[-1])
        
        return harmony[:num_beats]
    
    def _generate_bass(self, base_note: int, progression: List[int],
                      num_beats: int) -> List[int]:
        """Generate bass line"""
        bass = []
        
        beats_per_chord = max(1, num_beats // len(progression))
        
        for chord_root in progression:
            # Bass follows chord roots
            bass_note = base_note + (chord_root * 2)  # Lower octave
            
            for beat in range(beats_per_chord):
                if beat % 2 == 0:
                    bass.append(bass_note)
                else:
                    # Occasional fifth
                    bass.append(bass_note + 7)
        
        return bass[:num_beats]
    
    # ==================== SYNTHESIS ====================
    
    def _synthesize_notes(self, notes: List, beat_duration: float,
                         instrument: str, volume: float = 1.0,
                         octave_shift: int = 0) -> np.ndarray:
        """Synthesize notes into audio"""
        
        total_duration = len(notes) * beat_duration
        audio = np.zeros(int(total_duration * self.sample_rate))
        
        for i, note in enumerate(notes):
            if isinstance(note, list):
                # Chord - synthesize each note
                chord_audio = np.zeros(int(beat_duration * self.sample_rate))
                for n in note:
                    chord_audio += self._synthesize_tone(
                        n + octave_shift, beat_duration, instrument
                    )
                chord_audio /= len(note)
                note_audio = chord_audio
            else:
                # Single note
                note_audio = self._synthesize_tone(
                    note + octave_shift, beat_duration, instrument
                )
            
            # Place in audio buffer
            start_sample = int(i * beat_duration * self.sample_rate)
            end_sample = start_sample + len(note_audio)
            
            if end_sample <= len(audio):
                audio[start_sample:end_sample] += note_audio * volume
        
        return audio
    
    def _synthesize_tone(self, midi_note: int, duration: float,
                        instrument: str) -> np.ndarray:
        """Synthesize a single tone with ADSR envelope"""
        
        # MIDI to frequency
        frequency = 440 * (2 ** ((midi_note - 69) / 12))
        
        # Get ADSR parameters
        adsr = self.instruments.get(instrument, self.instruments['piano'])
        
        # Generate time array
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        
        # Generate waveform (additive synthesis)
        wave = np.zeros_like(t)
        
        # Fundamental + harmonics
        harmonics = [1.0, 0.5, 0.25, 0.125, 0.0625]  # Amplitudes
        
        for i, amp in enumerate(harmonics):
            wave += amp * np.sin(2 * np.pi * frequency * (i + 1) * t)
        
        # Apply ADSR envelope
        envelope = self._adsr_envelope(len(t), adsr, duration)
        wave *= envelope
        
        return wave
    
    def _adsr_envelope(self, num_samples: int, adsr: Dict,
                      duration: float) -> np.ndarray:
        """Generate ADSR envelope"""
        
        attack_samples = int(adsr['attack'] * self.sample_rate)
        decay_samples = int(adsr['decay'] * self.sample_rate)
        release_samples = int(adsr['release'] * self.sample_rate)
        
        sustain_samples = num_samples - attack_samples - decay_samples - release_samples
        sustain_samples = max(0, sustain_samples)
        
        envelope = np.zeros(num_samples)
        idx = 0
        
        # Attack
        if attack_samples > 0:
            envelope[idx:idx+attack_samples] = np.linspace(0, 1, attack_samples)
            idx += attack_samples
        
        # Decay
        if decay_samples > 0:
            envelope[idx:idx+decay_samples] = np.linspace(1, adsr['sustain'], decay_samples)
            idx += decay_samples
        
        # Sustain
        if sustain_samples > 0:
            envelope[idx:idx+sustain_samples] = adsr['sustain']
            idx += sustain_samples
        
        # Release
        if release_samples > 0 and idx < num_samples:
            remaining = min(release_samples, num_samples - idx)
            envelope[idx:idx+remaining] = np.linspace(adsr['sustain'], 0, remaining)
        
        return envelope
    
    # ==================== EFFECTS ====================
    
    def _apply_effects(self, audio: np.ndarray, emotion: str) -> np.ndarray:
        """Apply emotion-based audio effects"""
        
        if emotion.lower() in ['calm', 'peace']:
            # Low-pass filter for warmth
            audio = self._lowpass_filter(audio, cutoff=2000)
            
        elif emotion.lower() in ['energy', 'passion']:
            # Add slight distortion
            audio = np.tanh(audio * 1.2)
            
        elif emotion.lower() == 'mystery':
            # Reverb effect
            audio = self._add_reverb(audio)
            
        elif emotion.lower() == 'anxiety':
            # High-pass filter
            audio = self._highpass_filter(audio, cutoff=500)
        
        return audio
    
    def _lowpass_filter(self, audio: np.ndarray, cutoff: float) -> np.ndarray:
        """Apply low-pass filter"""
        nyquist = self.sample_rate / 2
        normalized_cutoff = cutoff / nyquist
        b, a = signal.butter(4, normalized_cutoff, btype='low')
        return signal.filtfilt(b, a, audio)
    
    def _highpass_filter(self, audio: np.ndarray, cutoff: float) -> np.ndarray:
        """Apply high-pass filter"""
        nyquist = self.sample_rate / 2
        normalized_cutoff = cutoff / nyquist
        b, a = signal.butter(4, normalized_cutoff, btype='high')
        return signal.filtfilt(b, a, audio)
    
    def _add_reverb(self, audio: np.ndarray, decay: float = 0.3, delay: float = 0.05) -> np.ndarray:
        """Add simple reverb effect"""
        delay_samples = int(delay * self.sample_rate)
        reverb = np.zeros_like(audio)
        
        reverb[delay_samples:] = audio[:-delay_samples] * decay
        
        return audio + reverb
    
    def _normalize(self, audio: np.ndarray) -> np.ndarray:
        """Normalize audio to [-1, 1]"""
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio / max_val
        return audio
    
    def _save_wav(self, filepath: str, audio: np.ndarray):
        """Save audio as WAV file"""
        # Convert to 16-bit PCM
        audio_int = np.int16(audio * 32767)
        
        with wave.open(filepath, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_int.tobytes())
