"""
Moore's Mediation Process: Phase 3-4 Implementation
Problem Definition, Agenda Setting, Option Generation & Reality Testing

Based on:
- Moore, C. W. (2014). The Mediation Process (4th ed.)
- Fisher & Ury (1981). Getting to Yes
- Lax & Sebenius (1986). The Manager as Negotiator
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Set
from enum import Enum
import itertools
from collections import defaultdict


class IssueType(Enum):
    """Types of negotiation issues"""
    DISTRIBUTIVE = "distributive"  # Fixed pie (territory, money)
    INTEGRATIVE = "integrative"    # Expandable pie (security, cooperation)
    PROCEDURAL = "procedural"      # How to negotiate
    SYMBOLIC = "symbolic"          # Identity, recognition, face


@dataclass
class Issue:
    """A negotiable issue in the conflict"""
    name: str
    issue_type: IssueType
    description: str
    
    # Stakeholder perspectives
    positions: Dict[str, str] = field(default_factory=dict)  # stakeholder -> position
    interests: Dict[str, List[str]] = field(default_factory=dict)  # stakeholder -> interests
    priorities: Dict[str, float] = field(default_factory=dict)  # stakeholder -> priority weight
    
    # Issue characteristics
    divisibility: float = 0.5  # Can it be split? (0=indivisible, 1=highly divisible)
    linkage_potential: float = 0.5  # Can it be linked to other issues?
    symbolic_value: float = 0.5  # How emotionally charged?
    objective_criteria: List[str] = field(default_factory=list)  # Standards for evaluation
    
    # Constraints
    constraints: List[str] = field(default_factory=list)
    deadlines: Optional[str] = None


@dataclass
class NegotiationOption:
    """A potential solution or agreement option"""
    option_id: str
    description: str
    provisions: Dict[str, Any]  # Specific terms for each issue
    
    # Evaluation
    feasibility: float = 0.0  # Can it be implemented?
    durability: float = 0.0  # Will it last?
    fairness: float = 0.0  # Is it equitable?
    efficiency: float = 0.0  # Pareto optimal?
    
    # Stakeholder acceptance
    utility_scores: Dict[str, float] = field(default_factory=dict)
    objections: Dict[str, List[str]] = field(default_factory=dict)
    
    # Implementation requirements
    required_resources: List[str] = field(default_factory=list)
    implementation_timeline: str = ""
    verification_mechanisms: List[str] = field(default_factory=list)


class AgendaDesigner:
    """
    Phase 3: Problem Definition & Agenda Setting
    
    Key Activities:
    1. Reframe issues from positions to interests
    2. Identify negotiable issues and non-negotiables
    3. Sequence issues strategically
    4. Establish ground rules
    5. Create safe space protocols
    """
    
    def __init__(self, conflict_name: str, stakeholders: List[str]):
        self.conflict_name = conflict_name
        self.stakeholders = stakeholders
        self.issues: Dict[str, Issue] = {}
        self.ground_rules: List[str] = []
        self.agenda_sequence: List[str] = []
        self.non_negotiables: Dict[str, List[str]] = {}  # stakeholder -> red lines
    
    def add_issue(self, issue: Issue):
        """Add issue to negotiation"""
        self.issues[issue.name] = issue
    
    def reframe_positions_to_interests(self, issue_name: str, stakeholder: str) -> List[str]:
        """
        Reframe stated positions as underlying interests
        Critical technique in interest-based negotiation
        
        Example:
        Position: "We must have 100% control of the territory"
        Interests: ["Security from attacks", "Resource access", "National pride"]
        """
        if issue_name not in self.issues:
            return []
        
        issue = self.issues[issue_name]
        position = issue.positions.get(stakeholder, "")
        
        # Interest identification heuristics
        potential_interests = []
        
        # Security interests
        if any(word in position.lower() for word in ["control", "protect", "defense", "safety"]):
            potential_interests.append("Security and protection")
        
        # Economic interests
        if any(word in position.lower() for word in ["resource", "economic", "access", "development"]):
            potential_interests.append("Economic prosperity")
        
        # Identity/face interests
        if any(word in position.lower() for word in ["sovereignty", "national", "historical", "legitimate"]):
            potential_interests.append("Recognition and respect")
        
        # Political interests
        if any(word in position.lower() for word in ["influence", "power", "authority", "governance"]):
            potential_interests.append("Political influence and stability")
        
        # Relationship interests
        if any(word in position.lower() for word in ["cooperation", "partnership", "alliance"]):
            potential_interests.append("Positive relationships")
        
        return potential_interests if potential_interests else ["Interests not yet clarified"]
    
    def identify_integrative_potential(self, issue1_name: str, issue2_name: str) -> float:
        """
        Assess potential for log-rolling or package deals between issues
        High potential when parties have different priorities
        """
        if issue1_name not in self.issues or issue2_name not in self.issues:
            return 0.0
        
        issue1 = self.issues[issue1_name]
        issue2 = self.issues[issue2_name]
        
        potential = 0.0
        
        # Check if stakeholders have different priorities on these issues
        for stakeholder in self.stakeholders:
            if stakeholder in issue1.priorities and stakeholder in issue2.priorities:
                priority_diff = abs(issue1.priorities[stakeholder] - issue2.priorities[stakeholder])
                potential += priority_diff
        
        # Normalize
        if self.stakeholders:
            potential /= len(self.stakeholders)
        
        # Adjust for linkage potential
        potential *= (issue1.linkage_potential + issue2.linkage_potential) / 2
        
        return min(1.0, potential)
    
    def sequence_issues(self, strategy: str = "easy_first") -> List[str]:
        """
        Strategically sequence issues in agenda
        
        Strategies:
        - easy_first: Build momentum with simple agreements
        - hard_first: Tackle difficult issues while energy is high
        - linkage: Group issues with trade-off potential
        - symbolic_last: Save face-saving symbolic issues for end
        """
        if not self.issues:
            return []
        
        issue_list = list(self.issues.items())
        
        if strategy == "easy_first":
            # Sort by: low symbolic value, high divisibility, few constraints
            def ease_score(item):
                issue = item[1]
                return (
                    (1 - issue.symbolic_value) * 0.4 +
                    issue.divisibility * 0.3 +
                    (1 - len(issue.constraints) / 10) * 0.3
                )
            issue_list.sort(key=ease_score, reverse=True)
        
        elif strategy == "hard_first":
            # Reverse of easy_first
            def difficulty_score(item):
                issue = item[1]
                return (
                    issue.symbolic_value * 0.4 +
                    (1 - issue.divisibility) * 0.3 +
                    (len(issue.constraints) / 10) * 0.3
                )
            issue_list.sort(key=difficulty_score, reverse=True)
        
        elif strategy == "linkage":
            # Group issues with high integrative potential
            # This is more complex - use clustering
            sequenced = []
            remaining = set(self.issues.keys())
            
            while remaining:
                # Pick highest priority unassigned issue
                current = max(remaining, key=lambda i: sum(self.issues[i].priorities.values()))
                sequenced.append(current)
                remaining.remove(current)
                
                # Find best link
                if remaining:
                    best_link = max(
                        remaining,
                        key=lambda i: self.identify_integrative_potential(current, i)
                    )
                    link_potential = self.identify_integrative_potential(current, best_link)
                    if link_potential > 0.5:  # Threshold
                        sequenced.append(best_link)
                        remaining.remove(best_link)
            
            self.agenda_sequence = sequenced
            return sequenced
        
        elif strategy == "symbolic_last":
            # Non-symbolic first, symbolic last
            issue_list.sort(key=lambda item: item[1].symbolic_value)
        
        self.agenda_sequence = [name for name, _ in issue_list]
        return self.agenda_sequence
    
    def establish_ground_rules(self, context: str = "default") -> List[str]:
        """
        Create ground rules appropriate for context
        Critical for creating safe space
        """
        rules = []
        
        # Universal ground rules
        rules.extend([
            "Confidentiality: Discussions are private unless agreed otherwise",
            "Respect: No personal attacks or inflammatory language",
            "Listen actively: Allow others to finish speaking",
            "Focus on interests, not positions",
            "Seek mutual gain where possible",
            "Use objective criteria where interests conflict"
        ])
        
        # Context-specific rules
        if context == "high_tension":
            rules.extend([
                "Cooling-off breaks available any time",
                "Mediator can call time-out if discussion becomes unproductive",
                "Start each session by acknowledging progress made"
            ])
        
        elif context == "power_asymmetry":
            rules.extend([
                "Equal speaking time for all parties",
                "Technical support available to all parties equally",
                "Decisions made by consensus, not majority vote"
            ])
        
        elif context == "high_face_sensitivity":
            rules.extend([
                "Option to meet separately with mediator (shuttle diplomacy)",
                "Proposals framed as mediator suggestions, not party demands",
                "Media embargo until agreement reached"
            ])
        
        self.ground_rules = rules
        return rules
    
    def identify_non_negotiables(self, stakeholder: str, red_lines: List[str]):
        """
        Document each party's non-negotiable constraints (BATNAs, red lines)
        Helps prevent wasted time on impossible proposals
        """
        self.non_negotiables[stakeholder] = red_lines
    
    def create_agenda_document(self) -> Dict[str, Any]:
        """Generate structured agenda for mediation"""
        return {
            "conflict_name": self.conflict_name,
            "participants": self.stakeholders,
            "ground_rules": self.ground_rules,
            "issue_sequence": self.agenda_sequence,
            "issue_details": {
                name: {
                    "description": issue.description,
                    "type": issue.issue_type.value,
                    "priorities": issue.priorities
                }
                for name, issue in self.issues.items()
            },
            "non_negotiables": self.non_negotiables
        }


class OptionGenerator:
    """
    Phase 4: Option Generation & Reality Testing
    
    Key Activities:
    1. Brainstorm creative solutions
    2. Evaluate against objective criteria
    3. Test feasibility
    4. Assess sustainability
    5. Identify implementation requirements
    """
    
    def __init__(self, issues: Dict[str, Issue], stakeholders: List[str]):
        self.issues = issues
        self.stakeholders = stakeholders
        self.options: Dict[str, NegotiationOption] = {}
        self.option_counter = 0
    
    def generate_single_issue_options(self, issue_name: str) -> List[NegotiationOption]:
        """
        Generate options for a single issue
        Uses various creative techniques
        """
        if issue_name not in self.issues:
            return []
        
        issue = self.issues[issue_name]
        options = []
        
        # Technique 1: Expand the pie (integrative)
        if issue.issue_type == IssueType.INTEGRATIVE:
            options.append(self._create_expanded_pie_option(issue))
        
        # Technique 2: Split the difference (distributive)
        if issue.issue_type == IssueType.DISTRIBUTIVE and issue.divisibility > 0.5:
            options.append(self._create_split_difference_option(issue))
        
        # Technique 3: Phased approach (time dimension)
        options.append(self._create_phased_option(issue))
        
        # Technique 4: Conditional approach (contingent on events)
        options.append(self._create_conditional_option(issue))
        
        # Technique 5: Third-party guarantor
        options.append(self._create_guarantor_option(issue))
        
        return [o for o in options if o is not None]
    
    def _create_expanded_pie_option(self, issue: Issue) -> Optional[NegotiationOption]:
        """Create option that expands value for all parties"""
        self.option_counter += 1
        
        # Find shared or complementary interests
        shared_interests = self._find_shared_interests(issue)
        
        if not shared_interests:
            return None
        
        return NegotiationOption(
            option_id=f"OPT_{self.option_counter}",
            description=f"Cooperative approach to {issue.name}: {', '.join(shared_interests)}",
            provisions={
                issue.name: {
                    "approach": "joint_development",
                    "shared_benefits": shared_interests,
                    "cooperation_mechanism": "joint_committee"
                }
            }
        )
    
    def _create_split_difference_option(self, issue: Issue) -> Optional[NegotiationOption]:
        """Create compromise option"""
        self.option_counter += 1
        
        return NegotiationOption(
            option_id=f"OPT_{self.option_counter}",
            description=f"Compromise on {issue.name}",
            provisions={
                issue.name: {
                    "approach": "split",
                    "allocation": {s: 1.0 / len(self.stakeholders) for s in self.stakeholders}
                }
            }
        )
    
    def _create_phased_option(self, issue: Issue) -> NegotiationOption:
        """Create option with staged implementation"""
        self.option_counter += 1
        
        return NegotiationOption(
            option_id=f"OPT_{self.option_counter}",
            description=f"Phased approach to {issue.name}",
            provisions={
                issue.name: {
                    "approach": "phased",
                    "phase_1": "confidence_building_measures",
                    "phase_2": "partial_implementation",
                    "phase_3": "full_implementation",
                    "triggers": "compliance_in_previous_phase"
                }
            }
        )
    
    def _create_conditional_option(self, issue: Issue) -> NegotiationOption:
        """Create option contingent on external events"""
        self.option_counter += 1
        
        return NegotiationOption(
            option_id=f"OPT_{self.option_counter}",
            description=f"Conditional approach to {issue.name}",
            provisions={
                issue.name: {
                    "approach": "conditional",
                    "conditions": ["if_no_incidents_for_6_months", "if_third_party_monitoring_succeeds"],
                    "fallback": "revert_to_status_quo"
                }
            }
        )
    
    def _create_guarantor_option(self, issue: Issue) -> NegotiationOption:
        """Create option with third-party guarantor"""
        self.option_counter += 1
        
        return NegotiationOption(
            option_id=f"OPT_{self.option_counter}",
            description=f"Third-party guaranteed {issue.name}",
            provisions={
                issue.name: {
                    "approach": "guaranteed",
                    "guarantor": "UN_or_regional_organization",
                    "monitoring": "continuous",
                    "enforcement": "sanctions_for_violation"
                }
            }
        )
    
    def _find_shared_interests(self, issue: Issue) -> List[str]:
        """Identify interests shared by multiple stakeholders"""
        if not issue.interests:
            return []
        
        # Count how many stakeholders have each interest
        interest_counts = defaultdict(int)
        for stakeholder, interests in issue.interests.items():
            for interest in interests:
                interest_counts[interest] += 1
        
        # Return interests shared by at least 50% of stakeholders
        threshold = len(self.stakeholders) / 2
        shared = [interest for interest, count in interest_counts.items() if count >= threshold]
        
        return shared
    
    def generate_package_deals(self, issue_names: List[str]) -> List[NegotiationOption]:
        """
        Generate package deals across multiple issues
        Enables log-rolling and trade-offs
        """
        options = []
        
        # Simple pairwise packages
        for i, issue1_name in enumerate(issue_names):
            for issue2_name in issue_names[i+1:]:
                package = self._create_package_option(issue1_name, issue2_name)
                if package:
                    options.append(package)
        
        # Comprehensive package (all issues)
        if len(issue_names) > 2:
            comprehensive = self._create_comprehensive_package(issue_names)
            if comprehensive:
                options.append(comprehensive)
        
        return options
    
    def _create_package_option(self, issue1_name: str, issue2_name: str) -> Optional[NegotiationOption]:
        """Create package deal between two issues"""
        if issue1_name not in self.issues or issue2_name not in self.issues:
            return None
        
        self.option_counter += 1
        issue1 = self.issues[issue1_name]
        issue2 = self.issues[issue2_name]
        
        # Find stakeholder who values issue1 more
        priority_diffs = {}
        for stakeholder in self.stakeholders:
            if stakeholder in issue1.priorities and stakeholder in issue2.priorities:
                priority_diffs[stakeholder] = issue1.priorities[stakeholder] - issue2.priorities[stakeholder]
        
        if not priority_diffs:
            return None
        
        # Trade: high-priority stakeholder gets preferred outcome on their priority issue
        # in exchange for concession on low-priority issue
        provisions = {}
        for stakeholder, diff in priority_diffs.items():
            if diff > 0.2:  # Stakeholder values issue1 more
                provisions[issue1_name] = {"favors": stakeholder}
                provisions[issue2_name] = {"concession_by": stakeholder}
        
        return NegotiationOption(
            option_id=f"OPT_{self.option_counter}",
            description=f"Package: Trade-off between {issue1_name} and {issue2_name}",
            provisions=provisions
        )
    
    def _create_comprehensive_package(self, issue_names: List[str]) -> NegotiationOption:
        """Create comprehensive package deal"""
        self.option_counter += 1
        
        provisions = {}
        for issue_name in issue_names:
            if issue_name in self.issues:
                provisions[issue_name] = {"approach": "balanced_across_all_issues"}
        
        return NegotiationOption(
            option_id=f"OPT_{self.option_counter}",
            description="Comprehensive package across all issues",
            provisions=provisions
        )
    
    def reality_test_option(self, option: NegotiationOption) -> Dict[str, float]:
        """
        Test option against reality criteria
        Returns scores for: feasibility, durability, fairness, efficiency
        """
        scores = {
            "feasibility": 0.0,
            "durability": 0.0,
            "fairness": 0.0,
            "efficiency": 0.0
        }
        
        # Feasibility: Can it be implemented?
        feasibility_factors = []
        
        # Check if provisions match issue types
        for issue_name in option.provisions:
            if issue_name in self.issues:
                issue = self.issues[issue_name]
                # Simpler provisions are more feasible
                if len(option.provisions[issue_name]) <= 3:
                    feasibility_factors.append(0.8)
                else:
                    feasibility_factors.append(0.5)
        
        scores["feasibility"] = np.mean(feasibility_factors) if feasibility_factors else 0.5
        
        # Durability: Will it last?
        # Options with monitoring and enforcement are more durable
        has_monitoring = any("monitoring" in str(p) for p in option.provisions.values())
        has_enforcement = any("enforcement" in str(p) or "guarantor" in str(p) for p in option.provisions.values())
        
        scores["durability"] = 0.4 + (0.3 if has_monitoring else 0) + (0.3 if has_enforcement else 0)
        
        # Fairness: Is it equitable?
        # More balanced if addresses multiple stakeholders' interests
        stakeholders_addressed = set()
        for provision in option.provisions.values():
            if isinstance(provision, dict):
                if "favors" in provision:
                    stakeholders_addressed.add(provision["favors"])
                if "allocation" in provision:
                    stakeholders_addressed.update(provision["allocation"].keys())
        
        scores["fairness"] = len(stakeholders_addressed) / len(self.stakeholders) if self.stakeholders else 0.5
        
        # Efficiency: Pareto optimal?
        # Package deals tend to be more efficient than single-issue solutions
        scores["efficiency"] = 0.6 if len(option.provisions) > 1 else 0.4
        
        # Update option scores
        option.feasibility = scores["feasibility"]
        option.durability = scores["durability"]
        option.fairness = scores["fairness"]
        option.efficiency = scores["efficiency"]
        
        return scores
    
    def rank_options(self, criteria_weights: Dict[str, float] = None) -> List[Tuple[str, float]]:
        """
        Rank all options by weighted criteria
        Default weights: feasibility=0.3, durability=0.3, fairness=0.2, efficiency=0.2
        """
        if criteria_weights is None:
            criteria_weights = {
                "feasibility": 0.3,
                "durability": 0.3,
                "fairness": 0.2,
                "efficiency": 0.2
            }
        
        rankings = []
        for option_id, option in self.options.items():
            # Ensure option has been reality tested
            if option.feasibility == 0.0:
                self.reality_test_option(option)
            
            score = (
                option.feasibility * criteria_weights["feasibility"] +
                option.durability * criteria_weights["durability"] +
                option.fairness * criteria_weights["fairness"] +
                option.efficiency * criteria_weights["efficiency"]
            )
            rankings.append((option_id, score))
        
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings


# Example usage
if __name__ == "__main__":
    # Set up stakeholders
    stakeholders = ["Country A", "Country B"]
    
    # Phase 3: Agenda Design
    agenda = AgendaDesigner("Maritime Boundary Dispute", stakeholders)
    
    # Add issues
    issue1 = Issue(
        name="Maritime Boundary",
        issue_type=IssueType.DISTRIBUTIVE,
        description="Location of EEZ boundary",
        positions={
            "Country A": "Boundary at median line",
            "Country B": "Boundary based on continental shelf"
        },
        priorities={"Country A": 0.9, "Country B": 0.8},
        divisibility=0.6,
        symbolic_value=0.7
    )
    
    issue2 = Issue(
        name="Fisheries Access",
        issue_type=IssueType.INTEGRATIVE,
        description="Fishing rights in disputed zone",
        priorities={"Country A": 0.7, "Country B": 0.9},
        divisibility=0.8,
        linkage_potential=0.9,
        symbolic_value=0.4
    )
    
    agenda.add_issue(issue1)
    agenda.add_issue(issue2)
    
    # Reframe positions to interests
    interests_a = agenda.reframe_positions_to_interests("Maritime Boundary", "Country A")
    print(f"Country A interests on Maritime Boundary: {interests_a}")
    
    # Sequence agenda
    sequence = agenda.sequence_issues(strategy="linkage")
    print(f"\nRecommended agenda sequence: {sequence}")
    
    # Establish ground rules
    rules = agenda.establish_ground_rules(context="high_tension")
    print(f"\nGround rules: {len(rules)} rules established")
    
    # Phase 4: Option Generation
    generator = OptionGenerator(agenda.issues, stakeholders)
    
    # Generate single-issue options
    options1 = generator.generate_single_issue_options("Maritime Boundary")
    print(f"\nGenerated {len(options1)} options for Maritime Boundary")
    
    # Generate package deals
    packages = generator.generate_package_deals(["Maritime Boundary", "Fisheries Access"])
    print(f"Generated {len(packages)} package deals")
    
    # Reality test options
    for option in options1 + packages:
        scores = generator.reality_test_option(option)
        print(f"\nOption {option.option_id}: {option.description}")
        print(f"  Feasibility: {scores['feasibility']:.2f}")
        print(f"  Durability: {scores['durability']:.2f}")
        print(f"  Fairness: {scores['fairness']:.2f}")
        print(f"  Efficiency: {scores['efficiency']:.2f}")
        generator.options[option.option_id] = option
    
    # Rank all options
    rankings = generator.rank_options()
    print(f"\nTop 3 options:")
    for option_id, score in rankings[:3]:
        option = generator.options[option_id]
        print(f"  {option_id}: {option.description} (score: {score:.2f})")
