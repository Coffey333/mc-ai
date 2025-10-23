"""
User Profile Management
Stores and retrieves user preferences, including neurodivergent status
"""

import json
import os
from datetime import datetime

class UserProfileManager:
    """Manages user profiles and communication preferences"""
    
    def __init__(self):
        self.profiles_dir = 'user_data/profiles'
        os.makedirs(self.profiles_dir, exist_ok=True)
    
    def get_profile_path(self, user_id):
        """Get file path for user profile"""
        if not user_id:
            raise ValueError("user_id cannot be None or empty")
        safe_user_id = str(user_id).replace('/', '_').replace('\\', '_')
        return os.path.join(self.profiles_dir, f'{safe_user_id}_profile.json')
    
    def load_profile(self, user_id):
        """Load user profile from file"""
        profile_path = self.get_profile_path(user_id)
        
        if os.path.exists(profile_path):
            try:
                with open(profile_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading profile for {user_id}: {e}")
                return self._create_default_profile(user_id)
        else:
            return self._create_default_profile(user_id)
    
    def save_profile(self, user_id, profile_data):
        """Save user profile to file"""
        profile_path = self.get_profile_path(user_id)
        
        try:
            with open(profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving profile for {user_id}: {e}")
            return False
    
    def _create_default_profile(self, user_id):
        """Create default user profile"""
        return {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'neurodivergent': False,
            'communication_preferences': {
                'literal_language': False,
                'simple_structure': False,
                'direct_answers': False,
                'concrete_examples': False,
                'visual_formatting': False
            },
            'safety_protocol': 'standard',
            'notes': '',
            'conversation_count': 0,
            'last_interaction': datetime.now().isoformat()
        }
    
    def mark_as_neurodivergent(self, user_id, facilitator_name=None):
        """Mark user as neurodivergent and activate safety protocol"""
        profile = self.load_profile(user_id)
        
        profile['neurodivergent'] = True
        profile['safety_protocol'] = 'neurodivergent_active'
        profile['communication_preferences'] = {
            'literal_language': True,
            'simple_structure': True,
            'direct_answers': True,
            'concrete_examples': True,
            'visual_formatting': True
        }
        
        if facilitator_name:
            profile['facilitator'] = facilitator_name
            profile['notes'] = f'Neurodivergent client facilitated by {facilitator_name}. Requires clear, direct, literal communication.'
        else:
            profile['notes'] = 'Neurodivergent user. Requires clear, direct, literal communication.'
        
        profile['protocol_activated_at'] = datetime.now().isoformat()
        
        self.save_profile(user_id, profile)
        return profile
    
    def is_neurodivergent(self, user_id):
        """Check if user is marked as neurodivergent"""
        profile = self.load_profile(user_id)
        return profile.get('neurodivergent', False)
    
    def update_interaction(self, user_id):
        """Update last interaction timestamp"""
        profile = self.load_profile(user_id)
        profile['last_interaction'] = datetime.now().isoformat()
        profile['conversation_count'] = profile.get('conversation_count', 0) + 1
        self.save_profile(user_id, profile)
    
    def get_communication_preferences(self, user_id):
        """Get user's communication preferences"""
        profile = self.load_profile(user_id)
        return profile.get('communication_preferences', {})
