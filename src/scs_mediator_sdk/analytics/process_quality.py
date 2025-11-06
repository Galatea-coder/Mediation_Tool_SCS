"""
Process Quality Analysis

Evaluates the quality of the mediation process itself,
including strategy choices, timing of interventions, and
procedural effectiveness.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import numpy as np
from enum import Enum


class ProcessMetric(Enum):
    """Key process quality metrics"""
    INTERVENTION_TIMING = "intervention_timing"
    STRATEGY_APPROPRIATENESS = "strategy_appropriateness"
    COMMUNICATION_EFFECTIVENESS = "communication_effectiveness"
    POWER_BALANCING = "power_balancing"
    CULTURAL_SENSITIVITY = "cultural_sensitivity"
    PHASE_COMPLETION = "phase_completion"


@dataclass
class ProcessScore:
    """Score for a process metric"""
    metric: ProcessMetric
    score: float  # 0-1
    explanation: str
    recommendations: List[str] = field(default_factory=list)


@dataclass
class InterventionRecord:
    """Record of a mediator intervention"""
    round_num: int
    intervention_type: str
    intervention_id: str
    timing: float  # 0-1 (early to late in process)
    context: Dict[str, Any]
    outcome: Optional[str] = None


class ProcessQualityAnalyzer:
    """
    Analyzes the quality of mediation process

    Evaluates:
    - Did mediator follow Moore's 6-phase structure?
    - Were interventions timely and appropriate?
    - Was power balanced effectively?
    - Was cultural sensitivity demonstrated?
    """

    def __init__(self):
        self.interventions: List[InterventionRecord] = []
        self.phase_completions: Dict[str, bool] = {}
        self.process_timeline: List[Dict[str, Any]] = []

    def record_intervention(self, intervention: InterventionRecord):
        """Record a mediator intervention"""
        self.interventions.append(intervention)

    def record_phase_completion(self, phase: str, completed: bool):
        """Record phase completion"""
        self.phase_completions[phase] = completed

    def analyze(self) -> Dict[str, Any]:
        """
        Perform comprehensive process quality analysis

        Returns scores, explanations, and recommendations
        """
        scores = {}

        # 1. Intervention Timing
        scores['intervention_timing'] = self._analyze_intervention_timing()

        # 2. Strategy Appropriateness
        scores['strategy_appropriateness'] = self._analyze_strategy_appropriateness()

        # 3. Phase Completion
        scores['phase_completion'] = self._analyze_phase_completion()

        # 4. Power Balancing
        scores['power_balancing'] = self._analyze_power_balancing()

        # 5. Overall Process Score
        overall_score = np.mean([s.score for s in scores.values()])

        return {
            'overall_score': overall_score,
            'detailed_scores': scores,
            'grade': self._score_to_grade(overall_score),
            'key_strengths': self._identify_strengths(scores),
            'areas_for_improvement': self._identify_improvements(scores),
            'next_steps': self._generate_next_steps(scores)
        }

    def _analyze_intervention_timing(self) -> ProcessScore:
        """
        Analyze whether interventions were well-timed

        Early game: procedural interventions
        Mid game: substantive interventions
        Late game: pressure/deadline interventions
        """
        if not self.interventions:
            return ProcessScore(
                metric=ProcessMetric.INTERVENTION_TIMING,
                score=0.5,
                explanation="No interventions recorded",
                recommendations=["Try using mediator interventions during the session"]
            )

        timing_scores = []
        issues = []

        for intervention in self.interventions:
            timing = intervention.timing
            itype = intervention.intervention_type

            # Expected timing for each type
            if itype == "procedural":
                # Should be early (0-0.4)
                optimal = timing < 0.4
                timing_scores.append(1.0 if optimal else 0.6)
                if not optimal:
                    issues.append(f"Procedural intervention at {timing:.0%} (better early)")

            elif itype == "substantive":
                # Should be mid (0.3-0.7)
                optimal = 0.3 <= timing <= 0.7
                timing_scores.append(1.0 if optimal else 0.7)
                if not optimal:
                    issues.append(f"Substantive intervention at {timing:.0%} (better mid-process)")

            elif itype == "manipulative" or itype == "pressure":
                # Should be late (0.6-1.0)
                optimal = timing > 0.6
                timing_scores.append(1.0 if optimal else 0.6)
                if not optimal:
                    issues.append(f"Pressure tactic at {timing:.0%} (better late)")

        avg_score = np.mean(timing_scores) if timing_scores else 0.5

        recommendations = []
        if avg_score < 0.7:
            recommendations.append("Review timing guidelines for different intervention types")
            recommendations.append("Consider the phase of mediation when choosing interventions")
        if issues:
            recommendations.extend(issues[:2])  # Top 2 issues

        explanation = f"Analyzed {len(self.interventions)} interventions. "
        if avg_score >= 0.8:
            explanation += "Excellent timing overall."
        elif avg_score >= 0.6:
            explanation += "Good timing with some room for improvement."
        else:
            explanation += "Several interventions could have been better timed."

        return ProcessScore(
            metric=ProcessMetric.INTERVENTION_TIMING,
            score=avg_score,
            explanation=explanation,
            recommendations=recommendations
        )

    def _analyze_strategy_appropriateness(self) -> ProcessScore:
        """
        Analyze whether mediator strategies matched the situation

        Facilitative: for cooperative parties
        Formulative: when parties need help generating options
        Manipulative: when power imbalance or impasse
        """
        if not self.interventions:
            return ProcessScore(
                metric=ProcessMetric.STRATEGY_APPROPRIATENESS,
                score=0.5,
                explanation="No strategy data available",
                recommendations=[]
            )

        # Analyze strategy mix
        strategy_counts = {}
        for intervention in self.interventions:
            strategy = intervention.context.get('strategy', 'unknown')
            strategy_counts[strategy] = strategy_counts.get(strategy, 0) + 1

        # Ideal: use all three strategies appropriately
        strategies_used = len(strategy_counts)

        if strategies_used >= 2:
            score = 0.85
            explanation = "Good strategic diversity - used multiple approaches."
            recommendations = []
        elif strategies_used == 1:
            score = 0.65
            only_strategy = list(strategy_counts.keys())[0]
            explanation = f"Relied primarily on {only_strategy} strategy."
            recommendations = ["Try incorporating other strategy types for different situations"]
        else:
            score = 0.5
            explanation = "Limited strategic variety."
            recommendations = ["Explore facilitative, formulative, and manipulative strategies"]

        return ProcessScore(
            metric=ProcessMetric.STRATEGY_APPROPRIATENESS,
            score=score,
            explanation=explanation,
            recommendations=recommendations
        )

    def _analyze_phase_completion(self) -> ProcessScore:
        """
        Analyze whether mediator completed all phases

        Moore's 6 phases should all be addressed
        """
        phases = ['phase_1', 'phase_2', 'phase_3', 'phase_4', 'phase_5', 'phase_6']
        completed_count = sum(1 for p in phases if self.phase_completions.get(p, False))

        score = completed_count / len(phases)

        if score >= 0.83:  # 5+ phases
            explanation = "Excellent phase coverage - addressed all/most phases."
            recommendations = []
        elif score >= 0.5:  # 3+ phases
            explanation = f"Completed {completed_count}/6 phases."
            missing = [p for p in phases if not self.phase_completions.get(p, False)]
            recommendations = [f"Consider incorporating {missing[0].replace('_', ' ')}"]
        else:
            explanation = f"Only completed {completed_count}/6 phases."
            recommendations = [
                "Follow Moore's 6-phase structure more closely",
                "Ensure pre-mediation assessment is done (Phase 1-2)",
                "Don't skip directly to bargaining (Phase 5)"
            ]

        return ProcessScore(
            metric=ProcessMetric.PHASE_COMPLETION,
            score=score,
            explanation=explanation,
            recommendations=recommendations
        )

    def _analyze_power_balancing(self) -> ProcessScore:
        """Analyze whether mediator balanced power asymmetries"""
        # Look for power-balancing interventions
        power_interventions = [i for i in self.interventions if i.intervention_type == "power_balancing"]

        if len(power_interventions) >= 2:
            score = 0.9
            explanation = "Actively managed power dynamics."
            recommendations = []
        elif len(power_interventions) == 1:
            score = 0.7
            explanation = "Some attention to power balancing."
            recommendations = ["Consider additional power-balancing techniques"]
        else:
            score = 0.5
            explanation = "Limited focus on power dynamics."
            recommendations = [
                "Assess power asymmetries early",
                "Use empowerment interventions for weaker parties",
                "Consider procedural protections"
            ]

        return ProcessScore(
            metric=ProcessMetric.POWER_BALANCING,
            score=score,
            explanation=explanation,
            recommendations=recommendations
        )

    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 0.9:
            return "A"
        elif score >= 0.8:
            return "B+"
        elif score >= 0.7:
            return "B"
        elif score >= 0.6:
            return "C+"
        elif score >= 0.5:
            return "C"
        else:
            return "D"

    def _identify_strengths(self, scores: Dict[str, ProcessScore]) -> List[str]:
        """Identify top strengths"""
        strengths = []
        sorted_scores = sorted(scores.items(), key=lambda x: x[1].score, reverse=True)

        for metric_name, process_score in sorted_scores[:2]:
            if process_score.score >= 0.75:
                strengths.append(f"{process_score.metric.value}: {process_score.explanation}")

        return strengths

    def _identify_improvements(self, scores: Dict[str, ProcessScore]) -> List[str]:
        """Identify areas for improvement"""
        improvements = []
        sorted_scores = sorted(scores.items(), key=lambda x: x[1].score)

        for metric_name, process_score in sorted_scores[:2]:
            if process_score.score < 0.75:
                improvements.extend(process_score.recommendations[:2])

        return improvements

    def _generate_next_steps(self, scores: Dict[str, ProcessScore]) -> List[str]:
        """Generate personalized next steps"""
        overall_avg = np.mean([s.score for s in scores.values()])

        next_steps = []

        if overall_avg >= 0.8:
            next_steps.append("Try a more complex scenario with additional parties")
            next_steps.append("Experiment with advanced intervention techniques")
        elif overall_avg >= 0.6:
            next_steps.append("Review feedback and try this scenario again")
            next_steps.append("Focus on the areas marked for improvement")
        else:
            next_steps.append("Review Moore's 6-phase process framework")
            next_steps.append("Practice with a simpler bilateral scenario")
            next_steps.append("Study the mediator toolkit interventions")

        # Add specific recommendations from low-scoring areas
        for metric_name, score in scores.items():
            if score.score < 0.6 and score.recommendations:
                next_steps.append(score.recommendations[0])

        return next_steps[:4]  # Top 4
