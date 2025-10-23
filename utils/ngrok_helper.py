"""
Ngrok Helper for MC AI
Helps expose local services and connect to remote AI services
"""
import os
from pyngrok import ngrok, conf
import requests

def setup_ngrok():
    """Configure ngrok with authtoken from environment"""
    token = os.environ.get('Ngrok')
    if token:
        conf.get_default().auth_token = token
        print("✅ Ngrok authenticated successfully!")
        return True
    else:
        print("❌ Ngrok token not found in environment")
        return False

def expose_service(port=5000, name="MC AI"):
    """Expose a local service via ngrok"""
    if not setup_ngrok():
        return None
    
    try:
        public_url = ngrok.connect(str(port))
        print(f"🌐 {name} is now publicly accessible at: {public_url}")
        return public_url
    except Exception as e:
        print(f"Error creating tunnel: {e}")
        return None

def get_active_tunnels():
    """Get all active ngrok tunnels"""
    tunnels = ngrok.get_tunnels()
    return [{"name": t.name, "url": t.public_url, "port": t.config['addr']} for t in tunnels]

def close_all_tunnels():
    """Close all ngrok tunnels"""
    ngrok.kill()
    print("🔒 All ngrok tunnels closed")

# Example usage for Kaggle/Colab services
def register_external_service(service_type, service_url):
    """Register an external AI service (from Kaggle/Colab)"""
    services = {
        'art': service_url,
        'music': service_url,
        'video': service_url
    }
    
    print(f"✅ Registered {service_type} service at: {service_url}")
    return services.get(service_type)

if __name__ == "__main__":
    # Test ngrok setup
    setup_ngrok()
    print("\n📋 Available functions:")
    print("- expose_service(port) - Make MC AI publicly accessible")
    print("- get_active_tunnels() - List active tunnels")
    print("- close_all_tunnels() - Shutdown all tunnels")
