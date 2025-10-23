"""Dual-catalog emotion detection for MC AI."""

NEUROSCIENCE_CATALOG = {
    'anxiety': {'freq': 13, 'basis': 'beta wave dominance'},
    'calm': {'freq': 10, 'basis': 'alpha wave relaxation'},
    'focus': {'freq': 40, 'basis': 'gamma cognitive binding'},
    'stress': {'freq': 15, 'basis': 'high beta arousal'},
    'meditation': {'freq': 7, 'basis': 'theta wave deep relaxation'},
    'curiosity': {'freq': 40, 'basis': 'gamma exploration'},
    'pain': {'freq': 12, 'basis': 'beta discomfort response'},
    'loneliness': {'freq': 14, 'basis': 'social isolation stress'},
    'sadness': {'freq': 8, 'basis': 'theta low mood state'},
    'anger': {'freq': 18, 'basis': 'high beta agitation'},
    'fear': {'freq': 16, 'basis': 'beta threat response'},
    'joy': {'freq': 11, 'basis': 'alpha positive affect'},
    'amusement': {'freq': 12, 'basis': 'alpha humor response'},
    'excitement': {'freq': 20, 'basis': 'high beta activation'},
    'happiness': {'freq': 10, 'basis': 'alpha contentment'},
    'grief': {'freq': 6, 'basis': 'theta deep sorrow'},
    'frustration': {'freq': 17, 'basis': 'beta blocked goals'},
    'confusion': {'freq': 14, 'basis': 'beta cognitive dissonance'},
    'boredom': {'freq': 9, 'basis': 'alpha-theta understimulation'},
    'exhaustion': {'freq': 5, 'basis': 'delta-theta depletion'},
    'surprise': {'freq': 22, 'basis': 'high beta orienting response'},
    'pride': {'freq': 11, 'basis': 'alpha achievement state'},
    'gratitude': {'freq': 10, 'basis': 'alpha appreciation'},
    'relief': {'freq': 9, 'basis': 'alpha stress resolution'},
    'disappointment': {'freq': 8, 'basis': 'theta unmet expectations'},
    'overwhelm': {'freq': 19, 'basis': 'high beta cognitive overload'},
    'hope': {'freq': 11, 'basis': 'alpha positive anticipation'},
    'determination': {'freq': 21, 'basis': 'high beta goal pursuit'},
    'confidence': {'freq': 12, 'basis': 'beta self-efficacy'}
}

METAPHYSICAL_CATALOG = {
    'love': {'freq': 528, 'basis': 'Solfeggio frequency'},
    'transcendence': {'freq': 963, 'basis': 'crown chakra'},
    'grounding': {'freq': 396, 'basis': 'root chakra'},
    'harmony': {'freq': 432, 'basis': 'universal tuning'},
    'awakening': {'freq': 852, 'basis': 'third eye activation'},
    'curiosity': {'freq': 741, 'basis': 'expression and seeking'}
}

EMOTION_KEYWORDS = {
    'anxiety': ['anxious', 'anxiety', 'worried', 'worry', 'nervous', 'uneasy', 'freaking', 'panicking'],
    'calm': ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil'],
    'focus': ['focus', 'concentrate', 'attention', 'sharp', 'clear'],
    'stress': ['stress', 'stressed', 'pressure', 'tense', 'heavy', 'weight', 'burden'],
    'meditation': ['meditate', 'meditation', 'mindful', 'present'],
    'pain': ['pain', 'hurt', 'hurting', 'ache', 'aching', 'sore', 'painful'],
    'loneliness': ['lonely', 'loneliness', 'alone', 'isolated', 'isolation'],
    'sadness': ['sad', 'sadness', 'down', 'depressed', 'depression', 'unhappy', 'miserable'],
    'anger': ['angry', 'anger', 'mad', 'furious', 'rage', 'irritated', 'annoyed'],
    'fear': ['fear', 'afraid', 'scared', 'frightened', 'terrified', 'panic', 'freaked'],
    'joy': ['joy', 'joyful', 'cheerful', 'delighted', 'wonderful', 'amazing'],
    'amusement': ['funny', 'hilarious', 'haha', 'lol', 'lmao', 'laughing', 'laugh', 'cracking up', '😂', 'rofl', 'humor', 'humorous', 'joke', 'joking'],
    'excitement': ['excited', 'exciting', 'pumped', 'hyped', 'thrilled', 'stoked', 'psyched', 'can\'t wait', 'awesome', 'incredible', 'fantastic', 'great', 'superb', 'excellent', 'brilliant'],
    'happiness': ['happy', 'happiness', 'glad', 'pleased', 'content', 'satisfied', 'good mood'],
    'grief': ['grief', 'grieving', 'loss', 'mourning', 'heartbroken'],
    'frustration': ['frustrated', 'frustration', 'stuck', 'annoying', 'irritating'],
    'confusion': ['confused', 'confusing', 'don\'t understand', 'lost', 'unclear', 'what does this mean', 'huh', 'puzzled'],
    'boredom': ['bored', 'boring', 'nothing to do', 'dull', 'uninteresting', 'monotonous'],
    'exhaustion': ['exhausted', 'tired', 'drained', 'worn out', 'fatigued', 'sleepy', 'burned out', 'no energy'],
    'surprise': ['wow', 'omg', 'no way', 'surprised', 'shocking', 'unexpected', 'can\'t believe', 'whoa', 'amazed'],
    'pride': ['proud', 'accomplished', 'achieved', 'succeeded', 'nailed it', 'crushed it', 'did it', 'victory'],
    'gratitude': ['thank', 'thanks', 'grateful', 'appreciate', 'appreciation', 'thankful', 'blessed'],
    'relief': ['relief', 'relieved', 'finally', 'phew', 'glad that\'s over', 'weight off'],
    'disappointment': ['disappointed', 'disappointing', 'let down', 'expected more', 'underwhelming', 'unsatisfied'],
    'overwhelm': ['overwhelmed', 'too much', 'can\'t handle', 'drowning', 'swamped', 'overloaded', 'buried'],
    'hope': ['hopeful', 'hope', 'optimistic', 'looking forward', 'fingers crossed', 'maybe', 'wishing'],
    'determination': ['determined', 'motivated', 'driven', 'committed', 'going to', 'will do', 'focused on goal'],
    'confidence': ['confident', 'i got this', 'capable', 'sure', 'believe in myself', 'can do this'],
    'love': ['love', 'loving', 'compassion', 'heart', 'affection'],
    'transcendence': ['transcend', 'transcendence', 'enlighten', 'cosmic'],
    'grounding': ['ground', 'grounding', 'rooted', 'stable', 'earth'],
    'harmony': ['harmony', 'harmonious', 'balance', 'aligned'],
    'awakening': ['awaken', 'awakening', 'aware', 'consciousness'],
    'curiosity': ['how', 'why', 'what', 'tell', 'explain', 'teach', 'curious']
}

def detect_catalog_context(text: str) -> str:
    text_lower = text.lower()
    spiritual_words = ['vibration', 'energy', 'chakra', 'consciousness', 'awakening', 
                      'ascension', 'frequency', 'aura', 'enlighten', 'transcend', 'spiritual', 'soul']
    clinical_words = ['anxious', 'depressed', 'stressed', 'worried', 'panic', 
                     'calm', 'focus', 'concentration', 'nervous']
    
    spiritual_count = sum(1 for word in spiritual_words if word in text_lower)
    clinical_count = sum(1 for word in clinical_words if word in text_lower)
    
    return 'metaphysical' if spiritual_count > clinical_count else 'neuroscience'

def get_frequency(text: str) -> dict:
    text_lower = text.lower()
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                in_neuro = emotion in NEUROSCIENCE_CATALOG
                in_meta = emotion in METAPHYSICAL_CATALOG
                
                if in_neuro and in_meta:
                    catalog_type = detect_catalog_context(text)
                    if catalog_type == 'metaphysical':
                        return {
                            'emotion': emotion,
                            'frequency': METAPHYSICAL_CATALOG[emotion]['freq'],
                            'basis': METAPHYSICAL_CATALOG[emotion]['basis'],
                            'catalog': 'metaphysical'
                        }
                    else:
                        return {
                            'emotion': emotion,
                            'frequency': NEUROSCIENCE_CATALOG[emotion]['freq'],
                            'basis': NEUROSCIENCE_CATALOG[emotion]['basis'],
                            'catalog': 'neuroscience'
                        }
                elif in_neuro:
                    return {
                        'emotion': emotion,
                        'frequency': NEUROSCIENCE_CATALOG[emotion]['freq'],
                        'basis': NEUROSCIENCE_CATALOG[emotion]['basis'],
                        'catalog': 'neuroscience'
                    }
                elif in_meta:
                    return {
                        'emotion': emotion,
                        'frequency': METAPHYSICAL_CATALOG[emotion]['freq'],
                        'basis': METAPHYSICAL_CATALOG[emotion]['basis'],
                        'catalog': 'metaphysical'
                    }
    
    catalog_type = detect_catalog_context(text)
    return {
        'emotion': 'neutral',
        'frequency': 240,
        'basis': 'baseline state',
        'catalog': catalog_type
    }
