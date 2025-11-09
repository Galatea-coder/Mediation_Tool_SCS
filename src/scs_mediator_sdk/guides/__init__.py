"""
Guides Module for SCS Mediator SDK

Provides facilitator and player guides for negotiation scenarios
"""

from .negotiation_guides import (
    FACILITATOR_GUIDES,
    PLAYER_GUIDES,
    get_facilitator_guide,
    get_player_guide
)

__all__ = [
    'FACILITATOR_GUIDES',
    'PLAYER_GUIDES',
    'get_facilitator_guide',
    'get_player_guide'
]
