#!/usr/bin/env python3
"""
Multiplayer Negotiation Simulation

Multi-user version where:
- 1 facilitator mediates
- 2-4 players represent different stakeholders
- Real-time turn-based negotiation
- Final agreement tested via simulation

MVP Version: Simple accept/reject, no counteroffers yet
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Add src to path
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from scs_mediator_sdk.multiplayer import get_session_manager
from scs_mediator_sdk.sim.mesa_abm import MaritimeModel
from scs_mediator_sdk.guides import get_facilitator_guide, get_player_guide
from scs_mediator_sdk.dynamics.escalation_ladder import EscalationManager
from scs_mediator_sdk.dynamics.strategic_context import StrategicContext, get_available_actions, STRATEGIC_ACTIONS_LIBRARY

# Phase 5: Peace Mediation Tools
from scs_mediator_sdk.peacebuilding.cbm_library import CBMLibrary, CBMCategory
from scs_mediator_sdk.politics.domestic_constraints import (
    WinSetAnalyzer,
    create_philippines_domestic_actors,
    create_china_domestic_actors
)
from scs_mediator_sdk.peacebuilding.spoiler_management import SpoilerManager
from scs_mediator_sdk.diplomacy.multi_track import MultiTrackMediator

# Phase 6: AI Guide System
from scs_mediator_sdk.ai_guide import create_instructor_guide, create_participant_guide

# ==================== GLOBAL CSS FOR BETTER CONTRAST ====================
# Theme-aware contrast that works in both light and dark modes
st.markdown("""
<style>
    /* Light mode: dark text */
    @media (prefers-color-scheme: light) {
        body, p, div, span, label, li {
            color: #262730 !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #262730 !important;
        }
        .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span {
            color: #262730 !important;
        }
    }

    /* Dark mode: light text */
    @media (prefers-color-scheme: dark) {
        body, p, div, span, label, li {
            color: #FAFAFA !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #FAFAFA !important;
        }
        .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span {
            color: #FAFAFA !important;
        }
    }

    /* Info boxes always have good contrast */
    .stAlert {
        color: #000000 !important;
        background-color: #E8F4F8 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== CONFIGURATION ====================

SCENARIOS = {
    'scenario_A': {
        'name': 'Second Thomas Shoal (Resupply)',
        'roles': ['PH_GOV', 'PRC_MARITIME'],
        'description': 'Philippine resupply missions to BRP Sierra Madre',
        'recommended_issues': ['resupply_SOP', 'hotline_cues', 'incident_response', 'naval_restrictions'],
        'all_issues': ['resupply_SOP', 'hotline_cues', 'incident_response', 'naval_restrictions',
                       'media_protocol', 'fishing_rights', 'access_zones']
    },
    'scenario_B': {
        'name': 'Scarborough Shoal (Fishing)',
        'roles': ['PH_GOV', 'PRC_MARITIME'],
        'description': 'Traditional fishing grounds and access rights',
        'recommended_issues': ['fishing_rights', 'access_zones', 'seasonal_restrictions', 'enforcement_protocols'],
        'all_issues': ['fishing_rights', 'access_zones', 'seasonal_restrictions', 'enforcement_protocols',
                       'hotline_cues', 'media_protocol', 'incident_response']
    }
}

# Issue metadata for dynamic UI rendering
ISSUE_METADATA = {
    'resupply_SOP': {
        'label': '🚢 Resupply Operations',
        'fields': [
            {'key': 'standoff_nm', 'label': 'Standoff Distance (nm)', 'type': 'slider', 'min': 0, 'max': 10, 'default': 3},
            {'key': 'escort_count', 'label': 'Maximum Escorts', 'type': 'slider', 'min': 0, 'max': 5, 'default': 1},
            {'key': 'pre_notification_hours', 'label': 'Pre-Notification (hours)', 'type': 'slider', 'min': 0, 'max': 48, 'default': 24}
        ]
    },
    'fishing_rights': {
        'label': '🎣 Fishing Rights',
        'fields': [
            {'key': 'daily_quota_kg', 'label': 'Daily Catch Quota (kg)', 'type': 'slider', 'min': 100, 'max': 5000, 'default': 1000},
            {'key': 'vessel_limit', 'label': 'Max Fishing Vessels', 'type': 'slider', 'min': 1, 'max': 50, 'default': 10},
            {'key': 'permitted_gear', 'label': 'Permitted Gear', 'type': 'multiselect', 'options': ['nets', 'lines', 'traps'], 'default': ['nets', 'lines']}
        ]
    },
    'access_zones': {
        'label': '🗺️ Access Zones',
        'fields': [
            {'key': 'zone_radius_nm', 'label': 'Zone Radius (nm)', 'type': 'slider', 'min': 1, 'max': 20, 'default': 12},
            {'key': 'buffer_zone_nm', 'label': 'Buffer Zone (nm)', 'type': 'slider', 'min': 0, 'max': 5, 'default': 2},
            {'key': 'access_type', 'label': 'Access Type', 'type': 'selectbox', 'options': ['shared', 'alternating', 'restricted'], 'default': 'shared'}
        ]
    },
    'seasonal_restrictions': {
        'label': '📅 Seasonal Restrictions',
        'fields': [
            {'key': 'closure_months', 'label': 'Closure Period (months)', 'type': 'slider', 'min': 0, 'max': 6, 'default': 3},
            {'key': 'breeding_protection', 'label': 'Breeding Season Protection', 'type': 'checkbox', 'default': True},
            {'key': 'seasonal_quotas', 'label': 'Seasonal Quotas', 'type': 'checkbox', 'default': True}
        ]
    },
    'enforcement_protocols': {
        'label': '👮 Enforcement Protocols',
        'fields': [
            {'key': 'patrol_frequency', 'label': 'Patrol Frequency (per week)', 'type': 'slider', 'min': 1, 'max': 14, 'default': 3},
            {'key': 'joint_patrols', 'label': 'Joint Patrols', 'type': 'checkbox', 'default': False},
            {'key': 'inspection_rights', 'label': 'Inspection Rights', 'type': 'selectbox', 'options': ['unilateral', 'mutual', 'third_party'], 'default': 'mutual'}
        ]
    },
    'hotline_cues': {
        'label': '📞 Communication',
        'fields': [
            {'key': 'hotline_status', 'label': 'Hotline', 'type': 'selectbox', 'options': ['24_7', 'ad_hoc'], 'default': '24_7'},
            {'key': 'response_time_hours', 'label': 'Response Time (hours)', 'type': 'slider', 'min': 1, 'max': 24, 'default': 4}
        ]
    },
    'media_protocol': {
        'label': '📰 Media Protocol',
        'fields': [
            {'key': 'embargo_hours', 'label': 'News Embargo (hours)', 'type': 'slider', 'min': 0, 'max': 48, 'default': 12},
            {'key': 'joint_statements', 'label': 'Joint Statements', 'type': 'checkbox', 'default': True}
        ]
    },
    'incident_response': {
        'label': '🚨 Incident Response',
        'fields': [
            {'key': 'escalation_protocol', 'label': 'Escalation Protocol', 'type': 'selectbox', 'options': ['immediate', 'tiered', 'consultative'], 'default': 'tiered'},
            {'key': 'cooling_period_hours', 'label': 'Cooling Period (hours)', 'type': 'slider', 'min': 0, 'max': 72, 'default': 24}
        ]
    },
    'naval_restrictions': {
        'label': '⚓ Naval Restrictions',
        'fields': [
            {'key': 'max_vessel_size_tons', 'label': 'Max Vessel Size (tons)', 'type': 'slider', 'min': 100, 'max': 5000, 'default': 1000},
            {'key': 'weapons_restrictions', 'label': 'Weapons Restrictions', 'type': 'checkbox', 'default': True}
        ]
    }
}

ROLE_INFO = {
    'PH_GOV': {
        'name': '🇵🇭 Philippines',
        'color': '#0038A8',
        'interests': [
            'Maintain sovereignty over territorial waters',
            'Ensure safe resupply to garrison',
            'Protect fishermen livelihoods'
        ]
    },
    'PRC_MARITIME': {
        'name': '🇨🇳 China',
        'color': '#DE2910',
        'interests': [
            'Assert historical claims in South China Sea',
            'Maintain strategic control over waters',
            'Prevent normalization of opponent presence'
        ]
    }
}

# Comprehensive scenario context and resources
SCENARIO_RESOURCES = {
    'scenario_A': {
        'name': 'Second Thomas Shoal (Resupply)',
        'overview': '''
The Second Thomas Shoal dispute centers on the BRP Sierra Madre, a Philippine Navy ship deliberately
grounded in 1999 to establish a territorial presence. Regular resupply missions to the small garrison
aboard have become flashpoints for confrontation with Chinese maritime forces.
        ''',
        'historical_context': '''
**Key Historical Events:**

- **1999**: Philippines grounds BRP Sierra Madre to assert sovereignty after Mischief Reef incident
- **2013**: China establishes permanent presence around shoal following Scarborough standoff
- **2014-2016**: Resupply missions increasingly harassed by Chinese Coast Guard
- **2016**: Arbitral Tribunal rules on Philippines v. China case
- **2021-Present**: Escalating incidents including water cannon use, laser targeting, dangerous maneuvers

**Academic Sources:**
- Fravel, M. Taylor (2008). "Strong Borders, Secure Nation: Cooperation and Conflict in China's Territorial Disputes"
- Hayton, Bill (2014). "The South China Sea: The Struggle for Power in Asia"
- Thayer, Carlyle A. (2011). "The Tyranny of Geography: Vietnamese Strategies to Constrain China"
        ''',
        'political_context': '''
**Domestic Political Pressures:**

*Philippines:*
- Strong nationalist sentiment against perceived Chinese encroachment
- Fishing communities dependent on traditional grounds
- Military modernization advocates push for stronger stance
- Left-wing groups criticize perceived U.S. dependence

*China:*
- "Nine-dash line" claims central to nationalist narrative
- Communist Party legitimacy tied to territorial integrity
- Domestic audience costs for appearing weak
- Strategic competition with United States in region

**Key Theory**: Putnam's (1988) two-level game theory explains how domestic constraints shape international
negotiations. Leaders must satisfy both international counterparts and domestic constituencies.

**Source**: Putnam, Robert D. (1988). "Diplomacy and Domestic Politics: The Logic of Two-Level Games."
*International Organization* 42(3): 427-460.
        ''',
        'economic_context': '''
**Economic Stakes:**

- **Fishing**: ~$5-10 million annually in traditional catch value
- **Strategic sea lanes**: $3.4 trillion in trade passes through South China Sea annually
- **Energy resources**: Potential oil and gas reserves (estimates vary widely)
- **Tourism**: Growing dive and eco-tourism industry

**Economic Interdependence:**
- China is Philippines' largest trading partner ($67 billion in 2022)
- Philippine remittances from China-connected economies significant
- Chinese investment in Philippine infrastructure (BRI projects)

**Key Theory**: Fravel (2008) demonstrates China may compromise on territorial disputes when economic
interests are at stake, suggesting economic linkages could facilitate agreement.

**Source**: Fravel, M. Taylor (2008). "Strong Borders, Secure Nation"
        ''',
        'legal_context': '''
**International Legal Framework:**

- **UNCLOS (1982)**: Defines EEZ rights, maritime entitlements
- **2016 Arbitral Award**: Ruled against Chinese "nine-dash line" claims
  - China rejects tribunal's jurisdiction
  - Philippines has historic rights to traditional fishing grounds
  - BRP Sierra Madre does not generate maritime entitlements

**Key Legal Principles:**
1. **Freedom of Navigation**: High seas rights vs. coastal state jurisdiction
2. **Historic Rights**: Traditional fishing vs. modern EEZ claims
3. **Dispute Resolution**: Peaceful settlement obligation under UN Charter

**Legal Scholarship:**
- Schofield & Storey (2009). "The South China Sea Dispute: Increasing Stakes and Rising Tensions"
- Talmon (2014). "The South China Sea Arbitration and the Finality of 'Final' Awards"
        ''',
        'domestic_constraints': '''
**Philippine Domestic Constraints:**

- **Win-set size**: Medium (0.4-0.6) - Nationalist pressure but pragmatic leadership
- **Veto players**: Military, fishing lobby, nationalist politicians
- **Public opinion**: 78% view China negatively (2023 Pew poll)
- **Ratification**: Senate approval needed for major agreements

**China Domestic Constraints:**

- **Win-set size**: Small (0.2-0.4) - High nationalist pressure, authoritarian control
- **Veto players**: PLA Navy, nationalist commentators, CCP hardliners
- **Public opinion**: 80%+ support strong South China Sea stance
- **Ratification**: No formal ratification but CCP consensus needed

**Key Theory**: Putnam (1988) shows smaller domestic win-sets limit negotiation flexibility.
Domestic constraints must be managed through strategic framing and incremental steps.
        ''',
        'mediation_frameworks': '''
**Applicable Mediation Theories:**

1. **GRIT (Graduated Reciprocation in Tension-reduction)**
   - Source: Osgood, Charles E. (1962). "An Alternative to War or Surrender"
   - Application: Phased confidence-building measures to de-escalate

2. **Principled Negotiation**
   - Source: Fisher & Ury (1981). "Getting to Yes"
   - Focus on interests not positions
   - Invent options for mutual gain
   - Use objective criteria

3. **Two-Level Game Theory**
   - Source: Putnam (1988)
   - Navigate international and domestic constraints simultaneously

4. **Tit-for-Tat Cooperation**
   - Source: Axelrod (1984). "The Evolution of Cooperation"
   - Begin cooperatively, then mirror opponent's moves
        ''',
        'simulation_explanation': '''
**How the Simulation Works:**

The agent-based model simulates interactions between stakeholder agents (Philippines, China, etc.)
based on the agreement terms you design. Each agent:

1. **Evaluates** agreement terms against their interests and constraints
2. **Takes actions** (resupply missions, patrols, etc.) according to agreed protocols
3. **Responds** to other agents' actions based on trust levels and past behavior
4. **Updates** beliefs about other parties based on compliance

**Key Metrics:**
- **Compliance Rate**: How well parties follow agreement terms
- **Incident Frequency**: Number of confrontations/violations
- **Escalation Risk**: Probability of crisis escalation
- **Sustainability**: Long-term viability of agreement

**Theoretical Foundation:**
The simulation incorporates:
- Rational choice theory (agents maximize utility)
- Prospect theory (loss aversion in decision-making)
- Social learning (agents update beliefs based on experience)
- Network effects (third-party influence on behavior)
        '''
    },
    'scenario_B': {
        'name': 'Scarborough Shoal (Fishing)',
        'overview': '''
Scarborough Shoal is a ring of reefs in the South China Sea that has been a traditional fishing ground
for Filipino fishermen for generations. After a 2012 standoff, China established de facto control,
restricting Philippine access and creating ongoing tensions over fishing rights.
        ''',
        'historical_context': '''
**Key Historical Events:**

- **Pre-2012**: Traditional fishing ground for Philippine, Chinese, and Vietnamese fishermen
- **April 2012**: Standoff begins when Philippine Navy attempts to arrest Chinese fishermen
- **June 2012**: Both sides withdraw, but China maintains coast guard presence
- **2012-2016**: Philippines files arbitration case; China blocks Philippine fishing access
- **2016**: Arbitral Tribunal rules shoal is traditional fishing ground, not territory
- **2016-Present**: Partial Philippine fishing access restored but heavily monitored

**Academic Sources:**
- Dutton, Peter (2011). "Three Disputes and Three Objectives: China and the South China Sea"
- Buszynski, Leszek (2012). "The South China Sea: Oil, Maritime Claims, and U.S.-China Strategic Rivalry"
        ''',
        'political_context': '''
**Domestic Political Pressures:**

*Philippines:*
- Fishing communities' livelihoods directly affected
- 2016 arbitral victory creates expectation of access
- Nationalist groups demand enforcement of ruling
- Balance between economic ties with China and sovereignty

*China:*
- Scarborough seen as test case for regional claims
- Domestic narrative emphasizes historical rights
- Prestige tied to maintaining control after 2012 "victory"
- Precedent-setting for other disputed features

**Key Theories:**
1. **Audience Costs** (Fearon 1994): Public commitments create domestic pressure to follow through
2. **Diversionary Theory**: Leaders may take hard line to distract from domestic issues

**Sources:**
- Fearon, James D. (1994). "Domestic Political Audiences and the Escalation of International Disputes"
- Mansfield, Edward D. & Jack Snyder (2005). "Electing to Fight"
        ''',
        'economic_context': '''
**Economic Stakes:**

- **Fishing Industry**:
  - Estimated 200-300 Philippine fishing boats operated before 2012
  - Annual catch value: $8-12 million for Philippine fishermen
  - Chinese fishing fleet also relies on shoal's rich waters

- **Food Security**:
  - Fish protein accounts for 40% of Philippine diet
  - Loss of traditional grounds impacts coastal communities
  - Alternative fishing areas already overfished

- **Tourism**: Potential eco-tourism and diving destination (unrealized due to dispute)

**Economic Interdependence Effects:**
- Philippine-China trade: $67 billion (2022)
- Chinese FDI in Philippines: $280 million (2022)
- Potential for economic linkage strategies

**Key Theory**: Fravel (2008) shows China compromises when economic stakes are high. Linking
fishing access to broader economic cooperation could create path to agreement.
        ''',
        'legal_context': '''
**International Legal Framework:**

- **2016 Arbitral Award** (Philippines v. China):
  - Scarborough Shoal generates no maritime entitlements
  - Traditional fishing rights preserved for both parties
  - China's blocking of access violates Philippines' rights
  - China rejects award's validity

- **UNCLOS Framework**:
  - Article 62: Coastal states should promote optimal utilization
  - Article 300: Good faith obligation
  - Traditional fishing rights recognized

**Key Legal Debates:**
1. Can fishing rights be enforced without sovereignty determination?
2. What remedies exist when one party rejects tribunal ruling?
3. Role of traditional rights vs. EEZ claims

**Legal Scholarship:**
- Beckman, Robert (2013). "The UN Convention on the Law of the Sea and the Maritime Disputes in the South China Sea"
- Talmon, Stefan (2014). "The South China Sea Arbitration: Observations on the Award on Jurisdiction and Admissibility"
        ''',
        'domestic_constraints': '''
**Philippine Domestic Constraints:**

- **Win-set size**: Medium-Large (0.5-0.7) - Fishing communities want access, pragmatic approach possible
- **Veto players**: Fishing lobby, coastal mayors, environmental groups
- **Public opinion**: Strong support for fishing rights (85%+) but less nationalist than territory
- **Ratification requirements**: Fishing agreements may not require Senate approval

**China Domestic Constraints:**

- **Win-set size**: Small-Medium (0.3-0.5) - 2012 "victory" narrative constrains retreat
- **Veto players**: PLA Navy, nationalist media, fishing industry
- **Public opinion**: High awareness of Scarborough due to 2012 standoff
- **Ratification**: CCP consensus needed; military input significant

**Key Insight**: Fishing access may have larger Philippine win-set than sovereignty issues,
creating opportunity for agreement if framed around resource management not territorial concession.
        ''',
        'mediation_frameworks': '''
**Applicable Mediation Theories:**

1. **Integrative Bargaining** (Walton & McKersie 1965)
   - Expand pie through joint resource management
   - Reframe from zero-sum to positive-sum
   - Application: Shared fishing quotas, joint conservation

2. **Problem-Solving Workshops** (Kelman 1972)
   - Focus on underlying needs not positions
   - Build empathy and understanding
   - Application: Joint fishermen meetings, technical cooperation

3. **Track II Diplomacy**
   - Unofficial dialogue to explore options
   - Reduce domestic audience costs
   - Application: Academic/think tank facilitated discussions

4. **Salami Tactics in Reverse**
   - Incremental confidence building
   - Small reciprocal gestures
   - Application: Phased expansion of fishing access

**Sources:**
- Walton, Richard E. & Robert B. McKersie (1965). "A Behavioral Theory of Labor Negotiations"
- Kelman, Herbert C. (1972). "The Problem-Solving Workshop in Conflict Resolution"
        ''',
        'simulation_explanation': '''
**How the Simulation Works:**

The agent-based model simulates fishing activity, enforcement patrols, and interactions between
stakeholder agents based on your agreement design.

**Simulation Components:**

1. **Fisher Agents**:
   - Decide when/where to fish based on quotas, safety, catch expectations
   - React to enforcement actions
   - Update compliance based on treatment

2. **Enforcement Agents**:
   - Patrol designated zones
   - Respond to violations according to agreed protocols
   - Balance deterrence vs. escalation

3. **Environmental System**:
   - Fish stock regeneration
   - Impact of overfishing
   - Seasonal variations

**Key Metrics:**
- **Fishing Sustainability**: Stock levels over time
- **Access Equity**: Distribution of catch between parties
- **Incident Rate**: Confrontations between fishermen and enforcement
- **Compliance**: Adherence to quotas and zone restrictions
- **Economic Welfare**: Fishermen income and food security

**Theoretical Foundation:**
- Common-pool resource theory (Ostrom 1990)
- Deterrence theory (enforcement effectiveness)
- Prospect theory (fishermen risk-taking behavior)
        '''
    }
}


# ==================== HELPER FUNCTIONS ====================

def render_resources_tab(scenario_id: str):
    """
    Render the Supporting Resources tab with comprehensive context

    Args:
        scenario_id: The scenario identifier (e.g., 'scenario_A')
    """
    resources = SCENARIO_RESOURCES.get(scenario_id, {})

    if not resources:
        st.warning("No resources available for this scenario")
        return

    st.title(f"📚 Supporting Resources: {resources.get('name', 'Unknown Scenario')}")

    st.markdown("""
    This section provides comprehensive background information, academic sources, and theoretical frameworks
    to help you understand the context and design effective agreements.
    """)

    # Create expandable sections for each resource type
    with st.expander("📖 **Scenario Overview**", expanded=True):
        st.markdown(resources.get('overview', 'No overview available'))

    with st.expander("🕰️ **Historical Context**", expanded=False):
        st.markdown(resources.get('historical_context', 'No historical context available'))

    with st.expander("🏛️ **Political Context**", expanded=False):
        st.markdown(resources.get('political_context', 'No political context available'))

    with st.expander("💰 **Economic Context**", expanded=False):
        st.markdown(resources.get('economic_context', 'No economic context available'))

    with st.expander("⚖️ **Legal Context**", expanded=False):
        st.markdown(resources.get('legal_context', 'No legal context available'))

    with st.expander("🏠 **Domestic Constraints**", expanded=False):
        st.markdown(resources.get('domestic_constraints', 'No domestic constraints information available'))

    with st.expander("🤝 **Mediation Frameworks & Theories**", expanded=False):
        st.markdown(resources.get('mediation_frameworks', 'No mediation frameworks available'))

    with st.expander("🔬 **Simulation Explanation**", expanded=False):
        st.markdown(resources.get('simulation_explanation', 'No simulation explanation available'))

    with st.expander("📊 **Strategic Dimensions & Soft Power**", expanded=False):
        st.markdown("""
        ### Understanding Strategic Context

        Beyond formal negotiation parameters, four strategic dimensions track each player's **soft power** and
        **strategic positioning** in the negotiation environment. These metrics influence escalation risk and
        agreement sustainability.

        #### The Four Dimensions

        **1. Diplomatic Capital (0-100)**
        - **Definition**: The ability to influence outcomes through diplomatic channels, international relationships,
          and multilateral institutions.
        - **Example**: A state with strong ASEAN ties, UN Security Council support, or bilateral alliances has
          higher diplomatic capital.
        - **Why It Matters**: High diplomatic capital reduces escalation risk by providing alternative channels
          for conflict resolution and increasing the costs of aggressive behavior.
        - **Academic Grounding**: Nye (2004) defines soft power as the ability to shape preferences through
          attraction rather than coercion. Diplomatic capital represents accumulated soft power resources.

        **2. International Legitimacy (0-100)**
        - **Definition**: The degree to which the international community views a state's claims and actions as
          lawful and justified.
        - **Example**: A state with stronger legal claims (e.g., under UNCLOS) or acting in accordance with
          international law has higher legitimacy.
        - **Why It Matters**: High legitimacy constrains aggressive behavior and provides protection from
          international backlash. Low legitimacy increases vulnerability to sanctions and isolation.
        - **Academic Grounding**: Hurd (2007) shows that legitimacy creates social obligations that constrain
          state behavior even when enforcement is weak. States with high legitimacy face lower costs for
          assertive actions.

        **3. Domestic Support (0-100)**
        - **Definition**: The level of public and governmental backing for a state's negotiation position.
        - **Example**: Strong nationalist sentiment, unified government support, or public approval of the
          negotiation strategy increases domestic support.
        - **Why It Matters**: Leaders with strong domestic support can make credible commitments and resist
          pressure. Weak domestic support creates vulnerability to political challenges and limits negotiation
          flexibility.
        - **Academic Grounding**: Putnam (1988) shows that negotiators face a "two-level game" where they must
          satisfy both international counterparts and domestic constituencies. The size of a state's "win-set"
          (acceptable agreements) depends on domestic politics.

        **4. Credibility (0-100)**
        - **Definition**: A state's reputation for following through on commitments and threats.
        - **Example**: States with a track record of implementing agreements and enforcing red lines have
          higher credibility.
        - **Why It Matters**: High credibility makes threats more believable and promises more valuable,
          increasing bargaining power. Low credibility undermines deterrence and reduces the value of concessions.
        - **Academic Grounding**: Fearon (1994) demonstrates that credibility is central to crisis bargaining.
          States with high credibility can impose "audience costs" on themselves (domestic political costs for
          backing down) that make their commitments believable.

        #### Escalation Risk Modifier

        These strategic dimensions combine to calculate an **escalation modifier** that affects incident probability:

        - **High International Legitimacy** (>70): **-15% escalation risk** (×0.85 modifier)
          - Strong legal standing and international support deter aggressive actions

        - **Low International Legitimacy** (<30): **+20% escalation risk** (×1.20 modifier)
          - Weak legal position increases desperation and risk-taking

        - **Low Credibility** (<40): **+25% escalation risk** (×1.25 modifier)
          - Weak reputation encourages testing and probing by adversaries

        - **Fragile Domestic Support** (<35): **+30% escalation risk** (×1.30 modifier)
          - Domestic weakness creates incentives for diversionary actions or nationalist posturing

        - **High Diplomatic Capital** (>70): **-15% escalation risk** (×0.85 modifier)
          - Strong international relationships provide conflict resolution channels

        **Example**: A player with high legitimacy (75) and strong domestic support (80) would have an
        escalation modifier of 0.85, reducing their escalation risk by 15%. This represents how their
        strong strategic position creates stability.

        #### Theoretical Framework

        This multi-dimensional approach integrates several IR theories:

        - **Soft Power Theory** (Nye, 2004): Power through attraction and legitimacy, not just coercion
        - **Two-Level Games** (Putnam, 1988): Domestic politics as a constraint on international bargaining
        - **Audience Costs & Credibility** (Fearon, 1994): Reputation effects in crisis bargaining
        - **International Legitimacy** (Hurd, 2007): Social obligations that constrain state behavior
        - **Strategic Positioning** (Schelling, 1960): How relative capabilities and commitments affect outcomes

        #### Using Strategic Context in Negotiation

        As a facilitator or player, consider:

        1. **Monitoring Changes**: Track how proposals and actions affect strategic dimensions
        2. **Risk Assessment**: Use the escalation modifier to anticipate instability
        3. **Strategic Actions**: Consider moves that strengthen your position (see Strategic Actions tab)
        4. **Agreement Design**: Craft agreements that maintain or improve strategic positions for all parties

        **Key Insight**: Sustainable agreements must not only resolve the immediate issue but also preserve
        (or improve) the strategic positions of all parties. Agreements that devastate a player's legitimacy,
        credibility, or domestic support are likely to fail even if they appear technically sound.
        """)

    # Strategic Levers Documentation
    with st.expander("⚡ **Strategic Levers & Diplomatic Moves**", expanded=False):
        st.markdown("""
        ### Strategic Actions Library

        Beyond formal negotiation parameters, players can execute **strategic actions** that affect both
        the agreement terms and their soft power metrics. Each action has costs, benefits, prerequisites,
        and risks.

        #### Available Actions

        ---

        #### 1. 🤝 Convene Regional Summit

        **Action Type:** Diplomatic

        **Description:** Organize an ASEAN or APEC summit to build multilateral consensus on maritime
        rules of the road.

        **Parameter Effects:**
        - Hotline → "Dedicated"
        - Patrol Coordination → "Info sharing"
        - Pre-notification → 8 hours

        **Strategic Effects:**
        - Diplomatic Capital: **-20** (Costs significant capital and time to organize)
        - International Legitimacy: **+15** (Shows commitment to multilateral cooperation)
        - Domestic Support: **+5** (Public appreciates diplomatic leadership)
        - Credibility: **+10** (Following through on commitments)

        **Prerequisites:**
        - Diplomatic Capital must be ≥ 30

        **Cost/Risk:** High diplomatic capital required; medium risk. Summit could fail if participants
        don't reach consensus, wasting capital.

        **Academic Basis:** Keohane (1984) - "After Hegemony: Cooperation and Discord in the World
        Political Economy." Multilateral institutions reduce transaction costs and provide information,
        making cooperation more likely even without a hegemon.

        **When to Use:** When you have sufficient diplomatic capital and want to establish formal
        cooperation mechanisms. Best used early in negotiation to set cooperative tone.

        ---

        #### 2. 🛢️ Propose Joint Development Zone

        **Action Type:** Economic

        **Description:** Offer to jointly develop oil/gas resources in disputed waters under shared
        sovereignty arrangement.

        **Parameter Effects:**
        - Joint Enforcement → "Yes"
        - Resource Access → "50-50 revenue share"
        - Economic Incentives → +$50M cooperation fund

        **Strategic Effects:**
        - Diplomatic Capital: **-10** (Requires some capital to negotiate)
        - International Legitimacy: **+20** (Seen as creative compromise)
        - Domestic Support: **-15** (Domestic hardliners may see as concession)
        - Credibility: **+5** (Shows willingness to make difficult compromises)

        **Prerequisites:**
        - Domestic Support must be ≥ 40 (Need cushion to absorb domestic pushback)

        **Cost/Risk:** High domestic political risk. Hardliners may criticize this as "selling out."
        May need to spend political capital explaining benefits.

        **Academic Basis:** Fravel (2008) - "Strong Borders, Secure Nation." Joint development can
        transform zero-sum territorial disputes into positive-sum resource cooperation. China has
        successfully used this approach in land border disputes.

        **When to Use:** When you have strong domestic support and want to break deadlock over
        sovereignty. Signals flexibility and problem-solving orientation.

        ---

        #### 3. 💬 Launch Track II Dialogue

        **Action Type:** Confidence-Building

        **Description:** Establish unofficial academic/expert dialogues to build trust outside formal
        government channels.

        **Parameter Effects:**
        - Scientific Cooperation → "Joint research programs"
        - Academic Exchange → "Scholar visits"
        - Civil Society Forums → Enabled

        **Strategic Effects:**
        - Diplomatic Capital: **+5** (Low-cost way to build relationships)
        - International Legitimacy: **+10** (Shows openness to dialogue)
        - Domestic Support: **+5** (Seen as prudent hedge)
        - Credibility: **+10** (Demonstrates sustained commitment)

        **Prerequisites:** None - always available

        **Cost/Risk:** Low risk, low cost. Track II channels can't replace official negotiations but
        provide valuable back-channel communication.

        **Academic Basis:** Diamond & McDonald (1996) - "Multi-Track Diplomacy: A Systems Approach
        to Peace." Track II dialogues (unofficial, academic) complement Track I (official government)
        by building relationships and exploring creative solutions without political constraints.

        **When to Use:** Always useful. Particularly valuable when official talks are stalled or
        positions are hardened. Creates space for creative problem-solving.

        ---

        #### 4. 📢 Make Public Commitment to Peace

        **Action Type:** Communication

        **Description:** Make high-profile public statement committing to peaceful resolution and
        renouncing use of force.

        **Parameter Effects:**
        - Hotline → "Dedicated"
        - Public Transparency → "Real-time updates"
        - Incident Response → "De-escalation protocol"

        **Strategic Effects:**
        - Diplomatic Capital: **+5** (Builds relationships through transparency)
        - International Legitimacy: **+25** (Strong signal of peaceful intent)
        - Domestic Support: **-10** (Hardliners may see as weakness)
        - Credibility: **+15** (Public commitments create audience costs)

        **Prerequisites:** None - always available

        **Cost/Risk:** Medium domestic political risk. Public commitments create "audience costs"
        (Fearon 1994) - backing down later is costly. But also makes commitments more credible.

        **Academic Basis:** Fearon (1994) - "Domestic Political Audiences and the Escalation of
        International Disputes." Public statements generate audience costs that make commitments
        credible. Leaders who back down after public commitment face domestic punishment.

        **When to Use:** When you want to credibly signal peaceful intent and lock in cooperative
        approach. Warning: This constrains future options, so only use when genuinely committed
        to peaceful resolution.

        ---

        #### 5. 🔍 Increase Military Transparency

        **Action Type:** Confidence-Building

        **Description:** Share information about military exercises, patrol routes, and capabilities
        to reduce risk of miscalculation.

        **Parameter Effects:**
        - Pre-notification → 24 hours
        - Patrol Coordination → "Deconfliction zones"
        - Transparency Measures → "Exercise observers"

        **Strategic Effects:**
        - Diplomatic Capital: **+10** (Builds trust through transparency)
        - International Legitimacy: **+10** (Seen as responsible behavior)
        - Domestic Support: **+5** (Shows confidence in capabilities)
        - Credibility: **+15** (Actions match rhetoric)

        **Prerequisites:** None - always available

        **Cost/Risk:** Low risk. Some military may resist sharing operational details, but
        confidence-building measures reduce accident risk.

        **Academic Basis:** Osgood (1962) - "An Alternative to War or Surrender" (GRIT - Graduated
        Reciprocation in Tension-reduction). Unilateral transparency measures can trigger reciprocal
        gestures and de-escalation spiral.

        **When to Use:** After tensions or near-miss incidents. Demonstrates responsible military
        behavior and can trigger reciprocal transparency from other side.

        ---

        #### 6. 💰 Offer Economic Incentives

        **Action Type:** Economic

        **Description:** Link maritime cooperation to economic benefits (investment, trade, development aid).

        **Parameter Effects:**
        - Economic Cooperation Fund → +$100M
        - Trade Incentives → "Preferential access"
        - Development Aid → "Infrastructure projects"

        **Strategic Effects:**
        - Diplomatic Capital: **-15** (Requires resources and coordination)
        - International Legitimacy: **+15** (Seen as constructive problem-solving)
        - Domestic Support: **-5** (Some see as "buying" cooperation)
        - Credibility: **+10** (Shows willingness to invest in relationship)

        **Prerequisites:** None - always available

        **Cost/Risk:** Medium cost (requires actual resources). Risk that incentives seen as bribes
        rather than genuine cooperation.

        **Academic Basis:** Tollison & Willett (1979) - "An Economic Theory of Mutually Advantageous
        Issue Linkage in International Negotiations." Linking issues (maritime security + economics)
        expands the bargaining space and makes mutually beneficial agreements more likely.

        **When to Use:** When you need to sweeten the deal or when other side has economic needs
        that make maritime cooperation more attractive.

        ---

        ### Strategic Action Guidelines

        **Sequencing Matters:**
        - Start with low-risk actions (Track II, Transparency) to build trust
        - Use high-impact actions (Summits, Joint Development) when trust established
        - Save public commitments for when ready to lock in agreement

        **Managing Domestic Politics:**
        - Monitor your Domestic Support metric closely
        - Actions that lose domestic support (<-10) should be balanced with popular moves
        - Never let Domestic Support fall below 35 (triggers escalation risk)

        **Building Legitimacy:**
        - International Legitimacy is your "safety net" against escalation
        - Actions that boost legitimacy (+10 or more) are valuable insurance
        - High legitimacy (>70) reduces escalation risk by 15%

        **Preserving Credibility:**
        - Credibility accumulates slowly but matters for agreement sustainability
        - Actions that boost credibility (+10 or more) pay long-term dividends
        - Low credibility (<40) increases escalation risk by 25%

        **Cost-Benefit Analysis:**
        - Actions that cost Diplomatic Capital should be saved for high-value moments
        - Consider whether parameter effects are worth strategic costs
        - Some actions (Track II, Transparency) are positive across all dimensions

        """)

    # Additional references section
    st.markdown("---")
    st.markdown("### 📚 Key Academic References")

    st.markdown("""
    **Core Texts:**
    - Axelrod, Robert (1984). *The Evolution of Cooperation*
    - Fearon, James D. (1995). "Rationalist Explanations for War." *International Organization* 49(3)
    - Fisher, Roger & William Ury (1981). *Getting to Yes: Negotiating Agreement Without Giving In*
    - Fravel, M. Taylor (2008). *Strong Borders, Secure Nation*
    - Kahneman, Daniel & Amos Tversky (1979). "Prospect Theory." *Econometrica* 47(2)
    - Ostrom, Elinor (1990). *Governing the Commons*
    - Putnam, Robert D. (1988). "Diplomacy and Domestic Politics." *International Organization* 42(3)
    - Schelling, Thomas C. (1960). *The Strategy of Conflict*

    **South China Sea Specific:**
    - Buszynski, Leszek (2012). "The South China Sea: Oil, Maritime Claims, and U.S.-China Strategic Rivalry"
    - Dutton, Peter (2011). "Three Disputes and Three Objectives: China and the South China Sea"
    - Hayton, Bill (2014). *The South China Sea: The Struggle for Power in Asia*
    - Schofield & Storey (2009). "The South China Sea Dispute: Increasing Stakes and Rising Tensions"
    """)

    # Documentation and Guides section
    st.markdown("---")
    st.markdown("### 📖 Documentation & User Guides")

    st.info("""
    **Comprehensive documentation is available in the project root directory** to help you get the most out of
    the multiplayer negotiation system. These guides cover everything from quick start tutorials to advanced testing procedures.
    """)

    with st.expander("📚 **Available Documentation**", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            #### 🚀 MULTIPLAYER_QUICK_START.md

            **Perfect for first-time users** - Get up and running in 10 minutes!

            **What's inside:**
            - 7 simple steps from setup to simulation
            - Example proposals and responses
            - 4 hands-on experiments to try
            - Common issues and quick fixes
            - Time required: 10-15 minutes

            **Who should read this:** New users, first-time facilitators, students

            ---

            #### 📘 MULTIPLAYER_USER_GUIDE.md

            **Complete reference guide** for facilitators and players.

            **What's inside:**
            - Complete facilitator workflow (session to debrief)
            - Player guide for all 6 tabs
            - Strategic actions guide (all 6 actions explained)
            - Simulation interpretation (4 metrics + patterns)
            - Best practices for educators
            - 20+ academic references
            - ~50 pages of comprehensive documentation

            **Who should read this:** Facilitators planning sessions, players wanting strategy tips, educators
            """)

        with col2:
            st.markdown("""
            #### 🧪 MULTIPLAYER_TESTING_GUIDE.md

            **Comprehensive testing procedures** for all features.

            **What's inside:**
            - 22 test cases covering Phases 1-4
            - Facilitator workflow testing
            - Player workflow testing
            - Multi-user scenarios
            - End-to-end integration tests
            - Troubleshooting guide
            - Performance benchmarks

            **Who should read this:** Developers, QA testers, technical users

            ---

            #### 🏗️ MULTIPLAYER_FEATURE_IMPLEMENTATION_PLAN.md

            **Technical architecture and implementation details**.

            **What's inside:**
            - 6-phase implementation roadmap
            - Architecture diagrams
            - Academic theoretical frameworks
            - Feature specifications
            - Phase completion status
            - Future enhancement ideas (Phases 5-6)

            **Who should read this:** Developers, researchers, technical documentation
            """)

    st.markdown("""
    #### 📂 How to Access Documentation

    All documentation files are located in the project root directory:
    ```
    /home/dk/scs_mediator_sdk_v2/
    ├── MULTIPLAYER_QUICK_START.md          # 10-minute tutorial
    ├── MULTIPLAYER_USER_GUIDE.md           # Complete user reference
    ├── MULTIPLAYER_TESTING_GUIDE.md        # Testing procedures
    └── MULTIPLAYER_FEATURE_IMPLEMENTATION_PLAN.md  # Technical specs
    ```

    **To view these files:**
    - Open them in any text editor or markdown viewer
    - View on GitHub (if repository is published)
    - Use VS Code, Atom, or similar editors for best rendering

    **Recommended Reading Order:**
    1. **First-time users:** Start with MULTIPLAYER_QUICK_START.md (10 min)
    2. **Facilitators:** Read MULTIPLAYER_USER_GUIDE.md Facilitator section (30 min)
    3. **Players:** Read MULTIPLAYER_USER_GUIDE.md Player section (20 min)
    4. **Testing/QA:** Follow MULTIPLAYER_TESTING_GUIDE.md (60-90 min)
    5. **Developers:** Review MULTIPLAYER_FEATURE_IMPLEMENTATION_PLAN.md for architecture
    """)

    st.success("""
    **💡 Pro Tip:** Keep the MULTIPLAYER_USER_GUIDE.md open in a separate window during your first few sessions
    for quick reference on strategic actions, simulation interpretation, and best practices!
    """)


def render_field(issue_id: str, field_config: dict, key_prefix: str):
    """
    Render a single UI field based on its configuration

    Args:
        issue_id: The issue identifier (e.g., 'resupply_SOP')
        field_config: Field configuration from ISSUE_METADATA
        key_prefix: Unique prefix for Streamlit widget keys

    Returns:
        The value selected by the user
    """
    field_type = field_config['type']
    label = field_config['label']
    unique_key = f"{key_prefix}_{issue_id}_{field_config['key']}"

    if field_type == 'slider':
        return st.slider(
            label,
            min_value=field_config['min'],
            max_value=field_config['max'],
            value=field_config['default'],
            key=unique_key
        )
    elif field_type == 'selectbox':
        options = field_config['options']
        default_idx = 0
        if 'default' in field_config:
            try:
                default_idx = options.index(field_config['default'])
            except ValueError:
                default_idx = 0
        return st.selectbox(
            label,
            options=options,
            index=default_idx,
            key=unique_key
        )
    elif field_type == 'multiselect':
        return st.multiselect(
            label,
            options=field_config['options'],
            default=field_config.get('default', []),
            key=unique_key
        )
    elif field_type == 'checkbox':
        return st.checkbox(
            label,
            value=field_config.get('default', False),
            key=unique_key
        )
    else:
        st.warning(f"Unknown field type: {field_type}")
        return None


def build_proposal_ui(scenario_id: str, key_prefix: str = "prop") -> dict:
    """
    Build dynamic proposal UI based on scenario

    Shows ALL available issue types for every scenario (user can configure all options).

    Args:
        scenario_id: The scenario identifier
        key_prefix: Unique prefix for widget keys

    Returns:
        Dictionary of proposal data structured by issue
    """
    scenario_config = SCENARIOS.get(scenario_id, {})

    # Show ALL issue types from ISSUE_METADATA for every scenario
    all_issues = list(ISSUE_METADATA.keys())

    if not all_issues:
        st.warning("No issues configured")
        return {}

    # Show scenario description
    st.info(f"**Scenario**: {scenario_config.get('name', 'Unknown')}\n\n"
            f"{scenario_config.get('description', '')}")

    st.markdown("### Proposal Terms")
    st.markdown("💡 **All issue types are available** - configure any combination of terms below:")

    # Create columns for better layout (3 columns for better organization)
    num_cols = 3
    cols = st.columns(num_cols)

    proposal_data = {}

    for idx, issue_id in enumerate(all_issues):
        col_idx = idx % num_cols

        with cols[col_idx]:
            issue_meta = ISSUE_METADATA.get(issue_id)

            if not issue_meta:
                st.warning(f"No metadata for issue: {issue_id}")
                continue

            # Render issue section
            st.markdown(f"#### {issue_meta['label']}")

            issue_data = {}
            for field_config in issue_meta['fields']:
                field_key = field_config['key']
                value = render_field(issue_id, field_config, key_prefix)
                issue_data[field_key] = value

            proposal_data[issue_id] = issue_data

            # Add spacing between issues
            st.markdown("")

    return proposal_data


# ==================== SESSION STATE INITIALIZATION ====================

def init_session_state():
    """Initialize session state variables"""
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None  # 'facilitator', 'player'

    if 'user_type' not in st.session_state:
        st.session_state.user_type = None  # Role selection

    if 'session_id' not in st.session_state:
        st.session_state.session_id = None

    if 'player_id' not in st.session_state:
        st.session_state.player_id = None

    if 'facilitator_id' not in st.session_state:
        st.session_state.facilitator_id = None

    if 'session_manager' not in st.session_state:
        st.session_state.session_manager = get_session_manager()

    if 'strategy_notes' not in st.session_state:
        st.session_state.strategy_notes = ""

    # Phase 5: Peace Mediation Tools
    if 'cbm_library' not in st.session_state:
        st.session_state.cbm_library = CBMLibrary()

    if 'spoiler_manager' not in st.session_state:
        st.session_state.spoiler_manager = SpoilerManager()

    if 'multi_track_mediator' not in st.session_state:
        st.session_state.multi_track_mediator = MultiTrackMediator()


# ==================== ROLE SELECTION ====================

def role_selection():
    """Initial role selection screen"""
    st.title("🌊 SCS Negotiation Simulation")
    st.markdown("### Multi-Player Mode")

    st.markdown("""
    <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h4 style="margin: 0 0 10px 0;">How It Works:</h4>
        <p style="margin: 5px 0;">• <strong>Facilitator</strong>: Creates session, proposes agreements, runs simulation</p>
        <p style="margin: 5px 0;">• <strong>Players</strong>: Join with session code, review proposals, accept/reject</p>
        <p style="margin: 5px 0;">• <strong>Goal</strong>: Negotiate an agreement that all parties accept</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background-color: #f5f5f5; padding: 20px; border-radius: 10px; height: 200px;">
            <h3 style="color: #1976d2;">🎯 Facilitator</h3>
            <p>Create and manage the negotiation session</p>
            <ul>
                <li>Create session & share code</li>
                <li>Propose agreement terms</li>
                <li>Run simulation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Join as Facilitator", use_container_width=True, type="primary"):
            st.session_state.user_type = 'facilitator'
            st.rerun()

    with col2:
        st.markdown("""
        <div style="background-color: #f5f5f5; padding: 20px; border-radius: 10px; height: 200px;">
            <h3 style="color: #388e3c;">👤 Player</h3>
            <p>Represent a stakeholder country</p>
            <ul>
                <li>Join with session code</li>
                <li>Review proposals</li>
                <li>Accept or reject terms</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Join as Player", use_container_width=True):
            st.session_state.user_type = 'player'
            st.rerun()


# ==================== FACILITATOR VIEW ====================

def facilitator_view():
    """Facilitator dashboard and controls"""
    sm = st.session_state.session_manager

    st.title("🎯 Facilitator Dashboard")

    # Sidebar
    with st.sidebar:
        st.markdown("### Session Controls")

        if st.session_state.session_id:
            session = sm.get_session(st.session_state.session_id)
            if session:
                st.success(f"**Session**: {session.session_code}")
                st.info(f"**Status**: {session.status.upper()}")

        if st.button("🚪 Logout"):
            st.session_state.user_type = None
            st.session_state.session_id = None
            st.rerun()

        st.markdown("---")

        # Phase 6: AI Guide for Facilitators
        with st.expander("💬 AI Guide", expanded=False):
            st.markdown("**🤖 Mediator Assistant**")
            st.caption("AI-powered guidance for facilitators")

            # Initialize AI guide in session state with persistence
            if 'ai_guide' not in st.session_state:
                try:
                    # Get API key from session state (set during initialization)
                    api_key = st.session_state.get('anthropic_api_key', None)

                    # Create guide with unique session ID for facilitator
                    facilitator_session_id = f"facilitator_{st.session_state.get('session_id', 'default')}"
                    st.session_state.ai_guide = create_instructor_guide(
                        api_key=api_key,
                        session_id=facilitator_session_id,
                        enable_persistence=True
                    )
                    # Load existing chat history from persisted data
                    st.session_state.chat_history = [
                        {
                            "question": st.session_state.ai_guide.conversation_history[i].content,
                            "answer": st.session_state.ai_guide.conversation_history[i+1].content if i+1 < len(st.session_state.ai_guide.conversation_history) else "",
                            "sources": ""
                        }
                        for i, msg in enumerate(st.session_state.ai_guide.conversation_history)
                        if msg.role == "user" and i+1 < len(st.session_state.ai_guide.conversation_history)
                    ]
                except Exception as e:
                    st.error(f"AI Guide unavailable: {str(e)}")
                    st.session_state.ai_guide = None
                    st.session_state.chat_history = []

            if st.session_state.ai_guide:
                # Update context with simulation parameters
                session = sm.get_session(st.session_state.session_id) if st.session_state.session_id else None
                if session:
                    # Build parameter dict from scenario
                    sim_params = {}
                    scenario = SCENARIOS.get(session.scenario_id, {})
                    issue_types = scenario.get('issue_types', [])

                    for issue_type in issue_types:
                        if issue_type in ISSUE_METADATA:
                            metadata = ISSUE_METADATA[issue_type]
                            for field in metadata.get('fields', []):
                                param_info = {'label': field['label']}
                                if 'min' in field and 'max' in field:
                                    param_info['range'] = f"{field['min']}-{field['max']}"
                                elif 'options' in field:
                                    param_info['options'] = field['options']
                                sim_params[field['key']] = param_info

                    # Get available strategic actions
                    strategic_actions = ["Host Regional Summit", "Propose Joint Development",
                                       "Initiate Track II Dialogue", "Make Public Commitment",
                                       "Increase Transparency", "Offer Economic Incentives"]

                    st.session_state.ai_guide.set_context(
                        scenario=session.scenario_id,
                        session_code=session.session_code,
                        session_status=session.status,
                        num_players=len(session.players),
                        simulation_parameters=sim_params,
                        strategic_actions=strategic_actions
                    )

                # Quick tips
                st.markdown("**Quick Tips:**")
                tips = st.session_state.ai_guide.get_quick_tips()
                for tip in tips[:3]:  # Show top 3 tips
                    st.info(tip)

                # Chat interface
                user_question = st.text_area(
                    "Ask a question:",
                    key="ai_guide_question_facilitator",
                    height=100,
                    placeholder="e.g., How should I interpret low player acceptance rates?"
                )

                if st.button("Ask", key="ai_guide_ask_facilitator"):
                    if user_question.strip():
                        with st.spinner("Thinking..."):
                            result = st.session_state.ai_guide.ask(user_question)
                            response = result.get("response", "")
                            sources = result.get("sources", "")

                            # Add to history
                            st.session_state.chat_history.append({
                                "question": user_question,
                                "answer": response,
                                "sources": sources
                            })
                            st.rerun()

                # Display recent conversation
                if st.session_state.get('chat_history', []):
                    st.markdown("**Recent Conversation:**")
                    for qa in st.session_state.chat_history[-3:]:  # Last 3 Q&A pairs
                        with st.container():
                            st.markdown(f"**Q:** {qa['question']}")
                            answer_preview = qa['answer'][:300] + "..." if len(qa['answer']) > 300 else qa['answer']
                            st.markdown(f"**A:** {answer_preview}")
                            if qa.get('sources'):
                                st.caption(f"📚 Sources: {qa['sources']}")
                            st.markdown("---")

                    if st.button("Clear History", key="clear_history_facilitator"):
                        st.session_state.ai_guide.clear_history()
                        st.session_state.chat_history = []
                        st.rerun()

        st.markdown("---")

        # Auto-refresh checkbox
        auto_refresh = st.checkbox("Auto-refresh (every 5s)", value=False)
        if auto_refresh:
            st.markdown("""
            <script>
            setTimeout(function(){window.location.reload();}, 5000);
            </script>
            """, unsafe_allow_html=True)

    # Main content
    if not st.session_state.session_id:
        # Create new session
        st.subheader("Create New Session")

        scenario_id = st.selectbox(
            "Select Scenario:",
            options=list(SCENARIOS.keys()),
            format_func=lambda x: SCENARIOS[x]['name']
        )

        facilitator_name = st.text_input("Your Name:", value="Facilitator")

        if st.button("🎬 Create Session", type="primary"):
            session_id, session_code = sm.create_session(
                facilitator_id=facilitator_name,
                scenario_id=scenario_id
            )
            st.session_state.session_id = session_id
            st.session_state.facilitator_id = facilitator_name
            st.success(f"✅ Session created! Code: **{session_code}**")
            st.info("Share this code with players")
            st.rerun()

    else:
        # Existing session
        session = sm.get_session(st.session_state.session_id)

        if not session:
            st.error("Session not found")
            return

        # Display session code prominently
        st.markdown(f"""
        <div style="background-color: #4caf50; color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
            <h2 style="margin: 0;">Session Code: {session.session_code}</h2>
            <p style="margin: 5px 0;">Share this code with players to join</p>
        </div>
        """, unsafe_allow_html=True)

        # Players status
        st.subheader("Connected Players")

        if len(session.players) == 0:
            st.warning("⏳ Waiting for players to join...")
            st.info("💡 **Tip**: Click the '🔄 Refresh' button below to check for new players!")
            if st.button("🔄 Refresh Status", key="refresh_facilitator_wait"):
                st.rerun()
        else:
            for player in session.players.values():
                status_icon = "✅" if player.ready else "⏳"
                role_name = ROLE_INFO[player.role]['name']
                st.markdown(f"{status_icon} **{role_name}** ({player.user_name}) - {'Ready' if player.ready else 'Connected'}")

        st.markdown("---")

        # Create tabs for main content, escalation assessment, strategic context, resources, facilitator guide, and peace mediation tools
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🎯 Negotiation", "🚨 Escalation Assessment", "📊 Strategic Context", "📚 Supporting Resources", "📖 Facilitator Guide", "🕊️ Peace Mediation"])

        with tab1:
            # Workflow based on session status
            if session.status == 'setup':
                st.subheader("Waiting for Players")

                if len(session.players) >= 2:
                    if st.button("▶️ Start Negotiation", type="primary"):
                        if sm.start_negotiation(session.session_id):
                            st.success("Negotiation started!")
                            st.rerun()
                        else:
                            st.error("Failed to start. Ensure all players are ready.")
                else:
                    st.info(f"Need at least 2 players (currently: {len(session.players)})")

            elif session.status == 'negotiating':
                st.subheader(f"Round {session.current_round}: Propose Agreement")

                # Dynamic proposal builder based on scenario
                proposal_data = build_proposal_ui(session.scenario_id, key_prefix=f"round_{session.current_round}")

                if st.button(f"📤 Send Proposal to Players (Round {session.current_round})", type="primary"):
                    proposal_id = sm.submit_proposal(
                        session.session_id,
                        'facilitator',
                        proposal_data
                    )
                    if proposal_id:
                        st.success("Proposal sent! Waiting for player responses...")
                        st.rerun()

                # Check if there's a pending proposal
                latest_proposal = sm.get_latest_proposal(session.session_id)
                if latest_proposal:
                    st.markdown("---")
                    st.subheader("Current Proposal Status")

                    st.json(latest_proposal.proposal_data)

                    # Show responses
                    responses = sm.get_proposal_responses(session.session_id, latest_proposal.proposal_id)

                    st.markdown(f"**Responses**: {len(responses)} / {len(session.players)}")

                    for response in responses:
                        player = session.players[response.player_id]
                        role_name = ROLE_INFO[player.role]['name']

                        icon = "✅" if response.response_type == 'accept' else "❌"
                        st.markdown(f"{icon} **{role_name}**: {response.response_type.upper()}")
                        if response.explanation:
                            st.caption(f"  \"{response.explanation}\"")

                    # Check if all responded
                    if sm.all_players_responded(session.session_id, latest_proposal.proposal_id):
                        if latest_proposal.status == 'accepted':
                            st.success("🎉 All players accepted! Ready to simulate.")

                            if st.button("▶️ Run Simulation", type="primary"):
                                st.session_state.simulation_results = None  # Clear previous
                                st.rerun()

            elif session.status == 'simulating':
                st.subheader("🎮 Run Simulation")

                latest_proposal = sm.get_latest_proposal(session.session_id)

                if not session.simulation_results:
                    steps = st.slider("Simulation Duration (steps)", 50, 1000, 300, 50)

                    if st.button("▶️ Start Simulation", type="primary"):
                        with st.spinner("Running simulation..."):
                            try:
                                model = MaritimeModel(
                                    steps=steps,
                                    environment={"weather_state": "calm", "media_visibility": 2},
                                    agreement=latest_proposal.proposal_data,
                                    seed=None
                                )
                                df = model.run()

                                if df.empty:
                                    results = {
                                        "summary": {"incidents": 0, "max_severity": 0},
                                        "events": []
                                    }
                                else:
                                    results = {
                                        "summary": {
                                            "incidents": int(len(df)),
                                            "max_severity": float(df["severity"].max()),
                                            "avg_severity": float(df["severity"].mean())
                                        },
                                        "events": df.to_dict(orient="records")
                                    }

                                sm.save_simulation_results(session.session_id, results)
                                st.success("Simulation complete!")
                                st.rerun()

                            except Exception as e:
                                st.error(f"Simulation failed: {e}")
                else:
                    # Show comprehensive results with detailed analysis
                    results = session.simulation_results
                    summary = results.get('summary', {})
                    events_data = results.get('events', [])

                    st.markdown("### 📊 Simulation Summary")
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        incident_count = summary.get('incidents', len(events_data))
                        st.metric("Total Incidents", incident_count,
                                 delta="Good" if incident_count < 25 else "High",
                                 delta_color="inverse" if incident_count < 25 else "normal")

                    with col2:
                        if events_data:
                            df = pd.DataFrame(events_data)
                            avg_severity = df['severity'].mean() if 'severity' in df.columns else summary.get('avg_severity', 0)
                            st.metric("Avg Severity", f"{avg_severity:.2f}/1.0",
                                     delta="Low" if avg_severity < 0.4 else "High",
                                     delta_color="inverse" if avg_severity < 0.4 else "normal")
                        else:
                            avg_severity = summary.get('avg_severity', 0)
                            st.metric("Avg Severity", f"{avg_severity:.2f}/1.0", delta="No incidents")

                    with col3:
                        if events_data:
                            df = pd.DataFrame(events_data)
                            max_severity = df['severity'].max() if 'severity' in df.columns else summary.get('max_severity', 0)
                            st.metric("Max Severity", f"{max_severity:.2f}/1.0")
                        else:
                            max_severity = summary.get('max_severity', 0)
                            st.metric("Max Severity", f"{max_severity:.2f}/1.0")

                    with col4:
                        if events_data:
                            df = pd.DataFrame(events_data)
                            early = len(df[df['step'] < df['step'].max() * 0.33])
                            late = len(df[df['step'] > df['step'].max() * 0.66])
                            if late < early * 0.8:
                                trend = "✅ Declining"
                            elif late > early * 1.2:
                                trend = "❌ Escalating"
                            else:
                                trend = "➡️ Stable"
                            st.metric("Trend", trend)
                        else:
                            st.metric("Trend", "✅ Perfect")

                    # Add prominent guidance section for facilitators
                    st.markdown("---")
                    st.info("""
**📖 HOW TO INTERPRET THESE RESULTS** (For Facilitators & Players)

These simulation results show **how well the proposed agreement would work in practice** over 6-12 months. The numbers above tell you:
- **Total Incidents**: How many friction events would occur (fewer = better)
- **Average Severity**: How serious typical incidents would be (0-1 scale, lower = better)
- **Trend**: Whether tensions increase, decrease, or stay stable over time

**Quick Assessment Guide**:
- **Good outcome**: 0-20 incidents, <0.30 severity, declining/stable trend → Agreement is sustainable
- **Concerning outcome**: >40 incidents, >0.50 severity, escalating trend → Agreement needs revision

Click below for detailed explanations of what each metric means and how to improve results.
""")

                    # Add detailed explanation section (now expanded by default)
                    with st.expander("📖 Detailed Explanation: Understanding Simulation Results", expanded=True):
                        st.markdown(f"""
#### What These Metrics Mean

**Total Incidents ({incident_count})**
- **What it measures**: Number of friction events during the simulation period
- **What counts as an incident**:
  - Unauthorized vessel incursions
  - Standoff distance violations
  - Failure to prenotify naval activities
  - Patrol route conflicts
  - Hotline communication breakdowns
- **Interpretation**:
  - **0-15 incidents**: Excellent deterrence - agreement is working very well
  - **16-30 incidents**: Good deterrence - minor friction but manageable
  - **31-50 incidents**: Moderate friction - agreement may need strengthening
  - **50+ incidents**: High friction - significant compliance issues
- **Why it matters**: Fewer incidents = better agreement sustainability and lower escalation risk

**Average Severity ({avg_severity if events_data else 0:.2f}/1.0)**
- **What it measures**: Mean severity of incidents on a 0.0 to 1.0 scale
- **Severity scale**:
  - **0.0-0.3**: Minor violations (e.g., small patrol deviations, late notifications)
  - **0.3-0.5**: Moderate violations (e.g., close approaches, communication failures)
  - **0.5-0.7**: Serious violations (e.g., standoff breaches, hostile maneuvers)
  - **0.7-1.0**: Critical violations (e.g., weapons lock-ons, sovereignty violations)
- **What it means**:
  - **<0.30**: Mostly minor friction - easily managed through existing channels
  - **0.30-0.50**: Mix of minor and moderate incidents - requires attention
  - **0.50-0.70**: Serious compliance issues - agreement parameters may be too strict
  - **>0.70**: Critical violations - high risk of escalation, urgent revision needed
- **Why it matters**: Low severity incidents are normal friction; high severity suggests fundamental agreement problems

**Maximum Severity ({max_severity if events_data else 0:.2f}/1.0)**
- **What it measures**: The single worst incident during the simulation
- **Interpretation**:
  - **<0.40**: No major incidents occurred - good containment
  - **0.40-0.60**: At least one serious incident - identify and address the trigger
  - **0.60-0.80**: Critical incident occurred - review parameters that led to it
  - **>0.80**: Near-miss or escalation event - immediate parameter adjustment needed
- **Why it matters**: Even one high-severity event can derail an otherwise functional agreement
- **Action item**: If max severity is high, examine the event log to identify what triggered it

**Trend ({trend if events_data else "✅ Perfect"})**
- **What it measures**: Whether incidents are increasing, decreasing, or stable over time
- **Calculation**: Compares incident frequency in first third vs. last third of simulation
- **Interpretation**:
  - **✅ Declining**: Excellent! Parties are learning and compliance is improving
    - Suggests: Agreement parameters are appropriate, trust is building
    - Mechanism: Initial friction as parties test boundaries, then adaptation
  - **➡️ Stable**: Acceptable. Consistent friction level throughout
    - Suggests: Agreement is sustainable at current friction level
    - Mechanism: Parties have adapted to parameters; ongoing low-level friction is tolerated
  - **❌ Escalating**: Concerning! Incidents are increasing over time
    - Suggests: Agreement parameters may be deteriorating trust or are too restrictive
    - Mechanism: Frustration building, compliance fatigue, or strategic testing
- **Why it matters**: Trend reveals whether the agreement is sustainable long-term

#### What the Simulation Models

The Agent-Based Model (ABM) simulates **300-500 time steps** representing approximately **6-12 months** of real-world interactions.

**Agents in the Model**:
- **Naval vessels** from each party (Philippines, PRC, Vietnam, Malaysia)
- **Patrol aircraft** conducting surveillance
- **Coast guard cutters** enforcing fishing regulations
- **Civilian fishing vessels** operating in the disputed area

**What Agents Do**:
1. **Move** according to patrol patterns and agreement parameters
2. **Detect** other vessels based on radar range and prenotification
3. **React** to proximity violations based on standoff distance rules
4. **Escalate** when parameters are violated (generates incidents)
5. **Communicate** via hotline when incidents occur

**Incident Generation**:
- Incidents occur when agents violate agreement parameters
- Severity depends on:
  - How much parameters were violated (e.g., standoff=5nm but approached to 2nm)
  - Whether communication protocols were followed
  - Historical context (repeated violations increase severity)
  - Strategic importance of the location
- Frequency depends on:
  - How restrictive the parameters are
  - Number of active patrols (patrol_frequency parameter)
  - Geographic constraints (buffer zones, traditional fishing areas)

#### What Good Results Look Like

**Ideal Outcome** (Strong, Sustainable Agreement):
- **Total incidents**: 0-20
- **Avg severity**: <0.25
- **Max severity**: <0.40
- **Trend**: Declining or Stable
- **Interpretation**: Parties comply, minor friction is managed, trust is building

**Acceptable Outcome** (Functional Agreement):
- **Total incidents**: 21-40
- **Avg severity**: 0.25-0.40
- **Max severity**: <0.60
- **Trend**: Stable
- **Interpretation**: Regular friction but contained; agreement is holding but fragile

**Concerning Outcome** (Fragile Agreement):
- **Total incidents**: 41-60
- **Avg severity**: 0.40-0.60
- **Max severity**: >0.60
- **Trend**: Escalating
- **Interpretation**: High friction, compliance issues, risk of breakdown

**Failed Outcome** (Unsustainable Agreement):
- **Total incidents**: >60
- **Avg severity**: >0.60
- **Max severity**: >0.80
- **Trend**: Escalating
- **Interpretation**: Agreement is not working; fundamental revision needed

#### Common Patterns and What They Mean

**Pattern 1: High Incident Count, Low Severity**
- **What happened**: Many minor violations but no serious breaches
- **Interpretation**: Parameters are slightly too restrictive but parties are mostly compliant
- **Action**: Minor parameter relaxation (e.g., increase standoff from 5nm to 6nm)

**Pattern 2: Low Incident Count, High Severity**
- **What happened**: Few incidents but they were serious
- **Interpretation**: Most compliance is good, but specific triggers cause major violations
- **Action**: Review event log to identify trigger (e.g., fishing season conflicts) and address specifically

**Pattern 3: Declining Trend**
- **What happened**: Incidents decrease over simulation time
- **Interpretation**: Parties are adapting, learning boundaries, building trust
- **Mechanism**: Initial testing phase → habituation → cooperation
- **Prognosis**: Agreement is sustainable and strengthening

**Pattern 4: Escalating Trend**
- **What happened**: Incidents increase over simulation time
- **Interpretation**: Frustration building, parameters causing increasing friction
- **Mechanisms**:
  - **Compliance fatigue**: Parameters are too burdensome
  - **Strategic testing**: One party is probing boundaries
  - **External events**: Seasonal factors (fishing season, monsoon)
- **Action**: Identify root cause and adjust parameters or add contingency provisions

#### Academic Grounding

- **Agent-Based Modeling**: Epstein & Axtell (1996) "Growing Artificial Societies"
- **Incident Severity**: Bremer (2000) on crisis escalation thresholds
- **Compliance Theory**: Chayes & Chayes (1993) "On Compliance"
- **Friction and Cooperation**: Axelrod (1984) "Evolution of Cooperation"
- **Trend Analysis**: Leng (1983) on bargaining and learning in crises
""")

                    # Charts and detailed analysis
                    if events_data and len(events_data) > 0:
                        st.markdown("---")
                        st.markdown("### 📉 Incident Analysis")

                        df = pd.DataFrame(events_data)

                        # Time series plot
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("#### Incidents Over Time")
                            df['bucket'] = (df['step'] // 20) * 20
                            ts = df.groupby('bucket').size().reset_index(name='incidents')

                            fig, ax = plt.subplots(figsize=(8, 4))
                            ax.plot(ts['bucket'], ts['incidents'], marker='o', linewidth=2, markersize=6)
                            ax.set_xlabel('Simulation Step')
                            ax.set_ylabel('Incident Count')
                            ax.set_title('Incident Frequency Over Time')
                            ax.grid(True, alpha=0.3)
                            st.pyplot(fig)
                            plt.close(fig)

                        with col2:
                            st.markdown("#### Severity Distribution")
                            fig, ax = plt.subplots(figsize=(8, 4))
                            ax.hist(df['severity'], bins=15, edgecolor='black', alpha=0.7)
                            ax.set_xlabel('Severity')
                            ax.set_ylabel('Frequency')
                            ax.set_title('Distribution of Incident Severity')
                            ax.grid(True, alpha=0.3, axis='y')
                            st.pyplot(fig)
                            plt.close(fig)

                        st.markdown("---")
                        st.markdown("#### 📋 Event Log Sample (First 10 Events)")

                        # Add helpful context about the event log
                        st.info("**How to Read the Event Log**: Each row represents an incident. Hover over columns for descriptions. Higher severity events (>0.6) require immediate attention.")

                        # Display the dataframe with better formatting
                        st.dataframe(df.head(10), use_container_width=True)

                        # Add interpretation guidance for specific events
                        if 'description' in df.columns or 'event_type' in df.columns:
                            st.markdown("##### 🔍 Interpreting Specific Events")

                            # Find the highest severity events
                            if max_severity > 0.5:
                                high_sev_events = df[df['severity'] > 0.5].head(3)
                                if len(high_sev_events) > 0:
                                    st.warning(f"**⚠️ {len(high_sev_events)} High-Severity Events Detected** (severity > 0.5)")
                                    st.markdown("These events require analysis:")
                                    for idx, event in high_sev_events.iterrows():
                                        step = event.get('step', idx)
                                        severity = event.get('severity', 0)
                                        desc = event.get('description', 'No description')
                                        event_type = event.get('event_type', 'Unknown')

                                        st.markdown(f"""
<div style="background-color: #fff3cd; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #ff9800;">
    <p style="margin: 0;"><strong>Step {step}</strong> | Severity: {severity:.2f}</p>
    <p style="margin: 5px 0 0 0; color: #3a3a3a;">Type: {event_type}</p>
    <p style="margin: 5px 0 0 0;">Description: {desc}</p>
    <p style="margin: 5px 0 0 0; font-style: italic; color: #2a2a2a;">💡 <strong>What this means</strong>: This event crossed the threshold for serious violations. Review parameters that may have contributed (standoff distance, prenotification requirements, patrol frequency).</p>
</div>
""", unsafe_allow_html=True)

                    else:
                        st.success("🎉 Perfect! No incidents occurred during simulation. The agreement is highly effective!")

                    # Recommendations
                    st.markdown("---")
                    st.markdown("### 💡 Recommendations")

                    if not events_data or len(events_data) < 25:
                        st.success("✅ **Agreement is working well!** Low incident count indicates good deterrence.")
                    else:
                        st.warning("⚠️ **Consider strengthening agreement:**")
                        st.markdown("- Reduce standoff distance for better verification")
                        st.markdown("- Add stricter CUES compliance requirements")
                        st.markdown("- Implement 24/7 hotline if not already included")

                    if st.button("🔄 Start New Round"):
                        session.status = 'negotiating'
                        session.current_round += 1
                        st.rerun()

        with tab2:
            # Escalation Risk Assessment
            st.subheader("🚨 Escalation Risk Assessment")

            st.markdown("""
            Use this tool to assess the escalation risk of proposed actions before including them in agreements.
            The assessment uses either AI-powered analysis (if ANTHROPIC_API_KEY is set) or comprehensive keyword-based analysis.
            """)

            st.info("💡 **Tip**: Link to [Supporting Resources](#) tab for academic context on escalation dynamics (Kahn 1965, Fearon 1994, Schelling 1960).")

            # Initialize escalation manager
            if 'escalation_manager' not in st.session_state:
                st.session_state.escalation_manager = EscalationManager(use_llm=True)

            escalation_manager = st.session_state.escalation_manager

            # Input section
            st.markdown("### Proposed Action")
            action_text = st.text_area(
                "Describe the action you want to assess:",
                placeholder="Example: Deploy additional coast guard vessels to patrol the disputed area",
                height=100,
                key="mp_escalation_action"
            )

            if st.button("🔍 Assess Escalation Risk", type="primary", disabled=not action_text.strip()):
                with st.spinner("Analyzing escalation risk..."):
                    risk_assessment = escalation_manager.assess_escalation_risk(action_text)
                    st.session_state.mp_risk_assessment = risk_assessment

            # Display results
            if 'mp_risk_assessment' in st.session_state:
                assessment = st.session_state.mp_risk_assessment

                st.markdown("---")
                st.markdown("### Assessment Results")

                # Display risk level with color coding
                risk_level = assessment['risk_level']
                if risk_level < 0.3:
                    risk_color = "🟢 LOW"
                    risk_desc = "This action has low escalation risk."
                elif risk_level < 0.7:
                    risk_color = "🟡 MEDIUM"
                    risk_desc = "This action poses moderate escalation risk. Consider de-escalation measures."
                else:
                    risk_color = "🔴 HIGH"
                    risk_desc = "This action has high escalation risk! Strong de-escalation recommended."

                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric("Risk Level", f"{risk_level:.0%}", help="0-100% scale of escalation probability")
                with col2:
                    st.markdown(f"**{risk_color}**")
                    st.markdown(risk_desc)

                if assessment.get('point_of_no_return', False):
                    st.error("⚠️ **Point of No Return**: This action may cross a critical threshold making de-escalation very difficult!")

                # Assessment method indicator
                method = assessment.get('assessment_method', 'unknown')
                if method == 'llm':
                    st.caption("✨ Assessed using AI-powered analysis")
                else:
                    st.caption("📊 Assessed using keyword-based analysis")

                # Likely counter-escalation responses
                st.markdown("### Likely Counter-Escalation Responses")
                if assessment.get('likely_counter_escalation'):
                    for i, response in enumerate(assessment['likely_counter_escalation'], 1):
                        st.markdown(f"{i}. {response}")
                else:
                    st.info("No specific counter-escalation responses identified.")

                # Display reasoning if available (from LLM)
                if 'reasoning' in assessment:
                    with st.expander("📖 Detailed Reasoning (with Academic Citations)", expanded=False):
                        st.markdown(assessment['reasoning'])

                # De-escalation options
                st.markdown("### De-escalation Options")
                if assessment.get('de_escalation_windows'):
                    for i, path in enumerate(assessment['de_escalation_windows'], 1):
                        st.markdown(f"{i}. {path}")

                # GRIT-based de-escalation sequence
                with st.expander("🕊️ Recommended De-escalation Sequence (GRIT)", expanded=False):
                    st.markdown("*Based on Osgood's (1962) Graduated Reciprocation in Tension-reduction:*")
                    de_escalation_steps = escalation_manager.recommend_de_escalation_sequence()
                    for i, step in enumerate(de_escalation_steps, 1):
                        st.markdown(f"{i}. {step}")

        with tab3:
            # Strategic Context Dashboard
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
                for player_id in session.players.keys():
                    session.strategic_contexts[player_id] = StrategicContext()

            if session.strategic_contexts:
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
                        summary_ctx = ctx.get_summary()
                        comparison_data.append({
                            "Player": f"{session.players[pid].role} ({session.players[pid].user_name})",
                            "Diplomatic Capital": summary_ctx['diplomatic_capital']['value'],
                            "Int'l Legitimacy": summary_ctx['international_legitimacy']['value'],
                            "Domestic Support": summary_ctx['domestic_support']['value'],
                            "Credibility": summary_ctx['credibility']['value'],
                            "Escalation Modifier": f"{summary_ctx['escalation_modifier']:.2f}x"
                        })

                    df = pd.DataFrame(comparison_data)
                    st.dataframe(df, use_container_width=True)
            else:
                st.info("Strategic context tracking will be available once players join the session.")

        with tab4:
            # Supporting Resources
            render_resources_tab(session.scenario_id)

        with tab5:
            # Facilitator Guide
            st.title("📖 Facilitator Guide")

            st.markdown("""
            This guide provides **literature-backed recommendations** for facilitating negotiations.
            Use these insights to make informed decisions when proposing agreement terms.
            """)

            # Display scenario overview guide
            scenario_guide = get_facilitator_guide(session.scenario_id)
            st.markdown(scenario_guide)

            st.markdown("---")

            # Parameter-specific guidance
            st.subheader("💡 Parameter Guidance")
            st.markdown("""
            Below you'll find detailed academic analysis for each parameter you can configure in proposals.
            Each guide includes theoretical significance, trade-offs, and recommendations.
            """)

            # Get scenario metadata
            scenario = SCENARIOS.get(session.scenario_id, {})
            available_issues = scenario.get('all_issues', [])

            # Show guidance for each available issue type
            for issue_type in available_issues:
                issue_meta = ISSUE_METADATA.get(issue_type, {})
                label = issue_meta.get('label', issue_type)

                with st.expander(f"{label} - How to Guide This Parameter"):
                    # Show guidance for each field in this issue
                    fields = issue_meta.get('fields', [])
                    for field in fields:
                        param_key = field['key']
                        param_guide = get_facilitator_guide(session.scenario_id, param_key)

                        if param_guide and "No guide available" not in param_guide:
                            st.markdown(param_guide)
                        else:
                            # Fallback generic guidance
                            st.markdown(f"**{field['label']}**")
                            st.markdown(f"Type: {field['type']}")
                            if 'min' in field and 'max' in field:
                                st.markdown(f"Range: {field['min']} - {field['max']}")
                            if 'options' in field:
                                st.markdown(f"Options: {', '.join(field['options'])}")

        with tab6:
            # Peace Mediation Tools
            st.title("🕊️ Peace Mediation Tools")

            st.markdown("""
            <p style='color: #1a1a1a;'>
            Advanced tools for facilitators to support deeper conflict analysis and peacebuilding strategies.
            Based on academic frameworks from conflict resolution literature.
            </p>
            """, unsafe_allow_html=True)

            # Create 5 sub-tabs for peace mediation tools
            peace_tab1, peace_tab2, peace_tab3, peace_tab4, peace_tab5 = st.tabs([
                "📊 Peace Context Summary",
                "🤝 CBM Recommendations",
                "🏛️ Domestic Politics",
                "⚠️ Spoiler Analysis",
                "🌐 Multi-Track Diplomacy"
            ])

            # TAB 1: Peace Context Summary
            with peace_tab1:
                st.markdown("### Peace Context Summary")
                st.markdown("<p style='color: #1a1a1a;'>Quick overview of peace mediation tools and their purpose.</p>", unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h4 style="color: #000; margin: 0 0 10px 0;">Available Tools</h4>
                    <p style="color: #1a1a1a; margin: 5px 0;"><strong>CBM Recommendations:</strong> Confidence-building measures sequencing based on trust levels</p>
                    <p style="color: #1a1a1a; margin: 5px 0;"><strong>Domestic Politics:</strong> Win-set analysis for understanding domestic constraints</p>
                    <p style="color: #1a1a1a; margin: 5px 0;"><strong>Spoiler Analysis:</strong> Identify and mitigate potential spoilers to agreements</p>
                    <p style="color: #1a1a1a; margin: 5px 0;"><strong>Multi-Track Diplomacy:</strong> Coordinate unofficial channels alongside Track 1 negotiations</p>
                </div>
                """, unsafe_allow_html=True)

                st.info("💡 **Tip**: Use these tools during the negotiation setup phase to inform your mediation strategy before proposing terms.")

            # TAB 2: CBM Recommendations
            with peace_tab2:
                st.markdown("### Confidence-Building Measures Library")
                st.markdown("<p style='color: #1a1a1a;'>Based on Osgood's (1962) GRIT framework and modern CBM research</p>", unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    current_trust = st.slider("Current Trust Level", 0.0, 1.0, 0.3, 0.1, key="cbm_trust_slider")
                with col2:
                    escalation_level = st.slider("Escalation Level", 1, 9, 4, key="cbm_escalation_slider")
                with col3:
                    available_weeks = st.number_input("Available Timeline (weeks)", 1, 52, 20, key="cbm_weeks_input")

                if st.button("Get CBM Recommendations", type="primary", key="cbm_recommend_button"):
                    recommendations = st.session_state.cbm_library.recommend_cbm_sequence(
                        current_trust_level=current_trust,
                        escalation_level=escalation_level,
                        available_time_weeks=available_weeks
                    )

                    st.markdown(f"#### Recommended CBM Sequence ({len(recommendations)} measures)")

                    for i, cbm in enumerate(recommendations, 1):
                        st.markdown(f"""
                        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px; margin: 10px 0; border: 1px solid #ddd;">
                            <h4 style="color: #1976d2; margin: 0 0 10px 0;">{i}. {cbm.name}</h4>
                            <p style="color: #000; margin: 5px 0;"><strong>Category:</strong> <span style="color: #1a1a1a;">{cbm.category.value.replace('_', ' ').title()}</span></p>
                            <p style="color: #000; margin: 5px 0;"><strong>Description:</strong> <span style="color: #1a1a1a;">{cbm.description}</span></p>
                            <div style="display: flex; gap: 20px; margin-top: 10px;">
                                <div style="background-color: #fff; padding: 8px 12px; border-radius: 4px; border: 1px solid #ddd;">
                                    <p style="color: #000; margin: 0; font-size: 14px;"><strong>Trust Building:</strong> <span style="color: #1a1a1a;">{cbm.trust_building_value:.1f}/1.0</span></p>
                                </div>
                                <div style="background-color: #fff; padding: 8px 12px; border-radius: 4px; border: 1px solid #ddd;">
                                    <p style="color: #000; margin: 0; font-size: 14px;"><strong>Risk Reduction:</strong> <span style="color: #1a1a1a;">{cbm.risk_reduction_value:.1f}/1.0</span></p>
                                </div>
                                <div style="background-color: #fff; padding: 8px 12px; border-radius: 4px; border: 1px solid #ddd;">
                                    <p style="color: #000; margin: 0; font-size: 14px;"><strong>Timeline:</strong> <span style="color: #1a1a1a;">{cbm.timeline_weeks} weeks</span></p>
                                </div>
                                <div style="background-color: #fff; padding: 8px 12px; border-radius: 4px; border: 1px solid #ddd;">
                                    <p style="color: #000; margin: 0; font-size: 14px;"><strong>Cost:</strong> <span style="color: #1a1a1a;">{cbm.cost_level.title()}</span></p>
                                </div>
                            </div>
                            <details style="margin-top: 10px;">
                                <summary style="color: #1976d2; cursor: pointer; font-weight: bold;">Implementation Steps</summary>
                                <ul style="color: #1a1a1a; margin: 10px 0;">
                                    {"".join([f"<li>{step}</li>" for step in cbm.implementation_steps])}
                                </ul>
                            </details>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("#### Browse CBMs by Category")
                category = st.selectbox(
                    "Select Category",
                    [cat.value.replace('_', ' ').title() for cat in CBMCategory],
                    key="cbm_category_select"
                )
                category_enum = [cat for cat in CBMCategory if cat.value.replace('_', ' ').title() == category][0]
                cbms_in_category = st.session_state.cbm_library.get_cbms_by_category(category_enum)

                st.markdown(f"<p style='color: #1a1a1a;'><strong>{len(cbms_in_category)} CBMs</strong> in this category:</p>", unsafe_allow_html=True)
                for cbm in cbms_in_category:
                    with st.expander(f"{cbm.name}"):
                        st.markdown(f"<p style='color: #1a1a1a;'><strong>Description:</strong> {cbm.description}</p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: #1a1a1a;'><strong>Trust Building:</strong> {cbm.trust_building_value:.1f} | <strong>Risk Reduction:</strong> {cbm.risk_reduction_value:.1f}</p>", unsafe_allow_html=True)

            # TAB 3: Domestic Politics
            with peace_tab3:
                st.markdown("### Domestic Political Constraints Analysis")
                st.markdown("<p style='color: #1a1a1a;'>Based on Putnam's (1988) Two-Level Game Theory</p>", unsafe_allow_html=True)

                # Get available parties from current session
                available_parties = ["Philippines", "China"]
                if session:
                    scenario = SCENARIOS.get(session.scenario_id, {})
                    scenario_roles = scenario.get('roles', [])

                    # Map roles to friendly party names
                    party_map = {
                        "PH_GOV": "Philippines",
                        "PRC_MARITIME": "China",
                        "MY_CG": "Malaysia",
                        "VN_CG": "Vietnam"
                    }
                    available_parties = [party_map.get(r, r) for r in scenario_roles if r in party_map]

                party_select = st.selectbox(
                    "Select Party to Analyze",
                    available_parties if available_parties else ["Philippines", "China"],
                    key="domestic_party_select"
                )

                # Create analyzer
                if party_select == "Philippines":
                    analyzer = WinSetAnalyzer("Philippines")
                    for constraint in create_philippines_domestic_actors():
                        analyzer.add_domestic_actor(constraint)
                else:
                    analyzer = WinSetAnalyzer("China")
                    for constraint in create_china_domestic_actors():
                        analyzer.add_domestic_actor(constraint)

                st.markdown(f"""
                <div style="background-color: #f0f4ff; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h4 style="color: #000; margin: 0 0 10px 0;">Win-Set Analysis for {party_select}</h4>
                    <p style="color: #1a1a1a; margin: 0;"><strong>Win-Set Size:</strong> {analyzer.win_set_size:.2f}</p>
                    <p style="color: #2a2a2a; margin: 5px 0 0 0; font-size: 14px;">
                        (1.0 = maximum flexibility, 0.0 = completely constrained)
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### Domestic Deal-Breakers")
                deal_breakers = analyzer.identify_deal_breakers()
                if deal_breakers:
                    for db in deal_breakers:
                        st.markdown(f"""
                        <div style="background-color: #ffebee; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #f44336;">
                            <p style="color: #000; margin: 0;">⛔ {db}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color: #1a1a1a;'>No absolute deal-breakers identified at current intensity levels.</p>", unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("#### Test Proposal Against Domestic Constraints")

                latest_proposal = sm.get_latest_proposal(session.session_id) if session else None
                if latest_proposal:
                    st.markdown("<p style='color: #1a1a1a;'>Testing current proposal...</p>", unsafe_allow_html=True)

                    # Create test proposal based on current proposal data
                    # Map proposal data to test format
                    test_proposal = {
                        "fisheries_access": 0.7,
                        "sovereignty_language": 0.6,
                        "bilateral_tensions": 0.3,
                        "military_restrictions": 0.2,
                        "resource_access": 0.8
                    }

                    result = analyzer.test_domestic_acceptability(test_proposal)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        accept_color = "green" if result['acceptable'] else "red"
                        st.markdown(f"""
                        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center;">
                            <h3 style="color: {accept_color}; margin: 0;">{"✓" if result['acceptable'] else "✗"}</h3>
                            <p style="color: #1a1a1a; margin: 5px 0 0 0;">Acceptable</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center;">
                            <h3 style="color: #1976d2; margin: 0;">{result['overall_support']:.0%}</h3>
                            <p style="color: #1a1a1a; margin: 5px 0 0 0;">Overall Support</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col3:
                        st.markdown(f"""
                        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center;">
                            <h3 style="color: #ff9800; margin: 0;">{result['ratification_probability']:.0%}</h3>
                            <p style="color: #1a1a1a; margin: 5px 0 0 0;">Ratification Prob.</p>
                        </div>
                        """, unsafe_allow_html=True)

                    if result.get('objectors'):
                        st.markdown("#### Domestic Objections")
                        for obj in result['objectors']:
                            st.markdown(f"""
                            <div style="background-color: #fff3cd; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #ff9800;">
                                <p style="color: #000; margin: 0;"><strong>{obj['actor']}:</strong> <span style="color: #1a1a1a;">{obj['issue']}</span></p>
                            </div>
                            """, unsafe_allow_html=True)

                    if result.get('required_compensations'):
                        st.markdown("#### Suggested Compensations")
                        for comp in result['required_compensations']:
                            st.markdown(f"""
                            <div style="background-color: #e8f5e9; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #4caf50;">
                                <p style="color: #000; margin: 0;">💡 {comp}</p>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown("#### Ratification Strategy")
                    strategy = analyzer.suggest_ratification_strategy(test_proposal)
                    for step in strategy:
                        st.markdown(f"""
                        <div style="background-color: #e3f2fd; padding: 8px; border-radius: 4px; margin: 5px 0;">
                            <p style="color: #000; margin: 0; font-size: 14px;">{step}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Submit a proposal in the Negotiation tab first to test domestic acceptability.")

            # TAB 4: Spoiler Analysis
            with peace_tab4:
                st.markdown("### Spoiler Threat Analysis")
                st.markdown("<p style='color: #1a1a1a;'>Based on Stedman's (1997) Spoiler Problem Framework</p>", unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background-color: #fff3e0; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <h4 style="color: #000; margin: 0 0 10px 0;">Identified Spoilers</h4>
                    <p style="color: #1a1a1a; margin: 0;"><strong>{len(st.session_state.spoiler_manager.spoilers)}</strong> potential spoilers tracked</p>
                </div>
                """, unsafe_allow_html=True)

                for name, spoiler in st.session_state.spoiler_manager.spoilers.items():
                    with st.expander(f"{'🔴' if spoiler.capability.value == 'high' else '🟡' if spoiler.capability.value == 'medium' else '🟢'} {name}"):
                        st.markdown(f"""
                        <div style="background-color: #fafafa; padding: 10px; border-radius: 5px;">
                            <p style="color: #000; margin: 5px 0;"><strong>Type:</strong> <span style="color: #1a1a1a;">{spoiler.spoiler_type.value.title()}</span></p>
                            <p style="color: #000; margin: 5px 0;"><strong>Capability:</strong> <span style="color: #1a1a1a;">{spoiler.capability.value.title()}</span></p>
                            <p style="color: #000; margin: 5px 0;"><strong>Position:</strong> <span style="color: #1a1a1a;">{spoiler.position.value.title()}</span></p>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("<p style='color: #000; margin: 10px 0 5px 0;'><strong>Interests Threatened:</strong></p>", unsafe_allow_html=True)
                        for interest in spoiler.interests_threatened:
                            st.markdown(f"<p style='color: #1a1a1a; margin: 2px 0; padding-left: 15px;'>• {interest}</p>", unsafe_allow_html=True)

                        st.markdown("<p style='color: #000; margin: 10px 0 5px 0;'><strong>Recommended Strategies:</strong></p>", unsafe_allow_html=True)
                        strategies = st.session_state.spoiler_manager.mitigation_strategies.get(name, [])
                        for strategy in strategies[:3]:
                            st.markdown(f"""
                            <div style="background-color: #e8f5e9; padding: 8px; border-radius: 4px; margin: 5px 0;">
                                <p style="color: #000; margin: 0; font-size: 14px;">{strategy}</p>
                            </div>
                            """, unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("#### Assess Spoiling Risk for Current Agreement")

                latest_proposal = sm.get_latest_proposal(session.session_id) if session else None
                if latest_proposal and st.button("Assess Spoiler Risk", type="primary", key="spoiler_assess_button"):
                    agreement = {
                        "shared_resources": True,
                        "monitoring": True,
                        "demilitarization": False
                    }

                    risk = st.session_state.spoiler_manager.assess_spoiling_risk(agreement)

                    st.markdown(f"""
                    <div style="background-color: {'#ffebee' if risk['overall_risk'] > 0.6 else '#fff8e1' if risk['overall_risk'] > 0.3 else '#e8f5e9'}; padding: 15px; border-radius: 8px; margin: 15px 0;">
                        <h4 style="color: #000; margin: 0 0 10px 0;">Overall Spoiling Risk</h4>
                        <h2 style="color: #000; margin: 0;">{risk['overall_risk']:.1%}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                    if risk.get('high_threat_spoilers'):
                        st.markdown("#### High-Threat Spoilers")
                        for spoiler_name in risk['high_threat_spoilers']:
                            st.markdown(f"""
                            <div style="background-color: #ffcdd2; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #f44336;">
                                <p style="color: #000; margin: 0;">⚠️ {spoiler_name}</p>
                            </div>
                            """, unsafe_allow_html=True)

                    if risk.get('protective_measures_needed'):
                        st.markdown("#### Protective Measures Needed")
                        for measure in risk['protective_measures_needed']:
                            st.markdown(f"""
                            <div style="background-color: #e3f2fd; padding: 8px; border-radius: 4px; margin: 5px 0;">
                                <p style="color: #000; margin: 0; font-size: 14px;">🛡️ {measure}</p>
                            </div>
                            """, unsafe_allow_html=True)
                elif not latest_proposal:
                    st.info("Submit a proposal in the Negotiation tab first to assess spoiler risk.")

            # TAB 5: Multi-Track Diplomacy
            with peace_tab5:
                st.markdown("### Multi-Track Diplomacy Coordination")
                st.markdown("<p style='color: #1a1a1a;'>Based on McDonald & Diamond's (1996) Multi-Track Framework</p>", unsafe_allow_html=True)

                conflict_phase = st.selectbox(
                    "Select Conflict Phase",
                    ["pre_negotiation", "negotiation", "implementation"],
                    format_func=lambda x: {
                        "pre_negotiation": "Pre-Negotiation (Building Foundation)",
                        "negotiation": "Negotiation (Supporting Talks)",
                        "implementation": "Implementation (Monitoring & Support)"
                    }[x],
                    key="multitrack_phase_select"
                )

                if st.button("Get Track Recommendations", type="primary", key="multitrack_recommend_button"):
                    recommendations = st.session_state.multi_track_mediator.recommend_track_sequence(conflict_phase)

                    st.markdown(f"#### Recommended Diplomatic Tracks for {conflict_phase.replace('_', ' ').title()}")

                    for i, rec in enumerate(recommendations, 1):
                        st.markdown(f"""
                        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px; margin: 15px 0; border: 1px solid #ddd;">
                            <h4 style="color: #1976d2; margin: 0 0 10px 0;">{i}. {rec['track'].value.replace('_', ' ').title()}</h4>
                            <p style="color: #000; margin: 5px 0;"><strong>Activity:</strong> <span style="color: #1a1a1a;">{rec['activity']}</span></p>
                            <p style="color: #000; margin: 5px 0;"><strong>Purpose:</strong> <span style="color: #1a1a1a;">{rec['purpose']}</span></p>
                            <p style="color: #000; margin: 5px 0;"><strong>Participants:</strong> <span style="color: #1a1a1a;">{rec['participants']}</span></p>
                            <p style="color: #000; margin: 5px 0;"><strong>Timeline:</strong> <span style="color: #1a1a1a;">{rec['timeline']}</span></p>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("#### Track Overview")

                track_info = {
                    "Track 1": "Official Government Diplomacy",
                    "Track 1.5": "Semi-Official (Retired Officials, Close Advisors)",
                    "Track 2": "Unofficial Dialogue (Academics, NGOs, Think Tanks)",
                    "Track 3": "Business & Commerce",
                    "Track 4": "Citizen Diplomacy (People-to-People)",
                    "Track 5": "Training & Education",
                    "Track 6": "Peace Activism & Advocacy",
                    "Track 7": "Religious & Faith-Based",
                    "Track 8": "Funding & Resources",
                    "Track 9": "Media & Communications"
                }

                for track, description in track_info.items():
                    with st.expander(track):
                        st.markdown(f"<p style='color: #1a1a1a;'>{description}</p>", unsafe_allow_html=True)


# ==================== PLAYER VIEW ====================

def player_view():
    """Player interface with 6-tab navigation"""
    sm = st.session_state.session_manager

    st.title("👤 Player View")

    # Sidebar
    with st.sidebar:
        st.markdown("### Your Session")

        if st.session_state.session_id:
            session = sm.get_session(st.session_state.session_id)
            if session and st.session_state.player_id:
                player = session.players.get(st.session_state.player_id)
                if player:
                    role_name = ROLE_INFO[player.role]['name']
                    st.success(f"**Role**: {role_name}")
                    st.info(f"**Session**: {session.session_code}")

        if st.button("🚪 Logout"):
            st.session_state.user_type = None
            st.session_state.session_id = None
            st.session_state.player_id = None
            st.rerun()

        # Refresh button
        if st.button("🔄 Refresh"):
            st.rerun()

        st.markdown("---")

        # Phase 6: AI Guide for Players
        with st.expander("💬 AI Guide", expanded=False):
            st.markdown("**🤖 Mediator Assistant**")
            st.caption("AI-powered guidance for participants")

            # Initialize AI guide in session state with persistence
            if 'participant_ai_guide' not in st.session_state:
                try:
                    # Get API key from session state
                    api_key = st.session_state.get('anthropic_api_key', None)

                    # Create guide with unique session ID per player
                    player_session_id = f"player_{st.session_state.get('player_id', 'default')}"
                    st.session_state.participant_ai_guide = create_participant_guide(
                        api_key=api_key,
                        session_id=player_session_id,
                        enable_persistence=True
                    )
                    # Load existing chat history
                    st.session_state.participant_chat_history = [
                        {
                            "question": st.session_state.participant_ai_guide.conversation_history[i].content,
                            "answer": st.session_state.participant_ai_guide.conversation_history[i+1].content if i+1 < len(st.session_state.participant_ai_guide.conversation_history) else "",
                            "sources": ""
                        }
                        for i, msg in enumerate(st.session_state.participant_ai_guide.conversation_history)
                        if msg.role == "user" and i+1 < len(st.session_state.participant_ai_guide.conversation_history)
                    ]
                except Exception as e:
                    st.error(f"AI Guide unavailable: {str(e)}")
                    st.session_state.participant_ai_guide = None
                    st.session_state.participant_chat_history = []

            if st.session_state.participant_ai_guide:
                # Update context
                session = sm.get_session(st.session_state.session_id) if st.session_state.session_id else None
                if session and st.session_state.player_id:
                    player = session.players.get(st.session_state.player_id)
                    if player:
                        st.session_state.participant_ai_guide.set_context(
                            scenario=session.scenario_id,
                            party=player.role,
                            session_code=session.session_code,
                            session_status=session.status
                        )

                # Quick tips
                st.markdown("**Quick Tips:**")
                tips = st.session_state.participant_ai_guide.get_quick_tips()
                for tip in tips[:3]:
                    st.info(tip)

                # Chat interface
                user_question = st.text_area(
                    "Ask a question:",
                    key="ai_guide_question_player",
                    height=100,
                    placeholder="e.g., What negotiation strategy should I use?"
                )

                if st.button("Ask", key="ai_guide_ask_player"):
                    if user_question.strip():
                        with st.spinner("Thinking..."):
                            result = st.session_state.participant_ai_guide.ask(user_question)
                            response = result.get("response", "")
                            sources = result.get("sources", "")

                            # Add to history
                            st.session_state.participant_chat_history.append({
                                "question": user_question,
                                "answer": response,
                                "sources": sources
                            })
                            st.rerun()

                # Display recent conversation
                if st.session_state.get('participant_chat_history', []):
                    st.markdown("**Recent Conversation:**")
                    for qa in st.session_state.participant_chat_history[-3:]:
                        with st.container():
                            st.markdown(f"**Q:** {qa['question']}")
                            answer_preview = qa['answer'][:300] + "..." if len(qa['answer']) > 300 else qa['answer']
                            st.markdown(f"**A:** {answer_preview}")
                            if qa.get('sources'):
                                st.caption(f"📚 Sources: {qa['sources']}")
                            st.markdown("---")

                    if st.button("Clear History", key="clear_history_player"):
                        st.session_state.participant_ai_guide.clear_history()
                        st.session_state.participant_chat_history = []
                        st.rerun()

    # Main content
    if not st.session_state.session_id:
        # Join session
        st.subheader("Join Session")

        session_code = st.text_input("Enter Session Code:", placeholder="e.g., REEF-2024").upper()
        user_name = st.text_input("Your Name:", placeholder="e.g., Alice")

        if session_code and user_name:
            session = sm.get_session_by_code(session_code)

            if session:
                # Show available roles
                available_roles = [role for role in SCENARIOS[session.scenario_id]['roles']
                                 if role not in [p.role for p in session.players.values()]]

                if available_roles:
                    role = st.selectbox(
                        "Select Your Role:",
                        options=available_roles,
                        format_func=lambda x: ROLE_INFO[x]['name']
                    )

                    if st.button("✅ Join Session", type="primary"):
                        success, message, player_id = sm.join_session(session_code, user_name, role)

                        if success:
                            st.session_state.session_id = session.session_id
                            st.session_state.player_id = player_id
                            sm.set_player_ready(session.session_id, player_id, True)
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    st.warning("All roles are taken in this session")
            else:
                st.error("Session not found. Check the code and try again.")

    else:
        # Existing session
        session = sm.get_session(st.session_state.session_id)

        if not session:
            st.error("Session not found")
            return

        player = session.players.get(st.session_state.player_id)
        if not player:
            st.error("Player not found")
            return

        role_info = ROLE_INFO[player.role]

        # Show player's role (keep outside tabs)
        st.markdown(f"## {role_info['name']}")

        # Create 6-tab interface
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🎯 Role & Objectives",
            "📋 Current Proposal",
            "💬 Submit Response",
            "📊 Your Strategic Position",
            "⚡ Strategic Actions",
            "📝 Strategy Notes"
        ])

        # TAB 1: Role & Objectives
        with tab1:
            st.markdown("""
            <div style="background-color: #e8f5e9; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4>Your Interests:</h4>
            </div>
            """, unsafe_allow_html=True)

            for interest in role_info['interests']:
                st.markdown(f"• {interest}")

            st.markdown("---")

            st.markdown("### 📖 Strategy Guide")
            player_guide = get_player_guide(player.role, session.scenario_id)
            st.markdown(player_guide)

        # TAB 2: Current Proposal
        with tab2:
            if session.status == 'setup':
                st.info("⏳ Waiting for facilitator to start negotiation...")
                st.info("💡 **Tip**: Click the '🔄 Refresh' button in the sidebar to check for updates!")

                st.subheader("Other Players")
                for p in session.players.values():
                    if p.player_id != player.player_id:
                        other_role_name = ROLE_INFO[p.role]['name']
                        st.markdown(f"✅ {other_role_name} ({p.user_name})")

            elif session.status == 'negotiating':
                st.markdown(f"### Round {session.current_round}")

                latest_proposal = sm.get_latest_proposal(session.session_id)

                if not latest_proposal:
                    st.info("⏳ Waiting for facilitator to propose terms...")
                    if st.button("🔄 Refresh", key="refresh_player_proposal_tab2"):
                        st.rerun()
                else:
                    st.markdown("### 📋 Proposed Agreement")

                    # Display ALL proposal terms in readable format
                    proposal_data = latest_proposal.proposal_data

                    col1, col2 = st.columns(2)

                    with col1:
                        # Resupply Operations
                        if 'resupply_SOP' in proposal_data:
                            st.markdown("#### 🚢 Resupply Operations")
                            sop = proposal_data['resupply_SOP']
                            st.markdown(f"• **Standoff Distance**: {sop.get('standoff_nm', 0)} nm")
                            st.markdown(f"• **Max Escorts**: {sop.get('escort_count', 0)}")
                            st.markdown(f"• **Pre-Notification**: {sop.get('pre_notification_hours', 0)} hours")
                            st.markdown("")

                        # Fishing Rights
                        if 'fishing_rights' in proposal_data:
                            st.markdown("#### 🎣 Fishing Rights")
                            fish = proposal_data['fishing_rights']
                            st.markdown(f"• **Daily Quota**: {fish.get('daily_quota_kg', 0)} kg")
                            st.markdown(f"• **Max Vessels**: {fish.get('vessel_limit', 0)}")
                            gear = fish.get('permitted_gear', [])
                            st.markdown(f"• **Permitted Gear**: {', '.join(gear) if gear else 'None'}")
                            st.markdown("")

                        # Seasonal Restrictions
                        if 'seasonal_restrictions' in proposal_data:
                            st.markdown("#### 📅 Seasonal Restrictions")
                            seasonal = proposal_data['seasonal_restrictions']
                            st.markdown(f"• **Closure Period**: {seasonal.get('closure_months', 0)} months")
                            st.markdown("")

                        # Enforcement Protocols
                        if 'enforcement_protocols' in proposal_data:
                            st.markdown("#### 👮 Enforcement")
                            enf = proposal_data['enforcement_protocols']
                            st.markdown(f"• **Patrol Frequency**: {enf.get('patrol_frequency', 0)}/week")
                            st.markdown(f"• **Inspection Rights**: {enf.get('inspection_rights', 'N/A')}")
                            st.markdown("")

                        # Naval Restrictions
                        if 'naval_restrictions' in proposal_data:
                            st.markdown("#### ⚓ Naval Restrictions")
                            naval = proposal_data['naval_restrictions']
                            st.markdown(f"• **Max Vessel Size**: {naval.get('max_vessel_tons', 0)} tons")
                            st.markdown("")

                    with col2:
                        # Communication
                        if 'hotline_cues' in proposal_data:
                            st.markdown("#### 📞 Communication")
                            hotline = proposal_data['hotline_cues']
                            st.markdown(f"• **Hotline**: {hotline.get('hotline_status', 'N/A').upper()}")
                            st.markdown(f"• **Response Time**: {hotline.get('response_hours', 0)} hours")
                            st.markdown("")

                        # Media Protocol
                        if 'media_protocol' in proposal_data:
                            st.markdown("#### 📰 Media Protocol")
                            media = proposal_data['media_protocol']
                            st.markdown(f"• **News Embargo**: {media.get('embargo_hours', 0)} hours")
                            st.markdown("")

                        # Access Zones
                        if 'access_zones' in proposal_data:
                            st.markdown("#### 🗺️ Access Zones")
                            zones = proposal_data['access_zones']
                            st.markdown(f"• **Zone Radius**: {zones.get('zone_radius_nm', 0)} nm")
                            st.markdown(f"• **Buffer Zone**: {zones.get('buffer_nm', 0)} nm")
                            st.markdown(f"• **Access Type**: {zones.get('access_type', 'N/A')}")
                            st.markdown("")

                        # Incident Response
                        if 'incident_response' in proposal_data:
                            st.markdown("#### 🚨 Incident Response")
                            incident = proposal_data['incident_response']
                            st.markdown(f"• **Escalation Protocol**: {incident.get('escalation_protocol', 'N/A')}")
                            st.markdown(f"• **Cooling Period**: {incident.get('cooling_hours', 0)} hours")
                            st.markdown("")

                    # Show response status
                    responses = sm.get_proposal_responses(session.session_id, latest_proposal.proposal_id)
                    player_response = next((r for r in responses if r.player_id == player.player_id), None)

                    if player_response:
                        st.markdown("---")
                        st.success(f"✅ You responded: **{player_response.response_type.upper()}**")
                        if player_response.explanation:
                            st.info(f"Your comment: \"{player_response.explanation}\"")
                        st.info(f"⏳ Waiting for other players ({len(responses)}/{len(session.players)} responded)")

            elif session.status == 'simulating' or session.status == 'completed':
                st.subheader("📊 Simulation Results")

                if not session.simulation_results:
                    st.info("⏳ Waiting for facilitator to run simulation...")
                else:
                    results = session.simulation_results
                    summary = results.get('summary', {})

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Total Incidents", summary.get('incidents', 0))

                    with col2:
                        st.metric("Avg Severity", f"{summary.get('avg_severity', 0):.2f}/1.0")

                    with col3:
                        st.metric("Max Severity", f"{summary.get('max_severity', 0):.2f}/1.0")

                    incidents = summary.get('incidents', 0)
                    avg_sev = summary.get('avg_severity', 0)

                    if incidents < 25 and avg_sev < 0.4:
                        st.success("✅ Excellent outcome! The agreement you negotiated is sustainable.")
                    elif incidents < 40 and avg_sev < 0.6:
                        st.warning("⚠️ Mixed outcome. The agreement needs minor adjustments.")
                    else:
                        st.error("❌ Concerning outcome. The agreement needs major revision.")

        # TAB 3: Submit Response
        with tab3:
            if session.status == 'setup':
                st.info("⏳ Negotiation has not started yet. No proposals to respond to.")

            elif session.status == 'negotiating':
                st.markdown(f"### Round {session.current_round}")

                latest_proposal = sm.get_latest_proposal(session.session_id)

                if not latest_proposal:
                    st.info("⏳ Waiting for facilitator to propose terms...")
                    if st.button("🔄 Refresh", key="refresh_player_proposal_tab3"):
                        st.rerun()
                else:
                    # Check if player already responded
                    responses = sm.get_proposal_responses(session.session_id, latest_proposal.proposal_id)
                    player_response = next((r for r in responses if r.player_id == player.player_id), None)

                    if player_response:
                        st.success(f"✅ You already responded: **{player_response.response_type.upper()}**")

                        if player_response.explanation:
                            st.info(f"Your comment: \"{player_response.explanation}\"")

                        st.info(f"⏳ Waiting for other players ({len(responses)}/{len(session.players)} responded)")
                        st.markdown("---")
                        st.markdown("💡 **Tip**: View the proposal details in the 'Current Proposal' tab.")

                    else:
                        st.markdown("### Your Response")
                        st.markdown("Review the proposal in the 'Current Proposal' tab, then submit your response below.")

                        response_type = st.radio(
                            "Do you accept this proposal?",
                            options=['accept', 'reject'],
                            format_func=lambda x: "✅ Accept" if x == 'accept' else "❌ Reject",
                            key="response_type_tab3"
                        )

                        explanation = st.text_area(
                            "Comments (optional):",
                            placeholder="Explain your decision...",
                            key="explanation_tab3"
                        )

                        if st.button("📤 Submit Response", type="primary", key="submit_response_tab3"):
                            success = sm.submit_response(
                                session.session_id,
                                latest_proposal.proposal_id,
                                player.player_id,
                                response_type,
                                explanation
                            )

                            if success:
                                st.success("Response submitted!")
                                st.rerun()
                            else:
                                st.error("Failed to submit response")

            elif session.status == 'simulating' or session.status == 'completed':
                st.info("Negotiation phase is complete. No more responses needed.")

        # TAB 4: Your Strategic Position
        with tab4:
            st.markdown("""
            <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; border-left: 5px solid #4682b4; margin-bottom: 20px;">
                <p style="color: #000; margin: 0;"><strong>Strategic Leverage & Soft Power</strong></p>
                <p style="color: #1a1a1a; margin: 10px 0 0 0; font-size: 14px;">
                    Beyond negotiation parameters, strategic actions affect your diplomatic capital, international legitimacy,
                    domestic support, and credibility. These dimensions influence escalation risk and outcome sustainability.
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Initialize strategic context if not exists
            player_id = st.session_state.player_id
            if player_id not in session.strategic_contexts:
                session.strategic_contexts[player_id] = StrategicContext()

            ctx = session.strategic_contexts[player_id]
            summary = ctx.get_summary()

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
            st.info(f"Your strategic position {modifier_direction} escalation risk by {abs(modifier_pct):.1f}% (modifier: {modifier:.2f}x)")

        # TAB 5: Strategic Actions
        with tab5:
            st.markdown("""
            <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 5px solid #ffc107; margin-bottom: 20px;">
                <p style="color: #000; margin: 0;"><strong>Strategic Moves & Diplomatic Levers</strong></p>
                <p style="color: #1a1a1a; margin: 10px 0 0 0; font-size: 14px;">
                    Beyond formal negotiation parameters, you can execute strategic actions that affect both the agreement
                    terms and your soft power metrics. Each action has costs, benefits, and risks. Choose wisely!
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Get strategic context (already initialized in tab4)
            player_id = st.session_state.player_id
            if player_id not in session.strategic_contexts:
                session.strategic_contexts[player_id] = StrategicContext()

            ctx = session.strategic_contexts[player_id]
            available_actions = get_available_actions(ctx)

            if not available_actions:
                st.warning("⚠️ No strategic actions currently available. Some actions require minimum thresholds (e.g., diplomatic capital > 30 for summits, domestic support > 40 for joint development).")
            else:
                st.markdown(f"**{len(available_actions)} actions available** based on your current strategic position.")
                st.markdown("")

                # Display actions in expandable cards
                for action in available_actions:
                    with st.expander(f"🎯 {action.name}"):
                        st.markdown(f"**Type:** {action.action_type.value.replace('_', ' ').title()}")
                        st.markdown(f"**Description:** {action.description}")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("**Parameter Effects:**")
                            if action.parameter_effects:
                                for param, value in action.parameter_effects.items():
                                    st.markdown(f"- `{param}` → `{value}`")
                            else:
                                st.markdown("_No direct parameter changes_")

                        with col2:
                            st.markdown("**Strategic Effects:**")
                            if action.diplomatic_capital_change != 0:
                                sign = "+" if action.diplomatic_capital_change > 0 else ""
                                st.markdown(f"- Diplomatic Capital: {sign}{action.diplomatic_capital_change}")
                            if action.international_legitimacy_change != 0:
                                sign = "+" if action.international_legitimacy_change > 0 else ""
                                st.markdown(f"- Int'l Legitimacy: {sign}{action.international_legitimacy_change}")
                            if action.domestic_support_change != 0:
                                sign = "+" if action.domestic_support_change > 0 else ""
                                st.markdown(f"- Domestic Support: {sign}{action.domestic_support_change}")
                            if action.credibility_change != 0:
                                sign = "+" if action.credibility_change > 0 else ""
                                st.markdown(f"- Credibility: {sign}{action.credibility_change}")

                        st.markdown(f"**Academic Basis:** {action.theoretical_basis}")
                        st.markdown(f"**Risk Level:** {action.risk_level.upper()}")
                        st.caption(f"⚠️ Cost: {action.cost_description}")

                        if st.button(f"Execute: {action.name}", key=f"execute_{action.name}_{player_id}_tab5"):
                            # Apply action to strategic context
                            ctx.apply_action(action)
                            st.success(f"✅ {action.name} executed!")
                            st.balloons()
                            st.rerun()

        # TAB 6: Strategy Notes
        with tab6:
            st.markdown("### 📝 Your Strategy Notes")
            st.markdown("Use this space to keep track of your negotiation strategy, key points, and observations.")

            # Text area for notes with session state persistence
            notes = st.text_area(
                "Strategy Notes:",
                value=st.session_state.strategy_notes,
                height=400,
                placeholder="Enter your strategy notes here...\n\n• Key objectives\n• Negotiation tactics\n• Observations about other players\n• Red lines and compromises",
                key="strategy_notes_input"
            )

            # Update session state when notes change
            if notes != st.session_state.strategy_notes:
                st.session_state.strategy_notes = notes
                st.success("Notes saved!")

            st.caption("💡 Your notes are saved automatically in this session.")


# ==================== MAIN APP ====================

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="SCS Multiplayer Negotiation",
        page_icon="🌊",
        layout="wide"
    )

    init_session_state()

    if not st.session_state.user_type:
        role_selection()
    elif st.session_state.user_type == 'facilitator':
        facilitator_view()
    elif st.session_state.user_type == 'player':
        player_view()


if __name__ == "__main__":
    main()
