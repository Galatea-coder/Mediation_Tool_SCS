# Multiplayer Quick Start Guide

**Get up and running with SCS Mediator SDK multiplayer in 10 minutes**

---

## What You'll Do

In this quick start, you'll:
1. Start the app
2. Create a negotiation session
3. Join as players
4. Negotiate an agreement
5. Run a simulation
6. Review results

**Time Required**: 10-15 minutes
**Participants**: 1 facilitator + 2-4 players (can test alone with multiple browser windows)

---

## Step 1: Start the App (1 minute)

```bash
cd /home/dk/scs_mediator_sdk_v2
streamlit run src/scs_mediator_sdk/ui/multiplayer_app.py --server.port 8506
```

The app opens in your browser at `http://localhost:8506`

**If you see an error**, ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

---

## Step 2: Create a Session (2 minutes)

**As Facilitator**:

1. Select **"🎓 Create as Facilitator"**
2. Enter your name: `Professor Smith`
3. Select scenario: **"Resupply Ship Incident"** (good starting scenario)
4. Click **"🚀 Create Session"**

**You'll see**:
```
Session Created: REEF-2024
Status: setup
```

**Write down the session code** (e.g., "REEF-2024") - players need this to join!

---

## Step 3: Join as Players (3 minutes)

**For testing alone**: Open 2-3 incognito/private browser windows at `http://localhost:8506`

**Each Player**:

1. Select **"👥 Join as Player"**
2. Enter session code: `REEF-2024` (use the code from Step 2)
3. Enter player name: `Ambassador Chen`, `Minister Wang`, etc.
4. Select role:
   - **Player 1**: PH_GOV (Philippines)
   - **Player 2**: PRC_MARITIME (China)
   - **Player 3** (optional): VN_CG (Vietnam)
5. Click **"Join Session"**
6. Click **"Mark as Ready"** button (in Tab 1)

**Facilitator**: Wait until all players show green checkmarks (✅ Ready)

---

## Step 4: Start Negotiation & Submit Proposal (3 minutes)

**Facilitator**:

1. Click **"🚀 Start Negotiation Round"** (button activates when all players ready)
2. In Tab 1 (🎯 Negotiation), fill out the proposal form:

**Suggested Moderate Proposal**:
```
Standoff Distance: 300 meters
Number of Escorts: 2
Escort Rules of Engagement: Defensive only
Inspection Protocol: Observer vessels only
Communication Channel: Encrypted VHF radio
Regular Updates Frequency: 6 hours
```

3. Click **"📤 Submit Proposal"**

**All Players Now See the Proposal** in their Tab 2 (📋 Current Proposal)

---

## Step 5: Players Respond (3 minutes)

**Each Player**:

1. Navigate to **Tab 2** (📋 Current Proposal) - review the terms
2. Navigate to **Tab 3** (💬 Submit Response)
3. Select response type and enter explanation:

**Player 1 (Philippines) - Accept**:
```
Response Type: Accept
Explanation: "The 300m standoff distance meets our security needs while allowing resupply operations. The defensive-only ROE reduces escalation risk."
```

**Player 2 (China) - Accept**:
```
Response Type: Accept
Explanation: "Observer vessel inspection respects sovereignty while providing transparency. This is a fair compromise."
```

**Player 3 (Vietnam) - Accept** (if present):
```
Response Type: Accept
Explanation: "The encrypted communication channel ensures security. Update frequency is reasonable."
```

4. Click **"Submit Response"**

**Facilitator**: Watch response count update (2/2 or 3/3 responded)

---

## Step 6: Run Simulation (2 minutes)

**Facilitator**:

1. Once all players accept, proposal status becomes **"✅ accepted"**
2. Scroll down in Tab 1 to **"Run Simulation"** section
3. Click **"🎮 Run Simulation with Accepted Agreement"**
4. Wait 5-10 seconds (progress spinner appears)

**Simulation Results Appear!**

---

## Step 7: Review Results (3 minutes)

**Look at the 4 Key Metrics**:

```
Incident Count: 12
  → Acceptable (under 20)

Escalation Frequency: 8%
  → Acceptable (under 15%)

Average Severity: 3.5
  → Acceptable (3.0-5.0 range)

Trend Analysis: Stable
  → Good (not increasing)
```

**Quick Assessment**: ✅ **Acceptable Outcome**

**What This Means**:
- Your agreement prevents most escalation
- Incidents occur but stay low-severity
- The situation is stable, not deteriorating
- Parameters were well-calibrated

**If you got a "Concerning" outcome**:
- Try tighter parameters (lower standoff distance, more escorts)
- Or try looser parameters (higher standoff distance, fewer escorts)
- Run multiple simulations to test different approaches

---

## What You Just Learned

**Phase 1 - Core Multiplayer**:
- ✅ Creating sessions with unique codes
- ✅ Joining as different roles
- ✅ Proposing agreement terms
- ✅ Submitting responses (accept/reject/conditional)
- ✅ Running agent-based simulations
- ✅ Interpreting results

---

## Try This Next

### Experiment 1: Tighter Parameters

**Facilitator**: Start a new round (or new session) with:
```
Standoff Distance: 150 meters (tighter)
Number of Escorts: 4 (more restrictive)
Escort Rules of Engagement: Weapons free
```

**Expected**: Some players may reject. If accepted, simulation may show higher escalation (stricter = more confrontation).

---

### Experiment 2: Looser Parameters

**Facilitator**: Try lenient approach:
```
Standoff Distance: 500 meters (more space)
Number of Escorts: 1 (less threatening)
Escort Rules of Engagement: Observe only
```

**Expected**: Players more likely to accept. Simulation may show lower escalation but possibly more incidents (less control).

---

### Experiment 3: Strategic Actions (Phase 3)

**Players**: Before responding to proposals, try executing strategic actions:

1. Navigate to **Tab 5** (⚡ Strategic Actions)
2. Click **"Execute: Initiate Track II Dialogue"** (no prerequisites, low cost)
   - **Effect**: +10 Diplomatic Capital, +5 Domestic Support
3. If you now have Capital ≥30, try **"Execute: Host Regional Summit"**
   - **Effect**: +10 International Legitimacy, +5 Credibility

**Then respond to proposal** - your improved strategic position affects escalation risk!

---

### Experiment 4: Multi-Round Negotiation

**Facilitator**: Try a realistic negotiation arc:

**Round 1**: Submit tight proposal
**Expected**: Mixed responses (some reject)

**Round 2**: Adjust based on player feedback, submit moderate proposal
**Expected**: More accepts

**Round 3**: Fine-tune, submit final proposal
**Expected**: Unanimous acceptance

**Debrief**: Discuss how iteration led to better outcomes

---

## Explore the Full Features

Now that you've completed the quick start, explore advanced features:

### Phase 2: Strategic Context System

**Facilitator**: Navigate to **Tab 3** (📊 Strategic Context Dashboard)
- View all players' strategic positions
- See 4-dimensional soft power metrics:
  - Diplomatic Capital
  - International Legitimacy
  - Domestic Support
  - Credibility
- Check escalation risk modifiers

**Players**: Navigate to **Tab 4** (📊 Your Strategic Position)
- Monitor your own metrics
- See how strategic actions affect your position

---

### Phase 3: Strategic Actions (Already Previewed Above)

**Players** can execute 6 different diplomatic moves:
1. **Host Regional Summit** - Build legitimacy through multilateral engagement
2. **Propose Joint Development** - Cooperative resource sharing
3. **Initiate Track II Dialogue** - Informal relationship building
4. **Make Public Commitment** - Lock in position with audience costs
5. **Increase Transparency** - Build trust through openness
6. **Offer Economic Incentives** - Issue linkage for breakthroughs

Each action has costs, prerequisites, and strategic effects!

---

### Phase 4: Enhanced Player Experience

**Players** have a 6-tab interface:
- **Tab 1**: Role & Objectives (your mission)
- **Tab 2**: Current Proposal (what's on the table)
- **Tab 3**: Submit Response (your answer)
- **Tab 4**: Your Strategic Position (your metrics)
- **Tab 5**: Strategic Actions (diplomatic moves)
- **Tab 6**: Strategy Notes (take notes during negotiation)

**Try Tab 6 - Strategy Notes**:
```
My Red Lines:
- Standoff distance must be ≥300m
- Maximum 2 escorts

My BATNA:
- Bilateral negotiation
- International arbitration

Concessions I Can Make:
- Update frequency (6h → 12h)
- Inspection protocol (observer vs remote)
```

---

## Common Quick Start Issues

### Issue: Session code not working
**Solution**: Check spelling (case-sensitive), ensure facilitator created session first

### Issue: "Role already taken"
**Solution**: Choose a different role or create new session

### Issue: Can't start negotiation
**Solution**: All players must click "Mark as Ready" button

### Issue: Can't submit response
**Solution**: Check if you already responded (can only respond once per proposal)

### Issue: Simulation button disabled
**Solution**: Proposal must be "accepted" (all players accepted, not mixed/rejected)

---

## Next Steps

### For Learning More:

1. **MULTIPLAYER_USER_GUIDE.md** - Comprehensive usage instructions
   - Detailed facilitator workflow
   - Player strategies and tactics
   - Strategic actions guide
   - Simulation interpretation

2. **MULTIPLAYER_TESTING_GUIDE.md** - Testing procedures
   - All 22 test cases
   - Multi-user scenarios
   - Expected behaviors
   - Troubleshooting

3. **MULTIPLAYER_FEATURE_IMPLEMENTATION_PLAN.md** - Technical details
   - Architecture overview
   - Phase implementation details
   - Academic foundations

### For Educators:

**Classroom Use** (60-90 min session):
1. **Introduction** (10 min): Explain South China Sea context
2. **Setup** (10 min): Create session, assign roles
3. **Negotiation** (30 min): 2-3 rounds of proposals and responses
4. **Simulation** (10 min): Run simulation, review results
5. **Debrief** (30 min): Discuss strategies, connect to theory

**Assessment Ideas**:
- Pre-negotiation strategy memo
- Post-negotiation reflection paper
- Comparative analysis of different approaches
- Connection to academic theories

---

## Academic Grounding

All features are based on academic research:

**Negotiation**:
- Fisher & Ury (1981) - *Getting to Yes*
- Raiffa (1982) - *The Art and Science of Negotiation*

**Strategic Context**:
- Nye (2004) - Soft Power
- Putnam (1988) - Two-Level Games
- Fearon (1994) - Credibility & Audience Costs
- Hurd (2007) - International Legitimacy
- Schelling (1960) - Strategic Positioning

**Strategic Actions**:
- Keohane (1984) - Multilateral Institutions
- Fravel (2008) - Joint Development
- Diamond & McDonald (1996) - Multi-Track Diplomacy
- Osgood (1962) - GRIT & Confidence-Building
- Tollison & Willett (1979) - Issue Linkage

**Agent-Based Modeling**:
- Epstein & Axtell (1996) - Growing Artificial Societies
- Axelrod (1984) - Evolution of Cooperation
- Bremer (1992) - Dangerous Dyads

---

## Support and Feedback

**Need Help?**
- Check troubleshooting sections in this guide
- See MULTIPLAYER_USER_GUIDE.md for detailed instructions
- See MULTIPLAYER_TESTING_GUIDE.md for common issues

**Found a Bug?**
- Check if it's a known issue in testing guide
- Document steps to reproduce
- Note your browser and system info

**Want to Customize?**
- See MULTIPLAYER_FEATURE_IMPLEMENTATION_PLAN.md for architecture
- Scenarios are defined in `src/scs_mediator_sdk/ui/multiplayer_app.py`
- Strategic actions in `src/scs_mediator_sdk/strategic_levers/actions.py`

---

## Summary: What's Possible

After this 10-minute quick start, you can now:

**Run Negotiations** (Phase 1):
- Multi-user sessions with unique codes
- Dynamic scenario-based proposals
- Accept/reject/conditional responses
- Agent-based simulation testing
- Outcome interpretation

**Track Strategic Context** (Phase 2):
- 4-dimensional soft power metrics
- Per-player strategic positions
- Escalation risk modifiers
- Academic grounding in IR theory

**Execute Strategic Actions** (Phase 3):
- 6 diplomatic moves with costs & effects
- Prerequisites based on metrics
- Cascading strategic consequences
- Literature-backed action library

**Enhanced Player Experience** (Phase 4):
- 6-tab organized interface
- Strategy notes for planning
- Status-aware content
- Streamlined navigation

**Educational Applications**:
- IR courses (negotiation, conflict resolution)
- Wargaming exercises
- Professional training
- Policy research

---

**Congratulations!** You've completed the quick start. You're now ready to run sophisticated multiplayer maritime negotiation simulations.

**Recommended Next Action**:
1. Run 2-3 more simulations with different parameters
2. Experiment with strategic actions (Tab 5)
3. Review the comprehensive MULTIPLAYER_USER_GUIDE.md
4. Try multi-round negotiations with player feedback

---

**Last Updated**: 2025-01-09
**Version**: 1.0 (Phases 1-4 Complete)
**Est. Time to Proficiency**: 30-60 minutes of hands-on practice
