"""
Two-Level Games & Domestic Politics Constraints

This module implements Putnam's (1988) two-level game theory, modeling how
domestic political constraints affect international negotiations and ratification.

Part 3 of 10 Peace Mediation Enhancements.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum


class DomesticActor(Enum):
    """Key domestic political actors"""
    HARDLINE_NATIONALISTS = "hardline_nationalists"
    MODERATE_PRAGMATISTS = "moderate_pragmatists"
    BUSINESS_INTERESTS = "business_interests"
    MILITARY = "military"
    FISHERMEN = "fishermen"
    PUBLIC_OPINION = "public_opinion"
    MEDIA = "media"


@dataclass
class DomesticConstraint:
    """A constraint from domestic politics"""
    actor: DomesticActor
    issue: str
    position: str
    intensity: float  # 0-1, how strongly held
    mobilization_capacity: float  # 0-1, ability to cause problems

    # Red lines
    acceptable_range: Dict[str, tuple] = field(default_factory=dict)  # issue -> (min, max)

    # Pressure tactics
    pressure_tactics: List[str] = field(default_factory=list)


class WinSetAnalyzer:
    """
    Analyze 'win-sets' - deals that can be ratified domestically
    Based on Putnam (1988) two-level game theory
    """

    def __init__(self, country: str):
        self.country = country
        self.domestic_actors: Dict[DomesticActor, DomesticConstraint] = {}
        self.win_set_size = 1.0  # Start fully flexible

    def add_domestic_actor(self, constraint: DomesticConstraint):
        """Add domestic constraint"""
        self.domestic_actors[constraint.actor] = constraint
        self._recalculate_win_set()

    def _recalculate_win_set(self):
        """Calculate how constrained negotiator is"""
        # More hardline actors = smaller win-set = less flexibility
        hardline_influence = 0.0

        for actor, constraint in self.domestic_actors.items():
            if actor in [DomesticActor.HARDLINE_NATIONALISTS, DomesticActor.MILITARY]:
                hardline_influence += constraint.intensity * constraint.mobilization_capacity

        # Win-set shrinks with hardline pressure
        self.win_set_size = max(0.1, 1.0 - (hardline_influence / 2))

    def test_domestic_acceptability(self, proposed_deal: Dict) -> Dict:
        """
        Test if proposed deal can be ratified domestically

        Args:
            proposed_deal: Dictionary of deal terms to test

        Returns:
            Dictionary containing:
            - acceptable: Boolean indicating if deal can be ratified
            - overall_support: Float 0-1 indicating support level
            - objectors: List of actors who object
            - required_compensations: List of suggested compensations
            - ratification_probability: Float 0-1 probability of ratification
        """
        result = {
            "acceptable": True,
            "overall_support": 0.0,
            "objectors": [],
            "required_compensations": [],
            "ratification_probability": 0.0
        }

        total_influence = 0.0
        support_weighted = 0.0

        for actor, constraint in self.domestic_actors.items():
            # Check if deal violates this actor's red lines
            violated = False
            for issue, acceptable_range in constraint.acceptable_range.items():
                if issue in proposed_deal:
                    value = proposed_deal[issue]
                    min_val, max_val = acceptable_range
                    if value < min_val or value > max_val:
                        violated = True
                        result["objectors"].append({
                            "actor": actor.value,
                            "issue": issue,
                            "required": f"{min_val}-{max_val}",
                            "proposed": value
                        })

            # Weight by mobilization capacity
            weight = constraint.mobilization_capacity
            total_influence += weight

            if not violated:
                support_weighted += weight
            else:
                # Suggest compensation
                if actor == DomesticActor.FISHERMEN:
                    result["required_compensations"].append(
                        "Compensation fund for displaced fishermen"
                    )
                elif actor == DomesticActor.HARDLINE_NATIONALISTS:
                    result["required_compensations"].append(
                        "Symbolic victory on sovereignty language"
                    )

        # Calculate overall support
        if total_influence > 0:
            result["overall_support"] = support_weighted / total_influence

        # Ratification probability
        result["ratification_probability"] = result["overall_support"] * self.win_set_size

        # Acceptable if >50% probability
        result["acceptable"] = result["ratification_probability"] > 0.5

        return result

    def identify_deal_breakers(self) -> List[str]:
        """Identify issues that are complete red lines"""
        deal_breakers = []

        for actor, constraint in self.domestic_actors.items():
            if constraint.intensity > 0.8 and constraint.mobilization_capacity > 0.7:
                # This actor has both strong views and power
                deal_breakers.append(f"{actor.value}: {constraint.position}")

        return deal_breakers

    def suggest_ratification_strategy(self, proposed_deal: Dict) -> List[str]:
        """
        Suggest how to get deal ratified

        Args:
            proposed_deal: The deal to be ratified

        Returns:
            List of strategic recommendations
        """
        strategy = []

        acceptance = self.test_domestic_acceptability(proposed_deal)

        if acceptance["acceptable"]:
            strategy.append("Sell deal emphasizing benefits to key constituencies")
            strategy.append("Frame as protecting national interests")
        else:
            strategy.append("Modify deal to address major objections:")
            for objection in acceptance["objectors"]:
                strategy.append(f"  - Address {objection['actor']} concerns on {objection['issue']}")

            strategy.append("Provide compensations:")
            for comp in acceptance["required_compensations"]:
                strategy.append(f"  - {comp}")

            strategy.append("Build coalition of moderate supporters")
            strategy.append("Manage nationalist backlash through media strategy")

        return strategy


# Example domestic configurations for SCS countries

def create_philippines_domestic_actors() -> List[DomesticConstraint]:
    """
    Philippines domestic political landscape

    Returns:
        List of domestic constraints for Philippines
    """
    return [
        DomesticConstraint(
            actor=DomesticActor.HARDLINE_NATIONALISTS,
            issue="Scarborough Shoal",
            position="Must regain access to traditional fishing grounds",
            intensity=0.8,
            mobilization_capacity=0.6,
            acceptable_range={"fisheries_access": (0.5, 1.0)},
            pressure_tactics=["protests", "social_media", "congressional_hearings"]
        ),
        DomesticConstraint(
            actor=DomesticActor.FISHERMEN,
            issue="Livelihoods",
            position="Need guaranteed fishing access",
            intensity=0.9,
            mobilization_capacity=0.7,
            acceptable_range={"fisheries_access": (0.6, 1.0)},
            pressure_tactics=["blockades", "demonstrations", "sympathy_from_public"]
        ),
        DomesticConstraint(
            actor=DomesticActor.MILITARY,
            issue="Defense",
            position="Cannot appear weak to China",
            intensity=0.7,
            mobilization_capacity=0.8,
            acceptable_range={"sovereignty_language": (0.5, 1.0)},
            pressure_tactics=["press_leaks", "bureaucratic_resistance"]
        ),
        DomesticConstraint(
            actor=DomesticActor.BUSINESS_INTERESTS,
            issue="Economic ties with China",
            position="Avoid disrupting trade and investment",
            intensity=0.6,
            mobilization_capacity=0.5,
            acceptable_range={"bilateral_tensions": (0.0, 0.5)},
            pressure_tactics=["lobbying", "campaign_donations"]
        )
    ]


def create_china_domestic_actors() -> List[DomesticConstraint]:
    """
    China domestic political landscape

    Returns:
        List of domestic constraints for China
    """
    return [
        DomesticConstraint(
            actor=DomesticActor.HARDLINE_NATIONALISTS,
            issue="Sovereignty",
            position="Nine-dash line is non-negotiable",
            intensity=0.9,
            mobilization_capacity=0.8,
            acceptable_range={"sovereignty_concessions": (0.0, 0.2)},
            pressure_tactics=["social_media", "protests", "boycotts"]
        ),
        DomesticConstraint(
            actor=DomesticActor.MILITARY,
            issue="Strategic access",
            position="Must maintain military freedom of action",
            intensity=0.85,
            mobilization_capacity=0.9,
            acceptable_range={"military_restrictions": (0.0, 0.3)},
            pressure_tactics=["policy_resistance", "shows_of_force"]
        ),
        DomesticConstraint(
            actor=DomesticActor.BUSINESS_INTERESTS,
            issue="Resource access",
            position="Need energy security",
            intensity=0.7,
            mobilization_capacity=0.6,
            acceptable_range={"resource_access": (0.7, 1.0)},
            pressure_tactics=["economic_analysis", "policy_papers"]
        )
    ]


# Example usage
if __name__ == "__main__":
    # Create win-set analyzer for Philippines
    phil_analyzer = WinSetAnalyzer("Philippines")

    # Add domestic actors
    for constraint in create_philippines_domestic_actors():
        phil_analyzer.add_domestic_actor(constraint)

    print(f"Philippines Win-Set Size: {phil_analyzer.win_set_size:.2f}")
    print(f"\nDeal Breakers:")
    for deal_breaker in phil_analyzer.identify_deal_breakers():
        print(f"  - {deal_breaker}")

    # Test a proposed deal
    proposed_deal = {
        "fisheries_access": 0.7,  # 70% access to traditional fishing grounds
        "sovereignty_language": 0.6,  # Moderate sovereignty language
        "bilateral_tensions": 0.3  # Some tension acceptable
    }

    print(f"\nTesting Proposed Deal:")
    print(f"  Fisheries Access: {proposed_deal['fisheries_access']}")
    print(f"  Sovereignty Language: {proposed_deal['sovereignty_language']}")
    print(f"  Bilateral Tensions: {proposed_deal['bilateral_tensions']}")

    result = phil_analyzer.test_domestic_acceptability(proposed_deal)
    print(f"\nDomestic Acceptability Results:")
    print(f"  Acceptable: {result['acceptable']}")
    print(f"  Ratification Probability: {result['ratification_probability']:.2%}")
    print(f"  Overall Support: {result['overall_support']:.2%}")

    if result['objectors']:
        print(f"\n  Objectors:")
        for obj in result['objectors']:
            print(f"    - {obj['actor']}: {obj['issue']} (requires {obj['required']}, proposed {obj['proposed']})")

    if result['required_compensations']:
        print(f"\n  Required Compensations:")
        for comp in result['required_compensations']:
            print(f"    - {comp}")

    # Get ratification strategy
    print(f"\nRatification Strategy:")
    strategy = phil_analyzer.suggest_ratification_strategy(proposed_deal)
    for step in strategy:
        print(f"  {step}")
