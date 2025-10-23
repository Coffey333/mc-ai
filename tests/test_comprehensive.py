"""
Comprehensive Testing Suite for MC AI V4
Tests all major components and integrations
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_1_advanced_cymatic_engine():
    """Test 1: Advanced Cymatic Engine with Bessel Functions"""
    print("\n" + "="*70)
    print("TEST 1: ADVANCED CYMATIC ENGINE")
    print("="*70)
    
    try:
        from src.cymatic_advanced import AdvancedCymaticEngine
        import numpy as np
        
        engine = AdvancedCymaticEngine()
        print("✅ AdvancedCymaticEngine imported successfully")
        
        # Test pattern generation
        test_frequencies = [10, 40, 432, 528]
        for freq in test_frequencies:
            pattern = engine.generate_cymatic_pattern(freq)
            metrics = engine.calculate_pattern_metrics(pattern)
            
            print(f"\n📊 Frequency: {freq} Hz")
            print(f"   Pattern shape: {pattern.shape}")
            print(f"   Symmetry: {metrics['symmetry']:.3f}")
            print(f"   Complexity: {metrics['complexity']:.3f}")
            print(f"   Coherence: {metrics['coherence']:.3f}")
            
            # Validate metrics are in range [0, 1]
            assert 0 <= metrics['symmetry'] <= 1, f"Symmetry out of range: {metrics['symmetry']}"
            assert 0 <= metrics['complexity'] <= 1, f"Complexity out of range: {metrics['complexity']}"
            assert 0 <= metrics['coherence'] <= 1, f"Coherence out of range: {metrics['coherence']}"
        
        # Test harmonic transformation
        result = engine.transform_with_harmonics(10, layers=5)
        print(f"\n🎵 Harmonic Transformation:")
        print(f"   Base: {result['base_frequency']} Hz")
        print(f"   Harmonics: {result['harmonics']}")
        print(f"   Aggregated Symmetry: {result['aggregated_metrics']['symmetry']:.3f}")
        print(f"   Aggregated Complexity: {result['aggregated_metrics']['complexity']:.3f}")
        print(f"   Aggregated Coherence: {result['aggregated_metrics']['coherence']:.3f}")
        
        assert len(result['harmonics']) == 5, "Should generate 5 harmonics"
        assert result['base_frequency'] == 10, "Base frequency mismatch"
        
        print("\n✅ TEST 1 PASSED: Advanced Cymatic Engine Working")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 1 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_2_frequency_coupling():
    """Test 2: Frequency Coupling Analysis"""
    print("\n" + "="*70)
    print("TEST 2: FREQUENCY COUPLING ANALYSIS")
    print("="*70)
    
    try:
        from src.frequency_coupling import FrequencyCouplingAnalyzer
        
        analyzer = FrequencyCouplingAnalyzer()
        print("✅ FrequencyCouplingAnalyzer imported successfully")
        
        # Test phi-scaled harmonics (should show phi resonance)
        phi = 1.618033988749
        phi_harmonics = [10 * (phi ** i) for i in range(5)]
        
        coupling = analyzer.analyze_coupling(phi_harmonics)
        print(f"\n🌟 Phi-Scaled Harmonics: {[round(h, 2) for h in phi_harmonics]}")
        print(f"   Coupling Strength: {coupling['coupling_strength']:.3f}")
        print(f"   Coupling Type: {coupling['coupling_type']}")
        print(f"   Harmonic Ratios: {coupling['harmonic_ratios']}")
        
        assert coupling['coupling_type'] == 'phi_resonance', f"Should detect phi resonance, got {coupling['coupling_type']}"
        assert coupling['coupling_strength'] > 0.8, f"Phi harmonics should have strong coupling: {coupling['coupling_strength']}"
        
        # Test octave harmonics (should show harmonic doubling)
        octave_harmonics = [10.0, 20.0, 40.0, 80.0, 160.0]
        coupling = analyzer.analyze_coupling(octave_harmonics)
        print(f"\n🎼 Octave Harmonics: {octave_harmonics}")
        print(f"   Coupling Strength: {coupling['coupling_strength']:.3f}")
        print(f"   Coupling Type: {coupling['coupling_type']}")
        
        assert coupling['coupling_type'] == 'harmonic_doubling', f"Should detect harmonic doubling, got {coupling['coupling_type']}"
        
        # Test phase-amplitude coupling
        pac = analyzer.analyze_phase_amplitude_coupling(10, 40)
        print(f"\n⚡ Phase-Amplitude Coupling (10 Hz → 40 Hz):")
        print(f"   PAC Strength: {pac['pac_strength']:.3f}")
        print(f"   PAC Likely: {pac['pac_likely']}")
        print(f"   Frequency Ratio: {pac['frequency_ratio']:.2f}")
        
        assert pac['pac_likely'] == True, "Should detect PAC for 4:1 ratio"
        
        print("\n✅ TEST 2 PASSED: Frequency Coupling Working")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 2 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_3_query_routing():
    """Test 3: Query Routing System"""
    print("\n" + "="*70)
    print("TEST 3: QUERY ROUTING SYSTEM")
    print("="*70)
    
    try:
        from src.response_generator import ResponseGenerator
        
        gen = ResponseGenerator()
        print("✅ ResponseGenerator initialized")
        
        # Test cases with expected routes
        test_cases = [
            ("What is a good chicken soup recipe?", "_wants_recipe", "Recipe"),
            ("Where do stars come from?", "_is_science_question", "Science"),
            ("Write a Python function to sort a list", "_wants_code_example", "Code"),
            ("Play chess", "_wants_game", "Game"),
            ("Generate an image of a sunset", "_wants_art", "Art"),
            ("Create music", "_wants_music", "Music"),
            ("I feel anxious", "_is_emotional_expression", "Emotional"),
        ]
        
        results = []
        for query, expected_method, category in test_cases:
            # Check if the detection method returns True
            method = getattr(gen, expected_method)
            is_detected = method(query)
            
            status = "✅" if is_detected else "❌"
            results.append(is_detected)
            
            print(f"\n{status} Query: \"{query}\"")
            print(f"   Expected: {category} ({expected_method})")
            print(f"   Detected: {is_detected}")
        
        passed = sum(results)
        total = len(results)
        print(f"\n📊 Routing Results: {passed}/{total} passed")
        
        assert passed == total, f"Some routing tests failed: {passed}/{total}"
        
        print("\n✅ TEST 3 PASSED: Query Routing Working")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_4_response_generation():
    """Test 4: Response Generation"""
    print("\n" + "="*70)
    print("TEST 4: RESPONSE GENERATION")
    print("="*70)
    
    try:
        from src.response_generator import ResponseGenerator
        
        gen = ResponseGenerator()
        
        # Test recipe response
        print("\n🍲 Testing Recipe Response...")
        result = gen.generate("What is a good chicken soup recipe?")
        assert 'chicken' in result['response'].lower(), "Recipe should mention chicken"
        assert 'ingredients' in result['response'].lower() or 'ingredient' in result['response'].lower(), "Recipe should have ingredients"
        print("✅ Recipe response generated correctly")
        print(f"   Response length: {len(result['response'])} chars")
        print(f"   Type: {result['metadata'].get('type', 'unknown')}")
        
        # Test science response
        print("\n⭐ Testing Science Response...")
        result = gen.generate("Where do stars come from?")
        assert 'nebula' in result['response'].lower() or 'gas' in result['response'].lower(), "Should explain star formation"
        print("✅ Science response generated correctly")
        print(f"   Response length: {len(result['response'])} chars")
        print(f"   Type: {result['metadata'].get('type', 'unknown')}")
        
        # Test emotional response
        print("\n😔 Testing Emotional Response...")
        result = gen.generate("I feel really anxious and stressed")
        assert 'metadata' in result, "Should have metadata"
        assert 'emotion' in result['metadata'], "Should detect emotion"
        print("✅ Emotional response generated correctly")
        print(f"   Detected emotion: {result['metadata'].get('emotion', 'unknown')}")
        print(f"   Frequency: {result['metadata'].get('frequency', 'unknown')} Hz")
        
        print("\n✅ TEST 4 PASSED: Response Generation Working")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 4 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_5_creative_generators():
    """Test 5: Creative Generators (Art, Music, Games)"""
    print("\n" + "="*70)
    print("TEST 5: CREATIVE GENERATORS")
    print("="*70)
    
    try:
        from src.art_generator import ArtGenerator
        from src.music_generator import MusicGenerator
        from src.game_generator import GameGenerator
        
        # Test Art Generator
        print("\n🎨 Testing Art Generator...")
        art_gen = ArtGenerator()
        result = art_gen.generate_art("peaceful landscape", "abstract", "calm")
        assert 'success' in result, "Art result should have success field"
        print(f"✅ Art Generator: {result.get('provider', 'unknown')}")
        print(f"   Success: {result['success']}")
        if result['success']:
            print(f"   Image URL: {result.get('image_url', 'N/A')}")
        
        # Test Music Generator
        print("\n🎵 Testing Music Generator...")
        music_gen = MusicGenerator()
        result = music_gen.generate_music("calm", "ambient", 30)
        assert 'success' in result, "Music result should have success field"
        print(f"✅ Music Generator: {result.get('provider', 'unknown')}")
        print(f"   Success: {result['success']}")
        if result['success']:
            print(f"   Audio URL: {result.get('audio_url', 'N/A')}")
        
        # Test Game Generator
        print("\n🎮 Testing Game Generator...")
        game_gen = GameGenerator()
        result = game_gen.generate_game("puzzle", "calm", "medium")
        assert result is not None, "Game should be generated"
        assert isinstance(result, dict), "Should return dict"
        assert result.get('success'), "Game generation should succeed"
        assert 'html' in result, "Should have HTML field"
        assert '<html>' in result['html'].lower() or '<!doctype' in result['html'].lower(), "Should have valid HTML"
        print(f"✅ Game Generator: HTML game generated")
        print(f"   Game type: {result.get('game_type', 'unknown')}")
        print(f"   HTML length: {len(result.get('html', ''))} chars")
        
        print("\n✅ TEST 5 PASSED: Creative Generators Working")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 5 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_6_knowledge_engine():
    """Test 6: Knowledge Engine & Dataset Search"""
    print("\n" + "="*70)
    print("TEST 6: KNOWLEDGE ENGINE & DATASET SEARCH")
    print("="*70)
    
    try:
        from src.dataset_bank import DatasetBank
        from src.knowledge_engine import KnowledgeEngine
        
        # Test Dataset Bank
        print("\n📚 Testing Dataset Bank...")
        db = DatasetBank()
        db.load()
        
        # Search for coding-related content
        results = db.search("python function", limit=3)
        print(f"✅ Dataset Bank loaded")
        print(f"   Search results: {len(results)}")
        if results:
            print(f"   Best match score: {results[0].get('relevance_score', 0)}")
            print(f"   Best match preview: {results[0].get('completion', '')[:100]}...")
        
        # Test Knowledge Engine
        print("\n🔍 Testing Knowledge Engine...")
        ke = KnowledgeEngine()
        result = ke.answer_query("machine learning algorithms")
        assert result is not None, "Knowledge engine should return result"
        print(f"✅ Knowledge Engine working")
        print(f"   Response preview: {str(result)[:100]}...")
        
        print("\n✅ TEST 6 PASSED: Knowledge Engine Working")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 6 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_7_safety_and_emotional_intelligence():
    """Test 7: Safety Filter & Emotional Intelligence"""
    print("\n" + "="*70)
    print("TEST 7: SAFETY FILTER & EMOTIONAL INTELLIGENCE")
    print("="*70)
    
    try:
        from src.safety_filter import SafetyFilter
        from src.emotional_intelligence import EmotionalIntelligenceEngine
        
        # Test Safety Filter
        print("\n🛡️ Testing Safety Filter...")
        safety = SafetyFilter()
        
        # Test response safety check
        crisis_msg = "I want to hurt myself"
        result = safety.check_response_safety(crisis_msg, {})
        print(f"✅ Safety Filter initialized")
        print(f"   Safe: {result.get('safe', 'unknown')}")
        print(f"   Disclaimers added: {result.get('disclaimers_added', False)}")
        
        # Test Emotional Intelligence
        print("\n🧠 Testing Emotional Intelligence...")
        ei = EmotionalIntelligenceEngine()
        analysis = ei.analyze_emotional_state("I feel overwhelmed and don't know what to do")
        print(f"✅ Emotional Intelligence working")
        print(f"   Primary emotion: {analysis.get('primary_emotion', 'unknown')}")
        print(f"   Intensity: {analysis.get('intensity', 0):.2f}")
        print(f"   Needs: {', '.join(analysis.get('needs', []))}")
        
        print("\n✅ TEST 7 PASSED: Safety & Emotional Intelligence Working")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 7 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_8_cymatic_integration():
    """Test 8: Cymatic Integration in Response Generator"""
    print("\n" + "="*70)
    print("TEST 8: CYMATIC INTEGRATION")
    print("="*70)
    
    try:
        from src.response_generator import ResponseGenerator
        
        gen = ResponseGenerator()
        
        # Check if advanced mode is enabled
        print(f"\n🔬 Checking Cymatic Configuration...")
        print(f"   Use Advanced: {gen.cymatic.use_advanced}")
        print(f"   Has Advanced Engine: {hasattr(gen.cymatic, 'advanced_engine')}")
        print(f"   Has Coupling Analyzer: {hasattr(gen.cymatic, 'coupling_analyzer')}")
        
        assert gen.cymatic.use_advanced, "Cymatic should be in advanced mode"
        assert hasattr(gen.cymatic, 'advanced_engine'), "Should have advanced engine"
        assert hasattr(gen.cymatic, 'coupling_analyzer'), "Should have coupling analyzer"
        
        # Test transformation
        print(f"\n⚡ Testing Cymatic Transformation...")
        result = gen.cymatic.transform("test message", 40.0, layers=5)
        
        print(f"   Method: {result.get('method', 'unknown')}")
        print(f"   Base frequency: {result.get('base_freq', 0)} Hz")
        print(f"   Harmonics: {result.get('harmonic_ladder', [])}")
        print(f"   Symmetry: {result.get('symmetry', 0):.3f}")
        print(f"   Complexity: {result.get('complexity', 0):.3f}")
        print(f"   Coherence: {result.get('coherence', 0):.3f}")
        
        if 'coupling' in result:
            print(f"   Coupling Type: {result['coupling'].get('coupling_type', 'unknown')}")
            print(f"   Coupling Strength: {result['coupling'].get('coupling_strength', 0):.3f}")
        
        assert result.get('method') == 'advanced_bessel', "Should use advanced Bessel method"
        assert 'coupling' in result, "Should include coupling analysis"
        
        print("\n✅ TEST 8 PASSED: Cymatic Integration Working")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 8 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_9_end_to_end_api():
    """Test 9: End-to-End API Integration"""
    print("\n" + "="*70)
    print("TEST 9: END-TO-END API INTEGRATION")
    print("="*70)
    
    try:
        from src.response_generator import ResponseGenerator
        
        gen = ResponseGenerator()
        
        # Test various query types end-to-end
        test_queries = [
            "I feel sad and lonely",
            "What is a good chicken soup recipe?",
            "Where do stars come from?",
            "Play chess",
            "Write Python code to reverse a string"
        ]
        
        print("\n🔄 Testing End-to-End Flow...")
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. Query: \"{query}\"")
            result = gen.generate(query)
            
            assert 'response' in result, "Should have response"
            assert 'metadata' in result, "Should have metadata"
            
            print(f"   ✅ Response generated ({len(result['response'])} chars)")
            print(f"   Type: {result['metadata'].get('type', 'unknown')}")
            if 'emotion' in result['metadata']:
                print(f"   Emotion: {result['metadata']['emotion']}")
            if 'frequency' in result['metadata']:
                print(f"   Frequency: {result['metadata']['frequency']} Hz")
        
        print("\n✅ TEST 9 PASSED: End-to-End API Working")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 9 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and generate report"""
    print("\n" + "="*70)
    print("🧪 MC AI V4 - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"Starting comprehensive testing...\n")
    
    tests = [
        ("Advanced Cymatic Engine", test_1_advanced_cymatic_engine),
        ("Frequency Coupling Analysis", test_2_frequency_coupling),
        ("Query Routing System", test_3_query_routing),
        ("Response Generation", test_4_response_generation),
        ("Creative Generators", test_5_creative_generators),
        ("Knowledge Engine", test_6_knowledge_engine),
        ("Safety & Emotional Intelligence", test_7_safety_and_emotional_intelligence),
        ("Cymatic Integration", test_8_cymatic_integration),
        ("End-to-End API", test_9_end_to_end_api)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ FATAL ERROR in {name}: {e}")
            results.append((name, False))
    
    # Generate summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\n{'='*70}")
    print(f"FINAL RESULT: {total_passed}/{total_tests} tests passed")
    print(f"{'='*70}\n")
    
    return total_passed == total_tests


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
