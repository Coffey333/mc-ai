"""
Evolution Orchestrator
Main controller for MC AI's self-evolution system
"""

import asyncio
from typing import Dict, List, Optional
from .monitors.live_error_monitor import get_live_error_monitor
from .diagnosis.self_diagnosis_engine import get_self_diagnosis_engine
from .proposals.change_proposal_system import get_change_proposal_system
from .sandbox.sandbox_environment import get_sandbox_environment
from .security.security_scanner import get_security_scanner
from .deployment.safe_deployment import get_safe_deployment

class EvolutionOrchestrator:
    """
    Coordinates MC AI's self-evolution process
    """
    
    def __init__(self, llm_client=None):
        self.error_monitor = get_live_error_monitor()
        self.diagnosis_engine = get_self_diagnosis_engine(llm_client)
        self.proposal_system = get_change_proposal_system()
        self.sandbox = get_sandbox_environment()
        self.security = get_security_scanner()
        self.deployment = get_safe_deployment()
        
    async def auto_diagnose_errors(self) -> List[Dict]:
        """
        MC AI automatically diagnoses recent errors
        
        Returns list of diagnoses with proposals
        """
        # Get recent errors
        recent_errors = self.error_monitor.get_recent_errors(limit=10)
        
        if not recent_errors:
            return []
        
        diagnoses = []
        
        for error in recent_errors:
            # MC AI analyzes the error
            diagnosis = await self.diagnosis_engine.diagnose_error(error)
            
            # Only create proposal if confidence is high enough
            if diagnosis.get('confidence', 0) >= 60:
                proposal = self.proposal_system.create_proposal(diagnosis)
                diagnosis['proposal_id'] = proposal.id
            
            diagnoses.append(diagnosis)
        
        return diagnoses
    
    async def test_proposal_in_sandbox(self, proposal_id: str) -> Dict:
        """
        Test a proposal in isolated sandbox
        
        Returns test results
        """
        proposal = self.proposal_system.proposals.get(proposal_id)
        
        if not proposal:
            return {'error': 'Proposal not found'}
        
        # Create sandbox
        sandbox = self.sandbox.create_sandbox(proposal_id)
        
        if 'error' in sandbox:
            return sandbox
        
        sandbox_id = sandbox['sandbox_id']
        
        try:
            # Apply changes to sandbox
            for file_path in proposal.affected_files:
                # Extract new code from code_diff
                # (In production, this would parse the diff properly)
                self.sandbox.apply_changes(sandbox_id, file_path, proposal.code_diff)
            
            # Run security scan
            security_result = self.security.scan_code(proposal.code_diff, proposal.affected_files[0])
            
            # Run automated tests
            test_results = self.sandbox.run_tests(sandbox_id)
            
            # Combine results
            results = {
                'sandbox_id': sandbox_id,
                'security_scan': security_result,
                'automated_tests': test_results,
                'ready_for_deployment': (
                    security_result['safe'] and 
                    test_results['passed']
                )
            }
            
            # Cleanup sandbox
            self.sandbox.cleanup_sandbox(sandbox_id)
            
            return results
            
        except Exception as e:
            self.sandbox.cleanup_sandbox(sandbox_id)
            return {'error': f'Testing failed: {e}'}
    
    async def deploy_approved_proposal(self, proposal_id: str, reviewer: str) -> Dict:
        """
        Deploy an approved proposal to production
        
        Returns deployment result
        """
        proposal = self.proposal_system.proposals.get(proposal_id)
        
        if not proposal:
            return {'error': 'Proposal not found'}
        
        # Verify it's approved
        if proposal.status.value != 'approved':
            return {'error': 'Proposal not approved'}
        
        # Prepare file changes
        file_changes = {}
        for file_path in proposal.affected_files:
            # In production, extract actual changes from diff
            file_changes[file_path] = proposal.code_diff
        
        # Deploy
        deployment_result = self.deployment.deploy_changes(proposal_id, file_changes)
        
        if deployment_result['success']:
            # Mark as deployed
            self.proposal_system.mark_deployed(proposal_id)
            
            # Mark errors as resolved
            if proposal.error_id:
                self.error_monitor.clear_resolved([proposal.error_id])
        
        return deployment_result
    
    def get_evolution_stats(self) -> Dict:
        """Get overall evolution statistics"""
        error_stats = self.error_monitor.get_statistics()
        proposals = self.proposal_system.proposals.values()
        
        return {
            'errors': error_stats,
            'proposals': {
                'total': len(proposals),
                'pending': len([p for p in proposals if p.status.value == 'pending']),
                'approved': len([p for p in proposals if p.status.value == 'approved']),
                'deployed': len([p for p in proposals if p.status.value == 'deployed']),
                'rejected': len([p for p in proposals if p.status.value == 'rejected'])
            },
            'fix_success_rate': self.diagnosis_engine.get_success_rate(),
            'deployments': len(self.deployment.deployment_history)
        }

# Global instance
_orchestrator = None

def get_evolution_orchestrator(llm_client=None) -> EvolutionOrchestrator:
    """Get or create global orchestrator"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = EvolutionOrchestrator(llm_client)
    return _orchestrator
