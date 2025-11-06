"""
Outcome Quality Analysis

Evaluates the quality of mediation outcomes including
Pareto efficiency, fairness, durability, and implementation feasibility.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List
import numpy as np


@dataclass
class OutcomeAssessment:
    """Complete outcome quality assessment"""
    overall_score: float
    pareto_efficiency: float
    fairness: float
    durability: float
    feasibility: float
    sustainability: float
    explanation: str
    strengths: List[str]
    weaknesses: List[str]


class OutcomeQualityAnalyzer:
    """
    Analyzes quality of mediation outcomes

    Evaluates multiple dimensions:
    - Pareto efficiency (can't improve without hurting someone)
    - Fairness (equitable distribution of value)
    - Durability (will it last?)
    - Feasibility (can it be implemented?)
    - Sustainability (environmental/social/economic)
    """

    def analyze_outcome(
        self,
        agreement: Dict[str, Any],
        utilities: Dict[str, float],
        batna_thresholds: Dict[str, float],
        simulation_results: Dict[str, Any],
        domain: str = "maritime"
    ) -> OutcomeAssessment:
        """
        Comprehensive outcome analysis

        Args:
            agreement: The agreement terms
            utilities: Party utilities from agreement
            batna_thresholds: BATNA thresholds for each party
            simulation_results: Results from ABM simulation
            domain: Conflict domain

        Returns:
            Complete outcome assessment
        """
        # 1. Pareto Efficiency
        pareto_score = self._assess_pareto_efficiency(utilities, batna_thresholds)

        # 2. Fairness
        fairness_score = self._assess_fairness(utilities, batna_thresholds)

        # 3. Durability
        durability_score = self._assess_durability(agreement, simulation_results)

        # 4. Feasibility
        feasibility_score = self._assess_feasibility(agreement, domain)

        # 5. Sustainability
        sustainability_score = self._assess_sustainability(agreement, domain)

        # Overall score (weighted average)
        overall_score = (
            pareto_score * 0.25 +
            fairness_score * 0.25 +
            durability_score * 0.25 +
            feasibility_score * 0.15 +
            sustainability_score * 0.10
        )

        # Generate explanation
        explanation = self._generate_explanation(
            overall_score, pareto_score, fairness_score,
            durability_score, feasibility_score, sustainability_score
        )

        # Identify strengths and weaknesses
        scores_dict = {
            'Pareto Efficiency': pareto_score,
            'Fairness': fairness_score,
            'Durability': durability_score,
            'Feasibility': feasibility_score,
            'Sustainability': sustainability_score
        }
        strengths = [k for k, v in scores_dict.items() if v >= 0.75]
        weaknesses = [k for k, v in scores_dict.items() if v < 0.60]

        return OutcomeAssessment(
            overall_score=overall_score,
            pareto_efficiency=pareto_score,
            fairness=fairness_score,
            durability=durability_score,
            feasibility=feasibility_score,
            sustainability=sustainability_score,
            explanation=explanation,
            strengths=strengths,
            weaknesses=weaknesses
        )

    def _assess_pareto_efficiency(
        self,
        utilities: Dict[str, float],
        batna_thresholds: Dict[str, float]
    ) -> float:
        """
        Assess Pareto efficiency

        High score if:
        - All parties above BATNA
        - At least one party close to maximum utility
        - Little "waste" (sum of utilities is high)
        """
        # All above BATNA?
        all_above_batna = all(
            utilities[p] >= batna_thresholds[p]
            for p in utilities
        )

        if not all_above_batna:
            return 0.3  # Not even individually rational

        # Surplus above BATNA
        surpluses = [utilities[p] - batna_thresholds[p] for p in utilities]
        avg_surplus = np.mean(surpluses)

        # At least one party doing well?
        max_utility = max(utilities.values())

        # Combined score
        score = 0.4  # Base for being above BATNA

        # Bonus for good average surplus
        score += min(0.3, avg_surplus * 0.6)

        # Bonus for at least one party near maximum
        if max_utility >= 0.8:
            score += 0.2

        # Bonus for high total surplus
        total_surplus = sum(surpluses)
        score += min(0.1, total_surplus * 0.05)

        return min(1.0, score)

    def _assess_fairness(
        self,
        utilities: Dict[str, float],
        batna_thresholds: Dict[str, float]
    ) -> float:
        """
        Assess fairness of outcome

        Fair if:
        - Balanced distribution of surplus
        - No party far below others
        - Proportional to power/legitimacy (if data available)
        """
        surpluses = [utilities[p] - batna_thresholds[p] for p in utilities]

        # Equal surplus is fairest (for Nash bargaining solution)
        surplus_variance = np.var(surpluses)

        # Low variance = high fairness
        fairness_from_variance = max(0, 1 - surplus_variance * 5)

        # No party left behind
        min_surplus = min(surpluses)
        fairness_from_min = max(0, min(1, min_surplus * 2))

        # Combined
        score = 0.5 * fairness_from_variance + 0.5 * fairness_from_min

        return max(0, min(1.0, score))

    def _assess_durability(
        self,
        agreement: Dict[str, Any],
        simulation_results: Dict[str, Any]
    ) -> float:
        """
        Assess likely durability of agreement

        Durable if:
        - Low incident rate in simulation
        - Declining incident trend
        - Low severity of incidents
        - Verification mechanisms present
        """
        score = 0.5  # Base score

        # Check simulation results
        if simulation_results and 'summary' in simulation_results:
            summary = simulation_results['summary']

            # Low incident rate
            incident_count = summary.get('incidents', 0)
            max_incidents = 50  # Expected baseline
            if incident_count < max_incidents * 0.5:
                score += 0.2
            elif incident_count < max_incidents:
                score += 0.1

            # Low severity
            max_severity = summary.get('max_severity', 0)
            if max_severity < 0.5:
                score += 0.15
            elif max_severity < 0.7:
                score += 0.05

        # Structural features that improve durability
        if agreement.get('monitoring_mechanism') or agreement.get('verification'):
            score += 0.1

        if agreement.get('dispute_resolution_mechanism'):
            score += 0.1

        if agreement.get('implementation_timeline'):
            score += 0.05

        return min(1.0, score)

    def _assess_feasibility(self, agreement: Dict[str, Any], domain: str) -> float:
        """
        Assess implementation feasibility

        Feasible if:
        - Clear implementation steps
        - Adequate resources
        - Political will likely
        - Technical capability exists
        """
        score = 0.6  # Assume moderately feasible by default

        # Implementation plan
        if agreement.get('implementation_timeline') or agreement.get('implementation_plan'):
            score += 0.15

        # Resources
        if agreement.get('funding_mechanism') or agreement.get('budget'):
            score += 0.1

        # Simplicity (fewer provisions = easier to implement)
        provision_count = len(agreement)
        if provision_count <= 5:
            score += 0.1
        elif provision_count > 10:
            score -= 0.1

        # Domain-specific
        if domain == "maritime":
            # Maritime agreements need enforcement capacity
            if agreement.get('enforcement_mechanism'):
                score += 0.05
        elif domain == "resource":
            # Resource agreements need technical capacity
            if agreement.get('technical_assistance'):
                score += 0.05

        return max(0, min(1.0, score))

    def _assess_sustainability(self, agreement: Dict[str, Any], domain: str) -> float:
        """
        Assess long-term sustainability

        Sustainable if:
        - Environmental protections
        - Economic viability
        - Social acceptance
        - Adaptability to change
        """
        score = 0.5

        # Environmental
        if any(k in agreement for k in ['environmental_safeguards', 'sustainability_provisions', 'conservation']):
            score += 0.15

        # Economic
        if any(k in agreement for k in ['economic_benefits', 'joint_development', 'resource_sharing']):
            score += 0.15

        # Adaptability
        if any(k in agreement for k in ['review_mechanism', 'adjustment_clause', 'renegotiation_trigger']):
            score += 0.15

        # Stakeholder buy-in
        if any(k in agreement for k in ['consultation_process', 'stakeholder_engagement']):
            score += 0.05

        return min(1.0, score)

    def _generate_explanation(
        self,
        overall: float,
        pareto: float,
        fairness: float,
        durability: float,
        feasibility: float,
        sustainability: float
    ) -> str:
        """Generate human-readable explanation"""
        grade = self._score_to_grade(overall)

        explanation = f"Overall outcome quality: {grade} ({overall:.1%}).\n\n"

        # Strengths
        if pareto >= 0.75:
            explanation += "Strong Pareto efficiency - value maximization. "
        if fairness >= 0.75:
            explanation += "Fair distribution of benefits. "
        if durability >= 0.75:
            explanation += "Likely to be durable. "

        explanation += "\n\n"

        # Weaknesses
        if pareto < 0.60:
            explanation += "Consider ways to expand value (not just divide it). "
        if fairness < 0.60:
            explanation += "Fairness concerns - some parties may feel shortchanged. "
        if durability < 0.60:
            explanation += "Durability concerns - may not last without improvements. "
        if feasibility < 0.60:
            explanation += "Implementation challenges likely. "

        return explanation

    def _score_to_grade(self, score: float) -> str:
        """Convert score to grade"""
        if score >= 0.9:
            return "A (Excellent)"
        elif score >= 0.8:
            return "B+ (Very Good)"
        elif score >= 0.7:
            return "B (Good)"
        elif score >= 0.6:
            return "C+ (Satisfactory)"
        elif score >= 0.5:
            return "C (Adequate)"
        else:
            return "D (Needs Improvement)"
