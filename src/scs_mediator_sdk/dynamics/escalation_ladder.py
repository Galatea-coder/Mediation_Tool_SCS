"""
Crisis Escalation & De-escalation Dynamics for Maritime Conflicts

This module implements Herman Kahn's escalation ladder adapted for maritime conflicts,
providing tools for risk assessment and de-escalation sequencing based on Osgood's GRIT
(Graduated Reciprocation in Tension-reduction).

Part 1 of 10 Peace Mediation Enhancements.

Risk Assessment System:
- Primary: LLM-based intelligent analysis (requires Anthropic API key)
- Fallback: Comprehensive keyword-based classification (offline capable)
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
import os
import json


class EscalationLevel(Enum):
    """9-level escalation ladder for maritime conflicts"""
    LEVEL_1 = "routine_operations"           # Normal patrols, fishing
    LEVEL_2 = "increased_presence"           # More frequent patrols
    LEVEL_3 = "close_encounters"             # Deliberate proximity, shadowing
    LEVEL_4 = "verbal_warnings"              # Radio challenges, loudspeaker warnings
    LEVEL_5 = "non_lethal_actions"          # Water cannons, ramming, blockades
    LEVEL_6 = "detention_seizure"           # Arresting crew, seizing vessels
    LEVEL_7 = "shows_of_force"              # Military exercises, mobilization
    LEVEL_8 = "limited_engagement"          # Warning shots, disabling fire
    LEVEL_9 = "armed_conflict"              # Sustained combat operations


@dataclass
class EscalationEvent:
    """An action that moves up or down the ladder"""
    event_type: str
    from_level: EscalationLevel
    to_level: EscalationLevel
    actor: str
    triggers: List[str]  # What caused this
    response_options: List[str]  # Available responses
    de_escalation_paths: List[str]  # How to walk back


class EscalationManager:
    """Manages crisis escalation dynamics with LLM-enhanced assessment"""

    def __init__(self, use_llm: bool = True):
        """
        Initialize escalation manager

        Args:
            use_llm: Whether to attempt LLM-based assessment (requires ANTHROPIC_API_KEY)
        """
        self.current_level = EscalationLevel.LEVEL_1
        self.escalation_history: List[EscalationEvent] = []
        self.use_llm = use_llm
        self.thresholds: Dict[str, float] = {
            "public_outrage": 0.5,
            "military_pressure": 0.5,
            "alliance_commitment": 0.5,
            "domestic_politics": 0.5
        }

        # Check for Anthropic API key
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if self.use_llm and not self.api_key:
            print("Warning: ANTHROPIC_API_KEY not found. Falling back to keyword-based assessment.")
            self.use_llm = False

    def assess_escalation_risk(self, proposed_action: str) -> Dict:
        """
        Predict escalation risk of proposed action using LLM or enhanced keywords

        Args:
            proposed_action: Description of the proposed action

        Returns:
            Dictionary containing:
            - risk_level: Float 0-1 indicating escalation risk
            - likely_counter_escalation: List of predicted responses
            - de_escalation_windows: Available de-escalation options
            - point_of_no_return: Boolean indicating if past critical threshold
            - assessment_method: "llm" or "keywords"
        """
        # Try LLM first if enabled
        if self.use_llm and self.api_key:
            try:
                return self._assess_with_llm(proposed_action)
            except Exception as e:
                print(f"LLM assessment failed ({e}), falling back to keywords")

        # Fall back to enhanced keyword system
        return self._assess_with_keywords(proposed_action)

    def _assess_with_llm(self, proposed_action: str) -> Dict:
        """Use Claude API for intelligent escalation assessment"""
        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

        client = anthropic.Anthropic(api_key=self.api_key)

        prompt = f"""You are an expert in crisis escalation dynamics and maritime conflict. Analyze this proposed action in the South China Sea context and assess its escalation risk.

Proposed Action: "{proposed_action}"

Provide a risk assessment with:
1. Overall escalation risk (0.0-1.0 scale)
2. 2-4 likely counter-escalation responses from the other party
3. Whether this crosses the "point of no return" (true/false)

Respond in JSON format:
{{
    "risk_level": 0.0-1.0,
    "likely_counter_escalation": ["response 1", "response 2", ...],
    "point_of_no_return": true/false,
    "reasoning": "brief explanation"
}}"""

        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse Claude's response
        response_text = message.content[0].text

        # Extract JSON from response (Claude might add text before/after)
        import re
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
        if json_match:
            assessment = json.loads(json_match.group())
        else:
            raise ValueError("Could not parse JSON from Claude response")

        # Add de-escalation windows
        assessment["de_escalation_windows"] = self._find_de_escalation_paths()
        assessment["assessment_method"] = "llm"

        return assessment

    def _assess_with_keywords(self, proposed_action: str) -> Dict:
        """Enhanced keyword-based escalation assessment"""
        risk_assessment = {
            "risk_level": 0.0,
            "likely_counter_escalation": [],
            "de_escalation_windows": [],
            "point_of_no_return": False,
            "assessment_method": "keywords"
        }

        action_lower = proposed_action.lower()

        # Comprehensive keyword classification
        severity = self._classify_action_severity_enhanced(action_lower)

        # Calculate overall risk
        risk_assessment["risk_level"] = min(1.0, sum(severity.values()) / 4.0)

        # Generate counter-escalation responses based on severity
        responses = []

        if severity["military_pressure"] > 0.3:
            if severity["military_pressure"] > 0.7:
                responses.append("Major military exercises near the area")
                responses.append("Deployment of advanced weapons systems")
            else:
                responses.append("Increased naval patrols in the area")
                responses.append("Military show of force")

        if severity["public_outrage"] > 0.3:
            if severity["public_outrage"] > 0.7:
                responses.append("Mass nationalist protests and calls for retaliation")
                responses.append("Economic sanctions or trade restrictions")
            else:
                responses.append("Public condemnation and diplomatic protests")
                responses.append("Increased media coverage and public pressure")

        if severity["alliance_commitment"] > 0.3:
            responses.append("Consultation with allied nations")
            responses.append("Request for international mediation")

        if severity["domestic_politics"] > 0.3:
            responses.append("Hardline political response due to domestic pressure")
            responses.append("Government feels compelled to respond forcefully")

        # If no specific triggers, add generic response
        if not responses:
            responses.append("Proportional counter-action in the same area")
            responses.append("Increased surveillance and monitoring")

        risk_assessment["likely_counter_escalation"] = responses[:4]  # Limit to 4
        risk_assessment["de_escalation_windows"] = self._find_de_escalation_paths()

        # Point of no return check
        if severity["military_pressure"] > 0.8 or risk_assessment["risk_level"] > 0.8:
            risk_assessment["point_of_no_return"] = True

        return risk_assessment

    def _classify_action_severity_enhanced(self, action: str) -> Dict[str, float]:
        """
        Comprehensive classification of action severity across multiple dimensions

        Returns severity scores (0-1) for:
        - public_outrage: How likely to trigger public anger
        - military_pressure: Military/security threat level
        - alliance_commitment: Impact on alliances and treaties
        - domestic_politics: Domestic political pressure to respond
        """
        severity = {
            "public_outrage": 0.0,
            "military_pressure": 0.0,
            "alliance_commitment": 0.0,
            "domestic_politics": 0.0
        }

        # LEVEL 9: Armed Conflict (0.9-1.0)
        level_9_keywords = ["attack", "fire upon", "sink", "destroy", "kill", "combat",
                           "warfare", "missile", "torpedo", "bomb", "strike", "assault"]
        if any(kw in action for kw in level_9_keywords):
            severity["military_pressure"] = 0.95
            severity["public_outrage"] = 0.95
            severity["alliance_commitment"] = 0.9
            severity["domestic_politics"] = 0.95
            return severity

        # LEVEL 8: Limited Engagement (0.7-0.9)
        level_8_keywords = ["warning shot", "fire at", "disable", "targeting radar",
                           "weapons lock", "fire control", "engage"]
        if any(kw in action for kw in level_8_keywords):
            severity["military_pressure"] = 0.85
            severity["public_outrage"] = 0.75
            severity["alliance_commitment"] = 0.8
            severity["domestic_politics"] = 0.8
            return severity

        # LEVEL 7: Shows of Force (0.6-0.8)
        level_7_keywords = ["military exercise", "mobilize", "deploy destroyer",
                           "deploy frigate", "deploy warship", "carrier", "submarine",
                           "major deployment", "military buildup"]
        if any(kw in action for kw in level_7_keywords):
            severity["military_pressure"] = 0.75
            severity["public_outrage"] = 0.6
            severity["alliance_commitment"] = 0.7
            severity["domestic_politics"] = 0.65

        # LEVEL 6: Detention/Seizure (0.5-0.7)
        level_6_keywords = ["detain", "arrest", "seize", "capture", "board forcibly",
                           "impound", "confiscate", "take into custody"]
        if any(kw in action for kw in level_6_keywords):
            severity["public_outrage"] = 0.7
            severity["military_pressure"] = 0.6
            severity["domestic_politics"] = 0.75
            severity["alliance_commitment"] = 0.5

        # LEVEL 5: Non-lethal Actions (0.4-0.6)
        level_5_keywords = ["water cannon", "ram", "ramming", "collision", "blockade",
                           "block access", "prevent passage", "force away", "push back"]
        if any(kw in action for kw in level_5_keywords):
            severity["public_outrage"] = 0.6
            severity["military_pressure"] = 0.5
            severity["domestic_politics"] = 0.55
            severity["alliance_commitment"] = 0.4

        # LEVEL 4: Verbal Warnings (0.3-0.5)
        level_4_keywords = ["warning", "challenge", "demand", "order to leave",
                           "threaten", "ultimatum", "loudspeaker", "radio challenge"]
        if any(kw in action for kw in level_4_keywords):
            severity["public_outrage"] = 0.4
            severity["military_pressure"] = 0.35
            severity["domestic_politics"] = 0.4
            severity["alliance_commitment"] = 0.3

        # LEVEL 3: Close Encounters (0.2-0.4)
        level_3_keywords = ["shadow", "follow closely", "approach", "proximity",
                           "intercept", "close distance", "trail", "monitor closely"]
        if any(kw in action for kw in level_3_keywords):
            severity["military_pressure"] = 0.3
            severity["public_outrage"] = 0.25
            severity["domestic_politics"] = 0.2
            severity["alliance_commitment"] = 0.2

        # LEVEL 2: Increased Presence (0.1-0.3)
        level_2_keywords = ["increase patrol", "more frequent", "additional vessels",
                           "deploy more", "send more", "reinforce presence"]
        if any(kw in action for kw in level_2_keywords):
            severity["military_pressure"] = 0.2
            severity["public_outrage"] = 0.15
            severity["domestic_politics"] = 0.15
            severity["alliance_commitment"] = 0.1

        # Additional context modifiers
        if "military" in action or "naval" in action or "armed" in action:
            severity["military_pressure"] += 0.15
            severity["alliance_commitment"] += 0.1

        if "civilian" in action or "fishermen" in action or "fishing vessel" in action:
            severity["public_outrage"] += 0.2
            severity["domestic_politics"] += 0.15

        if "sovereignty" in action or "territorial" in action:
            severity["public_outrage"] += 0.15
            severity["domestic_politics"] += 0.2
            severity["alliance_commitment"] += 0.1

        if "disputed" in action or "contested" in action:
            severity["public_outrage"] += 0.1
            severity["domestic_politics"] += 0.1

        # Cap all values at 1.0
        for key in severity:
            severity[key] = min(1.0, severity[key])

        return severity

    def recommend_de_escalation_sequence(self) -> List[str]:
        """
        Recommend step-by-step de-escalation from current level
        Based on Osgood's GRIT (Graduated Reciprocation in Tension-reduction)

        Returns:
            List of recommended de-escalation steps in sequence
        """
        sequence = []

        # Step 1: Signal intent
        sequence.append("Public statement of de-escalation intent")

        # Step 2: Unilateral gesture
        sequence.append("Small, unilateral conciliatory action (verifiable)")

        # Step 3: Invite reciprocation
        sequence.append("Request matching gesture from other side")

        # Step 4: Gradual scaling
        sequence.append("Increase concessions if reciprocated")

        # Step 5: Maintain deterrence
        sequence.append("Keep defensive capabilities (don't appear weak)")

        return sequence

    def _find_de_escalation_paths(self) -> List[str]:
        """Identify available de-escalation options"""
        paths = []

        if self.current_level.value <= EscalationLevel.LEVEL_4.value:
            paths.append("Direct communication channels")
            paths.append("Reduce patrol frequency")

        if self.current_level.value <= EscalationLevel.LEVEL_6.value:
            paths.append("Third-party mediation")
            paths.append("Temporary restraint agreement")

        paths.append("Confidence-building measures")
        paths.append("Face-saving formula")

        return paths


# Example usage
if __name__ == "__main__":
    # Create escalation manager (will use LLM if API key available)
    manager = EscalationManager()

    print(f"Assessment method: {'LLM' if manager.use_llm else 'Keywords'}")
    print()

    # Test various actions
    test_actions = [
        "Deploy military vessels to disputed waters",
        "Send fishing boats to traditional fishing grounds",
        "Conduct freedom of navigation operation",
        "Ram and sink a foreign fishing vessel",
        "Issue radio warning to approaching vessel"
    ]

    for action in test_actions:
        print(f"\n{'='*60}")
        print(f"Action: {action}")
        print(f"{'='*60}")

        risk = manager.assess_escalation_risk(action)

        print(f"Risk Level: {risk['risk_level']:.1%}")
        print(f"Point of No Return: {risk['point_of_no_return']}")
        print(f"Assessment Method: {risk.get('assessment_method', 'unknown')}")

        if risk['likely_counter_escalation']:
            print(f"\nLikely Counter-Escalation:")
            for i, response in enumerate(risk['likely_counter_escalation'], 1):
                print(f"  {i}. {response}")

        if risk['de_escalation_windows']:
            print(f"\nDe-escalation Options:")
            for i, path in enumerate(risk['de_escalation_windows'], 1):
                print(f"  {i}. {path}")

    # Show de-escalation sequence
    print(f"\n\n{'='*60}")
    print("Recommended De-escalation Sequence (GRIT):")
    print(f"{'='*60}")
    for i, step in enumerate(manager.recommend_de_escalation_sequence(), 1):
        print(f"{i}. {step}")
