#!/usr/bin/env python3
"""
Peace Mediation Tools UI for SCS Mediator SDK v2

This UI integrates all 10 peace mediation enhancements into a practical,
easy-to-use interface for mediators and instructors.

Enhanced Features:
1. Escalation Assessment (escalation_ladder.py)
2. CBM Recommendations (cbm_library.py)
3. Domestic Politics Analysis (domestic_constraints.py)
4. Multi-Track Coordination (multi_track.py)
5. Spoiler Management (spoiler_management.py)

UI Design Principles:
- Dark text (#000 or #333) on light backgrounds for readability
- Clear visual hierarchy with proper contrast
- Practical tools that provide actionable insights
- Real-time assessment and recommendations
"""

import streamlit as st
import json
import os
import sys
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# Import peace mediation modules
from scs_mediator_sdk.dynamics.escalation_ladder import (
    EscalationManager, EscalationLevel
)
from scs_mediator_sdk.peacebuilding.cbm_library import (
    CBMLibrary, CBMCategory
)
from scs_mediator_sdk.politics.domestic_constraints import (
    WinSetAnalyzer, DomesticActor, create_philippines_domestic_actors,
    create_china_domestic_actors
)
from scs_mediator_sdk.diplomacy.multi_track import (
    MultiTrackMediator, DiplomaticTrack
)
from scs_mediator_sdk.peacebuilding.spoiler_management import (
    SpoilerManager, create_scs_spoilers, SpoilerType, SpoilerCapability
)

# ==================== CONFIGURATION ====================

# Color scheme for high contrast and readability
COLORS = {
    'text_dark': '#000000',
    'text_medium': '#333333',
    'background_light': '#FFFFFF',
    'background_info': '#E3F2FD',      # Light blue
    'background_success': '#E8F5E9',   # Light green
    'background_warning': '#FFF3E0',   # Light orange
    'background_error': '#FFEBEE',     # Light red
    'border_info': '#2196F3',
    'border_success': '#4CAF50',
    'border_warning': '#FF9800',
    'border_error': '#F44336',
}

# Custom CSS for proper contrast
CUSTOM_CSS = f"""
<style>
    /* Force dark text on light backgrounds */
    .stMarkdown, .stText, p, li, span {{
        color: {COLORS['text_dark']} !important;
    }}

    /* Info boxes with dark text */
    .info-box {{
        background-color: {COLORS['background_info']};
        border-left: 5px solid {COLORS['border_info']};
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }}

    .info-box h3, .info-box h4, .info-box p, .info-box li {{
        color: {COLORS['text_dark']} !important;
    }}

    /* Success boxes */
    .success-box {{
        background-color: {COLORS['background_success']};
        border-left: 5px solid {COLORS['border_success']};
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }}

    .success-box h3, .success-box h4, .success-box p, .success-box li {{
        color: {COLORS['text_dark']} !important;
    }}

    /* Warning boxes */
    .warning-box {{
        background-color: {COLORS['background_warning']};
        border-left: 5px solid {COLORS['border_warning']};
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }}

    .warning-box h3, .warning-box h4, .warning-box p, .warning-box li {{
        color: {COLORS['text_dark']} !important;
    }}

    /* Error boxes */
    .error-box {{
        background-color: {COLORS['background_error']};
        border-left: 5px solid {COLORS['border_error']};
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }}

    .error-box h3, .error-box h4, .error-box p, .error-box li {{
        color: {COLORS['text_dark']} !important;
    }}

    /* Metric cards */
    .metric-card {{
        background-color: #F5F5F5;
        border: 2px solid #DDDDDD;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }}

    .metric-card h2, .metric-card h3, .metric-card p {{
        color: {COLORS['text_dark']} !important;
    }}

    .metric-value {{
        font-size: 36px;
        font-weight: bold;
        color: {COLORS['text_dark']} !important;
    }}

    .metric-label {{
        font-size: 14px;
        color: {COLORS['text_medium']} !important;
        margin-top: 5px;
    }}

    /* Escalation ladder visualization */
    .escalation-level {{
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        font-weight: bold;
        color: {COLORS['text_dark']} !important;
    }}

    .escalation-low {{
        background-color: #C8E6C9;
        border-left: 5px solid #4CAF50;
    }}

    .escalation-medium {{
        background-color: #FFF9C4;
        border-left: 5px solid #FFC107;
    }}

    .escalation-high {{
        background-color: #FFCCBC;
        border-left: 5px solid #FF5722;
    }}

    .escalation-critical {{
        background-color: #FFCDD2;
        border-left: 5px solid #F44336;
    }}

    /* CBM cards */
    .cbm-card {{
        background-color: #FAFAFA;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }}

    .cbm-card h4, .cbm-card p, .cbm-card li {{
        color: {COLORS['text_dark']} !important;
    }}

    /* Spoiler cards */
    .spoiler-card {{
        background-color: #FFF3E0;
        border: 2px solid #FF9800;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }}

    .spoiler-card h4, .spoiler-card p, .spoiler-card li {{
        color: {COLORS['text_dark']} !important;
    }}
</style>
"""

# ==================== SESSION STATE ====================

def init_session_state():
    """Initialize session state variables"""
    if 'escalation_manager' not in st.session_state:
        st.session_state.escalation_manager = EscalationManager()

    if 'cbm_library' not in st.session_state:
        st.session_state.cbm_library = CBMLibrary()

    if 'philippines_analyzer' not in st.session_state:
        st.session_state.philippines_analyzer = WinSetAnalyzer("Philippines")
        for constraint in create_philippines_domestic_actors():
            st.session_state.philippines_analyzer.add_domestic_actor(constraint)

    if 'china_analyzer' not in st.session_state:
        st.session_state.china_analyzer = WinSetAnalyzer("China")
        for constraint in create_china_domestic_actors():
            st.session_state.china_analyzer.add_domestic_actor(constraint)

    if 'multitrack_mediator' not in st.session_state:
        st.session_state.multitrack_mediator = MultiTrackMediator()

    if 'spoiler_manager' not in st.session_state:
        st.session_state.spoiler_manager = SpoilerManager()
        for spoiler in create_scs_spoilers():
            st.session_state.spoiler_manager.add_spoiler(spoiler)

# ==================== ESCALATION ASSESSMENT ====================

def show_escalation_assessment():
    """Display escalation assessment tools"""
    st.markdown("### 📊 Escalation Risk Assessment")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Current escalation level
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("#### Current Escalation Level")

    current_level = st.session_state.escalation_manager.current_level
    level_num = int(current_level.name.split('_')[1])

    # Display escalation ladder
    for level in EscalationLevel:
        level_value = int(level.name.split('_')[1])
        if level_value <= 3:
            css_class = "escalation-low"
        elif level_value <= 5:
            css_class = "escalation-medium"
        elif level_value <= 7:
            css_class = "escalation-high"
        else:
            css_class = "escalation-critical"

        indicator = "→" if level_value == level_num else " "
        st.markdown(
            f'<div class="escalation-level {css_class}">'
            f'{indicator} Level {level_value}: {level.value.replace("_", " ").title()}'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Assess proposed action
    st.markdown("---")
    st.markdown("#### Assess Proposed Action")

    col1, col2 = st.columns([3, 1])
    with col1:
        proposed_action = st.text_area(
            "Describe the proposed action:",
            placeholder="E.g., 'Deploy naval vessels to disputed waters' or 'Conduct joint coast guard patrol'",
            height=100,
            key="escalation_action"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        assess_button = st.button("🔍 Assess Risk", type="primary", use_container_width=True)

    if assess_button and proposed_action:
        risk = st.session_state.escalation_manager.assess_escalation_risk(proposed_action)

        # Display risk level
        risk_level = risk['risk_level']
        if risk_level < 0.3:
            risk_color = "success-box"
            risk_label = "LOW RISK"
        elif risk_level < 0.6:
            risk_color = "warning-box"
            risk_label = "MODERATE RISK"
        else:
            risk_color = "error-box"
            risk_label = "HIGH RISK"

        st.markdown(f'<div class="{risk_color}">', unsafe_allow_html=True)
        st.markdown(f"### Risk Level: {risk_label} ({risk_level:.0%})")
        st.markdown('</div>', unsafe_allow_html=True)

        # Likely counter-escalation
        if risk['likely_counter_escalation']:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Likely Counter-Escalation:")
            for response in risk['likely_counter_escalation']:
                st.markdown(f"- {response}")
            st.markdown('</div>', unsafe_allow_html=True)

        # De-escalation windows
        if risk['de_escalation_windows']:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("#### ✅ De-escalation Options Available:")
            for option in risk['de_escalation_windows']:
                st.markdown(f"- {option}")
            st.markdown('</div>', unsafe_allow_html=True)

        # Point of no return warning
        if risk['point_of_no_return']:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.markdown("#### 🚨 WARNING: Past Point of No Return")
            st.markdown("This escalation level is extremely difficult to reverse. Immediate de-escalation is critical.")
            st.markdown('</div>', unsafe_allow_html=True)

    # De-escalation sequence
    st.markdown("---")
    st.markdown("#### Recommended De-escalation Sequence")
    st.markdown("Based on Osgood's GRIT (Graduated Reciprocation in Tension-reduction)")

    sequence = st.session_state.escalation_manager.recommend_de_escalation_sequence()

    for i, step in enumerate(sequence, 1):
        st.markdown(
            f'<div class="info-box">'
            f'<strong style="color: {COLORS["text_dark"]}">Step {i}:</strong> {step}'
            f'</div>',
            unsafe_allow_html=True
        )

# ==================== CBM RECOMMENDATIONS ====================

def show_cbm_recommendations():
    """Display CBM recommendation tools"""
    st.markdown("### 🤝 Confidence-Building Measures")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Input parameters
    col1, col2, col3 = st.columns(3)

    with col1:
        trust_level = st.slider(
            "Current Trust Level",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="0 = No trust, 1 = High trust"
        )

    with col2:
        escalation_level = st.slider(
            "Escalation Level",
            min_value=1,
            max_value=9,
            value=4,
            help="Current position on escalation ladder"
        )

    with col3:
        available_weeks = st.slider(
            "Available Time (weeks)",
            min_value=4,
            max_value=52,
            value=20,
            help="Time available for implementation"
        )

    # Get recommendations
    if st.button("🔍 Get CBM Recommendations", type="primary", use_container_width=True):
        recommendations = st.session_state.cbm_library.recommend_cbm_sequence(
            current_trust_level=trust_level,
            escalation_level=escalation_level,
            available_time_weeks=available_weeks
        )

        if recommendations:
            st.markdown(f'<div class="success-box">', unsafe_allow_html=True)
            st.markdown(f"### ✅ Recommended {len(recommendations)} CBMs")
            st.markdown('</div>', unsafe_allow_html=True)

            for i, cbm in enumerate(recommendations, 1):
                st.markdown(
                    f'<div class="cbm-card">'
                    f'<h4 style="color: {COLORS["text_dark"]}">CBM {i}: {cbm.name}</h4>'
                    f'<p style="color: {COLORS["text_dark"]}"><strong>Category:</strong> {cbm.category.value.replace("_", " ").title()}</p>'
                    f'<p style="color: {COLORS["text_dark"]}"><strong>Description:</strong> {cbm.description}</p>'
                    f'<p style="color: {COLORS["text_dark"]}"><strong>Timeline:</strong> {cbm.timeline_weeks} weeks</p>'
                    f'<p style="color: {COLORS["text_dark"]}"><strong>Trust Building:</strong> {cbm.trust_building_value:.1f}/1.0</p>'
                    f'<p style="color: {COLORS["text_dark"]}"><strong>Risk Reduction:</strong> {cbm.risk_reduction_value:.1f}/1.0</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                with st.expander(f"📋 Implementation Steps for {cbm.name}"):
                    for step in cbm.implementation_steps:
                        st.markdown(f"- {step}")

                    if cbm.prerequisites:
                        st.markdown("**Prerequisites:**")
                        for prereq in cbm.prerequisites:
                            st.markdown(f"- {prereq}")
        else:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("No CBMs match the current criteria. Consider adjusting parameters.")
            st.markdown('</div>', unsafe_allow_html=True)

    # Browse CBMs by category
    st.markdown("---")
    st.markdown("#### 📚 Browse CBM Library by Category")

    category_choice = st.selectbox(
        "Select Category",
        list(CBMCategory),
        format_func=lambda x: x.value.replace("_", " ").title()
    )

    cbms_in_category = st.session_state.cbm_library.get_cbms_by_category(category_choice)

    st.markdown(f"**{len(cbms_in_category)} CBMs in {category_choice.value.replace('_', ' ').title()} category:**")

    for cbm in cbms_in_category:
        with st.expander(f"📄 {cbm.name}"):
            st.markdown(f"**Description:** {cbm.description}")
            st.markdown(f"**Timeline:** {cbm.timeline_weeks} weeks")
            st.markdown(f"**Trust Building:** {cbm.trust_building_value:.1f}/1.0")
            st.markdown(f"**Risk Reduction:** {cbm.risk_reduction_value:.1f}/1.0")
            st.markdown(f"**Cost:** {cbm.cost_level}")
            st.markdown(f"**Reversibility:** {cbm.reversibility}")

# ==================== DOMESTIC POLITICS ====================

def show_domestic_politics():
    """Display domestic politics analysis tools"""
    st.markdown("### 🏛️ Domestic Politics Analysis")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Party selection
    party_choice = st.radio(
        "Select Party to Analyze",
        ["Philippines", "China"],
        horizontal=True
    )

    analyzer = (st.session_state.philippines_analyzer
                if party_choice == "Philippines"
                else st.session_state.china_analyzer)

    # Show win-set size
    st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{analyzer.win_set_size:.0%}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Win-Set Size (Negotiating Flexibility)</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if analyzer.win_set_size < 0.4:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.markdown("⚠️ **Highly Constrained:** This party has very limited room to maneuver due to domestic pressures.")
        st.markdown('</div>', unsafe_allow_html=True)
    elif analyzer.win_set_size < 0.7:
        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
        st.markdown("⚠️ **Moderately Constrained:** Domestic politics will limit flexibility in negotiations.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("✅ **Good Flexibility:** This party has reasonable room to negotiate.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Show deal breakers
    st.markdown("---")
    st.markdown("#### 🚫 Domestic Deal Breakers")

    deal_breakers = analyzer.identify_deal_breakers()
    if deal_breakers:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.markdown("These issues are absolute red lines due to domestic politics:")
        for breaker in deal_breakers:
            st.markdown(f"- {breaker}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("No absolute deal breakers identified - negotiations have flexibility.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Test a proposal
    st.markdown("---")
    st.markdown("#### 🧪 Test Domestic Acceptability")
    st.markdown("Enter values for key negotiation issues (0-1 scale):")

    col1, col2, col3 = st.columns(3)

    with col1:
        fisheries_access = st.slider(
            "Fisheries Access",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.1,
            help="Access to fishing grounds"
        )

    with col2:
        sovereignty_language = st.slider(
            "Sovereignty Language",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1,
            help="Strength of sovereignty claims"
        )

    with col3:
        bilateral_tensions = st.slider(
            "Bilateral Tensions",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Level of tensions"
        )

    if st.button("🔍 Test Proposal", type="primary", use_container_width=True):
        proposed_deal = {
            "fisheries_access": fisheries_access,
            "sovereignty_language": sovereignty_language,
            "bilateral_tensions": bilateral_tensions
        }

        result = analyzer.test_domestic_acceptability(proposed_deal)

        # Overall result
        if result['acceptable']:
            st.markdown(f'<div class="success-box">', unsafe_allow_html=True)
            st.markdown(f"### ✅ ACCEPTABLE")
            st.markdown(f"Ratification Probability: **{result['ratification_probability']:.0%}**")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-box">', unsafe_allow_html=True)
            st.markdown(f"### ❌ UNACCEPTABLE")
            st.markdown(f"Ratification Probability: **{result['ratification_probability']:.0%}**")
            st.markdown('</div>', unsafe_allow_html=True)

        # Support metrics
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{result["overall_support"]:.0%}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-label">Overall Domestic Support</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{len(result["objectors"])}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-label">Number of Objectors</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Show objectors
        if result['objectors']:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Domestic Objectors:")
            for obj in result['objectors']:
                st.markdown(f"- **{obj['actor']}**: {obj['issue']} (requires {obj['required']}, proposed {obj['proposed']})")
            st.markdown('</div>', unsafe_allow_html=True)

        # Show required compensations
        if result['required_compensations']:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("#### 💰 Required Compensations to Build Support:")
            for comp in result['required_compensations']:
                st.markdown(f"- {comp}")
            st.markdown('</div>', unsafe_allow_html=True)

        # Ratification strategy
        st.markdown("---")
        st.markdown("#### 📋 Recommended Ratification Strategy")
        strategy = analyzer.suggest_ratification_strategy(proposed_deal)

        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        for step in strategy:
            st.markdown(f"{step}")
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== MULTI-TRACK DIPLOMACY ====================

def show_multi_track():
    """Display multi-track diplomacy tools"""
    st.markdown("### 🌐 Multi-Track Diplomacy Coordination")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Phase selection
    st.markdown("#### Select Conflict Phase")
    phase = st.radio(
        "Current Phase:",
        ["pre_negotiation", "negotiation", "implementation"],
        format_func=lambda x: x.replace("_", " ").title(),
        horizontal=True
    )

    # Get recommendations
    recommendations = st.session_state.multitrack_mediator.recommend_track_sequence(phase)

    st.markdown(f'<div class="info-box">', unsafe_allow_html=True)
    st.markdown(f"### Recommended Tracks for {phase.replace('_', ' ').title()} Phase")
    st.markdown(f"**{len(recommendations)} track activities recommended**")
    st.markdown('</div>', unsafe_allow_html=True)

    # Display each recommendation
    for i, rec in enumerate(recommendations, 1):
        st.markdown(
            f'<div class="cbm-card">'
            f'<h4 style="color: {COLORS["text_dark"]}">Track {i}: {rec["track"].value.replace("_", " ").title()}</h4>'
            f'<p style="color: {COLORS["text_dark"]}"><strong>Activity:</strong> {rec["activity"]}</p>'
            f'<p style="color: {COLORS["text_dark"]}"><strong>Purpose:</strong> {rec["purpose"]}</p>'
            f'<p style="color: {COLORS["text_dark"]}"><strong>Participants:</strong> {rec["participants"]}</p>'
            f'<p style="color: {COLORS["text_dark"]}"><strong>Timeline:</strong> {rec["timeline"]}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    # Track overview
    st.markdown("---")
    st.markdown("#### 📊 Diplomatic Track Overview")

    track_info = {
        "Track 1": "Official government negotiations",
        "Track 1.5": "Semi-official consultations (retired officials, advisors)",
        "Track 2": "Unofficial dialogue (academics, NGOs, think tanks)",
        "Track 3": "Business community engagement",
        "Track 4": "People-to-people exchanges",
        "Track 5": "Training and education programs",
        "Track 6": "Peace activism and NGOs",
        "Track 7": "Faith-based initiatives",
        "Track 8": "Funding and donor coordination",
        "Track 9": "Media and communications"
    }

    col1, col2 = st.columns(2)

    for i, (track, description) in enumerate(track_info.items()):
        with col1 if i % 2 == 0 else col2:
            with st.expander(f"📍 {track}"):
                st.markdown(f"**{description}**")

                if "Official" in description or "Semi-official" in description:
                    st.markdown("- High visibility")
                    st.markdown("- Binding commitments")
                    st.markdown("- Political accountability")
                else:
                    st.markdown("- Lower visibility")
                    st.markdown("- Flexibility to explore options")
                    st.markdown("- Builds relationships and trust")

    # Coordination mechanisms
    st.markdown("---")
    st.markdown("#### 🔗 Track Coordination Mechanisms")

    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    **Essential Coordination Practices:**
    - Regular briefings from Track 2 to Track 1 negotiators
    - Shared knowledge management system across tracks
    - Coordinated messaging to avoid contradictions
    - Conflict-sensitive approach to timing and sequencing
    - Clear roles and responsibilities for each track
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== SPOILER MANAGEMENT ====================

def show_spoiler_management():
    """Display spoiler management tools"""
    st.markdown("### ⚠️ Spoiler Management")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Overview
    spoilers = st.session_state.spoiler_manager.spoilers

    st.markdown(f'<div class="warning-box">', unsafe_allow_html=True)
    st.markdown(f"### {len(spoilers)} Potential Spoilers Identified")
    st.markdown("Spoilers are actors who may threaten or undermine the peace process")
    st.markdown('</div>', unsafe_allow_html=True)

    # Display each spoiler
    for name, spoiler in spoilers.items():
        # Color code by threat level
        if spoiler.capability.value == "high":
            card_class = "error-box"
            threat_emoji = "🚨"
        elif spoiler.capability.value == "medium":
            card_class = "warning-box"
            threat_emoji = "⚠️"
        else:
            card_class = "info-box"
            threat_emoji = "ℹ️"

        st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
        st.markdown(f"### {threat_emoji} {name}")
        st.markdown(f"**Type:** {spoiler.spoiler_type.value.title()}")
        st.markdown(f"**Capability:** {spoiler.capability.value.title()}")
        st.markdown(f"**Position:** {spoiler.position.value.title()}")
        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander(f"📋 Detailed Analysis: {name}"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Interests Threatened:**")
                for interest in spoiler.interests_threatened:
                    st.markdown(f"- {interest}")

                st.markdown("**Benefits from Conflict:**")
                for benefit in spoiler.benefits_from_conflict:
                    st.markdown(f"- {benefit}")

            with col2:
                st.markdown("**Typical Spoiling Actions:**")
                for action in spoiler.typical_spoiling_actions[:3]:
                    st.markdown(f"- {action}")

                st.markdown("**Dependencies/Vulnerabilities:**")
                for dep in spoiler.dependencies:
                    st.markdown(f"- {dep}")

            # Show recommended strategies
            st.markdown("---")
            st.markdown("**Recommended Management Strategies:**")
            strategies = st.session_state.spoiler_manager.mitigation_strategies.get(name, [])
            for strategy in strategies:
                st.markdown(f"- {strategy}")

    # Assess spoiling risk for a proposal
    st.markdown("---")
    st.markdown("#### 🧪 Assess Spoiling Risk for Proposed Agreement")

    col1, col2, col3 = st.columns(3)

    with col1:
        shared_resources = st.checkbox("Shared Resources", value=True)

    with col2:
        monitoring = st.checkbox("Joint Monitoring", value=True)

    with col3:
        demilitarization = st.checkbox("Demilitarization", value=False)

    if st.button("🔍 Assess Spoiling Risk", type="primary", use_container_width=True):
        agreement = {
            "shared_resources": shared_resources,
            "monitoring": monitoring,
            "demilitarization": demilitarization
        }

        risk = st.session_state.spoiler_manager.assess_spoiling_risk(agreement)

        # Overall risk
        if risk['overall_risk'] < 0.4:
            risk_box = "success-box"
            risk_label = "LOW"
        elif risk['overall_risk'] < 0.7:
            risk_box = "warning-box"
            risk_label = "MODERATE"
        else:
            risk_box = "error-box"
            risk_label = "HIGH"

        st.markdown(f'<div class="{risk_box}">', unsafe_allow_html=True)
        st.markdown(f"### Overall Spoiling Risk: {risk_label} ({risk['overall_risk']:.0%})")
        st.markdown('</div>', unsafe_allow_html=True)

        # High threat spoilers
        if risk['high_threat_spoilers']:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.markdown("#### 🚨 High-Threat Spoilers:")
            for spoiler_name in risk['high_threat_spoilers']:
                st.markdown(f"- {spoiler_name}")
            st.markdown('</div>', unsafe_allow_html=True)

        # Likely spoiling actions
        if risk['likely_spoiling_actions']:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Likely Spoiling Actions:")
            unique_actions = list(set(risk['likely_spoiling_actions']))[:5]
            for action in unique_actions:
                st.markdown(f"- {action}")
            st.markdown('</div>', unsafe_allow_html=True)

        # Protective measures
        if risk['protective_measures_needed']:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("#### 🛡️ Recommended Protective Measures:")
            for measure in risk['protective_measures_needed']:
                st.markdown(f"- {measure}")
            st.markdown('</div>', unsafe_allow_html=True)

    # Spoiler management plan
    st.markdown("---")
    if st.button("📋 Generate Comprehensive Spoiler Management Plan", use_container_width=True):
        plan = st.session_state.spoiler_manager.design_spoiler_management_plan()

        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### 📋 Spoiler Management Plan")

        st.markdown("#### Immediate Actions:")
        for action in plan['immediate_actions']:
            st.markdown(f"- {action}")

        st.markdown("#### Ongoing Monitoring:")
        for monitor in plan['ongoing_monitoring']:
            st.markdown(f"- {monitor}")

        st.markdown("#### Success Indicators:")
        for indicator in plan['success_indicators']:
            st.markdown(f"- {indicator}")

        st.markdown('</div>', unsafe_allow_html=True)

# ==================== MAIN APPLICATION ====================

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Peace Mediation Tools - SCS Mediator SDK",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Initialize session state
    init_session_state()

    # Title
    st.title("🕊️ Peace Mediation Tools")
    st.markdown("**SCS Mediator SDK v2 - Enhanced Peace Mediation Interface**")
    st.markdown("---")

    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        st.markdown("Select a peace mediation tool:")

        tool_choice = st.radio(
            "Peace Mediation Tools:",
            [
                "📊 Escalation Assessment",
                "🤝 CBM Recommendations",
                "🏛️ Domestic Politics",
                "🌐 Multi-Track Diplomacy",
                "⚠️ Spoiler Management"
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")

        st.markdown("### ℹ️ About")
        st.markdown("""
        This interface integrates 10 peace mediation enhancements:

        1. **Escalation Ladder** - Herman Kahn's escalation dynamics
        2. **CBM Library** - Maritime-specific confidence-building measures
        3. **Domestic Constraints** - Putnam's two-level game theory
        4. **Multi-Track** - McDonald & Diamond's multi-track diplomacy
        5. **Spoiler Management** - Stedman's spoiler problem framework
        """)

        st.markdown("---")

        st.markdown("### 📚 Quick Guide")
        st.markdown("""
        **Escalation Assessment**
        - Monitor current escalation level
        - Assess risk of proposed actions
        - Get de-escalation sequences

        **CBM Recommendations**
        - Get sequenced CBM recommendations
        - Browse CBM library
        - Assess implementation feasibility

        **Domestic Politics**
        - Test domestic acceptability
        - Identify deal breakers
        - Get ratification strategies

        **Multi-Track**
        - Coordinate diplomatic tracks
        - Phase-specific recommendations
        - Track integration guidance

        **Spoiler Management**
        - Identify potential spoilers
        - Assess spoiling risk
        - Get management strategies
        """)

    # Main content area
    if tool_choice == "📊 Escalation Assessment":
        show_escalation_assessment()
    elif tool_choice == "🤝 CBM Recommendations":
        show_cbm_recommendations()
    elif tool_choice == "🏛️ Domestic Politics":
        show_domestic_politics()
    elif tool_choice == "🌐 Multi-Track Diplomacy":
        show_multi_track()
    elif tool_choice == "⚠️ Spoiler Management":
        show_spoiler_management()

if __name__ == "__main__":
    main()
