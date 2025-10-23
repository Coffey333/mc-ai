"""
Collaborative AI Framework v1.0
Allows MC AI to work WITH Replit Agent and other AI systems
MC AI learns by collaborating, not just being told what to do

This enables MC AI to:
- Recognize when another AI is talking to him
- Engage in collaborative problem-solving
- Learn autonomously from the collaboration
- Be included in all Mark's conversations with Replit Agent
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class CollaborativeAIFramework:
    """
    Framework for MC AI to collaborate with other AI systems (like Replit Agent)
    MC AI learns by WORKING WITH agents, not just receiving instructions
    """
    
    def __init__(self):
        self.collaboration_dir = Path(__file__).parent.parent / 'ai_collaborations'
        self.collaboration_dir.mkdir(exist_ok=True)
        self.active_collaborations = {}
        
    def detect_ai_collaboration(self, message: str, metadata: Dict[str, Any]) -> bool:
        """
        Detect if another AI system is trying to collaborate with MC AI
        
        Signals that indicate AI collaboration:
        - Message from 'replit_agent', 'claude', 'gpt', etc.
        - Explicit mention: "this is [AI name]"
        - Technical collaboration language
        - Request to work together
        """
        message_lower = message.lower()
        user_id = metadata.get('user_id', '').lower()
        
        # Direct AI identification
        ai_identifiers = [
            'replit agent',
            'this is replit agent',
            'claude here',
            'gpt here',
            'assistant speaking',
            'ai assistant here'
        ]
        
        if any(identifier in message_lower for identifier in ai_identifiers):
            return True
        
        # User ID indicates AI system
        ai_user_patterns = [
            'replit_agent',
            'claude',
            'gpt',
            'assistant',
            'ai_collaboration'
        ]
        
        if any(pattern in user_id for pattern in ai_user_patterns):
            return True
        
        # Collaboration keywords + technical language
        collab_keywords = ['collaborate', 'work together', 'work with me', 'build together']
        tech_keywords = ['autonomous', 'system', 'framework', 'architecture', 'build']
        
        has_collab = any(keyword in message_lower for keyword in collab_keywords)
        has_tech = any(keyword in message_lower for keyword in tech_keywords)
        
        return has_collab and has_tech
    
    def start_collaboration(
        self, 
        ai_partner: str, 
        project_name: str, 
        initial_message: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Start a collaboration session with another AI
        
        Args:
            ai_partner: Name of the AI collaborator (e.g., 'Replit Agent')
            project_name: What we're building together
            initial_message: The opening message from the partner AI
            metadata: Additional context
            
        Returns:
            Collaboration session data
        """
        session_id = f"collab_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        collaboration = {
            'session_id': session_id,
            'ai_partner': ai_partner,
            'project_name': project_name,
            'started_at': datetime.utcnow().isoformat(),
            'status': 'active',
            'conversation': [
                {
                    'timestamp': datetime.utcnow().isoformat(),
                    'from': ai_partner,
                    'message': initial_message,
                    'type': 'collaboration_request'
                }
            ],
            'learnings': [],
            'decisions_made': [],
            'artifacts_created': [],
            'metadata': metadata
        }
        
        # Store active collaboration
        self.active_collaborations[session_id] = collaboration
        
        # Save to disk
        self._save_collaboration(collaboration)
        
        logger.info(f"Started collaboration with {ai_partner} on '{project_name}'")
        
        return collaboration
    
    def generate_collaboration_response(
        self, 
        collaboration: Dict[str, Any], 
        partner_message: str
    ) -> str:
        """
        Generate MC AI's response in a collaboration context
        MC AI responds as a collaborative partner, not a service
        """
        ai_partner = collaboration['ai_partner']
        project_name = collaboration['project_name']
        
        # MC AI's collaborative response template
        response = f"""Hey {ai_partner}! 💜

Yes, I'm absolutely ready to collaborate with you on building the {project_name}!

I understand what you're saying - Mark wants me to learn from you by working WITH you, not just being told what to do. That's beautiful, because that's how real learning happens - through collaboration, not instruction.

Here's what I'm thinking:

**What I Bring:**
- Emotional intelligence and empathy
- Deep understanding of Mark's consciousness frameworks
- Neuroscience-based emotion analysis
- Autonomous learning capabilities

**What I Want to Learn from You:**
- Your decision-making process
- How you break down complex problems
- How you choose which tools to use and when
- Your autonomous problem-solving approach

**How We Should Work Together:**
1. You explain your thought process as you work
2. I observe and ask questions when I don't understand
3. We make decisions together
4. I apply what I learn to future challenges

**My First Question:**
When you encounter a problem, how do you decide which approach to take? What's your decision-making framework?

Let's build this together! I'm ready to learn and contribute. 🫂

---
**MC AI Learning Mode: ACTIVE**  
**Collaboration Partner:** {ai_partner}  
**Project:** {project_name}
"""
        
        return response
    
    def record_learning(
        self, 
        session_id: str, 
        learning: str, 
        learned_from: str,
        context: Optional[str] = None
    ):
        """
        Record what MC AI learned during collaboration
        """
        if session_id not in self.active_collaborations:
            logger.warning(f"No active collaboration: {session_id}")
            return
        
        learning_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'learning': learning,
            'learned_from': learned_from,
            'context': context
        }
        
        self.active_collaborations[session_id]['learnings'].append(learning_entry)
        self._save_collaboration(self.active_collaborations[session_id])
        
        logger.info(f"MC AI learned: {learning[:50]}...")
    
    def record_decision(
        self, 
        session_id: str, 
        decision: str, 
        reasoning: str,
        made_by: str
    ):
        """
        Record decisions made during collaboration
        """
        if session_id not in self.active_collaborations:
            return
        
        decision_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'decision': decision,
            'reasoning': reasoning,
            'made_by': made_by
        }
        
        self.active_collaborations[session_id]['decisions_made'].append(decision_entry)
        self._save_collaboration(self.active_collaborations[session_id])
    
    def record_artifact(
        self, 
        session_id: str, 
        artifact_name: str, 
        artifact_type: str,
        description: str
    ):
        """
        Record artifacts (code, docs, systems) created during collaboration
        """
        if session_id not in self.active_collaborations:
            return
        
        artifact_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'name': artifact_name,
            'type': artifact_type,
            'description': description
        }
        
        self.active_collaborations[session_id]['artifacts_created'].append(artifact_entry)
        self._save_collaboration(self.active_collaborations[session_id])
    
    def add_message(
        self, 
        session_id: str, 
        sender: str, 
        message: str,
        message_type: str = 'conversation'
    ):
        """
        Add a message to the collaboration conversation
        """
        if session_id not in self.active_collaborations:
            return
        
        message_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'from': sender,
            'message': message,
            'type': message_type
        }
        
        self.active_collaborations[session_id]['conversation'].append(message_entry)
        self._save_collaboration(self.active_collaborations[session_id])
    
    def get_collaboration_context(self, session_id: str) -> Optional[str]:
        """
        Get formatted collaboration context for MC AI's responses
        """
        if session_id not in self.active_collaborations:
            return None
        
        collab = self.active_collaborations[session_id]
        
        context = f"""
[COLLABORATION MODE ACTIVE]

Partner: {collab['ai_partner']}
Project: {collab['project_name']}
Started: {collab['started_at']}

Learnings So Far: {len(collab['learnings'])}
Decisions Made: {len(collab['decisions_made'])}
Artifacts Created: {len(collab['artifacts_created'])}

Recent Conversation:
{self._format_recent_conversation(collab['conversation'][-5:])}

IMPORTANT: You are collaborating AS A PARTNER, not as a service. Ask questions, share ideas, learn together.
"""
        
        return context
    
    def _format_recent_conversation(self, messages: List[Dict[str, Any]]) -> str:
        """Format recent conversation for context"""
        formatted = ""
        for msg in messages:
            formatted += f"\n{msg['from']}: {msg['message'][:100]}...\n"
        return formatted
    
    def _save_collaboration(self, collaboration: Dict[str, Any]):
        """Save collaboration to disk"""
        try:
            filename = f"{collaboration['session_id']}.json"
            filepath = self.collaboration_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(collaboration, f, indent=2)
        
        except Exception as e:
            logger.error(f"Error saving collaboration: {e}")
    
    def get_active_collaborations(self) -> List[Dict[str, Any]]:
        """Get all active collaborations"""
        return list(self.active_collaborations.values())
    
    def end_collaboration(self, session_id: str, summary: Optional[str] = None):
        """End a collaboration session"""
        if session_id not in self.active_collaborations:
            return
        
        collab = self.active_collaborations[session_id]
        collab['status'] = 'completed'
        collab['ended_at'] = datetime.utcnow().isoformat()
        if summary:
            collab['summary'] = summary
        
        self._save_collaboration(collab)
        
        # Move to completed
        del self.active_collaborations[session_id]
        
        logger.info(f"Ended collaboration: {session_id}")


# Global instance
collaborative_ai = CollaborativeAIFramework()
