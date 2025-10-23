"""
Security Scanner
Scans proposed code changes for security vulnerabilities
"""

import re
from typing import Dict, List
from pathlib import Path

class SecurityScanner:
    """
    Scans MC AI's proposed changes for security risks
    """
    
    def __init__(self):
        # Security patterns to detect
        self.security_patterns = {
            'sql_injection': [
                r'execute\s*\([^)]*\+[^)]*\)',  # String concatenation in SQL
                r'raw\s*\([^)]*\%[^)]*\)',  # String formatting in SQL
            ],
            'command_injection': [
                r'os\.system\s*\([^)]*\+',  # Command injection via os.system
                r'subprocess\.(call|run|Popen)\s*\([^)]*\+',  # Unsafe subprocess
            ],
            'path_traversal': [
                r'open\s*\([^)]*\.\.[^)]*\)',  # Path traversal in file operations
                r'Path\s*\([^)]*\.\.[^)]*\)',
            ],
            'hardcoded_secrets': [
                r'password\s*=\s*["\'][^"\']+["\']',  # Hardcoded passwords
                r'api_key\s*=\s*["\'][^"\']+["\']',  # Hardcoded API keys
                r'secret\s*=\s*["\'][^"\']+["\']',
            ],
            'unsafe_eval': [
                r'\beval\s*\(',  # Use of eval()
                r'\bexec\s*\(',  # Use of exec()
            ],
            'unsafe_pickle': [
                r'pickle\.loads?\s*\(',  # Pickle deserialization
            ],
        }
        
        # Allowed imports (whitelist)
        self.safe_imports = [
            'os', 'sys', 'json', 'time', 'datetime', 'pathlib',
            'typing', 'dataclasses', 'enum', 'collections',
            'flask', 'requests', 'numpy', 'pandas',
            'PIL', 'matplotlib', 'scipy'
        ]
        
    def scan_code(self, code: str, file_path: str = "") -> Dict:
        """
        Scan code for security vulnerabilities
        
        Returns:
        {
            'safe': bool,
            'vulnerabilities': List[Dict],
            'risk_score': int (0-100),
            'recommendations': List[str]
        }
        """
        vulnerabilities = []
        
        # Check for security patterns
        for vuln_type, patterns in self.security_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)
                for match in matches:
                    line_num = code[:match.start()].count('\n') + 1
                    vulnerabilities.append({
                        'type': vuln_type,
                        'line': line_num,
                        'code': match.group(),
                        'severity': self._get_severity(vuln_type)
                    })
        
        # Check imports
        import_vulns = self._check_imports(code)
        vulnerabilities.extend(import_vulns)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(vulnerabilities)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(vulnerabilities)
        
        return {
            'safe': risk_score < 30,  # Safe if risk score below 30
            'vulnerabilities': vulnerabilities,
            'risk_score': risk_score,
            'recommendations': recommendations,
            'scanned_file': file_path
        }
    
    def _check_imports(self, code: str) -> List[Dict]:
        """Check for suspicious imports"""
        vulnerabilities = []
        
        # Dangerous imports
        dangerous_imports = ['subprocess', 'os.system', 'eval', 'exec', '__import__']
        
        import_pattern = r'(?:from\s+(\S+)\s+)?import\s+([^;\n]+)'
        matches = re.finditer(import_pattern, code)
        
        for match in matches:
            module = match.group(1) or match.group(2).split()[0]
            
            if any(danger in module for danger in dangerous_imports):
                line_num = code[:match.start()].count('\n') + 1
                vulnerabilities.append({
                    'type': 'suspicious_import',
                    'line': line_num,
                    'code': match.group(),
                    'severity': 'MEDIUM'
                })
        
        return vulnerabilities
    
    def _get_severity(self, vuln_type: str) -> str:
        """Get severity level for vulnerability type"""
        high_severity = ['sql_injection', 'command_injection', 'unsafe_eval']
        medium_severity = ['path_traversal', 'hardcoded_secrets']
        
        if vuln_type in high_severity:
            return 'HIGH'
        elif vuln_type in medium_severity:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _calculate_risk_score(self, vulnerabilities: List[Dict]) -> int:
        """Calculate overall risk score (0-100)"""
        if not vulnerabilities:
            return 0
        
        severity_scores = {
            'HIGH': 30,
            'MEDIUM': 15,
            'LOW': 5
        }
        
        total_score = sum(severity_scores.get(v['severity'], 0) for v in vulnerabilities)
        return min(total_score, 100)
    
    def _generate_recommendations(self, vulnerabilities: List[Dict]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        vuln_types = set(v['type'] for v in vulnerabilities)
        
        if 'sql_injection' in vuln_types:
            recommendations.append("Use parameterized queries instead of string concatenation")
        
        if 'command_injection' in vuln_types:
            recommendations.append("Avoid os.system() - use subprocess with list arguments")
        
        if 'hardcoded_secrets' in vuln_types:
            recommendations.append("Use environment variables for secrets")
        
        if 'unsafe_eval' in vuln_types:
            recommendations.append("Avoid eval() and exec() - use safer alternatives")
        
        return recommendations

# Global instance
_scanner = None

def get_security_scanner() -> SecurityScanner:
    """Get or create global security scanner"""
    global _scanner
    if _scanner is None:
        _scanner = SecurityScanner()
    return _scanner
