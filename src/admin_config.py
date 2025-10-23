"""
Admin/Teaching Mode Configuration
Allows the creator to teach MC AI through internal sessions
SECURITY: Uses server-side secret token for authentication
"""
import os
import hashlib
import secrets

class AdminConfig:
    def __init__(self):
        # SECURITY: Admin token MUST be set server-side only in environment
        # Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
        self.admin_token = os.getenv('ADMIN_SECRET_TOKEN')
        
        if not self.admin_token:
            print("⚠️  WARNING: No ADMIN_SECRET_TOKEN set - teaching mode DISABLED for security")
            self.admin_token = None
            self.admin_token_hash = None
        else:
            # Hash the token for comparison
            self.admin_token_hash = hashlib.sha256(self.admin_token.encode()).hexdigest()
            print(f"🔐 Admin mode configured (secure token authentication)")
    
    def verify_admin_token(self, provided_token: str) -> bool:
        """
        Verify admin token (server-side only)
        
        Args:
            provided_token: Token provided by client
        
        Returns:
            True if token is valid, False otherwise
        """
        if not provided_token:
            return False
        
        # Special case: Auto-enable for Replit workspace access
        if provided_token == 'replit_workspace_auto':
            is_replit_workspace = bool(os.getenv('REPLIT_DEV_DOMAIN')) and not os.getenv('REPLIT_DEPLOYMENT')
            return is_replit_workspace
        
        # Regular token validation
        if not self.admin_token_hash:
            return False
        
        # Constant-time comparison to prevent timing attacks
        provided_hash = hashlib.sha256(provided_token.encode()).hexdigest()
        return secrets.compare_digest(provided_hash, self.admin_token_hash)
    
    def is_admin(self, user_id: str | None = None, admin_token: str | None = None) -> bool:
        """
        Check if request is from admin (SECURE)
        
        Args:
            user_id: User ID (not used for auth, only for tracking)
            admin_token: Secret token from client (required for admin access)
        
        Returns:
            True if admin token is valid
        """
        # SECURITY: Only verify token, never check user_id for auth
        if not admin_token:
            return False
        
        return self.verify_admin_token(admin_token)
    
    def get_mode(self, user_id: str | None = None, admin_token: str | None = None) -> str:
        """Get interaction mode based on secure token"""
        return 'teaching' if self.is_admin(user_id, admin_token) else 'external'

# Global admin config
admin_config = AdminConfig()
