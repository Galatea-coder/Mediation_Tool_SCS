"""
Mediator Toolkit: Intervention Strategies and Tactics

Based on:
- UN DPPA (2017). Guidance for Effective Mediation
- Moore, C. W. (2014). The Mediation Process
- Mnookin, R., et al. (2000). Beyond Winning
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from enum import Enum
import random


class MediationStrategy(Enum):
    """Three main mediation strategies (Moore)"""
    FACILITATIVE = "facilitative"    # Process management, neutral facilitation
    FORMULATIVE = "formulative"      # Substantive proposals, single-text procedure
    MANIPULATIVE = "manipulative"    # Pressure, incentives, deadlines


class InterventionType(Enum):
    """Categories of mediator interventions"""
    PROCEDURAL = "procedural"              # Control of process
    SUBSTANTIVE = "substantive"            # Content suggestions
    COMMUNICATION = "communication"        # Facilitation and reframing
    POWER_BALANCING = "power_balancing"    # Equalizing power dynamics
    CULTURAL = "cultural"                  # Cultural sensitivity adaptations


@dataclass
class Intervention:
    """A specific mediator intervention"""
    intervention_id: str
    intervention_type: InterventionType
    strategy: MediationStrategy
    description: str
    
    # When to use
    conditions: List[str] = field(default_factory=list)
    timing: str = ""  # early, middle, late, any
    
    # How to implement
    steps: List[str] = field(default_factory=list)
    talking_points: List[str] = field(default_factory=list)
    
    # Expected outcomes
    intended_effects: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    
    # Effectiveness tracking
    success_indicators: List[str] = field(default_factory=list)


class MediatorToolkit:
    """
    Comprehensive toolkit of mediator interventions
    Organized by type and strategy
    """
    
    def __init__(self):
        self.interventions: Dict[str, Intervention] = {}
        self._initialize_interventions()
    
    def _initialize_interventions(self):
        """Load standard intervention library"""
        
        # PROCEDURAL INTERVENTIONS
        self._add_intervention(Intervention(
            intervention_id="PROC_001",
            intervention_type=InterventionType.PROCEDURAL,
            strategy=MediationStrategy.FACILITATIVE,
            description="Establish negotiation ground rules",
            conditions=["Start of mediation", "Parties lack structure"],
            timing="early",
            steps=[
                "Propose ground rules collaboratively",
                "Get explicit agreement from all parties",
                "Document rules in writing",
                "Post rules visibly during sessions"
            ],
            talking_points=[
                "To make our discussions productive, let's agree on some basic ground rules",
                "What principles would help us work together effectively?",
                "Can we all commit to these guidelines?"
            ],
            intended_effects=["Create safe space", "Set expectations", "Enable accountability"],
            risks=["May seem too formal", "Parties may reject mediator control"],
            success_indicators=["Parties follow rules", "Fewer disruptions", "Improved civility"]
        ))
        
        self._add_intervention(Intervention(
            intervention_id="PROC_002",
            intervention_type=InterventionType.PROCEDURAL,
            strategy=MediationStrategy.FACILITATIVE,
            description="Call strategic break/caucus",
            conditions=["Tensions rising", "Impasse reached", "Party needs to consult"],
            timing="any",
            steps=[
                "Recognize signs of unproductive discussion",
                "Suggest break to all parties",
                "Set clear time limit",
                "Use break for private consultations if needed"
            ],
            talking_points=[
                "This might be a good time to take a break and reflect",
                "Let's pause here and reconvene in 20 minutes",
                "I'd like to meet separately with each party before we continue"
            ],
            intended_effects=["Reduce tension", "Allow reflection", "Enable strategy adjustment"],
            risks=["May lose momentum", "Parties may harden positions during break"],
            success_indicators=["Parties return calmer", "New ideas emerge", "Willingness to continue"]
        ))
        
        self._add_intervention(Intervention(
            intervention_id="PROC_003",
            intervention_type=InterventionType.PROCEDURAL,
            strategy=MediationStrategy.MANIPULATIVE,
            description="Set deadline for agreement",
            conditions=["Negotiations dragging", "External deadline approaching"],
            timing="middle",
            steps=[
                "Explain rationale for deadline",
                "Set specific date and time",
                "Clarify consequences of missing deadline",
                "Intensify schedule as deadline approaches"
            ],
            talking_points=[
                "We have limited time to reach agreement",
                "Let me suggest we aim to conclude by [date]",
                "What happens if we don't reach agreement by then?"
            ],
            intended_effects=["Create urgency", "Force decisions", "Overcome procrastination"],
            risks=["May appear coercive", "Could lead to poor agreements", "May backfire"],
            success_indicators=["Accelerated pace", "Increased concessions", "Agreement reached"]
        ))
        
        # SUBSTANTIVE INTERVENTIONS
        self._add_intervention(Intervention(
            intervention_id="SUBST_001",
            intervention_type=InterventionType.SUBSTANTIVE,
            strategy=MediationStrategy.FORMULATIVE,
            description="Single-text procedure",
            conditions=["Multiple parties", "Complex issues", "Bilateral negotiation ineffective"],
            timing="middle",
            steps=[
                "Draft initial proposal incorporating all interests",
                "Present as mediator's proposal (not party proposal)",
                "Solicit criticisms from all parties",
                "Revise text based on feedback",
                "Iterate until objections minimized",
                "Present final text as package (no cherry-picking)"
            ],
            talking_points=[
                "Let me draft a proposal that tries to balance everyone's interests",
                "This is just a starting point - please tell me what doesn't work",
                "I'll revise based on your input, but the final text must be accepted or rejected as a whole"
            ],
            intended_effects=["Avoid positional bargaining", "Focus on interests", "Build consensus"],
            risks=["Mediator proposal may anchor expectations", "Parties may reject mediator authority"],
            success_indicators=["Objections decrease with iterations", "Parties engage constructively", "Convergence toward agreement"]
        ))
        
        self._add_intervention(Intervention(
            intervention_id="SUBST_002",
            intervention_type=InterventionType.SUBSTANTIVE,
            strategy=MediationStrategy.FORMULATIVE,
            description="Bridging proposal",
            conditions=["Parties at impasse", "Small gap between positions", "Interests potentially compatible"],
            timing="middle",
            steps=[
                "Identify underlying interests behind positions",
                "Find creative solution that satisfies both interests",
                "Frame as mediator insight, not party concession",
                "Present to both parties simultaneously or through shuttle"
            ],
            talking_points=[
                "I notice you both need [common interest]",
                "What if we approached it this way...",
                "This might give you both what you really need"
            ],
            intended_effects=["Break impasse", "Reframe positions as compatible", "Enable face-saving"],
            risks=["Parties may reject as unrealistic", "May seem to favor one side"],
            success_indicators=["Parties consider proposal seriously", "Discussion moves forward", "New options emerge"]
        ))
        
        self._add_intervention(Intervention(
            intervention_id="SUBST_003",
            intervention_type=InterventionType.SUBSTANTIVE,
            strategy=MediationStrategy.FORMULATIVE,
            description="Reality testing",
            conditions=["Unrealistic expectations", "Parties need to understand consequences"],
            timing="middle",
            steps=[
                "Ask questions that prompt critical thinking",
                "Introduce objective information/expertise",
                "Explore consequences of no agreement",
                "Compare to similar cases/outcomes",
                "Avoid being judgmental"
            ],
            talking_points=[
                "How do you think the other side will respond to that proposal?",
                "What happens if we can't reach agreement?",
                "Let me share what happened in similar situations...",
                "Have you considered...?"
            ],
            intended_effects=["Adjust expectations", "Increase realism", "Strengthen BATNAs"],
            risks=["May seem to favor other side", "Could offend party", "May appear directive"],
            success_indicators=["Parties acknowledge realities", "Expectations adjust", "More reasonable proposals"]
        ))
        
        # COMMUNICATION INTERVENTIONS
        self._add_intervention(Intervention(
            intervention_id="COMM_001",
            intervention_type=InterventionType.COMMUNICATION,
            strategy=MediationStrategy.FACILITATIVE,
            description="Active listening and reflection",
            conditions=["Party feels unheard", "Emotions running high", "Need to build empathy"],
            timing="any",
            steps=[
                "Listen without interrupting",
                "Reflect back what you heard",
                "Validate emotions (not positions)",
                "Check understanding",
                "Ask for other party's reaction"
            ],
            talking_points=[
                "Let me make sure I understand what you're saying...",
                "It sounds like you feel [emotion] because [reason]",
                "Is that accurate?",
                "How does that land with you, [other party]?"
            ],
            intended_effects=["Build trust", "Demonstrate understanding", "Reduce tension"],
            risks=["May appear to side with speaker", "Time-consuming"],
            success_indicators=["Party feels heard", "Tension decreases", "Willingness to reciprocate"]
        ))
        
        self._add_intervention(Intervention(
            intervention_id="COMM_002",
            intervention_type=InterventionType.COMMUNICATION,
            strategy=MediationStrategy.FACILITATIVE,
            description="Reframing from positions to interests",
            conditions=["Parties stuck in positions", "Hostility in language", "Need shift in perspective"],
            timing="any",
            steps=[
                "Identify underlying interest behind position",
                "Rephrase in neutral, forward-looking terms",
                "Remove inflammatory language",
                "Focus on needs and concerns, not demands"
            ],
            talking_points=[
                "So if I understand correctly, your concern is really about [interest]?",
                "It seems like you both need [common interest]",
                "Let me rephrase that in a different way..."
            ],
            intended_effects=["Reduce hostility", "Reveal common ground", "Enable problem-solving"],
            risks=["Party may reject reframing", "May lose nuance"],
            success_indicators=["Parties adopt interest language", "Hostility decreases", "Options expand"]
        ))
        
        self._add_intervention(Intervention(
            intervention_id="COMM_003",
            intervention_type=InterventionType.COMMUNICATION,
            strategy=MediationStrategy.FACILITATIVE,
            description="Shuttle diplomacy",
            conditions=["High tension", "Face-saving needed", "Parties refuse direct dialogue"],
            timing="any",
            steps=[
                "Meet separately with each party",
                "Carry messages and proposals between them",
                "Test ideas without commitment",
                "Build trust incrementally",
                "Eventually bring parties together"
            ],
            talking_points=[
                "Let me talk to each of you separately first",
                "If they were willing to [X], would you consider [Y]?",
                "I think there may be a way forward - let me check with them"
            ],
            intended_effects=["Enable communication when direct talks impossible", "Test proposals safely", "Build momentum"],
            risks=["Time-intensive", "Parties may become dependent on mediator", "Mediator may be manipulated"],
            success_indicators=["Positions soften", "Trust in mediator grows", "Direct dialogue becomes possible"]
        ))
        
        # POWER BALANCING INTERVENTIONS
        self._add_intervention(Intervention(
            intervention_id="POWER_001",
            intervention_type=InterventionType.POWER_BALANCING,
            strategy=MediationStrategy.FACILITATIVE,
            description="Procedural empowerment of weaker party",
            conditions=["Clear power asymmetry", "Weaker party disadvantaged", "Fairness concerns"],
            timing="early",
            steps=[
                "Ensure equal speaking time",
                "Provide technical assistance to weaker party",
                "Allow caucuses for consultation",
                "Enforce ground rules strictly",
                "Prevent intimidation or coercion"
            ],
            talking_points=[
                "Let's make sure everyone has a chance to speak",
                "Would it help to have an expert review this for you?",
                "I want to ensure this is a fair process for all"
            ],
            intended_effects=["Level playing field", "Increase weaker party confidence", "Improve legitimacy"],
            risks=["Stronger party may resent", "May appear biased", "Could be seen as ineffective"],
            success_indicators=["Weaker party participates fully", "Power gap narrows", "More balanced agreement"]
        ))
        
        self._add_intervention(Intervention(
            intervention_id="POWER_002",
            intervention_type=InterventionType.POWER_BALANCING,
            strategy=MediationStrategy.MANIPULATIVE,
            description="Leverage third-party pressure on stronger party",
            conditions=["Stronger party being unreasonable", "Third parties available", "Need to shift dynamics"],
            timing="middle",
            steps=[
                "Identify relevant third parties (allies, donors, public opinion)",
                "Communicate consequences of no agreement",
                "Facilitate third-party statements or engagement",
                "Use reputational concerns"
            ],
            talking_points=[
                "How do you think [ally/international community] will view this?",
                "There may be consequences if we can't resolve this...",
                "Perhaps we should involve [third party]?"
            ],
            intended_effects=["Constrain stronger party", "Create incentive for fairness", "Shift bargaining power"],
            risks=["May backfire", "Could escalate conflict", "Damages mediator neutrality"],
            success_indicators=["Stronger party moderates demands", "More balanced proposals", "Movement toward agreement"]
        ))
        
        # CULTURAL INTERVENTIONS
        self._add_intervention(Intervention(
            intervention_id="CULT_001",
            intervention_type=InterventionType.CULTURAL,
            strategy=MediationStrategy.FACILITATIVE,
            description="Face-saving provisions",
            conditions=["High face sensitivity", "Public scrutiny", "Symbolic concessions needed"],
            timing="any",
            steps=[
                "Identify face concerns early",
                "Design process to minimize public concessions",
                "Frame agreements as mutual gains",
                "Allow time for internal consultation",
                "Control information release"
            ],
            talking_points=[
                "How can we structure this so both of you can present it positively?",
                "Perhaps we keep this confidential until we have a complete package",
                "This approach allows you both to claim success"
            ],
            intended_effects=["Enable concessions", "Maintain dignity", "Facilitate agreement"],
            risks=["May slow process", "Complexity increases"],
            success_indicators=["Parties make concessions", "Agreement presented positively", "Domestic support maintained"]
        ))
    
    def _add_intervention(self, intervention: Intervention):
        """Add intervention to toolkit"""
        self.interventions[intervention.intervention_id] = intervention
    
    def recommend_intervention(self, 
                               situation: Dict[str, Any],
                               strategy_preference: Optional[MediationStrategy] = None) -> List[Intervention]:
        """
        Recommend interventions based on current situation
        
        Args:
            situation: Dict with keys like "phase", "tension_level", "power_asymmetry", etc.
            strategy_preference: Preferred mediation strategy
        
        Returns:
            List of recommended interventions, ranked by relevance
        """
        recommendations = []
        
        phase = situation.get("phase", "middle")
        tension = situation.get("tension_level", 0.5)
        power_asymmetry = situation.get("power_asymmetry", 0.0)
        face_sensitivity = situation.get("face_sensitivity", 0.5)
        impasse = situation.get("impasse", False)
        
        for intervention in self.interventions.values():
            relevance_score = 0.0
            
            # Check timing match
            if intervention.timing == "any" or intervention.timing == phase:
                relevance_score += 0.3
            
            # Check strategy preference
            if strategy_preference and intervention.strategy == strategy_preference:
                relevance_score += 0.3
            
            # Check condition match
            if tension > 0.7 and any("tension" in c.lower() for c in intervention.conditions):
                relevance_score += 0.4
            
            if abs(power_asymmetry) > 0.5 and intervention.intervention_type == InterventionType.POWER_BALANCING:
                relevance_score += 0.4
            
            if face_sensitivity > 0.7 and intervention.intervention_type == InterventionType.CULTURAL:
                relevance_score += 0.4
            
            if impasse and "impasse" in " ".join(intervention.conditions).lower():
                relevance_score += 0.5
            
            if relevance_score > 0.5:  # Threshold
                recommendations.append((relevance_score, intervention))
        
        # Sort by relevance
        recommendations.sort(reverse=True, key=lambda x: x[0])
        
        return [intervention for _, intervention in recommendations[:5]]
    
    def get_interventions_by_type(self, intervention_type: InterventionType) -> List[Intervention]:
        """Get all interventions of a specific type"""
        return [
            intervention for intervention in self.interventions.values()
            if intervention.intervention_type == intervention_type
        ]
    
    def get_interventions_by_strategy(self, strategy: MediationStrategy) -> List[Intervention]:
        """Get all interventions for a specific strategy"""
        return [
            intervention for intervention in self.interventions.values()
            if intervention.strategy == strategy
        ]
    
    def generate_intervention_guide(self, intervention_id: str) -> str:
        """Generate detailed implementation guide for intervention"""
        if intervention_id not in self.interventions:
            return "Intervention not found"
        
        intervention = self.interventions[intervention_id]
        
        guide = f"""
INTERVENTION GUIDE: {intervention.description}
{'=' * 60}

TYPE: {intervention.intervention_type.value}
STRATEGY: {intervention.strategy.value}
TIMING: {intervention.timing}

WHEN TO USE:
{chr(10).join(f'  - {c}' for c in intervention.conditions)}

IMPLEMENTATION STEPS:
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(intervention.steps))}

TALKING POINTS:
{chr(10).join(f'  "{tp}"' for tp in intervention.talking_points)}

INTENDED EFFECTS:
{chr(10).join(f'  • {effect}' for effect in intervention.intended_effects)}

RISKS TO WATCH:
{chr(10).join(f'  ⚠ {risk}' for risk in intervention.risks)}

SUCCESS INDICATORS:
{chr(10).join(f'  ✓ {indicator}' for indicator in intervention.success_indicators)}
"""
        return guide


# Example usage
if __name__ == "__main__":
    toolkit = MediatorToolkit()
    
    print(f"Loaded {len(toolkit.interventions)} interventions")
    print(f"\nIntervention types:")
    for itype in InterventionType:
        count = len(toolkit.get_interventions_by_type(itype))
        print(f"  {itype.value}: {count} interventions")
    
    # Scenario: High tension, impasse, need for procedural control
    situation = {
        "phase": "middle",
        "tension_level": 0.8,
        "power_asymmetry": 0.3,
        "face_sensitivity": 0.6,
        "impasse": True
    }
    
    print(f"\n\nSITUATION: High tension, impasse")
    print("=" * 60)
    recommendations = toolkit.recommend_intervention(situation)
    print(f"\nRecommended {len(recommendations)} interventions:")
    for i, intervention in enumerate(recommendations, 1):
        print(f"\n{i}. {intervention.description}")
        print(f"   Type: {intervention.intervention_type.value}")
        print(f"   Strategy: {intervention.strategy.value}")
    
    # Generate detailed guide for first recommendation
    if recommendations:
        print("\n" + "=" * 60)
        print("DETAILED GUIDE FOR TOP RECOMMENDATION:")
        print(toolkit.generate_intervention_guide(recommendations[0].intervention_id))
