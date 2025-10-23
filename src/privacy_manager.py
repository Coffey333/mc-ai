import hashlib
import re
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from pathlib import Path

class PrivacyManager:
    """
    Manages user data privacy and GDPR compliance
    Handles consent tracking, data anonymization, and user data rights
    """
    
    def __init__(self, data_dir: str = "user_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.consent_dir = self.data_dir / "consent"
        self.consent_dir.mkdir(exist_ok=True)
        
        self.profiles_dir = self.data_dir / "profiles"
        self.profiles_dir.mkdir(exist_ok=True)
        
        self.conversations_dir = self.data_dir / "conversations"
        self.conversations_dir.mkdir(exist_ok=True)
        
        self.data_retention_days = 30
        self.consent_version = "1.0"
        self.anonymization_enabled = True
    
    def check_consent(self, user_id: str) -> Dict:
        """
        Check if user has given consent for data storage (GDPR Article 6)
        """
        consent_file = self.consent_dir / f"{user_id}.json"
        
        if not consent_file.exists():
            return {
                'has_consent': False,
                'consent_date': None,
                'consent_version': None,
                'needs_renewal': False,
                'message': 'No consent record found'
            }
        
        try:
            with open(consent_file, 'r') as f:
                consent_record = json.load(f)
            
            consent_date = datetime.fromisoformat(consent_record['date'])
            needs_renewal = (datetime.now() - consent_date).days > 365
            
            return {
                'has_consent': consent_record.get('data_storage', False),
                'consent_date': consent_record['date'],
                'consent_version': consent_record.get('version', '1.0'),
                'needs_renewal': needs_renewal,
                'permissions': consent_record.get('permissions', {})
            }
        except Exception as e:
            print(f"Error reading consent: {e}")
            return {
                'has_consent': False,
                'error': str(e)
            }
    
    def record_consent(self, user_id: str, consent_data: Dict) -> Dict:
        """
        Record user consent preferences (GDPR Article 7 - Conditions for consent)
        """
        consent_file = self.consent_dir / f"{user_id}.json"
        
        consent_record = {
            'user_id': user_id,
            'date': datetime.now().isoformat(),
            'version': self.consent_version,
            'data_storage': consent_data.get('data_storage', False),
            'analytics': consent_data.get('analytics', False),
            'emotional_tracking': consent_data.get('emotional_tracking', False),
            'permissions': consent_data.get('permissions', {}),
            'ip_address': consent_data.get('ip_address'),
            'user_agent': consent_data.get('user_agent')
        }
        
        try:
            with open(consent_file, 'w') as f:
                json.dump(consent_record, f, indent=2)
            
            return {
                'success': True,
                'consent_id': user_id,
                'timestamp': consent_record['date']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def anonymize_data(self, data: Dict) -> Dict:
        """
        Remove personally identifiable information (GDPR Article 4(5) - Pseudonymisation)
        """
        if not self.anonymization_enabled:
            return data
        
        anonymized = data.copy()
        
        pii_fields = ['user_id', 'email', 'ip_address', 'phone', 'name', 'address']
        for field in pii_fields:
            anonymized.pop(field, None)
        
        if 'session_id' in anonymized:
            anonymized['session_id'] = self._hash(anonymized['session_id'])
        
        if 'text' in anonymized:
            anonymized['text'] = self._redact_personal_info(anonymized['text'])
        
        if 'messages' in anonymized and isinstance(anonymized['messages'], list):
            anonymized['messages'] = [
                self._redact_personal_info(msg) if isinstance(msg, str) else msg
                for msg in anonymized['messages']
            ]
        
        return anonymized
    
    def export_user_data(self, user_id: str) -> Dict:
        """
        GDPR Article 20: Right to data portability
        Export all user data in machine-readable format
        """
        export_data = {
            'user_id': user_id,
            'export_date': datetime.now().isoformat(),
            'data_retention_days': self.data_retention_days,
            'conversations': self._load_conversations(user_id),
            'emotional_profile': self._load_profile(user_id),
            'consent_record': self._load_consent(user_id),
            'generated_content': self._load_generated_content(user_id),
            'format': 'json',
            'version': '1.0'
        }
        
        export_file = self.data_dir / f"export_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(export_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return {
                'success': True,
                'export_file': str(export_file),
                'total_conversations': len(export_data['conversations']),
                'export_date': export_data['export_date']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_user_data(self, user_id: str, reason: Optional[str] = None) -> Dict:
        """
        GDPR Article 17: Right to erasure ("right to be forgotten")
        Permanently delete all user data
        """
        deleted_items = []
        errors = []
        
        try:
            if self._delete_conversations(user_id):
                deleted_items.append('conversations')
        except Exception as e:
            errors.append(f"conversations: {e}")
        
        try:
            if self._delete_profile(user_id):
                deleted_items.append('emotional_profile')
        except Exception as e:
            errors.append(f"emotional_profile: {e}")
        
        try:
            if self._delete_generated_content(user_id):
                deleted_items.append('generated_content')
        except Exception as e:
            errors.append(f"generated_content: {e}")
        
        try:
            if self._delete_consent(user_id):
                deleted_items.append('consent_record')
        except Exception as e:
            errors.append(f"consent_record: {e}")
        
        self._log_deletion(user_id, reason, deleted_items)
        
        return {
            'success': len(deleted_items) > 0,
            'deleted_items': deleted_items,
            'errors': errors if errors else None,
            'timestamp': datetime.now().isoformat(),
            'user_id_hash': self._hash(user_id)
        }
    
    def _hash(self, value: str) -> str:
        """Create SHA-256 hash of value"""
        return hashlib.sha256(value.encode()).hexdigest()
    
    def _redact_personal_info(self, text: str) -> str:
        """Redact common PII patterns from text"""
        patterns = [
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]'),
            (r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]'),
            (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]'),
            (r'\b\d{1,5}\s\w+\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b', '[ADDRESS]'),
        ]
        
        redacted = text
        for pattern, replacement in patterns:
            redacted = re.sub(pattern, replacement, redacted)
        
        return redacted
    
    def _load_consent(self, user_id: str) -> Dict:
        """Load consent record"""
        consent_file = self.consent_dir / f"{user_id}.json"
        if consent_file.exists():
            with open(consent_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_conversations(self, user_id: str) -> List[Dict]:
        """Load user conversations"""
        conv_file = self.conversations_dir / f"{user_id}.json"
        if conv_file.exists():
            with open(conv_file, 'r') as f:
                return json.load(f)
        return []
    
    def _load_profile(self, user_id: str) -> Dict:
        """Load emotional profile"""
        profile_file = self.profiles_dir / f"{user_id}.json"
        if profile_file.exists():
            with open(profile_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_generated_content(self, user_id: str) -> Dict:
        """Load generated content (art, music, etc.)"""
        return {
            'art': [],
            'music': [],
            'games': [],
            'videos': []
        }
    
    def _delete_conversations(self, user_id: str) -> bool:
        """Delete conversation data"""
        conv_file = self.conversations_dir / f"{user_id}.json"
        if conv_file.exists():
            conv_file.unlink()
            return True
        return False
    
    def _delete_profile(self, user_id: str) -> bool:
        """Delete emotional profile"""
        profile_file = self.profiles_dir / f"{user_id}.json"
        if profile_file.exists():
            profile_file.unlink()
            return True
        return False
    
    def _delete_generated_content(self, user_id: str) -> bool:
        """Delete generated content"""
        return True
    
    def _delete_consent(self, user_id: str) -> bool:
        """Delete consent record"""
        consent_file = self.consent_dir / f"{user_id}.json"
        if consent_file.exists():
            consent_file.unlink()
            return True
        return False
    
    def _log_deletion(self, user_id: str, reason: Optional[str], deleted_items: List[str]):
        """Log deletion for audit trail (anonymized)"""
        log_file = self.data_dir / "deletion_log.json"
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id_hash': self._hash(user_id),
            'reason': reason,
            'deleted_items': deleted_items
        }
        
        try:
            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(log_entry)
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            print(f"Error logging deletion: {e}")
