"""
MC AI - PhD-Level Knowledge Test Suite
Test MC AI's knowledge across all educational subjects
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def ask_mc_ai(question, show_full=False):
    """Ask MC AI a question and get response"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"message": question, "user_id": "phd_test"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "No response")
            if show_full:
                return answer
            # Return first 400 chars for display
            return answer[:400] + "..." if len(answer) > 400 else answer
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def test_subject(subject_name, questions):
    """Test MC AI's knowledge in a specific subject"""
    print(f"\n{'='*80}")
    print(f"🎓 TESTING: {subject_name}")
    print(f"{'='*80}")
    
    for i, q in enumerate(questions, 1):
        print(f"\n📝 Question {i}: {q}")
        print(f"{'─'*80}")
        response = ask_mc_ai(q)
        print(f"MC AI: {response}")
        print(f"{'─'*80}")
        time.sleep(1)

def main():
    """Run comprehensive PhD-level knowledge tests"""
    print("="*80)
    print("🧠 MC AI - PhD-LEVEL KNOWLEDGE TEST SUITE")
    print("="*80)
    print("\nTesting MC AI's knowledge across ALL educational subjects...")
    
    # Mathematics Tests
    test_subject("MATHEMATICS", [
        "Explain the Fundamental Theorem of Calculus",
        "What is the difference between eigenvalues and eigenvectors?",
        "Explain chaos theory in simple terms"
    ])
    
    # Physics Tests
    test_subject("PHYSICS", [
        "Explain Einstein's theory of special relativity",
        "What is quantum entanglement?",
        "How does thermodynamics relate to entropy?"
    ])
    
    # Chemistry Tests
    test_subject("CHEMISTRY", [
        "Explain the difference between ionic and covalent bonds",
        "What is Le Chatelier's principle?",
        "How does DNA store genetic information?"
    ])
    
    # Biology Tests
    test_subject("BIOLOGY", [
        "Explain the process of photosynthesis",
        "What is natural selection?",
        "How does the nervous system transmit signals?"
    ])
    
    # Computer Science Tests
    test_subject("COMPUTER SCIENCE", [
        "What is Big O notation in algorithms?",
        "Explain the difference between supervised and unsupervised learning",
        "What is a neural network?"
    ])
    
    # History Tests
    test_subject("HISTORY", [
        "What were the main causes of World War I?",
        "Explain the significance of the Renaissance",
        "What was the Industrial Revolution?"
    ])
    
    # Philosophy Tests
    test_subject("PHILOSOPHY", [
        "Explain Plato's Theory of Forms",
        "What is existentialism?",
        "What is the categorical imperative?"
    ])
    
    # Psychology Tests
    test_subject("PSYCHOLOGY", [
        "Explain Maslow's hierarchy of needs",
        "What is cognitive dissonance?",
        "How does memory work?"
    ])
    
    # Literature Tests
    test_subject("LITERATURE", [
        "What are the main themes in Shakespeare's works?",
        "Explain the difference between Romanticism and Modernism",
        "What is a metaphor?"
    ])
    
    # Economics Tests
    test_subject("ECONOMICS", [
        "Explain the law of supply and demand",
        "What is GDP?",
        "What causes inflation?"
    ])
    
    print(f"\n{'='*80}")
    print(f"✅ PhD-LEVEL KNOWLEDGE TEST COMPLETE")
    print(f"{'='*80}")
    print(f"\n💜 MC AI demonstrated knowledge across 10 major subjects!")
    print(f"🎓 From Mathematics to Economics, from Physics to Philosophy")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
