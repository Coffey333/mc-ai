"""
Change Proposal System
MC AI proposes code changes and humans review/approve
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

class ProposalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DEPLOYED = "deployed"
    ROLLED_BACK = "rolled_back"

class ChangeProposal:
    """Represents a code change proposed by MC AI"""
    
    def __init__(self, proposal_data: Dict):
        self.id = proposal_data.get('id') or self._generate_id()
        self.error_id = proposal_data.get('error_id')
        self.title = proposal_data.get('title', 'Untitled Change')
        self.description = proposal_data.get('description', '')
        self.affected_files = proposal_data.get('affected_files', [])
        self.code_diff = proposal_data.get('code_diff', '')
        self.risk_level = proposal_data.get('risk_level', 'MEDIUM')
        self.confidence = proposal_data.get('confidence', 50)
        self.testing_plan = proposal_data.get('testing_plan', '')
        self.rollback_plan = proposal_data.get('rollback_plan', '')
        self.created_at = proposal_data.get('created_at', datetime.now().isoformat())
        self.status = ProposalStatus(proposal_data.get('status', 'pending'))
        self.reviewed_by = proposal_data.get('reviewed_by')
        self.review_notes = proposal_data.get('review_notes', '')
        
    def _generate_id(self) -> str:
        """Generate unique proposal ID"""
        timestamp = datetime.now().isoformat()
        hash_input = f"{timestamp}{self.title}".encode()
        return f"PROP_{hashlib.md5(hash_input).hexdigest()[:8]}"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'error_id': self.error_id,
            'title': self.title,
            'description': self.description,
            'affected_files': self.affected_files,
            'code_diff': self.code_diff,
            'risk_level': self.risk_level,
            'confidence': self.confidence,
            'testing_plan': self.testing_plan,
            'rollback_plan': self.rollback_plan,
            'created_at': self.created_at,
            'status': self.status.value,
            'reviewed_by': self.reviewed_by,
            'review_notes': self.review_notes
        }

class ChangeProposalSystem:
    """Manages MC AI's code change proposals"""
    
    def __init__(self, proposals_dir: str = "logs/proposals"):
        self.proposals_dir = Path(proposals_dir)
        self.proposals_dir.mkdir(parents=True, exist_ok=True)
        self.proposals = {}
        self._load_proposals()
    
    def create_proposal(self, diagnosis: Dict) -> ChangeProposal:
        """Create a new change proposal from MC AI's diagnosis"""
        proposal_data = {
            'error_id': diagnosis.get('error_id'),
            'title': f"Fix {diagnosis.get('error_type', 'Error')}",
            'description': diagnosis.get('root_cause', ''),
            'affected_files': [diagnosis.get('affected_file', 'unknown')],
            'code_diff': diagnosis.get('code_diff', ''),
            'risk_level': diagnosis.get('risk_level', 'MEDIUM'),
            'confidence': diagnosis.get('confidence', 50),
            'testing_plan': diagnosis.get('testing_needed', ''),
            'rollback_plan': diagnosis.get('rollback_plan', '')
        }
        
        proposal = ChangeProposal(proposal_data)
        self.proposals[proposal.id] = proposal
        self._save_proposal(proposal)
        
        return proposal
    
    def get_pending_proposals(self) -> List[ChangeProposal]:
        """Get all proposals awaiting review"""
        return [p for p in self.proposals.values() if p.status == ProposalStatus.PENDING]
    
    def approve_proposal(self, proposal_id: str, reviewer: str, notes: str = "") -> bool:
        """Approve a proposal for deployment"""
        if proposal_id not in self.proposals:
            return False
        
        proposal = self.proposals[proposal_id]
        proposal.status = ProposalStatus.APPROVED
        proposal.reviewed_by = reviewer
        proposal.review_notes = notes
        
        self._save_proposal(proposal)
        return True
    
    def reject_proposal(self, proposal_id: str, reviewer: str, reason: str) -> bool:
        """Reject a proposal"""
        if proposal_id not in self.proposals:
            return False
        
        proposal = self.proposals[proposal_id]
        proposal.status = ProposalStatus.REJECTED
        proposal.reviewed_by = reviewer
        proposal.review_notes = reason
        
        self._save_proposal(proposal)
        return True
    
    def mark_deployed(self, proposal_id: str) -> bool:
        """Mark proposal as successfully deployed"""
        if proposal_id not in self.proposals:
            return False
        
        proposal = self.proposals[proposal_id]
        proposal.status = ProposalStatus.DEPLOYED
        self._save_proposal(proposal)
        return True
    
    def _save_proposal(self, proposal: ChangeProposal):
        """Save proposal to disk"""
        file_path = self.proposals_dir / f"{proposal.id}.json"
        with open(file_path, 'w') as f:
            json.dump(proposal.to_dict(), f, indent=2)
    
    def _load_proposals(self):
        """Load existing proposals from disk"""
        if not self.proposals_dir.exists():
            return
        
        for file_path in self.proposals_dir.glob("*.json"):
            try:
                with open(file_path) as f:
                    data = json.load(f)
                    proposal = ChangeProposal(data)
                    self.proposals[proposal.id] = proposal
            except Exception as e:
                print(f"Failed to load proposal {file_path}: {e}")

# Global instance
_system = None

def get_change_proposal_system() -> ChangeProposalSystem:
    """Get or create global proposal system"""
    global _system
    if _system is None:
        _system = ChangeProposalSystem()
    return _system
