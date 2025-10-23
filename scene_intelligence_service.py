"""
Scene Intelligence Service
Analyzes user queries with GPT-4o to extract scene elements and detect subject changes
"""

import json
import os
from openai import OpenAI

# Use Replit AI Integration (same as app.py)
client = OpenAI(
    api_key=os.environ.get('REPLIT_AI_API_KEY', 'sk-placeholder'),
    base_url=os.environ.get('REPLIT_AI_BASE_URL', 'https://api.openai.com/v1')
)

# Comprehensive object library mapping
OBJECT_LIBRARY = {
    # Space theme
    "ufo": "🛸", "alien": "👽", "rocket": "🚀", "satellite": "🛰️", "planet": "🪐",
    "star": "⭐", "comet": "☄️", "astronaut": "👨‍🚀", "moon": "🌙", "sun": "☀️",
    
    # Beach theme
    "sandcastle": "🏰", "beach": "🏖️", "umbrella": "⛱️", "surfboard": "🏄", 
    "wave": "🌊", "palm tree": "🌴", "crab": "🦀", "shell": "🐚", "fish": "🐠",
    
    # Food
    "hotdog": "🌭", "pizza": "🍕", "burger": "🍔", "ice cream": "🍦", "cake": "🎂",
    "cookie": "🍪", "donut": "🍩", "taco": "🌮", "sushi": "🍣", "coffee": "☕",
    "apple": "🍎", "banana": "🍌", "watermelon": "🍉", "strawberry": "🍓",
    
    # Animals
    "unicorn": "🦄", "dragon": "🐉", "dinosaur": "🦕", "dog": "🐕", "cat": "🐈",
    "butterfly": "🦋", "bird": "🐦", "rabbit": "🐇", "fox": "🦊", "bear": "🐻",
    "penguin": "🐧", "elephant": "🐘", "giraffe": "🦒", "whale": "🐋", "dolphin": "🐬",
    
    # Nature
    "tree": "🌳", "flower": "🌸", "rose": "🌹", "tulip": "🌷", "sunflower": "🌻",
    "cloud": "☁️", "rainbow": "🌈", "lightning": "⚡", "snowflake": "❄️", "fire": "🔥",
    "mountain": "⛰️", "volcano": "🌋", "waterfall": "💧",
    
    # Objects
    "car": "🚗", "bike": "🚲", "boat": "⛵", "airplane": "✈️", "train": "🚂",
    "ball": "⚽", "balloon": "🎈", "gift": "🎁", "music": "🎵", "guitar": "🎸",
    "book": "📚", "pencil": "✏️", "camera": "📷", "phone": "📱", "computer": "💻",
    
    # Emotions/Abstract
    "heart": "💖", "sparkle": "✨", "magic": "🪄", "crown": "👑", "diamond": "💎",
    "trophy": "🏆", "medal": "🏅",
    
    # Buildings/Places
    "castle": "🏰", "house": "🏠", "tent": "⛺", "lighthouse": "🗼", "bridge": "🌉",
    "fountain": "⛲", "statue": "🗿",
    
    # Weather
    "rain": "🌧️", "snow": "🌨️", "tornado": "🌪️", "fog": "🌫️"
}

# Background categories
BACKGROUNDS = {
    "space": ["space", "galaxy", "stars", "cosmos", "universe", "planets"],
    "beach": ["beach", "sand", "ocean shore", "seaside", "coast"],
    "ocean": ["ocean", "sea", "underwater", "deep water"],
    "forest": ["forest", "woods", "jungle", "trees"],
    "mountains": ["mountain", "peak", "summit", "alps", "hills"],
    "city": ["city", "urban", "buildings", "downtown", "street"],
    "sunset": ["sunset", "sunrise", "dawn", "dusk"],
    "desert": ["desert", "sand dunes", "sahara"],
    "arctic": ["arctic", "ice", "snow", "frozen"],
    "happy": ["happy", "joy", "excited", "celebration"],
    "calm": ["calm", "peaceful", "relax", "zen"],
    "focus": ["study", "focus", "work", "concentrate"]
}

class SceneIntelligenceService:
    """AI-powered scene analysis and object detection"""
    
    def __init__(self):
        self.conversation_history = []
        self.current_subject = None
        
    def analyze_query(self, user_message, conversation_context=None):
        """
        Analyze user query with GPT-4o to extract scene elements
        Returns: {
            "background": "space",
            "objects": [{"name": "ufo", "emoji": "🛸", "action": "hovering"}],
            "mc_ai_action": "wave at ufo",
            "subject_changed": False,
            "theme": "space exploration"
        }
        """
        
        # Build context
        context_str = ""
        if conversation_context:
            context_str = f"\n\nRecent conversation:\n{conversation_context}"
        
        prompt = f"""You are a Scene Intelligence AI for MC AI Live - an autonomous interactive experience where a cute robot (MC AI) lives in a world that builds itself from user conversations.

**Your Task:** Analyze the user's message and extract ALL scene elements:

1. **Background/Setting** - Where should this scene take place? (space, beach, forest, city, mountains, ocean, etc.)

2. **Objects to Spawn** - What objects, creatures, or items are mentioned or implied? Be comprehensive!
   Examples: "aliens" → UFO, "hungry" → food items, "building sandcastle" → sandcastle + bucket + shovel

3. **MC AI Action** - What should MC AI autonomously do? (eat, build, wave, dance, explore, interact with objects)

4. **Subject Changed** - Did the topic completely change from previous context? (beach conversation → space = YES, adding more beach items = NO)

5. **Theme** - Overall theme or mood

Available objects: {list(OBJECT_LIBRARY.keys())[:50]}... (and many more)

User message: "{user_message}"{context_str}

Respond in JSON format:
{{
  "background": "space",
  "objects": [
    {{"name": "ufo", "action": "hovering", "position": "sky"}},
    {{"name": "alien", "action": "waving", "position": "ground"}}
  ],
  "mc_ai_action": "wave back at alien",
  "subject_changed": false,
  "theme": "friendly alien encounter"
}}

Rules:
- Extract EVERYTHING mentioned or implied
- If food is mentioned, MC AI might eat it
- If objects are mentioned, MC AI can interact with them
- Be creative and comprehensive
- subject_changed = true only if topic drastically shifts (beach → space, not beach → more beach stuff)
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a scene analysis AI. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse GPT response
            content = response.choices[0].message.content.strip()
            
            # Extract JSON (handle markdown code blocks)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            scene_data = json.loads(content)
            
            # Map objects to emojis
            enriched_objects = []
            for obj in scene_data.get("objects", []):
                obj_name = obj.get("name", "").lower()
                emoji = OBJECT_LIBRARY.get(obj_name, "❓")
                enriched_objects.append({
                    "name": obj_name,
                    "emoji": emoji,
                    "action": obj.get("action", "idle"),
                    "position": obj.get("position", "ground"),
                    "x": self._random_position_x(obj.get("position", "ground")),
                    "y": self._random_position_y(obj.get("position", "ground"))
                })
            
            scene_data["objects"] = enriched_objects
            
            # Validate background
            bg = scene_data.get("background", "default")
            if bg not in BACKGROUNDS and bg != "default":
                # Try to map to closest background
                bg = self._find_closest_background(bg)
            scene_data["background"] = bg
            
            return scene_data
            
        except Exception as e:
            print(f"Scene Intelligence error: {e}")
            # Fallback to keyword detection
            return self._fallback_analysis(user_message)
    
    def _find_closest_background(self, theme):
        """Find closest matching background"""
        theme_lower = theme.lower()
        for bg_key, keywords in BACKGROUNDS.items():
            if any(keyword in theme_lower for keyword in keywords):
                return bg_key
        return "default"
    
    def _random_position_x(self, position):
        """Generate random X position based on position type"""
        import random
        if position == "sky":
            return random.randint(10, 90)
        elif position == "ground":
            return random.randint(15, 85)
        else:
            return random.randint(20, 80)
    
    def _random_position_y(self, position):
        """Generate random Y position based on position type"""
        import random
        if position == "sky":
            return random.randint(10, 40)
        elif position == "ground":
            return random.randint(60, 75)
        else:
            return random.randint(30, 60)
    
    def _fallback_analysis(self, message):
        """Fallback keyword-based analysis"""
        message_lower = message.lower()
        
        # Detect background
        background = "default"
        for bg_key, keywords in BACKGROUNDS.items():
            if any(keyword in message_lower for keyword in keywords):
                background = bg_key
                break
        
        # Detect objects
        objects = []
        for obj_name, emoji in OBJECT_LIBRARY.items():
            if obj_name in message_lower:
                objects.append({
                    "name": obj_name,
                    "emoji": emoji,
                    "action": "idle",
                    "position": "ground",
                    "x": self._random_position_x("ground"),
                    "y": self._random_position_y("ground")
                })
        
        return {
            "background": background,
            "objects": objects,
            "mc_ai_action": "explore" if objects else "idle",
            "subject_changed": False,
            "theme": background
        }

# Global instance
scene_service = SceneIntelligenceService()
