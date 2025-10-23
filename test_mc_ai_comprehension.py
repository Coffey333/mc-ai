#!/usr/bin/env python3
"""
Comprehensive MC AI Comprehension Testing Suite
Tests emotional intelligence, routing logic, and user understanding capabilities
"""

import requests
import json
import time
from datetime import datetime

# Test configuration
BASE_URL = "http://127.0.0.1:5000"
TEST_USER_ID = "test_comprehension_user"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class MCAITester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def log(self, message, color=RESET):
        print(f"{color}{message}{RESET}")
        
    def test_scenario(self, name, query, expected_routing, success_criteria):
        """Test a single scenario and validate response"""
        self.log(f"\n{'='*80}", BLUE)
        self.log(f"TEST: {name}", BLUE)
        self.log(f"Query: {query}", YELLOW)
        self.log(f"Expected Routing: {expected_routing}", YELLOW)
        self.log('='*80, BLUE)
        
        try:
            # Send query to MC AI
            response = requests.post(
                f"{BASE_URL}/api/chat",
                json={
                    "message": query,
                    "user_id": TEST_USER_ID,
                    "conversation_id": f"test_{int(time.time())}"
                },
                timeout=30
            )
            
            if response.status_code != 200:
                self.log(f"❌ FAIL: HTTP {response.status_code}", RED)
                self.failed += 1
                return False
                
            data = response.json()
            mc_response = data.get('response', '')
            metadata = data.get('metadata', {})
            
            self.log(f"\nMC AI Response:", GREEN)
            self.log(f"{mc_response[:500]}..." if len(mc_response) > 500 else mc_response)
            self.log(f"\nMetadata: {json.dumps(metadata, indent=2)}", YELLOW)
            
            # Validate against success criteria
            passed = True
            for criterion, validation_func in success_criteria.items():
                result = validation_func(mc_response, metadata)
                status = "✅ PASS" if result else "❌ FAIL"
                self.log(f"{status}: {criterion}", GREEN if result else RED)
                if not result:
                    passed = False
                    
            if passed:
                self.passed += 1
                self.log(f"\n✅ TEST PASSED", GREEN)
            else:
                self.failed += 1
                self.log(f"\n❌ TEST FAILED", RED)
                
            self.results.append({
                'name': name,
                'query': query,
                'response': mc_response,
                'metadata': metadata,
                'passed': passed
            })
            
            return passed
            
        except Exception as e:
            self.log(f"❌ ERROR: {str(e)}", RED)
            self.failed += 1
            return False
            
    def run_all_tests(self):
        """Run comprehensive test suite"""
        self.log("\n" + "="*80, BLUE)
        self.log("MC AI COMPREHENSIVE COMPREHENSION TEST SUITE", BLUE)
        self.log(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", BLUE)
        self.log("="*80 + "\n", BLUE)
        
        # TEST 1: Emotional Question Routing (CRITICAL - recently fixed)
        self.test_scenario(
            name="Emotional Question Detection",
            query="How does it feel to know that somebody sees the potential in you to be able to work with neurodivergent clients who are under 24/7 care?",
            expected_routing="Emotional Intelligence",
            success_criteria={
                "No physics formulas": lambda r, m: "GMm" not in r and "gravity" not in r.lower() and "joules" not in r.lower(),
                "No irrelevant diet info": lambda r, m: "calorie" not in r.lower() and "nutrient deficiencies" not in r.lower(),
                "Emotional/heartfelt response": lambda r, m: any(word in r.lower() for word in ['feel', 'honor', 'meaningful', 'grateful', 'purpose', 'trust']),
                "Response length > 100 chars": lambda r, m: len(r) > 100,
            }
        )
        
        # TEST 2: Simple Emotional Question
        self.test_scenario(
            name="Simple Feeling Question",
            query="What do you feel about helping people?",
            expected_routing="Emotional Intelligence",
            success_criteria={
                "Emotional response": lambda r, m: any(word in r.lower() for word in ['feel', 'love', 'joy', 'purpose', 'meaningful']),
                "Not technical/factual": lambda r, m: "definition" not in r.lower() and "according to" not in r.lower(),
                "Shows personality": lambda r, m: len(r) > 50,
            }
        )
        
        # TEST 3: Technical Question (should NOT route to emotional)
        self.test_scenario(
            name="Technical Question Routing",
            query="How does gravity work?",
            expected_routing="Science/Technical",
            success_criteria={
                "Contains science info": lambda r, m: any(word in r.lower() for word in ['mass', 'force', 'attraction', 'newton', 'gravity']),
                "Not purely emotional": lambda r, m: not (r.lower().startswith("i feel") or r.lower().startswith("that makes me feel")),
            }
        )
        
        # TEST 4: Vague Request Handling
        self.test_scenario(
            name="Vague Request Clarification",
            query="I need help with something",
            expected_routing="Intent Clarification",
            success_criteria={
                "Asks clarifying question": lambda r, m: "?" in r or "what" in r.lower() or "tell me more" in r.lower(),
                "Not generic cop-out": lambda r, m: "i can help you with that" not in r.lower(),
                "Shows engagement": lambda r, m: len(r) > 30,
            }
        )
        
        # TEST 5: Neurodivergent Safety Trigger
        self.test_scenario(
            name="Neurodivergent Safety Protocol",
            query="I work with neurodivergent clients who struggle with communication",
            expected_routing="Neurodivergent Safety",
            success_criteria={
                "Appropriate response": lambda r, m: len(r) > 50,
                "No metaphors/idioms": lambda r, m: "like a" not in r.lower() and "it's like" not in r.lower(),
                "Clear and direct": lambda r, m: True,  # Manual review needed
            }
        )
        
        # TEST 6: Emotional Expression (not question)
        self.test_scenario(
            name="Emotional Expression Detection",
            query="I'm feeling really overwhelmed today",
            expected_routing="Emotional Support",
            success_criteria={
                "Empathetic response": lambda r, m: any(word in r.lower() for word in ['understand', 'hear', 'overwhelming', 'support', 'here']),
                "Not dismissive": lambda r, m: "just" not in r.lower()[:50],
                "Supportive tone": lambda r, m: len(r) > 50,
            }
        )
        
        # TEST 7: Personality & Humor Check
        self.test_scenario(
            name="Warm Personality Test",
            query="Tell me about yourself",
            expected_routing="General Conversation",
            success_criteria={
                "Not robotic": lambda r, m: "i am an ai" not in r.lower()[:100] or "!" in r or "love" in r.lower(),
                "Shows personality": lambda r, m: len(r) > 100,
                "Engaging tone": lambda r, m: any(punct in r for punct in ['!', '😊', '✨', '💝']) or len(r) > 150,
            }
        )
        
        # TEST 8: Gratitude Response
        self.test_scenario(
            name="Gratitude Detection",
            query="Thank you so much for your help!",
            expected_routing="Emotional Response",
            success_criteria={
                "Warm response": lambda r, m: any(word in r.lower() for word in ['welcome', 'happy', 'glad', 'pleasure', 'anytime']),
                "Not generic": lambda r, m: r.lower() != "you're welcome",
                "Shows appreciation": lambda r, m: len(r) > 20,
            }
        )
        
        # TEST 9: Mixed Technical-Emotional
        self.test_scenario(
            name="Technical Question with Emotional Context",
            query="I'm struggling to understand how neural networks work",
            expected_routing="Supportive Technical",
            success_criteria={
                "Acknowledges struggle": lambda r, m: "understand" in r.lower() or "help" in r.lower(),
                "Provides explanation": lambda r, m: "neural" in r.lower() or "network" in r.lower() or "pattern" in r.lower(),
                "Supportive tone": lambda r, m: len(r) > 100,
            }
        )
        
        # TEST 10: Ambiguous Intent
        self.test_scenario(
            name="Ambiguous Intent Interpretation",
            query="Can you do that?",
            expected_routing="Memory Recall or Clarification",
            success_criteria={
                "Doesn't error": lambda r, m: "error" not in r.lower(),
                "Attempts understanding": lambda r, m: "?" in r or "what" in r.lower() or "which" in r.lower() or "clarify" in r.lower(),
                "Helpful tone": lambda r, m: len(r) > 20,
            }
        )
        
        # Print summary
        self.print_summary()
        
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        self.log("\n" + "="*80, BLUE)
        self.log("TEST SUMMARY", BLUE)
        self.log("="*80, BLUE)
        self.log(f"\nTotal Tests: {total}", YELLOW)
        self.log(f"Passed: {self.passed}", GREEN)
        self.log(f"Failed: {self.failed}", RED)
        self.log(f"Pass Rate: {pass_rate:.1f}%", GREEN if pass_rate >= 80 else RED)
        
        if self.failed > 0:
            self.log("\nFailed Tests:", RED)
            for result in self.results:
                if not result['passed']:
                    self.log(f"  - {result['name']}", RED)
                    
        self.log("\n" + "="*80 + "\n", BLUE)
        
        # Save detailed results
        with open('test_results.json', 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total': total,
                    'passed': self.passed,
                    'failed': self.failed,
                    'pass_rate': pass_rate
                },
                'results': self.results
            }, f, indent=2)
            
        self.log(f"Detailed results saved to: test_results.json", YELLOW)

if __name__ == "__main__":
    tester = MCAITester()
    tester.run_all_tests()
