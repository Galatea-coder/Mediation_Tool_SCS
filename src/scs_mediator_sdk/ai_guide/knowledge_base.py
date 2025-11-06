"""
Knowledge Base and RAG (Retrieval-Augmented Generation) for AI Guide
Loads documentation and retrieves relevant context to minimize hallucinations
"""

import os
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DocumentChunk:
    """A chunk of documentation with metadata"""
    content: str
    source: str  # File name
    section: str  # Section header
    page_range: Optional[str] = None  # Line numbers


class KnowledgeBase:
    """
    Loads and retrieves relevant documentation for AI guide
    Implements simple keyword-based retrieval (no embeddings needed)
    """

    def __init__(self, docs_path: str = None):
        """
        Initialize knowledge base

        Args:
            docs_path: Path to documentation directory (defaults to project root)
        """
        if docs_path is None:
            # Default to project root
            self.docs_path = Path(__file__).parent.parent.parent.parent
        else:
            self.docs_path = Path(docs_path)

        self.documents: Dict[str, str] = {}
        self.chunks: List[DocumentChunk] = []
        self._load_documents()
        self._create_chunks()

    def _load_documents(self):
        """Load key documentation files"""
        doc_files = [
            "DETAILED_INSTRUCTOR_MANUAL.md",
            "DETAILED_PARTICIPANT_MANUAL.md",
            "RUNNING_V2.md",
            "INTEGRATION_STATUS.md",
            "LLM_ESCALATION_ENHANCEMENT.md",
            "README_V2.md"
        ]

        for filename in doc_files:
            file_path = self.docs_path / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.documents[filename] = f.read()
                except Exception as e:
                    print(f"Warning: Could not load {filename}: {e}")

    def _create_chunks(self):
        """Create searchable chunks from documents"""
        for filename, content in self.documents.items():
            # Split by sections (markdown headers)
            sections = content.split('\n## ')

            for i, section in enumerate(sections):
                if not section.strip():
                    continue

                # Extract section header
                lines = section.split('\n')
                section_header = lines[0].strip('#').strip() if lines else "Introduction"
                section_content = '\n'.join(lines[1:]) if len(lines) > 1 else section

                # Create chunk
                chunk = DocumentChunk(
                    content=section_content,
                    source=filename,
                    section=section_header
                )
                self.chunks.append(chunk)

    def retrieve(self, query: str, top_k: int = 3) -> List[DocumentChunk]:
        """
        Retrieve most relevant document chunks for a query

        Args:
            query: User's question
            top_k: Number of chunks to return

        Returns:
            List of most relevant document chunks
        """
        # Simple keyword-based scoring
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        scored_chunks = []
        for chunk in self.chunks:
            chunk_lower = (chunk.section + " " + chunk.content).lower()

            # Score based on keyword matches
            score = 0
            for term in query_terms:
                if len(term) > 3:  # Skip short words
                    score += chunk_lower.count(term)

            # Boost for section header matches
            if any(term in chunk.section.lower() for term in query_terms if len(term) > 3):
                score *= 2

            scored_chunks.append((score, chunk))

        # Sort by score and return top k
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for score, chunk in scored_chunks[:top_k] if score > 0]

    def get_scenario_info(self, scenario: str) -> str:
        """Get specific scenario information"""
        scenario_map = {
            "scenario_A_second_thomas.json": "Second Thomas Shoal",
            "scenario_B_scarborough.json": "Scarborough Shoal",
            "scenario_C_kasawari.json": "Kasawari Gas Field",
            "scenario_D_natuna.json": "Natuna Islands"
        }

        scenario_name = scenario_map.get(scenario, scenario)

        # Search for scenario-specific content
        results = self.retrieve(scenario_name, top_k=2)

        if results:
            return f"\n\n**Scenario Context from Documentation:**\n{results[0].content[:500]}..."
        return ""

    def get_academic_references(self) -> str:
        """Get list of academic references used in the system"""
        references = """
**Academic Sources Used in SCS Mediator SDK:**

1. **Putnam, R. D. (1988).** "Diplomacy and domestic politics: the logic of two-level games." *International Organization*, 42(3), 427-460.
   - Two-level game theory for analyzing domestic constraints on international negotiations

2. **Osgood, C. E. (1962).** "An Alternative to War or Surrender." Urbana: University of Illinois Press.
   - GRIT (Graduated Reciprocation in Tension-reduction) for de-escalation

3. **Kahn, H. (1965).** "On Escalation: Metaphors and Scenarios." New York: Praeger.
   - Escalation ladder framework for crisis dynamics

4. **Fisher, R., & Ury, W. (1981).** "Getting to Yes: Negotiating Agreement Without Giving In." New York: Penguin Books.
   - Principled negotiation, BATNA, ZOPA concepts

5. **Stedman, S. J. (1997).** "Spoiler Problems in Peace Processes." *International Security*, 22(2), 5-53.
   - Classification and management of spoilers

6. **McDonald, J. W., & Diamond, L. (1996).** "Multi-Track Diplomacy: A Systems Approach to Peace." West Hartford: Kumarian Press.
   - Multi-track diplomacy framework

7. **Touval, S., & Zartman, I. W. (1985).** "International Mediation in Theory and Practice." Boulder: Westview Press.
   - Third-party mediation and regional architecture

8. **Ross, M. H. (2007).** "Cultural Contestation in Ethnic Conflict." Cambridge University Press.
   - Cultural and historical narratives in conflict

9. **United Nations Convention on the Law of the Sea (UNCLOS).** (1982).
   - Maritime law framework for EEZs, territorial seas, and maritime rights

10. **Permanent Court of Arbitration.** (2016). "The South China Sea Arbitration (Philippines v. China)."
    - Legal precedent for maritime disputes in SCS
"""
        return references


class RAGEnhancedPrompt:
    """Enhances prompts with retrieved documentation"""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base

    def enhance_question(self, question: str, context: Dict) -> tuple[str, str]:
        """
        Enhance question with relevant documentation

        Args:
            question: User's question
            context: Session context (scenario, step, party, etc.)

        Returns:
            Tuple of (enhanced_question, sources_used)
        """
        # Retrieve relevant documentation - REDUCED to minimize emphasis
        relevant_chunks = self.kb.retrieve(question, top_k=1)  # Reduced from 3 to 1

        # Build enhanced prompt with MANDATORY citation requirement at the TOP
        enhanced = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRITICAL INSTRUCTION - YOUR PRIMARY TASK 🚨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your response MUST be grounded in EXTERNAL ACADEMIC LITERATURE, not the internal documentation below.

Internal documentation is provided ONLY as context about this specific simulation system.
You MUST NOT cite it as your primary source.

Instead, you MUST cite 8-12 EXTERNAL published academic sources:
- Full author names and publication years
- Book/article titles for major works
- Journal names for articles
- Specific concepts and frameworks from each work

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User question: {question}

"""

        if relevant_chunks:
            enhanced += "**Background Context (for reference only - DO NOT cite as primary source):**\n\n"
            sources = []

            for i, chunk in enumerate(relevant_chunks, 1):
                enhanced += f"[Context {i}] {chunk.source} - {chunk.section}:\n"
                # REDUCED from 400 to 200 chars to minimize emphasis
                content_preview = chunk.content[:200]
                if len(chunk.content) > 200:
                    content_preview += "..."
                enhanced += f"{content_preview}\n\n"
                sources.append(f"{chunk.source} ({chunk.section})")

            sources_str = ", ".join(sources)
        else:
            sources_str = "None (using general knowledge)"

        # Add scenario context if available
        if "scenario" in context and context["scenario"]:
            scenario_info = self.kb.get_scenario_info(context["scenario"])
            if scenario_info:
                enhanced += scenario_info + "\n\n"

        # Add simulation parameters if available
        if "simulation_parameters" in context and context["simulation_parameters"]:
            enhanced += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 AVAILABLE SIMULATION PARAMETERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The simulation allows participants to adjust these specific parameters:

"""
            for param_name, param_info in context["simulation_parameters"].items():
                enhanced += f"- **{param_name}**: {param_info}\n"

            enhanced += """

CRITICAL: Your response MUST include a section that maps academic recommendations to these SPECIFIC simulation parameters.
For each recommendation, specify EXACTLY which parameters to adjust and to what values.

Example format:
"According to Schelling (1960), graduated reciprocation works by...
→ SIMULATION ACTION: Set standoff=5, escort=3, prenotify=7 to signal cooperative intent."

"""

        enhanced += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  REMINDER: The above documentation is CONTEXT ONLY
    Your answer must draw primarily from EXTERNAL ACADEMIC LITERATURE
    BUT you must map recommendations to SPECIFIC SIMULATION PARAMETERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

        # Add explicit instruction to cite external academic sources
        enhanced += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 REQUIRED EXTERNAL SOURCES TO CITE (8-12 citations mandatory)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your response MUST be:
1. THOROUGH and DETAILED (not generic advice)
2. HIGHLY PRESCRIPTIVE with specific recommendations
3. DEEPLY GROUNDED in EXTERNAL academic theory (cite 8-12+ external sources)
4. ACTIONABLE with concrete steps from the literature

DO NOT apologize for lack of documentation. Instead, provide COMPREHENSIVE guidance drawing from the academic literature below.

You MUST cite EXTENSIVELY from these EXTERNAL academic works:

**Game Theory & Strategic Behavior:**
- Schelling (1960) "The Strategy of Conflict" - focal points, commitment devices, threats vs. promises
- Schelling (1966) "Arms and Influence" - coercive diplomacy, graduated pressure
- Axelrod (1984) "The Evolution of Cooperation" - tit-for-tat, shadow of the future, reciprocity
- Nash (1950) - equilibrium concepts, best response strategies
- Myerson (1991) "Game Theory: Analysis of Conflict" - mechanism design, information asymmetry
- Dixit & Nalebuff (1991) "Thinking Strategically" - strategic moves, credible commitments

**Negotiation Theory & Practice:**
- Fisher & Ury (1981) "Getting to Yes" - BATNA, ZOPA, principled negotiation, separating people from problem
- Raiffa (1982) "The Art and Science of Negotiation" - decision trees, probability assessment, value tradeoffs
- Lax & Sebenius (1986) "The Manager as Negotiator" - creating value vs. claiming value tension
- Mnookin, Peppet & Tulumello (2000) "Beyond Winning" - five tensions in negotiation
- Ury (1991) "Getting Past No" - overcoming barriers, breakthrough strategies
- Thompson (2015) "The Mind and Heart of the Negotiator" - preparation, tactics

**Behavioral Science & Decision-Making:**
- Kahneman & Tversky (1979) "Prospect Theory" - loss aversion, framing effects, reference points
- Kahneman (2011) "Thinking, Fast and Slow" - System 1/System 2, anchoring, availability heuristic
- Bazerman & Neale (1992) "Negotiating Rationally" - cognitive biases in bargaining
- Ross & Stillinger (1991) - reactive devaluation in negotiations
- Tversky & Kahneman (1981) - framing of gains vs. losses
- Ariely (2008) "Predictably Irrational" - irrational decision patterns

**Political Science & International Relations:**
- Putnam (1988) "Diplomacy and domestic politics: the logic of two-level games" - win-sets, ratification constraints
- Fearon (1995) "Rationalist explanations for war" - commitment problems, information asymmetries
- Fearon (1994) "Domestic political audiences and the escalation of international disputes" - audience costs
- Allison (1971) "Essence of Decision" - bureaucratic politics, organizational process models
- Jervis (1978) "Cooperation under the security dilemma" - offense-defense balance, spiral model
- Walt (1987) "The Origins of Alliances" - balance of threat theory
- Waltz (1979) "Theory of International Politics" - structural realism, self-help

**Peace Mediation & Conflict Resolution:**
- Osgood (1962) "An Alternative to War or Surrender" - GRIT (Graduated Reciprocation in Tension-reduction)
- Kahn (1965) "On Escalation: Metaphors and Scenarios" - escalation ladder, rungs of escalation
- Stedman (1997) "Spoiler problems in peace processes" - types of spoilers, strategies for management
- Touval & Zartman (1985) "International Mediation in Theory and Practice" - mediator leverage, ripeness
- Lederach (1997) "Building Peace" - conflict transformation, long-term peacebuilding
- Fisher (2001) - contingency model of third-party intervention
- Mitchell (2000) "Gestures of Conciliation" - timing and effectiveness of conciliatory actions

**Maritime Disputes & Regional Security:**
- Fravel (2008) "Strong Borders, Secure Nation" - China's approach to territorial disputes
- Hayton (2014) "The South China Sea: The Struggle for Power in Asia"
- UNCLOS (1982) - EEZ rights, territorial seas, continental shelf
- Johnston & Ross (1999) "Engaging China" - engagement strategies with rising powers

MANDATORY RESPONSE FORMAT:
1. **Open with strategic framework** - cite 2-3 key EXTERNAL theories (Schelling, Putnam, etc.)
2. **Provide 5-7 specific, actionable recommendations** - each grounded in EXTERNAL academic works
3. **Map EACH recommendation to simulation parameters** - for EVERY recommendation, specify which simulation parameters to adjust and to what values
4. **Explain WHY each recommendation works** - using EXTERNAL behavioral science, game theory, or political science
5. **Anticipate challenges** - cite EXTERNAL literature on common pitfalls
6. **Provide a "Quick Actions" summary** - bullet list of specific parameter settings at the end

Example structure for each recommendation:
📚 Academic Grounding: "Schelling (1960) argues that gradual de-escalation..."
→ Simulation Action: Set standoff=6, escort=4, prenotify=8
💡 Why This Works: "This implements GRIT by signaling cooperative intent..."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ FORBIDDEN RESPONSES (Will be rejected):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ "Based on the DETAILED_INSTRUCTOR_MANUAL.md..." - NO! Cite external academic sources!
❌ "According to the participant manual..." - NO! Cite Schelling, Putnam, Kahneman, etc.!
❌ "Limited specific guidance available" - NO! Draw on academic literature instead!
❌ "Documentation doesn't cover this" - NO! Use your theoretical knowledge!
❌ Generic advice without external citations - NO! Everything must cite published academic works!
❌ Fewer than 8 external citations - NO! You need 8-12 external sources!
❌ Citing only internal documentation - ABSOLUTELY FORBIDDEN!

Your answer must be COMPREHENSIVE, THOROUGH, and DEEPLY ACADEMIC while remaining practical and actionable.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 FINAL CHECKLIST - BEFORE YOU WRITE YOUR RESPONSE 🚨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Confirm your response will include:

✓ AT LEAST 8-10 citations to EXTERNAL PUBLISHED academic sources
✓ ZERO citations to DETAILED_INSTRUCTOR_MANUAL.md, DETAILED_PARTICIPANT_MANUAL.md, or other internal docs
✓ Full author names with years: "Schelling (1960)", "Kahneman & Tversky (1979)"
✓ Book/article titles for major works: "Fisher & Ury's (1981) Getting to Yes..."
✓ Journal names for articles: "...published in International Organization"
✓ Specific concepts from each work you cite (not just name-dropping)
✓ Integration throughout your response (not just a list at the end)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ REQUIRED CITATION EXAMPLES (Follow these exactly):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ "According to Putnam's (1988) two-level game theory published in International Organization..."
✓ "Schelling (1960) in The Strategy of Conflict argues that focal points..."
✓ "Kahneman and Tversky's (1979) prospect theory, published in Econometrica, demonstrates that loss aversion..."
✓ "Fisher and Ury (1981) in Getting to Yes recommend developing your BATNA..."
✓ "Axelrod's (1984) Evolution of Cooperation shows that tit-for-tat strategies..."
✓ "As Fearon (1995) argues in his International Organization article on rationalist explanations for war..."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⛔ ABSOLUTELY FORBIDDEN - DO NOT DO THIS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⛔ "According to the DETAILED_INSTRUCTOR_MANUAL.md, you should..."
⛔ "The participant manual suggests..."
⛔ "Based on the documentation provided..."
⛔ Any citation that references files ending in .md or internal documents

NOW WRITE YOUR RESPONSE USING ONLY EXTERNAL ACADEMIC SOURCES.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        return enhanced, sources_str


def create_knowledge_base() -> KnowledgeBase:
    """Convenience function to create knowledge base"""
    return KnowledgeBase()


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Knowledge Base and RAG")
    print("=" * 60)

    # Create knowledge base
    kb = KnowledgeBase()
    print(f"\nLoaded {len(kb.documents)} documents")
    print(f"Created {len(kb.chunks)} searchable chunks")

    # Test retrieval
    test_queries = [
        "How do I use the escalation assessment?",
        "What is BATNA?",
        "What are confidence-building measures?",
        "How does domestic politics affect negotiations?"
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")

        results = kb.retrieve(query, top_k=2)

        if results:
            for i, chunk in enumerate(results, 1):
                print(f"\n[{i}] {chunk.source} - {chunk.section}")
                print(f"Preview: {chunk.content[:200]}...")
        else:
            print("No relevant documentation found")

    # Test RAG enhancement
    print(f"\n\n{'='*60}")
    print("Testing RAG Enhancement")
    print(f"{'='*60}")

    rag = RAGEnhancedPrompt(kb)
    enhanced, sources = rag.enhance_question(
        "How do I interpret escalation risk levels?",
        {"scenario": "scenario_A_second_thomas.json"}
    )

    print(f"\nSources used: {sources}")
    print(f"\nEnhanced prompt (first 500 chars):\n{enhanced[:500]}...")

    # Show academic references
    print(f"\n\n{'='*60}")
    print("Academic References")
    print(f"{'='*60}")
    print(kb.get_academic_references())
