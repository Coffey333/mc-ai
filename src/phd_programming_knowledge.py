"""
PhD-Level Programming Knowledge System for MC AI
Comprehensive knowledge across 20+ programming languages and frameworks
Uses verified educational sources (.edu universities, official documentation)
"""

import os
import json
import sqlite3
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class PhDProgrammingKnowledge:
    """
    PhD-level programming knowledge across all major languages and paradigms
    """
    
    def __init__(self, db_path: str = "knowledge_library/programming_knowledge.db"):
        self.db_path = db_path
        self.setup_database()
        
        # Programming language knowledge organized by category
        self.languages = {
            'systems_programming': {
                'C': self._get_c_knowledge(),
                'C++': self._get_cpp_knowledge(),
                'Rust': self._get_rust_knowledge(),
                'Go': self._get_go_knowledge(),
                'Zig': self._get_zig_knowledge()
            },
            'web_backend': {
                'Python': self._get_python_knowledge(),
                'JavaScript': self._get_javascript_knowledge(),
                'TypeScript': self._get_typescript_knowledge(),
                'Ruby': self._get_ruby_knowledge(),
                'PHP': self._get_php_knowledge(),
                'Java': self._get_java_knowledge(),
                'C#': self._get_csharp_knowledge(),
                'Kotlin': self._get_kotlin_knowledge(),
                'Elixir': self._get_elixir_knowledge()
            },
            'web_frontend': {
                'HTML': self._get_html_knowledge(),
                'CSS': self._get_css_knowledge(),
                'JavaScript': self._get_javascript_knowledge(),
                'TypeScript': self._get_typescript_knowledge(),
                'React': self._get_react_knowledge(),
                'Vue': self._get_vue_knowledge(),
                'Angular': self._get_angular_knowledge(),
                'Svelte': self._get_svelte_knowledge()
            },
            'mobile': {
                'Swift': self._get_swift_knowledge(),
                'Kotlin': self._get_kotlin_knowledge(),
                'Dart': self._get_dart_knowledge(),
                'React Native': self._get_react_native_knowledge(),
                'Flutter': self._get_flutter_knowledge()
            },
            'data_science_ml': {
                'Python': self._get_python_ml_knowledge(),
                'R': self._get_r_knowledge(),
                'Julia': self._get_julia_knowledge(),
                'MATLAB': self._get_matlab_knowledge()
            },
            'functional': {
                'Haskell': self._get_haskell_knowledge(),
                'Scala': self._get_scala_knowledge(),
                'Clojure': self._get_clojure_knowledge(),
                'F#': self._get_fsharp_knowledge(),
                'Erlang': self._get_erlang_knowledge()
            },
            'scripting': {
                'Bash': self._get_bash_knowledge(),
                'PowerShell': self._get_powershell_knowledge(),
                'Lua': self._get_lua_knowledge(),
                'Perl': self._get_perl_knowledge()
            },
            'database': {
                'SQL': self._get_sql_knowledge(),
                'PostgreSQL': self._get_postgresql_knowledge(),
                'MySQL': self._get_mysql_knowledge(),
                'MongoDB': self._get_mongodb_knowledge(),
                'Redis': self._get_redis_knowledge()
            }
        }
        
        # Verified educational sources for programming knowledge
        self.verified_sources = {
            'mit_opencourseware': [
                'https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/',
                'https://ocw.mit.edu/courses/intro-programming/',
                'https://ocw.mit.edu/courses/algorithms-data-structures/'
            ],
            'stanford': [
                'https://cs.stanford.edu/',
                'https://web.stanford.edu/class/cs106b/',
                'https://web.stanford.edu/class/cs107/'
            ],
            'official_docs': [
                'https://docs.python.org/',
                'https://developer.mozilla.org/en-US/',
                'https://doc.rust-lang.org/',
                'https://go.dev/doc/',
                'https://www.typescriptlang.org/docs/'
            ]
        }
    
    def setup_database(self):
        """Create database schema for programming knowledge"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Programming knowledge table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS programming_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT NOT NULL,
                category TEXT NOT NULL,
                concept TEXT NOT NULL,
                explanation TEXT NOT NULL,
                example_code TEXT,
                best_practices TEXT,
                common_pitfalls TEXT,
                advanced_techniques TEXT,
                source_url TEXT,
                difficulty_level TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Design patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS design_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT NOT NULL,
                category TEXT NOT NULL,
                intent TEXT NOT NULL,
                applicability TEXT,
                structure TEXT,
                implementation TEXT,
                example_code TEXT,
                consequences TEXT,
                related_patterns TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Architecture patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS architecture_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT NOT NULL,
                description TEXT NOT NULL,
                use_cases TEXT,
                advantages TEXT,
                disadvantages TEXT,
                example_implementation TEXT,
                related_patterns TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_language_expertise(self, language: str, topic: Optional[str] = None) -> Dict:
        """
        Get PhD-level expertise for a specific language
        
        Args:
            language: Programming language name
            topic: Specific topic (optional)
        
        Returns:
            Dict with comprehensive knowledge
        """
        knowledge = self._find_language_knowledge(language)
        
        if not knowledge:
            return {
                'language': language,
                'status': 'not_found',
                'suggestion': 'I can learn this language from verified sources'
            }
        
        # Get from database if available
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if topic:
            cursor.execute('''
                SELECT concept, explanation, example_code, best_practices, 
                       advanced_techniques, source_url
                FROM programming_knowledge
                WHERE language = ? AND concept LIKE ?
            ''', (language, f'%{topic}%'))
        else:
            cursor.execute('''
                SELECT concept, explanation, example_code, best_practices,
                       advanced_techniques, source_url
                FROM programming_knowledge
                WHERE language = ?
                LIMIT 10
            ''', (language,))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            return {
                'language': language,
                'knowledge_base': [
                    {
                        'concept': row[0],
                        'explanation': row[1],
                        'example': row[2],
                        'best_practices': row[3],
                        'advanced_techniques': row[4],
                        'source': row[5]
                    }
                    for row in results
                ],
                'foundational_knowledge': knowledge
            }
        
        return {
            'language': language,
            'foundational_knowledge': knowledge
        }
    
    def _find_language_knowledge(self, language: str) -> Optional[Dict]:
        """Find language knowledge across all categories"""
        for category, langs in self.languages.items():
            if language in langs:
                return langs[language]
        return None
    
    # Knowledge base methods for each language
    def _get_python_knowledge(self) -> Dict:
        return {
            'paradigms': ['Object-Oriented', 'Functional', 'Procedural', 'Imperative'],
            'core_concepts': {
                'data_structures': ['list', 'dict', 'set', 'tuple', 'frozenset', 'deque', 'defaultdict'],
                'advanced_features': ['decorators', 'generators', 'context_managers', 'metaclasses', 'descriptors'],
                'concurrency': ['threading', 'multiprocessing', 'asyncio', 'concurrent.futures'],
                'memory_management': ['garbage_collection', 'reference_counting', 'memory_profiling']
            },
            'frameworks': {
                'web': ['Django', 'Flask', 'FastAPI', 'Tornado'],
                'data_science': ['NumPy', 'Pandas', 'SciPy', 'scikit-learn'],
                'ml_dl': ['TensorFlow', 'PyTorch', 'Keras', 'JAX'],
                'testing': ['pytest', 'unittest', 'doctest', 'hypothesis']
            },
            'best_practices': [
                'Follow PEP 8 style guide',
                'Use type hints (Python 3.5+)',
                'Prefer composition over inheritance',
                'Use context managers for resource management',
                'Write comprehensive docstrings',
                'Use virtual environments',
                'Leverage list comprehensions and generator expressions'
            ],
            'advanced_techniques': [
                'Metaclass programming for framework creation',
                'Descriptor protocol for attribute access control',
                'Abstract base classes for interface definition',
                'Function decorators for cross-cutting concerns',
                'Coroutines and async/await for concurrent operations',
                'Memory-mapped files for large data processing',
                'C extensions for performance-critical code'
            ],
            'performance': {
                'profiling_tools': ['cProfile', 'line_profiler', 'memory_profiler', 'py-spy'],
                'optimization': ['use numpy for numerical operations', 'cython for speedups', 'numba for JIT compilation']
            }
        }
    
    def _get_javascript_knowledge(self) -> Dict:
        return {
            'paradigms': ['Object-Oriented', 'Functional', 'Event-Driven', 'Prototypal'],
            'core_concepts': {
                'fundamentals': ['closures', 'hoisting', 'event_loop', 'promises', 'async_await'],
                'es6_plus': ['arrow_functions', 'destructuring', 'spread_operator', 'modules', 'classes'],
                'advanced': ['prototypal_inheritance', 'this_binding', 'call_apply_bind', 'generators', 'proxies']
            },
            'frameworks': {
                'frontend': ['React', 'Vue', 'Angular', 'Svelte'],
                'backend': ['Node.js', 'Express', 'NestJS', 'Fastify'],
                'fullstack': ['Next.js', 'Nuxt.js', 'SvelteKit']
            },
            'best_practices': [
                'Use strict mode',
                'Avoid global variables',
                'Use const/let instead of var',
                'Handle errors properly with try/catch',
                'Use async/await for asynchronous operations',
                'Avoid callback hell',
                'Use ESLint for code quality'
            ],
            'advanced_techniques': [
                'Functional programming patterns (map, filter, reduce)',
                'Currying and partial application',
                'Memoization for performance',
                'Web Workers for multi-threading',
                'Service Workers for PWAs',
                'WebAssembly integration for performance'
            ]
        }
    
    def _get_rust_knowledge(self) -> Dict:
        return {
            'paradigms': ['Systems', 'Functional', 'Concurrent', 'Memory-Safe'],
            'core_concepts': {
                'ownership': ['borrowing', 'lifetimes', 'move_semantics'],
                'memory_safety': ['no_null', 'no_data_races', 'safe_concurrency'],
                'advanced': ['traits', 'generics', 'macros', 'unsafe_code']
            },
            'best_practices': [
                'Leverage ownership system for memory safety',
                'Use Result and Option types instead of exceptions',
                'Prefer iterators over manual loops',
                'Use cargo for dependency management',
                'Write comprehensive tests',
                'Minimize unsafe code blocks'
            ],
            'advanced_techniques': [
                'Zero-cost abstractions',
                'Procedural macros for code generation',
                'Pin and Unpin for self-referential structures',
                'Phantom data for compile-time guarantees',
                'Lock-free concurrency with atomics'
            ]
        }
    
    def _get_c_knowledge(self) -> Dict:
        return {
            'paradigms': ['Procedural', 'Imperative', 'Low-Level'],
            'core_concepts': {
                'memory': ['pointers', 'malloc_free', 'stack_heap', 'memory_leaks'],
                'advanced': ['function_pointers', 'void_pointers', 'unions', 'bit_manipulation']
            },
            'best_practices': [
                'Always free allocated memory',
                'Check return values',
                'Use const for read-only data',
                'Avoid buffer overflows',
                'Use valgrind for memory debugging'
            ]
        }
    
    def _get_cpp_knowledge(self) -> Dict:
        return {
            'paradigms': ['Object-Oriented', 'Generic', 'Procedural', 'Functional'],
            'core_concepts': {
                'modern_cpp': ['smart_pointers', 'move_semantics', 'lambda_expressions', 'constexpr'],
                'templates': ['generic_programming', 'template_metaprogramming', 'SFINAE', 'concepts'],
                'stl': ['containers', 'algorithms', 'iterators', 'function_objects']
            },
            'best_practices': [
                'Use RAII for resource management',
                'Prefer unique_ptr over raw pointers',
                'Use std::move for ownership transfer',
                'Leverage const correctness',
                'Follow Rule of Five/Zero'
            ]
        }
    
    def _get_go_knowledge(self) -> Dict:
        return {
            'paradigms': ['Concurrent', 'Compiled', 'Statically-Typed'],
            'core_concepts': {
                'concurrency': ['goroutines', 'channels', 'select_statement', 'sync_package'],
                'interfaces': ['implicit_implementation', 'empty_interface', 'type_assertions'],
                'error_handling': ['error_interface', 'panic_recover', 'custom_errors']
            },
            'best_practices': [
                'Handle errors explicitly',
                'Use goroutines for concurrency',
                'Close channels when done',
                'Use defer for cleanup',
                'Follow effective Go guidelines'
            ]
        }
    
    def _get_typescript_knowledge(self) -> Dict:
        return {
            'paradigms': ['Object-Oriented', 'Functional', 'Typed-JavaScript'],
            'core_concepts': {
                'type_system': ['interfaces', 'type_aliases', 'generics', 'union_types', 'intersection_types'],
                'advanced': ['conditional_types', 'mapped_types', 'template_literal_types', 'decorators']
            },
            'best_practices': [
                'Enable strict mode',
                'Use interfaces for object shapes',
                'Leverage type inference',
                'Avoid any type',
                'Use utility types'
            ]
        }
    
    # Placeholder methods for other languages (to be expanded)
    def _get_ruby_knowledge(self) -> Dict:
        return {'paradigms': ['Object-Oriented', 'Functional'], 'status': 'basic_knowledge'}
    
    def _get_php_knowledge(self) -> Dict:
        return {'paradigms': ['Object-Oriented', 'Procedural'], 'status': 'basic_knowledge'}
    
    def _get_java_knowledge(self) -> Dict:
        return {'paradigms': ['Object-Oriented', 'Concurrent'], 'status': 'basic_knowledge'}
    
    def _get_csharp_knowledge(self) -> Dict:
        return {'paradigms': ['Object-Oriented', 'Functional'], 'status': 'basic_knowledge'}
    
    def _get_kotlin_knowledge(self) -> Dict:
        return {'paradigms': ['Object-Oriented', 'Functional'], 'status': 'basic_knowledge'}
    
    def _get_elixir_knowledge(self) -> Dict:
        return {'paradigms': ['Functional', 'Concurrent'], 'status': 'basic_knowledge'}
    
    def _get_html_knowledge(self) -> Dict:
        return {'type': 'markup', 'status': 'basic_knowledge'}
    
    def _get_css_knowledge(self) -> Dict:
        return {'type': 'styling', 'status': 'basic_knowledge'}
    
    def _get_react_knowledge(self) -> Dict:
        return {'type': 'framework', 'status': 'basic_knowledge'}
    
    def _get_vue_knowledge(self) -> Dict:
        return {'type': 'framework', 'status': 'basic_knowledge'}
    
    def _get_angular_knowledge(self) -> Dict:
        return {'type': 'framework', 'status': 'basic_knowledge'}
    
    def _get_svelte_knowledge(self) -> Dict:
        return {'type': 'framework', 'status': 'basic_knowledge'}
    
    def _get_swift_knowledge(self) -> Dict:
        return {'paradigms': ['Object-Oriented', 'Functional'], 'status': 'basic_knowledge'}
    
    def _get_dart_knowledge(self) -> Dict:
        return {'paradigms': ['Object-Oriented'], 'status': 'basic_knowledge'}
    
    def _get_react_native_knowledge(self) -> Dict:
        return {'type': 'framework', 'status': 'basic_knowledge'}
    
    def _get_flutter_knowledge(self) -> Dict:
        return {'type': 'framework', 'status': 'basic_knowledge'}
    
    def _get_python_ml_knowledge(self) -> Dict:
        return {'focus': 'machine_learning', 'status': 'basic_knowledge'}
    
    def _get_r_knowledge(self) -> Dict:
        return {'paradigms': ['Functional', 'Statistical'], 'status': 'basic_knowledge'}
    
    def _get_julia_knowledge(self) -> Dict:
        return {'paradigms': ['Functional', 'Scientific'], 'status': 'basic_knowledge'}
    
    def _get_matlab_knowledge(self) -> Dict:
        return {'type': 'numerical_computing', 'status': 'basic_knowledge'}
    
    def _get_haskell_knowledge(self) -> Dict:
        return {'paradigms': ['Functional', 'Pure'], 'status': 'basic_knowledge'}
    
    def _get_scala_knowledge(self) -> Dict:
        return {'paradigms': ['Functional', 'Object-Oriented'], 'status': 'basic_knowledge'}
    
    def _get_clojure_knowledge(self) -> Dict:
        return {'paradigms': ['Functional', 'Lisp'], 'status': 'basic_knowledge'}
    
    def _get_fsharp_knowledge(self) -> Dict:
        return {'paradigms': ['Functional'], 'status': 'basic_knowledge'}
    
    def _get_erlang_knowledge(self) -> Dict:
        return {'paradigms': ['Functional', 'Concurrent'], 'status': 'basic_knowledge'}
    
    def _get_bash_knowledge(self) -> Dict:
        return {'type': 'shell_scripting', 'status': 'basic_knowledge'}
    
    def _get_powershell_knowledge(self) -> Dict:
        return {'type': 'shell_scripting', 'status': 'basic_knowledge'}
    
    def _get_lua_knowledge(self) -> Dict:
        return {'paradigms': ['Scripting', 'Embedded'], 'status': 'basic_knowledge'}
    
    def _get_perl_knowledge(self) -> Dict:
        return {'paradigms': ['Scripting', 'Text-Processing'], 'status': 'basic_knowledge'}
    
    def _get_sql_knowledge(self) -> Dict:
        return {'type': 'database_query', 'status': 'basic_knowledge'}
    
    def _get_postgresql_knowledge(self) -> Dict:
        return {'type': 'relational_database', 'status': 'basic_knowledge'}
    
    def _get_mysql_knowledge(self) -> Dict:
        return {'type': 'relational_database', 'status': 'basic_knowledge'}
    
    def _get_mongodb_knowledge(self) -> Dict:
        return {'type': 'document_database', 'status': 'basic_knowledge'}
    
    def _get_redis_knowledge(self) -> Dict:
        return {'type': 'key_value_store', 'status': 'basic_knowledge'}
    
    def _get_zig_knowledge(self) -> Dict:
        return {'paradigms': ['Systems', 'Low-Level'], 'status': 'basic_knowledge'}
