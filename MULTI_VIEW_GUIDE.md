# Multi-View Simulation Training Guide

## Overview

You now have **two different user interfaces** for different purposes:

### 1. Original Instructor Console (Port 8501)
**Purpose**: Solo analysis and testing
**URL**: http://localhost:8501
**Use for**: Analyzing scenarios, testing agreements, running simulations independently

### 2. Multi-View Training Interface (Port 8502)
**Purpose**: Live training workshops with multiple participants
**URL**: http://localhost:8502
**Use for**: Role-playing negotiations with separate views for instructor and parties

---

## Quick Start: Multi-View Training Interface

### Architecture

The multi-view interface has 3 types of views:

1. **Role Selection Page** (Landing)
   - Choose whether you're an Instructor or Party
   - Each participant selects their role

2. **Instructor Console** (Full visibility)
   - Select scenarios
   - Start sessions
   - See ALL utilities and probabilities
   - Run simulations
   - Monitor all parties in real-time

3. **Party Views** (Limited information)
   - See only YOUR position and interests
   - View current proposals
   - See only YOUR utility (not other parties')
   - Make counter-offers
   - Realistic negotiation experience

---

## Usage Scenarios

### Scenario A: Solo Analysis (Use Port 8501)

**What**: You alone, exploring scenarios and testing agreements

**Steps**:
1. Open http://localhost:8501
2. Select scenario from sidebar
3. Build agreement terms with sliders
4. Click "Evaluate Offer" to see ALL parties' utilities
5. Run simulation to test durability
6. Adjust and repeat

**Best for**:
- Learning the system
- Preparing for training
- Testing scenario parameters
- Calibrating the model

---

### Scenario B: Live Training Workshop (Use Port 8502)

**What**: Multiple participants negotiating in real-time

**Setup** (15 minutes before workshop):

1. **Start the API server** (if not already running):
   ```bash
   uvicorn src.scs_mediator_sdk.api.server:app --reload
   ```

2. **Start the multi-view UI**:
   ```bash
   streamlit run src/scs_mediator_sdk/ui/multi_view_app.py --server.port=8502
   ```

3. **Share the URL** with participants:
   - Give everyone: http://localhost:8502 (or your server IP)
   - Each person opens it in their browser

**Participant Assignment**:

| Participant | Role | What They Do |
|-------------|------|--------------|
| Facilitator | Instructor | Controls scenario, monitors all parties |
| Person 1 | PH_GOV | Negotiates for Philippines |
| Person 2 | PRC_MARITIME | Negotiates for China |
| (Optional) Person 3 | VN_CG | Negotiates for Vietnam |
| (Optional) Person 4 | MY_CG | Negotiates for Malaysia |

---

## Step-by-Step: Running a Live Training Workshop

### Phase 1: Setup (Instructor Only)

1. **Instructor opens** http://localhost:8502
2. Clicks **"Enter as Instructor"**
3. Sees full control console
4. In sidebar:
   - Select scenario (e.g., "scenario_A_second_thomas.json")
   - Review scenario details (map, context)
5. In sidebar expander **"Start Session"**:
   - Select parties: PH_GOV, PRC_MARITIME
   - Enter mediator name: "ASEAN_Facilitator"
   - Select issues: resupply_SOP, hotline_cues, media_protocol
   - Click **"Start Session"**
6. Session is now active!

### Phase 2: Party Login (All Negotiators)

1. **Each negotiator** opens http://localhost:8502 in their own browser
2. Clicks **"Enter as Party"**
3. Selects their assigned role:
   - Person 1: 🇵🇭 Philippines Government
   - Person 2: 🇨🇳 PRC Maritime Forces
4. Clicks **"Enter as Party"**
5. Now sees their party-specific view

### Phase 3: Understand Positions (Each Party)

Each party should:

1. Click **"Your Position" tab**
2. Review:
   - Your primary interests
   - Your BATNA (fallback option)
   - Your key concerns
   - Your constraints
3. Take notes in **"Your Assessment" tab**
4. Strategize: What are your priorities? What can you concede?

### Phase 4: Initial Offers (Round 1)

**Philippines (PH_GOV) goes first**:

1. Click **"Make Offer" tab**
2. Adjust sliders to propose terms:
   - Resupply SOP: Standoff distance, escorts, notification time
   - Hotline & CUES: Communication protocols
   - Media Protocol: Embargo period
3. Click **"Preview My Utility"** to see if offer is above your BATNA
4. Click **"Submit Offer to Mediator"**

**Instructor monitors**:
- Click **"Live Session Monitor" tab**
- See "Current Offers on Table"
- Can see the submitted offer

**PRC_MARITIME responds**:
1. Click **"Current Proposal" tab**
2. See Philippines' offer
3. See YOUR utility from this offer
4. Decision:
   - If utility > 0.6: Consider accepting
   - If utility < 0.4: Make counter-offer
5. Go to **"Make Offer" tab** and propose counter-terms
6. Click **"Submit Offer to Mediator"**

### Phase 5: Negotiation Rounds

Repeat:
- Parties take turns making offers
- Each party sees only THEIR utility
- Instructor sees EVERYTHING (all utilities, acceptance probabilities)
- Parties adjust terms based on their utility scores
- Goal: Find agreement where both parties > 0.5 utility

**Instructor can**:
- Evaluate any offer to see ALL utilities
- Provide feedback: "Philippines is at 0.65, China is at 0.42"
- Suggest: "China needs more concessions on issue X"
- Guide parties toward Zone of Possible Agreement (ZOPA)

### Phase 6: Test Agreement Durability (Instructor)

Once parties reach tentative agreement:

1. Instructor clicks **"Simulate" tab**
2. Sets:
   - Steps: 300
   - Environment: Uses scenario weather/media settings
3. Clicks **"Run Simulation"**
4. Reviews results:
   - Total incidents: <25 is good
   - Trend: Declining is good
   - Severity: <0.4 average is good

**If simulation shows problems**:
- High incidents? Strengthen enforcement provisions
- Escalating trend? Agreement terms too weak
- High severity? Add crisis management protocols

### Phase 7: Refine and Finalize

Based on simulation results:
1. Parties negotiate additional clauses
2. Adjust parameters (e.g., reduce standoff distance, add hotline requirement)
3. Re-simulate until results are acceptable
4. Finalize agreement

---

## Example Workshop Timeline (2 hours)

| Time | Activity | Who |
|------|----------|-----|
| 0:00-0:10 | Introduction & role assignment | Facilitator |
| 0:10-0:15 | Login and review positions | All parties |
| 0:15-0:25 | PH_GOV makes opening offer | Philippines |
| 0:25-0:35 | PRC_MARITIME makes counter-offer | China |
| 0:35-0:55 | Negotiation rounds (3-4 rounds) | Both parties |
| 0:55-1:05 | Test agreement via simulation | Instructor |
| 1:05-1:20 | Refine terms based on results | Both parties |
| 1:20-1:30 | Final simulation | Instructor |
| 1:30-1:45 | Debrief: What worked? What didn't? | All |
| 1:45-2:00 | Lessons learned & next steps | Facilitator |

---

## Key Differences: Party View vs Instructor View

### Party View (Limited Information)

**You CAN see**:
- Your own position and interests
- Your BATNA
- The current proposal on the table
- YOUR utility from any proposal
- YOUR acceptance probability

**You CANNOT see**:
- Other parties' utilities
- Other parties' acceptance probabilities
- Overall agreement probability
- Other parties' BATNA
- Full simulation results

**Why**: Realistic negotiation! In real mediation, you don't know the other side's exact numbers.

### Instructor View (Full Information)

**You CAN see**:
- ALL parties' utilities
- ALL acceptance probabilities
- Overall agreement probability
- Complete simulation results
- All offers from all parties
- Full scenario details

**Why**: You're the facilitator. You need full visibility to guide the process.

---

## Tips for Successful Training

### For Instructors:

1. **Prep beforehand**: Review scenario, understand party positions
2. **Set expectations**: Explain that parties have limited info (like real life)
3. **Guide gently**: Don't reveal exact numbers, give hints
4. **Use simulation**: Show consequences of weak agreements
5. **Debrief thoroughly**: Compare party estimates vs actual utilities

### For Parties:

1. **Understand your BATNA**: Never accept below 0.4 utility
2. **Start ambitious**: Your first offer can be aggressive
3. **Track patterns**: If instructor says "other side is unhappy", adjust
4. **Use preview**: Always check "Preview My Utility" before submitting
5. **Think creatively**: Package issues (give on X, get on Y)

### Common Pitfalls:

❌ **Don't**: Reveal all utilities immediately (instructor)
✅ **Do**: Let parties discover through negotiation

❌ **Don't**: Make wild offers that waste time
✅ **Do**: Use "Preview My Utility" to check reasonableness

❌ **Don't**: Focus only on simulation numbers
✅ **Do**: Discuss interests, concerns, and real-world implications

---

## Troubleshooting

### "Cannot connect to API"

**Problem**: Backend server not running
**Fix**:
```bash
uvicorn src.scs_mediator_sdk.api.server:app --reload
```

### "No active session"

**Problem**: Instructor hasn't started session yet
**Fix**: Instructor must click "Start Session" in sidebar

### "Offer submitted but nothing happens"

**Expected**: Offers are stored in session state, instructor can review in "Live Session Monitor"
**Note**: Real-time synchronization between browsers requires additional setup (WebSockets)

### "I logged in as wrong role"

**Fix**: Click "Logout" button in sidebar, then re-select role

---

## Current Limitations & Future Enhancements

### Current Version:

✅ Separate views for instructor and parties
✅ Party-specific utility calculations
✅ Offer submission to session state
✅ Role-based access control

### Not Yet Implemented:

⚠️ Real-time synchronization between browsers
   - Current: Each browser is independent session
   - Future: Use WebSockets for live updates across all participants

⚠️ Offer queue management
   - Current: Latest offer overwrites previous
   - Future: History of all offers, turn-based system

⚠️ Chat/messaging between parties
   - Future: Built-in communication channel

⚠️ Automated notifications
   - Future: Alert when new offer arrives

**For production workshops**: Use shared screen or verbal communication to coordinate between parties until real-time sync is implemented.

---

## Summary

**Two interfaces, two purposes:**

| Purpose | URL | Who Uses It |
|---------|-----|-------------|
| **Solo analysis** | http://localhost:8501 | You alone |
| **Live training** | http://localhost:8502 | Multiple participants |

**Key insight**: The multi-view interface simulates realistic mediation where parties have **incomplete information** - just like real negotiation!

---

## Next Steps

1. **Try solo first**:
   - Open http://localhost:8501
   - Play with Scenario A (Second Thomas Shoal)
   - Learn the mechanics

2. **Test multi-view yourself**:
   - Open http://localhost:8502 in two browser windows
   - Window 1: Login as Instructor
   - Window 2: Login as PH_GOV
   - Practice the workflow

3. **Run a pilot workshop**:
   - Invite 2-3 colleagues
   - Assign roles
   - Walk through Phase 1-7 above
   - Gather feedback

4. **Scale up**:
   - Try all 4 scenarios (A, B, C, D)
   - Add more parties (3-4 way negotiations)
   - Experiment with different mediation styles

**Ready to start!** 🚀
