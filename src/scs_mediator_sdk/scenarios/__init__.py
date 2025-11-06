"""
Scenario Framework for Generalizable Conflict Simulation

Provides abstraction layer to support multiple conflict domains:
- Territorial disputes (maritime, land borders)
- Resource conflicts (water, energy, fisheries, minerals)
- Ethnic tensions (identity, autonomy, discrimination)
- Political conflicts (power-sharing, governance)
- Economic disputes (trade, investment)
"""

from .templates.base import (
    ConflictDomain,
    ScenarioTemplate,
    ScenarioBuilder
)

__all__ = [
    'ConflictDomain',
    'ScenarioTemplate',
    'ScenarioBuilder',
]
