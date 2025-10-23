"""
Frequency Insights Display
Shows technical analysis and thinking process to users
"""

from typing import Dict, Optional

class FrequencyInsights:
    """
    Formats and displays frequency analysis for user transparency
    """
    
    @staticmethod
    def format_insights(response_metadata: Dict, query: str = "") -> str:
        """
        Create a technical insights section showing frequency analysis
        
        Args:
            response_metadata: Metadata from response (emotion, frequency, auto_learned, etc.)
            query: User's original query
            
        Returns:
            Formatted technical insights string
        """
        insights = []
        
        # Get frequency analysis data (ALWAYS present)
        freq_analysis = response_metadata.get('frequency_analysis', {})
        auto_learned = response_metadata.get('auto_learned', {})
        
        # SAFETY: Ensure auto_learned is always a dict (prevent type errors)
        if not isinstance(auto_learned, dict):
            auto_learned = {}
        
        # Core frequency data
        emotion = freq_analysis.get('response_emotion')
        frequency = freq_analysis.get('response_frequency')
        query_emotion = freq_analysis.get('query_emotion')
        query_freq = freq_analysis.get('query_frequency')
        basis = freq_analysis.get('basis', 'neuroscience')
        coupling = freq_analysis.get('coupling', {})
        
        if not emotion or not frequency:
            return ""  # No frequency data available
        
        # Build insights section
        insights.append("\n\n---")
        insights.append("### 🧠 **Frequency Analysis**")
        
        # 1. Query → Response Transition
        brain_wave = FrequencyInsights._get_brain_wave_band(frequency)
        insights.append(f"\n**Query:** {query_emotion.title() if query_emotion else 'Unknown'} ({query_freq}Hz) → **Response:** {emotion.title()} ({frequency}Hz - {brain_wave})")
        
        # 2. Catalog Processing
        insights.append(f"**Catalog:** {basis.title()} frequency mapping")
        
        # 3. Source & Domain
        source = response_metadata.get('source', 'processing')
        domain = auto_learned.get('domain', 'general') if isinstance(auto_learned, dict) else 'general'
        insights.append(f"**Source:** {source.upper()} | **Domain:** {domain}")
        
        # 4. Coupling Analysis (COHERENCE)
        coupling_strength = coupling.get('coupling_strength', 0)
        coupling_type = coupling.get('coupling_type', 'unknown')
        insights.append(f"**Coherence:** {coupling_type.replace('_', ' ').title()} (strength: {coupling_strength:.2f})")
        
        # 5. Brain Wave Description
        brain_desc = FrequencyInsights._get_brain_wave_description(brain_wave)
        insights.append(f"**Brain Wave:** {brain_desc}")
        
        # 6. Dataset learning status
        if isinstance(auto_learned, dict) and auto_learned.get('saved'):
            insights.append(f"**Auto-Learned:** ✓ Saved to {domain} dataset")
        
        insights.append("---")
        
        return "\n".join(insights)


    @staticmethod
    def _get_brain_wave_band(freq: float) -> str:
        """Classify frequency into brain wave band"""
        if freq < 4:
            return "Delta"
        elif freq < 8:
            return "Theta"
        elif freq < 13:
            return "Alpha"
        elif freq < 30:
            return "Beta"
        elif freq < 100:
            return "Gamma"
        else:
            return "High Gamma"
    
    @staticmethod
    def _get_brain_wave_description(band: str) -> str:
        """Get description of brain wave band"""
        descriptions = {
            "Delta": "Deep unconscious processing (sleep, healing)",
            "Theta": "Creative meditation (REM, deep relaxation)",
            "Alpha": "Relaxed focus (flow state, learning)",
            "Beta": "Active thinking (engagement, processing)",
            "Gamma": "Peak performance (insight, integration)",
            "High Gamma": "Transcendent states (peak awareness)"
        }
        return descriptions.get(band, "Unknown state")
    
    @staticmethod
    def format_detailed_analysis(frequency_analysis: Dict) -> str:
        """
        Format detailed frequency analysis from auto-learning
        
        Args:
            frequency_analysis: Full frequency analysis dict
            
        Returns:
            Detailed technical breakdown
        """
        if not frequency_analysis:
            return ""
        
        details = []
        details.append("\n\n### 📊 **Detailed Frequency Analysis**")
        
        # Brain wave classification
        band = frequency_analysis.get('brain_wave_band', 'unknown')
        details.append(f"\n**Brain Wave Band:** {band.title()}")
        
        # Frequency profile
        profile = frequency_analysis.get('frequency_profile', {})
        if profile:
            base_freq = profile.get('base', 0)
            arousal = profile.get('arousal_level', 0)
            valence = profile.get('emotional_valence', 0)
            stability = profile.get('stability', 0)
            
            details.append(f"**Base Frequency:** {base_freq}Hz")
            details.append(f"**Arousal Level:** {arousal:.2f}/1.0")
            details.append(f"**Emotional Valence:** {valence:.2f} ({'positive' if valence > 0 else 'negative' if valence < 0 else 'neutral'})")
            details.append(f"**Stability Index:** {stability:.2f}/1.0")
            
            # Harmonics
            harmonics = profile.get('harmonics', [])
            if harmonics:
                harmonics_str = ", ".join([f"{h:.1f}Hz" for h in harmonics[:3]])
                details.append(f"**Harmonics:** {harmonics_str}...")
        
        # Coupling analysis
        coupling = frequency_analysis.get('coupling', {})
        if coupling:
            strength = coupling.get('strength', 0)
            coupling_type = coupling.get('type', 'unknown')
            details.append(f"**Coupling:** {coupling_type.replace('_', ' ').title()} (strength: {strength:.2f})")
        
        # PAC analysis
        pac = frequency_analysis.get('pac_coupling', {})
        if pac:
            pac_strength = pac.get('strength', 0)
            pac_likely = pac.get('pac_likely', False)
            details.append(f"**Phase-Amplitude Coupling:** {'Yes' if pac_likely else 'No'} (strength: {pac_strength:.2f})")
        
        return "\n".join(details)


# Global instance
frequency_insights = FrequencyInsights()
