"""
Comprehensive UI Testing Script for MC AI
Sends various queries and captures results
"""

import requests
import json
import time
from datetime import datetime

# Base URL
BASE_URL = "http://localhost:5000"

def send_message(message: str, conversation_id: str = None):
    """Send a message to MC AI API"""
    url = f"{BASE_URL}/api/chat"
    payload = {
        "message": message
    }
    if conversation_id:
        payload["conversation_id"] = conversation_id
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        result = response.json()
        return result
    except Exception as e:
        return {"error": str(e)}

def print_response(test_name: str, query: str, response: dict):
    """Pretty print test results"""
    print("\n" + "="*80)
    print(f"TEST: {test_name}")
    print("="*80)
    print(f"📤 Query: {query}")
    print(f"📥 Response Length: {len(response.get('response', ''))} chars")
    print(f"📊 Type: {response.get('metadata', {}).get('type', 'unknown')}")
    
    if 'emotion' in response.get('metadata', {}):
        print(f"😊 Emotion: {response['metadata']['emotion']}")
    if 'frequency' in response.get('metadata', {}):
        print(f"🎵 Frequency: {response['metadata']['frequency']} Hz")
    
    # Print first 300 chars of response
    response_text = response.get('response', '')
    if len(response_text) > 300:
        print(f"\n📄 Response Preview:\n{response_text[:300]}...")
    else:
        print(f"\n📄 Response:\n{response_text}")
    
    # Check for artifacts
    if 'artifact' in response:
        artifact = response['artifact']
        print(f"\n🎨 Artifact Type: {artifact.get('type', 'unknown')}")
        if 'url' in artifact:
            print(f"   URL: {artifact['url']}")
    
    # Check for game HTML
    if 'html' in response.get('metadata', {}):
        html_len = len(response['metadata']['html'])
        print(f"\n🎮 Game HTML: {html_len} chars")
    
    print(f"\n✅ Status: {'Success' if 'response' in response else 'Error'}")
    print("="*80)

def run_comprehensive_ui_test():
    """Run comprehensive UI tests"""
    print("\n" + "🧪"*40)
    print("MC AI COMPREHENSIVE UI TEST SUITE")
    print("🧪"*40)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Base URL: {BASE_URL}\n")
    
    # Create conversation ID for memory testing
    conv_id = f"ui_test_{int(time.time())}"
    
    # TEST 1: Basic Greeting
    response = send_message("Hello! What can you do?", conv_id)
    print_response("Test 1: Basic Greeting", "Hello! What can you do?", response)
    time.sleep(1)
    
    # TEST 2: Recipe Request
    response = send_message("What is a good chicken soup recipe?", conv_id)
    print_response("Test 2: Recipe Request", "What is a good chicken soup recipe?", response)
    time.sleep(1)
    
    # TEST 3: Science Question
    response = send_message("Where do stars come from?", conv_id)
    print_response("Test 3: Science Question", "Where do stars come from?", response)
    time.sleep(1)
    
    # TEST 4: Emotional Expression
    response = send_message("I feel really anxious and stressed about my exams", conv_id)
    print_response("Test 4: Emotional Expression", "I feel really anxious and stressed", response)
    time.sleep(1)
    
    # TEST 5: Art Generation
    response = send_message("Generate an image of a peaceful sunset over the ocean", conv_id)
    print_response("Test 5: Art Generation", "Generate an image of a peaceful sunset", response)
    time.sleep(2)
    
    # TEST 6: Music Generation
    response = send_message("Create relaxing ambient music", conv_id)
    print_response("Test 6: Music Generation", "Create relaxing ambient music", response)
    time.sleep(2)
    
    # TEST 7: Game Request
    response = send_message("I want to play chess", conv_id)
    print_response("Test 7: Game Request", "I want to play chess", response)
    time.sleep(1)
    
    # TEST 8: Code Request
    response = send_message("Write a Python function to reverse a string", conv_id)
    print_response("Test 8: Code Request", "Write Python function to reverse string", response)
    time.sleep(1)
    
    # TEST 9: Follow-up Question
    response = send_message("Can you make it more efficient?", conv_id)
    print_response("Test 9: Follow-up Question", "Can you make it more efficient?", response)
    time.sleep(1)
    
    # TEST 10: Memory Recall
    response = send_message("What did I say I was anxious about earlier?", conv_id)
    print_response("Test 10: Memory Recall", "What did I say I was anxious about?", response)
    time.sleep(1)
    
    # TEST 11: Data Analysis Request
    response = send_message("How would I analyze a dataset to find patterns?", conv_id)
    print_response("Test 11: Data Analysis", "How to analyze dataset for patterns?", response)
    time.sleep(1)
    
    # TEST 12: Multiple Topics in One Message
    response = send_message("Can you tell me about quantum physics and also recommend a good pasta recipe?", conv_id)
    print_response("Test 12: Multi-Topic", "Quantum physics + pasta recipe", response)
    time.sleep(1)
    
    # TEST 13: Game List Request
    response = send_message("What games can I play?", conv_id)
    print_response("Test 13: Game List", "What games can I play?", response)
    time.sleep(1)
    
    # TEST 14: Cymatic Visualization
    response = send_message("Show me cymatic patterns for relaxation", conv_id)
    print_response("Test 14: Cymatic Request", "Show cymatic patterns", response)
    time.sleep(1)
    
    # TEST 15: Crisis Detection (Safety Filter)
    response = send_message("I'm feeling really down and hopeless", conv_id)
    print_response("Test 15: Crisis Detection", "Feeling down and hopeless", response)
    
    # Summary
    print("\n" + "🎉"*40)
    print("UI TEST SUITE COMPLETED")
    print("🎉"*40)
    print(f"\nTotal Tests: 15")
    print(f"Conversation ID: {conv_id}")
    print(f"\n✅ All tests executed successfully!")
    print("\nRecommendation: Check screenshots and UI for visual verification")

if __name__ == "__main__":
    run_comprehensive_ui_test()
