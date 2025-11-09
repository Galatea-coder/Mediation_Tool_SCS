# SCS Mediator SDK - Engineering Documentation

**Version**: 2.0
**Last Updated**: 2025-01-09
**Architecture**: Multi-user negotiation platform with AI guidance
**Technology Stack**: Python 3.9+, Streamlit, LangChain, Mesa (ABM)

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Data Models](#data-models)
3. [Module Structure](#module-structure)
4. [Phase Implementation Details](#phase-implementation-details)
5. [AI Guide System](#ai-guide-system)
6. [Simulation Engine](#simulation-engine)
7. [API Specifications](#api-specifications)
8. [State Management](#state-management)
9. [Database Design](#database-design)
10. [Security Considerations](#security-considerations)
11. [Performance Optimization](#performance-optimization)
12. [Testing Strategy](#testing-strategy)
13. [Deployment Architecture](#deployment-architecture)
14. [Extension Points](#extension-points)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│  ┌─────────────────┐          ┌─────────────────┐          │
│  │  Facilitator UI │          │   Player UI     │          │
│  │  (6 tabs)       │          │   (6 tabs)      │          │
│  └────────┬────────┘          └────────┬────────┘          │
└───────────┼──────────────────────────────┼──────────────────┘
            │                               │
            ▼                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  Session Manager (Singleton)                 │
│  • In-memory session storage                                 │
│  • Player registration & authentication                      │
│  • Proposal & response management                           │
│  • Strategic context tracking                               │
└─────────────────────────────────────────────────────────────┘
            │                               │
            ▼                               ▼
┌──────────────────┐          ┌──────────────────────────────┐
│  AI Guide System │          │  Simulation Engine (Mesa)    │
│  • RAG retrieval │          │  • Agent-based modeling      │
│  • Context-aware │          │  • Escalation dynamics       │
│  • LangChain     │          │  • Incident generation       │
└──────────────────┘          └──────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────────────┐
│              External Dependencies                            │
│  • OpenAI API (GPT-4)                                        │
│  • FAISS Vector Store (documentation retrieval)              │
│  • Strategic Levers Library                                  │
│  • Peace Mediation Tools                                     │
└──────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

**1. Session Creation Flow:**
```
Facilitator → UI → SessionManager.create_session()
                 → Generate unique session_code
                 → Initialize Session object
                 → Store in sessions dict
                 → Return (session_id, session_code)
```

**2. Player Join Flow:**
```
Player → Enter session_code → SessionManager.join_session()
                            → Validate session exists
                            → Check role availability
                            → Create Player object
                            → Initialize StrategicContext
                            → Return player_id
```

**3. Proposal Submission Flow:**
```
Facilitator → Submit proposal → SessionManager.submit_proposal()
                              → Create Proposal object
                              → Notify all players (UI refresh)
                              → Players respond
                              → Update proposal status
```

**4. AI Guide Query Flow:**
```
User → Ask question → ChatbotInterface.ask_question()
                   → Retrieve context (RAG)
                   → Inject simulation parameters
                   → Call LLM with enhanced prompt
                   → Return structured response
```

---

## Data Models

### Core Session Models

#### 1. Session Dataclass
**Location**: `src/scs_mediator_sdk/multiplayer/session_manager.py:61-76`

```python
@dataclass
class Session:
    """Represents a negotiation session"""
    session_id: str                          # Unique identifier
    session_code: str                        # User-friendly code (e.g., REEF-2024)
    facilitator_id: str                      # ID of session creator
    scenario_id: str                         # Scenario identifier
    status: str = 'setup'                    # 'setup' | 'negotiating' | 'simulating' | 'completed'
    current_round: int = 0                   # Round counter
    players: Dict[str, Player]               # player_id -> Player object
    proposals: List[Proposal]                # All proposals in chronological order
    responses: Dict[str, List[Response]]     # proposal_id -> List[Response]
    simulation_results: Optional[Dict]       # Latest simulation output
    strategic_contexts: Dict[str, Any]       # player_id -> StrategicContext (Phase 2)
    created_at: datetime
    updated_at: datetime
```

**Design Decisions:**
- **In-memory storage**: MVP uses in-memory dict for simplicity. Production should use PostgreSQL/Redis.
- **status field**: State machine pattern for session lifecycle management.
- **strategic_contexts**: Added in Phase 2 for soft power tracking.

#### 2. Player Dataclass
**Location**: `src/scs_mediator_sdk/multiplayer/session_manager.py:28-36`

```python
@dataclass
class Player:
    """Represents a player in the session"""
    player_id: str              # Unique identifier
    role: str                   # 'PH_GOV' | 'PRC_MARITIME' | 'VN_CG' | 'MY_CG'
    user_name: str              # Display name
    connected: bool = True      # Connection status
    ready: bool = False         # Ready to begin negotiation
    last_active: datetime       # Heartbeat for timeout detection
```

**Design Decisions:**
- **role enforcement**: One player per role (checked in `join_session()`).
- **ready flag**: Synchronization mechanism - negotiation starts when all ready.
- **last_active**: Future work for connection timeout handling.

#### 3. Proposal Dataclass
**Location**: `src/scs_mediator_sdk/multiplayer/session_manager.py:39-47`

```python
@dataclass
class Proposal:
    """Represents an agreement proposal"""
    proposal_id: str                     # Unique identifier
    round_number: int                    # Round counter
    proposer_id: str                     # 'facilitator' or player_id
    proposal_data: Dict[str, Any]        # Agreement terms (flexible schema)
    status: str = 'pending'              # 'pending' | 'accepted' | 'rejected' | 'mixed'
    created_at: datetime
```

**Proposal Data Schema:**
```python
proposal_data = {
    # Resupply scenario example
    'standoff_nm': 5.0,                  # Nautical miles
    'num_escorts': 2,                    # Integer
    'escort_roe': 'defensive_only',      # String option
    'inspection_protocol': 'observer',   # String option
    'comms_channel': 'encrypted_vhf',    # String option
    'update_frequency_hrs': 6,           # Hours

    # Fishing scenario example
    'daily_quota_tons': 150,
    'vessel_limit': 10,
    'monitoring': 'satellite',
    # ... scenario-specific fields
}
```

**Design Decisions:**
- **Flexible proposal_data**: Different scenarios have different parameters (see ISSUE_METADATA).
- **status calculation**: Updated when all players respond (`_update_proposal_status()`).

#### 4. Response Dataclass
**Location**: `src/scs_mediator_sdk/multiplayer/session_manager.py:50-58`

```python
@dataclass
class Response:
    """Represents a player's response to a proposal"""
    response_id: str                     # Unique identifier
    proposal_id: str                     # Foreign key to proposal
    player_id: str                       # Foreign key to player
    response_type: str                   # 'accept' | 'reject' | 'conditional'
    explanation: str = ""                # Player's reasoning
    created_at: datetime
```

**Response Type Logic:**
```python
# In _update_proposal_status():
if accept_count == len(responses):
    proposal.status = 'accepted'         # All accepted
    session.status = 'simulating'        # Ready to simulate
elif accept_count == 0:
    proposal.status = 'rejected'         # All rejected
else:
    proposal.status = 'mixed'            # Mixed responses
```

#### 5. StrategicContext Dataclass
**Location**: `src/scs_mediator_sdk/strategic_levers/context.py`

```python
@dataclass
class StrategicContext:
    """4-dimensional soft power tracking (Phase 2)"""
    player_id: str
    role: str

    # Nye (2004): Soft power dimensions
    diplomatic_capital: float = 50.0     # 0-100 scale
    international_legitimacy: float = 50.0
    domestic_support: float = 50.0
    credibility: float = 50.0

    # Derived metrics
    escalation_risk_modifier: float = 0.0   # Calculated from dimensions

    # Action history
    actions_taken: List[str] = field(default_factory=list)
```

**Escalation Risk Calculation:**
```python
def calculate_escalation_modifier(context: StrategicContext) -> float:
    """
    Higher legitimacy & support reduce escalation risk.
    Lower values increase risk.
    """
    modifier = 0.0

    # Legitimacy effects (Hurd 2007)
    if context.international_legitimacy > 70:
        modifier -= 0.15   # -15% escalation risk
    elif context.international_legitimacy < 30:
        modifier += 0.20   # +20% escalation risk

    # Domestic support effects (Putnam 1988)
    if context.domestic_support < 35:
        modifier += 0.30   # Fragile domestic support increases risk

    # Credibility effects (Fearon 1994)
    if context.credibility < 40:
        modifier += 0.10   # Low credibility increases uncertainty

    return modifier
```

---

## Module Structure

### Directory Tree

```
src/scs_mediator_sdk/
├── ai_guide/                      # Phase 6: AI Guide System
│   ├── __init__.py
│   ├── chatbot.py                 # Main chatbot interface
│   ├── rag_system.py              # Retrieval-augmented generation
│   └── prompts/                   # System prompts
│       ├── instructor_prompt.py
│       └── participant_prompt.py
│
├── multiplayer/                   # Phase 1: Core multiplayer
│   ├── __init__.py
│   └── session_manager.py         # Session management logic
│
├── strategic_levers/              # Phase 3: Strategic actions
│   ├── __init__.py
│   ├── actions.py                 # Strategic action library
│   ├── context.py                 # StrategicContext dataclass
│   └── effects.py                 # Action effect calculations
│
├── peace_mediation/               # Phase 5: Peace tools
│   ├── __init__.py
│   ├── cbm_library.py             # Confidence-building measures
│   ├── win_set_analyzer.py        # Domestic constraints
│   ├── spoiler_manager.py         # Spoiler analysis
│   └── multi_track_mediator.py    # Multi-track diplomacy
│
├── guides/                        # Player/facilitator guides
│   ├── __init__.py
│   └── negotiation_guides.py      # Role-specific guidance
│
├── simulation/                    # Agent-based modeling
│   ├── __init__.py
│   ├── scs_model.py               # Mesa model definition
│   ├── agents.py                  # Agent behaviors
│   └── escalation_dynamics.py     # Escalation calculations
│
├── dynamics/                      # Conflict dynamics
│   ├── __init__.py
│   ├── escalation_ladder.py       # Kahn escalation ladder
│   └── incident_generator.py      # Stochastic incident generation
│
└── ui/                            # User interfaces
    ├── multiplayer_app.py         # Main multiplayer UI (Phases 1-6)
    ├── enhanced_multi_view.py     # Single-player UI
    └── streamlit_app.py           # Original UI (legacy)
```

### Module Dependencies

```
multiplayer_app.py (Entry Point)
  ├─→ session_manager.py (Core state)
  ├─→ chatbot.py (AI Guide)
  ├─→ actions.py (Strategic levers)
  ├─→ cbm_library.py (Peace tools)
  ├─→ scs_model.py (Simulation)
  └─→ negotiation_guides.py (Guidance)

chatbot.py
  ├─→ rag_system.py (Document retrieval)
  ├─→ LangChain (LLM interface)
  └─→ FAISS (Vector store)

scs_model.py
  ├─→ Mesa (ABM framework)
  ├─→ agents.py (Agent definitions)
  └─→ escalation_dynamics.py (Incident logic)
```

---

## Phase Implementation Details

### Phase 1: Core Multiplayer Foundation

**Goal**: Multi-user sessions with proposals and responses.

**Key Components:**
1. **SessionManager** (`session_manager.py`):
   - Singleton pattern for global state
   - Session lifecycle management
   - Player registration & authentication

2. **UI Components** (`multiplayer_app.py:100-800`):
   - Role selection (Facilitator vs Player)
   - Session creation with unique codes
   - Player join flow
   - Proposal builder (dynamic based on scenario)
   - Response submission

**Technical Implementation:**

```python
# Singleton pattern for session manager
_session_manager = None

def get_session_manager() -> SessionManager:
    """Get the global session manager instance"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager

# Usage in UI
sm = get_session_manager()
session_id, session_code = sm.create_session(facilitator_id, scenario_id)
```

**Session Code Generation:**
```python
def generate_session_code() -> str:
    """Generate memorable session codes like REEF-2024"""
    words = ['REEF', 'WAVE', 'TIDE', 'SAIL', 'CALM',
             'BLUE', 'DEEP', 'SHIP', 'PORT', 'COAST']
    word = random.choice(words)
    number = random.randint(1000, 9999)
    return f"{word}-{number}"
```

**State Synchronization:**
- Streamlit's `st.session_state` for per-user state
- SessionManager for shared state
- UI refresh via `st.rerun()` after state changes

**Lines of Code**: ~800 lines (multiplayer_app.py base implementation)

---

### Phase 2: Strategic Context System

**Goal**: Track 4-dimensional soft power metrics per player.

**Academic Foundation:**
- **Nye (2004)**: Soft power theory → 4 dimensions
- **Putnam (1988)**: Two-level games → Domestic support
- **Fearon (1994)**: Audience costs → Credibility
- **Hurd (2007)**: International legitimacy
- **Schelling (1960)**: Strategic positioning

**Key Components:**

1. **StrategicContext Dataclass** (`context.py`):
```python
@dataclass
class StrategicContext:
    diplomatic_capital: float = 50.0
    international_legitimacy: float = 50.0
    domestic_support: float = 50.0
    credibility: float = 50.0
    escalation_risk_modifier: float = 0.0
```

2. **Facilitator Dashboard** (`multiplayer_app.py:1500-1650`):
   - Display all players' strategic positions
   - Color-coded status indicators
   - Comparison table
   - Escalation risk modifiers

3. **Player Display** (`multiplayer_app.py:2100-2200`):
   - View own strategic position
   - Understand escalation modifier
   - Plan strategic actions accordingly

**Color Coding Logic:**
```python
def get_status_color(value: float) -> str:
    """Color code strategic metrics"""
    if value >= 70:
        return "🟢 Strong"   # Green
    elif value >= 50:
        return "🟡 Moderate" # Yellow
    elif value >= 30:
        return "🟠 Weak"     # Orange
    else:
        return "🔴 Critical" # Red
```

**Integration with Simulation:**
- Strategic context affects escalation calculations
- High legitimacy reduces incident probability
- Low domestic support increases escalation risk

**Lines of Code**: ~300 lines (dashboard + player view + documentation)

---

### Phase 3: Strategic Actions System

**Goal**: Enable players to execute diplomatic moves that affect strategic context.

**Academic Foundation:**
- **Keohane (1984)**: Multilateral institutions
- **Fravel (2008)**: Joint development strategies
- **Diamond & McDonald (1996)**: Multi-track diplomacy
- **Fearon (1994)**: Audience costs & commitment
- **Osgood (1962)**: GRIT & transparency
- **Tollison & Willett (1979)**: Issue linkage

**Strategic Actions Library:**

```python
STRATEGIC_ACTIONS_LIBRARY = [
    StrategicAction(
        name="Host Regional Summit",
        description="Convene multilateral meeting",
        prerequisites={"diplomatic_capital": 30},
        cost={"diplomatic_capital": -5},
        parameter_effects={
            "incident_probability": -0.10,
            "escalation_rate": -0.08
        },
        strategic_effects={
            "international_legitimacy": +10,
            "credibility": +5
        },
        risk_level="low",
        academic_basis="Keohane (1984): Multilateral institutionalism"
    ),
    # ... 5 more actions
]
```

**Action Execution Flow:**

```python
def execute_strategic_action(player_id: str, action: StrategicAction):
    """
    1. Check prerequisites (e.g., diplomatic_capital >= 30)
    2. Deduct costs from strategic context
    3. Apply parameter effects (reduce escalation)
    4. Apply strategic effects (boost legitimacy)
    5. Record in action history
    6. Trigger UI refresh
    """
    context = session.strategic_contexts[player_id]

    # Check prerequisites
    if not check_prerequisites(context, action.prerequisites):
        return False

    # Apply costs
    for metric, change in action.cost.items():
        setattr(context, metric, getattr(context, metric) + change)

    # Apply effects
    for metric, change in action.strategic_effects.items():
        setattr(context, metric, getattr(context, metric) + change)

    # Record action
    context.actions_taken.append(action.name)

    return True
```

**UI Implementation** (`multiplayer_app.py:2200-2350`):
- List available actions
- Filter by prerequisites (grayed out if not met)
- Two-column effect display
- Execute buttons with confirmation
- Success feedback with `st.balloons()`

**Lines of Code**: ~300 lines (UI + documentation)

---

### Phase 4: Enhanced Player View

**Goal**: Organize player interface into 6 clear tabs.

**Tab Structure:**

```python
tabs = st.tabs([
    "🎯 Role & Objectives",     # Tab 1: Know your role
    "📋 Current Proposal",       # Tab 2: View proposal
    "💬 Submit Response",        # Tab 3: Respond
    "📊 Your Strategic Position", # Tab 4: Metrics
    "⚡ Strategic Actions",      # Tab 5: Diplomatic moves
    "📝 Strategy Notes"          # Tab 6: Note-taking
])
```

**Tab 6: Strategy Notes Implementation:**
```python
with tabs[5]:
    st.subheader("📝 Strategy Notes")
    st.write("Take notes during negotiation")

    # Initialize notes in session state
    if 'strategy_notes' not in st.session_state:
        st.session_state.strategy_notes = {}

    notes_key = f"notes_{player_id}"
    current_notes = st.session_state.strategy_notes.get(notes_key, "")

    notes = st.text_area(
        "Your private notes:",
        value=current_notes,
        height=400,
        placeholder="""Example notes:

My Red Lines:
- Standoff distance must be ≥300m
- Maximum 2 escorts

My BATNA:
- Bilateral negotiation with Vietnam
- International arbitration at UNCLOS

Concessions I Can Make:
- Update frequency (6h → 12h acceptable)
- Inspection protocol (observer vs remote)
        """
    )

    if st.button("💾 Save Notes"):
        st.session_state.strategy_notes[notes_key] = notes
        st.success("✅ Notes saved!")
```

**Lines of Code**: ~150 lines (tab reorganization + notes feature)

---

### Phase 5: Peace Mediation Tools

**Goal**: Provide facilitators with academic frameworks for conflict resolution.

**Facilitator Tab Structure:**
```python
peace_tabs = st.tabs([
    "📊 Peace Context",          # Tool overview
    "🤝 CBM Recommendations",    # Osgood (1962)
    "🏛️ Domestic Politics",     # Putnam (1988)
    "⚠️ Spoiler Analysis",       # Stedman (1997)
    "🌐 Multi-Track Diplomacy"   # Diamond & McDonald (1996)
])
```

**5.1: CBM Library Integration**

```python
from scs_mediator_sdk.peace_mediation.cbm_library import CBMLibrary

cbm_library = CBMLibrary()

# Interactive parameter selection
trust_level = st.slider("Current Trust Level", 1, 10, 5)
escalation = st.slider("Escalation Level", 1, 10, 5)
timeline = st.selectbox("Timeline", ["short", "medium", "long"])

# Get sequenced recommendations
cbms = cbm_library.recommend_cbms(
    trust_level=trust_level,
    escalation_level=escalation,
    timeline=timeline,
    category="communication"  # or "transparency", "military", "economic"
)

# Display recommendations
for cbm in cbms:
    st.write(f"**{cbm.name}**")
    st.write(f"*Category*: {cbm.category}")
    st.write(f"*Steps*: {cbm.implementation_steps}")
    st.write(f"*Expected Outcome*: {cbm.expected_outcome}")
```

**5.2: Win-Set Analyzer**

```python
from scs_mediator_sdk.peace_mediation.win_set_analyzer import WinSetAnalyzer

analyzer = WinSetAnalyzer()

# Party selection
party = st.selectbox("Select Party", ["Philippines", "China", "Malaysia", "Vietnam"])

# Calculate win-set size
win_set = analyzer.calculate_win_set(
    party=party,
    issue="territorial_dispute"
)

st.metric("Win-Set Size", f"{win_set.size}%",
          help="Percentage of agreements ratifiable domestically")

# Identify deal-breakers
st.write("**Deal-Breakers:**")
for constraint in win_set.constraints:
    st.write(f"- {constraint.description} (veto player: {constraint.actor})")

# Test proposal acceptability
proposal_acceptable = analyzer.test_proposal_acceptability(
    party=party,
    proposal=current_proposal
)

if proposal_acceptable:
    st.success("✅ Proposal likely acceptable domestically")
else:
    st.error("❌ Proposal may face domestic opposition")
```

**5.3: Spoiler Manager**

```python
from scs_mediator_sdk.peace_mediation.spoiler_manager import SpoilerManager

spoiler_mgr = SpoilerManager()

# Pre-configured spoiler database
spoilers = spoiler_mgr.get_potential_spoilers(scenario="south_china_sea")

for spoiler in spoilers:
    st.write(f"**{spoiler.name}**")
    st.write(f"*Type*: {spoiler.type}")  # 'greedy', 'limited', 'total'
    st.write(f"*Capability*: {spoiler.capability}/10")
    st.write(f"*Motivation*: {spoiler.motivation}")

# Risk assessment
risk = spoiler_mgr.assess_spoiler_risk(
    agreement=current_proposal,
    spoilers=spoilers
)

st.metric("Spoiler Risk", f"{risk}%")

# Protective measures
measures = spoiler_mgr.recommend_protective_measures(risk_level=risk)
st.write("**Recommended Measures:**")
for measure in measures:
    st.write(f"- {measure}")
```

**5.4: Multi-Track Mediator**

```python
from scs_mediator_sdk.peace_mediation.multi_track_mediator import MultiTrackMediator

mediator = MultiTrackMediator()

# Phase-based recommendations
phase = st.selectbox("Negotiation Phase",
                     ["pre-negotiation", "negotiation", "implementation"])

recommendations = mediator.get_track_recommendations(
    phase=phase,
    scenario="maritime_dispute"
)

# Display 9-track framework
for track_num, activities in recommendations.items():
    st.write(f"**Track {track_num}**: {activities['track_name']}")
    for activity in activities['recommendations']:
        st.write(f"- {activity['activity']} (Timeline: {activity['timeline']})")
```

**Lines of Code**: ~360 lines (5 sub-tabs + tool integration)

---

### Phase 6: AI Guide System

**Goal**: Provide context-aware AI assistance with parameter alignment.

**6.1: System Architecture**

```python
# Two distinct personas
INSTRUCTOR_PERSONA = "Dr. Marina Chen"  # For facilitators
PARTICIPANT_PERSONA = "Ambassador Zhou Wei"  # For players

# RAG-enhanced responses
chatbot = ChatbotInterface(
    persona=INSTRUCTOR_PERSONA,
    rag_enabled=True,
    doc_sources=[
        "MULTIPLAYER_USER_GUIDE.md",
        "academic_literature/",
        "scenario_docs/"
    ]
)
```

**6.2: Parameter-Aware Context Injection**

**Problem Solved**: AI was suggesting parameters not in simulation (e.g., "joint patrol frequency" when that parameter doesn't exist).

**Solution**: Three-tier guidance structure (implemented in this session):

```python
# System prompt enhancement (chatbot.py:191-336)
PARAMETER_ALIGNMENT_REQUIREMENT = """
When providing recommendations, you MUST clearly distinguish between:

1. **PRIMARY RECOMMENDATIONS** (aligned with simulation parameters):
   - Focus on parameters available in the current scenario
   - Use specific parameter names and ranges (e.g., "standoff_nm: 0-10 nautical miles")
   - Recommend strategic actions from the available action library
   - These should be your MAIN guidance - actionable within the simulation

2. **ADDITIONAL CONSIDERATIONS** (theoretical/contextual guidance):
   - Broader strategic or theoretical insights
   - Real-world factors not modeled in simulation
   - Clearly label these as "Additional Considerations"
   - Explain why these matter even if not directly simulated

3. **NOVEL SUGGESTIONS** (beyond current simulation):
   - If suggesting parameters/actions not in the simulation, explicitly flag them
   - Use format: "⚠️ NOVEL SUGGESTION (not in current simulation): [suggestion]"
   - Explain how facilitators might incorporate this (e.g., adjust scenario parameters)
"""
```

**6.3: Context Enhancement Implementation**

```python
# Extract simulation parameters from ISSUE_METADATA (multiplayer_app.py:1293-1325)
def build_parameter_context(session: Session) -> Dict[str, Any]:
    """Build parameter dictionary for AI context"""
    sim_params = {}
    scenario = SCENARIOS.get(session.scenario_id, {})
    issue_types = scenario.get('issue_types', [])

    for issue_type in issue_types:
        if issue_type in ISSUE_METADATA:
            metadata = ISSUE_METADATA[issue_type]
            for field in metadata.get('fields', []):
                param_info = {'label': field['label']}

                # Add range if numeric
                if 'min' in field and 'max' in field:
                    param_info['range'] = f"{field['min']}-{field['max']}"

                # Add options if categorical
                elif 'options' in field:
                    param_info['options'] = field['options']

                sim_params[field['key']] = param_info

    return sim_params

# Inject into AI context
chatbot.set_context(
    scenario=session.scenario_id,
    session_code=session.session_code,
    simulation_parameters=sim_params,
    strategic_actions=["Host Regional Summit", "Propose Joint Development", ...]
)
```

**6.4: Enhanced Context Display**

```python
# Context injection (chatbot.py:404-483)
def _enhance_question_with_context(self, question: str) -> str:
    """Inject available parameters into every query"""
    context_str = f"User Question: {question}\n\n"

    # Add simulation parameters if available
    if "simulation_parameters" in self.context:
        context_str += "\n**AVAILABLE SIMULATION PARAMETERS** (use these in your recommendations):\n"
        params = self.context["simulation_parameters"]
        for param_name, param_info in params.items():
            if isinstance(param_info, dict):
                context_str += f"  - {param_name}: {param_info.get('label', param_name)}\n"
                if 'range' in param_info:
                    context_str += f"    Range: {param_info['range']}\n"
                elif 'options' in param_info:
                    context_str += f"    Options: {', '.join(param_info['options'])}\n"

    # Add available strategic actions if provided
    if "strategic_actions" in self.context:
        context_str += "\n**AVAILABLE STRATEGIC ACTIONS** (players can execute these):\n"
        actions = self.context["strategic_actions"]
        for action in actions:
            context_str += f"  - {action}\n"

    return context_str
```

**6.5: Example AI Response Structure**

**User Query**: "What standoff distance should I recommend for the resupply scenario?"

**AI Response**:
```
**Primary Recommendation (Simulation Parameters):**
I recommend setting standoff_nm to 5.0 nautical miles (available range: 0-10 nautical miles).
This balances security concerns with de-escalation goals.

Rationale:
- Provides adequate safety buffer for resupply operations
- Reduces perceived threat (Fisher & Ury 1981: interest-based positioning)
- Historically, 5nm has been used in similar agreements (Fravel 2008)

Strategic Actions to Combine:
- Have players execute "Initiate Track II Dialogue" to build trust before proposing
- Consider "Increase Transparency" to reduce uncertainty around escort intentions

**Additional Considerations:**
While not directly modeled, consider environmental factors:
- Weather conditions in the South China Sea (monsoon season affects safe distances)
- Ship maneuverability (larger vessels need more space)
- Historical precedents from COC negotiations (Thayer 2011)

These don't appear as simulation parameters but should inform your facilitation discussion.

⚠️ **Novel Suggestion (not in current simulation):**
Consider adding a "contingency distance" parameter for emergency situations (e.g., medical
evacuations requiring closer approach). This would require modifying the scenario's
ISSUE_METADATA to include a new field. Discuss with players whether this refinement would
add value to the exercise.
```

**Lines of Code**: ~280 lines (2 personas × ~94 lines + context enhancement ~92 lines)

---

## AI Guide System

### Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  User Query (Streamlit)                   │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│              ChatbotInterface.ask_question()              │
│  1. Retrieve relevant docs (RAG)                          │
│  2. Inject simulation parameters                          │
│  3. Inject strategic actions                              │
│  4. Format with persona & academic requirements           │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│                  FAISS Vector Store                       │
│  • 500+ document chunks                                   │
│  • User guide, implementation plan, academic papers       │
│  • Top-K retrieval (K=5)                                  │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│                  LangChain LLM Call                       │
│  • Model: GPT-4                                           │
│  • Temperature: 0.7                                       │
│  • Max tokens: 1000                                       │
│  • System prompt: INSTRUCTOR or PARTICIPANT               │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│              Structured Response (3-tier)                 │
│  1. Primary recommendations (simulation-aligned)          │
│  2. Additional considerations (theoretical)               │
│  3. Novel suggestions (explicitly flagged)                │
└──────────────────────────────────────────────────────────┘
```

### RAG System Implementation

**Document Preprocessing:**
```python
# rag_system.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def build_rag_index(doc_paths: List[str]) -> FAISS:
    """Build vector store from documentation"""

    # Load documents
    documents = []
    for path in doc_paths:
        with open(path, 'r') as f:
            documents.append(f.read())

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "]
    )
    chunks = text_splitter.create_documents(documents)

    # Create embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

    # Build FAISS index
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore
```

**Query-time Retrieval:**
```python
def retrieve_relevant_context(question: str, vectorstore: FAISS, k: int = 5) -> str:
    """Retrieve top-K relevant document chunks"""

    docs = vectorstore.similarity_search(question, k=k)

    context = "\n\n---\n\n".join([
        f"**Source**: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
        for doc in docs
    ])

    return context
```

### Conversation History Management

```python
# chatbot.py
class ChatbotInterface:
    def __init__(self, session_id: str, persona: str):
        self.session_id = session_id
        self.persona = persona
        self.conversation_history: List[Tuple[str, str]] = []  # (question, answer) pairs

    def ask_question(self, question: str) -> str:
        """Ask question with history context"""

        # Retrieve RAG context
        rag_context = retrieve_relevant_context(question, self.vectorstore)

        # Build conversation history string
        history_str = "\n".join([
            f"Previous Q: {q}\nPrevious A: {a}"
            for q, a in self.conversation_history[-3:]  # Last 3 exchanges
        ])

        # Construct full prompt
        full_prompt = f"""
{self.system_prompt}

{history_str}

**Retrieved Context:**
{rag_context}

**Current Question:**
{question}

**Available Simulation Parameters:**
{self.context.get('simulation_parameters', {})}

**Available Strategic Actions:**
{self.context.get('strategic_actions', [])}
"""

        # Call LLM
        response = self.llm.generate(full_prompt)

        # Store in history
        self.conversation_history.append((question, response))

        return response

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
```

### Academic Citation Enforcement

**System Prompt Requirement:**
```python
CITATION_REQUIREMENT = """
When discussing negotiation theory or conflict resolution, you MUST cite relevant academic
sources. Use author-year format: (Fisher & Ury 1981), (Putnam 1988), etc.

Required citations for common topics:
- Principled negotiation: Fisher & Ury (1981)
- Two-level games: Putnam (1988)
- Confidence-building: Osgood (1962)
- Audience costs: Fearon (1994)
- International legitimacy: Hurd (2007)
- Soft power: Nye (2004)
- Strategic positioning: Schelling (1960)
- Agent-based modeling: Epstein & Axtell (1996)
- Escalation dynamics: Bremer (1992)

If no source is available, state: "This recommendation is based on practitioner experience
rather than published research."
"""
```

---

## Simulation Engine

### Mesa Agent-Based Model

**Model Structure:**

```python
# scs_model.py
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

class SCSModel(Model):
    """South China Sea maritime dispute simulation"""

    def __init__(self, agreement_params: Dict[str, Any], num_steps: int = 100):
        super().__init__()
        self.agreement_params = agreement_params
        self.schedule = RandomActivation(self)
        self.current_step = 0

        # Create agents for each country
        self.agents = {
            'PH_GOV': StateAgent('PH_GOV', self, strategic_context),
            'PRC_MARITIME': StateAgent('PRC_MARITIME', self, strategic_context),
            'VN_CG': StateAgent('VN_CG', self, strategic_context),
        }

        for agent in self.agents.values():
            self.schedule.add(agent)

        # Data collection
        self.datacollector = DataCollector(
            model_reporters={
                "incident_count": lambda m: m.incident_count,
                "escalation_frequency": lambda m: m.escalation_frequency,
                "average_severity": lambda m: m.average_severity
            },
            agent_reporters={
                "stress_level": "stress_level",
                "cooperation": "cooperation"
            }
        )

    def step(self):
        """Execute one time step"""
        self.current_step += 1

        # Generate potential incidents (stochastic)
        if random.random() < self.calculate_incident_probability():
            incident = self.generate_incident()
            self.handle_incident(incident)

        # Agents react
        self.schedule.step()

        # Collect data
        self.datacollector.collect(self)

    def calculate_incident_probability(self) -> float:
        """
        Calculate probability of incident based on agreement parameters.

        Factors:
        - Standoff distance (closer = higher probability)
        - Number of escorts (more = higher probability)
        - Inspection protocol (intrusive = higher probability)
        - Strategic context (low legitimacy = higher probability)
        """
        base_probability = 0.15  # 15% per time step

        # Standoff distance effect
        standoff = self.agreement_params.get('standoff_nm', 5.0)
        if standoff < 3:
            base_probability *= 1.5  # 50% increase if too close
        elif standoff > 7:
            base_probability *= 0.7  # 30% decrease if far apart

        # Escort effect
        num_escorts = self.agreement_params.get('num_escorts', 2)
        if num_escorts > 3:
            base_probability *= 1.3  # More escorts = more tension

        # Strategic context modifier
        avg_legitimacy = np.mean([
            agent.strategic_context.international_legitimacy
            for agent in self.agents.values()
        ])
        if avg_legitimacy < 40:
            base_probability *= 1.4  # Low legitimacy increases incidents

        return min(base_probability, 0.9)  # Cap at 90%
```

### Agent Behavior

```python
# agents.py
class StateAgent(Agent):
    """Represents a state actor (Philippines, China, Vietnam, etc.)"""

    def __init__(self, unique_id: str, model: Model, strategic_context: StrategicContext):
        super().__init__(unique_id, model)
        self.strategic_context = strategic_context
        self.stress_level = 0.0  # 0-1 scale
        self.cooperation = 0.5   # 0-1 scale
        self.recent_incidents = []

    def step(self):
        """Agent behavior each time step"""

        # Update stress based on recent incidents
        self.update_stress()

        # Decide whether to cooperate or defect
        cooperation_decision = self.decide_cooperation()

        # Update cooperation level
        self.cooperation = cooperation_decision

    def update_stress(self):
        """Calculate stress from recent incidents"""
        if not self.recent_incidents:
            self.stress_level *= 0.95  # Decay stress
            return

        # Count high-severity recent incidents
        high_severity_count = sum(
            1 for incident in self.recent_incidents[-10:]
            if incident.severity >= 7
        )

        self.stress_level = min(high_severity_count / 10.0, 1.0)

    def decide_cooperation(self) -> float:
        """
        Decide cooperation level based on:
        - Strategic context (high legitimacy → cooperate)
        - Stress level (high stress → defect)
        - Agreement parameters (fair agreement → cooperate)
        """
        base_cooperation = 0.5

        # Strategic context effect (Nye 2004)
        if self.strategic_context.international_legitimacy > 60:
            base_cooperation += 0.2
        elif self.strategic_context.international_legitimacy < 40:
            base_cooperation -= 0.2

        # Stress effect (Bremer 1992: stressed states escalate)
        base_cooperation -= self.stress_level * 0.3

        # Domestic support effect (Putnam 1988)
        if self.strategic_context.domestic_support < 40:
            base_cooperation -= 0.15  # Domestic pressure to be tough

        return np.clip(base_cooperation, 0.0, 1.0)
```

### Incident Generation

```python
# incident_generator.py
class IncidentGenerator:
    """Generate maritime incidents based on escalation ladder"""

    def generate_incident(self, current_stress: float) -> Incident:
        """
        Generate incident with severity based on current tension level.
        Uses Kahn's escalation ladder framework.
        """
        # Base severity increases with stress
        base_severity = int(current_stress * 10)  # 0-10 scale

        # Add stochastic variation
        severity = max(1, min(10, base_severity + random.randint(-2, 2)))

        # Map severity to incident type (Kahn escalation ladder)
        incident_types = {
            1: "Political gesture (statement of concern)",
            2: "Diplomatic protest",
            3: "Legal action (arbitration filing)",
            4: "Economic sanctions",
            5: "Show of force (increased patrols)",
            6: "Harassing action (water cannon)",
            7: "Local violence (ramming)",
            8: "Limited military action",
            9: "Major conventional action",
            10: "Full-scale war"
        }

        return Incident(
            type=incident_types[severity],
            severity=severity,
            timestamp=datetime.now(),
            actors=self._select_actors(),
            location=self._select_location()
        )
```

### Simulation Results Processing

```python
def run_simulation(agreement: Dict[str, Any], strategic_contexts: Dict[str, StrategicContext]) -> Dict[str, Any]:
    """
    Run full simulation and return results.

    Returns:
        {
            'incident_count': int,
            'escalation_frequency': float,  # % of incidents that escalated
            'average_severity': float,      # 1-10 scale
            'trend': str,                   # 'stable', 'increasing', 'decreasing'
            'events': List[Incident],       # All incidents
            'time_series': List[float],     # Severity over time
        }
    """
    model = SCSModel(agreement_params=agreement, num_steps=100)

    # Inject strategic contexts
    for player_id, context in strategic_contexts.items():
        if player_id in model.agents:
            model.agents[player_id].strategic_context = context

    # Run simulation
    for _ in range(100):
        model.step()

    # Collect results
    results = {
        'incident_count': model.incident_count,
        'escalation_frequency': model.escalation_count / max(model.incident_count, 1),
        'average_severity': np.mean([inc.severity for inc in model.incidents]),
        'trend': calculate_trend(model.incidents),
        'events': model.incidents,
        'time_series': model.datacollector.get_model_vars_dataframe()['average_severity'].tolist()
    }

    return results

def calculate_trend(incidents: List[Incident]) -> str:
    """Calculate whether incidents are increasing, stable, or decreasing"""
    if len(incidents) < 10:
        return "insufficient_data"

    # Split into first and second half
    mid = len(incidents) // 2
    first_half_avg = np.mean([inc.severity for inc in incidents[:mid]])
    second_half_avg = np.mean([inc.severity for inc in incidents[mid:]])

    if second_half_avg > first_half_avg + 1.0:
        return "increasing"
    elif second_half_avg < first_half_avg - 1.0:
        return "decreasing"
    else:
        return "stable"
```

---

## API Specifications

### SessionManager API

```python
class SessionManager:
    """Core API for session management"""

    def create_session(self, facilitator_id: str, scenario_id: str) -> Tuple[str, str]:
        """
        Create a new session.

        Args:
            facilitator_id: ID of the facilitator
            scenario_id: Scenario identifier (e.g., 'scenario_resupply')

        Returns:
            Tuple of (session_id, session_code)

        Example:
            sm = get_session_manager()
            session_id, code = sm.create_session("facilitator_123", "scenario_resupply")
            # Returns: ("session_20250109_143022_1234", "REEF-5678")
        """
        pass

    def get_session_by_code(self, session_code: str) -> Optional[Session]:
        """
        Retrieve session by user-friendly code.

        Args:
            session_code: Session code (e.g., "REEF-5678")

        Returns:
            Session object or None if not found
        """
        pass

    def join_session(self, session_code: str, user_name: str, role: str) -> Tuple[bool, str, Optional[str]]:
        """
        Player joins a session.

        Args:
            session_code: Session code to join
            user_name: Player's display name
            role: Role to play (e.g., 'PH_GOV')

        Returns:
            Tuple of (success, message, player_id)

        Example:
            success, msg, player_id = sm.join_session("REEF-5678", "Alice", "PH_GOV")
            # Returns: (True, "Joined as PH_GOV", "player_20250109_143045_567")

        Error Cases:
            - Session not found: (False, "Session not found", None)
            - Role taken: (False, "Role PH_GOV is already taken", None)
        """
        pass

    def submit_proposal(self, session_id: str, proposer_id: str, proposal_data: Dict[str, Any]) -> Optional[str]:
        """
        Submit a new proposal.

        Args:
            session_id: Session ID
            proposer_id: 'facilitator' or player_id
            proposal_data: Agreement terms

        Returns:
            proposal_id if successful, None otherwise

        Example:
            proposal_id = sm.submit_proposal(
                session_id="session_123",
                proposer_id="facilitator",
                proposal_data={
                    'standoff_nm': 5.0,
                    'num_escorts': 2,
                    'escort_roe': 'defensive_only'
                }
            )
        """
        pass

    def submit_response(self, session_id: str, proposal_id: str, player_id: str,
                       response_type: str, explanation: str = "") -> bool:
        """
        Player submits response to a proposal.

        Args:
            session_id: Session ID
            proposal_id: Proposal ID
            player_id: Player ID
            response_type: 'accept' | 'reject' | 'conditional'
            explanation: Optional explanation text

        Returns:
            True if successful, False otherwise

        Example:
            success = sm.submit_response(
                session_id="session_123",
                proposal_id="proposal_123_1_143500",
                player_id="player_567",
                response_type="accept",
                explanation="The 5nm standoff is acceptable for our security needs."
            )
        """
        pass
```

### ChatbotInterface API

```python
class ChatbotInterface:
    """AI Guide interface"""

    def __init__(self, session_id: str, persona: str, rag_enabled: bool = True):
        """
        Initialize chatbot.

        Args:
            session_id: Unique session ID for conversation persistence
            persona: 'instructor' or 'participant'
            rag_enabled: Enable document retrieval
        """
        pass

    def set_context(self, **kwargs):
        """
        Update chatbot context.

        Args:
            scenario: Scenario ID
            session_code: Session code
            session_status: Session status
            num_players: Number of players
            simulation_parameters: Dict of available parameters
            strategic_actions: List of available actions

        Example:
            chatbot.set_context(
                scenario="scenario_resupply",
                session_code="REEF-5678",
                session_status="negotiating",
                num_players=2,
                simulation_parameters={
                    'standoff_nm': {'label': 'Standoff Distance', 'range': '0-10'},
                    'num_escorts': {'label': 'Number of Escorts', 'range': '0-5'}
                },
                strategic_actions=["Host Regional Summit", "Initiate Track II Dialogue"]
            )
        """
        pass

    def ask_question(self, question: str) -> str:
        """
        Ask a question and get AI response.

        Args:
            question: User's question

        Returns:
            AI-generated response (markdown formatted)

        Example:
            response = chatbot.ask_question("What standoff distance should I recommend?")
        """
        pass

    def clear_history(self):
        """Clear conversation history"""
        pass

    def get_quick_tips(self, num_tips: int = 3) -> List[str]:
        """
        Get quick tips for current context.

        Args:
            num_tips: Number of tips to return

        Returns:
            List of tip strings
        """
        pass
```

---

## State Management

### Streamlit Session State Structure

```python
# Per-user session state (Streamlit st.session_state)
{
    # Role & identity
    'user_type': 'facilitator' | 'player',
    'user_name': str,
    'session_id': str,          # Facilitator: session ID, Player: player ID
    'session_code': str,        # Session code for joining
    'role': str,                # Player only: 'PH_GOV' | 'PRC_MARITIME' | etc.

    # UI state
    'view': 'create' | 'join' | 'facilitator_view' | 'player_view',
    'ready': bool,              # Player only: ready status

    # Strategic context
    'strategic_context': StrategicContext,  # Player only

    # Strategy notes (Phase 4)
    'strategy_notes': {
        'notes_{player_id}': str  # Player's private notes
    },

    # AI Guide
    'ai_guide': ChatbotInterface,  # Initialized per user

    # Peace tools (Facilitator only)
    'cbm_library': CBMLibrary,
    'win_set_analyzer': WinSetAnalyzer,
    'spoiler_manager': SpoilerManager,
    'multi_track_mediator': MultiTrackMediator,
}
```

### Global State (SessionManager Singleton)

```python
# Global session manager instance
_session_manager = SessionManager()

# Internal state structure
{
    'sessions': {
        'session_20250109_143022_1234': Session(
            session_id='session_20250109_143022_1234',
            session_code='REEF-5678',
            facilitator_id='facilitator_123',
            scenario_id='scenario_resupply',
            status='negotiating',
            current_round=1,
            players={
                'player_567': Player(...),
                'player_890': Player(...),
            },
            proposals=[Proposal(...)],
            responses={
                'proposal_123': [Response(...), Response(...)]
            },
            strategic_contexts={
                'player_567': StrategicContext(...),
                'player_890': StrategicContext(...),
            },
            simulation_results=None
        ),
        # ... more sessions
    },
    'session_codes': {
        'REEF-5678': 'session_20250109_143022_1234',
        # ... more codes
    }
}
```

### State Synchronization

**Problem**: Streamlit reruns entire script on every interaction, but we need shared state across users.

**Solution**:
1. **Per-user state**: `st.session_state` (Streamlit manages this)
2. **Shared state**: `SessionManager` singleton (Python module-level variable)
3. **Refresh mechanism**: `st.rerun()` after state changes

**Example Flow:**
```python
# Player submits response
if st.button("Submit Response"):
    # Update shared state
    sm = get_session_manager()
    success = sm.submit_response(session_id, proposal_id, player_id, response_type)

    if success:
        st.success("Response submitted!")
        st.rerun()  # Refresh UI to show updated state

# On next rerun, facilitator sees updated response count
session = sm.get_session(session_id)
num_responses = len(session.responses.get(proposal_id, []))
st.write(f"{num_responses}/{len(session.players)} players responded")
```

---

## Database Design

### Current MVP: In-Memory Storage

**Advantages:**
- Simple implementation
- No setup required
- Fast access (no I/O)

**Limitations:**
- Data lost on restart
- Not scalable to production
- No concurrent user support (single process)

### Production Database Schema (PostgreSQL)

**sessions table:**
```sql
CREATE TABLE sessions (
    session_id VARCHAR(100) PRIMARY KEY,
    session_code VARCHAR(20) UNIQUE NOT NULL,
    facilitator_id VARCHAR(100) NOT NULL,
    scenario_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,  -- 'setup', 'negotiating', 'simulating', 'completed'
    current_round INT DEFAULT 0,
    simulation_results JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_session_code (session_code),
    INDEX idx_facilitator (facilitator_id),
    INDEX idx_status (status)
);
```

**players table:**
```sql
CREATE TABLE players (
    player_id VARCHAR(100) PRIMARY KEY,
    session_id VARCHAR(100) REFERENCES sessions(session_id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    connected BOOLEAN DEFAULT TRUE,
    ready BOOLEAN DEFAULT FALSE,
    last_active TIMESTAMP DEFAULT NOW(),

    UNIQUE (session_id, role),  -- One player per role per session
    INDEX idx_session (session_id)
);
```

**proposals table:**
```sql
CREATE TABLE proposals (
    proposal_id VARCHAR(150) PRIMARY KEY,
    session_id VARCHAR(100) REFERENCES sessions(session_id) ON DELETE CASCADE,
    round_number INT NOT NULL,
    proposer_id VARCHAR(100) NOT NULL,
    proposal_data JSONB NOT NULL,  -- Flexible schema for different scenarios
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_session (session_id),
    INDEX idx_round (session_id, round_number)
);
```

**responses table:**
```sql
CREATE TABLE responses (
    response_id VARCHAR(150) PRIMARY KEY,
    proposal_id VARCHAR(150) REFERENCES proposals(proposal_id) ON DELETE CASCADE,
    player_id VARCHAR(100) REFERENCES players(player_id) ON DELETE CASCADE,
    response_type VARCHAR(20) NOT NULL,  -- 'accept', 'reject', 'conditional'
    explanation TEXT,
    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE (proposal_id, player_id),  -- One response per player per proposal
    INDEX idx_proposal (proposal_id)
);
```

**strategic_contexts table:**
```sql
CREATE TABLE strategic_contexts (
    context_id SERIAL PRIMARY KEY,
    player_id VARCHAR(100) REFERENCES players(player_id) ON DELETE CASCADE,
    diplomatic_capital FLOAT DEFAULT 50.0,
    international_legitimacy FLOAT DEFAULT 50.0,
    domestic_support FLOAT DEFAULT 50.0,
    credibility FLOAT DEFAULT 50.0,
    escalation_risk_modifier FLOAT DEFAULT 0.0,
    actions_taken JSONB DEFAULT '[]',
    updated_at TIMESTAMP DEFAULT NOW(),

    UNIQUE (player_id)
);
```

**conversations table (AI Guide history):**
```sql
CREATE TABLE conversations (
    conversation_id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,  -- facilitator or player session ID
    persona VARCHAR(20) NOT NULL,  -- 'instructor' or 'participant'
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),

    INDEX idx_session (session_id)
);
```

### Migration Strategy

**Phase 1**: Keep in-memory for MVP
**Phase 2**: Add PostgreSQL backend with dual-write (write to both, read from memory)
**Phase 3**: Switch to PostgreSQL-only with caching layer (Redis)
**Phase 4**: Add connection pooling and read replicas

**Code changes required:**
```python
# session_manager.py - Add database backend
class SessionManager:
    def __init__(self, use_database: bool = False):
        if use_database:
            self.db = DatabaseBackend()  # PostgreSQL connection
        else:
            self.sessions = {}  # In-memory (current MVP)

    def create_session(self, facilitator_id: str, scenario_id: str):
        session = Session(...)

        if self.db:
            self.db.insert_session(session)
        else:
            self.sessions[session.session_id] = session

        return session.session_id, session.session_code
```

---

## Security Considerations

### Current MVP Security Posture

**Authentication**: None (MVP assumes trusted environment)
**Authorization**: None (all users have full access)
**Data Protection**: No encryption
**Session Hijacking**: Possible (session codes are guessable)

### Production Security Requirements

#### 1. Authentication & Authorization

```python
# Implement user authentication
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Verify JWT token and return user"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return get_user_by_id(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Protect endpoints
@app.post("/api/sessions/create")
def create_session(
    scenario_id: str,
    current_user: User = Depends(get_current_user)
):
    """Only authenticated users can create sessions"""
    if not current_user.has_role("facilitator"):
        raise HTTPException(status_code=403, detail="Facilitator role required")

    sm = get_session_manager()
    return sm.create_session(current_user.id, scenario_id)
```

#### 2. Session Code Security

**Current**: 4-digit random number (10,000 possibilities) → easily guessable
**Recommendation**: 6-character alphanumeric (36^6 = 2.1 billion possibilities)

```python
def generate_session_code() -> str:
    """Generate cryptographically secure session code"""
    words = ['REEF', 'WAVE', 'TIDE', 'SAIL', 'CALM', 'BLUE']
    word = random.choice(words)

    # 6 characters: letters + numbers (36^6 = 2.1B combinations)
    chars = string.ascii_uppercase + string.digits
    code = ''.join(secrets.choice(chars) for _ in range(6))

    return f"{word}-{code}"  # Example: REEF-X7K9Q2
```

#### 3. Input Validation

```python
from pydantic import BaseModel, validator, Field

class ProposalData(BaseModel):
    """Validate proposal data"""
    standoff_nm: float = Field(ge=0, le=10, description="Standoff distance")
    num_escorts: int = Field(ge=0, le=5, description="Number of escorts")
    escort_roe: str = Field(regex="^(observe_only|defensive_only|weapons_free)$")

    @validator('standoff_nm')
    def standoff_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Standoff distance must be non-negative')
        return v

# Usage
try:
    proposal = ProposalData(**request_data)
except ValidationError as e:
    return {"error": e.errors()}
```

#### 4. Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/ai_guide/ask")
@limiter.limit("10/minute")  # Max 10 questions per minute
def ask_ai_guide(question: str, request: Request):
    """Rate-limited AI Guide endpoint"""
    return chatbot.ask_question(question)
```

#### 5. API Key Protection

```python
# Store API keys securely (not in code)
import os
from cryptography.fernet import Fernet

# Load encryption key from environment
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
fernet = Fernet(ENCRYPTION_KEY)

# Encrypt API key before storing in database
def encrypt_api_key(api_key: str) -> str:
    return fernet.encrypt(api_key.encode()).decode()

# Decrypt when needed
def decrypt_api_key(encrypted_key: str) -> str:
    return fernet.decrypt(encrypted_key.encode()).decode()

# Use environment variables for OpenAI key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")
```

---

## Performance Optimization

### Current Performance Profile

**Measured Metrics** (on local machine):
- Session creation: ~50ms
- Player join: ~30ms
- Proposal submission: ~20ms
- AI Guide query: ~2-5 seconds (LLM call dominates)
- Simulation run: ~3-8 seconds (100 steps)

### Optimization Strategies

#### 1. Database Query Optimization

```python
# Use connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # Verify connections before using
)

# Use eager loading to avoid N+1 queries
from sqlalchemy.orm import joinedload

session = db.query(Session).options(
    joinedload(Session.players),
    joinedload(Session.proposals).joinedload(Proposal.responses)
).filter_by(session_id=session_id).first()
```

#### 2. Caching Layer (Redis)

```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_session_cached(session_id: str) -> Optional[Session]:
    """Get session with Redis caching"""

    # Check cache first
    cached = redis_client.get(f"session:{session_id}")
    if cached:
        return Session(**json.loads(cached))

    # Cache miss - query database
    session = db.query(Session).filter_by(session_id=session_id).first()
    if session:
        # Cache for 5 minutes
        redis_client.setex(
            f"session:{session_id}",
            300,
            json.dumps(session.to_dict())
        )

    return session

def invalidate_session_cache(session_id: str):
    """Invalidate cache after updates"""
    redis_client.delete(f"session:{session_id}")
```

#### 3. Async AI Guide Queries

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)

async def ask_ai_guide_async(question: str) -> str:
    """Run AI query in background thread"""
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        executor,
        chatbot.ask_question,
        question
    )
    return response

# Usage in Streamlit
if st.button("Ask AI"):
    with st.spinner("Thinking..."):
        response = asyncio.run(ask_ai_guide_async(question))
        st.write(response)
```

#### 4. Simulation Parallelization

```python
from multiprocessing import Pool

def run_simulation_parallel(agreement: Dict, num_runs: int = 5) -> Dict:
    """Run multiple simulations in parallel and aggregate results"""

    with Pool(processes=5) as pool:
        results = pool.starmap(
            run_single_simulation,
            [(agreement, strategic_contexts) for _ in range(num_runs)]
        )

    # Aggregate results
    aggregated = {
        'incident_count': np.mean([r['incident_count'] for r in results]),
        'escalation_frequency': np.mean([r['escalation_frequency'] for r in results]),
        'average_severity': np.mean([r['average_severity'] for r in results]),
        'confidence_interval': calculate_confidence_interval(results)
    }

    return aggregated
```

#### 5. Frontend Optimization

```python
# Use st.cache_data for expensive computations
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_scenario_metadata(scenario_id: str) -> Dict:
    """Cached scenario metadata lookup"""
    return SCENARIOS[scenario_id]

# Use st.cache_resource for ML models
@st.cache_resource
def load_rag_vectorstore():
    """Load FAISS index once and reuse"""
    return FAISS.load_local("vectorstore_index")

# Lazy load heavy dependencies
@st.cache_resource
def get_chatbot():
    """Initialize chatbot only when needed"""
    return ChatbotInterface(...)
```

---

## Testing Strategy

### Unit Tests

**Location**: `tests/unit/`

```python
# tests/unit/test_session_manager.py
import pytest
from scs_mediator_sdk.multiplayer.session_manager import SessionManager

@pytest.fixture
def session_manager():
    """Fresh session manager for each test"""
    return SessionManager()

def test_create_session(session_manager):
    """Test session creation"""
    session_id, session_code = session_manager.create_session(
        facilitator_id="facilitator_123",
        scenario_id="scenario_resupply"
    )

    assert session_id is not None
    assert len(session_code) > 0
    assert "test" not in session_code.lower()  # Should be random

    # Verify session exists
    session = session_manager.get_session(session_id)
    assert session is not None
    assert session.facilitator_id == "facilitator_123"
    assert session.scenario_id == "scenario_resupply"
    assert session.status == "setup"

def test_join_session_success(session_manager):
    """Test player successfully joins session"""
    # Create session
    session_id, session_code = session_manager.create_session("facilitator_123", "scenario_resupply")

    # Player joins
    success, message, player_id = session_manager.join_session(
        session_code=session_code,
        user_name="Alice",
        role="PH_GOV"
    )

    assert success is True
    assert "Joined as PH_GOV" in message
    assert player_id is not None

    # Verify player added
    session = session_manager.get_session(session_id)
    assert player_id in session.players
    assert session.players[player_id].user_name == "Alice"

def test_join_session_role_taken(session_manager):
    """Test error when role already taken"""
    session_id, session_code = session_manager.create_session("facilitator_123", "scenario_resupply")

    # First player takes PH_GOV
    session_manager.join_session(session_code, "Alice", "PH_GOV")

    # Second player tries to take same role
    success, message, player_id = session_manager.join_session(session_code, "Bob", "PH_GOV")

    assert success is False
    assert "already taken" in message.lower()
    assert player_id is None

def test_submit_proposal(session_manager):
    """Test proposal submission"""
    session_id, _ = session_manager.create_session("facilitator_123", "scenario_resupply")

    proposal_id = session_manager.submit_proposal(
        session_id=session_id,
        proposer_id="facilitator",
        proposal_data={'standoff_nm': 5.0, 'num_escorts': 2}
    )

    assert proposal_id is not None

    # Verify proposal added
    session = session_manager.get_session(session_id)
    assert len(session.proposals) == 1
    assert session.proposals[0].proposal_id == proposal_id
    assert session.proposals[0].status == "pending"

def test_all_players_responded(session_manager):
    """Test proposal status update when all players respond"""
    session_id, session_code = session_manager.create_session("facilitator_123", "scenario_resupply")

    # Add 2 players
    _, _, player1_id = session_manager.join_session(session_code, "Alice", "PH_GOV")
    _, _, player2_id = session_manager.join_session(session_code, "Bob", "PRC_MARITIME")

    # Submit proposal
    proposal_id = session_manager.submit_proposal(session_id, "facilitator", {})

    # Both players accept
    session_manager.submit_response(session_id, proposal_id, player1_id, "accept")
    session_manager.submit_response(session_id, proposal_id, player2_id, "accept")

    # Check proposal status
    session = session_manager.get_session(session_id)
    proposal = session.proposals[0]
    assert proposal.status == "accepted"
    assert session.status == "simulating"
```

### Integration Tests

**Location**: `tests/integration/`

```python
# tests/integration/test_full_workflow.py
import pytest
from scs_mediator_sdk.multiplayer.session_manager import get_session_manager
from scs_mediator_sdk.simulation.scs_model import run_simulation

@pytest.fixture
def full_session():
    """Set up complete session with players"""
    sm = get_session_manager()
    session_id, session_code = sm.create_session("facilitator_123", "scenario_resupply")

    # Add players
    _, _, player1_id = sm.join_session(session_code, "Alice", "PH_GOV")
    _, _, player2_id = sm.join_session(session_code, "Bob", "PRC_MARITIME")

    # Mark ready
    sm.set_player_ready(session_id, player1_id, True)
    sm.set_player_ready(session_id, player2_id, True)

    # Start negotiation
    sm.start_negotiation(session_id)

    return session_id, player1_id, player2_id

def test_complete_negotiation_flow(full_session):
    """Test complete negotiation from proposal to simulation"""
    session_id, player1_id, player2_id = full_session
    sm = get_session_manager()

    # Facilitator submits proposal
    proposal_id = sm.submit_proposal(
        session_id=session_id,
        proposer_id="facilitator",
        proposal_data={
            'standoff_nm': 5.0,
            'num_escorts': 2,
            'escort_roe': 'defensive_only'
        }
    )

    # Players respond
    sm.submit_response(session_id, proposal_id, player1_id, "accept", "Acceptable terms")
    sm.submit_response(session_id, proposal_id, player2_id, "accept", "Fair compromise")

    # Check proposal accepted
    session = sm.get_session(session_id)
    assert session.proposals[0].status == "accepted"

    # Run simulation
    results = run_simulation(
        agreement=session.proposals[0].proposal_data,
        strategic_contexts=session.strategic_contexts
    )

    # Verify simulation results
    assert 'incident_count' in results
    assert 'escalation_frequency' in results
    assert results['incident_count'] >= 0
    assert 0 <= results['escalation_frequency'] <= 1

    # Save results
    sm.save_simulation_results(session_id, results)

    # Verify saved
    session = sm.get_session(session_id)
    assert session.simulation_results is not None
    assert session.status == "completed"
```

### End-to-End Tests (Streamlit UI)

**Location**: `tests/e2e/`

```python
# tests/e2e/test_ui_workflow.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

@pytest.fixture
def browser():
    """Set up headless browser"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:8506")
    yield driver
    driver.quit()

def test_create_and_join_session(browser):
    """Test creating session as facilitator and joining as player"""

    # Facilitator creates session
    role_select = browser.find_element(By.XPATH, "//select[@aria-label='Select your role']")
    role_select.send_keys("Facilitator")

    name_input = browser.find_element(By.XPATH, "//input[@placeholder='Enter your name']")
    name_input.send_keys("Dr. Smith")

    scenario_select = browser.find_element(By.XPATH, "//select[@aria-label='Select scenario']")
    scenario_select.send_keys("Resupply Ship Incident")

    create_button = browser.find_element(By.XPATH, "//button[text()='Create Session']")
    create_button.click()

    # Wait for session code
    wait = WebDriverWait(browser, 10)
    session_code_element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//code[contains(text(), '-')]"))
    )
    session_code = session_code_element.text

    assert len(session_code) > 0
    assert '-' in session_code

    # Open new tab to join as player
    browser.execute_script("window.open('http://localhost:8506', '_blank');")
    browser.switch_to.window(browser.window_handles[1])

    # Player joins
    role_select = browser.find_element(By.XPATH, "//select[@aria-label='Select your role']")
    role_select.send_keys("Player")

    code_input = browser.find_element(By.XPATH, "//input[@placeholder='Enter session code']")
    code_input.send_keys(session_code)

    name_input = browser.find_element(By.XPATH, "//input[@placeholder='Enter your name']")
    name_input.send_keys("Alice")

    player_role_select = browser.find_element(By.XPATH, "//select[@aria-label='Select role']")
    player_role_select.send_keys("PH_GOV")

    join_button = browser.find_element(By.XPATH, "//button[text()='Join Session']")
    join_button.click()

    # Verify joined
    success_message = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Joined as PH_GOV')]"))
    )
    assert success_message is not None
```

### Load Testing

**Location**: `tests/load/`

```python
# tests/load/test_concurrent_users.py
from locust import HttpUser, task, between

class MultiplayerUser(HttpUser):
    """Simulate concurrent users"""
    wait_time = between(1, 5)

    def on_start(self):
        """Initialize user session"""
        # Create or join session
        response = self.client.post("/api/sessions/create", json={
            "facilitator_id": f"user_{self.user_id}",
            "scenario_id": "scenario_resupply"
        })
        self.session_code = response.json()['session_code']

    @task(3)
    def view_session(self):
        """Simulate viewing session state"""
        self.client.get(f"/api/sessions/{self.session_code}")

    @task(1)
    def submit_proposal(self):
        """Simulate submitting proposal"""
        self.client.post(f"/api/sessions/{self.session_code}/proposals", json={
            'standoff_nm': 5.0,
            'num_escorts': 2
        })

    @task(2)
    def ask_ai_guide(self):
        """Simulate asking AI Guide"""
        self.client.post("/api/ai_guide/ask", json={
            'question': 'What standoff distance should I use?'
        })

# Run with: locust -f tests/load/test_concurrent_users.py --headless -u 50 -r 10
```

---

## Deployment Architecture

### Development Deployment

```yaml
# docker-compose.yml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8506:8506"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./src:/app/src
    command: streamlit run src/scs_mediator_sdk/ui/multiplayer_app.py --server.port 8506
```

### Production Deployment (AWS)

```
┌─────────────────────────────────────────────────────────────┐
│                    Route 53 (DNS)                            │
│              scs-mediator.example.com                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                CloudFront (CDN)                              │
│  • SSL/TLS termination                                       │
│  • DDoS protection                                           │
│  • Static asset caching                                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         Application Load Balancer (ALB)                      │
│  • Health checks                                             │
│  • Auto-scaling trigger                                      │
└────────┬───────────────────────────────────────┬────────────┘
         │                                       │
         ▼                                       ▼
┌──────────────────┐                  ┌──────────────────┐
│  ECS Fargate     │                  │  ECS Fargate     │
│  (Container 1)   │                  │  (Container 2)   │
│  • Streamlit App │                  │  • Streamlit App │
│  • 2 vCPU        │                  │  • 2 vCPU        │
│  • 4 GB RAM      │                  │  • 4 GB RAM      │
└────────┬─────────┘                  └────────┬─────────┘
         │                                     │
         └──────────────┬──────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  RDS PostgreSQL                              │
│  • db.t3.medium                                              │
│  • Multi-AZ deployment                                       │
│  • Automated backups                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               ElastiCache Redis                              │
│  • Session state caching                                     │
│  • cache.t3.micro                                            │
└─────────────────────────────────────────────────────────────┘
```

**Infrastructure as Code (Terraform):**

```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

# ECS Cluster
resource "aws_ecs_cluster" "scs_mediator" {
  name = "scs-mediator-cluster"
}

# ECS Task Definition
resource "aws_ecs_task_definition" "streamlit_app" {
  family                   = "scs-mediator-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "2048"
  memory                   = "4096"

  container_definitions = jsonencode([{
    name  = "streamlit"
    image = "${aws_ecr_repository.scs_mediator.repository_url}:latest"
    portMappings = [{
      containerPort = 8506
      protocol      = "tcp"
    }]
    environment = [
      {
        name  = "DATABASE_URL"
        value = "postgresql://${aws_db_instance.postgres.endpoint}/scs_mediator"
      },
      {
        name  = "REDIS_URL"
        value = "redis://${aws_elasticache_cluster.redis.cache_nodes[0].address}:6379"
      }
    ]
    secrets = [
      {
        name      = "OPENAI_API_KEY"
        valueFrom = aws_secretsmanager_secret.openai_key.arn
      }
    ]
  }])
}

# RDS PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier             = "scs-mediator-db"
  engine                 = "postgres"
  engine_version         = "14.7"
  instance_class         = "db.t3.medium"
  allocated_storage      = 100
  storage_type           = "gp3"
  multi_az               = true
  backup_retention_period = 7

  db_name  = "scs_mediator"
  username = "admin"
  password = random_password.db_password.result
}

# ElastiCache Redis
resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "scs-mediator-cache"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
}

# Auto Scaling
resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = 10
  min_capacity       = 2
  resource_id        = "service/${aws_ecs_cluster.scs_mediator.name}/${aws_ecs_service.streamlit.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "ecs_policy" {
  name               = "cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = 70.0
  }
}
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: scs-mediator
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ECS
        run: |
          aws ecs update-service --cluster scs-mediator-cluster --service streamlit-service --force-new-deployment
```

---

## Extension Points

### Adding New Scenarios

**Step 1**: Define scenario metadata

```python
# multiplayer_app.py
SCENARIOS = {
    'my_new_scenario': {
        'name': 'My New Scenario',
        'description': 'Description of the scenario',
        'issue_types': ['new_issue_type'],
        'roles': {
            'ROLE_A': {
                'name': 'Role A',
                'description': 'Description of Role A'
            },
            'ROLE_B': {
                'name': 'Role B',
                'description': 'Description of Role B'
            }
        }
    }
}
```

**Step 2**: Define issue metadata

```python
ISSUE_METADATA = {
    'new_issue_type': {
        'name': 'New Issue Type',
        'fields': [
            {
                'key': 'parameter_1',
                'label': 'Parameter 1',
                'type': 'number',
                'min': 0,
                'max': 100,
                'default': 50,
                'help': 'Description of parameter 1'
            },
            {
                'key': 'parameter_2',
                'label': 'Parameter 2',
                'type': 'select',
                'options': ['option1', 'option2', 'option3'],
                'default': 'option1',
                'help': 'Description of parameter 2'
            }
        ]
    }
}
```

**Step 3**: Add simulation logic

```python
# scs_model.py
def calculate_incident_probability(self) -> float:
    """Add handling for new parameters"""
    base_prob = 0.15

    # Existing logic...

    # New parameter effect
    if 'parameter_1' in self.agreement_params:
        value = self.agreement_params['parameter_1']
        if value > 75:
            base_prob *= 1.3  # High values increase risk

    return base_prob
```

### Adding New Strategic Actions

```python
# actions.py
new_action = StrategicAction(
    name="New Strategic Action",
    description="Description of what this action does",
    prerequisites={
        "diplomatic_capital": 40,
        "domestic_support": 50
    },
    cost={
        "diplomatic_capital": -10
    },
    parameter_effects={
        "incident_probability": -0.05,
        "parameter_1": +5
    },
    strategic_effects={
        "international_legitimacy": +8,
        "credibility": +3
    },
    risk_level="medium",
    academic_basis="Author (Year): Citation"
)

STRATEGIC_ACTIONS_LIBRARY.append(new_action)
```

### Adding New Peace Mediation Tools

```python
# peace_mediation/new_tool.py
class NewMediationTool:
    """New peace mediation tool"""

    def __init__(self):
        # Initialize tool
        pass

    def analyze(self, context: Dict) -> Dict:
        """Perform analysis"""
        # Implementation
        pass

    def recommend(self, analysis: Dict) -> List[str]:
        """Generate recommendations"""
        # Implementation
        pass

# Register tool
from scs_mediator_sdk.peace_mediation.new_tool import NewMediationTool

# Use in UI (multiplayer_app.py)
with st.expander("🆕 New Tool"):
    tool = NewMediationTool()
    results = tool.analyze(current_context)
    recommendations = tool.recommend(results)
    st.write(recommendations)
```

---

## Changelog

**Version 2.0 (2025-01-09)**:
- ✅ Phase 1: Core multiplayer foundation
- ✅ Phase 2: Strategic context tracking (4D soft power)
- ✅ Phase 3: Strategic actions system (6 actions)
- ✅ Phase 4: Enhanced player view (6-tab interface)
- ✅ Phase 5: Peace mediation tools (CBM, Win-Set, Spoiler, Multi-Track)
- ✅ Phase 6: AI Guide system (RAG-enhanced, parameter-aware)
- ✅ Parameter alignment system (three-tier guidance structure)
- ✅ Comprehensive documentation (Quick Start, User Guide, Testing Guide, Implementation Plan)

**Version 1.0 (2024)**:
- Single-player simulation
- Basic UI with facilitator view
- Escalation dynamics modeling
- Strategic levers (early version)

---

## References

**Academic Sources:**
- Epstein, J. M., & Axtell, R. (1996). *Growing Artificial Societies*. MIT Press.
- Fearon, J. D. (1994). "Domestic Political Audiences and the Escalation of International Disputes." *American Political Science Review*, 88(3), 577-592.
- Fisher, R., & Ury, W. (1981). *Getting to Yes: Negotiating Agreement Without Giving In*. Penguin Books.
- Hurd, I. (2007). "Breaking and Making Norms: American Revisionism and Crises of Legitimacy." *International Politics*, 44(2), 194-213.
- Nye, J. S. (2004). *Soft Power: The Means to Success in World Politics*. PublicAffairs.
- Osgood, C. E. (1962). *An Alternative to War or Surrender*. University of Illinois Press.
- Putnam, R. D. (1988). "Diplomacy and Domestic Politics: The Logic of Two-Level Games." *International Organization*, 42(3), 427-460.
- Schelling, T. C. (1960). *The Strategy of Conflict*. Harvard University Press.

**Technical Documentation:**
- Streamlit Documentation: https://docs.streamlit.io
- LangChain Documentation: https://python.langchain.com
- Mesa Documentation: https://mesa.readthedocs.io
- FastAPI Documentation: https://fastapi.tiangolo.com

---

**Document Version**: 1.0
**Maintained By**: SCS Mediator SDK Development Team
**Last Review**: 2025-01-09
**Next Review**: 2025-04-09
