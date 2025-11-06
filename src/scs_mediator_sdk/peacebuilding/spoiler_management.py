"""
Spoiler Management for Peace Mediation

This module implements Stedman's (1997) spoiler problem framework for identifying,
classifying, and managing actors who threaten peace processes.

Part 5 of 10 Peace Mediation Enhancements.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional


class SpoilerType(Enum):
    """Types of spoilers (Stedman 1997)"""
    LIMITED = "limited"        # Limited goals, will accept some agreements
    GREEDY = "greedy"          # Maximalist goals, but rational calculations
    TOTAL = "total"            # Reject all compromises, ideological


class SpoilerCapability(Enum):
    """Spoiler's capacity to disrupt peace"""
    LOW = "low"           # Can cause minor incidents
    MEDIUM = "medium"     # Can derail negotiations
    HIGH = "high"         # Can restart full conflict


class SpoilerPosition(Enum):
    """Spoiler's position relative to negotiation"""
    INSIDE = "inside"     # Party to negotiations
    OUTSIDE = "outside"   # Not at table, external
    FACTION = "faction"   # Internal faction within a party


@dataclass
class Spoiler:
    """An actor who threatens the peace process"""
    name: str
    spoiler_type: SpoilerType
    capability: SpoilerCapability
    position: SpoilerPosition

    # Motivations
    interests_threatened: List[str] = field(default_factory=list)
    benefits_from_conflict: List[str] = field(default_factory=list)

    # Behavior patterns
    typical_spoiling_actions: List[str] = field(default_factory=list)
    recent_incidents: List[Dict] = field(default_factory=list)

    # Vulnerabilities
    dependencies: List[str] = field(default_factory=list)  # What they need
    constituencies: List[str] = field(default_factory=list)  # Who supports them

    # Influence
    influence_on_parties: Dict[str, float] = field(default_factory=dict)  # party -> influence level


class SpoilerManager:
    """
    Manage spoilers in peace process
    Based on Stedman (1997) and Zahar (2003)
    """

    def __init__(self):
        self.spoilers: Dict[str, Spoiler] = {}
        self.mitigation_strategies: Dict[str, List[str]] = {}

    def add_spoiler(self, spoiler: Spoiler):
        """Register a spoiler"""
        self.spoilers[spoiler.name] = spoiler
        self._recommend_strategy(spoiler)

    def _recommend_strategy(self, spoiler: Spoiler) -> List[str]:
        """
        Recommend strategy based on spoiler type

        Stedman's strategies:
        - Inducement: Positive incentives
        - Socialization: Bring into process
        - Coercion: Punishment, isolation
        """
        strategies = []

        if spoiler.spoiler_type == SpoilerType.LIMITED:
            # Limited spoilers can be induced
            strategies.extend([
                "INDUCEMENT: Offer side payments or concessions",
                "INCLUSION: Bring to negotiating table",
                "ADDRESS: Accommodate some legitimate concerns",
                "ISOLATE_MODERATELY: If refuses reasonable offers"
            ])

        elif spoiler.spoiler_type == SpoilerType.GREEDY:
            # Greedy spoilers need mixed approach
            strategies.extend([
                "INDUCEMENT: Offer carrots for cooperation",
                "COERCION: Threaten sticks for spoiling",
                "DEADLINE: Create urgency and BATNA clarity",
                "SPLIT: Try to separate from extremists",
                "MONITOR: Watch for exploitation of concessions"
            ])

        elif spoiler.spoiler_type == SpoilerType.TOTAL:
            # Total spoilers rarely respond to inducement
            strategies.extend([
                "COERCION: Use force or isolation as primary tool",
                "MARGINALIZE: Reduce legitimacy and support",
                "PROTECT: Shield peace process from their attacks",
                "DELEGITIMIZE: Expose their extremism",
                "WAIT: Sometimes they lose support over time"
            ])

        # Adjust by capability
        if spoiler.capability == SpoilerCapability.HIGH:
            strategies.insert(0, "PRIORITY: This is high-threat spoiler - act urgently")

        # Adjust by position
        if spoiler.position == SpoilerPosition.INSIDE:
            strategies.append("MANAGE_INTERNALLY: Work through their parent party")
        elif spoiler.position == SpoilerPosition.OUTSIDE:
            strategies.append("EXTERNAL_PRESSURE: Use allies, sanctions, isolation")
        elif spoiler.position == SpoilerPosition.FACTION:
            strategies.append("SPLIT_STRATEGY: Strengthen moderates, isolate hardliners")

        self.mitigation_strategies[spoiler.name] = strategies
        return strategies

    def assess_spoiling_risk(self, proposed_agreement: Dict) -> Dict:
        """
        Assess risk that spoilers will undermine agreement

        Args:
            proposed_agreement: The agreement to assess

        Returns:
            Risk assessment dictionary
        """
        risk_assessment = {
            "overall_risk": 0.0,
            "high_threat_spoilers": [],
            "likely_spoiling_actions": [],
            "protective_measures_needed": [],
            "implementation_vulnerabilities": []
        }

        for name, spoiler in self.spoilers.items():
            # Calculate individual spoiler threat
            threat_score = 0.0

            # Type contributes
            if spoiler.spoiler_type == SpoilerType.TOTAL:
                threat_score += 0.4
            elif spoiler.spoiler_type == SpoilerType.GREEDY:
                threat_score += 0.3
            else:
                threat_score += 0.1

            # Capability contributes
            if spoiler.capability == SpoilerCapability.HIGH:
                threat_score += 0.4
            elif spoiler.capability == SpoilerCapability.MEDIUM:
                threat_score += 0.2
            else:
                threat_score += 0.1

            # Check if agreement threatens their interests
            threatens_interests = self._agreement_threatens_spoiler(proposed_agreement, spoiler)
            if threatens_interests:
                threat_score += 0.2
                risk_assessment["likely_spoiling_actions"].extend(
                    spoiler.typical_spoiling_actions
                )

            # Add to high threat list if significant
            if threat_score > 0.6:
                risk_assessment["high_threat_spoilers"].append(name)

            risk_assessment["overall_risk"] = max(risk_assessment["overall_risk"], threat_score)

        # Recommend protective measures
        if risk_assessment["overall_risk"] > 0.5:
            risk_assessment["protective_measures_needed"].extend([
                "Robust implementation monitoring",
                "Quick reaction force for violations",
                "Protected corridors for agreement implementation",
                "Early warning system for spoiler activity",
                "Isolation of spoilers from constituencies"
            ])

        return risk_assessment

    def _agreement_threatens_spoiler(self, agreement: Dict, spoiler: Spoiler) -> bool:
        """Check if agreement threatens spoiler's interests"""
        # Check if agreement provisions conflict with spoiler benefits
        for benefit in spoiler.benefits_from_conflict:
            if "resource_control" in benefit and "shared_resources" in agreement:
                return True
            if "smuggling" in benefit and "monitoring" in agreement:
                return True
            if "military_presence" in benefit and "demilitarization" in agreement:
                return True

        return False

    def design_spoiler_management_plan(self) -> Dict:
        """
        Create comprehensive plan to manage all identified spoilers

        Returns:
            Management plan dictionary
        """
        plan = {
            "immediate_actions": [],
            "ongoing_monitoring": [],
            "contingency_responses": {},
            "success_indicators": []
        }

        for name, spoiler in self.spoilers.items():
            strategies = self.mitigation_strategies.get(name, [])

            # Immediate actions for high-threat spoilers
            if spoiler.capability == SpoilerCapability.HIGH:
                plan["immediate_actions"].append(
                    f"Address {name} immediately using: {strategies[0]}"
                )

            # Ongoing monitoring
            plan["ongoing_monitoring"].append(
                f"Track {name} activity: {', '.join(spoiler.typical_spoiling_actions[:3])}"
            )

            # Contingency responses
            plan["contingency_responses"][name] = {
                "if_spoils": strategies,
                "early_warning_signs": spoiler.typical_spoiling_actions,
                "escalation_protocol": self._create_escalation_protocol(spoiler)
            }

        # Success indicators
        plan["success_indicators"] = [
            "No major spoiling incidents for 30 days",
            "Spoilers lose support from constituencies",
            "Moderate factions gain strength",
            "Agreement implementation proceeds on schedule"
        ]

        return plan

    def _create_escalation_protocol(self, spoiler: Spoiler) -> List[str]:
        """Create escalation protocol for responding to spoiler"""
        protocol = []

        if spoiler.spoiler_type == SpoilerType.LIMITED:
            protocol = [
                "Level 1: Private communication expressing concern",
                "Level 2: Public statement condemning action",
                "Level 3: Reduced incentives/benefits",
                "Level 4: Sanctions or exclusion from process"
            ]
        elif spoiler.spoiler_type == SpoilerType.GREEDY:
            protocol = [
                "Level 1: Warning about consequences",
                "Level 2: Targeted sanctions",
                "Level 3: Isolation from supporters",
                "Level 4: Coercive measures"
            ]
        else:  # TOTAL
            protocol = [
                "Level 1: Marginalization efforts",
                "Level 2: Delegitimization campaign",
                "Level 3: Coercive isolation",
                "Level 4: Direct confrontation if necessary"
            ]

        return protocol


# SCS-specific spoiler examples

def create_scs_spoilers() -> List[Spoiler]:
    """
    Potential spoilers in SCS peace process

    Returns:
        List of identified spoilers
    """
    return [
        Spoiler(
            name="Hardline Nationalist Faction (China)",
            spoiler_type=SpoilerType.GREEDY,
            capability=SpoilerCapability.MEDIUM,
            position=SpoilerPosition.FACTION,
            interests_threatened=["National pride", "Territorial claims"],
            benefits_from_conflict=["Political support", "Nationalist legitimacy"],
            typical_spoiling_actions=[
                "Inflammatory social media campaigns",
                "Pressure on government to take harder line",
                "Protests against any concessions",
                "Accusations of betrayal"
            ],
            dependencies=["Social media platforms", "Public support"],
            constituencies=["Urban youth", "Military veterans"],
            influence_on_parties={"China": 0.3}
        ),
        Spoiler(
            name="Maritime Militia (China)",
            spoiler_type=SpoilerType.LIMITED,
            capability=SpoilerCapability.MEDIUM,
            position=SpoilerPosition.INSIDE,
            interests_threatened=["Fishing income", "Military support payments"],
            benefits_from_conflict=["Government subsidies", "Fishing monopoly"],
            typical_spoiling_actions=[
                "Provocative fishing in disputed areas",
                "Harassment of other nations' vessels",
                "'Accidental' incidents",
                "Refusing to follow de-escalation protocols"
            ],
            dependencies=["Government funding", "Fuel subsidies"],
            constituencies=["Coastal fishing communities"],
            influence_on_parties={"China": 0.4}
        ),
        Spoiler(
            name="Weapons Suppliers",
            spoiler_type=SpoilerType.GREEDY,
            capability=SpoilerCapability.LOW,
            position=SpoilerPosition.OUTSIDE,
            interests_threatened=["Arms sales"],
            benefits_from_conflict=["Increased defense spending", "Military contracts"],
            typical_spoiling_actions=[
                "Lobbying against arms reduction",
                "Highlighting threats to justify purchases",
                "Campaign donations to hardliners"
            ],
            dependencies=["Defense budgets"],
            constituencies=["Defense industry"],
            influence_on_parties={"Philippines": 0.2, "Vietnam": 0.2}
        ),
        Spoiler(
            name="Illegal Fishing Cartels",
            spoiler_type=SpoilerType.LIMITED,
            capability=SpoilerCapability.LOW,
            position=SpoilerPosition.OUTSIDE,
            interests_threatened=["Illegal fishing operations"],
            benefits_from_conflict=["Reduced enforcement", "Overfishing opportunities"],
            typical_spoiling_actions=[
                "Fishing in protected areas",
                "Bribing officials to avoid enforcement",
                "Creating incidents to distract authorities"
            ],
            dependencies=["Weak enforcement"],
            constituencies=["Organized crime networks"],
            influence_on_parties={"Philippines": 0.1, "Vietnam": 0.1}
        )
    ]


# Example usage
if __name__ == "__main__":
    # Create spoiler manager
    manager = SpoilerManager()

    # Add SCS spoilers
    for spoiler in create_scs_spoilers():
        manager.add_spoiler(spoiler)

    print(f"Total Spoilers Identified: {len(manager.spoilers)}\n")

    # Show strategies for each spoiler
    for name, spoiler in manager.spoilers.items():
        print(f"\nSpoiler: {name}")
        print(f"  Type: {spoiler.spoiler_type.value}")
        print(f"  Capability: {spoiler.capability.value}")
        print(f"  Position: {spoiler.position.value}")
        print(f"\n  Recommended Strategies:")
        for strategy in manager.mitigation_strategies[name][:3]:
            print(f"    - {strategy}")

    # Assess spoiling risk
    print(f"\n\nAssessing Spoiling Risk for Proposed Agreement:")
    agreement = {
        "shared_resources": True,
        "monitoring": True,
        "demilitarization": False
    }

    risk = manager.assess_spoiling_risk(agreement)
    print(f"  Overall Risk: {risk['overall_risk']:.2f}")
    print(f"  High-Threat Spoilers: {', '.join(risk['high_threat_spoilers']) if risk['high_threat_spoilers'] else 'None'}")
    print(f"  Protective Measures Needed: {len(risk['protective_measures_needed'])}")

    # Design management plan
    print(f"\n\nSpoiler Management Plan:")
    plan = manager.design_spoiler_management_plan()
    print(f"  Immediate Actions: {len(plan['immediate_actions'])}")
    print(f"  Ongoing Monitoring: {len(plan['ongoing_monitoring'])}")
    print(f"  Success Indicators: {len(plan['success_indicators'])}")
