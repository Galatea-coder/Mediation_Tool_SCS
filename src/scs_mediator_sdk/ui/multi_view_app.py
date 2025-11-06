#!/usr/bin/env python3
"""
Multi-View Training Simulation Interface
- Instructor Console (full visibility)
- Party-Specific Views (limited information)
"""

import streamlit as st
import json
import os
import requests
from typing import Optional

# Configuration
API_URL = os.environ.get("SCS_API_URL", "http://localhost:8000")

def init_session_state():
    """Initialize session state variables"""
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None
    if 'current_offer' not in st.session_state:
        st.session_state.current_offer = None
    if 'live_mode' not in st.session_state:
        st.session_state.live_mode = False

def role_selection_page():
    """Landing page for role selection"""
    st.title("🌊 South China Sea Mediation Simulation")
    st.markdown("### Role Selection")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👨‍🏫 Instructor/Facilitator")
        st.markdown("""
        **Full Control Console:**
        - Select and configure scenarios
        - See all parties' utilities and probabilities
        - Run simulations and analysis
        - Control session flow
        - Calibrate model parameters
        """)
        if st.button("Enter as Instructor", use_container_width=True):
            st.session_state.user_role = "INSTRUCTOR"
            st.session_state.live_mode = False
            st.rerun()

    with col2:
        st.subheader("🎭 Negotiating Party")
        st.markdown("""
        **Party-Specific View:**
        - See your own position and interests
        - View current proposals
        - Make counter-offers
        - Limited information (realistic negotiation)
        """)

        party_choice = st.selectbox(
            "Select Your Party",
            ["PH_GOV", "PRC_MARITIME", "VN_CG", "MY_CG"],
            format_func=lambda x: {
                "PH_GOV": "🇵🇭 Philippines Government",
                "PRC_MARITIME": "🇨🇳 PRC Maritime Forces",
                "VN_CG": "🇻🇳 Vietnam Coast Guard",
                "MY_CG": "🇲🇾 Malaysia Coast Guard"
            }.get(x, x)
        )

        if st.button("Enter as Party", use_container_width=True):
            st.session_state.user_role = party_choice
            st.session_state.live_mode = True
            st.rerun()

    st.markdown("---")
    st.info("💡 **Tip**: For solo analysis, choose Instructor. For live training workshops, each participant chooses their assigned party.")

def instructor_console():
    """Full instructor console (complete view)"""
    import pandas as pd

    st.title("SCS Instructor Console — Multi-View Mode")

    # Sidebar with logout
    with st.sidebar:
        st.markdown(f"**Logged in as:** 👨‍🏫 Instructor")
        st.markdown("**Mode:** Full Control")
        st.markdown("---")

        if st.button("🚪 Logout"):
            st.session_state.user_role = None
            st.rerun()

        st.markdown("---")
        st.header("Scenario")

    # Case selection
    case_dir = st.sidebar.text_input("Cases folder", "cases/scs")
    scenario_files = [f for f in os.listdir(case_dir) if f.endswith(".json")] if os.path.exists(case_dir) else []
    scenario = st.sidebar.selectbox("Scenario file", scenario_files if scenario_files else ["(none)"])

    # Sidebar map preview
    map_candidates = []
    if scenario != "(none)":
        stem = os.path.splitext(scenario)[0].lower()
        if os.path.exists('assets/maps'):
            for fn in os.listdir('assets/maps'):
                if stem in fn.lower():
                    map_candidates.append(os.path.join('assets/maps', fn))

    for fn in ['assets/maps/overlay.png', 'assets/maps/map_second_thomas.png']:
        if os.path.exists(fn):
            map_candidates.append(fn)

    if map_candidates:
        st.sidebar.image(map_candidates[0], caption="Scenario Map", use_column_width=True)

    # Load scenario
    if scenario != "(none)":
        with open(os.path.join(case_dir, scenario), "r", encoding="utf-8") as f:
            case = json.load(f)
        st.subheader("Scenario Snapshot")
        st.json(case)
    else:
        case = {"id": "demo_case", "weather_state": "calm", "media_visibility": 2}

    # Start session
    with st.sidebar.expander("Start Session"):
        case_id = case.get("id", "demo_case")
        parties = st.multiselect("Parties", ["PH_GOV", "PRC_MARITIME", "VN_CG", "MY_CG"], default=["PH_GOV", "PRC_MARITIME"])
        mediator = st.text_input("Mediator", "ASEAN_Facilitator")
        issue_space = st.multiselect("Issues", ["resupply_SOP", "hotline_cues", "media_protocol"], default=["resupply_SOP", "hotline_cues", "media_protocol"])

        if st.button("Start Session"):
            payload = {"case_id": case_id, "parties": parties, "mediator": mediator, "issue_space": issue_space}
            try:
                r = requests.post(f"{API_URL}/bargain/sessions", json=payload, timeout=30)
                st.success(r.json())
                st.session_state.session_id = case_id
            except Exception as e:
                st.error(f"Failed to start session: {e}")

    # Main tabs
    tabs = st.tabs(["Offer", "Simulate", "Calibrate", "Live Session Monitor"])

    with tabs[0]:
        st.header("Offer Builder")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Resupply SOP")
            standoff = st.slider("standoff_nm", 0, 6, 3)
            escort = st.slider("escort_count", 0, 3, 1)
            prenotify = st.slider("pre_notification_hours", 0, 24, 12)

        with col2:
            st.subheader("Hotline & CUES")
            hotline = st.selectbox("hotline_status", ["ad_hoc", "24_7"], index=1)
            cues = ["distance", "AIS_on", "video_record"]

        with col3:
            st.subheader("Media Protocol")
            embargo = st.slider("embargo_hours", 0, 24, 6)

        offer = {
            "resupply_SOP": {"standoff_nm": standoff, "escort_count": escort, "pre_notification_hours": prenotify},
            "hotline_cues": {"hotline_status": hotline, "cues_checklist": cues},
            "media_protocol": {"embargo_hours": embargo}
        }

        st.code(json.dumps(offer, indent=2))

        if st.button("Evaluate Offer"):
            payload = {"proposer_party_id": parties[0] if parties else "PH_GOV", "agreement_vector": offer}
            try:
                r = requests.post(f"{API_URL}/bargain/{case_id}/offer", json=payload, timeout=60)
                result = r.json()
                st.session_state.current_offer = offer
                st.write(result)
            except Exception as e:
                st.error(f"Evaluation failed: {e}")

    with tabs[1]:
        st.header("Run Mesa ABM")
        steps = st.slider("Steps", 50, 1000, 300, 50)
        env = {"weather_state": case.get("weather_state", "calm"), "media_visibility": case.get("media_visibility", 2)}

        if st.button("Run Simulation"):
            sim_payload = {"steps": steps, "environment": env, "agreement_vector": offer}
            try:
                sr = requests.post(f"{API_URL}/sim/run", json=sim_payload, timeout=120)
                res = sr.json()
                st.subheader("Summary")
                st.json(res.get("summary", {}))
                st.subheader("Events")
                if len(res.get("events", [])) > 0:
                    df = pd.DataFrame(res["events"])
                    st.dataframe(df)
            except Exception as e:
                st.error(f"Simulation failed: {e}")

    with tabs[2]:
        st.header("Calibrate Model")
        st.write("Fit ABM params to historical incident counts.")
        c_steps = st.slider("Steps (calibration)", 100, 1000, 300, 50)
        c_bucket = st.number_input("Bucket size", min_value=10, max_value=100, value=20, step=5)

        if st.button("Run Calibration"):
            st.info("Calibration would run here (see streamlit_app.py for full implementation)")

    with tabs[3]:
        st.header("Live Session Monitor")
        st.markdown("Monitor all parties in real-time training")

        if st.button("Refresh Party Status"):
            st.write("Party connection status would appear here")

        st.subheader("Current Offers on Table")
        if st.session_state.current_offer:
            st.json(st.session_state.current_offer)
        else:
            st.info("No offers submitted yet")

def party_view():
    """Party-specific limited view"""
    party_id = st.session_state.user_role

    party_names = {
        "PH_GOV": "🇵🇭 Philippines Government",
        "PRC_MARITIME": "🇨🇳 PRC Maritime Forces",
        "VN_CG": "🇻🇳 Vietnam Coast Guard",
        "MY_CG": "🇲🇾 Malaysia Coast Guard"
    }

    st.title(f"SCS Mediation Simulation - {party_names.get(party_id, party_id)}")

    # Sidebar
    with st.sidebar:
        st.markdown(f"**Your Role:** {party_names.get(party_id, party_id)}")
        st.markdown("---")

        # Session info
        st.subheader("Session Info")
        if st.session_state.session_id:
            st.success(f"Session: {st.session_state.session_id}")
        else:
            st.warning("No active session")
            if st.button("Request Session Status"):
                # Query API for active sessions
                try:
                    r = requests.get(f"{API_URL}/bargain/sessions", timeout=5)
                    sessions = r.json()
                    if sessions:
                        st.json(sessions)
                except Exception as e:
                    st.error(f"Cannot connect to API: {e}")

        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.user_role = None
            st.session_state.session_id = None
            st.rerun()

    # Main area
    tabs = st.tabs(["📋 Your Position", "📝 Current Proposal", "💭 Make Offer", "📊 Your Assessment"])

    with tabs[0]:
        st.header("Your Position & Interests")

        # Party-specific information (would be loaded from scenario)
        positions = {
            "PH_GOV": {
                "primary_interests": [
                    "Maintain sovereignty over territorial waters",
                    "Ensure safe passage for resupply missions",
                    "Protect fishermen's livelihoods",
                    "Avoid military escalation"
                ],
                "batna": "Continue current ad-hoc resupply with risk of confrontation",
                "key_concerns": ["Safety of personnel", "Face/prestige", "Operational access"],
                "constraints": ["International law (UNCLOS)", "Domestic political pressure", "Alliance considerations"]
            },
            "PRC_MARITIME": {
                "primary_interests": [
                    "Assert historical claims in South China Sea",
                    "Maintain control over strategic waters",
                    "Prevent normalization of Philippine presence",
                    "Avoid international condemnation"
                ],
                "batna": "Continue blockade/harassment tactics",
                "key_concerns": ["Strategic control", "Face/prestige", "Regional influence"],
                "constraints": ["International scrutiny", "Regional relationships", "Domestic nationalism"]
            }
        }

        pos = positions.get(party_id, {"primary_interests": [], "batna": "Unknown", "key_concerns": [], "constraints": []})

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🎯 Your Interests")
            for interest in pos["primary_interests"]:
                st.markdown(f"- {interest}")

            st.subheader("⚠️ Your BATNA")
            st.info(pos["batna"])

        with col2:
            st.subheader("🔑 Key Concerns")
            for concern in pos["key_concerns"]:
                st.markdown(f"- {concern}")

            st.subheader("🚧 Constraints")
            for constraint in pos["constraints"]:
                st.markdown(f"- {constraint}")

    with tabs[1]:
        st.header("Current Proposal on the Table")

        if st.session_state.current_offer:
            st.json(st.session_state.current_offer)

            st.markdown("---")
            st.subheader("Your Utility from This Proposal")

            # Get utility for this party only
            case_id = st.session_state.session_id or "demo_case"
            try:
                payload = {
                    "proposer_party_id": party_id,
                    "agreement_vector": st.session_state.current_offer
                }
                r = requests.post(f"{API_URL}/bargain/{case_id}/offer", json=payload, timeout=30)
                result = r.json()

                my_utility = result['utilities'].get(party_id, 0)
                my_acceptance = result['acceptance_prob'].get(party_id, 0)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Your Utility", f"{my_utility:.1%}")
                with col2:
                    st.metric("Your Acceptance Probability", f"{my_acceptance:.1%}")

                if my_utility < 0.4:
                    st.error("⚠️ This offer is BELOW your BATNA. You should reject or counter-offer.")
                elif my_utility < 0.6:
                    st.warning("⚠️ This offer is MARGINAL. Consider negotiating for better terms.")
                else:
                    st.success("✅ This offer is ACCEPTABLE.")

            except Exception as e:
                st.error(f"Could not evaluate offer: {e}")
        else:
            st.info("No proposal currently on the table. Wait for instructor or another party to make an offer.")

    with tabs[2]:
        st.header("Make Your Offer")

        st.markdown("Propose terms for each issue area:")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Resupply SOP")
            standoff = st.slider("Standoff Distance (nm)", 0, 6, 3, key="p_standoff")
            escort = st.slider("Escort Count", 0, 3, 1, key="p_escort")
            prenotify = st.slider("Pre-notification (hours)", 0, 24, 12, key="p_notify")

        with col2:
            st.subheader("Hotline & CUES")
            hotline = st.selectbox("Hotline Status", ["ad_hoc", "24_7"], index=1, key="p_hotline")
            cues = st.multiselect("CUES Checklist", ["distance", "AIS_on", "video_record"], default=["distance", "AIS_on"], key="p_cues")

        with col3:
            st.subheader("Media Protocol")
            embargo = st.slider("Embargo (hours)", 0, 24, 6, key="p_embargo")

        offer = {
            "resupply_SOP": {"standoff_nm": standoff, "escort_count": escort, "pre_notification_hours": prenotify},
            "hotline_cues": {"hotline_status": hotline, "cues_checklist": cues},
            "media_protocol": {"embargo_hours": embargo}
        }

        st.code(json.dumps(offer, indent=2))

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Submit Offer to Mediator", use_container_width=True):
                st.session_state.current_offer = offer
                st.success("✅ Offer submitted! Waiting for other parties...")

        with col2:
            if st.button("🔍 Preview My Utility", use_container_width=True):
                case_id = st.session_state.session_id or "demo_case"
                try:
                    payload = {"proposer_party_id": party_id, "agreement_vector": offer}
                    r = requests.post(f"{API_URL}/bargain/{case_id}/offer", json=payload, timeout=30)
                    result = r.json()
                    my_utility = result['utilities'].get(party_id, 0)
                    st.info(f"Your utility from this offer: {my_utility:.1%}")
                except Exception as e:
                    st.error(f"Preview failed: {e}")

    with tabs[3]:
        st.header("Your Assessment")

        st.markdown("""
        Use this space to track your strategy:
        """)

        notes = st.text_area("Strategy Notes", height=200,
                            placeholder="What are your priorities? What concessions can you make? What are your red lines?")

        if st.button("💾 Save Notes"):
            # Could save to session state or file
            st.success("Notes saved (local session only)")

def main():
    """Main application entry point"""
    # Must be first Streamlit command
    st.set_page_config(page_title="SCS Simulation - Multi-View", layout="wide")

    init_session_state()

    # Route to appropriate view based on role
    if st.session_state.user_role is None:
        role_selection_page()
    elif st.session_state.user_role == "INSTRUCTOR":
        instructor_console()
    else:
        party_view()

if __name__ == "__main__":
    main()
