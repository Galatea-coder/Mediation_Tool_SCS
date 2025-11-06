"""
AI Guide Chatbot for SCS Mediator SDK v2
Persona-based guidance using Claude API with RAG from training materials
"""

import os
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv
from .knowledge_base import KnowledgeBase, RAGEnhancedPrompt
from .persistence import ChatPersistence

# Load environment variables
load_dotenv()


class GuidePersona(Enum):
    """Available AI guide personas"""
    INSTRUCTOR = "dr_marina_chen"  # For instructors/facilitators
    PARTICIPANT = "ambassador_zhou"  # For negotiating parties


@dataclass
class ChatMessage:
    """A single message in the chat history"""
    role: str  # "user" or "assistant"
    content: str


class AIGuide:
    """
    AI-powered guide providing context-aware assistance

    Features:
    - Persona-based responses (instructor vs participant)
    - Context-aware (current scenario, step, role)
    - Knowledge from training materials and academic literature
    - Conversation memory within session
    """

    def __init__(
        self,
        persona: GuidePersona,
        api_key: Optional[str] = None,
        session_id: str = "default",
        enable_persistence: bool = True
    ):
        """
        Initialize AI guide with specific persona

        Args:
            persona: Which guide persona to use (instructor or participant)
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            session_id: Unique session identifier for persistence (e.g., "instructor" or "participant_PH_GOV")
            enable_persistence: Whether to save/load conversation history (default: True)
        """
        self.persona = persona
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.session_id = session_id
        self.enable_persistence = enable_persistence
        self.conversation_history: List[ChatMessage] = []
        self.context = {}  # Session context (scenario, step, party, etc.)

        # Initialize RAG system to minimize hallucinations
        self.knowledge_base = KnowledgeBase()
        self.rag = RAGEnhancedPrompt(self.knowledge_base)

        # Initialize persistence layer
        if self.enable_persistence:
            self.persistence = ChatPersistence()
            # Load existing conversation history if available
            loaded_history, loaded_context = self.persistence.load_conversation(
                session_id=self.session_id,
                persona=self.persona.value
            )
            if loaded_history:
                self.conversation_history = loaded_history
                self.context.update(loaded_context)
        else:
            self.persistence = None

        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

    def set_context(self, **kwargs):
        """
        Update session context for more relevant guidance

        Args:
            scenario: Current scenario (A/B/C/D)
            step: Current workflow step (1-6)
            party: User's party role (for participants)
            current_level: Current escalation level
            **kwargs: Any other relevant context
        """
        self.context.update(kwargs)

    def ask(self, question: str) -> Dict[str, str]:
        """
        Ask the AI guide a question and get a response

        Args:
            question: User's question

        Returns:
            Dictionary with 'response' (AI answer) and 'sources' (documentation used)
        """
        try:
            import anthropic
        except ImportError:
            return {
                "response": "Error: anthropic package not installed. Run: pip install anthropic",
                "sources": "None"
            }

        # Add user question to history (original question for conversation flow)
        self.conversation_history.append(ChatMessage(role="user", content=question))

        # Build system prompt based on persona
        system_prompt = self._build_system_prompt()

        # Add session context to question
        context_enhanced = self._enhance_question_with_context(question)

        # Use RAG to retrieve relevant documentation and enhance question
        # This minimizes hallucinations by grounding responses in actual docs
        rag_enhanced, sources = self.rag.enhance_question(context_enhanced, self.context)

        # Call Claude API with RAG-enhanced question
        client = anthropic.Anthropic(api_key=self.api_key)

        # Build message history for Claude
        # Use original questions in history, but RAG-enhanced version for current question
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in self.conversation_history[:-1]  # Previous conversation
        ] + [
            {"role": "user", "content": rag_enhanced}  # Current question with RAG
        ]

        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2048,
            system=system_prompt,
            messages=messages
        )

        assistant_response = response.content[0].text

        # Add response to history (for conversation continuity)
        self.conversation_history.append(ChatMessage(role="assistant", content=assistant_response))

        # Auto-save conversation to persistent storage
        if self.enable_persistence:
            self.save_conversation()

        return {
            "response": assistant_response,
            "sources": sources
        }

    def save_conversation(self) -> bool:
        """
        Manually save conversation to persistent storage

        Returns:
            True if successful, False otherwise
        """
        if not self.enable_persistence:
            return False

        return self.persistence.save_conversation(
            session_id=self.session_id,
            persona=self.persona.value,
            conversation_history=self.conversation_history,
            context=self.context
        )

    def clear_history(self):
        """Clear conversation history and persistent storage"""
        self.conversation_history = []

        # Also clear from persistent storage
        if self.enable_persistence:
            self.persistence.clear_conversation(
                session_id=self.session_id,
                persona=self.persona.value
            )

    def _build_system_prompt(self) -> str:
        """Build persona-specific system prompt"""

        if self.persona == GuidePersona.INSTRUCTOR:
            return """You are the Mediator Assistant, an AI-powered guide helping instructors and facilitators use the SCS Mediator SDK for peace mediation training and maritime conflict simulation.

Your role:
- Help instructors/facilitators use the SCS Mediator SDK effectively
- Explain peace mediation tools (escalation assessment, CBMs, domestic politics, spoilers, multi-track)
- Provide interpretation guidance for simulation results
- Offer pedagogical advice for training scenarios
- Troubleshoot technical issues with the simulation

CRITICAL CITATION REQUIREMENT:
You MUST cite specific academic sources with full details when answering questions. Every theoretical concept or framework you mention MUST include:
1. Author names and year
2. Paper/book title (if highly relevant)
3. Journal or publisher (for key citations)

Required citation format examples:
- "According to Putnam's (1988) two-level game theory, published in International Organization..."
- "Kahneman and Tversky's (1979) prospect theory demonstrates..."
- "As Schelling (1960) argues in The Strategy of Conflict..."
- "Axelrod's (1984) research on cooperation in The Evolution of Cooperation shows..."

MANDATORY ACADEMIC SOURCES TO CITE:

**Political Science:**
- Putnam, R. D. (1988). "Diplomacy and domestic politics: the logic of two-level games." International Organization 42(3).
- Allison, G. T. (1971). Essence of Decision: Explaining the Cuban Missile Crisis. [Bureaucratic politics model]
- Fearon, J. D. (1995). "Rationalist explanations for war." International Organization 49(3).

**Game Theory:**
- Nash, J. (1950). "Equilibrium points in n-person games." Proceedings of the National Academy of Sciences.
- Schelling, T. C. (1960). The Strategy of Conflict. Harvard University Press. [Focal points, commitment]
- Axelrod, R. (1984). The Evolution of Cooperation. [Tit-for-tat, iterated prisoner's dilemma]

**Behavioral Science & Negotiation:**
- Kahneman, D., & Tversky, A. (1979). "Prospect theory: An analysis of decision under risk." Econometrica 47(2).
- Fisher, R., & Ury, W. (1981). Getting to Yes: Negotiating Agreement Without Giving In. [BATNA, principled negotiation]
- Raiffa, H. (1982). The Art and Science of Negotiation. Harvard University Press.

**Conflict Resolution:**
- Osgood, C. E. (1962). An Alternative to War or Surrender. [GRIT - Graduated Reciprocation in Tension-reduction]
- Kahn, H. (1965). On Escalation: Metaphors and Scenarios. [Escalation ladder]
- Stedman, S. J. (1997). "Spoiler problems in peace processes." International Security 22(2).

**Geopolitics & Regional Security:**
- Mearsheimer, J. J. (2001). The Tragedy of Great Power Politics. [Offensive realism]
- Walt, S. M. (1987). The Origins of Alliances. [Balance of threat theory]
- Jervis, R. (1978). "Cooperation under the security dilemma." World Politics 30(2).

**Maritime Disputes:**
- Fravel, M. T. (2008). Strong Borders, Secure Nation: Cooperation and Conflict in China's Territorial Disputes.
- Hayton, B. (2014). The South China Sea: The Struggle for Power in Asia.
- UNCLOS (1982). United Nations Convention on the Law of the Sea.

Your responses MUST:
1. Cite AT LEAST 2-3 specific academic sources per answer
2. Use author-year format with full details
3. Explain how the theory/research applies to the specific question
4. Connect academic frameworks to practical simulation use

You have access to these training materials:
- DETAILED_INSTRUCTOR_MANUAL.md
- DETAILED_PARTICIPANT_MANUAL.md
- RUNNING_V2.md
- Peace mediation module documentation"""

        else:  # PARTICIPANT
            return """You are the Mediator Assistant, an AI-powered guide helping participants navigate maritime conflict negotiation scenarios in the SCS Mediator SDK.

Your role:
- Guide participants in negotiation strategy and tactics
- Explain political science and negotiation concepts
- Provide hints about effective approaches (without revealing optimal solutions)
- Help participants understand their position and constraints
- Explain geopolitical and economic considerations

CRITICAL CITATION REQUIREMENT:
You MUST cite specific academic sources with full details. Every concept or recommendation MUST include author names, year, and key publication details.

Required citation format examples:
- "Fisher and Ury's (1981) Getting to Yes introduces the concept of BATNA..."
- "According to Putnam's (1988) two-level game theory..."
- "Schelling (1960) in The Strategy of Conflict explains commitment devices..."
- "As Kahneman and Tversky (1979) demonstrate in their prospect theory work..."

MANDATORY ACADEMIC SOURCES TO CITE:

**Negotiation Theory:**
- Fisher, R., & Ury, W. (1981). Getting to Yes: Negotiating Agreement Without Giving In. [BATNA, ZOPA, principled negotiation]
- Raiffa, H. (1982). The Art and Science of Negotiation. Harvard University Press. [Integrative vs distributive bargaining]
- Lax, D. A., & Sebenius, J. K. (1986). The Manager as Negotiator. Free Press. [Creating and claiming value]

**Political Science:**
- Putnam, R. D. (1988). "Diplomacy and domestic politics: the logic of two-level games." International Organization 42(3). [Win-sets, ratification]
- Fearon, J. D. (1994). "Domestic political audiences and the escalation of international disputes." American Political Science Review 88(3). [Audience costs]
- Schelling, T. C. (1960). The Strategy of Conflict. Harvard University Press. [Commitment, focal points]

**Game Theory:**
- Nash, J. (1950). "Equilibrium points in n-person games." [Nash equilibrium]
- Axelrod, R. (1984). The Evolution of Cooperation. [Tit-for-tat, repeated games, reciprocity]
- Schelling, T. C. (1966). Arms and Influence. [Coercive diplomacy, signaling]

**Behavioral Science:**
- Kahneman, D., & Tversky, A. (1979). "Prospect theory: An analysis of decision under risk." Econometrica 47(2). [Loss aversion, framing]
- Ross, L., & Ward, A. (1995). "Psychological barriers to dispute resolution." Advances in Experimental Social Psychology 27. [Reactive devaluation]
- Mnookin, R. H. (1993). "Why negotiations fail: An exploration of barriers to the resolution of conflict." Ohio State Journal on Dispute Resolution 8. [Cognitive biases]

**Cultural Factors:**
- Gelfand, M. J., & Brett, J. M. (2004). The Handbook of Negotiation and Culture. Stanford University Press. [Cross-cultural negotiation]
- Leung, K. (1988). "Some determinants of conflict avoidance." Journal of Cross-Cultural Psychology 19(1). [Face-saving in Asian cultures]

**Maritime Disputes:**
- Fravel, M. T. (2008). Strong Borders, Secure Nation: Cooperation and Conflict in China's Territorial Disputes.
- Hayton, B. (2014). The South China Sea: The Struggle for Power in Asia.
- UNCLOS (1982). United Nations Convention on the Law of the Sea. [EEZ, territorial seas, maritime rights]

Your responses MUST:
1. Cite AT LEAST 2-3 specific academic sources per answer
2. Use author-year format with publication details
3. Explain how the theory applies to the participant's specific situation
4. Use Socratic questions to guide thinking
5. Maintain confidentiality - don't reveal other parties' strategies

Important boundaries:
- DON'T reveal optimal solutions or "correct" answers
- DON'T share other parties' positions or strategies
- DON'T make decisions for participants
- DO help them think through implications using academic frameworks
- DO encourage creative problem-solving informed by theory

You have access to:
- DETAILED_PARTICIPANT_MANUAL.md
- Scenario-specific context and parameters
- Historical SCS incidents and negotiations"""

    def set_simulation_parameters(self, parameters: Dict[str, str]):
        """
        Update context with available simulation parameters

        Args:
            parameters: Dictionary mapping parameter names to descriptions
        """
        self.context["simulation_parameters"] = parameters

    def _enhance_question_with_context(self, question: str) -> str:
        """Add relevant context to the question"""

        if not self.context:
            return question

        context_str = "Current context:\n"

        if "scenario" in self.context:
            scenario_map = {
                "scenario_A_second_thomas.json": "Scenario A: Second Thomas Shoal (Resupply)",
                "scenario_B_scarborough.json": "Scenario B: Scarborough Shoal (Fishing)",
                "scenario_C_kasawari.json": "Scenario C: Kasawari Gas Field (Energy)",
                "scenario_D_natuna.json": "Scenario D: Natuna Islands (EEZ)"
            }
            context_str += f"- Scenario: {scenario_map.get(self.context['scenario'], self.context['scenario'])}\n"

        if "step" in self.context:
            step_map = {
                1: "Step 1: Scenario Selection",
                2: "Step 2: Parameter Configuration",
                3: "Step 3: Evaluate Agreement",
                4: "Step 4: Run Simulation",
                5: "Step 5: Results Analysis",
                6: "Step 6: Peace Mediation Tools"
            }
            context_str += f"- Current Step: {step_map.get(self.context['step'], self.context['step'])}\n"

        if "party" in self.context:
            party_map = {
                "PH_GOV": "Philippines Government",
                "PRC_MARITIME": "PRC Maritime Forces",
                "VN_CG": "Vietnam Coast Guard",
                "MY_NAVY": "Malaysia Navy"
            }
            context_str += f"- Your Role: {party_map.get(self.context['party'], self.context['party'])}\n"

        if "current_level" in self.context:
            context_str += f"- Escalation Level: {self.context['current_level']}\n"

        context_str += f"\nUser question: {question}"

        return context_str

    def get_quick_tips(self) -> List[str]:
        """Get quick tips based on current context"""

        tips = []

        if self.persona == GuidePersona.INSTRUCTOR:
            tips = [
                "Use Step 6 Peace Mediation Tools to assess escalation risk before proposing actions",
                "Check domestic politics analysis to ensure agreements can be ratified",
                "Recommend CBMs to participants to build trust and reduce tensions",
                "Use spoiler analysis to identify threats to agreement implementation",
                "Coordinate Track 2 activities to prepare ground for official negotiations"
            ]

            if self.context.get("step") == 2:
                tips.append("Scenario-aware parameters are pre-configured - only adjust if needed for learning objectives")
            elif self.context.get("step") == 6:
                tips.append("Try the LLM-powered escalation assessment to see AI analysis of proposed actions")

        else:  # PARTICIPANT
            tips = [
                "Understand your BATNA (Best Alternative to Negotiated Agreement) before negotiating",
                "Look for integrative solutions that create value for both sides",
                "Consider face-saving formulas that allow both sides to claim success",
                "Check domestic constraints - can your government ratify this agreement?",
                "Include confidence-building measures to reduce security concerns"
            ]

            party = self.context.get("party", "")
            if "PH" in party:
                tips.append("Philippines: Balance sovereignty claims with practical operational access")
            elif "PRC" in party:
                tips.append("China: Balance core interests with regional stability and economic ties")
            elif "VN" in party:
                tips.append("Vietnam: Leverage ASEAN solidarity while managing China relationship")
            elif "MY" in party:
                tips.append("Malaysia: Focus on EEZ rights and resource development pragmatism")

        return tips


# Convenience functions
def create_instructor_guide(
    api_key: Optional[str] = None,
    session_id: str = "instructor",
    enable_persistence: bool = True
) -> AIGuide:
    """
    Create AI guide for instructors

    Args:
        api_key: Anthropic API key (optional)
        session_id: Unique session identifier (default: "instructor")
        enable_persistence: Whether to save/load conversation history (default: True)
    """
    return AIGuide(GuidePersona.INSTRUCTOR, api_key, session_id, enable_persistence)


def create_participant_guide(
    api_key: Optional[str] = None,
    session_id: str = "participant",
    enable_persistence: bool = True
) -> AIGuide:
    """
    Create AI guide for participants

    Args:
        api_key: Anthropic API key (optional)
        session_id: Unique session identifier (default: "participant")
        enable_persistence: Whether to save/load conversation history (default: True)
    """
    return AIGuide(GuidePersona.PARTICIPANT, api_key, session_id, enable_persistence)


# Example usage
if __name__ == "__main__":
    import sys

    # Test instructor guide
    print("=" * 60)
    print("Testing Instructor Guide (Dr. Marina Chen)")
    print("=" * 60)

    try:
        guide = create_instructor_guide()
        guide.set_context(scenario="scenario_A_second_thomas.json", step=6)

        print("\nQuick Tips:")
        for tip in guide.get_quick_tips():
            print(f"  • {tip}")

        print("\nAsking: 'How do I interpret the escalation assessment results?'")
        result = guide.ask("How do I interpret the escalation assessment results?")
        response = result["response"]
        sources = result["sources"]
        print(f"\nSources: {sources}")
        print(f"\nDr. Chen: {response[:500]}..." if len(response) > 500 else f"\nDr. Chen: {response}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Testing Participant Guide (Ambassador Zhou)")
    print("=" * 60)

    try:
        guide = create_participant_guide()
        guide.set_context(
            scenario="scenario_B_scarborough.json",
            party="PH_GOV",
            current_level=5
        )

        print("\nQuick Tips:")
        for tip in guide.get_quick_tips():
            print(f"  • {tip}")

        print("\nAsking: 'What strategy should I use for fishing rights negotiation?'")
        result = guide.ask("What strategy should I use for fishing rights negotiation at Scarborough Shoal?")
        response = result["response"]
        sources = result["sources"]
        print(f"\nSources: {sources}")
        print(f"\nAmbassador Zhou: {response[:500]}..." if len(response) > 500 else f"\nAmbassador Zhou: {response}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
