"""
Multiplayer Negotiation Module

Enables multi-user negotiation sessions where human players
represent different stakeholders.
"""

from .session_manager import (
    SessionManager,
    Session,
    Player,
    Proposal,
    Response,
    get_session_manager
)

__all__ = [
    'SessionManager',
    'Session',
    'Player',
    'Proposal',
    'Response',
    'get_session_manager'
]
