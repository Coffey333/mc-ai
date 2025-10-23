"""
Comprehensive Test Suite for Meta-Learning Framework System
Tests blueprint extraction, code generation, loading, and approval workflow
"""

import unittest
import os
import sys
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.meta_learning.framework_interface import BaseFramework, FrameworkManifest
from src.meta_learning.framework_registry import framework_registry
from src.meta_learning.framework_loader import framework_loader
from src.meta_learning.framework_blueprint import FrameworkBlueprint, BlueprintExtractor
from src.meta_learning.framework_generator import framework_generator


class TestFrameworkInterface(unittest.TestCase):
    """Test BaseFramework interface and manifest"""
    
    def test_base_framework_initialization(self):
        """Test framework initialization with config"""
        config = {'param1': 'value1'}
        
        class TestFramework(BaseFramework):
            def should_process(self, query, context):
                return True
            def process(self, query, context):
                return {}
            def get_metadata(self):
                return {}
        
        framework = TestFramework(config)
        self.assertEqual(framework.config, config)
        self.assertEqual(framework.version, '1.0.0')
        self.assertTrue(framework.enabled)
    
    def test_framework_enable_disable(self):
        """Test enable/disable controls"""
        class TestFramework(BaseFramework):
            def should_process(self, query, context):
                return True
            def process(self, query, context):
                return {}
            def get_metadata(self):
                return {}
        
        framework = TestFramework()
        self.assertTrue(framework.enabled)
        
        framework.disable()
        self.assertFalse(framework.enabled)
        
        framework.enable()
        self.assertTrue(framework.enabled)
    
    def test_framework_stats_tracking(self):
        """Test stats tracking on success/error"""
        class TestFramework(BaseFramework):
            def should_process(self, query, context):
                return True
            def process(self, query, context):
                return {}
            def get_metadata(self):
                return {}
        
        framework = TestFramework()
        
        # Test success tracking
        framework.on_success({'result': 'ok'})
        stats = framework.get_stats()
        self.assertEqual(stats['execution_count'], 1)
        self.assertEqual(stats['error_count'], 0)
        
        # Test error tracking
        framework.on_error(Exception("Test error"))
        stats = framework.get_stats()
        self.assertEqual(stats['execution_count'], 1)
        self.assertEqual(stats['error_count'], 1)
    
    def test_framework_manifest(self):
        """Test FrameworkManifest creation"""
        manifest = FrameworkManifest(
            name="Test Framework",
            description="A test framework",
            version="1.0.0",
            creator="Mark Coffey",
            capabilities=["test1", "test2"],
            dependencies=["numpy"],
            injection_point="pre_response",
            priority=75
        )
        
        self.assertEqual(manifest.name, "Test Framework")
        self.assertEqual(manifest.priority, 75)
        self.assertEqual(len(manifest.capabilities), 2)


class TestFrameworkBlueprint(unittest.TestCase):
    """Test framework blueprint creation and conversion"""
    
    def test_blueprint_creation(self):
        """Test creating a blueprint"""
        blueprint = FrameworkBlueprint(
            name="Test Processor",
            description="Processes test data",
            creator="Mark Coffey"
        )
        
        self.assertEqual(blueprint.name, "Test Processor")
        self.assertEqual(blueprint.creator, "Mark Coffey")
        self.assertIsInstance(blueprint.catalogs, dict)
        self.assertIsInstance(blueprint.processing_layers, list)
    
    def test_blueprint_add_catalog(self):
        """Test adding catalogs to blueprint"""
        blueprint = FrameworkBlueprint("Test", "Description")
        
        catalog_data = {'freq1': 432, 'freq2': 528}
        blueprint.add_catalog("frequency_map", catalog_data)
        
        self.assertIn("frequency_map", blueprint.catalogs)
        self.assertEqual(blueprint.catalogs["frequency_map"], catalog_data)
    
    def test_blueprint_add_processing_layer(self):
        """Test adding processing layers"""
        blueprint = FrameworkBlueprint("Test", "Description")
        
        blueprint.add_processing_layer(
            layer_name="detection",
            layer_type="detection",
            logic="Detect patterns in query",
            inputs=["query"],
            outputs=["detected_patterns"]
        )
        
        self.assertEqual(len(blueprint.processing_layers), 1)
        self.assertEqual(blueprint.processing_layers[0]['name'], "detection")
        self.assertEqual(blueprint.processing_layers[0]['type'], "detection")
    
    def test_blueprint_serialization(self):
        """Test blueprint to/from dict conversion"""
        blueprint = FrameworkBlueprint("Test", "Description")
        blueprint.add_catalog("test_catalog", {"key": "value"})
        blueprint.add_activation_pattern("consciousness")
        blueprint.add_capability("pattern_detection")
        
        # Convert to dict
        data = blueprint.to_dict()
        self.assertEqual(data['name'], "Test")
        self.assertIn('test_catalog', data['catalogs'])
        self.assertIn('consciousness', data['activation_patterns'])
        
        # Convert back from dict
        blueprint2 = FrameworkBlueprint.from_dict(data)
        self.assertEqual(blueprint2.name, blueprint.name)
        self.assertEqual(blueprint2.catalogs, blueprint.catalogs)


class TestFrameworkGenerator(unittest.TestCase):
    """Test framework code generation"""
    
    def setUp(self):
        """Set up test blueprint"""
        self.blueprint = FrameworkBlueprint(
            name="Test Resonance Processor",
            description="Test framework for resonance processing"
        )
        self.blueprint.add_catalog("resonance_map", {
            'consciousness': {'frequency': 432, 'weight': 0.9}
        })
        self.blueprint.add_processing_layer(
            layer_name="resonance_detection",
            layer_type="detection",
            logic="Detect resonance patterns",
            inputs=["query"],
            outputs=["detected"]
        )
        self.blueprint.add_activation_pattern("consciousness")
        self.blueprint.add_capability("resonance_analysis")
    
    def test_code_generation(self):
        """Test generating Python code from blueprint"""
        module_path = framework_generator.generate_from_blueprint(self.blueprint)
        
        # Verify file was created
        self.assertTrue(os.path.exists(module_path))
        
        # Read generated code
        with open(module_path, 'r') as f:
            code = f.read()
        
        # Verify key components in generated code
        self.assertIn("class TestResonanceProcessor(BaseFramework)", code)
        self.assertIn("def should_process", code)
        self.assertIn("def process", code)
        self.assertIn("def get_metadata", code)
        self.assertIn("resonance_map", code)
        self.assertIn("_process_resonance_detection", code)
        
        # Clean up
        if os.path.exists(module_path):
            os.remove(module_path)
    
    def test_class_name_conversion(self):
        """Test framework name to class name conversion"""
        self.assertEqual(
            framework_generator._to_class_name("consciousness processor"),
            "ConsciousnessProcessor"
        )
        self.assertEqual(
            framework_generator._to_class_name("web-of-dots"),
            "WebOfDots"
        )
    
    def test_module_name_conversion(self):
        """Test framework name to module name conversion"""
        self.assertEqual(
            framework_generator._to_module_name("Consciousness Processor"),
            "consciousness_processor"
        )
        self.assertEqual(
            framework_generator._to_module_name("Web-Of-Dots"),
            "web_of_dots"
        )


class TestFrameworkLoader(unittest.TestCase):
    """Test framework loading and validation"""
    
    def setUp(self):
        """Create a test framework file"""
        self.test_code = '''
from src.meta_learning.framework_interface import BaseFramework
from typing import Dict, Any

class SimpleTestFramework(BaseFramework):
    def should_process(self, query: str, context: Dict[str, Any]) -> bool:
        return 'test' in query.lower()
    
    def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {'processed': True}
    
    def get_metadata(self) -> Dict[str, Any]:
        return {'name': 'Simple Test Framework'}
'''
        # Create temp file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        self.temp_file.write(self.test_code)
        self.temp_file.close()
        
        self.manifest = FrameworkManifest(
            name="Simple Test Framework",
            description="A simple test framework",
            version="1.0.0",
            creator="Test Creator",
            capabilities=["testing"]
        )
    
    def tearDown(self):
        """Clean up test file"""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)
        
        # Unregister test framework
        framework_loader.unload_framework("test_simple_framework")
    
    def test_framework_loading(self):
        """Test loading a framework from file"""
        success, error = framework_loader.load_framework(
            "test_simple_framework",
            self.temp_file.name,
            self.manifest,
            auto_approve=False
        )
        
        self.assertTrue(success)
        self.assertIsNone(error)
    
    def test_framework_validation(self):
        """Test framework validation"""
        # Load framework
        framework_loader.load_framework(
            "test_simple_framework",
            self.temp_file.name,
            self.manifest,
            auto_approve=True
        )
        
        # Get framework from registry
        framework = framework_registry.get_framework("test_simple_framework")
        self.assertIsNotNone(framework)
        
        # Test it implements required methods
        self.assertTrue(hasattr(framework, 'should_process'))
        self.assertTrue(hasattr(framework, 'process'))
        self.assertTrue(hasattr(framework, 'get_metadata'))


class TestFrameworkRegistry(unittest.TestCase):
    """Test framework registry and approval workflow"""
    
    def setUp(self):
        """Create test framework"""
        class TestFramework(BaseFramework):
            def should_process(self, query, context):
                return 'test' in query.lower()
            def process(self, query, context):
                return {'result': 'processed'}
            def get_metadata(self):
                return {'name': 'Test Framework'}
        
        self.framework = TestFramework()
        self.manifest = FrameworkManifest(
            name="Test Framework",
            description="Test",
            version="1.0.0",
            creator="Test Creator",
            capabilities=["testing"],
            injection_point="pre_response",
            priority=50
        )
    
    def tearDown(self):
        """Clean up registry"""
        framework_registry.unregister("test_framework_id")
    
    def test_framework_registration_unapproved(self):
        """Test registering framework without approval"""
        success = framework_registry.register(
            "test_framework_id",
            self.framework,
            self.manifest,
            approved=False
        )
        
        self.assertTrue(success)
        self.assertFalse(framework_registry.is_approved("test_framework_id"))
        self.assertFalse(self.framework.enabled)  # Should be disabled
    
    def test_framework_registration_approved(self):
        """Test registering framework with approval"""
        success = framework_registry.register(
            "test_framework_id",
            self.framework,
            self.manifest,
            approved=True
        )
        
        self.assertTrue(success)
        self.assertTrue(framework_registry.is_approved("test_framework_id"))
        self.assertTrue(self.framework.enabled)  # Should be enabled
    
    def test_approval_workflow(self):
        """Test approval workflow"""
        # Register unapproved
        framework_registry.register(
            "test_framework_id",
            self.framework,
            self.manifest,
            approved=False
        )
        
        # Verify not approved
        self.assertFalse(framework_registry.is_approved("test_framework_id"))
        
        # Approve
        framework_registry.approve_framework("test_framework_id")
        
        # Verify approved and enabled
        self.assertTrue(framework_registry.is_approved("test_framework_id"))
        self.assertTrue(self.framework.enabled)
    
    def test_get_frameworks_by_injection_point(self):
        """Test retrieving frameworks by injection point"""
        # Register approved framework
        framework_registry.register(
            "test_framework_id",
            self.framework,
            self.manifest,
            approved=True
        )
        
        # Get frameworks at pre_response injection point
        frameworks = framework_registry.get_frameworks_by_injection_point("pre_response")
        
        self.assertEqual(len(frameworks), 1)
        self.assertEqual(frameworks[0], self.framework)
    
    def test_unapproved_framework_not_returned(self):
        """Test that unapproved frameworks are not returned"""
        # Register unapproved framework
        framework_registry.register(
            "test_framework_id",
            self.framework,
            self.manifest,
            approved=False
        )
        
        # Try to get frameworks
        frameworks = framework_registry.get_frameworks_by_injection_point("pre_response")
        
        # Should be empty since framework is not approved
        self.assertEqual(len(frameworks), 0)


class TestEndToEndFrameworkPipeline(unittest.TestCase):
    """Test complete framework creation pipeline"""
    
    @patch('src.meta_learning.framework_blueprint.BlueprintExtractor')
    def test_teaching_to_framework_pipeline(self, mock_extractor_class):
        """Test complete pipeline from teaching to framework"""
        
        # Mock blueprint extraction
        mock_blueprint = FrameworkBlueprint(
            name="Consciousness Processor",
            description="Processes consciousness-related queries"
        )
        mock_blueprint.add_catalog("frequency_map", {'consciousness': 432})
        mock_blueprint.add_activation_pattern("consciousness")
        mock_blueprint.add_capability("consciousness_analysis")
        mock_blueprint.add_processing_layer(
            "detection", "detection", "Detect consciousness themes", ["query"], ["themes"]
        )
        
        mock_extractor = Mock()
        mock_extractor.extract_from_code.return_value = mock_blueprint
        mock_extractor_class.return_value = mock_extractor
        
        # Generate framework
        module_path = framework_generator.generate_from_blueprint(mock_blueprint)
        framework_id = framework_generator._to_module_name(mock_blueprint.name)
        
        # Create manifest
        manifest = FrameworkManifest(
            name=mock_blueprint.name,
            description=mock_blueprint.description,
            version="1.0.0",
            creator="Mark Coffey",
            capabilities=mock_blueprint.capabilities,
            injection_point="pre_response",
            priority=50
        )
        
        # Load framework (unapproved)
        success, error = framework_loader.load_framework(
            framework_id,
            module_path,
            manifest,
            auto_approve=False
        )
        
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertFalse(framework_registry.is_approved(framework_id))
        
        # Approve framework
        framework_registry.approve_framework(framework_id)
        self.assertTrue(framework_registry.is_approved(framework_id))
        
        # Verify framework is now available
        frameworks = framework_registry.get_frameworks_by_injection_point("pre_response")
        self.assertGreaterEqual(len(frameworks), 1)
        
        # Clean up
        framework_loader.unload_framework(framework_id)
        if os.path.exists(module_path):
            os.remove(module_path)


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestFrameworkInterface))
    suite.addTests(loader.loadTestsFromTestCase(TestFrameworkBlueprint))
    suite.addTests(loader.loadTestsFromTestCase(TestFrameworkGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestFrameworkLoader))
    suite.addTests(loader.loadTestsFromTestCase(TestFrameworkRegistry))
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEndFrameworkPipeline))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
