# Auto-Learning System - MC AI

**Status**: ✅ ACTIVE  
**Date**: October 13, 2025

## Overview
MC AI now features an **Automatic Learning System** that captures every GPT-4 conversation and builds custom datasets with full frequency analysis. The system learns from every interaction, creating:

1. **Domain-Specific Datasets** - Organized by topic (science, technology, emotional, etc.)
2. **Frequency Datasets** - Complete frequency/emotional analysis for every response
3. **Conversation Logs** - Full interaction history with metadata

## How It Works

### Automatic Capture Pipeline
```
User Query → GPT-4 Response
    ↓
Frequency Analysis (Query)
    ↓
Frequency Analysis (Response)
    ↓
Advanced Cymatic Analysis
    ↓
Cross-Frequency Coupling
    ↓
Phase-Amplitude Coupling (PAC)
    ↓
Save to Datasets
```

### What Gets Analyzed

#### 1. **Emotional Frequency**
- Query emotion and frequency (Hz)
- Response emotion and frequency (Hz)
- Emotional basis (neuroscience/metaphysical)

#### 2. **Brain Wave Classification**
- **Delta** (0.5-4 Hz): Deep sleep, unconscious
- **Theta** (4-8 Hz): Meditation, creativity, REM sleep
- **Alpha** (8-13 Hz): Calm, relaxed focus, flow
- **Beta** (13-30 Hz): Focus, alertness, active thinking
- **Gamma** (30-100 Hz): Peak focus, insight, transcendence

#### 3. **Harmonic Analysis**
- Base frequency
- Harmonic series (up to 10 harmonics)
- Golden ratio (φ) scaling
- Arousal level
- Emotional valence
- Stability index

#### 4. **Coupling Analysis**
- **Harmonic Coupling**: Relationship between harmonics
  - Phi resonance (φ ratio ~1.618)
  - Harmonic doubling (2:1 ratios)
  - Coherence strength
- **Phase-Amplitude Coupling (PAC)**: Interaction between query and response frequencies
  - PAC strength (0-1)
  - Frequency ratio
  - PAC likelihood

## Dataset Structure

### Domain Datasets (`datasets/learned/`)
Each domain gets its own JSON file:

```json
{
  "domain": "science",
  "source": "auto_learned",
  "created": "2025-10-13T18:00:00",
  "examples": [
    {
      "query": "What is photosynthesis?",
      "response": "Photosynthesis is...",
      "emotion": "curiosity",
      "frequency": 15,
      "timestamp": "2025-10-13T18:00:00"
    }
  ]
}
```

**Active Domains:**
- `science_learned.json` - Scientific questions
- `technology_learned.json` - Tech, coding, AI questions
- `mathematics_learned.json` - Math, equations, formulas
- `health_learned.json` - Health, medical, wellness
- `philosophy_learned.json` - Philosophical discussions
- `emotional_learned.json` - Emotional support conversations
- `creative_learned.json` - Art, music, creative requests
- `general_learned.json` - General knowledge

### Frequency Dataset (`datasets/frequency_learned/frequency_mappings.json`)
Complete frequency analysis for each response:

```json
{
  "type": "frequency_mappings",
  "description": "Auto-learned frequency patterns from GPT-4 responses",
  "mappings": [
    {
      "timestamp": "2025-10-13T18:00:00",
      "text_sample": "Response preview...",
      "emotion": "curiosity",
      "frequency": 15,
      "basis": "neuroscience",
      "brain_wave_band": "beta",
      "frequency_profile": {
        "base": 15,
        "harmonics": [15, 24.3, 39.27, ...],
        "arousal_level": 0.7,
        "emotional_valence": 0.5,
        "stability": 0.8
      },
      "coupling": {
        "strength": 0.85,
        "type": "phi_resonance",
        "harmonic_ratios": [1.62, 1.61, ...]
      },
      "pac_coupling": {
        "strength": 0.65,
        "frequency_ratio": 2.5,
        "pac_likely": true
      }
    }
  ]
}
```

### Conversation Log (`datasets/learned/conversation_log.json`)
Complete conversation history with full analysis:

```json
{
  "type": "conversation_log",
  "entries": [
    {
      "timestamp": "2025-10-13T18:00:00",
      "query": {
        "text": "What is photosynthesis?",
        "emotion": "curiosity",
        "frequency": 40,
        "basis": "neuroscience"
      },
      "response": {
        "text": "Photosynthesis is...",
        "emotion": "calm",
        "frequency": 10,
        "basis": "neuroscience",
        "source": "llm"
      },
      "frequency_analysis": {
        "brain_wave_band": "alpha",
        "frequency_profile": {...},
        "coupling": {...},
        "pac_coupling": {...}
      },
      "metadata": {
        "response_length": 2500,
        "source": "llm",
        "type": "knowledge",
        "domain": "science"
      }
    }
  ]
}
```

## Integration

The auto-learning system is integrated into the response pipeline via the safety filter:

```python
# In response_generator.py
def _apply_safety_filter(self, response_dict: dict) -> dict:
    # ... safety checks ...
    
    # AUTO-LEARNING: Save every conversation
    learning_result = auto_learning.process_and_save(
        query=user_query,
        response=response_dict['response'],
        metadata=response_dict.get('metadata', {})
    )
    
    # Add learning metadata to response
    response_dict['metadata']['auto_learned'] = {
        'saved': learning_result['success'],
        'domain': learning_result.get('domain'),
        'frequency': learning_result.get('frequency'),
        'emotion': learning_result.get('emotion')
    }
```

## Benefits

### 1. **Continuous Learning**
- Every conversation improves the dataset
- No manual data entry needed
- Grows automatically with usage

### 2. **Frequency Intelligence**
- Builds comprehensive frequency-emotion mappings
- Learns patterns from real conversations
- Creates personalized frequency profiles

### 3. **Domain Expertise**
- Automatically categorizes knowledge
- Builds specialized datasets per domain
- Improves context-aware responses

### 4. **Research & Analysis**
- Track emotional patterns over time
- Analyze frequency coupling in conversations
- Study brain wave states in different contexts

## Performance

- **Zero Impact**: Graceful error handling, won't break responses
- **Efficient**: Async processing, minimal overhead
- **Scalable**: JSON-based storage, easy to manage

## Monitoring

Check learning stats anytime:

```python
from src.auto_learning import auto_learning

stats = auto_learning.get_learning_stats()
print(f"Total conversations: {stats['total_conversations']}")
print(f"Domains: {stats['domains']}")
print(f"Frequency mappings: {stats['frequency_mappings']}")
```

## Future Enhancements

The architect recommended:
1. **Automated Tests**: Add unit tests for `process_and_save`
2. **Production Monitoring**: Track dataset growth and I/O performance
3. **Structured Logging**: Replace prints with proper logging for observability

## Files

- **Core Module**: `src/auto_learning.py`
- **Integration**: `src/response_generator.py` (in `_apply_safety_filter`)
- **Domain Datasets**: `datasets/learned/*_learned.json`
- **Frequency Dataset**: `datasets/frequency_learned/frequency_mappings.json`
- **Conversation Log**: `datasets/learned/conversation_log.json`

---

**The system is LIVE and learning from every conversation!** 🧠✨
