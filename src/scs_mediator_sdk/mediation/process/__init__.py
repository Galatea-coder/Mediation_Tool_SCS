"""
Mediation Process Implementation - Phases 1-6

This module provides the core mediation process framework based on
Christopher Moore's 6-phase model for conflict resolution.
"""

from .assessment import (
    ConflictType,
    ReadinessLevel,
    Stakeholder,
    ConflictContext,
    RipenessAssessment,
    PreMediationAssessment
)

from .facilitation import (
    IssueType,
    Issue,
    NegotiationOption,
    AgendaDesigner,
    OptionGenerator
)

__all__ = [
    # Phase 1-2: Assessment
    'ConflictType',
    'ReadinessLevel',
    'Stakeholder',
    'ConflictContext',
    'RipenessAssessment',
    'PreMediationAssessment',
    # Phase 3-4: Facilitation
    'IssueType',
    'Issue',
    'NegotiationOption',
    'AgendaDesigner',
    'OptionGenerator',
]
