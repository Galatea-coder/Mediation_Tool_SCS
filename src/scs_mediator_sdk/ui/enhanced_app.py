"""
Enhanced Mediation Simulation UI

Features:
- Moore's 6-Phase Process Navigation
- Scenario Builder for non-technical users
- Real-time analytics and feedback
- Learning progress tracking
- Professional visualizations
"""

import streamlit as st
import json
import os
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional

# Set page config
st.set_page_config(
    page_title="Advanced Mediation Simulation Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration
API_URL = os.environ.get("SCS_API_URL", "http://localhost:8000")

# Session state initialization
if 'current_phase' not in st.session_state:
    st.session_state.current_phase = 1
if 'scenario_data' not in st.session_state:
    st.session_state.scenario_data = {}
if 'stakeholder_assessment' not in st.session_state:
    st.session_state.stakeholder_assessment = {}
if 'agreement_draft' not in st.session_state:
    st.session_state.agreement_draft = {}
if 'participant_id' not in st.session_state:
    st.session_state.participant_id = "user_001"


# ===== PHASE NAVIGATION =====

def render_phase_navigator():
    """Render Moore's 6-Phase process navigator"""
    st.sidebar.markdown("## 📋 Mediation Process")

    phases = [
        "1️⃣ Initial Contact",
        "2️⃣ Conflict Analysis",
        "3️⃣ Agenda Setting",
        "4️⃣ Option Generation",
        "5️⃣ Bargaining",
        "6️⃣ Implementation"
    ]

    phase_descriptions = [
        "Build relationships and assess readiness",
        "Analyze stakeholders and interests",
        "Define problems and set agenda",
        "Generate creative options",
        "Negotiate and decide",
        "Monitor and ensure compliance"
    ]

    current = st.session_state.current_phase

    # Display all phases with status
    for i, (phase, desc) in enumerate(zip(phases, phase_descriptions), 1):
        if i < current:
            st.sidebar.success(f"✅ {phase}")
        elif i == current:
            st.sidebar.info(f"▶️ **{phase}**")
            st.sidebar.caption(desc)
        else:
            st.sidebar.text(f"⏸️ {phase}")

    st.sidebar.markdown("---")

    # Navigation buttons
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if current > 1:
            if st.button("⬅️ Previous"):
                st.session_state.current_phase -= 1
                st.rerun()
    with col2:
        if current < 6:
            if st.button("Next ➡️"):
                st.session_state.current_phase += 1
                st.rerun()


# ===== SCENARIO BUILDER =====

def render_scenario_builder():
    """User-friendly scenario builder"""
    st.header("🎬 Scenario Builder")
    st.caption("Create your mediation scenario step-by-step")

    # Domain selection
    domain = st.selectbox(
        "Conflict Domain",
        ["Maritime", "Territorial", "Resource", "Political", "Ethnic"],
        help="What type of conflict are you simulating?"
    )

    # Basic info
    col1, col2 = st.columns(2)
    with col1:
        scenario_name = st.text_input("Scenario Name", "My Custom Scenario")
        difficulty = st.select_slider(
            "Difficulty Level",
            options=["Beginner", "Intermediate", "Advanced", "Expert"]
        )
    with col2:
        duration = st.slider("Estimated Duration (minutes)", 30, 180, 60)
        parties_count = st.number_input("Number of Parties", 2, 6, 2)

    # Parties
    st.subheader("Define Parties")
    parties = {}
    for i in range(int(parties_count)):
        with st.expander(f"Party {i+1}"):
            party_id = st.text_input(f"Party ID", f"party_{i+1}", key=f"pid_{i}")
            party_name = st.text_input(f"Display Name", f"Party {i+1}", key=f"pname_{i}")
            party_type = st.selectbox(
                f"Type",
                ["Government", "Rebel Group", "Civil Society", "Business", "Regional Org"],
                key=f"ptype_{i}"
            )
            power = st.slider(f"Power Level", 0.0, 1.0, 0.5, key=f"power_{i}")
            parties[party_id] = {
                'name': party_name,
                'type': party_type,
                'power': power
            }

    # Issues
    st.subheader("Define Negotiable Issues")
    issues_count = st.number_input("Number of Issues", 1, 8, 3)
    issues = {}

    for i in range(int(issues_count)):
        with st.expander(f"Issue {i+1}"):
            issue_id = st.text_input(f"Issue ID", f"issue_{i+1}", key=f"iid_{i}")
            issue_name = st.text_input(f"Display Name", f"Issue {i+1}", key=f"iname_{i}")
            issue_type = st.selectbox(
                f"Type",
                ["Distributive (Fixed Pie)", "Integrative (Expandable)", "Procedural", "Symbolic"],
                key=f"itype_{i}"
            )
            issues[issue_id] = {
                'name': issue_name,
                'type': issue_type
            }

    if st.button("💾 Save Scenario Template"):
        scenario_template = {
            'domain': domain,
            'name': scenario_name,
            'difficulty': difficulty,
            'duration': duration,
            'parties': parties,
            'issues': issues
        }
        st.session_state.scenario_data = scenario_template
        st.success("✅ Scenario template saved!")
        st.json(scenario_template)


# ===== PHASE COMPONENTS =====

def render_phase_1():
    """Phase 1: Initial Contact & Relationship Building"""
    st.header("Phase 1: Initial Contact & Relationship Building")

    st.markdown("""
    **Objectives:**
    - Establish mediator credibility
    - Build trust with parties
    - Assess readiness for mediation
    - Explain the process
    """)

    with st.expander("🎯 Ripeness Assessment"):
        st.markdown("**Zartman's Ripeness Theory**: Is the conflict ripe for resolution?")

        col1, col2 = st.columns(2)
        with col1:
            hurting_stalemate = st.checkbox("Mutually Hurting Stalemate exists")
            recent_catastrophe = st.checkbox("Recent catastrophic event")
        with col2:
            impending_disaster = st.checkbox("Impending catastrophe visible")
            way_out = st.checkbox("Way out is visible to parties")

        if hurting_stalemate and way_out:
            st.success("✅ Conflict appears RIPE for mediation")
        elif hurting_stalemate or way_out:
            st.warning("⚠️ Possibly ready - proceed with caution")
        else:
            st.error("❌ NOT READY - mediation likely to fail")

    with st.expander("👥 Stakeholder Mapping"):
        st.markdown("Identify all stakeholders and their interests")

        # Quick stakeholder entry
        stakeholder_name = st.text_input("Stakeholder Name")
        stakeholder_role = st.selectbox("Role", ["Primary Party", "Secondary Party", "Influencer", "Observer"])

        if st.button("Add Stakeholder"):
            if stakeholder_name:
                if 'stakeholders' not in st.session_state.stakeholder_assessment:
                    st.session_state.stakeholder_assessment['stakeholders'] = []

                st.session_state.stakeholder_assessment['stakeholders'].append({
                    'name': stakeholder_name,
                    'role': stakeholder_role
                })
                st.success(f"Added: {stakeholder_name}")

        # Display stakeholders
        if 'stakeholders' in st.session_state.stakeholder_assessment:
            st.dataframe(pd.DataFrame(st.session_state.stakeholder_assessment['stakeholders']))


def render_phase_2():
    """Phase 2: Data Collection & Conflict Analysis"""
    st.header("Phase 2: Data Collection & Conflict Analysis")

    st.markdown("""
    **Objectives:**
    - Identify positions vs. interests
    - Analyze power dynamics
    - Understand cultural context
    - Map relationships
    """)

    tabs = st.tabs(["Positions & Interests", "Power Analysis", "Cultural Context", "Relationship Map"])

    with tabs[0]:
        st.subheader("Positions vs. Interests")
        st.info("💡 Tip: Positions are what people say they want. Interests are WHY they want it.")

        party_select = st.selectbox("Select Party", ["Party A", "Party B", "Party C"])

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Stated Position**")
            position = st.text_area("What do they say they want?", key="position")
        with col2:
            st.markdown("**Underlying Interests**")
            interests = st.text_area("WHY do they want it?", key="interests",
                                    placeholder="Security, economy, reputation, sovereignty...")

    with tabs[1]:
        st.subheader("Power Dynamics")

        parties_to_analyze = ["Party A", "Party B", "Party C"]
        power_data = []

        for party in parties_to_analyze:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text(party)
            with col2:
                military = st.slider(f"Military", 0.0, 1.0, 0.5, key=f"mil_{party}")
            with col3:
                economic = st.slider(f"Economic", 0.0, 1.0, 0.5, key=f"econ_{party}")

            power_data.append({'party': party, 'military': military, 'economic': economic})

        # Visualize power
        df_power = pd.DataFrame(power_data)
        fig = go.Figure(data=[
            go.Bar(name='Military', x=df_power['party'], y=df_power['military']),
            go.Bar(name='Economic', x=df_power['party'], y=df_power['economic'])
        ])
        fig.update_layout(title="Power Distribution", barmode='group')
        st.plotly_chart(fig)


    with tabs[2]:
        st.subheader("Cultural Context")

        culture_type = st.select_slider(
            "Cultural Orientation",
            options=["Highly Individualist", "Individualist", "Neutral", "Collectivist", "Highly Collectivist"]
        )

        face_sensitivity = st.slider("Face-Saving Importance", 0.0, 1.0, 0.5)
        time_orientation = st.radio("Time Orientation", ["Short-term", "Long-term"])

        if face_sensitivity > 0.7:
            st.warning("⚠️ High face sensitivity - use indirect communication, private caucuses")


def render_phase_3():
    """Phase 3: Problem Definition & Agenda Setting"""
    st.header("Phase 3: Problem Definition & Agenda Setting")

    st.markdown("""
    **Objectives:**
    - Reframe positions as interests
    - Sequence issues strategically
    - Establish ground rules
    - Identify non-negotiables
    """)

    tabs = st.tabs(["Reframing", "Issue Sequencing", "Ground Rules"])

    with tabs[0]:
        st.subheader("Reframe Positions to Interests")

        st.text_input("Position Statement", placeholder="We must control the entire territory")

        if st.button("🎨 Generate Interest Reframes"):
            st.markdown("**Possible Underlying Interests:**")
            st.markdown("- Security concerns about border defense")
            st.markdown("- Economic access to resources")
            st.markdown("- Historical/symbolic importance")
            st.markdown("- Domestic political pressures")

    with tabs[1]:
        st.subheader("Strategic Issue Sequencing")

        sequencing_strategy = st.selectbox(
            "Sequencing Strategy",
            [
                "Easy to Hard (Build momentum)",
                "Hard to Easy (Clear major obstacle first)",
                "Logrolling (Link issues for trades)",
                "Parallel Tracks (Address simultaneously)"
            ]
        )

        st.info(f"💡 {sequencing_strategy}")


def render_phase_4():
    """Phase 4: Option Generation & Reality Testing"""
    st.header("Phase 4: Option Generation & Reality Testing")

    st.markdown("""
    **Objectives:**
    - Generate creative options
    - Expand the pie (integrative potential)
    - Reality test options
    - Build package deals
    """)

    tabs = st.tabs(["Brainstorm", "Option Analysis", "Reality Testing"])

    with tabs[0]:
        st.subheader("Creative Option Generation")

        technique = st.selectbox(
            "Generation Technique",
            [
                "Expand the Pie (Integrative)",
                "Split the Difference (Distributive)",
                "Phased Approach (Time dimension)",
                "Contingent Agreement (Conditional)",
                "Third-Party Guarantor"
            ]
        )

        option_name = st.text_input("Option Name")
        option_desc = st.text_area("Description")

        if st.button("💡 Add Option"):
            if 'options' not in st.session_state.agreement_draft:
                st.session_state.agreement_draft['options'] = []

            st.session_state.agreement_draft['options'].append({
                'name': option_name,
                'description': option_desc,
                'technique': technique
            })
            st.success("Option added!")

    with tabs[2]:
        st.subheader("Reality Testing")

        st.markdown("**Test each option against these criteria:**")

        col1, col2 = st.columns(2)
        with col1:
            feasibility = st.slider("Feasibility (Can it be implemented?)", 0.0, 1.0, 0.5)
            durability = st.slider("Durability (Will it last?)", 0.0, 1.0, 0.5)
        with col2:
            fairness = st.slider("Fairness (Is it equitable?)", 0.0, 1.0, 0.5)
            efficiency = st.slider("Efficiency (Pareto optimal?)", 0.0, 1.0, 0.5)

        avg_score = (feasibility + durability + fairness + efficiency) / 4

        if avg_score >= 0.75:
            st.success(f"✅ Strong option (Score: {avg_score:.1%})")
        elif avg_score >= 0.5:
            st.warning(f"⚠️ Moderate option (Score: {avg_score:.1%}) - needs refinement")
        else:
            st.error(f"❌ Weak option (Score: {avg_score:.1%}) - reconsider")


def render_phase_5():
    """Phase 5: Bargaining & Decision Making"""
    st.header("Phase 5: Bargaining & Decision Making")

    # Load scenario
    case_dir = "cases/scs"
    scenario_files = [f for f in os.listdir(case_dir) if f.endswith(".json")]
    scenario = st.selectbox("Select Scenario", scenario_files if scenario_files else ["(none)"])

    if scenario != "(none)":
        with open(os.path.join(case_dir, scenario), "r") as f:
            case = json.load(f)
        st.json(case)

    # Offer builder
    st.subheader("Build Agreement Offer")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Resupply Procedures**")
        standoff = st.slider("Standoff Distance (nm)", 0, 10, 3)
        escorts = st.slider("Escort Count", 0, 5, 1)
    with col2:
        st.markdown("**Communication Protocol**")
        hotline = st.selectbox("Hotline Status", ["ad_hoc", "24/7"])
        notification = st.slider("Pre-notification (hours)", 0, 48, 12)

    offer = {
        "resupply_SOP": {"standoff_nm": standoff, "escort_count": escorts, "pre_notification_hours": notification},
        "hotline_cues": {"hotline_status": hotline, "cues_checklist": ["distance", "AIS_on"]}
    }

    if st.button("📊 Evaluate Offer"):
        try:
            response = requests.post(
                f"{API_URL}/bargain/demo_case/offer",
                json={"proposer_party_id": "PH_GOV", "agreement_vector": offer},
                timeout=30
            )
            results = response.json()

            st.subheader("Evaluation Results")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Utilities**")
                for party, util in results['utilities'].items():
                    st.metric(party, f"{util:.2%}")

            with col2:
                st.markdown("**Acceptance Probabilities**")
                for party, prob in results['acceptance_prob'].items():
                    st.metric(party, f"{prob:.2%}")

        except Exception as e:
            st.error(f"Error evaluating offer: {e}")


def render_phase_6():
    """Phase 6: Implementation & Monitoring"""
    st.header("Phase 6: Implementation & Monitoring")

    st.markdown("""
    **Objectives:**
    - Define implementation steps
    - Establish monitoring mechanisms
    - Create dispute resolution procedures
    - Set review milestones
    """)

    tabs = st.tabs(["Implementation Plan", "Monitoring Dashboard", "Dispute Resolution"])

    with tabs[0]:
        st.subheader("Implementation Timeline")

        milestone = st.text_input("Milestone")
        deadline = st.date_input("Deadline")
        responsible = st.text_input("Responsible Party")

        if st.button("Add Milestone"):
            st.success(f"Added: {milestone} - {deadline}")

    with tabs[1]:
        st.subheader("Monitoring Dashboard")

        # Simulate monitoring data
        st.metric("Compliance Rate", "85%", "5%")
        st.metric("Incidents (Last 30 Days)", "3", "-2")
        st.metric("Communication Events", "15", "5")


# ===== MAIN APP =====

def main():
    """Main application"""
    st.title("🕊️ Advanced Mediation Simulation Tool")
    st.caption("Interactive training for conflict mediators and peacemakers")

    # Render phase navigator
    render_phase_navigator()

    # Main content area
    current_phase = st.session_state.current_phase

    if current_phase == 1:
        render_phase_1()
    elif current_phase == 2:
        render_phase_2()
    elif current_phase == 3:
        render_phase_3()
    elif current_phase == 4:
        render_phase_4()
    elif current_phase == 5:
        render_phase_5()
    elif current_phase == 6:
        render_phase_6()

    # Bottom navigation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🏠 Home"):
            st.session_state.current_phase = 1
            st.rerun()
    with col3:
        if st.button("📊 View Analytics"):
            st.info("Analytics dashboard coming soon!")


if __name__ == "__main__":
    main()
