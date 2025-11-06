"""
Enhanced Agent-Based Model with Generalization

Implements:
- BDI (Belief-Desire-Intention) architecture
- Adaptive learning through Bayesian updating
- Multi-level agents (individual, group, organizational)
- Domain-agnostic incident generation
- Escalation dynamics with tipping points

Based on:
- Epstein (1999): Agent-Based Computational Models
- Cederman (2003): Modeling the Size of Wars
- BDI Architecture (Rao & Georgeff, 1995)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Callable
import random
import pandas as pd
from mesa import Model, Agent
from mesa.time import RandomActivation
import numpy as np


@dataclass
class AgentProfile:
    """Profile defining agent behavior"""
    agent_type: str
    base_aggression: float = 0.1
    risk_tolerance: float = 0.5
    rule_following: float = 0.7
    response_threshold: float = 0.5
    learning_rate: float = 0.1


class ConflictAgent(Agent):
    """
    Generalized conflict agent with BDI architecture

    Can represent:
    - Maritime: Coast Guard, Navy, Militia, Fishermen
    - Territorial: Military, Police, Civilians, Paramilitary
    - Resource: Farmers, Companies, Government agencies
    - Political: Parties, Militias, Protesters
    """

    def __init__(self, unique_id: int, model: ConflictSimulation, profile: AgentProfile):
        super().__init__(unique_id, model)
        self.profile = profile

        # BDI components
        self.beliefs: Dict[str, float] = {}  # About environment and other agents
        self.desires: List[str] = []  # Goals
        self.intentions: List[str] = []  # Committed actions

        # State
        self.aggression_level = profile.base_aggression
        self.last_action: Optional[str] = None
        self.action_history: List[str] = []

        # Learning
        self.experience: Dict[str, int] = {}  # Action -> outcome count
        self.success_rate: Dict[str, float] = {}  # Action -> success rate

    def step(self):
        """
        Agent decision-making step

        1. Update beliefs (perception)
        2. Generate options (deliberation)
        3. Select action (means-end reasoning)
        4. Execute action
        5. Learn from outcome
        """
        # 1. Update beliefs about environment
        self._update_beliefs()

        # 2. Assess if action is warranted
        action_threshold = self.profile.response_threshold

        # Adjust threshold based on agreement provisions
        if self.model.agreement:
            action_threshold = self._adjust_threshold_for_agreement(action_threshold)

        # Environmental factors affect threshold
        if self.model.context.get("high_tension", False):
            action_threshold *= 0.8  # More likely to act

        if self.model.context.get("monitoring_active", False):
            action_threshold *= 1.2  # Less likely to act (deterrence)

        # 3. Decide whether to generate incident
        if random.random() < self.aggression_level:
            # Check if threshold exceeded
            if self.aggression_level > action_threshold:
                self._generate_incident()

        # 4. Update aggression level (escalation/de-escalation dynamics)
        self._update_aggression()

    def _update_beliefs(self):
        """Update beliefs about environment through Bayesian updating"""
        # Observe model state
        self.beliefs['incident_pressure'] = self.model.incident_pressure
        self.beliefs['escalation_risk'] = self.model.escalation_risk

        # Learn from recent history
        recent_incidents = len([h for h in self.model.history if h['step'] >= self.model.schedule.steps - 10])
        self.beliefs['recent_activity'] = recent_incidents / 10.0

        # Update beliefs about effectiveness of restraint
        if self.model.agreement and len(self.model.history) < 5:
            self.beliefs['agreement_working'] = 0.8
        elif len(self.model.history) > 20:
            self.beliefs['agreement_working'] = 0.3
        else:
            self.beliefs['agreement_working'] = 0.5

    def _adjust_threshold_for_agreement(self, threshold: float) -> float:
        """Adjust action threshold based on agreement provisions"""
        agreement = self.model.agreement
        adjustment = 1.0

        # Generic agreement features
        if agreement.get("confidence_building_measures"):
            adjustment *= 1.3  # Higher threshold (less likely to act)

        if agreement.get("communication_protocol"):
            adjustment *= 1.2

        if agreement.get("monitoring_mechanism"):
            adjustment *= 1.25

        if agreement.get("penalty_provisions"):
            adjustment *= 1.15

        # Domain-specific adjustments
        domain = self.model.domain
        if domain == "maritime":
            if agreement.get("resupply_SOP"):
                sop = agreement["resupply_SOP"]
                adjustment *= 1 + (sop.get("standoff_nm", 0) * 0.05)
            if agreement.get("hotline_cues"):
                adjustment *= 1.2
        elif domain == "territorial":
            if agreement.get("buffer_zone"):
                adjustment *= 1.3
            if agreement.get("joint_patrols"):
                adjustment *= 1.15
        elif domain == "resource":
            if agreement.get("allocation_formula"):
                adjustment *= 1.2
            if agreement.get("dispute_resolution_mechanism"):
                adjustment *= 1.25

        return threshold * adjustment

    def _generate_incident(self):
        """Generate domain-appropriate incident"""
        # Select incident type based on domain
        incident_types = self.model.incident_types
        weights = [it['probability'] for it in incident_types]

        chosen_type = random.choices(incident_types, weights=weights)[0]

        # Severity influenced by agent profile and environment
        base_severity = chosen_type['severity_range']
        severity = random.uniform(base_severity[0], base_severity[1])

        # Adjust severity based on agent characteristics
        severity *= (self.aggression_level / self.profile.base_aggression)

        # Environmental amplification
        if self.model.context.get("weather_bad", False):
            severity *= 1.2
        if self.model.context.get("media_present", False):
            severity *= 0.8  # Restraint under observation

        # Record incident
        incident = {
            'step': self.model.schedule.steps,
            'agent_id': self.unique_id,
            'agent_type': self.profile.agent_type,
            'incident_type': chosen_type['name'],
            'severity': min(1.0, severity),
            'context': {
                'aggression_level': self.aggression_level,
                'beliefs': self.beliefs.copy()
            }
        }

        self.model.history.append(incident)
        self.last_action = chosen_type['name']
        self.action_history.append(chosen_type['name'])

        # Update experience
        self.experience[chosen_type['name']] = self.experience.get(chosen_type['name'], 0) + 1

    def _update_aggression(self):
        """Update aggression level (escalation/de-escalation dynamics)"""
        # Natural decay
        self.aggression_level *= 0.98

        # Influenced by model-level pressure
        self.aggression_level += self.model.incident_pressure * 0.02

        # Response to recent incidents (contagion effect)
        recent_incidents = [h for h in self.model.history if h['step'] >= self.model.schedule.steps - 5]
        if recent_incidents:
            contagion = len(recent_incidents) * 0.01
            self.aggression_level += contagion

        # Agreement effect
        if self.model.agreement and self.beliefs.get('agreement_working', 0.5) > 0.6:
            self.aggression_level *= 0.95  # De-escalation

        # Environmental factors
        if self.model.context.get("weather_bad", False):
            self.aggression_level *= 1.05

        # Bounds
        self.aggression_level = max(0.01, min(0.95, self.aggression_level))


class ConflictSimulation(Model):
    """
    Generalized conflict simulation model

    Supports multiple domains through configuration
    """

    def __init__(
        self,
        steps: int = 200,
        domain: str = "maritime",
        environment: Optional[Dict[str, Any]] = None,
        agreement: Optional[Dict[str, Any]] = None,
        agent_profiles: Optional[List[AgentProfile]] = None,
        incident_types: Optional[List[Dict[str, Any]]] = None,
        seed: Optional[int] = None
    ):
        super().__init__(seed=seed)
        self.schedule = RandomActivation(self)
        self.steps = steps
        self.domain = domain

        # Context
        self.context = environment or {}
        self.agreement = agreement or {}

        # Simulation state
        self.incident_pressure = 0.25
        self.escalation_risk = 0.3
        self.history: List[Dict[str, Any]] = []

        # Incident types (domain-specific)
        self.incident_types = incident_types or self._get_default_incident_types(domain)

        # Create agents
        if agent_profiles:
            for i, profile in enumerate(agent_profiles):
                agent = ConflictAgent(i, self, profile)
                self.schedule.add(agent)
        else:
            # Default agent creation
            default_profiles = self._get_default_agent_profiles(domain)
            for i, profile in enumerate(default_profiles):
                agent = ConflictAgent(i, self, profile)
                self.schedule.add(agent)

    def _get_default_incident_types(self, domain: str) -> List[Dict[str, Any]]:
        """Get default incident types for domain"""
        if domain == "maritime":
            return [
                {'name': 'water_cannon', 'probability': 0.35, 'severity_range': (0.2, 0.6)},
                {'name': 'ramming', 'probability': 0.20, 'severity_range': (0.5, 0.9)},
                {'name': 'detention_attempt', 'probability': 0.20, 'severity_range': (0.6, 0.95)},
                {'name': 'near_miss', 'probability': 0.25, 'severity_range': (0.1, 0.4)}
            ]
        elif domain == "territorial":
            return [
                {'name': 'border_crossing', 'probability': 0.30, 'severity_range': (0.2, 0.5)},
                {'name': 'patrol_confrontation', 'probability': 0.25, 'severity_range': (0.3, 0.7)},
                {'name': 'skirmish', 'probability': 0.15, 'severity_range': (0.6, 0.95)},
                {'name': 'civilian_incident', 'probability': 0.30, 'severity_range': (0.1, 0.4)}
            ]
        elif domain == "resource":
            return [
                {'name': 'unauthorized_extraction', 'probability': 0.35, 'severity_range': (0.2, 0.5)},
                {'name': 'infrastructure_sabotage', 'probability': 0.15, 'severity_range': (0.6, 0.9)},
                {'name': 'protest', 'probability': 0.30, 'severity_range': (0.1, 0.4)},
                {'name': 'access_denial', 'probability': 0.20, 'severity_range': (0.3, 0.6)}
            ]
        else:
            # Generic
            return [
                {'name': 'minor_violation', 'probability': 0.40, 'severity_range': (0.1, 0.4)},
                {'name': 'moderate_incident', 'probability': 0.35, 'severity_range': (0.3, 0.7)},
                {'name': 'major_incident', 'probability': 0.25, 'severity_range': (0.6, 0.95)}
            ]

    def _get_default_agent_profiles(self, domain: str) -> List[AgentProfile]:
        """Get default agent profiles for domain"""
        if domain == "maritime":
            return [
                AgentProfile("CCG", base_aggression=0.15, risk_tolerance=0.6, rule_following=0.7),
                AgentProfile("CCG", base_aggression=0.15, risk_tolerance=0.6, rule_following=0.7),
                AgentProfile("CCG", base_aggression=0.15, risk_tolerance=0.6, rule_following=0.7),
                AgentProfile("PCG", base_aggression=0.10, risk_tolerance=0.4, rule_following=0.8),
                AgentProfile("PCG", base_aggression=0.10, risk_tolerance=0.4, rule_following=0.8),
                AgentProfile("Militia", base_aggression=0.20, risk_tolerance=0.7, rule_following=0.5),
                AgentProfile("Militia", base_aggression=0.20, risk_tolerance=0.7, rule_following=0.5),
                AgentProfile("Militia", base_aggression=0.20, risk_tolerance=0.7, rule_following=0.5),
                AgentProfile("Militia", base_aggression=0.20, risk_tolerance=0.7, rule_following=0.5),
                AgentProfile("Fisher", base_aggression=0.05, risk_tolerance=0.3, rule_following=0.6),
                AgentProfile("Fisher", base_aggression=0.05, risk_tolerance=0.3, rule_following=0.6),
                AgentProfile("Fisher", base_aggression=0.05, risk_tolerance=0.3, rule_following=0.6),
                AgentProfile("Fisher", base_aggression=0.05, risk_tolerance=0.3, rule_following=0.6),
                AgentProfile("Fisher", base_aggression=0.05, risk_tolerance=0.3, rule_following=0.6),
                AgentProfile("Fisher", base_aggression=0.05, risk_tolerance=0.3, rule_following=0.6),
            ]
        elif domain == "territorial":
            return [
                AgentProfile("Military_A", base_aggression=0.12, risk_tolerance=0.5, rule_following=0.8),
                AgentProfile("Military_A", base_aggression=0.12, risk_tolerance=0.5, rule_following=0.8),
                AgentProfile("Military_A", base_aggression=0.12, risk_tolerance=0.5, rule_following=0.8),
                AgentProfile("Military_B", base_aggression=0.12, risk_tolerance=0.5, rule_following=0.8),
                AgentProfile("Military_B", base_aggression=0.12, risk_tolerance=0.5, rule_following=0.8),
                AgentProfile("Paramilitary", base_aggression=0.18, risk_tolerance=0.6, rule_following=0.6),
                AgentProfile("Paramilitary", base_aggression=0.18, risk_tolerance=0.6, rule_following=0.6),
                AgentProfile("Civilian", base_aggression=0.05, risk_tolerance=0.3, rule_following=0.7),
                AgentProfile("Civilian", base_aggression=0.05, risk_tolerance=0.3, rule_following=0.7),
                AgentProfile("Civilian", base_aggression=0.05, risk_tolerance=0.3, rule_following=0.7),
            ]
        else:
            # Generic
            return [AgentProfile(f"Agent_{i}", base_aggression=0.1, risk_tolerance=0.5) for i in range(10)]

    def step(self):
        """Execute one simulation step"""
        # Update model-level parameters
        self._update_incident_pressure()
        self._update_escalation_risk()

        # Agents act
        self.schedule.step()

    def _update_incident_pressure(self):
        """Update global incident pressure"""
        # Natural increase
        self.incident_pressure += 0.01

        # Agreement reduces pressure
        if self.agreement:
            reduction = self._calculate_agreement_effectiveness()
            self.incident_pressure *= (1 - reduction * 0.05)

        # Environmental factors
        if self.context.get("weather_bad", False):
            self.incident_pressure *= 1.05
        if self.context.get("media_visibility", 0) >= 2:
            self.incident_pressure *= 0.98  # Slight restraint

        # Recent incidents increase pressure (feedback loop)
        recent = len([h for h in self.history if h['step'] >= self.schedule.steps - 10])
        self.incident_pressure += recent * 0.002

        # Bounds
        self.incident_pressure = max(0.01, min(0.95, self.incident_pressure))

    def _update_escalation_risk(self):
        """Calculate escalation risk based on recent patterns"""
        if len(self.history) < 10:
            self.escalation_risk = 0.3
            return

        # Analyze recent trend
        recent_10 = [h for h in self.history if h['step'] >= self.schedule.steps - 10]
        recent_20 = [h for h in self.history if h['step'] >= self.schedule.steps - 20 and h['step'] < self.schedule.steps - 10]

        count_recent = len(recent_10)
        count_prior = len(recent_20)

        # Escalating if increasing frequency
        if count_recent > count_prior * 1.2:
            self.escalation_risk = min(0.9, self.escalation_risk + 0.05)
        else:
            self.escalation_risk = max(0.1, self.escalation_risk - 0.02)

        # Severity trend
        if recent_10:
            avg_severity = np.mean([h['severity'] for h in recent_10])
            if avg_severity > 0.6:
                self.escalation_risk = min(0.9, self.escalation_risk + 0.03)

    def _calculate_agreement_effectiveness(self) -> float:
        """Calculate how effective the agreement is"""
        if not self.agreement:
            return 0.0

        effectiveness = 0.5
        # Count provisions
        provision_count = len(self.agreement)
        effectiveness += min(0.3, provision_count * 0.05)

        return min(1.0, effectiveness)

    def run(self) -> pd.DataFrame:
        """Run simulation for specified steps"""
        for _ in range(self.steps):
            self.step()

        # Return results as DataFrame
        if not self.history:
            return pd.DataFrame()

        return pd.DataFrame(self.history)


# Backward compatibility with MaritimeModel
class MaritimeModel(ConflictSimulation):
    """Backward compatible maritime model"""

    def __init__(self, steps: int = 200, environment: Optional[Dict[str, Any]] = None,
                 agreement: Optional[Dict[str, Any]] = None, seed: Optional[int] = None):
        super().__init__(
            steps=steps,
            domain="maritime",
            environment=environment,
            agreement=agreement,
            seed=seed
        )

        # Set context from environment
        env = environment or {}
        self.weather = env.get("weather_state", "calm")
        self.media_visibility = env.get("media_visibility", 2)

        # Map to context
        self.context['weather_bad'] = (self.weather == "rough")
        self.context['media_visibility'] = self.media_visibility
