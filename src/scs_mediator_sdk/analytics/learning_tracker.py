"""
Learning Outcomes Tracker

Tracks participant learning over multiple sessions,
identifies patterns, and provides personalized recommendations.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
import json


@dataclass
class SessionSummary:
    """Summary of a single session"""
    session_id: str
    timestamp: str
    scenario_name: str
    difficulty: str
    process_score: float
    outcome_score: float
    duration_minutes: int
    concepts_practiced: List[str] = field(default_factory=list)


@dataclass
class ConceptMastery:
    """Mastery level for a concept"""
    concept_name: str
    attempts: int
    success_rate: float
    mastery_level: str  # novice, intermediate, expert
    last_practiced: str
    trend: str  # improving, stable, declining


class LearningOutcomesTracker:
    """
    Tracks learning outcomes across multiple sessions

    Provides:
    - Progress tracking
    - Concept mastery assessment
    - Personalized recommendations
    - Achievement tracking
    """

    def __init__(self, participant_id: str):
        self.participant_id = participant_id
        self.sessions: List[SessionSummary] = []
        self.concept_mastery: Dict[str, ConceptMastery] = {}
        self.achievements: List[str] = []

    def add_session(self, session: SessionSummary):
        """Record a completed session"""
        self.sessions.append(session)

        # Update concept mastery
        for concept in session.concepts_practiced:
            self._update_concept_mastery(concept, session.process_score)

        # Check for achievements
        self._check_achievements()

    def _update_concept_mastery(self, concept: str, session_score: float):
        """Update mastery level for a concept"""
        if concept not in self.concept_mastery:
            self.concept_mastery[concept] = ConceptMastery(
                concept_name=concept,
                attempts=0,
                success_rate=0.0,
                mastery_level="novice",
                last_practiced=datetime.now().isoformat(),
                trend="stable"
            )

        mastery = self.concept_mastery[concept]
        mastery.attempts += 1

        # Update success rate (exponential moving average)
        alpha = 0.3
        success = 1.0 if session_score >= 0.7 else 0.0
        mastery.success_rate = alpha * success + (1 - alpha) * mastery.success_rate

        # Update mastery level
        if mastery.success_rate >= 0.8 and mastery.attempts >= 3:
            mastery.mastery_level = "expert"
        elif mastery.success_rate >= 0.6 and mastery.attempts >= 2:
            mastery.mastery_level = "intermediate"
        else:
            mastery.mastery_level = "novice"

        # Determine trend
        if mastery.attempts >= 3:
            recent_scores = [s.process_score for s in self.sessions[-3:] if concept in s.concepts_practiced]
            if len(recent_scores) >= 2:
                if recent_scores[-1] > recent_scores[0] + 0.1:
                    mastery.trend = "improving"
                elif recent_scores[-1] < recent_scores[0] - 0.1:
                    mastery.trend = "declining"
                else:
                    mastery.trend = "stable"

        mastery.last_practiced = datetime.now().isoformat()

    def _check_achievements(self):
        """Check for unlocked achievements"""
        # First session
        if len(self.sessions) == 1:
            self.achievements.append("First Steps: Completed first mediation session")

        # Consistent practice
        if len(self.sessions) >= 5:
            if "Persistent Practitioner: 5+ sessions" not in self.achievements:
                self.achievements.append("Persistent Practitioner: 5+ sessions")

        # High performance
        recent_avg = sum(s.process_score for s in self.sessions[-3:]) / min(3, len(self.sessions))
        if recent_avg >= 0.85:
            if "Excellence: 3 consecutive strong performances" not in self.achievements:
                self.achievements.append("Excellence: 3 consecutive strong performances")

        # Concept mastery
        expert_concepts = [c for c, m in self.concept_mastery.items() if m.mastery_level == "expert"]
        if len(expert_concepts) >= 3:
            if "Master Mediator: Expert in 3+ concepts" not in self.achievements:
                self.achievements.append("Master Mediator: Expert in 3+ concepts")

        # Scenario variety
        unique_scenarios = len(set(s.scenario_name for s in self.sessions))
        if unique_scenarios >= 4:
            if "Versatile: Completed 4+ different scenarios" not in self.achievements:
                self.achievements.append("Versatile: Completed 4+ different scenarios")

    def get_progress_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive progress report

        Returns:
            - Overall progress metrics
            - Concept-by-concept mastery
            - Trend analysis
            - Personalized recommendations
        """
        if not self.sessions:
            return {
                'status': 'No sessions completed yet',
                'recommendations': ['Start with a beginner-level scenario']
            }

        # Overall metrics
        avg_process_score = sum(s.process_score for s in self.sessions) / len(self.sessions)
        avg_outcome_score = sum(s.outcome_score for s in self.sessions) / len(self.sessions)

        # Recent trend
        if len(self.sessions) >= 3:
            recent_avg = sum(s.process_score for s in self.sessions[-3:]) / 3
            early_avg = sum(s.process_score for s in self.sessions[:3]) / 3
            improvement = recent_avg - early_avg
        else:
            improvement = 0

        # Identify strengths and growth areas
        strengths = [
            c for c, m in self.concept_mastery.items()
            if m.mastery_level in ["intermediate", "expert"]
        ]
        growth_areas = [
            c for c, m in self.concept_mastery.items()
            if m.mastery_level == "novice" and m.attempts >= 2
        ]

        # Generate recommendations
        recommendations = self._generate_recommendations(strengths, growth_areas, improvement)

        return {
            'participant_id': self.participant_id,
            'total_sessions': len(self.sessions),
            'average_process_score': avg_process_score,
            'average_outcome_score': avg_outcome_score,
            'improvement_trend': 'improving' if improvement > 0.1 else 'stable' if improvement > -0.1 else 'declining',
            'improvement_amount': improvement,
            'concept_mastery': {
                c: {
                    'level': m.mastery_level,
                    'success_rate': m.success_rate,
                    'attempts': m.attempts,
                    'trend': m.trend
                }
                for c, m in self.concept_mastery.items()
            },
            'strengths': strengths,
            'growth_areas': growth_areas,
            'achievements': self.achievements,
            'recommendations': recommendations,
            'next_challenge': self._suggest_next_challenge(strengths, growth_areas, avg_process_score)
        }

    def _generate_recommendations(
        self,
        strengths: List[str],
        growth_areas: List[str],
        improvement: float
    ) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []

        # Based on improvement trend
        if improvement > 0.15:
            recommendations.append("Great progress! Consider moving to more complex scenarios.")
        elif improvement < -0.1:
            recommendations.append("Review fundamentals. Focus on one concept at a time.")

        # Based on growth areas
        if growth_areas:
            top_growth_area = growth_areas[0]
            recommendations.append(f"Focus on improving: {top_growth_area}")

        # Based on strengths
        if len(strengths) >= 3:
            recommendations.append("Strong foundation - try advanced scenarios with multiple parties")

        # Specific recommendations
        if 'power_balancing' in growth_areas:
            recommendations.append("Study power asymmetry management techniques")
        if 'intervention_timing' in growth_areas:
            recommendations.append("Review when to use different intervention types")
        if 'phase_completion' in growth_areas:
            recommendations.append("Practice following Moore's 6-phase process systematically")

        return recommendations[:5]  # Top 5

    def _suggest_next_challenge(
        self,
        strengths: List[str],
        growth_areas: List[str],
        avg_score: float
    ) -> Dict[str, Any]:
        """Suggest next appropriate challenge"""
        if avg_score >= 0.8 and len(strengths) >= 4:
            return {
                'difficulty': 'expert',
                'scenario_type': 'multilateral',
                'focus': 'Complex power dynamics and spoilers',
                'reason': 'Your strong performance indicates readiness for advanced challenges'
            }
        elif avg_score >= 0.6 and len(strengths) >= 2:
            return {
                'difficulty': 'intermediate',
                'scenario_type': 'trilateral',
                'focus': 'Coalition building and package deals',
                'reason': 'Build on your strengths while expanding skills'
            }
        else:
            return {
                'difficulty': 'beginner',
                'scenario_type': 'bilateral',
                'focus': growth_areas[0] if growth_areas else 'Basic mediation process',
                'reason': 'Strengthen fundamentals before advancing'
            }

    def save_progress(self, filepath: str):
        """Save progress to JSON file"""
        data = {
            'participant_id': self.participant_id,
            'sessions': [vars(s) for s in self.sessions],
            'concept_mastery': {
                k: vars(v) for k, v in self.concept_mastery.items()
            },
            'achievements': self.achievements
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_progress(cls, filepath: str) -> LearningOutcomesTracker:
        """Load progress from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        tracker = cls(data['participant_id'])

        # Restore sessions
        for s_data in data.get('sessions', []):
            tracker.sessions.append(SessionSummary(**s_data))

        # Restore concept mastery
        for c_name, c_data in data.get('concept_mastery', {}).items():
            tracker.concept_mastery[c_name] = ConceptMastery(**c_data)

        tracker.achievements = data.get('achievements', [])

        return tracker
