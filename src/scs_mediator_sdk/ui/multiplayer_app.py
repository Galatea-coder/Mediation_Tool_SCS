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

# Add src to path
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from scs_mediator_sdk.multiplayer import get_session_manager
from scs_mediator_sdk.sim.mesa_abm import MaritimeModel


# ==================== CONFIGURATION ====================

SCENARIOS = {
    'scenario_A': {
        'name': 'Second Thomas Shoal (Resupply)',
        'roles': ['PH_GOV', 'PRC_MARITIME'],
        'description': 'Philippine resupply missions to BRP Sierra Madre'
    },
    'scenario_B': {
        'name': 'Scarborough Shoal (Fishing)',
        'roles': ['PH_GOV', 'PRC_MARITIME'],
        'description': 'Traditional fishing grounds and access rights'
    }
}

ROLE_INFO = {
    'PH_GOV': {
        'name': '🇵🇭 Philippines',
        'color': '#0038A8',
        'interests': [
            'Maintain sovereignty over territorial waters',
            'Ensure safe resupply to garrison',
            'Protect fishermen's livelihoods'
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
        else:
            for player in session.players.values():
                status_icon = "✅" if player.ready else "⏳"
                role_name = ROLE_INFO[player.role]['name']
                st.markdown(f"{status_icon} **{role_name}** ({player.user_name}) - {'Ready' if player.ready else 'Connected'}")

        st.markdown("---")

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

            # Simple proposal builder
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🚢 Resupply Operations")
                standoff = st.slider("Standoff Distance (nm)", 0, 10, 3)
                escorts = st.slider("Maximum Escorts", 0, 5, 1)
                notification = st.slider("Pre-Notification (hours)", 0, 48, 24)

            with col2:
                st.markdown("#### 📞 Communication")
                hotline = st.selectbox("Hotline", ["24/7", "Ad-hoc"])
                st.markdown("#### 📰 Media")
                embargo = st.slider("News Embargo (hours)", 0, 48, 12)

            proposal_data = {
                'resupply_SOP': {
                    'standoff_nm': standoff,
                    'escort_count': escorts,
                    'pre_notification_hours': notification
                },
                'hotline_cues': {
                    'hotline_status': hotline.lower().replace('/', '_'),
                    'cues_checklist': ['distance', 'AIS_on']
                },
                'media_protocol': {
                    'embargo_hours': embargo
                }
            }

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
                # Show results
                st.subheader("📊 Simulation Results")

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
                    st.success("✅ Excellent outcome! Agreement is sustainable.")
                elif incidents < 40 and avg_sev < 0.6:
                    st.warning("⚠️ Mixed outcome. Agreement needs minor adjustments.")
                else:
                    st.error("❌ Concerning outcome. Agreement needs major revision.")

                if st.button("🔄 Start New Round"):
                    session.status = 'negotiating'
                    session.current_round += 1
                    st.rerun()


# ==================== PLAYER VIEW ====================

def player_view():
    """Player interface"""
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

        # Show player's role and interests
        st.markdown(f"## {role_info['name']}")

        st.markdown("""
        <div style="background-color: #e8f5e9; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <h4>Your Interests:</h4>
        </div>
        """, unsafe_allow_html=True)

        for interest in role_info['interests']:
            st.markdown(f"• {interest}")

        st.markdown("---")

        # Status messages
        if session.status == 'setup':
            st.info("⏳ Waiting for facilitator to start negotiation...")

            st.subheader("Other Players")
            for p in session.players.values():
                if p.player_id != player.player_id:
                    other_role_name = ROLE_INFO[p.role]['name']
                    st.markdown(f"✅ {other_role_name} ({p.user_name})")

        elif session.status == 'negotiating':
            st.subheader(f"Round {session.current_round}")

            latest_proposal = sm.get_latest_proposal(session.session_id)

            if not latest_proposal:
                st.info("⏳ Waiting for facilitator to propose terms...")
            else:
                st.markdown("### 📋 Proposed Agreement")

                # Display proposal in readable format
                proposal_data = latest_proposal.proposal_data

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### 🚢 Resupply Operations")
                    if 'resupply_SOP' in proposal_data:
                        sop = proposal_data['resupply_SOP']
                        st.markdown(f"• **Standoff Distance**: {sop.get('standoff_nm', 0)} nm")
                        st.markdown(f"• **Max Escorts**: {sop.get('escort_count', 0)}")
                        st.markdown(f"• **Pre-Notification**: {sop.get('pre_notification_hours', 0)} hours")

                with col2:
                    st.markdown("#### 📞 Communication & Media")
                    if 'hotline_cues' in proposal_data:
                        hotline = proposal_data['hotline_cues']
                        st.markdown(f"• **Hotline**: {hotline.get('hotline_status', 'N/A').upper()}")

                    if 'media_protocol' in proposal_data:
                        media = proposal_data['media_protocol']
                        st.markdown(f"• **News Embargo**: {media.get('embargo_hours', 0)} hours")

                st.markdown("---")

                # Check if player already responded
                responses = sm.get_proposal_responses(session.session_id, latest_proposal.proposal_id)
                player_response = next((r for r in responses if r.player_id == player.player_id), None)

                if player_response:
                    st.success(f"✅ You responded: **{player_response.response_type.upper()}**")

                    if player_response.explanation:
                        st.info(f"Your comment: \"{player_response.explanation}\"")

                    st.info(f"⏳ Waiting for other players ({len(responses)}/{len(session.players)} responded)")

                else:
                    st.subheader("Your Response")

                    response_type = st.radio(
                        "Do you accept this proposal?",
                        options=['accept', 'reject'],
                        format_func=lambda x: "✅ Accept" if x == 'accept' else "❌ Reject"
                    )

                    explanation = st.text_area(
                        "Comments (optional):",
                        placeholder="Explain your decision..."
                    )

                    if st.button("📤 Submit Response", type="primary"):
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
