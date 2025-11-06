#!/usr/bin/env python3
"""
Enhanced Multi-View Training Simulation Interface
Redesigned for optimal usability and clear workflow
"""

import streamlit as st
import json
import os
import pandas as pd
from typing import Optional, Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Peace Mediation Modules
from scs_mediator_sdk.dynamics.escalation_ladder import EscalationManager, EscalationLevel
from scs_mediator_sdk.peacebuilding.cbm_library import CBMLibrary, CBMCategory
from scs_mediator_sdk.politics.domestic_constraints import WinSetAnalyzer, create_philippines_domestic_actors, create_china_domestic_actors
from scs_mediator_sdk.diplomacy.multi_track import MultiTrackMediator, DiplomaticTrack
from scs_mediator_sdk.peacebuilding.spoiler_management import SpoilerManager, create_scs_spoilers

# AI Guide Module
from scs_mediator_sdk.ai_guide import create_instructor_guide, create_participant_guide

# Bargaining and Simulation Engines (no API server needed!)
from scs_mediator_sdk.engines.bargaining_engine import BargainingSession, AgreementVector
from scs_mediator_sdk.sim.mesa_abm import MaritimeModel

# ==================== SCENARIO CONFIGURATIONS ====================

# Scenario-specific configurations for context-aware UI
SCENARIO_CONFIG = {
    "scenario_A_second_thomas.json": {
        "name": "Second Thomas Shoal (Resupply)",
        "parties": ["PH_GOV", "PRC_MARITIME"],
        "recommended_issues": ["resupply_SOP", "hotline_cues", "incident_response", "naval_restrictions"],
        "all_issues": ["resupply_SOP", "hotline_cues", "incident_response", "naval_restrictions",
                       "media_protocol", "fishing_rights", "access_zones"],
        "context": "Philippine resupply missions to BRP Sierra Madre",
        "focus_area": "Ensuring safe passage for humanitarian resupply missions while managing naval presence",
        "cbm_priorities": ["hotline_establishment", "incident_reporting", "safe_passage_protocol"],
        "escalation_context": "Resupply operations at contested shoal with garrison presence"
    },
    "scenario_B_scarborough.json": {
        "name": "Scarborough Shoal (Fishing Rights)",
        "parties": ["PH_GOV", "PRC_MARITIME"],
        "recommended_issues": ["fishing_rights", "access_zones", "seasonal_restrictions", "enforcement_protocols"],
        "all_issues": ["fishing_rights", "access_zones", "seasonal_restrictions", "enforcement_protocols",
                       "hotline_cues", "media_protocol", "resource_sharing"],
        "context": "Traditional fishing grounds and access rights",
        "focus_area": "Balancing traditional fishing access with territorial claims",
        "cbm_priorities": ["fisheries_cooperation", "joint_patrols", "resource_sharing"],
        "escalation_context": "Fishing vessel confrontations in contested waters"
    },
    "scenario_C_kasawari.json": {
        "name": "Kasawari Gas Field (Energy)",
        "parties": ["MY_CG", "PRC_MARITIME"],
        "optional_parties": ["VN_CG"],
        "recommended_issues": ["resource_extraction", "maritime_boundaries", "joint_development", "revenue_sharing"],
        "all_issues": ["resource_extraction", "maritime_boundaries", "joint_development", "revenue_sharing",
                       "exploration_rights", "hotline_cues", "incident_response"],
        "context": "Oil and gas exploration rights in contested EEZ",
        "focus_area": "Managing energy resource extraction and revenue distribution",
        "cbm_priorities": ["joint_development", "technical_cooperation", "revenue_mechanisms"],
        "escalation_context": "Energy exploration activities in overlapping EEZ claims"
    },
    "scenario_D_natuna.json": {
        "name": "Natuna Islands (EEZ Boundaries)",
        "parties": ["MY_CG", "PRC_MARITIME"],
        "optional_parties": ["VN_CG"],
        "recommended_issues": ["eez_boundaries", "sovereign_rights", "fishing_zones", "naval_patrols"],
        "all_issues": ["eez_boundaries", "sovereign_rights", "fishing_zones", "naval_patrols",
                       "resource_extraction", "hotline_cues", "incident_response"],
        "context": "Exclusive Economic Zone boundary disputes",
        "focus_area": "Clarifying maritime boundaries and sovereign rights in contested waters",
        "cbm_priorities": ["boundary_clarification", "joint_patrols", "incident_prevention"],
        "escalation_context": "Overlapping EEZ claims and patrol activities"
    }
}

# Issue display names for UI
ISSUE_DISPLAY_NAMES = {
    "resupply_SOP": "Resupply Standard Operating Procedures",
    "hotline_cues": "Hotline & CUES Protocols",
    "incident_response": "Incident Response Procedures",
    "naval_restrictions": "Naval Movement Restrictions",
    "fishing_rights": "Fishing Rights & Access",
    "access_zones": "Designated Access Zones",
    "seasonal_restrictions": "Seasonal Access Restrictions",
    "enforcement_protocols": "Enforcement & Monitoring Protocols",
    "resource_extraction": "Resource Extraction Rights",
    "maritime_boundaries": "Maritime Boundary Delimitation",
    "joint_development": "Joint Development Agreements",
    "revenue_sharing": "Revenue Sharing Mechanisms",
    "eez_boundaries": "EEZ Boundary Clarification",
    "sovereign_rights": "Sovereign Rights Recognition",
    "fishing_zones": "Fishing Zone Management",
    "naval_patrols": "Naval Patrol Coordination",
    "media_protocol": "Media & Public Communication",
    "exploration_rights": "Exploration Rights Management",
    "resource_sharing": "Resource Sharing Arrangements"
}

# ==================== SESSION STATE ====================

def init_session_state():
    """Initialize all session state variables"""
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None
    if 'current_offer' not in st.session_state:
        st.session_state.current_offer = None
    if 'last_evaluation' not in st.session_state:
        st.session_state.last_evaluation = None
    if 'simulation_results' not in st.session_state:
        st.session_state.simulation_results = None
    if 'workflow_step' not in st.session_state:
        st.session_state.workflow_step = 1
    if 'selected_scenario' not in st.session_state:
        st.session_state.selected_scenario = None
    if 'scenario_config' not in st.session_state:
        st.session_state.scenario_config = None
    # Peace mediation modules
    if 'escalation_manager' not in st.session_state:
        st.session_state.escalation_manager = EscalationManager()
    if 'cbm_library' not in st.session_state:
        st.session_state.cbm_library = CBMLibrary()
    if 'multi_track_mediator' not in st.session_state:
        st.session_state.multi_track_mediator = MultiTrackMediator()
    if 'spoiler_manager' not in st.session_state:
        st.session_state.spoiler_manager = SpoilerManager()
        for spoiler in create_scs_spoilers():
            st.session_state.spoiler_manager.add_spoiler(spoiler)
    # Strategic context for soft power tracking (per-party)
    if 'strategic_contexts' not in st.session_state:
        from scs_mediator_sdk.dynamics.strategic_context import StrategicContext
        # Initialize strategic context for each party
        st.session_state.strategic_contexts = {
            "PH_GOV": StrategicContext(),
            "PRC_MARITIME": StrategicContext(),
            "VN_CG": StrategicContext(),
            "MY_CG": StrategicContext()
        }

    # API key configuration for AI features
    if 'anthropic_api_key' not in st.session_state:
        # Try to get from environment first (for backward compatibility)
        st.session_state.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    # Bargaining session storage (replaces API server sessions)
    if 'bargaining_sessions' not in st.session_state:
        st.session_state.bargaining_sessions = {}

# ==================== ROLE SELECTION ====================

def role_selection_page():
    """Enhanced landing page with clear role selection"""
    st.title("🌊 South China Sea Mediation Simulation")
    st.markdown("### Welcome! Please select your role to continue")
    st.markdown("---")

    col1, spacer, col2 = st.columns([5, 1, 5])

    with col1:
        st.markdown("""
        <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;">
            <h3 style="color: #1f77b4;">👨‍🏫 Facilitator</h3>
            <p><strong>You will be able to:</strong></p>
            <ul>
                <li>Select and configure scenarios</li>
                <li>See all parties' utilities and probabilities</li>
                <li>Run simulations and analyze results</li>
                <li>Monitor live training sessions</li>
                <li>Guide negotiations</li>
            </ul>
            <p><em>Choose this if you're facilitating a training session or conducting solo analysis.</em></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        if st.button("🎓 Enter as Facilitator", use_container_width=True, type="primary"):
            st.session_state.user_role = "INSTRUCTOR"
            st.session_state.workflow_step = 1
            st.rerun()

    with col2:
        st.markdown("""
        <div style="background-color: #f0f8e8; padding: 20px; border-radius: 10px; border-left: 5px solid #2ca02c;">
            <h3 style="color: #2ca02c;">🎭 Negotiating Party</h3>
            <p><strong>You will be able to:</strong></p>
            <ul>
                <li>View your party's position and interests</li>
                <li>See your own utility from proposals</li>
                <li>Make and submit counter-offers</li>
                <li>Participate in realistic negotiations</li>
                <li>Track your strategy</li>
            </ul>
            <p><em>Choose this if you're participating in a live training as one of the negotiating parties.</em></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")

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

        if st.button("🤝 Enter as Party", use_container_width=True, type="primary"):
            st.session_state.user_role = party_choice
            st.rerun()

    st.markdown("---")
    with st.expander("ℹ️ Need help deciding?"):
        st.markdown("""
        **For Solo Practice**: Choose Facilitator to explore scenarios and test agreements on your own.

        **For Live Training**:
        - One person chooses Facilitator (the session leader)
        - Each other participant chooses their assigned party
        - All participants open this URL in their own browser
        """)

# ==================== FACILITATOR CONSOLE ====================

def show_workflow_guide(current_step: int):
    """Show visual workflow guide for facilitator"""
    steps = [
        "1️⃣ Setup",
        "2️⃣ Build Offer",
        "3️⃣ Evaluate",
        "4️⃣ Simulate",
        "5️⃣ Refine",
        "6️⃣ Peace Tools"
    ]

    cols = st.columns(len(steps))
    for i, (col, step) in enumerate(zip(cols, steps)):
        with col:
            if i + 1 == current_step:
                st.markdown(f"**<span style='color: #1f77b4; font-size: 18px;'>{step}</span>**", unsafe_allow_html=True)
                st.markdown("▲")
            elif i + 1 < current_step:
                st.markdown(f"<span style='color: #2ca02c;'>✓ {step}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color: #999;'>{step}</span>", unsafe_allow_html=True)

def instructor_console():
    """Enhanced facilitator console with guided workflow"""
    import pandas as pd
    import matplotlib.pyplot as plt

    st.title("🎓 Facilitator Console")

    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Session Info")
        st.info(f"**Role:** Facilitator")
        if st.session_state.session_id:
            st.success(f"**Session:** {st.session_state.session_id}")
        else:
            st.warning("**Session:** Not started")

        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_role = None
            st.session_state.session_id = None
            st.rerun()

        st.markdown("---")

        # AI Guide
        with st.expander("💬 AI Guide", expanded=False):
            st.markdown("**🤖 Mediator Assistant**")
            st.caption("AI-powered guidance for facilitators")

            # Initialize AI guide in session state with persistence
            if 'ai_guide' not in st.session_state:
                try:
                    # Create guide with unique session ID for instructors
                    st.session_state.ai_guide = create_instructor_guide(
                        api_key=st.session_state.anthropic_api_key or None,
                        session_id="instructor",
                        enable_persistence=True
                    )
                    # Load existing chat history from persisted data
                    st.session_state.chat_history = [
                        {
                            "question": msg.content,
                            "response": st.session_state.ai_guide.conversation_history[i+1].content if i+1 < len(st.session_state.ai_guide.conversation_history) else "",
                            "sources": "Loaded from history"
                        }
                        for i, msg in enumerate(st.session_state.ai_guide.conversation_history)
                        if msg.role == "user" and i+1 < len(st.session_state.ai_guide.conversation_history)
                    ]
                except Exception as e:
                    st.error(f"AI Guide unavailable: {str(e)}")
                    st.session_state.ai_guide = None
                    st.session_state.chat_history = []

            if st.session_state.ai_guide:
                # Update context
                context_data = {
                    "scenario": st.session_state.get('selected_scenario'),
                    "step": st.session_state.get('workflow_step', 1)
                }
                st.session_state.ai_guide.set_context(**context_data)

                # Quick tips
                st.markdown("**Quick Tips:**")
                tips = st.session_state.ai_guide.get_quick_tips()
                for tip in tips[:3]:  # Show first 3 tips
                    st.info(tip)

                st.markdown("---")

                # Chat interface
                st.markdown("**Ask a Question:**")
                user_question = st.text_area("Your question:", key="instructor_ai_question", height=80)

                if st.button("Ask Assistant", key="instructor_ask_btn", use_container_width=True):
                    if user_question:
                        with st.spinner("Thinking..."):
                            try:
                                # Set simulation parameters for context-aware guidance
                                sim_params = {
                                    "standoff": "Distance (nm) between conflicting vessels (0-10, higher = less tension)",
                                    "escort": "Military escort intensity level (0-10, higher = more aggressive)",
                                    "prenotify": "Pre-notification requirements (0-10, higher = more transparency)",
                                    "hotline": "Communication channel status (None/Ad-hoc/Dedicated)",
                                    "embargo": "Economic pressure level (0-10)",
                                    "traditional_access": "Fishing rights for traditional fishermen (0-100%)",
                                    "seasonal_closure": "Days per year fishing is closed (0-180 days)",
                                    "patrol_frequency": "Joint patrol frequency (None/Monthly/Weekly/Daily)",
                                    "revenue_split": "Resource revenue sharing percentage (0-100%)",
                                    "moratorium_months": "Development freeze duration (0-36 months)",
                                    "boundary_method": "EEZ delimitation approach (Equidistance/Natural prolongation/Special circumstances)",
                                    "patrol_coordination": "Patrol cooperation level (Independent/Info sharing/Joint)",
                                    "buffer_zone_nm": "Neutral buffer zone width (0-50 nautical miles)"
                                }
                                st.session_state.ai_guide.set_simulation_parameters(sim_params)

                                result = st.session_state.ai_guide.ask(user_question)
                                st.session_state.chat_history.append({
                                    "question": user_question,
                                    "response": result["response"],
                                    "sources": result["sources"]
                                })
                            except Exception as e:
                                st.error(f"Error: {str(e)}")

                # Display chat history (most recent first)
                if st.session_state.get('chat_history'):
                    st.markdown("---")
                    st.markdown("**Recent Conversation:**")
                    for idx, chat in enumerate(reversed(st.session_state.chat_history[-2:])):  # Show last 2 full
                        with st.expander(f"Q: {chat['question'][:70]}...", expanded=(idx==0)):
                            st.markdown(f"**Question:** {chat['question']}")
                            st.markdown(f"**Answer:** {chat['response']}")
                            # Academic citations are inline in the response

                if st.button("Clear History", key="instructor_clear_history"):
                    st.session_state.ai_guide.clear_history()
                    st.session_state.chat_history = []
                    st.rerun()

    # Workflow guide
    show_workflow_guide(st.session_state.workflow_step)
    st.markdown("---")

    # ===== STEP 1: SETUP =====
    with st.expander("📋 Step 1: Setup Scenario & Session", expanded=(st.session_state.workflow_step == 1)):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Select Scenario")
            case_dir = "cases/scs"
            scenario_files = [f for f in os.listdir(case_dir) if f.endswith(".json")] if os.path.exists(case_dir) else []

            scenario_display_names = {
                "scenario_A_second_thomas.json": "🏝️ Scenario A: Second Thomas Shoal (Resupply)",
                "scenario_B_scarborough.json": "🎣 Scenario B: Scarborough Shoal (Fishing Rights)",
                "scenario_C_kasawari.json": "⛽ Scenario C: Kasawari Gas Field (Energy)",
                "scenario_D_natuna.json": "🌊 Scenario D: Natuna Islands (EEZ Boundaries)"
            }

            scenario = st.selectbox(
                "Choose a scenario",
                scenario_files if scenario_files else ["(none)"],
                format_func=lambda x: scenario_display_names.get(x, x),
                key="scenario_selector"
            )

            # Store selected scenario and config in session state
            if scenario != "(none)" and scenario != st.session_state.selected_scenario:
                st.session_state.selected_scenario = scenario
                st.session_state.scenario_config = SCENARIO_CONFIG.get(scenario, None)

            if scenario != "(none)":
                case_path = os.path.join(case_dir, scenario)
                with open(case_path, "r", encoding="utf-8") as f:
                    case = json.load(f)

                st.markdown(f"**Location:** {case.get('flashpoint', 'N/A')}")
                st.markdown(f"**Focus:** {case.get('focus', 'N/A')}")
                st.markdown(f"**Weather:** {case.get('weather_state', 'calm').capitalize()}")
                st.markdown(f"**Media Visibility:** {case.get('media_visibility', 2)}/3")

                # Display scenario context
                if st.session_state.scenario_config:
                    st.markdown("---")
                    st.markdown(f"""
                    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; margin: 10px 0;">
                        <h4 style="color: #1976d2; margin: 0 0 10px 0;">Scenario Context</h4>
                        <p style="color: #000; margin: 5px 0;"><strong>Focus:</strong> <span style="color: #333;">{st.session_state.scenario_config['focus_area']}</span></p>
                        <p style="color: #000; margin: 5px 0;"><strong>Context:</strong> <span style="color: #333;">{st.session_state.scenario_config['context']}</span></p>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                case = {"id": "demo_case", "weather_state": "calm", "media_visibility": 2}

        with col2:
            # Show map if available
            if scenario != "(none)":
                stem = os.path.splitext(scenario)[0].lower()
                map_path = None
                if os.path.exists('assets/maps'):
                    for fn in os.listdir('assets/maps'):
                        if stem in fn.lower():
                            map_path = os.path.join('assets/maps', fn)
                            break
                if map_path and os.path.exists(map_path):
                    st.image(map_path, caption="Scenario Map", use_container_width=True)

        st.markdown("---")
        st.subheader("Start Negotiation Session")

        # Get scenario-specific defaults
        if st.session_state.scenario_config:
            default_parties = st.session_state.scenario_config.get('parties', ["PH_GOV", "PRC_MARITIME"])
            all_parties = default_parties + st.session_state.scenario_config.get('optional_parties', [])
            default_issues = st.session_state.scenario_config.get('recommended_issues', ["resupply_SOP", "hotline_cues", "media_protocol"])
            all_issues = st.session_state.scenario_config.get('all_issues', default_issues)
        else:
            default_parties = ["PH_GOV", "PRC_MARITIME"]
            all_parties = ["PH_GOV", "PRC_MARITIME", "VN_CG", "MY_CG"]
            default_issues = ["resupply_SOP", "hotline_cues", "media_protocol"]
            all_issues = ["resupply_SOP", "hotline_cues", "media_protocol", "fishing_rights"]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Participating Parties**")
            if st.session_state.scenario_config:
                st.caption(f"✓ Recommended for this scenario: {', '.join([p.replace('_', ' ') for p in default_parties])}")

            parties = st.multiselect(
                "Select parties (you can add optional parties)",
                ["PH_GOV", "PRC_MARITIME", "VN_CG", "MY_CG"],
                default=default_parties,
                format_func=lambda x: {
                    "PH_GOV": "🇵🇭 Philippines",
                    "PRC_MARITIME": "🇨🇳 PRC Maritime",
                    "VN_CG": "🇻🇳 Vietnam",
                    "MY_CG": "🇲🇾 Malaysia"
                }.get(x, x),
                key="parties_selector"
            )

        with col2:
            mediator = st.text_input("Mediator Name", "ASEAN_Facilitator")

        st.markdown("**Issues to Negotiate**")
        if st.session_state.scenario_config:
            st.caption(f"✓ Recommended for this scenario: {', '.join([ISSUE_DISPLAY_NAMES.get(i, i.replace('_', ' ').title()) for i in default_issues])}")

        issue_space = st.multiselect(
            "Select issues (recommended issues pre-selected)",
            all_issues,
            default=default_issues,
            format_func=lambda x: ISSUE_DISPLAY_NAMES.get(x, x.replace("_", " ").title()),
            key="issues_selector"
        )

        if st.button("▶️ Start Session", type="primary", use_container_width=True):
            case_id = case.get("id", "demo_case")
            try:
                # Create bargaining session directly (no API server needed)
                session = BargainingSession.start(
                    case_id=case_id,
                    parties=parties,
                    mediator=mediator,
                    issue_space=issue_space,
                    priors=None,
                    max_rounds=12
                )
                st.session_state.bargaining_sessions[case_id] = session
                st.session_state.session_id = case_id
                st.session_state.selected_issues = issue_space  # Store for Step 2
                st.session_state.workflow_step = 2
                st.success("✅ Session started successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to start session: {e}")

    # ===== STEP 2: BUILD OFFER =====
    with st.expander("📝 Step 2: Build Agreement Offer", expanded=(st.session_state.workflow_step == 2)):
        if not st.session_state.session_id:
            st.warning("⚠️ Please complete Step 1 first")
        else:
            st.subheader("Configure Agreement Terms")

            # Display scenario context reminder
            if st.session_state.scenario_config:
                st.markdown(f"""
                <div style="background-color: #fff8e1; padding: 12px; border-radius: 5px; border-left: 4px solid #ffa500; margin-bottom: 15px;">
                    <p style="color: #000; margin: 0;"><strong>Scenario:</strong> {st.session_state.scenario_config['name']}</p>
                    <p style="color: #333; margin: 5px 0 0 0; font-size: 14px;">{st.session_state.scenario_config['focus_area']}</p>
                </div>
                """, unsafe_allow_html=True)

            # Get selected issues from session (stored when starting session)
            # For now, we'll use a default set, but in practice this would come from Step 1
            selected_issues = st.session_state.get('selected_issues', [])
            if not selected_issues and st.session_state.scenario_config:
                selected_issues = st.session_state.scenario_config.get('recommended_issues', [])

            offer = {}

            # Dynamically create columns based on number of issue categories
            issue_categories = []

            # Check which issue categories are selected
            has_resupply = any(issue in selected_issues for issue in ["resupply_SOP", "incident_response", "naval_restrictions"])
            has_communication = any(issue in selected_issues for issue in ["hotline_cues"])
            has_fishing = any(issue in selected_issues for issue in ["fishing_rights", "access_zones", "seasonal_restrictions", "enforcement_protocols"])
            has_energy = any(issue in selected_issues for issue in ["resource_extraction", "maritime_boundaries", "joint_development", "revenue_sharing"])
            has_eez = any(issue in selected_issues for issue in ["eez_boundaries", "sovereign_rights", "fishing_zones", "naval_patrols"])
            has_media = any(issue in selected_issues for issue in ["media_protocol"])

            # Build UI based on selected issues
            if has_resupply or has_communication or has_media or not selected_issues:
                # Default resupply scenario (backward compatible)
                col1, col2, col3 = st.columns(3)

                with col1:
                    if has_resupply or not selected_issues:
                        st.markdown("#### 🚢 Resupply Operations")
                        standoff = st.slider(
                            "Standoff Distance (nautical miles)",
                            min_value=0, max_value=10, value=3,
                            help="How far naval vessels must stay from resupply operations",
                            key="standoff_slider"
                        )
                        escort = st.slider(
                            "Maximum Escort Vessels",
                            min_value=0, max_value=5, value=1,
                            help="Number of military escorts allowed per resupply mission",
                            key="escort_slider"
                        )
                        prenotify = st.slider(
                            "Pre-Notification Period (hours)",
                            min_value=0, max_value=48, value=12,
                            help="Advance notice required before resupply missions",
                            key="prenotify_slider"
                        )
                        offer["resupply_SOP"] = {
                            "standoff_nm": standoff,
                            "escort_count": escort,
                            "pre_notification_hours": prenotify
                        }

                with col2:
                    if has_communication or not selected_issues:
                        st.markdown("#### 📞 Communication Protocols")
                        hotline = st.selectbox(
                            "Hotline Availability",
                            ["ad_hoc", "24_7"],
                            index=1,
                            format_func=lambda x: "24/7 Direct Line" if x == "24_7" else "Ad-Hoc (As Needed)",
                            key="hotline_select"
                        )
                        cues_options = st.multiselect(
                            "CUES Compliance Requirements",
                            ["distance", "AIS_on", "video_record"],
                            default=["distance", "AIS_on"],
                            format_func=lambda x: {
                                "distance": "Safe Distance Keeping",
                                "AIS_on": "AIS Transponders Active",
                                "video_record": "Incident Video Recording"
                            }.get(x, x),
                            key="cues_multiselect"
                        )
                        offer["hotline_cues"] = {
                            "hotline_status": hotline,
                            "cues_checklist": cues_options
                        }

                with col3:
                    if has_media or not selected_issues:
                        st.markdown("#### 📰 Media Management")
                        embargo = st.slider(
                            "News Embargo Period (hours)",
                            min_value=0, max_value=48, value=6,
                            help="Time before incidents can be reported publicly",
                            key="embargo_slider"
                        )
                        offer["media_protocol"] = {
                            "embargo_hours": embargo
                        }

            if has_fishing:
                st.markdown("---")
                st.markdown("### 🎣 Fishing & Access Rights")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("#### Access Zones")
                    traditional_access = st.slider("Traditional Fishing Access", 0, 100, 70, 5,
                                                  help="Percentage of traditional fishing grounds accessible",
                                                  key="fish_access_slider")

                with col2:
                    st.markdown("#### Seasonal Rules")
                    seasonal_closure = st.slider("Seasonal Closure (days/year)", 0, 180, 60, 10,
                                                help="Days per year with fishing restrictions",
                                                key="seasonal_slider")

                with col3:
                    st.markdown("#### Enforcement")
                    patrol_frequency = st.selectbox("Joint Patrol Frequency",
                                                   ["weekly", "monthly", "quarterly"],
                                                   index=1,
                                                   key="patrol_select")

                offer["fishing_rights"] = {
                    "traditional_access_pct": traditional_access,
                    "seasonal_closure_days": seasonal_closure,
                    "patrol_frequency": patrol_frequency
                }

            if has_energy:
                st.markdown("---")
                st.markdown("### ⛽ Energy & Resource Rights")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("#### Exploration Rights")
                    exploration_zones = st.multiselect("Approved Exploration Zones",
                                                      ["Zone A", "Zone B", "Zone C", "Zone D"],
                                                      default=["Zone A"],
                                                      key="exploration_multiselect")

                with col2:
                    st.markdown("#### Joint Development")
                    joint_dev = st.checkbox("Enable Joint Development", value=True, key="joint_dev_check")
                    revenue_split = st.slider("Revenue Split (%)", 0, 100, 50, 5,
                                             help="Percentage to initiating party",
                                             key="revenue_slider")

                with col3:
                    st.markdown("#### Timeline")
                    moratorium_months = st.slider("Initial Moratorium (months)", 0, 36, 12, 3,
                                                 help="Cooling-off period before extraction",
                                                 key="moratorium_slider")

                offer["resource_extraction"] = {
                    "exploration_zones": exploration_zones,
                    "joint_development": joint_dev,
                    "revenue_split_pct": revenue_split,
                    "moratorium_months": moratorium_months
                }

            if has_eez:
                st.markdown("---")
                st.markdown("### 🌊 EEZ & Maritime Boundaries")
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### Boundary Clarification")
                    boundary_method = st.selectbox("Delimitation Method",
                                                  ["equidistance", "natural_prolongation", "negotiated"],
                                                  index=2,
                                                  key="boundary_select")
                    provisional_arrangement = st.checkbox("Provisional Arrangement", value=True,
                                                         key="provisional_check")

                with col2:
                    st.markdown("#### Patrol Coordination")
                    patrol_coordination = st.selectbox("Coordination Level",
                                                      ["none", "notification", "joint_patrols"],
                                                      index=1,
                                                      key="patrol_coord_select")
                    buffer_zone_nm = st.slider("Buffer Zone (nautical miles)", 0, 50, 12, 2,
                                              key="buffer_slider")

                offer["eez_boundaries"] = {
                    "delimitation_method": boundary_method,
                    "provisional_arrangement": provisional_arrangement,
                    "patrol_coordination": patrol_coordination,
                    "buffer_zone_nm": buffer_zone_nm
                }

            st.session_state.current_offer = offer

            with st.expander("📄 View Agreement JSON"):
                st.code(json.dumps(offer, indent=2))

            if st.button("➡️ Proceed to Evaluation", type="primary", use_container_width=True):
                st.session_state.workflow_step = 3
                st.rerun()

    # ===== STEP 3: EVALUATE =====
    with st.expander("🎲 Step 3: Evaluate Offer", expanded=(st.session_state.workflow_step == 3)):
        if not st.session_state.current_offer:
            st.warning("⚠️ Please complete Step 2 first")
        else:
            st.subheader("Assess Agreement Quality")

            if st.button("🔍 Calculate Utilities & Acceptance Probabilities", type="primary", use_container_width=True):
                try:
                    case_id = st.session_state.session_id or "demo_case"
                    # Evaluate offer directly using bargaining session (no API needed)
                    session = st.session_state.bargaining_sessions.get(case_id)
                    if not session:
                        st.error("❌ Session not found. Please start a new session in Step 1.")
                    else:
                        av = AgreementVector(st.session_state.current_offer)
                        result = session.evaluate_offer("PH_GOV", av)
                        st.session_state.last_evaluation = result

                except Exception as e:
                    st.error(f"❌ Evaluation failed: {e}")
                    result = None

            if st.session_state.last_evaluation:
                result = st.session_state.last_evaluation

                # Add CSS for high contrast metrics
                st.markdown("""
                <style>
                [data-testid="stMetricValue"] {
                    color: #000000 !important;
                    font-weight: bold !important;
                }
                [data-testid="stMetricLabel"] {
                    color: #333333 !important;
                    font-weight: 600 !important;
                }
                [data-testid="stMetricDelta"] {
                    color: #000000 !important;
                    font-weight: 600 !important;
                }
                </style>
                """, unsafe_allow_html=True)

                st.markdown("### 📊 Results")

                # Utilities
                st.markdown("""
                <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4; margin-bottom: 20px;">
                    <h4 style="color: #000; margin-top: 0;">Party Utilities (0-1 scale)</h4>
                </div>
                """, unsafe_allow_html=True)

                utilities = result.get('utilities', {})

                cols = st.columns(len(utilities))
                for col, (party, utility) in zip(cols, utilities.items()):
                    with col:
                        party_name = {
                            "PH_GOV": "🇵🇭 Philippines",
                            "PRC_MARITIME": "🇨🇳 PRC",
                            "VN_CG": "🇻🇳 Vietnam",
                            "MY_CG": "🇲🇾 Malaysia"
                        }.get(party, party)

                        if utility > 0.7:
                            bg_color = "#d4edda"
                            status = "Excellent"
                        elif utility > 0.5:
                            bg_color = "#cfe2ff"
                            status = "Good"
                        elif utility > 0.4:
                            bg_color = "#fff3cd"
                            status = "Marginal"
                        else:
                            bg_color = "#f8d7da"
                            status = "Below BATNA"

                        st.markdown(f"""
                        <div style="background-color: {bg_color}; padding: 15px; border-radius: 8px; border: 2px solid #333; margin-bottom: 10px;">
                            <div style="color: #000; font-weight: bold; font-size: 16px; margin-bottom: 5px;">{party_name}</div>
                            <div style="color: #000; font-size: 28px; font-weight: bold; margin-bottom: 5px;">{utility:.1%}</div>
                            <div style="color: #333; font-size: 14px; font-weight: 600;">{status}</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")

                # Acceptance probabilities
                st.markdown("""
                <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4; margin-bottom: 20px;">
                    <h4 style="color: #000; margin-top: 0;">Acceptance Probabilities</h4>
                </div>
                """, unsafe_allow_html=True)

                acceptance = result.get('acceptance_prob', {})

                cols = st.columns(len(acceptance))
                for col, (party, prob) in zip(cols, acceptance.items()):
                    with col:
                        party_name = {
                            "PH_GOV": "🇵🇭 Philippines",
                            "PRC_MARITIME": "🇨🇳 PRC",
                            "VN_CG": "🇻🇳 Vietnam",
                            "MY_CG": "🇲🇾 Malaysia"
                        }.get(party, party)

                        if prob > 0.7:
                            emoji = "✅"
                            bg_color = "#d4edda"
                            status_text = "Likely Accept"
                        elif prob > 0.5:
                            emoji = "⚠️"
                            bg_color = "#fff3cd"
                            status_text = "Uncertain"
                        else:
                            emoji = "❌"
                            bg_color = "#f8d7da"
                            status_text = "Likely Reject"

                        st.markdown(f"""
                        <div style="background-color: {bg_color}; padding: 15px; border-radius: 8px; border: 2px solid #333; margin-bottom: 10px;">
                            <div style="color: #000; font-weight: bold; font-size: 16px; margin-bottom: 5px;">{party_name} {emoji}</div>
                            <div style="color: #000; font-size: 28px; font-weight: bold; margin-bottom: 5px;">{prob:.1%}</div>
                            <div style="color: #333; font-size: 14px; font-weight: 600;">{status_text}</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")

                # Overall assessment
                import numpy as np
                overall = np.prod(list(acceptance.values()))
                st.markdown(f"### Overall Agreement Probability: **{overall:.1%}**")

                if overall > 0.6:
                    st.success("✅ This agreement has a good chance of being accepted by all parties!")
                    if st.button("➡️ Proceed to Simulation", type="primary", use_container_width=True):
                        st.session_state.workflow_step = 4
                        st.rerun()
                elif overall > 0.3:
                    st.warning("⚠️ Agreement is uncertain. Consider adjusting terms to improve acceptance.")
                else:
                    st.error("❌ Low probability of agreement. Significant adjustments needed.")

    # ===== STEP 4: SIMULATE =====
    with st.expander("🎮 Step 4: Simulate Agreement Durability", expanded=(st.session_state.workflow_step == 4)):
        if not st.session_state.last_evaluation:
            st.warning("⚠️ Please complete Step 3 first")
        else:
            st.subheader("Test Agreement Over Time")
            st.markdown("Run agent-based simulation to see how the agreement holds up under realistic conditions.")

            col1, col2 = st.columns([2, 1])
            with col1:
                steps = st.slider("Simulation Duration (steps)", 50, 1000, 300, 50,
                                help="Each step represents a time period. More steps = longer test.")
            with col2:
                st.metric("Estimated Runtime", f"{steps // 100} sec")

            case_id = st.session_state.session_id or "demo_case"
            case_path = os.path.join("cases/scs", f"scenario_{case_id.split('_')[-1] if '_' in case_id else 'A'}_*.json")

            if st.button("▶️ Run Simulation", type="primary", use_container_width=True):
                with st.spinner("Running simulation..."):
                    try:
                        # Run simulation directly (no API server needed)
                        model = MaritimeModel(
                            steps=steps,
                            environment={"weather_state": "calm", "media_visibility": 2},
                            agreement=st.session_state.current_offer,
                            seed=None
                        )
                        df = model.run()

                        # Format results like API response
                        if df.empty:
                            sim_results = {
                                "summary": {"incidents": 0, "max_severity": 0},
                                "events": []
                            }
                        else:
                            sim_results = {
                                "summary": {
                                    "incidents": int(len(df)),
                                    "max_severity": float(df["severity"].max())
                                },
                                "events": df.to_dict(orient="records")
                            }

                        st.session_state.simulation_results = sim_results
                        st.session_state.workflow_step = 5
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Simulation failed: {e}")

    # ===== STEP 5: ANALYZE & REFINE =====
    if st.session_state.simulation_results:
        with st.expander("📈 Step 5: Analyze Results & Refine", expanded=(st.session_state.workflow_step == 5)):
            results = st.session_state.simulation_results

            summary = results.get("summary", {})
            events_data = results.get("events", [])

            # Summary metrics
            st.markdown("### 📊 Simulation Summary")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                incident_count = summary.get("total_incidents", len(events_data))
                st.metric("Total Incidents", incident_count,
                         delta="Good" if incident_count < 25 else "High",
                         delta_color="inverse" if incident_count < 25 else "normal")

            with col2:
                if events_data:
                    df = pd.DataFrame(events_data)
                    avg_severity = df['severity'].mean() if 'severity' in df.columns else 0
                    st.metric("Avg Severity", f"{avg_severity:.2f}/1.0",
                             delta="Low" if avg_severity < 0.4 else "High",
                             delta_color="inverse" if avg_severity < 0.4 else "normal")
                else:
                    st.metric("Avg Severity", "0.00/1.0", delta="No incidents")

            with col3:
                if events_data:
                    df = pd.DataFrame(events_data)
                    max_severity = df['severity'].max() if 'severity' in df.columns else 0
                    st.metric("Max Severity", f"{max_severity:.2f}/1.0")
                else:
                    st.metric("Max Severity", "0.00/1.0")

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
**📖 HOW TO INTERPRET THESE RESULTS** (For Facilitators & Participants)

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

                with col2:
                    st.markdown("#### Severity Distribution")
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.hist(df['severity'], bins=15, edgecolor='black', alpha=0.7)
                    ax.set_xlabel('Severity')
                    ax.set_ylabel('Frequency')
                    ax.set_title('Distribution of Incident Severity')
                    ax.grid(True, alpha=0.3, axis='y')
                    st.pyplot(fig)

                st.markdown("---")
                st.markdown("####  📋 Event Log Sample (First 10 Events)")

                # Add helpful context about the event log
                st.info("**How to Read the Event Log**: Each row represents an incident. Hover over columns for descriptions. Higher severity events (>0.6) require immediate attention.")

                # Display the dataframe with better formatting
                st.dataframe(df.head(10), use_container_width=True)

                # Add interpretation guidance for specific events
                if 'description' in df.columns or 'event_type' in df.columns:
                    st.markdown("##### 🔍 Interpreting Specific Events")

                    # Find the highest severity event
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
                                    <p style="margin: 5px 0 0 0;  color: #666;">Type: {event_type}</p>
                                    <p style="margin: 5px 0 0 0;">Description: {desc}</p>
                                    <p style="margin: 5px 0 0 0; font-style: italic; color: #555;">💡 <strong>What this means</strong>: This event crossed the threshold for serious violations. Review parameters that may have contributed (standoff distance, prenotification requirements, patrol frequency).</p>
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

            if st.button("🔄 Back to Step 2 to Refine Offer", use_container_width=True):
                st.session_state.workflow_step = 2
                st.rerun()

    # ===== STEP 6: PEACE MEDIATION TOOLS =====
    with st.expander("🕊️ Step 6: Peace Mediation Tools (V2 Enhancements)", expanded=(st.session_state.workflow_step == 6)):
        st.subheader("Advanced Peace Mediation Analysis")
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; border-left: 5px solid #4682b4;">
            <p style="color: #000; margin: 0;"><strong>These tools help you analyze the peace process from multiple dimensions:</strong></p>
            <ul style="color: #333; margin-top: 10px;">
                <li>Escalation risks and de-escalation strategies</li>
                <li>Confidence-building measures (CBMs) to reduce tensions</li>
                <li>Domestic political constraints and ratification challenges</li>
                <li>Spoiler threats and management strategies</li>
                <li>Multi-track diplomacy coordination</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Tabs for different peace mediation tools
        peace_tabs = st.tabs([
            "🔺 Escalation Assessment",
            "🤝 CBM Recommendations",
            "🏛️ Domestic Politics",
            "⚠️ Spoiler Analysis",
            "🌐 Multi-Track Coordination"
        ])

        # TAB 1: Escalation Assessment
        with peace_tabs[0]:
            st.markdown("### Escalation Risk Assessment")

            # Display scenario-specific context
            if st.session_state.scenario_config:
                st.markdown(f"""
                <div style="background-color: #e3f2fd; padding: 12px; border-radius: 5px; border-left: 4px solid #1976d2; margin-bottom: 15px;">
                    <p style="color: #000; margin: 0;"><strong>Scenario Context:</strong> {st.session_state.scenario_config['escalation_context']}</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background-color: #fff8dc; padding: 12px; border-radius: 5px; border-left: 4px solid #ffa500;">
                <p style="color: #000; margin: 0;"><strong>Current Escalation Level:</strong> Level {}</p>
                <p style="color: #333; margin: 5px 0 0 0; font-size: 14px;">{}</p>
            </div>
            """.format(
                st.session_state.escalation_manager.current_level.value.split('_')[0][-1],
                st.session_state.escalation_manager.current_level.value.replace('_', ' ').title()
            ), unsafe_allow_html=True)

            st.markdown("#### Assess Proposed Action")
            proposed_action = st.text_area(
                "Describe the action to assess:",
                placeholder="E.g., Deploy additional coast guard vessels to patrol disputed waters",
                height=100
            )

            if st.button("Assess Escalation Risk", type="primary"):
                if proposed_action:
                    risk = st.session_state.escalation_manager.assess_escalation_risk(proposed_action)

                    # Calculate average strategic modifier across all parties
                    total_modifier = 0
                    party_modifiers = {}
                    for party_id, ctx in st.session_state.strategic_contexts.items():
                        modifier = ctx.get_escalation_modifier()
                        party_modifiers[party_id] = modifier
                        total_modifier += modifier
                    avg_modifier = total_modifier / len(st.session_state.strategic_contexts)

                    # Apply average strategic modifier to base risk
                    base_risk = risk['risk_level']
                    modified_risk = base_risk * avg_modifier

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        risk_color = "red" if base_risk > 0.6 else "orange" if base_risk > 0.3 else "green"
                        st.markdown(f"""
                        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center;">
                            <h3 style="color: {risk_color}; margin: 0;">{base_risk:.1%}</h3>
                            <p style="color: #333; margin: 5px 0 0 0;">Base Risk</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        modifier_color = "green" if avg_modifier < 1 else "red" if avg_modifier > 1 else "orange"
                        st.markdown(f"""
                        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center;">
                            <h3 style="color: {modifier_color}; margin: 0;">{avg_modifier:.2f}x</h3>
                            <p style="color: #333; margin: 5px 0 0 0;">Strategic Modifier</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col3:
                        final_color = "red" if modified_risk > 0.6 else "orange" if modified_risk > 0.3 else "green"
                        st.markdown(f"""
                        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center;">
                            <h3 style="color: {final_color}; margin: 0;">{modified_risk:.1%}</h3>
                            <p style="color: #333; margin: 5px 0 0 0;">Final Risk</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col4:
                        st.markdown(f"""
                        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center;">
                            <h3 style="color: #d32f2f; margin: 0;">{"YES" if risk['point_of_no_return'] else "NO"}</h3>
                            <p style="color: #333; margin: 5px 0 0 0;">Point of No Return</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Add explanation section
                    with st.expander("📖 Understanding These Metrics", expanded=False):
                        st.markdown("""
                        #### What These Numbers Mean

                        **Base Risk ({:.1%})**
                        - The escalation probability based on the action itself and current military parameters
                        - Calculated from: vessel proximity, patrol patterns, prenotification levels, military posturing
                        - Higher percentages indicate greater likelihood of unintended escalation
                        - **Interpretation**:
                          - 0-20%: Low risk (routine operations)
                          - 20-40%: Moderate risk (heightened tensions)
                          - 40-60%: High risk (dangerous brinkmanship)
                          - 60%+: Critical risk (likely escalation)

                        **Strategic Modifier ({:.2f}x)**
                        - How soft power dimensions adjust the base risk
                        - Averaged across all parties' strategic positioning:
                          - **Diplomatic Capital**: Ability to influence through diplomacy
                          - **International Legitimacy**: Support from international community
                          - **Domestic Support**: Public backing for negotiation strategy
                          - **Credibility**: Reputation for following through on commitments
                        - **Interpretation**:
                          - <1.0 (green): Strong strategic position reduces escalation risk
                          - =1.0 (orange): Neutral - strategic factors have no net effect
                          - >1.0 (red): Weak strategic position increases escalation risk

                        **Final Risk ({:.1%})**
                        - The **actual escalation probability** = Base Risk × Strategic Modifier
                        - This is the most important metric - it combines hard military factors with soft power realities
                        - Example: A 40% base risk with 0.85x modifier = 34% final risk (strategic positioning helped!)
                        - **Use this number** when evaluating whether an action is too dangerous

                        **Point of No Return ({})**
                        - Whether the action crosses a critical threshold where de-escalation becomes extremely difficult
                        - Based on: irreversible commitments, casualties, sovereignty violations, public humiliation
                        - **YES** means the action likely triggers dynamics that are very hard to reverse (sunk costs, audience costs, honor)
                        - **NO** means there are still diplomatic off-ramps available

                        #### Academic Grounding
                        - **Base Risk Assessment**: Schelling (1960) on inadvertent escalation, Jervis (1976) on spiral model
                        - **Strategic Modifiers**: Nye (2004) on soft power, Putnam (1988) on domestic constraints
                        - **Point of No Return**: Fearon (1994) on audience costs, Kahneman & Tversky (1979) on sunk cost fallacy
                        """.format(base_risk, avg_modifier, modified_risk, "YES" if risk['point_of_no_return'] else "NO"))

                    # Display party-specific modifiers
                    st.markdown("#### Strategic Position Impact by Party")
                    party_names = {
                        "PH_GOV": "🇵🇭 Philippines",
                        "PRC_MARITIME": "🇨🇳 PRC Maritime",
                        "VN_CG": "🇻🇳 Vietnam",
                        "MY_CG": "🇲🇾 Malaysia"
                    }

                    cols_parties = st.columns(4)
                    for idx, (party_id, modifier) in enumerate(party_modifiers.items()):
                        with cols_parties[idx]:
                            modifier_pct = abs((1 - modifier) * 100)
                            color = "green" if modifier < 1 else "red" if modifier > 1 else "orange"
                            direction = "↓" if modifier < 1 else "↑" if modifier > 1 else "="
                            st.markdown(f"""
                            <div style="background-color: {color}15; padding: 10px; border-radius: 5px; border-left: 3px solid {color};">
                                <p style="color: #666; font-size: 11px; margin: 0;">{party_names.get(party_id, party_id)}</p>
                                <h4 style="color: {color}; margin: 5px 0;">{direction} {modifier:.2f}x</h4>
                            </div>
                            """, unsafe_allow_html=True)

                    st.markdown("#### Likely Counter-Escalation")
                    for i, response in enumerate(risk['likely_counter_escalation'], 1):
                        st.markdown(f"""
                        <div style="background-color: #fff3cd; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #ff9800;">
                            <p style="color: #000; margin: 0;"><strong>{i}.</strong> {response}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("#### De-escalation Windows")
                    for i, window in enumerate(risk['de_escalation_windows'], 1):
                        st.markdown(f"""
                        <div style="background-color: #d4edda; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #28a745;">
                            <p style="color: #000; margin: 0;"><strong>{i}.</strong> {window}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Please describe an action to assess.")

            st.markdown("---")
            st.markdown("#### Recommended De-escalation Sequence")
            st.markdown("<p style='color: #333;'>Based on Osgood's GRIT (Graduated Reciprocation in Tension-reduction):</p>", unsafe_allow_html=True)
            sequence = st.session_state.escalation_manager.recommend_de_escalation_sequence()
            for i, step in enumerate(sequence, 1):
                st.markdown(f"""
                <div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #2196f3;">
                    <p style="color: #000; margin: 0;"><strong>Step {i}:</strong> {step}</p>
                </div>
                """, unsafe_allow_html=True)

        # TAB 2: CBM Recommendations
        with peace_tabs[1]:
            st.markdown("### Confidence-Building Measures Library")

            # Display scenario-specific CBM priorities
            if st.session_state.scenario_config:
                priorities = st.session_state.scenario_config.get('cbm_priorities', [])
                st.markdown(f"""
                <div style="background-color: #e8f5e9; padding: 12px; border-radius: 5px; border-left: 4px solid #4caf50; margin-bottom: 15px;">
                    <p style="color: #000; margin: 0;"><strong>Priority CBMs for {st.session_state.scenario_config['name']}:</strong></p>
                    <ul style="color: #333; margin: 5px 0 0 0;">
                        {"".join([f"<li>{p.replace('_', ' ').title()}</li>" for p in priorities])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

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
                        <p style="color: #000; margin: 5px 0;"><strong>Category:</strong> <span style="color: #333;">{cbm.category.value.replace('_', ' ').title()}</span></p>
                        <p style="color: #000; margin: 5px 0;"><strong>Description:</strong> <span style="color: #333;">{cbm.description}</span></p>
                        <div style="display: flex; gap: 20px; margin-top: 10px;">
                            <div style="background-color: #fff; padding: 8px 12px; border-radius: 4px; border: 1px solid #ddd;">
                                <p style="color: #000; margin: 0; font-size: 14px;"><strong>Trust Building:</strong> <span style="color: #333;">{cbm.trust_building_value:.1f}/1.0</span></p>
                            </div>
                            <div style="background-color: #fff; padding: 8px 12px; border-radius: 4px; border: 1px solid #ddd;">
                                <p style="color: #000; margin: 0; font-size: 14px;"><strong>Risk Reduction:</strong> <span style="color: #333;">{cbm.risk_reduction_value:.1f}/1.0</span></p>
                            </div>
                            <div style="background-color: #fff; padding: 8px 12px; border-radius: 4px; border: 1px solid #ddd;">
                                <p style="color: #000; margin: 0; font-size: 14px;"><strong>Timeline:</strong> <span style="color: #333;">{cbm.timeline_weeks} weeks</span></p>
                            </div>
                            <div style="background-color: #fff; padding: 8px 12px; border-radius: 4px; border: 1px solid #ddd;">
                                <p style="color: #000; margin: 0; font-size: 14px;"><strong>Cost:</strong> <span style="color: #333;">{cbm.cost_level.title()}</span></p>
                            </div>
                        </div>
                        <details style="margin-top: 10px;">
                            <summary style="color: #1976d2; cursor: pointer; font-weight: bold;">Implementation Steps</summary>
                            <ul style="color: #333; margin: 10px 0;">
                                {"".join([f"<li>{step}</li>" for step in cbm.implementation_steps])}
                            </ul>
                        </details>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### Browse CBMs by Category")
            category = st.selectbox(
                "Select Category",
                [cat.value.replace('_', ' ').title() for cat in CBMCategory]
            )
            category_enum = [cat for cat in CBMCategory if cat.value.replace('_', ' ').title() == category][0]
            cbms_in_category = st.session_state.cbm_library.get_cbms_by_category(category_enum)

            st.markdown(f"<p style='color: #333;'><strong>{len(cbms_in_category)} CBMs</strong> in this category:</p>", unsafe_allow_html=True)
            for cbm in cbms_in_category:
                with st.expander(f"{cbm.name}"):
                    st.markdown(f"<p style='color: #333;'><strong>Description:</strong> {cbm.description}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color: #333;'><strong>Trust Building:</strong> {cbm.trust_building_value:.1f} | <strong>Risk Reduction:</strong> {cbm.risk_reduction_value:.1f}</p>", unsafe_allow_html=True)

        # TAB 3: Domestic Politics
        with peace_tabs[2]:
            st.markdown("### Domestic Political Constraints Analysis")
            st.markdown("<p style='color: #333;'>Based on Putnam's Two-Level Game Theory</p>", unsafe_allow_html=True)

            # Get scenario-specific parties
            available_parties = ["Philippines", "China"]
            if st.session_state.scenario_config:
                scenario_parties = st.session_state.scenario_config.get('parties', [])
                st.markdown(f"""
                <div style="background-color: #fff8e1; padding: 12px; border-radius: 5px; border-left: 4px solid #ffa500; margin-bottom: 15px;">
                    <p style="color: #000; margin: 0;"><strong>Parties in this scenario:</strong> {', '.join([p.replace('_', ' ') for p in scenario_parties])}</p>
                </div>
                """, unsafe_allow_html=True)

                # Map party IDs to friendly names
                party_map = {
                    "PH_GOV": "Philippines",
                    "PRC_MARITIME": "China",
                    "MY_CG": "Malaysia",
                    "VN_CG": "Vietnam"
                }
                available_parties = [party_map.get(p, p) for p in scenario_parties if p in party_map]

            party_select = st.selectbox(
                "Select Party to Analyze",
                available_parties if available_parties else ["Philippines", "China"],
                key="domestic_party"
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
                <p style="color: #333; margin: 0;"><strong>Win-Set Size:</strong> {analyzer.win_set_size:.2f}</p>
                <p style="color: #555; margin: 5px 0 0 0; font-size: 14px;">
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
                st.markdown("<p style='color: #333;'>No absolute deal-breakers identified at current intensity levels.</p>", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### Test Proposal Against Domestic Constraints")

            if st.session_state.current_offer:
                st.markdown("<p style='color: #333;'>Testing current proposal...</p>", unsafe_allow_html=True)

                # Create test proposal based on current offer
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
                        <p style="color: #333; margin: 5px 0 0 0;">Acceptable</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center;">
                        <h3 style="color: #1976d2; margin: 0;">{result['overall_support']:.0%}</h3>
                        <p style="color: #333; margin: 5px 0 0 0;">Overall Support</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; text-align: center;">
                        <h3 style="color: #ff9800; margin: 0;">{result['ratification_probability']:.0%}</h3>
                        <p style="color: #333; margin: 5px 0 0 0;">Ratification Prob.</p>
                    </div>
                    """, unsafe_allow_html=True)

                if result['objectors']:
                    st.markdown("#### Domestic Objections")
                    for obj in result['objectors']:
                        st.markdown(f"""
                        <div style="background-color: #fff3cd; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #ff9800;">
                            <p style="color: #000; margin: 0;"><strong>{obj['actor']}:</strong> <span style="color: #333;">{obj['issue']}</span></p>
                            <p style="color: #555; margin: 5px 0 0 0; font-size: 14px;">
                                Requires: {obj['required']} | Proposed: {obj['proposed']}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                if result['required_compensations']:
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
                st.info("Build an agreement in Step 2 first to test domestic acceptability.")

        # TAB 4: Spoiler Analysis
        with peace_tabs[3]:
            st.markdown("### Spoiler Threat Analysis")
            st.markdown("<p style='color: #333;'>Based on Stedman's Spoiler Problem Framework</p>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background-color: #fff3e0; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #000; margin: 0 0 10px 0;">Identified Spoilers</h4>
                <p style="color: #333; margin: 0;"><strong>{len(st.session_state.spoiler_manager.spoilers)}</strong> potential spoilers tracked</p>
            </div>
            """, unsafe_allow_html=True)

            for name, spoiler in st.session_state.spoiler_manager.spoilers.items():
                with st.expander(f"{'🔴' if spoiler.capability.value == 'high' else '🟡' if spoiler.capability.value == 'medium' else '🟢'} {name}"):
                    st.markdown(f"""
                    <div style="background-color: #fafafa; padding: 10px; border-radius: 5px;">
                        <p style="color: #000; margin: 5px 0;"><strong>Type:</strong> <span style="color: #333;">{spoiler.spoiler_type.value.title()}</span></p>
                        <p style="color: #000; margin: 5px 0;"><strong>Capability:</strong> <span style="color: #333;">{spoiler.capability.value.title()}</span></p>
                        <p style="color: #000; margin: 5px 0;"><strong>Position:</strong> <span style="color: #333;">{spoiler.position.value.title()}</span></p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<p style='color: #000; margin: 10px 0 5px 0;'><strong>Interests Threatened:</strong></p>", unsafe_allow_html=True)
                    for interest in spoiler.interests_threatened:
                        st.markdown(f"<p style='color: #333; margin: 2px 0; padding-left: 15px;'>• {interest}</p>", unsafe_allow_html=True)

                    st.markdown("<p style='color: #000; margin: 10px 0 5px 0;'><strong>Typical Spoiling Actions:</strong></p>", unsafe_allow_html=True)
                    for action in spoiler.typical_spoiling_actions[:3]:
                        st.markdown(f"<p style='color: #333; margin: 2px 0; padding-left: 15px;'>• {action}</p>", unsafe_allow_html=True)

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

            if st.session_state.current_offer and st.button("Assess Spoiler Risk", type="primary"):
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

                if risk['high_threat_spoilers']:
                    st.markdown("#### High-Threat Spoilers")
                    for spoiler_name in risk['high_threat_spoilers']:
                        st.markdown(f"""
                        <div style="background-color: #ffcdd2; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #f44336;">
                            <p style="color: #000; margin: 0;">⚠️ {spoiler_name}</p>
                        </div>
                        """, unsafe_allow_html=True)

                if risk['likely_spoiling_actions']:
                    st.markdown("#### Likely Spoiling Actions")
                    for action in risk['likely_spoiling_actions'][:5]:
                        st.markdown(f"<p style='color: #333; margin: 5px 0; padding-left: 15px;'>• {action}</p>", unsafe_allow_html=True)

                if risk['protective_measures_needed']:
                    st.markdown("#### Protective Measures Needed")
                    for measure in risk['protective_measures_needed']:
                        st.markdown(f"""
                        <div style="background-color: #e3f2fd; padding: 8px; border-radius: 4px; margin: 5px 0;">
                            <p style="color: #000; margin: 0; font-size: 14px;">🛡️ {measure}</p>
                        </div>
                        """, unsafe_allow_html=True)
            elif not st.session_state.current_offer:
                st.info("Build an agreement in Step 2 first to assess spoiler risk.")

        # TAB 5: Multi-Track Coordination
        with peace_tabs[4]:
            st.markdown("### Multi-Track Diplomacy Coordination")
            st.markdown("<p style='color: #333;'>Based on McDonald & Diamond's Multi-Track Framework</p>", unsafe_allow_html=True)

            conflict_phase = st.selectbox(
                "Select Conflict Phase",
                ["pre_negotiation", "negotiation", "implementation"],
                format_func=lambda x: {
                    "pre_negotiation": "Pre-Negotiation (Building Foundation)",
                    "negotiation": "Negotiation (Supporting Talks)",
                    "implementation": "Implementation (Monitoring & Support)"
                }[x]
            )

            if st.button("Get Track Recommendations", type="primary"):
                recommendations = st.session_state.multi_track_mediator.recommend_track_sequence(conflict_phase)

                st.markdown(f"#### Recommended Diplomatic Tracks for {conflict_phase.replace('_', ' ').title()}")

                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div style="background-color: #f5f5f5; padding: 15px; border-radius: 8px; margin: 15px 0; border: 1px solid #ddd;">
                        <h4 style="color: #1976d2; margin: 0 0 10px 0;">{i}. {rec['track'].value.replace('_', ' ').title()}</h4>
                        <p style="color: #000; margin: 5px 0;"><strong>Activity:</strong> <span style="color: #333;">{rec['activity']}</span></p>
                        <p style="color: #000; margin: 5px 0;"><strong>Purpose:</strong> <span style="color: #333;">{rec['purpose']}</span></p>
                        <p style="color: #000; margin: 5px 0;"><strong>Participants:</strong> <span style="color: #333;">{rec['participants']}</span></p>
                        <p style="color: #000; margin: 5px 0;"><strong>Timeline:</strong> <span style="color: #333;">{rec['timeline']}</span></p>
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
                    st.markdown(f"<p style='color: #333;'>{description}</p>", unsafe_allow_html=True)

        st.markdown("---")
        if st.button("📊 Back to Analysis", use_container_width=True):
            st.session_state.workflow_step = 5
            st.rerun()

# ==================== PARTY VIEW ====================

def party_view():
    """Enhanced party-specific view"""
    party_id = st.session_state.user_role

    party_info = {
        "PH_GOV": {
            "name": "🇵🇭 Philippines Government",
            "color": "#0038A8",
            "interests": [
                "Maintain sovereignty over territorial waters",
                "Ensure safe passage for resupply missions",
                "Protect fishermen's livelihoods",
                "Avoid military escalation"
            ],
            "batna": "Continue ad-hoc resupply with risk of confrontation",
            "concerns": ["Personnel safety", "National prestige", "Operational access"],
            "constraints": ["International law (UNCLOS)", "Domestic politics", "Alliance relationships"]
        },
        "PRC_MARITIME": {
            "name": "🇨🇳 PRC Maritime Forces",
            "color": "#DE2910",
            "interests": [
                "Assert historical claims in South China Sea",
                "Maintain strategic control over waters",
                "Prevent normalization of Philippine presence",
                "Avoid international condemnation"
            ],
            "batna": "Continue blockade and harassment tactics",
            "concerns": ["Strategic control", "National face", "Regional influence"],
            "constraints": ["International scrutiny", "Regional relationships", "Domestic expectations"]
        },
        "VN_CG": {
            "name": "🇻🇳 Vietnam Coast Guard",
            "color": "#DA251D",
            "interests": [
                "Protect fishing rights in traditional grounds",
                "Prevent Chinese expansion",
                "Maintain regional balance",
                "Economic development"
            ],
            "batna": "Unilateral fishing patrols with confrontation risk",
            "concerns": ["Economic interests", "Security", "Regional stability"],
            "constraints": ["Military limitations", "Economic ties with China", "ASEAN solidarity"]
        },
        "MY_CG": {
            "name": "🇲🇾 Malaysia Coast Guard",
            "color": "#CC0001",
            "interests": [
                "Protect EEZ boundaries",
                "Secure energy resources",
                "Maintain neutrality",
                "Economic development"
            ],
            "batna": "Diplomatic protest with limited enforcement",
            "concerns": ["Energy security", "Economic interests", "Regional relations"],
            "constraints": ["Military capacity", "Economic interests", "ASEAN role"]
        }
    }

    info = party_info.get(party_id, party_info["PH_GOV"])

    st.title(info["name"])
    st.markdown(f"**Your Role:** Negotiating Party")

    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Your Session")
        st.info(f"**Party:** {info['name']}")
        if st.session_state.session_id:
            st.success(f"**Session:** Active")
        else:
            st.warning("**Session:** Waiting for facilitator")

        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_role = None
            st.rerun()

        st.markdown("---")

        # AI Guide
        with st.expander("💬 AI Guide", expanded=False):
            st.markdown("**🤖 Mediator Assistant**")
            st.caption("AI-powered guidance for participants")

            # Initialize AI guide in session state with persistence (separate from instructor)
            if 'participant_ai_guide' not in st.session_state:
                try:
                    # Create guide with unique session ID per party
                    participant_session_id = f"participant_{party_id}"
                    st.session_state.participant_ai_guide = create_participant_guide(
                        api_key=st.session_state.anthropic_api_key or None,
                        session_id=participant_session_id,
                        enable_persistence=True
                    )
                    # Load existing chat history from persisted data
                    st.session_state.participant_chat_history = [
                        {
                            "question": msg.content,
                            "response": st.session_state.participant_ai_guide.conversation_history[i+1].content if i+1 < len(st.session_state.participant_ai_guide.conversation_history) else "",
                            "sources": "Loaded from history"
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
                context_data = {
                    "scenario": st.session_state.get('selected_scenario'),
                    "party": party_id
                }
                st.session_state.participant_ai_guide.set_context(**context_data)

                # Quick tips
                st.markdown("**Quick Tips:**")
                tips = st.session_state.participant_ai_guide.get_quick_tips()
                for tip in tips[:3]:  # Show first 3 tips
                    st.info(tip)

                st.markdown("---")

                # Chat interface
                st.markdown("**Ask a Question:**")
                user_question = st.text_area("Your question:", key="participant_ai_question", height=80)

                if st.button("Ask Assistant", key="participant_ask_btn", use_container_width=True):
                    if user_question:
                        with st.spinner("Thinking..."):
                            try:
                                # Set simulation parameters for context-aware guidance
                                sim_params = {
                                    "standoff": "Distance (nm) between conflicting vessels (0-10, higher = less tension)",
                                    "escort": "Military escort intensity level (0-10, higher = more aggressive)",
                                    "prenotify": "Pre-notification requirements (0-10, higher = more transparency)",
                                    "hotline": "Communication channel status (None/Ad-hoc/Dedicated)",
                                    "embargo": "Economic pressure level (0-10)",
                                    "traditional_access": "Fishing rights for traditional fishermen (0-100%)",
                                    "seasonal_closure": "Days per year fishing is closed (0-180 days)",
                                    "patrol_frequency": "Joint patrol frequency (None/Monthly/Weekly/Daily)",
                                    "revenue_split": "Resource revenue sharing percentage (0-100%)",
                                    "moratorium_months": "Development freeze duration (0-36 months)",
                                    "boundary_method": "EEZ delimitation approach (Equidistance/Natural prolongation/Special circumstances)",
                                    "patrol_coordination": "Patrol cooperation level (Independent/Info sharing/Joint)",
                                    "buffer_zone_nm": "Neutral buffer zone width (0-50 nautical miles)"
                                }
                                st.session_state.participant_ai_guide.set_simulation_parameters(sim_params)

                                # Pass strategic context to AI Guide
                                from scs_mediator_sdk.dynamics.strategic_context import get_available_actions
                                party_strategic_context = st.session_state.strategic_contexts.get(party_id, st.session_state.strategic_contexts["PH_GOV"])
                                strategic_summary = party_strategic_context.get_summary()
                                strategic_context_info = {
                                    "strategic_actions_available": [
                                        f"{action.name}: {action.description} (Risk: {action.risk_level})"
                                        for action in get_available_actions(party_strategic_context)
                                    ],
                                    "diplomatic_capital": f"{strategic_summary['diplomatic_capital']['value']:.0f}/100 ({strategic_summary['diplomatic_capital']['status']})",
                                    "international_legitimacy": f"{strategic_summary['international_legitimacy']['value']:.0f}/100 ({strategic_summary['international_legitimacy']['status']})",
                                    "domestic_support": f"{strategic_summary['domestic_support']['value']:.0f}/100 ({strategic_summary['domestic_support']['status']})",
                                    "credibility": f"{strategic_summary['credibility']['value']:.0f}/100 ({strategic_summary['credibility']['status']})",
                                    "escalation_modifier": f"{strategic_summary['escalation_modifier']:.2f}x ({'reduces' if strategic_summary['escalation_modifier'] < 1 else 'increases'} risk)"
                                }
                                # Add strategic context to simulation parameters
                                sim_params.update(strategic_context_info)

                                result = st.session_state.participant_ai_guide.ask(user_question)
                                st.session_state.participant_chat_history.append({
                                    "question": user_question,
                                    "response": result["response"],
                                    "sources": result["sources"]
                                })
                            except Exception as e:
                                st.error(f"Error: {str(e)}")

                # Display chat history (most recent first)
                if st.session_state.get('participant_chat_history'):
                    st.markdown("---")
                    st.markdown("**Recent Conversation:**")
                    for idx, chat in enumerate(reversed(st.session_state.participant_chat_history[-2:])):  # Show last 2 full
                        with st.expander(f"Q: {chat['question'][:70]}...", expanded=(idx==0)):
                            st.markdown(f"**Question:** {chat['question']}")
                            st.markdown(f"**Answer:** {chat['response']}")
                            # Academic citations are inline in the response

                if st.button("Clear History", key="participant_clear_history"):
                    st.session_state.participant_ai_guide.clear_history()
                    st.session_state.participant_chat_history = []
                    st.rerun()

    # Main tabs
    tabs = st.tabs(["📋 Your Position", "📝 Current Proposal", "💭 Make Offer", "📊 Your Strategy", "🕊️ Peace Context"])

    with tabs[0]:
        st.markdown("### Your Mandate & Objectives")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🎯 Your Interests")
            for interest in info["interests"]:
                st.markdown(f"- {interest}")

            st.markdown("")
            st.markdown("#### ⚠️ Your BATNA")
            st.info(info["batna"])
            st.caption("BATNA = Best Alternative To a Negotiated Agreement (your fallback option)")

        with col2:
            st.markdown("#### 🔑 Key Concerns")
            for concern in info["concerns"]:
                st.markdown(f"- {concern}")

            st.markdown("")
            st.markdown("#### 🚧 Constraints")
            for constraint in info["constraints"]:
                st.markdown(f"- {constraint}")

        st.markdown("---")
        st.info("💡 **Remember**: Never accept an offer below your BATNA! Aim for utility > 0.5 for a good agreement.")

    with tabs[1]:
        st.markdown("### Current Proposal on the Table")

        if st.session_state.current_offer:
            st.json(st.session_state.current_offer)

            st.markdown("---")
            st.markdown("### Your Utility from This Proposal")

            if st.button("🔍 Calculate My Utility", type="primary"):
                try:
                    case_id = st.session_state.session_id or "demo_case"
                    # Evaluate offer directly using bargaining session (no API needed)
                    session = st.session_state.bargaining_sessions.get(case_id)
                    if not session:
                        st.error("❌ Session not found. Please ask the instructor to start a new session.")
                        result = None
                    else:
                        av = AgreementVector(st.session_state.current_offer)
                        result = session.evaluate_offer(party_id, av)

                    if result:
                        my_utility = result['utilities'].get(party_id, 0)
                        my_acceptance = result['acceptance_prob'].get(party_id, 0)

                    col1, col2 = st.columns(2)
                    with col1:
                        if my_utility > 0.7:
                            st.success(f"### Your Utility: {my_utility:.1%}")
                            st.write("✅ Excellent offer for you!")
                        elif my_utility > 0.5:
                            st.info(f"### Your Utility: {my_utility:.1%}")
                            st.write("👍 Good offer, acceptable")
                        elif my_utility > 0.4:
                            st.warning(f"### Your Utility: {my_utility:.1%}")
                            st.write("⚠️ Marginal - at your BATNA threshold")
                        else:
                            st.error(f"### Your Utility: {my_utility:.1%}")
                            st.write("❌ Below your BATNA! Should reject or counter")

                    with col2:
                        st.metric("Your Acceptance Probability", f"{my_acceptance:.1%}")
                        st.progress(my_acceptance)

                except Exception as e:
                    st.error(f"Could not calculate utility: {e}")
        else:
            st.info("⏳ No proposal currently on the table. Waiting for offers...")

    with tabs[2]:
        st.markdown("### Make Your Counter-Offer")
        st.markdown("Adjust the terms below to propose your preferred agreement.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 🚢 Resupply Operations")
            standoff = st.slider("Standoff (nm)", 0, 10, 3, key="party_standoff")
            escort = st.slider("Max Escorts", 0, 5, 1, key="party_escort")
            prenotify = st.slider("Notice (hours)", 0, 48, 12, key="party_notify")

        with col2:
            st.markdown("#### 📞 Communications")
            hotline = st.selectbox("Hotline", ["ad_hoc", "24_7"], index=1, key="party_hotline",
                                  format_func=lambda x: "24/7" if x == "24_7" else "Ad-Hoc")
            cues = st.multiselect("CUES Requirements",
                                 ["distance", "AIS_on", "video_record"],
                                 default=["distance", "AIS_on"], key="party_cues")

        with col3:
            st.markdown("#### 📰 Media")
            embargo = st.slider("Embargo (hours)", 0, 48, 6, key="party_embargo")

        offer = {
            "resupply_SOP": {"standoff_nm": standoff, "escort_count": escort, "pre_notification_hours": prenotify},
            "hotline_cues": {"hotline_status": hotline, "cues_checklist": cues},
            "media_protocol": {"embargo_hours": embargo}
        }

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Preview My Utility", type="secondary", use_container_width=True):
                try:
                    case_id = st.session_state.session_id or "demo_case"
                    # Evaluate offer directly using bargaining session (no API needed)
                    session = st.session_state.bargaining_sessions.get(case_id)
                    if not session:
                        st.error("❌ Session not found. Please ask the instructor to start a new session.")
                    else:
                        av = AgreementVector(offer)
                        result = session.evaluate_offer(party_id, av)
                        my_utility = result['utilities'].get(party_id, 0)
                        st.info(f"Your utility from this offer: **{my_utility:.1%}**")
                except Exception as e:
                    st.error(f"Preview failed: {e}")

        with col2:
            if st.button("📤 Submit Offer", type="primary", use_container_width=True):
                st.session_state.current_offer = offer
                st.success("✅ Offer submitted to mediator! Waiting for response...")

    with tabs[3]:
        st.markdown("### Your Strategic Position")
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; border-left: 5px solid #4682b4; margin-bottom: 20px;">
            <p style="color: #000; margin: 0;"><strong>Strategic Leverage & Soft Power</strong></p>
            <p style="color: #333; margin: 10px 0 0 0; font-size: 14px;">
                Beyond parameters, strategic actions affect your diplomatic capital, international legitimacy,
                domestic support, and credibility. These dimensions influence escalation risk and outcome sustainability.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Get strategic context for this party
        ctx = st.session_state.strategic_contexts.get(party_id, st.session_state.strategic_contexts["PH_GOV"])
        summary = ctx.get_summary()

        # Strategic Context Dashboard
        st.markdown("#### Your Strategic Metrics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            val = summary['diplomatic_capital']['value']
            status = summary['diplomatic_capital']['status']
            color = '#2ca02c' if val >= 60 else '#ff7f0e' if val >= 40 else '#d62728'
            st.markdown(f"""
            <div style="background-color: {color}15; padding: 15px; border-radius: 8px; border-left: 5px solid {color};">
                <p style="color: #666; font-size: 12px; margin: 0;">DIPLOMATIC CAPITAL</p>
                <h2 style="color: {color}; margin: 5px 0;">{val:.0f}</h2>
                <p style="color: #666; font-size: 11px; margin: 0;">{status}</p>
            </div>
            """, unsafe_allow_html=True)
            st.caption(summary['diplomatic_capital']['description'])

        with col2:
            val = summary['international_legitimacy']['value']
            status = summary['international_legitimacy']['status']
            color = '#2ca02c' if val >= 60 else '#ff7f0e' if val >= 40 else '#d62728'
            st.markdown(f"""
            <div style="background-color: {color}15; padding: 15px; border-radius: 8px; border-left: 5px solid {color};">
                <p style="color: #666; font-size: 12px; margin: 0;">INT'L LEGITIMACY</p>
                <h2 style="color: {color}; margin: 5px 0;">{val:.0f}</h2>
                <p style="color: #666; font-size: 11px; margin: 0;">{status}</p>
            </div>
            """, unsafe_allow_html=True)
            st.caption(summary['international_legitimacy']['description'])

        with col3:
            val = summary['domestic_support']['value']
            status = summary['domestic_support']['status']
            color = '#2ca02c' if val >= 60 else '#ff7f0e' if val >= 40 else '#d62728'
            st.markdown(f"""
            <div style="background-color: {color}15; padding: 15px; border-radius: 8px; border-left: 5px solid {color};">
                <p style="color: #666; font-size: 12px; margin: 0;">DOMESTIC SUPPORT</p>
                <h2 style="color: {color}; margin: 5px 0;">{val:.0f}</h2>
                <p style="color: #666; font-size: 11px; margin: 0;">{status}</p>
            </div>
            """, unsafe_allow_html=True)
            st.caption(summary['domestic_support']['description'])

        with col4:
            val = summary['credibility']['value']
            status = summary['credibility']['status']
            color = '#2ca02c' if val >= 60 else '#ff7f0e' if val >= 40 else '#d62728'
            st.markdown(f"""
            <div style="background-color: {color}15; padding: 15px; border-radius: 8px; border-left: 5px solid {color};">
                <p style="color: #666; font-size: 12px; margin: 0;">CREDIBILITY</p>
                <h2 style="color: {color}; margin: 5px 0;">{val:.0f}</h2>
                <p style="color: #666; font-size: 11px; margin: 0;">{status}</p>
            </div>
            """, unsafe_allow_html=True)
            st.caption(summary['credibility']['description'])

        # Escalation modifier impact
        modifier = summary['escalation_modifier']
        modifier_pct = (1 - modifier) * 100 if modifier < 1 else (modifier - 1) * 100
        modifier_direction = "reduces" if modifier < 1 else "increases"
        st.info(f"Your strategic position {modifier_direction} escalation risk by {abs(modifier_pct):.1f}% (modifier: {modifier:.2f}x)")

        st.markdown("---")

        # Strategic Actions
        st.markdown("#### Available Strategic Actions")
        st.markdown("Select a strategic action to improve your position. Each action affects both parameters and strategic metrics.")

        from scs_mediator_sdk.dynamics.strategic_context import get_available_actions, STRATEGIC_ACTIONS_LIBRARY

        available_actions = get_available_actions(ctx)

        if not available_actions:
            st.warning("No strategic actions currently available. Some actions require minimum thresholds (e.g., diplomatic capital > 30).")
        else:
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

                    if st.button(f"Execute: {action.name}", key=f"execute_{action.name}"):
                        # Apply action to strategic context
                        ctx.apply_action(action)
                        st.success(f"✅ {action.name} executed!")
                        st.balloons()
                        st.rerun()

        st.markdown("---")

        # Strategy Notes (kept from original)
        st.markdown("#### Strategy Notes")
        notes = st.text_area(
            "Track your approach and decision-making",
            height=150,
            placeholder="What are your priorities?\nWhat concessions can you make?\nWhat are your red lines?\nHow is the negotiation progressing?"
        )

        if st.button("💾 Save Notes"):
            st.success("Notes saved (session only)")

    with tabs[4]:
        st.markdown("### Peace Context Information (V2 Enhancement)")
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; border-left: 5px solid #4682b4; margin-bottom: 20px;">
            <p style="color: #000; margin: 0;"><strong>Understanding the Broader Peace Process</strong></p>
            <p style="color: #333; margin: 10px 0 0 0; font-size: 14px;">
                These tools help you understand the escalation dynamics, confidence-building opportunities,
                and domestic political realities that affect negotiations.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Current Escalation Level
        st.markdown("#### Current Escalation Level")
        current_level = st.session_state.escalation_manager.current_level
        level_num = current_level.value.split('_')[0][-1] if current_level.value[0].isdigit() else "1"
        level_description = current_level.value.replace('_', ' ').title()

        st.markdown(f"""
        <div style="background-color: {'#ffebee' if int(level_num) >= 7 else '#fff8e1' if int(level_num) >= 4 else '#e8f5e9'}; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <h3 style="color: #000; margin: 0;">Level {level_num}: {level_description}</h3>
            <p style="color: #333; margin: 10px 0 0 0; font-size: 14px;">
                {"⚠️ High tension - de-escalation urgently needed" if int(level_num) >= 7 else "⚡ Moderate tension - manage carefully" if int(level_num) >= 4 else "✓ Low tension - good foundation for talks"}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Strategic Context Impact on Escalation
        party_strategic_context = st.session_state.strategic_contexts.get(party_id, st.session_state.strategic_contexts["PH_GOV"])
        strategic_summary = party_strategic_context.get_summary()
        modifier = strategic_summary['escalation_modifier']
        modifier_pct = abs((1 - modifier) * 100) if modifier < 1 else abs((modifier - 1) * 100)

        if modifier < 1:
            # Reducing escalation
            color = "#e8f5e9"
            border_color = "#2ca02c"
            icon = "✓"
            message = f"Your strategic position reduces escalation risk by {modifier_pct:.1f}%"
            details = []
            if strategic_summary['international_legitimacy']['value'] > 70:
                details.append(f"• High international legitimacy ({strategic_summary['international_legitimacy']['value']:.0f}) → -15% risk")
            if strategic_summary['credibility']['value'] > 75:
                details.append(f"• Strong credibility ({strategic_summary['credibility']['value']:.0f}) → -10% risk")
            if strategic_summary['diplomatic_capital']['value'] > 70:
                details.append(f"• High diplomatic capital ({strategic_summary['diplomatic_capital']['value']:.0f}) → -15% risk")
        elif modifier > 1:
            # Increasing escalation
            color = "#ffebee"
            border_color = "#d62728"
            icon = "⚠️"
            message = f"Your strategic position increases escalation risk by {modifier_pct:.1f}%"
            details = []
            if strategic_summary['international_legitimacy']['value'] < 30:
                details.append(f"• Low international legitimacy ({strategic_summary['international_legitimacy']['value']:.0f}) → +20% risk")
            if strategic_summary['credibility']['value'] < 40:
                details.append(f"• Weak credibility ({strategic_summary['credibility']['value']:.0f}) → +25% risk")
            if strategic_summary['domestic_support']['value'] < 35:
                details.append(f"• Fragile domestic support ({strategic_summary['domestic_support']['value']:.0f}) → +30% risk")
        else:
            # Neutral
            color = "#fff8e1"
            border_color = "#ff7f0e"
            icon = "="
            message = "Your strategic position has neutral impact on escalation"
            details = ["• All strategic metrics are at moderate levels"]

        st.markdown(f"""
        <div style="background-color: {color}; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 5px solid {border_color};">
            <h4 style="color: #000; margin: 0;">{icon} Strategic Context Impact</h4>
            <p style="color: #333; margin: 10px 0 0 0; font-size: 14px;">
                {message}<br/>
                <strong>Escalation Modifier: {modifier:.2f}x</strong>
            </p>
            <p style="color: #666; margin: 10px 0 0 0; font-size: 12px;">
                {'<br/>'.join(details)}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.info("💡 **Tip:** Improve your strategic position in the 'Your Strategic Position' tab by executing strategic actions.")

        st.markdown("---")

        # Available CBMs for this scenario
        st.markdown("#### Confidence-Building Measures Available")
        st.markdown("<p style='color: #333;'>These measures can help reduce tensions and build trust:</p>", unsafe_allow_html=True)

        # Get recommended CBMs
        cbm_recs = st.session_state.cbm_library.recommend_cbm_sequence(
            current_trust_level=0.3,
            escalation_level=int(level_num),
            available_time_weeks=20
        )

        for i, cbm in enumerate(cbm_recs[:5], 1):  # Show top 5
            with st.expander(f"{i}. {cbm.name}"):
                st.markdown(f"<p style='color: #333;'><strong>Description:</strong> {cbm.description}</p>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="display: flex; gap: 15px; margin-top: 10px;">
                    <div style="background-color: #f9f9f9; padding: 8px 12px; border-radius: 4px;">
                        <p style="color: #000; margin: 0; font-size: 14px;"><strong>Trust Building:</strong> <span style="color: #333;">{cbm.trust_building_value:.1f}/1.0</span></p>
                    </div>
                    <div style="background-color: #f9f9f9; padding: 8px 12px; border-radius: 4px;">
                        <p style="color: #000; margin: 0; font-size: 14px;"><strong>Timeline:</strong> <span style="color: #333;">{cbm.timeline_weeks} weeks</span></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # Your party's domestic constraints
        st.markdown("#### Your Domestic Political Constraints")
        st.markdown("<p style='color: #333;'>These are the key political actors you must satisfy at home:</p>", unsafe_allow_html=True)

        # Get domestic actors for this party
        if party_id in ["PH_GOV"]:
            domestic_actors = create_philippines_domestic_actors()
            party_name = "Philippines"
        elif party_id in ["PRC_MARITIME"]:
            domestic_actors = create_china_domestic_actors()
            party_name = "China"
        else:
            domestic_actors = []
            party_name = "Your Country"

        if domestic_actors:
            for constraint in domestic_actors:
                st.markdown(f"""
                <div style="background-color: #f5f5f5; padding: 12px; border-radius: 5px; margin: 8px 0; border-left: 3px solid #1976d2;">
                    <p style="color: #000; margin: 0 0 5px 0;"><strong>{constraint.actor.value.replace('_', ' ').title()}</strong></p>
                    <p style="color: #333; margin: 0; font-size: 14px;"><strong>Position:</strong> {constraint.position}</p>
                    <p style="color: #333; margin: 5px 0 0 0; font-size: 14px;"><strong>Intensity:</strong> {constraint.intensity:.1f}/1.0 | <strong>Influence:</strong> {constraint.mobilization_capacity:.1f}/1.0</p>
                </div>
                """, unsafe_allow_html=True)

            # Win-set analysis
            analyzer = WinSetAnalyzer(party_name)
            for constraint in domestic_actors:
                analyzer.add_domestic_actor(constraint)

            st.markdown("---")
            st.markdown("#### Your Negotiation Flexibility")
            st.markdown(f"""
            <div style="background-color: #e3f2fd; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: #000; margin: 0 0 10px 0;">Win-Set Size</h4>
                <h2 style="color: #1976d2; margin: 0;">{analyzer.win_set_size:.2f}</h2>
                <p style="color: #555; margin: 10px 0 0 0; font-size: 14px;">
                    (1.0 = maximum flexibility to make deals, 0.0 = completely constrained by domestic politics)
                </p>
            </div>
            """, unsafe_allow_html=True)

            deal_breakers = analyzer.identify_deal_breakers()
            if deal_breakers:
                st.markdown("#### Your Domestic Red Lines")
                st.markdown("<p style='color: #333;'>These are non-negotiable due to strong domestic opposition:</p>", unsafe_allow_html=True)
                for db in deal_breakers:
                    st.markdown(f"""
                    <div style="background-color: #ffebee; padding: 10px; border-radius: 5px; margin: 5px 0; border-left: 3px solid #f44336;">
                        <p style="color: #000; margin: 0;">⛔ {db}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: #333;'>Domestic constraint information not available for this party.</p>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style="background-color: #fff8e1; padding: 15px; border-radius: 5px; border-left: 4px solid #ffa500; margin-top: 20px;">
            <p style="color: #000; margin: 0;"><strong>💡 How to Use This Information</strong></p>
            <ul style="color: #333; margin: 10px 0 0 0;">
                <li>Understand the current escalation level and avoid actions that raise it</li>
                <li>Propose CBMs to build trust and reduce tensions</li>
                <li>Be aware of your own domestic constraints when evaluating offers</li>
                <li>Consider what domestic pressures the other side faces</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==================== MAIN ====================

def main():
    """Main application entry point"""
    st.set_page_config(page_title="SCS Simulation", layout="wide", initial_sidebar_state="expanded")

    # Custom CSS for better visuals
    st.markdown("""
    <style>
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    init_session_state()

    # API key configuration in sidebar (available across all views)
    with st.sidebar:
        with st.expander("⚙️ AI Configuration", expanded=False):
            st.markdown("### API Key Setup")
            st.markdown("Enter your Anthropic API key to enable AI-powered features:")
            st.markdown("- AI Guide assistance")
            st.markdown("- LLM-enhanced escalation assessment")

            # API key input
            api_key_input = st.text_input(
                "Anthropic API Key",
                value=st.session_state.anthropic_api_key,
                type="password",
                help="Get your API key from https://console.anthropic.com/",
                key="api_key_input_widget"
            )

            # Update session state and environment when key changes
            if api_key_input != st.session_state.anthropic_api_key:
                st.session_state.anthropic_api_key = api_key_input
                if api_key_input:
                    os.environ["ANTHROPIC_API_KEY"] = api_key_input
                    st.success("✓ API key configured!")
                else:
                    if "ANTHROPIC_API_KEY" in os.environ:
                        del os.environ["ANTHROPIC_API_KEY"]
                    st.info("ℹ️ AI features will be disabled without an API key")

            # Status indicator
            if st.session_state.anthropic_api_key:
                st.success("🟢 AI features enabled")
            else:
                st.warning("🟡 AI features disabled")

    # Route to appropriate view
    if st.session_state.user_role is None:
        role_selection_page()
    elif st.session_state.user_role == "INSTRUCTOR":
        instructor_console()
    else:
        party_view()

if __name__ == "__main__":
    main()
