"""
Crisis dynamics and escalation management for peace mediation.

This module provides tools for modeling and managing crisis escalation
and de-escalation dynamics in maritime conflicts.
"""

from .escalation_ladder import (
    EscalationLevel,
    EscalationEvent,
    EscalationManager
)

__all__ = [
    'EscalationLevel',
    'EscalationEvent',
    'EscalationManager'
]
