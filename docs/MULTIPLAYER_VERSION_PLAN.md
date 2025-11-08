# Multiplayer Version - Design Plan
## Multi-User Negotiation Simulation

**Created**: January 2025
**Status**: Planning Phase
**Goal**: Allow multiple human players to negotiate as different stakeholders

---

## 🎯 Vision

Transform the single-user training tool into a **multi-player negotiation simulation** where:
- **Facilitator/Mediator**: 1 person facilitating the negotiation
- **Stakeholder Players**: 2-4 people, each playing a different country
- **Real-time interaction**: Players make offers, counteroffers, and negotiate
- **Simulation**: Final agreement is tested with agent-based model

---

## 🏗️ Architecture Design

### Option A: Turn-Based with Session Codes (Recommended)

**Why**: Works well with Streamlit's architecture, no WebSockets needed

**How It Works**:

```
┌─────────────────────────────────────────────────┐
│  1. Facilitator creates session                 │
│     → Gets SESSION CODE (e.g., "REEF-2024")     │
├─────────────────────────────────────────────────┤
│  2. Players join with session code              │
│     → Philippines player enters "REEF-2024"     │
│     → China player enters "REEF-2024"           │
│     → Each selects their role                   │
├─────────────────────────────────────────────────┤
│  3. Facilitator sees all connected players      │
│     → ✅ Philippines (connected)                │
│     → ✅ China (connected)                      │
│     → ⏳ Vietnam (waiting...)                   │
├─────────────────────────────────────────────────┤
│  4. Negotiation begins (turn-based)             │
│     → Facilitator proposes initial terms        │
│     → Each player reviews privately             │
│     → Players accept/reject/counteroffer        │
│     → Facilitator mediates next round           │
├─────────────────────────────────────────────────┤
│  5. Agreement reached or impasse                │
│     → If agreement: Run simulation              │
│     → If impasse: Analyze breakdown             │
└─────────────────────────────────────────────────┘
```

**Backend**:
- SQLite database for session state
- Streamlit's built-in session management
- Polling for updates (players refresh to see changes)

---

## 📊 User Roles & Views

### 1. Facilitator/Mediator

**What they see:**
- **Dashboard**: All players' status (connected/disconnected)
- **Proposal Builder**: Create agreement terms
- **All Offers**: See what each party is proposing
- **Mediation Tools**: Escalation ladder, CBMs, spoiler analysis
- **Simulation Control**: Run simulation on final agreement

**What they can do:**
- Start session, generate session code
- Propose initial/revised agreements
- See all players' preferences (but players can't see each other's)
- Mediate between parties
- Control negotiation rounds
- Decide when to move to simulation

**View**: `facilitator_multi_view.py`

---

### 2. Stakeholder Players (Philippines, China, Vietnam, Malaysia)

**What they see:**
- **Your Position**: Your interests, constraints, BATNA
- **Current Proposal**: What the facilitator/other party is proposing
- **Your Preferences**: Set your red lines and priorities (private)
- **Make Counteroffer**: Propose alternative terms
- **Other Players**: Basic status (connected, waiting, submitted offer)

**What they can do:**
- Join session with code
- Select their role (Philippines, China, etc.)
- Review proposals from facilitator
- Accept/Reject/Counteroffer
- Set their priorities and red lines (private to them)
- Submit their position
- Chat with facilitator (optional)

**What they CAN'T see:**
- Other players' utility scores
- Other players' red lines
- Facilitator's mediation notes
- Internal calculations

**View**: `player_view.py`

---

### 3. Observer (Optional)

**What they see:**
- Public negotiation progress
- Submitted proposals (when made public)
- Simulation results

**What they can do:**
- Watch the negotiation
- See final agreement
- View simulation results

**View**: `observer_view.py` (low priority)

---

## 🔄 Workflow: Turn-Based Negotiation

### Phase 1: Setup (5 minutes)

**Facilitator**:
1. Logs in, selects "Facilitator" role
2. Chooses scenario (e.g., Second Thomas Shoal)
3. Clicks "Create Session" → Gets code: **"REEF-2024"**
4. Shares code with players (via Zoom chat, email, etc.)

**Players**:
1. Open app in their browser
2. Enter session code: **"REEF-2024"**
3. Select their role:
   - Player 1: Philippines
   - Player 2: China
   - Player 3: Vietnam (optional)
   - Player 4: Malaysia (optional)
4. Wait for all players to connect

**Facilitator Dashboard**:
```
SESSION: REEF-2024
Scenario: Second Thomas Shoal

Players:
✅ Philippines (User: Alice) - Ready
✅ China (User: Bob) - Ready
⏳ Vietnam - Waiting...
❌ Malaysia - Not joined

[Start Negotiation] (button enabled when 2+ players ready)
```

---

### Phase 2: Opening Positions (10 minutes)

**Each Player Privately**:

Players see their role-specific view:

```
┌─────────────────────────────────────────────────┐
│ 🇵🇭 PHILIPPINES - Your Position                 │
├─────────────────────────────────────────────────┤
│ Your Interests:                                 │
│ • Maintain sovereignty over territorial waters  │
│ • Ensure safe resupply to BRP Sierra Madre      │
│ • Protect fishermen's livelihoods               │
│ • Avoid military escalation                     │
│                                                 │
│ Your BATNA: Continue ad-hoc resupply with risk │
│                                                 │
│ Your Constraints:                               │
│ • Must maintain garrison on Sierra Madre        │
│ • Cannot accept full Chinese control            │
│ • Must protect fishing communities              │
└─────────────────────────────────────────────────┘

Set Your Priorities (Visible only to you):

Resupply Operations:
  Standoff Distance:
    [Slider: 0-10nm]
    Your minimum acceptable: 2nm
    Your ideal: 5nm

  Pre-Notification:
    Your maximum acceptable: 48 hours
    Your ideal: 12 hours

[Mark as] Red Line | Negotiable | Flexible

[Submit Position] (button)
```

**Players submit** their opening positions (what they want, what they'll accept).

**Facilitator sees** a summary:

```
Opening Positions Summary:

Philippines wants:
• Standoff: 5nm (will accept 2nm minimum)
• Escorts: 2 (will accept 1 minimum)
• Notification: 12h (will accept 48h maximum)
• Red lines: Cannot accept < 2nm standoff

China wants:
• Standoff: 2nm (will accept 4nm maximum)
• Escorts: 0 (will accept 1 maximum)
• Notification: 72h (will accept 24h minimum)
• Red lines: Cannot accept > 1 escort vessel

OVERLAP ZONES:
• Standoff: 2-4nm (both can accept)
• Escorts: 1 (both can accept)
• Notification: 24-48h (both can accept)
```

---

### Phase 3: Round 1 - Facilitator Proposal (5 minutes)

**Facilitator**:
- Reviews opening positions
- Identifies overlap zones
- Proposes initial agreement in the overlap

```
ROUND 1 PROPOSAL (Facilitator):

Resupply Operations:
• Standoff Distance: 3nm
• Maximum Escorts: 1
• Pre-Notification: 24 hours

Communication:
• Hotline: 24/7
• CUES compliance: Required

[Send to All Players]
```

---

### Phase 4: Round 1 - Player Responses (5-10 minutes)

**Each Player Reviews**:

Philippines sees:
```
┌─────────────────────────────────────────────────┐
│ FACILITATOR'S PROPOSAL - Round 1                │
├─────────────────────────────────────────────────┤
│ Standoff Distance: 3nm                          │
│   Your position: Wanted 5nm, minimum 2nm        │
│   Assessment: ✅ Acceptable (within range)      │
│                                                 │
│ Maximum Escorts: 1                              │
│   Your position: Wanted 2, minimum 1            │
│   Assessment: ⚠️ At minimum threshold           │
│                                                 │
│ Pre-Notification: 24 hours                      │
│   Your position: Wanted 12h, max 48h            │
│   Assessment: ✅ Acceptable (within range)      │
└─────────────────────────────────────────────────┘

Overall Assessment: 🟡 MARGINAL
- Meets minimum requirements
- But close to red lines
- Consider requesting adjustments

Your Response:
( ) ✅ Accept this proposal
( ) 🤝 Accept with conditions (specify below)
(•) 🔄 Counteroffer (modify terms below)
( ) ❌ Reject (explain why below)

[Text box for explanation/counteroffer]

[Submit Response]
```

**China** sees similar view with their assessment.

**Players submit**:
- Philippines: "Accept with condition: Need 2 escorts during typhoon season"
- China: "Counteroffer: 48h notification, keep rest same"

---

### Phase 5: Round 2 - Mediation (5-10 minutes)

**Facilitator sees** all responses:

```
ROUND 1 RESPONSES:

Philippines: Accept with condition
  → Wants 2 escorts during typhoon season
  → Rationale: Safety concerns in bad weather

China: Counteroffer
  → Wants 48h notification (vs proposed 24h)
  → Rationale: Need time for coordination

MEDIATION OPTIONS:
1. Accept both conditions (typhoon + 48h)
2. Split the difference (seasonal escorts but keep 24h)
3. Trade-off (one gets escorts, other gets notification)
4. Ask for clarification/negotiation
```

**Facilitator** chooses option 3 (trade-off), proposes Round 2:

```
ROUND 2 PROPOSAL (Facilitator):

Based on your feedback, revised proposal:

• Standoff: 3nm (unchanged)
• Escorts: 1 normal, 2 during severe weather (PH request)
• Notification: 48h (China request)
• Hotline: 24/7 (unchanged)

Trade-off rationale:
- Philippines gets safety flexibility (weather escorts)
- China gets coordination time (48h notice)
- Both parties make one concession, get one win

[Send to All Players]
```

---

### Phase 6: Round 2 - Responses & Final Agreement (5 minutes)

**Players review** Round 2:

- Philippines: ✅ Accept (got escort flexibility)
- China: ✅ Accept (got notification time)

**Facilitator Dashboard**:

```
AGREEMENT REACHED! 🎉

Round 2 Proposal:
• Standoff: 3nm
• Escorts: 1 (2 during severe weather)
• Notification: 48h
• Hotline: 24/7

Acceptance:
✅ Philippines - Accepted
✅ China - Accepted

[Proceed to Simulation]
```

---

### Phase 7: Simulation (10 minutes)

**Facilitator** runs simulation with agreed terms.

**All players** see results together:

```
SIMULATION RESULTS (300 steps / 6 months)

Total Incidents: 19 ✅
Average Severity: 0.28 ✅
Trend: Declining ✅

Your Agreement Performance:
✅ Excellent outcome
✅ Low incident count
✅ High compliance (87%)
✅ Effective de-escalation

Key Events:
• 3 typhoon-season resupplies: Used 2-escort option successfully
• 16 routine resupplies: All completed without incident
• 2 close approaches: De-escalated via hotline
• 48h notification proved effective for coordination
```

---

## 💾 Technical Implementation

### Database Schema

**sessions table**:
```sql
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    session_code TEXT UNIQUE,
    facilitator_id TEXT,
    scenario_id TEXT,
    status TEXT, -- 'setup', 'negotiating', 'simulating', 'completed'
    current_round INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

**players table**:
```sql
CREATE TABLE players (
    player_id TEXT PRIMARY KEY,
    session_id TEXT,
    role TEXT, -- 'PH_GOV', 'PRC_MARITIME', 'VN_CG', 'MY_CG'
    user_name TEXT,
    connected BOOLEAN,
    ready BOOLEAN,
    last_active TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

**proposals table**:
```sql
CREATE TABLE proposals (
    proposal_id TEXT PRIMARY KEY,
    session_id TEXT,
    round_number INTEGER,
    proposer_id TEXT, -- 'facilitator' or player_id
    proposal_data JSON, -- Agreement terms
    status TEXT, -- 'pending', 'accepted', 'rejected', 'countered'
    created_at TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
```

**responses table**:
```sql
CREATE TABLE responses (
    response_id TEXT PRIMARY KEY,
    proposal_id TEXT,
    player_id TEXT,
    response_type TEXT, -- 'accept', 'reject', 'counteroffer', 'conditional'
    response_data JSON,
    explanation TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (proposal_id) REFERENCES proposals(proposal_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
```

---

### Key Functions to Implement

**Session Management**:
```python
def create_session(facilitator_id, scenario_id) -> str:
    """Create new session, return session code"""
    session_code = generate_code()  # e.g., "REEF-2024"
    # Save to database
    return session_code

def join_session(session_code, user_name, role) -> bool:
    """Player joins session with code"""
    # Verify code exists
    # Check role not taken
    # Add player to session
    return success

def get_session_status(session_id) -> dict:
    """Get current session state"""
    return {
        'players': [...],
        'current_round': 2,
        'latest_proposal': {...},
        'responses': [...]
    }
```

**Proposal Management**:
```python
def submit_proposal(session_id, proposer_id, terms) -> str:
    """Submit new proposal"""
    round_number = get_current_round(session_id) + 1
    proposal_id = save_proposal(session_id, round_number, proposer_id, terms)
    notify_players(session_id)
    return proposal_id

def submit_response(proposal_id, player_id, response_type, data) -> bool:
    """Player responds to proposal"""
    save_response(proposal_id, player_id, response_type, data)
    check_if_all_responded(proposal_id)
    return success

def check_agreement(proposal_id) -> bool:
    """Check if all players accepted"""
    responses = get_responses(proposal_id)
    return all(r['response_type'] == 'accept' for r in responses)
```

---

### UI Components

**Facilitator Dashboard** (`src/scs_mediator_sdk/ui/facilitator_multi_view.py`):
```python
import streamlit as st
from session_manager import create_session, get_session_status, submit_proposal

def facilitator_dashboard():
    st.title("🎯 Facilitator Dashboard")

    # Session creation
    if 'session_id' not in st.session_state:
        if st.button("Create New Session"):
            session_code = create_session(
                facilitator_id=st.session_state.user_id,
                scenario_id=selected_scenario
            )
            st.session_state.session_code = session_code
            st.success(f"Session created! Code: {session_code}")

    # Show connected players
    status = get_session_status(st.session_state.session_id)
    st.subheader("Connected Players")
    for player in status['players']:
        st.write(f"{'✅' if player['ready'] else '⏳'} {player['role']}: {player['user_name']}")

    # Proposal builder
    if all(p['ready'] for p in status['players']):
        st.subheader("Make Proposal")
        terms = build_proposal_ui()
        if st.button("Send Proposal to Players"):
            submit_proposal(st.session_state.session_id, 'facilitator', terms)
            st.rerun()

    # View responses
    if status.get('latest_proposal'):
        st.subheader("Player Responses")
        display_responses(status['latest_proposal'])
```

**Player View** (`src/scs_mediator_sdk/ui/player_multi_view.py`):
```python
import streamlit as st
from session_manager import join_session, submit_response, get_proposal

def player_view():
    st.title(f"🇵🇭 {get_role_name(st.session_state.role)}")

    # Join session
    if 'session_id' not in st.session_state:
        session_code = st.text_input("Enter Session Code:")
        role = st.selectbox("Select Your Role:", ['PH_GOV', 'PRC_MARITIME', 'VN_CG', 'MY_CG'])
        if st.button("Join Session"):
            success = join_session(session_code, st.session_state.user_name, role)
            if success:
                st.success("Joined session!")
                st.rerun()

    # Show your position
    st.subheader("Your Position")
    display_role_interests(st.session_state.role)

    # Review proposal
    proposal = get_proposal(st.session_state.session_id, current=True)
    if proposal:
        st.subheader("Current Proposal")
        display_proposal(proposal)

        # Response options
        response_type = st.radio("Your Response:",
            ['Accept', 'Accept with Conditions', 'Counteroffer', 'Reject'])
        explanation = st.text_area("Explanation/Details:")

        if st.button("Submit Response"):
            submit_response(
                proposal['id'],
                st.session_state.player_id,
                response_type.lower(),
                {'explanation': explanation}
            )
            st.success("Response submitted!")
            st.rerun()
```

---

## 📅 Implementation Phases

### Phase 1: Core Infrastructure (Week 1)
- [ ] Database setup (SQLite)
- [ ] Session management functions
- [ ] Session code generation
- [ ] Player join/connection logic
- [ ] Basic facilitator dashboard
- [ ] Basic player view

### Phase 2: Negotiation Workflow (Week 2)
- [ ] Proposal submission (facilitator)
- [ ] Proposal review (players)
- [ ] Response submission (accept/reject/counter)
- [ ] Response aggregation (facilitator view)
- [ ] Round progression logic
- [ ] Agreement detection

### Phase 3: Integration with Existing Features (Week 3)
- [ ] Integrate bargaining engine for utility calculation
- [ ] Connect simulation engine
- [ ] Add AI assistant for players
- [ ] Add mediation tools for facilitator
- [ ] Peace context features

### Phase 4: Polish & Testing (Week 4)
- [ ] Real-time status updates (polling/refresh)
- [ ] Error handling (disconnections, etc.)
- [ ] Session timeout/cleanup
- [ ] UI/UX improvements
- [ ] Testing with real users
- [ ] Documentation

---

## 🎮 Usage Scenarios

### Scenario 1: Classroom Training
- **Setup**: Instructor is facilitator
- **Players**: Students divided into country teams
- **Duration**: 60-90 minutes
- **Goal**: Learn negotiation skills, experience real-time pressure

### Scenario 2: Workshop/Conference
- **Setup**: Professional mediator facilitates
- **Players**: Participants from different organizations
- **Duration**: 2-3 hours (multiple rounds)
- **Goal**: Explore policy options, build empathy

### Scenario 3: Research Study
- **Setup**: Researcher facilitates
- **Players**: Study participants
- **Duration**: 90 minutes
- **Goal**: Collect data on decision-making, test theories

---

## 🔐 Security & Privacy Considerations

1. **Session Codes**: Random, hard to guess (e.g., "REEF-2024-X7K9")
2. **Player Privacy**: Each player only sees their own utility scores
3. **Private Preferences**: Red lines not shared with other players
4. **Facilitator Privilege**: Can see all information (by design)
5. **Data Storage**: Anonymize for research, delete after session
6. **No Authentication**: Use session codes only (simpler)

---

## ⚠️ Challenges & Solutions

**Challenge 1: Players disconnect**
- **Solution**: Save state in database, allow reconnection with same code/role

**Challenge 2: Slow players (holding up others)**
- **Solution**: Time limits per round, facilitator can override

**Challenge 3: Streamlit isn't real-time**
- **Solution**: Auto-refresh every 10 seconds, or manual refresh button

**Challenge 4: Session management complexity**
- **Solution**: Start simple (2 players), expand later

**Challenge 5: Deployment (Streamlit Cloud free tier)**
- **Solution**: Use SQLite (included), limit concurrent sessions

---

## 🚀 Getting Started

### For Developers

1. **Create database schema**:
   ```bash
   python3 src/scs_mediator_sdk/multi/setup_database.py
   ```

2. **Test locally**:
   ```bash
   streamlit run src/scs_mediator_sdk/ui/multi_player_app.py
   ```

3. **Open multiple browser tabs** to simulate players

### For Users

1. **Facilitator**:
   - Go to app URL
   - Select "Facilitator" role
   - Create session, share code

2. **Players**:
   - Go to same app URL
   - Enter session code
   - Select their role
   - Wait for others

---

## 📚 Next Steps

1. **Review this plan** with stakeholders
2. **Prioritize features** (core vs. nice-to-have)
3. **Estimate timeline** (4 weeks? 8 weeks?)
4. **Assign development** (who builds what?)
5. **Set up testing** (how to test multi-user flows?)

---

**Questions for Discussion**:
- Do we need real-time updates or is polling OK?
- Should players see each other's names/responses?
- How long should sessions stay active?
- Do we need a lobby/waiting room?
- Should there be a time limit per round?
- Do we want text chat between players?

---

**Last Updated**: January 2025
**Status**: Planning Phase - Awaiting Approval
