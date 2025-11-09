# Multiplayer App Feature Implementation Plan
**Porting Features from enhanced_multi_view.py to multiplayer_app.py**

## Overview
This document provides detailed implementation steps for porting all remaining single-player features to the multiplayer app. Each phase includes:
- Exact code patterns to port
- Line number references from source
- Resources tab updates with citations
- Testing requirements

---

## ✅ PHASE 1: DETAILED SIMULATION RESULTS (COMPLETED)
**Status**: Implemented on port 8606
**Files Modified**: `multiplayer_app.py` lines 957-1265
**Features Added**:
- 4 metrics with delta indicators (Total Incidents, Avg Severity, Max Severity, Trend)
- Comprehensive explanation expander (expanded by default)
- Visual analytics (matplotlib charts)
- High-severity event highlighting
- Pattern recognition guide
- Academic citations: Epstein & Axtell (1996), Bremer (2000), Chayes & Chayes (1993), Axelrod (1984), Leng (1983)

---

## 🔄 PHASE 2: STRATEGIC CONTEXT TRACKING SYSTEM
**Priority**: HIGH | **Complexity**: MEDIUM

### Overview
Add 4-dimensional soft power metrics that complement hard parameters:
1. **Diplomatic Capital** (0-100): Ability to influence through diplomatic channels
2. **International Legitimacy** (0-100): Support from international community
3. **Domestic Support** (0-100): Public and government backing
4. **Credibility** (0-100): Reputation for following through

### Source Reference
- **Module**: `src/scs_mediator_sdk/dynamics/strategic_context.py` (lines 1-298)
- **Single-player UI**: `enhanced_multi_view.py` lines 572-575, 2618-2682

### Implementation Steps

#### 2.1 Add Import (multiplayer_app.py line 30)
```python
from scs_mediator_sdk.dynamics.strategic_context import StrategicContext
```

#### 2.2 Initialize Strategic Contexts in Session Manager
**File**: `src/scs_mediator_sdk/multiplayer/session_manager.py`
**Add to Session dataclass** (after line 72):
```python
    strategic_contexts: Dict[str, any] = field(default_factory=dict)  # player_id -> StrategicContext
```

**Add initialization method** (after line 113):
```python
    def initialize_strategic_contexts(self, session_id: str):
        """Initialize strategic contexts for all players"""
        session = self.get_session(session_id)
        if not session:
            return False

        from scs_mediator_sdk.dynamics.strategic_context import StrategicContext

        for player_id, player in session.players.items():
            session.strategic_contexts[player_id] = StrategicContext()

        session.updated_at = datetime.now()
        return True
```

#### 2.3 Add Strategic Context Display to Facilitator View
**File**: `multiplayer_app.py`
**Location**: After escalation assessment tab, before Peace Tools tab (around line 850)

```python
    with tabs[3]:  # Strategic Context tab
        st.markdown("### 📊 Strategic Context Dashboard")
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; border-left: 5px solid #4682b4; margin-bottom: 20px;">
            <p style="color: #000; margin: 0;"><strong>Soft Power & Strategic Positioning</strong></p>
            <p style="color: #1a1a1a; margin: 10px 0 0 0; font-size: 14px;">
                Beyond negotiation parameters, strategic dimensions affect escalation risk and agreement sustainability.
                These metrics are tracked per player and influence simulation outcomes.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Initialize if not yet done
        if not session.strategic_contexts:
            session_mgr.get_session(session.session_id).strategic_contexts = {}
            from scs_mediator_sdk.dynamics.strategic_context import StrategicContext
            for player_id in session.players.keys():
                session.strategic_contexts[player_id] = StrategicContext()

        # Player selector
        selected_stakeholder = st.selectbox(
            "Select Player to View",
            options=list(session.strategic_contexts.keys()),
            format_func=lambda pid: f"{session.players[pid].role} ({session.players[pid].user_name})"
        )

        if selected_stakeholder:
            stakeholder_ctx = session.strategic_contexts[selected_stakeholder]
            summary = stakeholder_ctx.get_summary()

            # 4-metric dashboard
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                val = summary['diplomatic_capital']['value']
                status = summary['diplomatic_capital']['status']
                color = '#2ca02c' if val >= 60 else '#ff7f0e' if val >= 40 else '#d62728'
                st.markdown(f"""
                <div style="background-color: {color}15; padding: 15px; border-radius: 8px; border-left: 5px solid {color};">
                    <p style="color: #3a3a3a; font-size: 12px; margin: 0;">DIPLOMATIC CAPITAL</p>
                    <h2 style="color: {color}; margin: 5px 0;">{val:.0f}</h2>
                    <p style="color: #3a3a3a; font-size: 11px; margin: 0;">{status}</p>
                </div>
                """, unsafe_allow_html=True)
                st.caption(summary['diplomatic_capital']['description'])

            with col2:
                val = summary['international_legitimacy']['value']
                status = summary['international_legitimacy']['status']
                color = '#2ca02c' if val >= 60 else '#ff7f0e' if val >= 40 else '#d62728'
                st.markdown(f"""
                <div style="background-color: {color}15; padding: 15px; border-radius: 8px; border-left: 5px solid {color};">
                    <p style="color: #3a3a3a; font-size: 12px; margin: 0;">INT'L LEGITIMACY</p>
                    <h2 style="color: {color}; margin: 5px 0;">{val:.0f}</h2>
                    <p style="color: #3a3a3a; font-size: 11px; margin: 0;">{status}</p>
                </div>
                """, unsafe_allow_html=True)
                st.caption(summary['international_legitimacy']['description'])

            with col3:
                val = summary['domestic_support']['value']
                status = summary['domestic_support']['status']
                color = '#2ca02c' if val >= 60 else '#ff7f0e' if val >= 40 else '#d62728'
                st.markdown(f"""
                <div style="background-color: {color}15; padding: 15px; border-radius: 8px; border-left: 5px solid {color};">
                    <p style="color: #3a3a3a; font-size: 12px; margin: 0;">DOMESTIC SUPPORT</p>
                    <h2 style="color: {color}; margin: 5px 0;">{val:.0f}</h2>
                    <p style="color: #3a3a3a; font-size: 11px; margin: 0;">{status}</p>
                </div>
                """, unsafe_allow_html=True)
                st.caption(summary['domestic_support']['description'])

            with col4:
                val = summary['credibility']['value']
                status = summary['credibility']['status']
                color = '#2ca02c' if val >= 60 else '#ff7f0e' if val >= 40 else '#d62728'
                st.markdown(f"""
                <div style="background-color: {color}15; padding: 15px; border-radius: 8px; border-left: 5px solid {color};">
                    <p style="color: #3a3a3a; font-size: 12px; margin: 0;">CREDIBILITY</p>
                    <h2 style="color: {color}; margin: 5px 0;">{val:.0f}</h2>
                    <p style="color: #3a3a3a; font-size: 11px; margin: 0;">{status}</p>
                </div>
                """, unsafe_allow_html=True)
                st.caption(summary['credibility']['description'])

            # Escalation modifier
            modifier = summary['escalation_modifier']
            modifier_pct = (1 - modifier) * 100 if modifier < 1 else (modifier - 1) * 100
            modifier_direction = "reduces" if modifier < 1 else "increases"
            st.info(f"This player's strategic position {modifier_direction} escalation risk by {abs(modifier_pct):.1f}% (modifier: {modifier:.2f}x)")

            # Show all players comparison
            st.markdown("---")
            st.markdown("#### All Players Comparison")

            comparison_data = []
            for pid, ctx in session.strategic_contexts.items():
                summary = ctx.get_summary()
                comparison_data.append({
                    "Player": f"{session.players[pid].role} ({session.players[pid].user_name})",
                    "Diplomatic Capital": summary['diplomatic_capital']['value'],
                    "Int'l Legitimacy": summary['international_legitimacy']['value'],
                    "Domestic Support": summary['domestic_support']['value'],
                    "Credibility": summary['credibility']['value'],
                    "Escalation Modifier": f"{summary['escalation_modifier']:.2f}x"
                })

            import pandas as pd
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)
```

#### 2.4 Add Strategic Context to Player View
**File**: `multiplayer_app.py`
**Location**: In player view, add as new tab (around line 1100)

```python
    with tabs[3]:  # Strategic Position tab (for players)
        st.markdown("### Your Strategic Position")
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; border-left: 5px solid #4682b4; margin-bottom: 20px;">
            <p style="color: #000; margin: 0;"><strong>Strategic Leverage & Soft Power</strong></p>
            <p style="color: #1a1a1a; margin: 10px 0 0 0; font-size: 14px;">
                Beyond parameters, strategic actions affect your diplomatic capital, international legitimacy,
                domestic support, and credibility. These dimensions influence escalation risk and outcome sustainability.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Get strategic context for this player
        ctx = session.strategic_contexts.get(player_id, None)
        if not ctx:
            from scs_mediator_sdk.dynamics.strategic_context import StrategicContext
            ctx = StrategicContext()
            session.strategic_contexts[player_id] = ctx

        summary = ctx.get_summary()

        # 4-metric dashboard (same as facilitator view)
        col1, col2, col3, col4 = st.columns(4)
        # ... [same dashboard code as facilitator view]
```

#### 2.5 Update Resources Tab
**File**: `multiplayer_app.py`
**Location**: In `render_resources_tab()` function (around line 680)

Add new section before existing sections:

```python
    with st.expander("📊 Strategic Dimensions & Soft Power", expanded=False):
        st.markdown("""
        ### Understanding Strategic Context

        Beyond numerical parameters, four strategic dimensions affect negotiation outcomes and escalation risk:

        #### 1. Diplomatic Capital (0-100)
        **Definition**: Ability to influence outcomes through diplomatic channels, trust, and relationships.

        **What it Measures**:
        - Accumulated goodwill from past cooperation
        - Network of diplomatic relationships
        - Credibility in multilateral forums
        - Ability to convene summits and coordinate responses

        **How it Changes**:
        - **Increases**: Hosting regional summits, facilitating dialogue, honoring commitments
        - **Decreases**: Undertaking high-stakes initiatives, being seen as aggressive

        **Impact on Outcomes**:
        - High diplomatic capital (>70) reduces escalation risk by 15%
        - Enables access to high-cost strategic actions (e.g., convening summits)
        - Makes proposals more acceptable to other parties

        **Academic Basis**: Nye, J. (2004). "Soft Power: The Means to Success in World Politics"

        ---

        #### 2. International Legitimacy (0-100)
        **Definition**: Support and recognition from the international community, allies, and multilateral institutions.

        **What it Measures**:
        - Alignment with international law (UNCLOS, ICJ rulings)
        - Support from major powers (US, EU, ASEAN)
        - Endorsement from multilateral bodies (UN, IMF)
        - International media perception

        **How it Changes**:
        - **Increases**: Aligning with international law, gaining ally endorsements, peaceful initiatives
        - **Decreases**: Unilateral actions, defying international norms

        **Impact on Outcomes**:
        - High legitimacy (>70) reduces escalation risk by 15%
        - Low legitimacy (<30) increases risk by 20%
        - Affects third-party willingness to mediate or provide support

        **Academic Basis**: Hurd, I. (2007). "After Anarchy: Legitimacy and Power in the UN Security Council"

        ---

        #### 3. Domestic Support (0-100)
        **Definition**: Public and government backing for the negotiation strategy.

        **What it Measures**:
        - Public opinion polls on government's handling of dispute
        - Legislative support for agreements
        - Media sentiment (nationalist vs. pragmatic)
        - Elite consensus on strategy

        **How it Changes**:
        - **Increases**: Low-risk initiatives, economic benefits, nationalist rhetoric
        - **Decreases**: Perceived concessions on sovereignty, appearing weak

        **Impact on Outcomes**:
        - Fragile support (<35) increases escalation risk by 30% (Fearon's audience costs)
        - Low support constrains negotiating flexibility (smaller win-set)
        - Affects ability to ratify agreements

        **Academic Basis**:
        - Putnam, R. (1988). "Diplomacy and Domestic Politics: The Logic of Two-Level Games"
        - Fearon, J. (1994). "Domestic Political Audiences and the Escalation of International Disputes"

        ---

        #### 4. Credibility (0-100)
        **Definition**: Reputation for following through on commitments and threats.

        **What it Measures**:
        - Track record of honoring past agreements
        - Consistency between rhetoric and actions
        - Resolve demonstrated in past crises
        - Reputation for reliability

        **How it Changes**:
        - **Increases**: Honoring commitments, transparency initiatives, consistent messaging
        - **Decreases**: Public commitments without follow-through, empty threats

        **Impact on Outcomes**:
        - Low credibility (<40) increases escalation risk by 25% (opponents don't believe threats)
        - High credibility (>75) reduces risk by 10% (commitments taken seriously)
        - Affects deterrence effectiveness

        **Academic Basis**: Schelling, T. (1966). "Arms and Influence" - commitment and credibility theory

        ---

        ### How Strategic Dimensions Affect Escalation Risk

        The simulation calculates an **escalation modifier** based on strategic context:

        ```
        Base Risk × Escalation Modifier = Actual Risk
        ```

        **Escalation Modifier Formula**:
        - Start at 1.0 (neutral)
        - High Int'l Legitimacy (>70): ×0.85 (-15% risk)
        - Low Int'l Legitimacy (<30): ×1.20 (+20% risk)
        - Low Credibility (<40): ×1.25 (+25% risk)
        - High Credibility (>75): ×0.90 (-10% risk)
        - Fragile Domestic Support (<35): ×1.30 (+30% risk) [Putnam's constraint]
        - High Diplomatic Capital (>70): ×0.85 (-15% risk)

        **Example**: A player with high legitimacy (75), low credibility (35), and fragile domestic support (30) would have:
        ```
        Modifier = 0.85 (legitimacy) × 1.25 (credibility) × 1.30 (domestic) = 1.38x
        ```
        This means their escalation risk is 38% higher than the base case.

        ---

        ### Strategic Actions vs. Parameters

        **Parameters** (standoff distance, escort count, etc.) are the **hard terms** of the agreement.

        **Strategic Dimensions** are the **soft power context** that determines:
        1. Whether parameters will be honored
        2. How much escalation risk the agreement carries
        3. Whether domestic actors will ratify the deal
        4. How the international community will respond

        **Example**: Two identical agreements with the same parameters can have vastly different outcomes:
        - **High Strategic Position**: Agreement honored, low escalation, successful implementation
        - **Weak Strategic Position**: Agreement violated, high escalation, domestic rejection

        ---

        ### Key Academic References

        1. **Nye, J. (2004)**. "Soft Power: The Means to Success in World Politics." PublicAffairs.
           - Foundational work on soft power dimensions

        2. **Putnam, R. (1988)**. "Diplomacy and Domestic Politics: The Logic of Two-Level Games." *International Organization* 42(3): 427-460.
           - How domestic constraints affect international bargaining

        3. **Fearon, J. (1994)**. "Domestic Political Audiences and the Escalation of International Disputes." *American Political Science Review* 88(3): 577-592.
           - Audience costs and domestic support dynamics

        4. **Schelling, T. (1966)**. "Arms and Influence." Yale University Press.
           - Credibility and commitment in bargaining

        5. **Hurd, I. (2007)**. "After Anarchy: Legitimacy and Power in the UN Security Council." Princeton University Press.
           - International legitimacy in conflict resolution
        """)
```

### Testing Requirements
- [ ] Strategic contexts initialize correctly when session starts
- [ ] All 4 metrics display correctly in facilitator view
- [ ] Per-player metrics display correctly in player view
- [ ] Escalation modifier calculates correctly
- [ ] Comparison table shows all players
- [ ] Resources tab displays documentation correctly

---

## 📋 PHASE 3: STRATEGIC ACTIONS SYSTEM
**Priority**: HIGH | **Complexity**: MEDIUM

### Overview
Add library of strategic moves that affect both parameters and strategic dimensions. Players can execute actions to improve their position.

### Source Reference
- **Module**: `strategic_context.py` lines 160-298 (STRATEGIC_ACTIONS_LIBRARY)
- **Single-player UI**: `enhanced_multi_view.py` lines 2686-2737

### Available Strategic Actions
1. **Convene Regional Summit**: Organize ASEAN/APEC summit (+diplomacy, +legitimacy, -capital)
2. **Propose Joint Development Zone**: Shelve sovereignty disputes for co-development
3. **Launch Track II Dialogue**: Unofficial academic/business channels
4. **Make Public Commitment to Peace**: High-profile peace pledge
5. **Increase Military Transparency**: Share naval schedules proactively
6. **Offer Economic Incentives**: Trade benefits for cooperation

### Implementation: Add to Player View Tab 4
(See detailed code in single-player lines 2686-2737)

### Resources Tab Update
Add "Strategic Levers & Diplomatic Moves" section with academic citations.

---

## 📑 PHASE 4: ENHANCED PLAYER VIEW (6-TAB INTERFACE)
**Priority**: MEDIUM | **Complexity**: LOW

### Current Player View
- Tab 1: Role & Objectives
- Tab 2: Current Proposal
- Tab 3: Submit Response

### Enhanced Player View
- Tab 1: Role & Objectives (keep as-is)
- Tab 2: Current Proposal (keep as-is)
- Tab 3: Submit Response (keep as-is)
- **Tab 4: Your Strategic Position** (NEW - from Phase 2)
- **Tab 5: Available Strategic Actions** (NEW - from Phase 3)
- **Tab 6: Strategy Notes** (NEW - text area for player notes)

Simple tab restructuring, leveraging Phase 2 & 3 implementations.

---

## 🕊️ PHASE 5: PEACE MEDIATION TOOLS
**Priority**: HIGH | **Complexity**: HIGH

### Overview
Add 5-tab section to facilitator view with academic peace mediation tools:

### 5.1 CBM Recommendations Tab
**Source**: `enhanced_multi_view.py` lines 1922-1998
**Module**: `src/scs_mediator_sdk/peacebuilding/cbm_library.py`

**Features**:
- CBM Library with 15+ confidence-building measures
- Sequenced recommendations based on trust level and escalation
- Categories: Communication, Transparency, Cooperation, Verification, Joint Activities
- Implementation steps for each CBM

**Academic Basis**: Osgood, C. (1962). "GRIT: Graduated Reciprocation in Tension-reduction"

### 5.2 Domestic Politics Tab
**Source**: `enhanced_multi_view.py` lines 1999-2135
**Module**: `src/scs_mediator_sdk/politics/domestic_constraints.py`

**Features**:
- Win-set analysis (Putnam's two-level game theory)
- Domestic deal-breakers identification
- Proposal acceptability testing
- Ratification probability calculation
- Compensation suggestions

**Academic Basis**: Putnam, R. (1988). "Diplomacy and Domestic Politics"

### 5.3 Spoiler Analysis Tab
**Source**: `enhanced_multi_view.py` lines 2136-2180
**Module**: `src/scs_mediator_sdk/peacebuilding/spoiler_management.py`

**Features**:
- Identify potential spoilers (hardliners, nationalists, military interests)
- Spoiler capability assessment (high/medium/low)
- Spoiler position (inside/outside process)
- Mitigation strategies

**Academic Basis**: Stedman, S. J. (1997). "Spoiler Problems in Peace Processes"

### 5.4 Multi-Track Diplomacy Tab
**Source**: `enhanced_multi_view.py` lines 2181-2250
**Module**: `src/scs_mediator_sdk/diplomacy/multi_track.py`

**Features**:
- 9-track diplomatic framework
- Track 1 (official government), Track 2 (unofficial), Track 3 (business), etc.
- Coordination recommendations

**Academic Basis**: Diamond, L. & McDonald, J. (1996). "Multi-Track Diplomacy"

### 5.5 Peace Context Summary Tab
**Source**: `enhanced_multi_view.py` lines 2251-2300

**Features**:
- Overall peace process health indicators
- Risk dashboard
- Timeline projections

### Resources Tab Updates
Add 5 new sections corresponding to each peace tool with full academic citations.

---

## 🤖 PHASE 6: AI GUIDE SYSTEM
**Priority**: MEDIUM | **Complexity**: MEDIUM

### Overview
Add persistent AI chat guide that provides context-aware assistance to facilitators and players.

### Source Reference
- **Module**: `src/scs_mediator_sdk/ai_guide.py`
- **Single-player UI**: `enhanced_multi_view.py` lines 2450-2550

### Features
- Separate guides for facilitator vs. player roles
- Context-aware (knows scenario, current proposal, player positions)
- Persistent chat history
- Academic grounding (cites relevant literature)

### Implementation Notes
- Requires ANTHROPIC_API_KEY
- Falls back to static guidance if key not available
- Chat history stored in session state

### Resources Tab Update
Add "Using AI Guidance Effectively" section.

---

## 🎯 IMPLEMENTATION ORDER

### Recommended Sequence
1. ✅ **Phase 1**: Detailed Simulation Results (COMPLETED)
2. 🔄 **Phase 2**: Strategic Context Tracking (IN PROGRESS)
3. **Phase 3**: Strategic Actions System
4. **Phase 4**: Enhanced Player View (depends on 2 & 3)
5. **Phase 5**: Peace Mediation Tools
6. **Phase 6**: AI Guide System

### Why This Order?
- Phase 2 provides foundation for Phase 3 (actions affect strategic context)
- Phase 4 is trivial once Phases 2 & 3 are done
- Phase 5 is independent and can be done in parallel
- Phase 6 is optional enhancement

---

## 📊 TESTING CHECKLIST

### Phase 2: Strategic Context
- [ ] Strategic contexts initialize when session starts
- [ ] 4 metrics display correctly (Diplomatic Capital, Legitimacy, Support, Credibility)
- [ ] Escalation modifier calculates correctly
- [ ] Facilitator can view all players' strategic positions
- [ ] Players can see their own strategic position
- [ ] Resources tab includes strategic dimensions documentation

### Phase 3: Strategic Actions
- [ ] Action library loads correctly
- [ ] Available actions filter based on prerequisites
- [ ] Executing action updates strategic context
- [ ] Parameter effects apply correctly
- [ ] Academic citations display for each action
- [ ] Resources tab includes strategic levers documentation

### Phase 4: Enhanced Player View
- [ ] 6 tabs display correctly
- [ ] Tab 4 shows strategic position
- [ ] Tab 5 shows available actions
- [ ] Tab 6 allows strategy notes

### Phase 5: Peace Tools
- [ ] CBM recommendations generate correctly
- [ ] Domestic politics analysis runs
- [ ] Spoiler threats identified
- [ ] Multi-track coordination displays
- [ ] Resources tab includes all 5 peace tool frameworks

### Phase 6: AI Guide
- [ ] Guide initializes with correct role context
- [ ] Chat history persists across interactions
- [ ] Fallback guidance works without API key
- [ ] Resources tab includes AI guidance tips

---

## 📚 KEY ACADEMIC REFERENCES

### Strategic Context & Soft Power
1. Nye, J. (2004). "Soft Power: The Means to Success in World Politics"
2. Schelling, T. (1966). "Arms and Influence"

### Domestic Politics & Ratification
3. Putnam, R. (1988). "Diplomacy and Domestic Politics: The Logic of Two-Level Games"
4. Fearon, J. (1994). "Domestic Political Audiences and the Escalation of International Disputes"

### Peace Mediation
5. Osgood, C. (1962). "An Alternative to War or Surrender" (GRIT)
6. Stedman, S. J. (1997). "Spoiler Problems in Peace Processes"
7. Diamond, L. & McDonald, J. (1996). "Multi-Track Diplomacy"

### Escalation & Crisis Management
8. Kahn, H. (1965). "On Escalation: Metaphors and Scenarios"
9. Jervis, R. (1978). "Cooperation Under the Security Dilemma"

### Maritime Disputes
10. Fravel, M. T. (2008). "Strong Borders, Secure Nation: Cooperation and Conflict in China's Territorial Disputes"

---

## 🚀 NEXT STEPS

1. **Immediate**: Begin Phase 2 implementation (Strategic Context Tracking)
2. **Documentation**: Update Resources tab as each phase completes
3. **Testing**: Validate each phase before moving to next
4. **Port Number**: Use 8607 for next deployment

---

**Document Version**: 1.0
**Created**: 2025-11-09
**Purpose**: Detailed implementation roadmap for porting single-player features to multiplayer app
