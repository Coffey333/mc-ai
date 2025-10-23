"""
External Services Configuration for MC AI
Manage connections to self-hosted AI services (Kaggle/Colab)
"""
import os

class ExternalServicesConfig:
    """Configuration for external AI services"""
    
    def __init__(self):
        # Self-hosted service URLs (from Kaggle/Colab via ngrok)
        self.CUSTOM_ART_SERVICE = os.environ.get('CUSTOM_ART_SERVICE_URL', None)
        self.CUSTOM_MUSIC_SERVICE = os.environ.get('CUSTOM_MUSIC_SERVICE_URL', None)
        self.CUSTOM_VIDEO_SERVICE = os.environ.get('CUSTOM_VIDEO_SERVICE_URL', None)
        
        # Fallback to external APIs if custom services not available
        self.USE_EXTERNAL_APIS = True
    
    def has_custom_art_service(self):
        """Check if custom art service is configured"""
        return self.CUSTOM_ART_SERVICE is not None
    
    def has_custom_music_service(self):
        """Check if custom music service is configured"""
        return self.CUSTOM_MUSIC_SERVICE is not None
    
    def has_custom_video_service(self):
        """Check if custom video service is configured"""
        return self.CUSTOM_VIDEO_SERVICE is not None
    
    def get_art_service_url(self):
        """Get art generation service URL"""
        if self.has_custom_art_service():
            return self.CUSTOM_ART_SERVICE
        return None
    
    def get_music_service_url(self):
        """Get music generation service URL"""
        if self.has_custom_music_service():
            return self.CUSTOM_MUSIC_SERVICE
        return None
    
    def get_video_service_url(self):
        """Get video generation service URL"""
        if self.has_custom_video_service():
            return self.CUSTOM_VIDEO_SERVICE
        return None
    
    def status(self):
        """Get status of all services"""
        return {
            'custom_art': self.has_custom_art_service(),
            'custom_music': self.has_custom_music_service(),
            'custom_video': self.has_custom_video_service(),
            'art_url': self.CUSTOM_ART_SERVICE,
            'music_url': self.CUSTOM_MUSIC_SERVICE,
            'video_url': self.CUSTOM_VIDEO_SERVICE
        }

# Global config instance
config = ExternalServicesConfig()
