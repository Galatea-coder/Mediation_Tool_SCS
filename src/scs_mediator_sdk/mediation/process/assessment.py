"""
Moore's Mediation Process: Phase 1-2 Implementation
Pre-Mediation Assessment and Conflict Analysis Engine

Based on:
- Moore, C. W. (2014). The Mediation Process (4th ed.)
- UN DPPA (2017). Guidance for Effective Mediation
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple, Optional, Set
from enum import Enum
import numpy as np


class ConflictType(Enum):
    """Classification of conflict types"""
    TERRITORIAL = "territorial"
    RESOURCE = "resource"
    ETHNIC = "ethnic"
    POLITICAL = "political"
    ECONOMIC = "economic"
    IDEOLOGICAL = "ideological"


class ReadinessLevel(Enum):
    """Ripeness assessment for mediation"""
    NOT_READY = "not_ready"        # Hurting stalemate not reached
    POSSIBLY_READY = "possibly_ready"  # Some conditions met
    READY = "ready"                # All conditions for mediation met
    OVERRIPE = "overripe"          # Window closing, urgency high


@dataclass
class Stakeholder:
    """Individual or group with interest in conflict"""
    name: str
    type: str  # government, rebel, civil_society, business, etc.
    power_level: float = 0.5  # 0-1 scale
    legitimacy: float = 0.5  # 0-1 scale
    
    # Positions and interests
    stated_positions: List[str] = field(default_factory=list)
    underlying_interests: List[str] = field(default_factory=list)
    needs: List[str] = field(default_factory=list)  # Fundamental human needs
    
    # Relationships
    allies: List[str] = field(default_factory=list)
    adversaries: List[str] = field(default_factory=list)
    trust_level: Dict[str, float] = field(default_factory=dict)  # stakeholder_name -> trust
    
    # Capacity and constraints
    resources: Dict[str, float] = field(default_factory=dict)  # military, economic, diplomatic
    constraints: List[str] = field(default_factory=list)  # domestic politics, legal, cultural
    decision_maker: str = ""  # Who has authority
    decision_process: str = ""  # How decisions are made
    
    # Cultural context
    culture_type: str = ""  # individualist vs collectivist
    communication_style: str = ""  # high-context vs low-context
    face_sensitivity: float = 0.5  # How important is saving face? (0-1)
    time_orientation: str = ""  # long-term vs short-term


@dataclass
class ConflictContext:
    """Historical and contextual background"""
    conflict_type: ConflictType
    duration_months: int
    intensity_level: float = 0.5  # 0=latent, 1=open warfare
    
    # History
    key_events: List[Dict[str, Any]] = field(default_factory=list)
    past_agreements: List[Dict[str, Any]] = field(default_factory=list)
    previous_mediation_attempts: List[Dict[str, Any]] = field(default_factory=list)
    
    # Context factors
    economic_interdependence: float = 0.5
    power_asymmetry: float = 0.0  # -1=extreme asymmetry, 0=balanced, +1=extreme
    third_party_involvement: List[str] = field(default_factory=list)
    media_attention: float = 0.5
    domestic_pressure: Dict[str, float] = field(default_factory=dict)  # stakeholder -> pressure
    
    # Geographic and resource factors
    disputed_territory: Optional[str] = None
    disputed_resources: List[str] = field(default_factory=list)
    strategic_importance: float = 0.5


@dataclass
class RipenessAssessment:
    """Assessment of conflict ripeness for mediation"""
    overall_readiness: ReadinessLevel
    
    # Zartman's ripeness criteria
    mutually_hurting_stalemate: bool = False
    recent_catastrophe: bool = False
    impending_catastrophe: bool = False
    way_out_visible: bool = False
    
    # Party-specific readiness
    party_readiness: Dict[str, float] = field(default_factory=dict)  # 0-1 scale
    
    # Barriers to negotiation
    barriers: List[str] = field(default_factory=list)
    
    # Opportunities
    opportunities: List[str] = field(default_factory=list)
    
    # Recommended timing
    timing_recommendation: str = ""
    
    def calculate_readiness_score(self) -> float:
        """Calculate overall readiness score"""
        score = 0.0
        
        # Structural factors (40%)
        if self.mutually_hurting_stalemate:
            score += 0.15
        if self.way_out_visible:
            score += 0.15
        if self.recent_catastrophe or self.impending_catastrophe:
            score += 0.10
        
        # Party readiness (40%)
        if self.party_readiness:
            avg_readiness = np.mean(list(self.party_readiness.values()))
            score += 0.40 * avg_readiness
        
        # Opportunities vs barriers (20%)
        if len(self.opportunities) > len(self.barriers):
            score += 0.20
        elif len(self.opportunities) == len(self.barriers):
            score += 0.10
        
        return min(1.0, score)


class PreMediationAssessment:
    """
    Phase 1-2 of Moore's Model: Initial Contact, Data Collection, and Analysis
    
    Purposes:
    1. Establish mediator credibility and impartiality
    2. Build trust with all parties
    3. Gather comprehensive information about conflict
    4. Map stakeholder landscape
    5. Identify underlying interests vs. stated positions
    6. Analyze power dynamics
    7. Assess cultural and historical context
    8. Determine ripeness for mediation
    """
    
    def __init__(self, conflict_name: str):
        self.conflict_name = conflict_name
        self.stakeholders: Dict[str, Stakeholder] = {}
        self.context: Optional[ConflictContext] = None
        self.ripeness: Optional[RipenessAssessment] = None
        
        # Assessment findings
        self.power_analysis: Dict[str, Any] = {}
        self.relationship_map: Dict[Tuple[str, str], float] = {}  # (party1, party2) -> relationship quality
        self.issue_dimensions: List[Dict[str, Any]] = []
        self.cultural_factors: Dict[str, Any] = {}
        
        # Recommendations
        self.mediation_strategy_recommendations: List[str] = []
        self.risk_factors: List[str] = []
        self.success_factors: List[str] = []
    
    def add_stakeholder(self, stakeholder: Stakeholder):
        """Add stakeholder to analysis"""
        self.stakeholders[stakeholder.name] = stakeholder
    
    def set_context(self, context: ConflictContext):
        """Set conflict context"""
        self.context = context
    
    def conduct_ripeness_assessment(self) -> RipenessAssessment:
        """
        Assess whether conflict is ripe for mediation
        Based on Zartman's ripeness theory
        """
        ripeness = RipenessAssessment(overall_readiness=ReadinessLevel.NOT_READY)
        
        if not self.context:
            return ripeness
        
        # Check for mutually hurting stalemate
        # Parties perceive continuing conflict as costly and see no unilateral solution
        if self.context.intensity_level > 0.5 and self.context.duration_months > 12:
            # Long, intense conflict suggests possible stalemate
            ripeness.mutually_hurting_stalemate = True
        
        # Check for recent or impending catastrophe
        recent_events = [e for e in self.context.key_events if e.get("severity", 0) > 0.8]
        if recent_events:
            ripeness.recent_catastrophe = True
        
        # Assess if way out is visible
        # Previous agreements or mediation attempts provide templates
        if self.context.past_agreements or self.context.previous_mediation_attempts:
            ripeness.way_out_visible = True
        
        # Assess party-specific readiness
        for name, stakeholder in self.stakeholders.items():
            readiness = 0.0
            
            # Has decision-making authority been identified?
            if stakeholder.decision_maker:
                readiness += 0.3
            
            # Are interests (not just positions) identified?
            if stakeholder.underlying_interests:
                readiness += 0.3
            
            # Is there some trust or relationship?
            if any(trust > 0.3 for trust in stakeholder.trust_level.values()):
                readiness += 0.2
            
            # Are constraints manageable?
            if len(stakeholder.constraints) < 3:
                readiness += 0.2
            
            ripeness.party_readiness[name] = readiness
        
        # Identify barriers
        if self.context.power_asymmetry > 0.7:
            ripeness.barriers.append("Extreme power asymmetry")
        if self.context.media_attention > 0.8:
            ripeness.barriers.append("High media scrutiny limits flexibility")
        if self.context.intensity_level > 0.8:
            ripeness.barriers.append("Violence level too high for negotiation")
        
        # Identify opportunities
        if self.context.economic_interdependence > 0.6:
            ripeness.opportunities.append("Economic interdependence creates incentive")
        if len(self.context.third_party_involvement) > 2:
            ripeness.opportunities.append("Multiple potential mediators and guarantors")
        
        # Overall readiness determination
        readiness_score = ripeness.calculate_readiness_score()
        
        if readiness_score < 0.3:
            ripeness.overall_readiness = ReadinessLevel.NOT_READY
            ripeness.timing_recommendation = "Focus on pre-mediation capacity building"
        elif readiness_score < 0.6:
            ripeness.overall_readiness = ReadinessLevel.POSSIBLY_READY
            ripeness.timing_recommendation = "Begin exploratory talks, shuttle diplomacy"
        elif readiness_score < 0.8:
            ripeness.overall_readiness = ReadinessLevel.READY
            ripeness.timing_recommendation = "Initiate formal mediation process"
        else:
            ripeness.overall_readiness = ReadinessLevel.OVERRIPE
            ripeness.timing_recommendation = "Urgent - act now before window closes"
        
        self.ripeness = ripeness
        return ripeness
    
    def analyze_power_dynamics(self) -> Dict[str, Any]:
        """
        Analyze power relationships among stakeholders
        Multiple dimensions of power:
        - Material power (military, economic resources)
        - Legitimacy (domestic and international)
        - Strategic position (allies, location)
        - Alternative resources (BATNAs)
        """
        power_analysis = {
            "power_rankings": {},
            "power_asymmetries": [],
            "power_sources": {},
            "balancing_needs": []
        }
        
        # Calculate multi-dimensional power scores
        for name, stakeholder in self.stakeholders.items():
            power_components = {
                "material": 0.0,
                "legitimacy": stakeholder.legitimacy,
                "strategic": 0.0,
                "alternatives": 0.0
            }
            
            # Material power from resources
            if stakeholder.resources:
                power_components["material"] = np.mean(list(stakeholder.resources.values()))
            
            # Strategic power from alliances
            power_components["strategic"] = len(stakeholder.allies) * 0.2
            
            # Alternative power (would need BATNA assessment)
            power_components["alternatives"] = stakeholder.power_level  # Simplified
            
            # Overall power score (weighted average)
            weights = {"material": 0.3, "legitimacy": 0.3, "strategic": 0.2, "alternatives": 0.2}
            total_power = sum(power_components[k] * weights[k] for k in weights)
            
            power_analysis["power_rankings"][name] = total_power
            power_analysis["power_sources"][name] = power_components
        
        # Identify significant asymmetries
        power_values = list(power_analysis["power_rankings"].values())
        if power_values:
            max_power = max(power_values)
            min_power = min(power_values)
            
            if max_power - min_power > 0.5:  # Significant gap
                strongest = max(power_analysis["power_rankings"].items(), key=lambda x: x[1])
                weakest = min(power_analysis["power_rankings"].items(), key=lambda x: x[1])
                power_analysis["power_asymmetries"].append({
                    "stronger_party": strongest[0],
                    "weaker_party": weakest[0],
                    "gap": strongest[1] - weakest[1]
                })
                
                # Recommend balancing interventions
                power_analysis["balancing_needs"].append(
                    f"Empower {weakest[0]} through: expert support, coalition building, legitimacy enhancement"
                )
        
        self.power_analysis = power_analysis
        return power_analysis
    
    def identify_positions_vs_interests(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Distinguish stated positions from underlying interests
        Critical for interest-based negotiation
        """
        analysis = {}
        
        for name, stakeholder in self.stakeholders.items():
            analysis[name] = {
                "positions": stakeholder.stated_positions,
                "interests": stakeholder.underlying_interests,
                "needs": stakeholder.needs,
                "reframing_opportunities": []
            }
            
            # Identify opportunities to reframe positions as interests
            # Example: "We must control X territory" (position) 
            #       -> "We need security and resource access" (interests)
            
            if stakeholder.stated_positions and not stakeholder.underlying_interests:
                analysis[name]["reframing_opportunities"].append(
                    "Position stated but underlying interests not yet identified - conduct deeper inquiry"
                )
        
        return analysis
    
    def map_relationships(self):
        """
        Map relationships and trust levels among stakeholders
        Create relationship matrix
        """
        for name1, stakeholder1 in self.stakeholders.items():
            for name2, stakeholder2 in self.stakeholders.items():
                if name1 != name2:
                    # Relationship quality from trust levels
                    if name2 in stakeholder1.trust_level:
                        relationship_quality = stakeholder1.trust_level[name2]
                    else:
                        # Infer from allies/adversaries
                        if name2 in stakeholder1.allies:
                            relationship_quality = 0.7
                        elif name2 in stakeholder1.adversaries:
                            relationship_quality = -0.7
                        else:
                            relationship_quality = 0.0  # Neutral
                    
                    self.relationship_map[(name1, name2)] = relationship_quality
    
    def assess_cultural_factors(self) -> Dict[str, Any]:
        """
        Assess cultural context that will affect mediation approach
        Critical for avoiding Western bias
        """
        cultural_assessment = {
            "dominant_cultures": set(),
            "communication_styles": set(),
            "face_concerns": {},
            "time_orientations": set(),
            "recommendations": []
        }
        
        for name, stakeholder in self.stakeholders.items():
            if stakeholder.culture_type:
                cultural_assessment["dominant_cultures"].add(stakeholder.culture_type)
            if stakeholder.communication_style:
                cultural_assessment["communication_styles"].add(stakeholder.communication_style)
            if stakeholder.time_orientation:
                cultural_assessment["time_orientations"].add(stakeholder.time_orientation)
            
            cultural_assessment["face_concerns"][name] = stakeholder.face_sensitivity
        
        # Generate recommendations
        if "high-context" in cultural_assessment["communication_styles"]:
            cultural_assessment["recommendations"].append(
                "Use indirect communication; allow face-saving mechanisms; emphasize relationships"
            )
        
        if any(level > 0.7 for level in cultural_assessment["face_concerns"].values()):
            cultural_assessment["recommendations"].append(
                "High face sensitivity detected - use shuttle diplomacy, avoid public blame"
            )
        
        if "long-term" in cultural_assessment["time_orientations"]:
            cultural_assessment["recommendations"].append(
                "Long-term orientation - emphasize sustainable relationships over quick deals"
            )
        
        self.cultural_factors = cultural_assessment
        return cultural_assessment
    
    def generate_strategy_recommendations(self) -> List[str]:
        """
        Generate recommended mediation strategies based on assessment
        """
        recommendations = []
        
        # Based on ripeness
        if self.ripeness:
            if self.ripeness.overall_readiness == ReadinessLevel.NOT_READY:
                recommendations.append("PRE-MEDIATION: Conduct track-2 dialogues, capacity building")
            elif self.ripeness.overall_readiness == ReadinessLevel.READY:
                recommendations.append("FORMAL MEDIATION: Initiate structured negotiation process")
        
        # Based on power dynamics
        if self.power_analysis.get("power_asymmetries"):
            recommendations.append("POWER BALANCING: Use procedural interventions to empower weaker party")
        
        # Based on relationships
        hostile_relationships = sum(1 for qual in self.relationship_map.values() if qual < -0.3)
        if hostile_relationships > len(self.relationship_map) / 2:
            recommendations.append("COMMUNICATION: Begin with separate meetings (shuttle diplomacy)")
        else:
            recommendations.append("COMMUNICATION: Direct dialogue feasible with facilitation")
        
        # Based on cultural factors
        if self.cultural_factors.get("recommendations"):
            recommendations.extend(self.cultural_factors["recommendations"])
        
        self.mediation_strategy_recommendations = recommendations
        return recommendations
    
    def generate_assessment_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive pre-mediation assessment report
        """
        # Run all analyses if not done
        if not self.ripeness:
            self.conduct_ripeness_assessment()
        if not self.power_analysis:
            self.analyze_power_dynamics()
        if not self.relationship_map:
            self.map_relationships()
        if not self.cultural_factors:
            self.assess_cultural_factors()
        if not self.mediation_strategy_recommendations:
            self.generate_strategy_recommendations()
        
        report = {
            "conflict_name": self.conflict_name,
            "assessment_date": "current",
            
            "executive_summary": {
                "readiness_level": self.ripeness.overall_readiness.value if self.ripeness else "unknown",
                "recommended_timing": self.ripeness.timing_recommendation if self.ripeness else "",
                "key_challenges": self.risk_factors[:3] if self.risk_factors else [],
                "key_opportunities": self.success_factors[:3] if self.success_factors else []
            },
            
            "stakeholder_analysis": {
                "parties": {name: {
                    "type": s.type,
                    "power_level": s.power_level,
                    "legitimacy": s.legitimacy,
                    "key_interests": s.underlying_interests
                } for name, s in self.stakeholders.items()},
                "relationship_map": self.relationship_map
            },
            
            "conflict_context": {
                "type": self.context.conflict_type.value if self.context else "unknown",
                "duration_months": self.context.duration_months if self.context else 0,
                "intensity": self.context.intensity_level if self.context else 0.5
            },
            
            "ripeness_assessment": {
                "overall_score": self.ripeness.calculate_readiness_score() if self.ripeness else 0,
                "mutually_hurting_stalemate": self.ripeness.mutually_hurting_stalemate if self.ripeness else False,
                "barriers": self.ripeness.barriers if self.ripeness else [],
                "opportunities": self.ripeness.opportunities if self.ripeness else []
            },
            
            "power_analysis": self.power_analysis,
            
            "cultural_assessment": self.cultural_factors,
            
            "strategy_recommendations": self.mediation_strategy_recommendations,
            
            "risk_factors": self.risk_factors,
            "success_factors": self.success_factors
        }
        
        return report


# Example usage
if __name__ == "__main__":
    # Create assessment for a territorial dispute
    assessment = PreMediationAssessment("Border Dispute Case Study")
    
    # Add stakeholders
    country_a = Stakeholder(
        name="Country A",
        type="government",
        power_level=0.7,
        legitimacy=0.8,
        stated_positions=["Must control disputed territory"],
        underlying_interests=["Security", "National pride", "Resource access"],
        needs=["Safety", "Identity recognition"],
        adversaries=["Country B"],
        culture_type="collectivist",
        communication_style="high-context",
        face_sensitivity=0.8
    )
    
    country_b = Stakeholder(
        name="Country B",
        type="government",
        power_level=0.6,
        legitimacy=0.7,
        stated_positions=["Territory is historically ours"],
        underlying_interests=["Economic development", "Political stability", "Regional influence"],
        needs=["Economic security", "Respect"],
        adversaries=["Country A"],
        culture_type="individualist",
        communication_style="low-context",
        face_sensitivity=0.5
    )
    
    assessment.add_stakeholder(country_a)
    assessment.add_stakeholder(country_b)
    
    # Set context
    context = ConflictContext(
        conflict_type=ConflictType.TERRITORIAL,
        duration_months=36,
        intensity_level=0.6,
        economic_interdependence=0.4,
        power_asymmetry=0.3,
        disputed_territory="Border Region X"
    )
    assessment.set_context(context)
    
    # Run assessment
    ripeness = assessment.conduct_ripeness_assessment()
    print(f"Ripeness Level: {ripeness.overall_readiness.value}")
    print(f"Readiness Score: {ripeness.calculate_readiness_score():.2f}")
    print(f"Recommendation: {ripeness.timing_recommendation}")
    
    power = assessment.analyze_power_dynamics()
    print(f"\nPower Rankings: {power['power_rankings']}")
    
    strategies = assessment.generate_strategy_recommendations()
    print(f"\nRecommended Strategies:")
    for strategy in strategies:
        print(f"  - {strategy}")
    
    # Generate full report
    report = assessment.generate_assessment_report()
    print(f"\nFull Assessment Report Generated")
    print(f"Stakeholders: {len(report['stakeholder_analysis']['parties'])}")
    print(f"Strategy Recommendations: {len(report['strategy_recommendations'])}")
