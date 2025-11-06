"""
Advanced Mediation Simulation SDK - Mediation Process Module

This module implements Moore's 6-Phase Mediation Process and provides
a comprehensive toolkit for conflict resolution simulation and training.

Based on:
- Moore, C. W. (2014). The Mediation Process (4th ed.)
- UN DPPA (2017). Guidance for Effective Mediation
- Fisher & Ury (1981). Getting to Yes
"""

from enum import Enum

__version__ = "9.0.0"
__author__ = "SCS Mediation Training Kit"


class MediationPhase(Enum):
    """Moore's 6-Phase Mediation Process"""
    PHASE_1 = "Initial Contact & Relationship Building"
    PHASE_2 = "Data Collection & Conflict Analysis"
    PHASE_3 = "Problem Definition & Agenda Setting"
    PHASE_4 = "Option Generation & Reality Testing"
    PHASE_5 = "Bargaining & Decision Making"
    PHASE_6 = "Implementation & Monitoring"


__all__ = ['MediationPhase']
