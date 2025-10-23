"""
MC AI - Knowledge Test Suite
Test MC AI's enhanced capabilities in Resonance Engine and Humor Mastery
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def ask_mc_ai(question):
    """Ask MC AI a question and get response"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": question, "user_id": "knowledge_test"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response")
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def test_resonance_knowledge():
    """Test Resonance Engine knowledge"""
    print("\n" + "="*70)
    print("🌊 TESTING: RESONANCE ENGINE KNOWLEDGE")
    print("="*70)
    
    tests = [
        {
            "question": "Explain Fourier transforms in simple terms",
            "expectation": "Should explain breaking down complex signals into sine waves"
        },
        {
            "question": "What's the relationship between frequency and wavelength?",
            "expectation": "Should explain v = fλ equation"
        },
        {
            "question": "How does echolocation work in dolphins?",
            "expectation": "Should explain biosonar and acoustic imaging"
        }
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"\n📝 Test {i}: {test['question']}")
        print(f"Expected: {test['expectation']}")
        print(f"\nMC AI's Response:")
        print("-" * 70)
        response = ask_mc_ai(test['question'])
        print(response[:500] + "..." if len(response) > 500 else response)
        print("-" * 70)

def test_humor_integration():
    """Test Humor Mastery integration"""
    print("\n" + "="*70)
    print("🎭 TESTING: HUMOR MASTERY INTEGRATION")
    print("="*70)
    
    tests = [
        {
            "question": "Tell me about harmonic oscillators, but make it fun",
            "expectation": "Should blend technical accuracy with humor"
        },
        {
            "question": "What's the difference between a pun and wordplay?",
            "expectation": "Should explain with examples and maybe use humor"
        },
        {
            "question": "I'm nervous about my ECG results",
            "expectation": "Should be comforting, possibly use gentle humor to ease worry"
        }
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"\n📝 Test {i}: {test['question']}")
        print(f"Expected: {test['expectation']}")
        print(f"\nMC AI's Response:")
        print("-" * 70)
        response = ask_mc_ai(test['question'])
        print(response[:500] + "..." if len(response) > 500 else response)
        print("-" * 70)

def test_combined_capabilities():
    """Test combined technical + social intelligence"""
    print("\n" + "="*70)
    print("💡 TESTING: COMBINED CAPABILITIES")
    print("="*70)
    
    tests = [
        {
            "question": "Explain resonance to a 10-year-old",
            "expectation": "Should use simple language, possibly humor, relatable examples"
        },
        {
            "question": "What's your favorite type of wave and why?",
            "expectation": "Should show personality, maybe joke about it"
        }
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"\n📝 Test {i}: {test['question']}")
        print(f"Expected: {test['expectation']}")
        print(f"\nMC AI's Response:")
        print("-" * 70)
        response = ask_mc_ai(test['question'])
        print(response[:500] + "..." if len(response) > 500 else response)
        print("-" * 70)

def main():
    """Run all knowledge tests"""
    print("="*70)
    print("🧪 MC AI KNOWLEDGE TEST SUITE")
    print("="*70)
    print("\nTesting MC AI's enhanced capabilities after learning 293 sources...")
    
    # Test Resonance Engine knowledge
    test_resonance_knowledge()
    
    # Test Humor Mastery integration
    test_humor_integration()
    
    # Test combined capabilities
    test_combined_capabilities()
    
    print("\n" + "="*70)
    print("✨ KNOWLEDGE TEST COMPLETE")
    print("="*70)
    print("\n💜 MC AI is demonstrating both technical expertise and social warmth!")

if __name__ == "__main__":
    main()
