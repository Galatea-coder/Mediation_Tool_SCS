"""
Base Scenario Template Framework

Provides generalization layer to abstract away domain-specific logic
and enable simulation of diverse conflict types.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import json


class ConflictDomain(Enum):
    """High-level conflict domains"""
    MARITIME = "maritime"  # Sea boundaries, fisheries, navigation
    LAND_BORDER = "land_border"  # Territorial disputes on land
    RESOURCE = "resource"  # Water, energy, minerals
    ETHNIC = "ethnic"  # Identity-based conflicts
    POLITICAL = "political"  # Power-sharing, governance
    ECONOMIC = "economic"  # Trade, investment, debt
    INTERNAL = "internal"  # Civil conflicts, separatist movements
    INTERNATIONAL = "international"  # Interstate disputes


@dataclass
class IssueDefinition:
    """
    Abstract definition of a negotiable issue
    Domain-agnostic representation
    """
    issue_id: str
    display_name: str
    description: str

    # Value specification
    value_type: str  # numeric, categorical, boolean, composite
    value_range: Optional[tuple] = None  # For numeric
    value_options: Optional[List[str]] = None  # For categorical

    # Semantic meaning
    domain_mapping: Dict[str, str] = field(default_factory=dict)  # Domain-specific interpretations

    # Utility function parameters
    parties_affected: List[str] = field(default_factory=list)
    utility_weights: Dict[str, float] = field(default_factory=dict)  # party_id -> weight

    # UI presentation
    widget_type: str = "slider"  # slider, select, checkbox, text
    widget_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PartyProfile:
    """
    Abstract party/stakeholder profile
    Domain-agnostic representation
    """
    party_id: str
    display_name: str
    party_type: str  # government, rebel, civil_society, business, regional_org

    # Interests and constraints
    primary_interests: List[str] = field(default_factory=list)
    secondary_interests: List[str] = field(default_factory=list)
    red_lines: List[str] = field(default_factory=list)

    # Capabilities
    power_level: float = 0.5
    legitimacy: float = 0.5
    resources: Dict[str, float] = field(default_factory=dict)

    # Cultural context
    culture_type: str = "individualist"  # or collectivist
    face_sensitivity: float = 0.5
    time_orientation: str = "short-term"  # or long-term

    # Game theory parameters
    batna_value: float = 0.3
    risk_attitude: float = 0.88
    loss_aversion: float = 2.25


@dataclass
class ContextParameters:
    """
    Environmental and contextual factors
    Domain-agnostic representation
    """
    # Temporal factors
    conflict_duration_months: int = 12
    time_pressure: float = 0.5
    seasonal_factors: Dict[str, Any] = field(default_factory=dict)

    # External factors
    media_attention: float = 0.5
    international_pressure: float = 0.5
    economic_interdependence: float = 0.5

    # Escalation dynamics
    recent_incidents: List[Dict[str, Any]] = field(default_factory=list)
    escalation_risk: float = 0.5
    de_escalation_opportunities: List[str] = field(default_factory=list)

    # Domain-specific context
    custom_parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ScenarioTemplate:
    """
    Complete scenario specification
    Domain-agnostic framework that can be instantiated for any conflict type
    """
    scenario_id: str
    name: str
    description: str
    domain: ConflictDomain

    # Core components
    parties: Dict[str, PartyProfile] = field(default_factory=dict)
    issues: Dict[str, IssueDefinition] = field(default_factory=dict)
    context: ContextParameters = field(default_factory=ContextParameters)

    # Feature extraction
    feature_extractors: Dict[str, Callable] = field(default_factory=dict)
    # Maps agreement vector to abstract features (safety, fairness, sustainability, etc.)

    # Simulation parameters
    agent_behaviors: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    incident_generators: List[Callable] = field(default_factory=list)

    # Pedagogical metadata
    learning_objectives: List[str] = field(default_factory=list)
    difficulty_level: str = "intermediate"  # novice, intermediate, expert
    estimated_duration_minutes: int = 60

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'scenario_id': self.scenario_id,
            'name': self.name,
            'description': self.description,
            'domain': self.domain.value,
            'parties': {pid: vars(p) for pid, p in self.parties.items()},
            'issues': {iid: vars(i) for iid, i in self.issues.items()},
            'context': vars(self.context),
            'difficulty_level': self.difficulty_level,
            'learning_objectives': self.learning_objectives
        }

    def to_json(self, filepath: str):
        """Save to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ScenarioTemplate:
        """Deserialize from dictionary"""
        # Reconstruct objects
        template = cls(
            scenario_id=data['scenario_id'],
            name=data['name'],
            description=data['description'],
            domain=ConflictDomain(data['domain']),
            difficulty_level=data.get('difficulty_level', 'intermediate'),
            learning_objectives=data.get('learning_objectives', [])
        )

        # Reconstruct parties
        for pid, pdata in data.get('parties', {}).items():
            template.parties[pid] = PartyProfile(**pdata)

        # Reconstruct issues
        for iid, idata in data.get('issues', {}).items():
            template.issues[iid] = IssueDefinition(**idata)

        # Reconstruct context
        if 'context' in data:
            template.context = ContextParameters(**data['context'])

        return template

    @classmethod
    def from_json(cls, filepath: str) -> ScenarioTemplate:
        """Load from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)


class ScenarioBuilder:
    """
    Fluent builder for creating scenarios programmatically
    Makes it easy for non-technical users to define scenarios
    """

    def __init__(self, scenario_id: str, name: str, description: str, domain: ConflictDomain):
        self.template = ScenarioTemplate(
            scenario_id=scenario_id,
            name=name,
            description=description,
            domain=domain
        )

    def add_party(
        self,
        party_id: str,
        display_name: str,
        party_type: str,
        power_level: float = 0.5,
        **kwargs
    ) -> ScenarioBuilder:
        """Add a party/stakeholder"""
        self.template.parties[party_id] = PartyProfile(
            party_id=party_id,
            display_name=display_name,
            party_type=party_type,
            power_level=power_level,
            **kwargs
        )
        return self

    def add_issue(
        self,
        issue_id: str,
        display_name: str,
        description: str,
        value_type: str = "numeric",
        **kwargs
    ) -> ScenarioBuilder:
        """Add a negotiable issue"""
        self.template.issues[issue_id] = IssueDefinition(
            issue_id=issue_id,
            display_name=display_name,
            description=description,
            value_type=value_type,
            **kwargs
        )
        return self

    def set_context(self, **kwargs) -> ScenarioBuilder:
        """Set contextual parameters"""
        for key, value in kwargs.items():
            setattr(self.template.context, key, value)
        return self

    def set_difficulty(self, level: str) -> ScenarioBuilder:
        """Set difficulty level"""
        self.template.difficulty_level = level
        return self

    def add_learning_objective(self, objective: str) -> ScenarioBuilder:
        """Add learning objective"""
        self.template.learning_objectives.append(objective)
        return self

    def build(self) -> ScenarioTemplate:
        """Build and return template"""
        return self.template


# Domain-specific feature extractors

def extract_maritime_features(agreement_vector: Dict[str, Any]) -> Dict[str, float]:
    """
    Extract abstract features from maritime-specific agreement
    Maps domain-specific terms to universal concepts
    """
    features = {
        "safety": 0.5,
        "fairness": 0.5,
        "sovereignty": 0.5,
        "economic_value": 0.5,
        "verification": 0.5,
        "flexibility": 0.5
    }

    # Safety features
    if "resupply_SOP" in agreement_vector:
        sop = agreement_vector["resupply_SOP"]
        features["safety"] += min(0.2, sop.get("standoff_nm", 0) * 0.03)
        features["verification"] += 0.1 if sop.get("pre_notification_hours", 0) >= 12 else 0

    if "hotline_cues" in agreement_vector:
        features["safety"] += 0.15
        features["flexibility"] += 0.1

    # Economic features
    if "fisheries_corridor" in agreement_vector or "scarborough_fisheries_corridor" in agreement_vector:
        features["economic_value"] += 0.2
        features["fairness"] += 0.15

    # Transparency
    if "ais_transparency" in agreement_vector or "ais_transparency_cell" in agreement_vector:
        features["verification"] += 0.2
        features["safety"] += 0.1

    # Face-saving
    if "media_protocol" in agreement_vector:
        protocol = agreement_vector["media_protocol"]
        if protocol.get("embargo_hours", 0) >= 6:
            features["sovereignty"] += 0.1  # Face-saving aspect

    # Normalize
    return {k: max(0, min(1, v)) for k, v in features.items()}


def extract_territorial_features(agreement_vector: Dict[str, Any]) -> Dict[str, float]:
    """Extract features for land border disputes"""
    features = {
        "safety": 0.5,
        "fairness": 0.5,
        "sovereignty": 0.5,
        "economic_value": 0.5,
        "verification": 0.5,
        "flexibility": 0.5
    }

    # Territory allocation
    if "territory_allocation" in agreement_vector:
        alloc = agreement_vector["territory_allocation"]
        # Fair division increases fairness
        if 0.4 <= alloc.get("percentage_party_a", 0.5) <= 0.6:
            features["fairness"] += 0.2

    # DMZ/buffer zones
    if "buffer_zone" in agreement_vector:
        features["safety"] += 0.2
        features["verification"] += 0.15

    # Joint development
    if "joint_development_area" in agreement_vector:
        features["economic_value"] += 0.25
        features["flexibility"] += 0.2
        features["fairness"] += 0.1

    # Population resettlement
    if "resettlement_plan" in agreement_vector:
        plan = agreement_vector["resettlement_plan"]
        if plan.get("compensation_provided", False):
            features["fairness"] += 0.15

    return {k: max(0, min(1, v)) for k, v in features.items()}


def extract_resource_features(agreement_vector: Dict[str, Any]) -> Dict[str, float]:
    """Extract features for resource conflicts (water, energy, etc.)"""
    features = {
        "sustainability": 0.5,
        "fairness": 0.5,
        "economic_value": 0.5,
        "verification": 0.5,
        "flexibility": 0.5,
        "resilience": 0.5
    }

    # Resource allocation
    if "water_allocation" in agreement_vector or "resource_allocation" in agreement_vector:
        alloc = agreement_vector.get("water_allocation", agreement_vector.get("resource_allocation", {}))

        # Equitable sharing
        if alloc.get("allocation_type") == "proportional":
            features["fairness"] += 0.2

        # Seasonal flexibility
        if "seasonal_variation" in alloc:
            features["flexibility"] += 0.15
            features["resilience"] += 0.1

    # Environmental protections
    if "environmental_safeguards" in agreement_vector:
        features["sustainability"] += 0.25
        features["resilience"] += 0.15

    # Monitoring mechanisms
    if "joint_monitoring" in agreement_vector:
        features["verification"] += 0.2
        features["fairness"] += 0.1

    # Economic compensation
    if "compensation_mechanism" in agreement_vector:
        features["fairness"] += 0.15
        features["economic_value"] += 0.1

    return {k: max(0, min(1, v)) for k, v in features.items()}


# Registry of feature extractors by domain
FEATURE_EXTRACTORS = {
    ConflictDomain.MARITIME: extract_maritime_features,
    ConflictDomain.LAND_BORDER: extract_territorial_features,
    ConflictDomain.RESOURCE: extract_resource_features,
    # Add more as needed
}


def get_feature_extractor(domain: ConflictDomain) -> Callable:
    """Get appropriate feature extractor for domain"""
    return FEATURE_EXTRACTORS.get(domain, extract_maritime_features)  # Default to maritime
