# Multiplayer Version - Quick Start Guide

**Status**: MVP Complete ✅
**Version**: 1.0.0 (MVP)
**Last Updated**: January 2025

---

## 🎯 What is This?

The **Multiplayer Version** allows multiple human users to negotiate together:
- **1 Facilitator**: Creates session, proposes terms, runs simulation
- **2-4 Players**: Join with session code, review proposals, accept/reject

This is different from the single-player version where one person designs everything alone.

---

## 🚀 Quick Start (Local Testing)

### 1. Run the App

```bash
streamlit run src/scs_mediator_sdk/ui/multiplayer_app.py
```

### 2. Open Multiple Browser Tabs

- Tab 1: `http://localhost:8501` (Facilitator)
- Tab 2: `http://localhost:8501` (Player 1 - Philippines)
- Tab 3: `http://localhost:8501` (Player 2 - China)

**Important**: Use **different browser profiles** or **incognito windows** to simulate different users.

### 3. Session Workflow

#### Tab 1 (Facilitator):
1. Click "Join as Facilitator"
2. Select scenario (e.g., "Second Thomas Shoal")
3. Enter name: "Facilitator"
4. Click "Create Session"
5. **Copy the session code** (e.g., "REEF-2024")

#### Tab 2 (Player 1):
1. Click "Join as Player"
2. Enter session code: **REEF-2024**
3. Enter name: "Alice"
4. Select role: **🇵🇭 Philippines**
5. Click "Join Session"

#### Tab 3 (Player 2):
1. Click "Join as Player"
2. Enter session code: **REEF-2024**
3. Enter name: "Bob"
4. Select role: **🇨🇳 China**
5. Click "Join Session"

#### Back to Tab 1 (Facilitator):
1. See both players connected
2. Click "Start Negotiation"
3. Set proposal terms:
   - Standoff distance: 3nm
   - Max escorts: 1
   - Pre-notification: 24 hours
4. Click "Send Proposal to Players"

#### Tab 2 & 3 (Players):
1. Review the proposal
2. Choose "Accept" or "Reject"
3. Add optional comment
4. Click "Submit Response"

#### Back to Tab 1 (Facilitator):
1. See all responses
2. If all accepted: Click "Run Simulation"
3. View results together

---

## 🌐 Deploy to Streamlit Cloud

### Option 1: Create New App

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Repository: `Galatea-coder/Mediation_Tool_SCS`
4. Branch: `master`
5. **Main file path**: `streamlit_app_multiplayer.py` ⚠️
6. App URL: `scs-multiplayer` (or your choice)
7. Click "Deploy"

### Option 2: Update Existing App

If you want to test the multiplayer version temporarily:

1. Go to your app dashboard
2. Find your app
3. Click "⋮" → "Settings"
4. Under "Main file path", change to: `streamlit_app_multiplayer.py`
5. Click "Save"
6. App will redeploy automatically

---

## 📋 Testing Checklist

Before deploying, test locally:

- [ ] Facilitator can create session and get code
- [ ] Player 1 can join with code
- [ ] Player 2 can join with code (different role)
- [ ] Both players appear in facilitator dashboard
- [ ] Facilitator can start negotiation
- [ ] Facilitator can send proposal
- [ ] Players can see proposal
- [ ] Players can accept/reject
- [ ] All responses appear in facilitator view
- [ ] Simulation runs when all accept
- [ ] Results visible to all users

---

## 🎮 Usage Examples

### Classroom Training (60-90 minutes)

**Setup** (10 min):
- Instructor = Facilitator
- Students pair up = Players
- Each pair picks Philippines or China

**Round 1** (20 min):
- Instructor proposes initial terms
- Students discuss in pairs
- Submit accept/reject with reasoning

**Discussion** (10 min):
- Why did you accept/reject?
- What would make this better?

**Round 2** (15 min):
- Instructor proposes revised terms
- Students respond

**Simulation** (15 min):
- Run simulation on agreed terms
- Discuss results

**Debrief** (20 min):
- What worked?
- What didn't?
- Real-world implications

### Workshop/Conference (2-3 hours)

- Mix of government, academic, NGO participants
- Rotate roles between rounds
- Multiple scenarios
- In-depth policy discussion

---

## 🔧 Technical Details

### Architecture

**Session Management**:
- In-memory state (no database for MVP)
- Session codes generated randomly (e.g., "REEF-2024")
- State persists until server restart

**Limitations**:
- If server restarts, all sessions lost
- No real-time updates (manual refresh needed)
- Simple accept/reject only (no counteroffers yet)

**Files**:
```
src/scs_mediator_sdk/multiplayer/
├── __init__.py
└── session_manager.py          # Core session logic

src/scs_mediator_sdk/ui/
└── multiplayer_app.py           # Full UI (facilitator + player)

streamlit_app_multiplayer.py    # Deployment entry point
```

### Adding More Features

Want to add counteroffers, private chat, or other features? Check:
- `docs/MULTIPLAYER_VERSION_PLAN.md` - Full design plan
- `src/scs_mediator_sdk/multiplayer/session_manager.py` - Extend here

---

## ❓ FAQ

**Q: Can players see each other's responses before submitting?**
A: No, responses are private until all players submit.

**Q: What if a player disconnects?**
A: Currently they need to rejoin with the same session code. Their role will still be taken, so they'll need to wait for a new session or have facilitator restart.

**Q: Can I have more than 2 players?**
A: Yes! The system supports 2-4 players. Just add more scenarios with more roles in `multiplayer_app.py`.

**Q: How do I add counteroffers?**
A: This is planned for v2.0. For now, use the comment field to suggest changes, and facilitator manually proposes revised terms in a new round.

**Q: Does this work on Streamlit Cloud?**
A: Yes! Just deploy with `streamlit_app_multiplayer.py` as the entry point.

**Q: Will sessions persist if I close the browser?**
A: Sessions persist on the server (not in browser), so you can close/reopen browser tabs and rejoin with the same session code. However, if the **server restarts**, all sessions are lost (in-memory storage).

---

## 🐛 Known Issues & Workarounds

**Issue**: Players need to manually refresh to see updates
**Workaround**: Click the "🔄 Refresh" button or enable auto-refresh (facilitator sidebar)

**Issue**: Session lost if server restarts
**Workaround**: For production, upgrade to SQLite/PostgreSQL database (see MULTIPLAYER_VERSION_PLAN.md)

**Issue**: Only 2 scenarios available
**Workaround**: Add more in `SCENARIOS` dict in `multiplayer_app.py`

**Issue**: Can't modify proposal after sending
**Workaround**: Start a new round with revised terms

---

## 🚦 Roadmap

### v1.0 (MVP) ✅ - DONE
- [x] Session codes
- [x] Player join
- [x] Facilitator proposal
- [x] Accept/reject voting
- [x] Simulation integration

### v1.1 - Next Steps
- [ ] Counteroffers
- [ ] Private comments to facilitator
- [ ] Session history/logs
- [ ] Export results

### v2.0 - Advanced
- [ ] Real-time updates (WebSockets)
- [ ] Persistent database (SQLite)
- [ ] More scenarios (4 total)
- [ ] Observer mode
- [ ] Session analytics

---

## 📞 Support

For issues or questions:
1. Check `docs/MULTIPLAYER_VERSION_PLAN.md` for design details
2. Review code in `src/scs_mediator_sdk/multiplayer/`
3. Test locally before deploying

---

**Happy Negotiating! 🌊**

---

**Version**: 1.0.0 MVP
**Last Updated**: January 2025
**Contributors**: Claude Code + Your Team
