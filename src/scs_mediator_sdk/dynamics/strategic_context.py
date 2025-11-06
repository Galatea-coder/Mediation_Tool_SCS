"""
Strategic Context and Soft Power Tracking
Adds diplomatic, economic, and political dimensions to simulation parameters
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class StrategicActionType(Enum):
    """Categories of strategic actions"""
    DIPLOMATIC = "diplomatic"
    MILITARY_SIGNALING = "military_signaling"
    ECONOMIC = "economic"
    COMMUNICATION = "communication"
    CONFIDENCE_BUILDING = "confidence_building"


@dataclass
class StrategicAction:
    """
    A strategic move that affects both hard parameters and soft power

    Based on:
    - Nye, J. (2004). "Soft Power: The Means to Success in World Politics"
    - Schelling, T. (1966). "Arms and Influence"
    """
    name: str
    description: str
    action_type: StrategicActionType

    # Effects on numerical simulation parameters
    parameter_effects: Dict[str, any] = field(default_factory=dict)

    # Effects on strategic context scores
    diplomatic_capital_change: int = 0  # -100 to +100
    international_legitimacy_change: int = 0
    domestic_support_change: int = 0
    credibility_change: int = 0

    # Costs and risks
    cost_description: str = ""
    risk_level: str = "low"  # low, medium, high

    # Academic grounding
    theoretical_basis: str = ""


@dataclass
class StrategicContext:
    """
    Soft power and strategic positioning metrics
    Complements numerical simulation parameters
    """
    # Core strategic dimensions (0-100 scale)
    diplomatic_capital: float = 50.0  # Ability to influence through diplomacy
    international_legitimacy: float = 50.0  # Support from int'l community
    domestic_support: float = 50.0  # Public/government backing
    credibility: float = 50.0  # Reputation for following through

    # Track which strategic actions have been taken
    actions_taken: List[str] = field(default_factory=list)

    # Turn-based tracking
    turn_number: int = 0

    def apply_action(self, action: StrategicAction):
        """Apply effects of a strategic action"""
        self.diplomatic_capital = self._clamp(
            self.diplomatic_capital + action.diplomatic_capital_change
        )
        self.international_legitimacy = self._clamp(
            self.international_legitimacy + action.international_legitimacy_change
        )
        self.domestic_support = self._clamp(
            self.domestic_support + action.domestic_support_change
        )
        self.credibility = self._clamp(
            self.credibility + action.credibility_change
        )

        self.actions_taken.append(action.name)

    def _clamp(self, value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
        """Clamp value to range"""
        return max(min_val, min(max_val, value))

    def get_escalation_modifier(self) -> float:
        """
        Calculate how strategic context modifies escalation risk

        Returns:
            Multiplier for base escalation risk (0.7 = 30% reduction, 1.3 = 30% increase)
        """
        modifier = 1.0

        # High international legitimacy reduces escalation risk
        if self.international_legitimacy > 70:
            modifier *= 0.85  # 15% reduction
        elif self.international_legitimacy < 30:
            modifier *= 1.20  # 20% increase

        # Low credibility increases escalation (opponent doesn't believe threats)
        if self.credibility < 40:
            modifier *= 1.25  # 25% increase
        elif self.credibility > 75:
            modifier *= 0.90  # 10% reduction

        # Fragile domestic support forces hardline positions
        if self.domestic_support < 35:
            modifier *= 1.30  # 30% increase (political constraints)

        # High diplomatic capital enables de-escalation
        if self.diplomatic_capital > 70:
            modifier *= 0.85  # 15% reduction

        return modifier

    def get_summary(self) -> Dict[str, any]:
        """Get strategic context summary for display"""
        return {
            "diplomatic_capital": {
                "value": self.diplomatic_capital,
                "status": self._get_status_label(self.diplomatic_capital),
                "description": "Ability to influence through diplomatic channels"
            },
            "international_legitimacy": {
                "value": self.international_legitimacy,
                "status": self._get_status_label(self.international_legitimacy),
                "description": "Support from international community and allies"
            },
            "domestic_support": {
                "value": self.domestic_support,
                "status": self._get_status_label(self.domestic_support),
                "description": "Public and government backing for negotiation strategy"
            },
            "credibility": {
                "value": self.credibility,
                "status": self._get_status_label(self.credibility),
                "description": "Reputation for following through on commitments"
            },
            "escalation_modifier": self.get_escalation_modifier(),
            "actions_taken": len(self.actions_taken)
        }

    def _get_status_label(self, value: float) -> str:
        """Get status label for a metric"""
        if value >= 75:
            return "Strong"
        elif value >= 60:
            return "Good"
        elif value >= 40:
            return "Moderate"
        elif value >= 25:
            return "Weak"
        else:
            return "Critical"


# Predefined strategic actions
STRATEGIC_ACTIONS_LIBRARY = {
    "convene_regional_summit": StrategicAction(
        name="Convene Regional Summit",
        description="Organize ASEAN/APEC summit to build multilateral consensus",
        action_type=StrategicActionType.DIPLOMATIC,
        parameter_effects={
            "hotline": "Dedicated",
            "patrol_coordination": "Info sharing",
            "prenotify": 8
        },
        diplomatic_capital_change=-20,  # Costs capital to organize
        international_legitimacy_change=+15,  # Gains legitimacy
        domestic_support_change=+5,
        credibility_change=+10,
        cost_description="Requires significant diplomatic capital and time",
        risk_level="medium",
        theoretical_basis="Multilateral institutionalism (Keohane, 1984) - institutions reduce transaction costs and build trust"
    ),

    "propose_joint_development": StrategicAction(
        name="Propose Joint Development Zone",
        description="Suggest shelving sovereignty disputes for resource co-development",
        action_type=StrategicActionType.ECONOMIC,
        parameter_effects={
            "revenue_split": 50,
            "moratorium_months": 12,
            "buffer_zone_nm": 15
        },
        diplomatic_capital_change=+10,
        international_legitimacy_change=+20,
        domestic_support_change=-15,  # Domestic nationalists oppose
        credibility_change=+15,
        cost_description="Domestic sovereignty concerns, nationalist opposition",
        risk_level="high",
        theoretical_basis="Deng Xiaoping's 'shelving disputes, joint development' - functional cooperation builds trust (Fravel, 2008)"
    ),

    "launch_track_ii": StrategicAction(
        name="Launch Track II Dialogue",
        description="Establish unofficial academic/business dialogue channels",
        action_type=StrategicActionType.CONFIDENCE_BUILDING,
        parameter_effects={
            "prenotify": 6,
            "patrol_frequency": "Monthly"
        },
        diplomatic_capital_change=+5,
        international_legitimacy_change=+5,
        domestic_support_change=+10,  # Low-risk, broadly acceptable
        credibility_change=+5,
        cost_description="Slow process, requires sustained engagement",
        risk_level="low",
        theoretical_basis="Multi-track diplomacy (Diamond & McDonald, 1996) - unofficial channels reduce risk while building relationships"
    ),

    "public_commitment": StrategicAction(
        name="Make Public Commitment to Peace",
        description="High-profile statement pledging peaceful resolution",
        action_type=StrategicActionType.COMMUNICATION,
        parameter_effects={
            "standoff": 7,
            "escort": 3
        },
        diplomatic_capital_change=+15,
        international_legitimacy_change=+25,
        domestic_support_change=-10,  # Hardliners criticize as weakness
        credibility_change=-5,  # Must follow through or lose credibility
        cost_description="Locks in position, vulnerable to opponent's moves",
        risk_level="medium",
        theoretical_basis="Audience costs (Fearon, 1994) - public commitments constrain but also signal resolve"
    ),

    "increase_transparency": StrategicAction(
        name="Increase Military Transparency",
        description="Share naval exercise schedules and patrol routes proactively",
        action_type=StrategicActionType.CONFIDENCE_BUILDING,
        parameter_effects={
            "prenotify": 9,
            "hotline": "Dedicated"
        },
        diplomatic_capital_change=+10,
        international_legitimacy_change=+10,
        domestic_support_change=0,
        credibility_change=+15,
        cost_description="Reduces tactical flexibility, requires sustained openness",
        risk_level="low",
        theoretical_basis="Confidence-building measures (Osgood, 1962 GRIT) - unilateral transparency initiatives reduce threat perceptions"
    ),

    "economic_incentives": StrategicAction(
        name="Offer Economic Incentives",
        description="Propose trade benefits or development aid for cooperation",
        action_type=StrategicActionType.ECONOMIC,
        parameter_effects={
            "traditional_access": 80,
            "revenue_split": 60
        },
        diplomatic_capital_change=-15,  # Costs resources
        international_legitimacy_change=+5,
        domestic_support_change=-5,  # "Why reward aggression?"
        credibility_change=+10,
        cost_description="Financial costs, may be seen as appeasement domestically",
        risk_level="medium",
        theoretical_basis="Issue linkage (Tollison & Willett, 1979) - expand pie through cross-issue trades"
    )
}


def get_available_actions(context: StrategicContext) -> List[StrategicAction]:
    """
    Get strategic actions available based on current context

    Args:
        context: Current strategic context

    Returns:
        List of available strategic actions
    """
    available = []

    for action_id, action in STRATEGIC_ACTIONS_LIBRARY.items():
        # Check if already taken (some actions can only be done once)
        if action.name in context.actions_taken:
            if action_id in ["convene_regional_summit", "propose_joint_development"]:
                continue  # These can only be done once

        # Check if prerequisites are met
        if action_id == "convene_regional_summit":
            if context.diplomatic_capital < 30:
                continue  # Not enough capital

        if action_id == "propose_joint_development":
            if context.domestic_support < 40:
                continue  # Too risky with low domestic support

        available.append(action)

    return available
