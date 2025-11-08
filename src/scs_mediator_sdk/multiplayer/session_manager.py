"""
Multiplayer Session Manager

Manages multi-user negotiation sessions with session codes, player connections,
proposals, and responses.

MVP Version: In-memory state (no database)
Future: Can be upgraded to SQLite/PostgreSQL
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import random
import string


def generate_session_code() -> str:
    """Generate a unique session code (e.g., 'REEF-2024')"""
    words = ['REEF', 'WAVE', 'TIDE', 'SAIL', 'CALM', 'BLUE', 'DEEP', 'SHIP', 'PORT', 'COAST']
    word = random.choice(words)
    number = random.randint(1000, 9999)
    return f"{word}-{number}"


@dataclass
class Player:
    """Represents a player in the session"""
    player_id: str
    role: str  # 'PH_GOV', 'PRC_MARITIME', 'VN_CG', 'MY_CG'
    user_name: str
    connected: bool = True
    ready: bool = False
    last_active: datetime = field(default_factory=datetime.now)


@dataclass
class Proposal:
    """Represents an agreement proposal"""
    proposal_id: str
    round_number: int
    proposer_id: str  # 'facilitator' or player_id
    proposal_data: Dict[str, Any]  # Agreement terms
    status: str = 'pending'  # 'pending', 'accepted', 'rejected', 'mixed'
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Response:
    """Represents a player's response to a proposal"""
    response_id: str
    proposal_id: str
    player_id: str
    response_type: str  # 'accept', 'reject', 'conditional'
    explanation: str = ""
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Session:
    """Represents a negotiation session"""
    session_id: str
    session_code: str
    facilitator_id: str
    scenario_id: str
    status: str = 'setup'  # 'setup', 'negotiating', 'simulating', 'completed'
    current_round: int = 0
    players: Dict[str, Player] = field(default_factory=dict)
    proposals: List[Proposal] = field(default_factory=list)
    responses: Dict[str, List[Response]] = field(default_factory=dict)
    simulation_results: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class SessionManager:
    """Manages all negotiation sessions"""

    def __init__(self):
        """Initialize session manager with in-memory storage"""
        self.sessions: Dict[str, Session] = {}  # session_id -> Session
        self.session_codes: Dict[str, str] = {}  # session_code -> session_id

    def create_session(self, facilitator_id: str, scenario_id: str) -> tuple[str, str]:
        """
        Create a new session

        Args:
            facilitator_id: ID of the facilitator
            scenario_id: Scenario identifier (e.g., 'scenario_A')

        Returns:
            Tuple of (session_id, session_code)
        """
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
        session_code = generate_session_code()

        # Ensure unique code
        while session_code in self.session_codes:
            session_code = generate_session_code()

        session = Session(
            session_id=session_id,
            session_code=session_code,
            facilitator_id=facilitator_id,
            scenario_id=scenario_id
        )

        self.sessions[session_id] = session
        self.session_codes[session_code] = session_id

        return session_id, session_code

    def get_session_by_code(self, session_code: str) -> Optional[Session]:
        """Get session by its code"""
        session_id = self.session_codes.get(session_code)
        if session_id:
            return self.sessions.get(session_id)
        return None

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        return self.sessions.get(session_id)

    def join_session(self, session_code: str, user_name: str, role: str) -> tuple[bool, str, Optional[str]]:
        """
        Player joins a session

        Args:
            session_code: Session code to join
            user_name: Player's display name
            role: Role to play ('PH_GOV', 'PRC_MARITIME', etc.)

        Returns:
            Tuple of (success, message, player_id)
        """
        session = self.get_session_by_code(session_code)

        if not session:
            return False, "Session not found", None

        # Check if role is already taken
        for player in session.players.values():
            if player.role == role:
                return False, f"Role {role} is already taken", None

        # Create player
        player_id = f"player_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(100, 999)}"
        player = Player(
            player_id=player_id,
            role=role,
            user_name=user_name
        )

        session.players[player_id] = player
        session.updated_at = datetime.now()

        return True, f"Joined as {role}", player_id

    def set_player_ready(self, session_id: str, player_id: str, ready: bool = True) -> bool:
        """Mark player as ready to begin negotiation"""
        session = self.get_session(session_id)
        if not session or player_id not in session.players:
            return False

        session.players[player_id].ready = ready
        session.updated_at = datetime.now()
        return True

    def all_players_ready(self, session_id: str) -> bool:
        """Check if all players are ready"""
        session = self.get_session(session_id)
        if not session or len(session.players) < 2:
            return False

        return all(player.ready for player in session.players.values())

    def start_negotiation(self, session_id: str) -> bool:
        """Start the negotiation phase"""
        session = self.get_session(session_id)
        if not session:
            return False

        if not self.all_players_ready(session_id):
            return False

        session.status = 'negotiating'
        session.current_round = 1
        session.updated_at = datetime.now()
        return True

    def submit_proposal(self, session_id: str, proposer_id: str, proposal_data: Dict[str, Any]) -> Optional[str]:
        """
        Submit a new proposal

        Args:
            session_id: Session ID
            proposer_id: 'facilitator' or player_id
            proposal_data: Agreement terms

        Returns:
            proposal_id if successful, None otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return None

        proposal_id = f"proposal_{session_id}_{session.current_round}_{datetime.now().strftime('%H%M%S')}"

        proposal = Proposal(
            proposal_id=proposal_id,
            round_number=session.current_round,
            proposer_id=proposer_id,
            proposal_data=proposal_data
        )

        session.proposals.append(proposal)
        session.responses[proposal_id] = []
        session.updated_at = datetime.now()

        return proposal_id

    def submit_response(self, session_id: str, proposal_id: str, player_id: str,
                       response_type: str, explanation: str = "") -> bool:
        """
        Player submits response to a proposal

        Args:
            session_id: Session ID
            proposal_id: Proposal ID
            player_id: Player ID
            response_type: 'accept', 'reject', 'conditional'
            explanation: Optional explanation text

        Returns:
            True if successful
        """
        session = self.get_session(session_id)
        if not session or proposal_id not in session.responses:
            return False

        # Check if player already responded
        for resp in session.responses[proposal_id]:
            if resp.player_id == player_id:
                return False  # Already responded

        response_id = f"response_{proposal_id}_{player_id}"
        response = Response(
            response_id=response_id,
            proposal_id=proposal_id,
            player_id=player_id,
            response_type=response_type,
            explanation=explanation
        )

        session.responses[proposal_id].append(response)
        session.updated_at = datetime.now()

        # Check if all players responded
        if self.all_players_responded(session_id, proposal_id):
            self._update_proposal_status(session_id, proposal_id)

        return True

    def all_players_responded(self, session_id: str, proposal_id: str) -> bool:
        """Check if all players have responded to a proposal"""
        session = self.get_session(session_id)
        if not session or proposal_id not in session.responses:
            return False

        responses = session.responses[proposal_id]
        return len(responses) == len(session.players)

    def _update_proposal_status(self, session_id: str, proposal_id: str):
        """Update proposal status based on responses"""
        session = self.get_session(session_id)
        if not session:
            return

        responses = session.responses[proposal_id]
        accept_count = sum(1 for r in responses if r.response_type == 'accept')

        # Find proposal
        proposal = None
        for p in session.proposals:
            if p.proposal_id == proposal_id:
                proposal = p
                break

        if not proposal:
            return

        if accept_count == len(responses):
            proposal.status = 'accepted'
            session.status = 'simulating'  # Ready to simulate
        elif accept_count == 0:
            proposal.status = 'rejected'
        else:
            proposal.status = 'mixed'

    def get_latest_proposal(self, session_id: str) -> Optional[Proposal]:
        """Get the most recent proposal"""
        session = self.get_session(session_id)
        if not session or not session.proposals:
            return None

        return session.proposals[-1]

    def get_proposal_responses(self, session_id: str, proposal_id: str) -> List[Response]:
        """Get all responses for a proposal"""
        session = self.get_session(session_id)
        if not session or proposal_id not in session.responses:
            return []

        return session.responses[proposal_id]

    def save_simulation_results(self, session_id: str, results: Dict[str, Any]) -> bool:
        """Save simulation results"""
        session = self.get_session(session_id)
        if not session:
            return False

        session.simulation_results = results
        session.status = 'completed'
        session.updated_at = datetime.now()
        return True

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get session summary for display"""
        session = self.get_session(session_id)
        if not session:
            return {}

        return {
            'session_id': session.session_id,
            'session_code': session.session_code,
            'scenario_id': session.scenario_id,
            'status': session.status,
            'current_round': session.current_round,
            'players': [
                {
                    'player_id': p.player_id,
                    'role': p.role,
                    'user_name': p.user_name,
                    'connected': p.connected,
                    'ready': p.ready
                }
                for p in session.players.values()
            ],
            'latest_proposal': self.get_latest_proposal(session_id),
            'simulation_results': session.simulation_results
        }


# Global session manager instance (singleton for MVP)
_session_manager = None

def get_session_manager() -> SessionManager:
    """Get the global session manager instance"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
