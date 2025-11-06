"""
Multi-track diplomacy and regional architecture for peace mediation.

This module provides tools for coordinating different diplomatic tracks
and managing third-party involvement in peace processes.
"""

from .multi_track import (
    DiplomaticTrack,
    TrackActivity,
    MultiTrackMediator,
    create_scs_track_2_workshop
)

__all__ = [
    'DiplomaticTrack',
    'TrackActivity',
    'MultiTrackMediator',
    'create_scs_track_2_workshop'
]
