# Multiplayer Negotiation User Guide

**SCS Mediator SDK v2 - Complete Guide for Facilitators and Players**

This guide provides practical instructions for using the multiplayer negotiation system to simulate South China Sea territorial disputes and practice conflict resolution.

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Facilitator Guide](#facilitator-guide)
4. [Player Guide](#player-guide)
5. [Strategic Actions Guide](#strategic-actions-guide)
6. [Interpreting Simulation Results](#interpreting-simulation-results)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### What is this tool?

The SCS Mediator SDK provides a **multiplayer negotiation simulation** where:
- A **facilitator** creates and manages the negotiation session
- **Players** represent different countries/actors (Philippines, China, Vietnam, Malaysia)
- Players negotiate **agreement terms** to manage maritime incidents
- A **simulation** tests how well the agreement prevents escalation

### Who is this for?

- **Educational Settings**: International relations courses, conflict resolution training
- **Policy Research**: Testing different negotiation approaches
- **Wargaming**: Realistic maritime security scenarios
- **Professional Development**: Diplomats and negotiators in training

### Key Features

**Core Negotiation** (Phase 1):
- Session-based multiplayer coordination
- Dynamic proposal creation with 9 scenario types
- Accept/reject/conditional responses
- Agent-based simulation of outcomes

**Strategic Context** (Phase 2):
- 4-dimensional soft power tracking (Diplomatic Capital, Legitimacy, Support, Credibility)
- Per-player strategic position dashboard
- Escalation risk modifiers based on strategic position

**Strategic Actions** (Phase 3):
- 6 diplomatic moves players can execute
- Prerequisites and costs for each action
- Effects on both agreement parameters and strategic position

**Enhanced Player UX** (Phase 4):
- 6-tab player interface for clear navigation
- Persistent strategy notes
- Status-aware content (adapts to negotiation phase)

---

## Getting Started

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/scs_mediator_sdk_v2.git
cd scs_mediator_sdk_v2

# Install dependencies
pip install -r requirements.txt

# Start the application
streamlit run src/scs_mediator_sdk/ui/multiplayer_app.py --server.port 8506
```

The app will open in your browser at `http://localhost:8506`

### System Requirements

- **Python**: 3.9 or higher
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)
- **Memory**: 2GB RAM minimum
- **Network**: No internet connection required (runs locally)

### First-Time Setup

1. **Facilitator**: Opens app, creates session
2. **Players**: Join using session code provided by facilitator
3. **Setup Phase**: Players select roles and mark ready
4. **Negotiation**: Facilitator proposes agreement terms, players respond
5. **Simulation**: System tests agreement with agent-based model
6. **Debrief**: Review results and discuss outcomes

---

## Facilitator Guide

### Your Role

As the facilitator, you:
- Create and manage the negotiation session
- Select the scenario and set up the context
- Propose agreement terms for players to consider
- Run simulations to test negotiated agreements
- Monitor player strategic positions
- Guide the debrief discussion

You are **not** a player in the negotiation. Your role is to design realistic proposals and guide the process.

### Step 1: Create a Session

1. Open the app and select **"🎓 Create as Facilitator"**
2. Enter your name (e.g., "Professor Smith", "Dr. Johnson")
3. Select a scenario from the dropdown:
   - **Resupply Ship Incident**: Humanitarian vessel access during standoff
   - **Fishing Vessel Confrontation**: Managing civilian fishing rights
   - **Access Zone Dispute**: Defining permissible maritime zones
   - **Seasonal Fishing Agreement**: Time-based fishing access
   - **Enforcement Protocols**: Rules for coast guard interactions
   - **Communication Hotline**: Crisis communication setup
   - **Media Management**: Joint statement protocols
   - **Incident Response**: Procedures for managing crises
   - **Naval Exercise Notice**: Military activity transparency
4. Click **"🚀 Create Session"**
5. **Session Code** appears (e.g., "REEF-2024")
6. Share this code with players

**Tip**: Choose scenarios that match your learning objectives. Resupply and Fishing scenarios are good starting points for beginners.

---

### Step 2: Wait for Players

1. Navigate to **Tab 1 (🎯 Negotiation)**
2. Monitor the **"Connected Players"** section
3. Verify all expected players have joined
4. Wait for all players to click **"Mark as Ready"**

**Player Status Indicators**:
- ✅ **Green checkmark**: Player is ready
- ⏸️ **Gray icon**: Player is not ready
- 🔴 **Red icon**: Player disconnected

**Minimum Players**: At least 2 players required to start negotiation.

---

### Step 3: Start Negotiation

1. Once all players are ready, the **"🚀 Start Negotiation Round"** button activates
2. Click to begin the negotiation phase
3. Session status changes from "setup" to "negotiating"
4. Round counter advances to Round 1

---

### Step 4: Submit Proposals

**Your Proposal Strategy**:
- **First Proposal**: Start with **moderate** terms to gauge player preferences
- **Subsequent Proposals**: Adjust based on player feedback
- **Don't aim for perfection**: 2-3 rounds is typical

**How to Build a Proposal**:

Each scenario has different parameters. Here's an example for **Resupply Ship Incident**:

```
Parameter: Standoff Distance
  - What it means: How close vessels can approach
  - Range: 100-1000 meters
  - Tight control (200m): Higher security, lower trust
  - Lenient (500m): Lower security, higher trust

Parameter: Number of Escorts
  - What it means: Military vessels accompanying resupply
  - Range: 0-5
  - More escorts: Higher security, more provocative

Parameter: Escort Rules of Engagement
  - Options: Observe only, Defensive only, Weapons free
  - Defensive only: Balanced approach

Parameter: Inspection Protocol
  - Options: No inspection, Remote monitoring, Observer vessels, Physical boarding
  - Observer vessels: Compromise between transparency and sovereignty

Parameter: Communication Channel
  - Options: Open VHF, Encrypted VHF, Encrypted satellite
  - Encrypted VHF: Secure but accessible in emergency

Parameter: Regular Updates Frequency
  - What it means: How often to share status updates
  - Range: 1-24 hours
  - 6 hours: Standard diplomatic practice
```

**Guidance for Other Scenarios** (see Tab 5: 📖 Facilitator Guide for details):

- **Fishing Vessel**: Balance fishing access with territorial control
- **Access Zones**: Define clear boundaries while respecting interests
- **Seasonal Fishing**: Use time-based restrictions to reduce conflict
- **Enforcement**: Establish proportional responses to violations

**Submit the Proposal**:
1. Fill out all required fields
2. Click **"📤 Submit Proposal"**
3. Success message confirms submission
4. All players now see the proposal

---

### Step 5: Monitor Player Responses

1. Scroll to **"Player Responses"** section in Tab 1
2. Track response count (e.g., "2/3 players responded")
3. Review each player's response:
   - ✅ **Accept**: Player approves proposal
   - ❌ **Reject**: Player opposes proposal
   - 🔄 **Conditional**: Player accepts with reservations

**Reading the Room**:
- **Unanimous Accept**: Proposal status becomes "accepted" → Ready to simulate
- **Unanimous Reject**: Proposal status "rejected" → Revise substantially
- **Mixed Responses**: Proposal status "mixed" → Adjust and try again

**Player Explanations**: Pay close attention to player explanations. They reveal:
- Which parameters are deal-breakers
- What concessions players are willing to make
- Hidden interests and priorities

---

### Step 6: Revise or Simulate

**If Proposal is Rejected/Mixed**:
1. Review player feedback
2. Identify common concerns
3. Adjust parameters accordingly
4. Submit revised proposal (Round 2)
5. Repeat until proposal is accepted

**Typical Negotiation Arc**:
- **Round 1**: Moderate proposal → Mixed responses (some reject)
- **Round 2**: Adjusted proposal → Mostly accepts (one conditional)
- **Round 3**: Fine-tuned proposal → Unanimous acceptance

**If Proposal is Accepted**:
1. Session status changes to "simulating"
2. Scroll to **"Run Simulation"** section
3. Click **"🎮 Run Simulation with Accepted Agreement"**
4. Wait 5-10 seconds for simulation to complete

---

### Step 7: Analyze Simulation Results

**Quick Assessment**:

The simulation displays 4 key metrics:

| Metric | What It Means | Good Outcome | Concerning Outcome |
|--------|---------------|--------------|---------------------|
| **Incident Count** | Total incidents over simulation period | <10 | >30 |
| **Escalation Frequency** | % of incidents that are high-severity | <5% | >30% |
| **Average Severity** | Mean severity score (1-10 scale) | <3.0 | >7.0 |
| **Trend Analysis** | Direction of incident pattern | Decreasing | Sharply Increasing |

**Detailed Analysis**:

1. **Time Series Chart**: Shows severity of incidents over time
   - Look for patterns: stable, increasing, decreasing, cyclical
   - Identify crisis points (spikes in severity)

2. **Severity Distribution**: Bar chart of incident types
   - Most incidents should be low severity (1-4)
   - Few high-severity incidents (8-10) is acceptable
   - Many high-severity incidents indicates weak agreement

3. **High-Severity Events**: Red warning cards for incidents ≥8
   - Read the AI analysis for each event
   - Understand why escalation occurred
   - Identify which agreement terms failed

4. **Common Patterns**:
   - **Early Spike, Then Stable**: Agreement working as intended
   - **Gradual Escalation**: Parameters too lenient, enforcement weak
   - **Random Volatility**: Agreement doesn't address core issues
   - **Sustained High Tension**: Fundamental mismatch between agreement and reality

**Academic Grounding**:
- **Agent-Based Modeling**: Epstein & Axtell (1996) - Emergent phenomena from individual agent interactions
- **Conflict Escalation**: Bremer (1992) - Factors that increase likelihood of militarized disputes
- **Compliance**: Chayes & Chayes (1993) - Why nations follow agreements
- **Cooperation**: Axelrod (1984) - Evolution of cooperation in repeated interactions
- **Crisis Stability**: Leng (1983) - Realism and interstate crisis behavior

---

### Step 8: Review Strategic Context

Navigate to **Tab 3 (📊 Strategic Context Dashboard)** to see how players' strategic positions evolved during negotiation.

**Strategic Dimensions** (0-100 scale):

1. **Diplomatic Capital**: Ability to influence through diplomatic channels
   - **High (≥70)**: Player has strong regional relationships, can propose initiatives
   - **Moderate (40-69)**: Normal diplomatic standing
   - **Low (<40)**: Isolated, proposals treated skeptically

2. **International Legitimacy**: Support from international community
   - **High**: Player's actions seen as lawful and justified
   - **Moderate**: Mixed international perceptions
   - **Low**: Player seen as aggressor or treaty violator

3. **Domestic Support**: Public and government backing
   - **High**: Strong mandate to negotiate
   - **Moderate**: Normal political constraints
   - **Fragile (<35)**: Risk of government instability, limits flexibility

4. **Credibility**: Reputation for following through on commitments
   - **High (≥70)**: Promises trusted
   - **Moderate**: Normal skepticism
   - **Low (<40)**: Commitments doubted, higher verification requirements

**Escalation Risk Modifier**:
- Strategic position affects escalation risk in simulation
- High legitimacy (>70): **-15% escalation risk**
- Low legitimacy (<30): **+20% escalation risk**
- Fragile domestic support (<35): **+30% escalation risk**

**Facilitator Questions for Debrief**:
1. Which players gained strategic capital during negotiation?
2. Did any player sacrifice legitimacy to secure concessions?
3. How did domestic constraints affect player flexibility?
4. Which strategic actions were most effective?

---

### Step 9: Debrief Discussion

**Structured Debrief Format** (30-45 minutes):

**Part 1: Player Reflections (15 min)**
- Each player shares:
  - Their objectives and priorities
  - Key decisions and reasoning
  - What surprised them
  - What they learned

**Part 2: Outcome Analysis (15 min)**
- Review simulation results together
- Discuss cause-and-effect:
  - Which agreement terms were most effective?
  - Which parameters needed adjustment?
  - How did strategic actions influence outcomes?
- Compare to real-world cases (if applicable)

**Part 3: Strategic Lessons (15 min)**
- How did players use strategic actions?
- What sequencing strategies worked?
- How did strategic context shape behavior?
- Connection to academic theories:
  - Putnam's two-level games (domestic constraints)
  - Nye's soft power (diplomatic capital and legitimacy)
  - Fearon's credibility theory (audience costs)

**Facilitator Tips**:
- Encourage honest reflection (this is a learning environment)
- Draw connections to real-world cases
- Highlight both successes and failures
- Discuss alternative approaches
- Ask "what would you do differently next time?"

---

## Player Guide

### Your Role

As a player, you represent a **country or actor** in the South China Sea dispute. Your goals:
- Protect your country's interests (security, economy, sovereignty)
- Negotiate acceptable agreements with other players
- Use strategic actions to improve your negotiating position
- Balance domestic political constraints with international cooperation

### Available Roles

| Role | Description | Key Interests |
|------|-------------|---------------|
| **PH_GOV** | Philippines Government | Sovereignty over Scarborough Shoal, exclusive economic zone (EEZ) rights, US alliance |
| **PRC_MARITIME** | China Maritime Militia | Nine-dash line claims, freedom of navigation, resource access |
| **VN_CG** | Vietnam Coast Guard | Paracel & Spratly Islands claims, fishing rights, ASEAN solidarity |
| **MY_CG** | Malaysia Coast Guard | Southern Spratly claims, oil/gas exploration, regional stability |

**Role Assignment**:
- One player per role (no duplicates)
- Choose based on your learning interests
- Different roles have different strategic challenges

---

### Step 1: Join a Session

1. Get the **session code** from your facilitator (e.g., "REEF-2024")
2. Select **"👥 Join as Player"**
3. Enter the session code
4. Enter your name (e.g., "Ambassador Chen", "Minister Park")
5. Select your role from the dropdown
6. Click **"Join Session"**

**Success Message**: "Joined as [YOUR_ROLE]"

---

### Step 2: Prepare for Negotiation

Navigate through the tabs to familiarize yourself with the interface:

**Tab 1: 🎯 Role & Objectives**
- Read your role description
- Review your country's interests
- Study the strategy guide for your role

**Tab 4: 📊 Your Strategic Position**
- Check your starting metrics (all start at 50)
- Understand the escalation risk modifier
- Plan how to improve your strategic position

**Tab 5: ⚡ Strategic Actions**
- Browse available strategic actions
- Note prerequisites for each action
- Consider which actions align with your goals

**Tab 6: 📝 Strategy Notes**
- Take notes on your strategy
- Document red lines (non-negotiables)
- Write BATNA (Best Alternative to Negotiated Agreement)

**Example Notes Template**:
```
RED LINES (Non-Negotiables):
- Standoff distance must be ≥300m (security concern)
- Maximum 2 escorts (avoid provocation)

BATNA (Walk-Away Point):
- Bilateral negotiation with China
- Unilateral resupply operations
- International arbitration

KEY INTERESTS (Priority Order):
1. Sovereignty recognition (HIGH)
2. Freedom of navigation (HIGH)
3. Fishing access (MEDIUM)
4. Resource exploration (LOW)

CONCESSIONS I CAN MAKE:
- Reduce inspection requirements
- Increase update frequency to 12 hours
- Accept observer vessels instead of physical boarding

STRATEGIC ACTION PLAN:
- Round 1: Execute "Initiate Track II Dialogue" (build capital)
- Round 2: If needed, execute "Increase Transparency" (build credibility)
- Later: Consider "Host Regional Summit" if I have capital ≥30
```

**When Ready**:
- Click **"Mark as Ready"** button in Tab 1
- Wait for other players and facilitator

---

### Step 3: Review Proposals

When the facilitator submits a proposal, navigate to **Tab 2: 📋 Current Proposal**.

**How to Analyze a Proposal**:

1. **Read all parameters carefully**
2. **Evaluate against your interests**:
   - ✅ Does it meet your red lines?
   - ✅ Does it advance your key interests?
   - ❌ What are the risks or downsides?
   - 🤔 Is it better than your BATNA?

3. **Consider strategic implications**:
   - Will accepting cost you domestic support?
   - Will rejecting harm your international legitimacy?
   - What message does your response send to other players?

**Example Analysis** (Resupply Ship Incident, PH_GOV perspective):

```
Proposal Parameters:
- Standoff Distance: 300m
- Escorts: 2
- ROE: Defensive only
- Inspection: Observer vessels only
- Communication: Encrypted VHF
- Updates: Every 6 hours

My Evaluation:
✅ Standoff distance meets my 300m red line
✅ 2 escorts is acceptable (not excessive)
✅ Defensive ROE reduces escalation risk
⚠️ Observer vessels: Acceptable but prefer remote monitoring
✅ Encrypted VHF: Good for crisis communication
✅ 6-hour updates: Standard practice

Decision: ACCEPT with explanation
Reasoning: Meets all red lines, balances security and de-escalation
```

---

### Step 4: Submit Your Response

Navigate to **Tab 3: 💬 Submit Response**.

**Response Types**:

1. **Accept**: You approve the proposal as written
   - Use when: Proposal meets your interests and red lines
   - Effect: Shows willingness to cooperate, builds trust
   - Tip: Explain why you accept (not just "OK")

2. **Reject**: You oppose the proposal
   - Use when: Proposal violates red lines or harms key interests
   - Effect: Blocks agreement, requires new proposal
   - Tip: Explain specifically what needs to change

3. **Conditional**: You accept with reservations
   - Use when: Proposal is close but imperfect
   - Effect: Signals flexibility while noting concerns
   - Tip: Specify what would make it fully acceptable

**Writing Effective Explanations**:

**Good Explanation (Accept)**:
```
"I accept this proposal. The 300m standoff distance ensures our
personnel safety while allowing resupply operations. The defensive-only
ROE reduces escalation risk. The observer vessel inspection protocol
respects our sovereignty while providing transparency. This balances our
security concerns with the need for regional stability."
```

**Good Explanation (Reject)**:
```
"I must reject this proposal. The 150m standoff distance is too close
and risks accidental confrontation. Our military advisors deem anything
under 250m unacceptable from a safety perspective. Additionally, 4
escorts is excessive and seen as provocative by our public. If standoff
distance increases to 300m and escorts reduce to 2, I could accept."
```

**Good Explanation (Conditional)**:
```
"I conditionally accept this proposal. Most terms are acceptable, but I
have concerns about the 2-hour update frequency. Our coast guard lacks
capacity for such frequent reporting. If updates can be every 6 hours
instead, this proposal fully meets our needs. Otherwise, implementation
will be challenging."
```

**Poor Explanation**:
```
"OK" ❌
"This is fine" ❌
"I don't like it" ❌
"Reject" ❌
```

**Why Explanations Matter**:
- Helps facilitator understand your priorities
- Educates other players about your constraints
- Demonstrates good-faith negotiation
- Builds trust and credibility
- Makes the simulation realistic

---

### Step 5: Use Strategic Actions

Strategic actions allow you to improve your negotiating position. Navigate to **Tab 5: ⚡ Strategic Actions**.

**6 Available Actions**:

#### 1. Host Regional Summit
- **Type**: Multilateral Engagement
- **Prerequisites**: Diplomatic Capital ≥30
- **Cost**: Medium
- **Effects**:
  - Diplomatic Capital: -5 (spent organizing)
  - International Legitimacy: +10 (shows leadership)
  - Credibility: +5 (follows through on commitment)
- **When to Use**: Early in negotiation to establish yourself as constructive player
- **Academic Basis**: Keohane (1984) - Multilateral institutionalism creates focal points

#### 2. Propose Joint Development
- **Type**: Bilateral Cooperation
- **Prerequisites**: Domestic Support ≥40
- **Cost**: Medium-High
- **Effects**:
  - Domestic Support: -10 (seen as concession by hardliners)
  - International Legitimacy: +10 (peaceful resolution)
  - Economic Benefits: +15 (shared resource gains)
- **When to Use**: Mid-negotiation when trust is established
- **Academic Basis**: Fravel (2008) - Joint development as dispute management strategy

#### 3. Initiate Track II Dialogue
- **Type**: Informal Diplomacy
- **Prerequisites**: Diplomatic Capital ≥20
- **Cost**: Low
- **Effects**:
  - Diplomatic Capital: +10 (builds relationships)
  - Domestic Support: +5 (seen as active diplomacy)
- **When to Use**: Early and often - low risk, good returns
- **Academic Basis**: Diamond & McDonald (1996) - Multi-track diplomacy complements official channels

#### 4. Make Public Commitment
- **Type**: Public Diplomacy
- **Prerequisites**: Credibility ≥40
- **Cost**: Medium
- **Effects**:
  - Credibility: +10 (keeps promise)
  - Domestic Support: +5 (public approves clear stance)
  - Flexibility: -5 (harder to back down due to audience costs)
- **When to Use**: When ready to lock in position on key issue
- **Academic Basis**: Fearon (1994) - Audience costs make commitments credible

#### 5. Increase Transparency
- **Type**: Confidence-Building Measure
- **Prerequisites**: Credibility ≥30
- **Cost**: Low
- **Effects**:
  - Credibility: +10 (demonstrates openness)
  - International Legitimacy: +5 (reduces suspicion)
- **When to Use**: When trust is low, to signal good intentions
- **Academic Basis**: Osgood (1962) - GRIT (Graduated Reciprocation in Tension-reduction)

#### 6. Offer Economic Incentives
- **Type**: Issue Linkage
- **Prerequisites**: None
- **Cost**: High
- **Effects**:
  - Diplomatic Capital: +5 (generates goodwill)
  - Economic Cost: High (uses fiscal resources)
- **When to Use**: When stuck and need breakthrough
- **Academic Basis**: Tollison & Willett (1979) - Issue linkage expands negotiation space

---

### Strategic Action Sequencing

**Early Game (Setup Phase)**:
1. **Initiate Track II Dialogue** (builds capital, low risk)
2. **Increase Transparency** (builds trust, signals good faith)

**Mid Game (Negotiation Rounds 1-2)**:
1. **Host Regional Summit** (if you have capital ≥30)
2. **Propose Joint Development** (if domestic support ≥40 and appropriate)

**Late Game (Final Proposal)**:
1. **Make Public Commitment** (lock in agreement)
2. **Offer Economic Incentives** (if needed to close deal)

**Strategic Considerations**:

**Managing Domestic Politics** (Putnam 1988):
- Actions that cost domestic support reduce your flexibility
- Build support before making concessions
- Time controversial actions carefully

**Building Legitimacy** (Hurd 2007):
- Legitimacy unlocks more ambitious actions
- Legitimacy reduces escalation risk in simulation
- Prioritize legitimacy-building early

**Preserving Credibility** (Fearon 1994):
- Never make commitments you can't keep
- Public commitments lock you in (audience costs)
- Credibility enables future agreements

**Cost-Benefit Analysis**:
- Some actions have high costs (domestic support, capital)
- Weigh short-term costs against long-term benefits
- Don't overspend - save resources for critical moments

---

### Step 6: Wait for Simulation

Once all players accept a proposal:
- Facilitator runs the simulation
- Results appear in Tab 2
- Review outcomes and reflect on your strategy

**Questions for Self-Reflection**:
1. Did my responses align with my stated interests?
2. Did I use strategic actions effectively?
3. What trade-offs did I make?
4. How did my actions affect other players?
5. What would I do differently next time?

---

## Strategic Actions Guide

### Action Comparison Table

| Action | Prerequisites | Cost | Diplomatic Capital | Int'l Legitimacy | Domestic Support | Credibility | When to Use |
|--------|---------------|------|-------------------|-----------------|-----------------|-------------|-------------|
| **Host Regional Summit** | Capital ≥30 | Medium | -5 | +10 | 0 | +5 | Early - establish leadership |
| **Joint Development** | Support ≥40 | Medium-High | 0 | +10 | -10 | 0 | Mid - when trust exists |
| **Track II Dialogue** | Capital ≥20 | Low | +10 | 0 | +5 | 0 | Early/Often - low risk builder |
| **Public Commitment** | Credibility ≥40 | Medium | 0 | 0 | +5 | +10 | Late - lock in position |
| **Increase Transparency** | Credibility ≥30 | Low | 0 | +5 | 0 | +10 | Mid - build trust |
| **Economic Incentives** | None | High | +5 | 0 | 0 | 0 | Late - breakthrough tool |

### Action Synergies

**Legitimacy-Building Chain**:
1. Track II Dialogue (builds capital)
2. Host Regional Summit (uses capital, builds legitimacy)
3. Result: +10 capital, +10 legitimacy, +5 credibility

**Trust-Building Chain**:
1. Increase Transparency (builds credibility)
2. Make Public Commitment (uses credibility, locks in stance)
3. Result: +10 credibility total, clear position

**Cooperative Strategy**:
1. Track II Dialogue
2. Host Regional Summit
3. Propose Joint Development
4. Result: Establishes player as constructive leader

**Assertive Strategy**:
1. Increase Transparency (signal strength)
2. Make Public Commitment (draw line)
3. Result: Clear red lines communicated

### Common Mistakes

**Over-Spending Capital**:
- Executing too many high-cost actions
- Running out of resources for critical moments
- Solution: Pace yourself, prioritize

**Ignoring Domestic Constraints**:
- Making concessions without domestic support
- Taking actions that anger your public
- Solution: Build support before risky moves

**Premature Commitment**:
- Making public commitments too early
- Losing flexibility before final terms are clear
- Solution: Wait until late negotiation to lock in

**Neglecting Legitimacy**:
- Focusing only on capital and support
- Ignoring international perception
- Solution: Balance all four dimensions

---

## Interpreting Simulation Results

### The 4 Key Metrics

#### 1. Incident Count
**What it measures**: Total number of incidents during simulation period

**Interpretation**:
- **<10**: Ideal - Agreement is very effective
- **10-20**: Acceptable - Normal incident rate
- **20-30**: Concerning - Agreement has gaps
- **>30**: Failed - Agreement is ineffective

**Why it matters**: Fewer incidents = better agreement design

---

#### 2. Escalation Frequency
**What it measures**: Percentage of incidents that reach high severity (≥8)

**Interpretation**:
- **<5%**: Ideal - Incidents rarely escalate
- **5-15%**: Acceptable - Some escalation is normal
- **15-30%**: Concerning - Escalation is too common
- **>30%**: Failed - Most incidents escalate

**Why it matters**: Even with incidents, they should remain low-level

---

#### 3. Average Severity
**What it measures**: Mean severity score across all incidents (1-10 scale)

**Severity Scale**:
- **1-3**: Minor (verbal warnings, brief encounters)
- **4-6**: Moderate (weapon locks, close approaches)
- **7-9**: Serious (weapon discharge, physical contact)
- **10**: Extreme (casualties, open conflict)

**Interpretation**:
- **<3.0**: Ideal - Mostly minor incidents
- **3.0-5.0**: Acceptable - Some moderate incidents
- **5.0-7.0**: Concerning - Trending toward serious
- **>7.0**: Failed - Repeated serious incidents

**Why it matters**: Reflects how dangerous the environment is

---

#### 4. Trend Analysis
**What it measures**: Pattern of incidents over time

**Trend Types**:
- **Decreasing**: Agreement working, actors learning to cooperate
- **Stable**: Normal fluctuation around steady state
- **Increasing**: Agreement deteriorating, tension rising
- **Sharply Increasing**: Crisis trajectory, urgent revision needed

**Interpretation**:
- **Decreasing**: Best outcome - shows agreement effectiveness
- **Stable**: Good outcome - situation is managed
- **Increasing**: Concerning - agreement may be insufficient
- **Sharply Increasing**: Failed - urgent renegotiation needed

**Why it matters**: Direction matters as much as magnitude

---

### Visual Analysis

#### Time Series Chart
- **X-axis**: Simulation step (0-500)
- **Y-axis**: Incident severity (0-10)
- **Each dot**: One incident

**What to look for**:
- **Clusters**: Periods of intense activity
- **Spikes**: Crisis moments
- **Gaps**: Periods of calm
- **Trend line**: Overall direction

**Patterns**:
- **Early spike, then calm**: Agreement needed time to take effect (good)
- **Gradual rise**: Agreement is weakening (concerning)
- **Random scatter around low level**: Agreement is working (good)
- **Late spike**: External shock or agreement breakdown (needs analysis)

---

#### Severity Distribution
- **X-axis**: Severity buckets (1-2, 3-4, 5-6, 7-8, 9-10)
- **Y-axis**: Count of incidents

**Ideal Distribution**:
- Mostly 1-2 (minor incidents)
- Some 3-4 (moderate incidents)
- Few 5-6 (borderline serious)
- Very few 7-10 (serious/extreme)

**Concerning Distribution**:
- High counts in 7-8 or 9-10 buckets
- Even distribution across all buckets (no clear pattern)
- Bimodal (both very low and very high, but nothing in middle)

---

### High-Severity Event Analysis

For each incident with severity ≥8, the system provides:

**Incident Details**:
- Severity score
- Step number (when it occurred)
- Location (if relevant)

**AI Analysis** (Academic Framing):
- What happened (description)
- Why it escalated (causal factors)
- Which agreement terms failed
- Recommendations for revision

**Example High-Severity Event**:
```
Severity: 9 | Step: 234

Analysis:
This incident represents a near-miss collision between a resupply vessel
and a coast guard cutter. The 150m standoff distance proved insufficient
to prevent close encounters in rough seas. Per Schelling (1960), such
proximity increases the risk of accidental escalation due to limited
reaction time. The defensive-only ROE was activated, leading to weapon
locks, which further escalated tensions (audience costs, Fearon 1994).

Recommendation: Increase standoff distance to minimum 300m to provide
adequate buffer for maneuvering. Consider adding weather-dependent
protocols for rough sea conditions.
```

---

### Common Outcome Patterns

#### Pattern 1: Early Spike, Then Stable
**Description**: High incidents in first 100 steps, then decreases

**Interpretation**:
- Agreement needed time to establish norms
- Actors learned to cooperate through iteration (Axelrod 1984)
- Initial uncertainty about rules caused early incidents

**Assessment**: **Acceptable to Good**

**Debrief Questions**:
- What caused early incidents?
- How did actors adapt?
- Could clearer initial communication reduce early spike?

---

#### Pattern 2: Gradual Escalation
**Description**: Severity increases steadily over time

**Interpretation**:
- Agreement parameters too lenient
- Enforcement mechanisms inadequate
- Trust is eroding (Chayes & Chayes 1993)

**Assessment**: **Concerning**

**Debrief Questions**:
- Which parameters need tightening?
- Is enforcement credible?
- Are incentives for compliance sufficient?

---

#### Pattern 3: Random Volatility
**Description**: High variance, no clear trend

**Interpretation**:
- Agreement doesn't address underlying issues
- External factors dominate (not captured in parameters)
- Agents have high uncertainty about each other's intentions

**Assessment**: **Concerning**

**Debrief Questions**:
- What core issues did the agreement miss?
- Do parameters actually constrain behavior?
- Is communication adequate?

---

#### Pattern 4: Sustained High Tension
**Description**: Consistently high severity throughout

**Interpretation**:
- Fundamental mismatch between agreement and reality
- Agreement is too tight or unrealistic
- Actors cannot comply even if they want to

**Assessment**: **Failed**

**Debrief Questions**:
- Is the agreement feasible?
- Did negotiation miss key constraints?
- Should we try a completely different approach?

---

## Best Practices

### For Facilitators

**Scenario Selection**:
- Start with simpler scenarios (Resupply, Fishing)
- Progress to complex scenarios (Enforcement, Naval Exercise)
- Match scenario to learning objectives

**Proposal Strategy**:
- Don't aim for perfection on Round 1
- Use player feedback to iterate
- 2-3 rounds is typical for good agreement

**Time Management**:
- Setup: 10-15 minutes
- Negotiation: 30-45 minutes (2-3 rounds)
- Simulation: 5-10 minutes
- Debrief: 30-45 minutes

**Debrief Excellence**:
- Ask open-ended questions
- Connect to academic theories
- Encourage player reflection
- Discuss alternative approaches
- Link to real-world cases

---

### For Players

**Preparation**:
- Read your role carefully
- Take notes on red lines and BATNA
- Plan strategic action sequence
- Understand other players' likely interests

**During Negotiation**:
- Explain your reasoning clearly
- Be specific about what you need
- Signal flexibility where possible
- Build relationships through Track II

**Strategic Actions**:
- Start with low-cost actions (Track II, Transparency)
- Build resources before expensive actions
- Time high-impact actions strategically
- Balance all four dimensions

**Reflection**:
- Compare your plan to what actually happened
- Identify learning moments
- Consider alternative strategies
- Connect to theory

---

### For Educators

**Curricular Integration**:
- Use as capstone for negotiation unit
- Assign roles based on class size (2-8 players)
- Run multiple sessions to test different strategies
- Compare results across sessions

**Assessment Options**:
- Strategy memo (pre-negotiation)
- Reflection paper (post-negotiation)
- Peer evaluation of negotiation performance
- Comparative analysis of outcomes

**Extensions**:
- Have students design new scenarios
- Analyze real South China Sea incidents
- Research historical maritime disputes
- Compare simulation to actual negotiations

**Academic Connections**:
- International Relations: Realism vs Liberalism
- Game Theory: Prisoner's Dilemma, Chicken Game
- Negotiation Theory: BATNA, ZOPA, interests vs positions
- Conflict Resolution: Mediation, arbitration, diplomacy

---

## Troubleshooting

### Session Issues

**Problem**: Session code not working
- **Solution**: Verify code spelling (case-sensitive), check facilitator created session

**Problem**: Can't join - "Role already taken"
- **Solution**: Choose different role or ask facilitator to create new session

**Problem**: Players not showing as ready
- **Solution**: Each player must click "Mark as Ready" button, refresh facilitator view

---

### Proposal Issues

**Problem**: Can't submit proposal
- **Solution**: Fill out all required fields, check for validation errors

**Problem**: Proposal not appearing for players
- **Solution**: Players should refresh Tab 2, check session status is "negotiating"

**Problem**: Can't revise proposal
- **Solution**: Wait for all players to respond, or start new round

---

### Response Issues

**Problem**: Can't submit response
- **Solution**: Check if you already responded (can only respond once per proposal)

**Problem**: Response not showing for facilitator
- **Solution**: Facilitator should refresh Tab 1, check response count

**Problem**: Want to change response
- **Solution**: Not possible once submitted (simulates real-world commitment)

---

### Simulation Issues

**Problem**: Simulation button disabled
- **Solution**: Proposal must be "accepted" (all players accepted)

**Problem**: Simulation taking too long
- **Solution**: Normal is 5-10 seconds, wait patiently, refresh if >30 seconds

**Problem**: Results seem random
- **Solution**: Expected behavior (probabilistic model), run multiple times to see patterns

---

### Strategic Action Issues

**Problem**: Action grayed out/unavailable
- **Solution**: Check prerequisites (Tab 4 shows your current metrics)

**Problem**: Action executed but no effect
- **Solution**: Check Tab 4 to see updated metrics, may take page refresh

**Problem**: Can't execute any actions
- **Solution**: Some actions have no prerequisites (Economic Incentives always available)

---

## Additional Resources

### Academic References

**Core Negotiation Theory**:
- Fisher, R., & Ury, W. (1981). *Getting to Yes*. Penguin.
- Raiffa, H. (1982). *The Art and Science of Negotiation*. Harvard University Press.

**International Relations**:
- Nye, J. S. (2004). *Soft Power: The Means to Success in World Politics*. PublicAffairs.
- Putnam, R. D. (1988). Diplomacy and domestic politics: The logic of two-level games. *International Organization*, 42(3), 427-460.
- Fearon, J. D. (1994). Domestic political audiences and the escalation of international disputes. *American Political Science Review*, 88(3), 577-592.
- Hurd, I. (2007). *After Anarchy: Legitimacy and Power in the United Nations Security Council*. Princeton University Press.

**Conflict Resolution**:
- Schelling, T. C. (1960). *The Strategy of Conflict*. Harvard University Press.
- Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books.
- Leng, R. J. (1983). When will they ever learn? Coercive bargaining in recurrent crises. *Journal of Conflict Resolution*, 27(3), 379-419.

**Simulation & Modeling**:
- Epstein, J. M., & Axtell, R. (1996). *Growing Artificial Societies: Social Science from the Bottom Up*. MIT Press.
- Bremer, S. A. (1992). Dangerous dyads: Conditions affecting the likelihood of interstate war. *Journal of Conflict Resolution*, 36(2), 309-341.

**Compliance & Institutions**:
- Chayes, A., & Chayes, A. H. (1993). On compliance. *International Organization*, 47(2), 175-205.
- Keohane, R. O. (1984). *After Hegemony: Cooperation and Discord in the World Political Economy*. Princeton University Press.

**Regional Strategies**:
- Fravel, M. T. (2008). *Strong Borders, Secure Nation: Cooperation and Conflict in China's Territorial Disputes*. Princeton University Press.
- Diamond, L., & McDonald, J. (1996). *Multi-Track Diplomacy: A Systems Approach to Peace*. Kumarian Press.

**Confidence-Building**:
- Osgood, C. E. (1962). *An Alternative to War or Surrender*. University of Illinois Press.
- Tollison, R. D., & Willett, T. D. (1979). An economic theory of mutually advantageous issue linkages in international negotiations. *International Organization*, 33(4), 425-449.

---

### Related Documentation

- **MULTIPLAYER_TESTING_GUIDE.md**: Comprehensive testing procedures
- **MULTIPLAYER_FEATURE_IMPLEMENTATION_PLAN.md**: Technical implementation details
- **SCENARIO_DESIGN_GUIDE.md**: Creating custom scenarios (if available)
- **API_DOCUMENTATION.md**: Programmatic access (if available)

---

**Last Updated**: 2025-01-09
**Version**: 1.0 (Phases 1-4 Complete)
**Maintainer**: SCS Mediator SDK Team
**Support**: For issues or questions, see MULTIPLAYER_TESTING_GUIDE.md troubleshooting section
