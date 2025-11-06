# Instructor User Guide
## SCS Mediation Simulation - Enhanced Multi-View Interface

**Version**: 10.0
**Last Updated**: November 2025
**For**: Facilitators, trainers, and educators running mediation simulations

---

## Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [UI Improvements](#ui-improvements)
4. [Step-by-Step Workflow](#step-by-step-workflow)
5. [Understanding Results](#understanding-results)
6. [Running Live Workshops](#running-live-workshops)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## Overview

### What is This Tool?

The SCS Mediation Simulation is an advanced training platform that combines:
- **Game Theory**: MAUT, Prospect Theory, BATNA analysis
- **Agent-Based Modeling**: Realistic incident simulation
- **Multi-Party Negotiation**: Support for 2-4 parties
- **Real Scenarios**: 4 South China Sea maritime disputes

### Your Role as Instructor

As an instructor, you have:
- **Full Visibility**: See all parties' utilities and acceptance probabilities
- **Control**: Start sessions, evaluate offers, run simulations
- **Guidance**: Use data to coach participants toward better agreements
- **Analysis**: Deep dive into why agreements work or fail

### What's New in Enhanced Version

✅ **Clear Workflow Guide**: 5-step process with visual progress tracking
✅ **Better Visual Hierarchy**: Important info stands out
✅ **Friendly Labels**: "Standoff Distance (nautical miles)" instead of "standoff_nm"
✅ **Rich Visualizations**: Metrics, charts, color-coded results
✅ **Contextual Help**: Tooltips and explanations throughout
✅ **Responsive Layout**: Optimized spacing and columns
✅ **Professional Design**: Modern UI with custom CSS

---

## Getting Started

### Prerequisites

1. **Backend API Running**:
   ```bash
   uvicorn src.scs_mediator_sdk.api.server:app --reload
   ```
   Should see: "Application startup complete"

2. **Enhanced UI Running**:
   ```bash
   streamlit run src/scs_mediator_sdk/ui/enhanced_multi_view.py
   ```
   Should see: "You can now view your Streamlit app in your browser"

3. **Open Browser**:
   Navigate to the URL shown (usually http://localhost:8501)

### First Launch

1. You'll see the **Role Selection** page
2. Two large boxes: **Instructor** (left) and **Negotiating Party** (right)
3. Click **"🎓 Enter as Instructor"** (blue button)
4. You'll enter the **Instructor Console**

---

## UI Improvements

### Before vs After

#### OLD UI Problems:
- ❌ Raw JSON dumps cluttering the screen
- ❌ Technical jargon ("standoff_nm", "pre_notification_hours")
- ❌ No clear workflow - users didn't know what to do next
- ❌ Results displayed as ugly text blocks
- ❌ Everything crammed in sidebar
- ❌ No visual feedback on success/failure

#### NEW UI Solutions:
- ✅ Expandable sections with clear step numbers
- ✅ Human-readable labels ("Standoff Distance (nautical miles)")
- ✅ Visual workflow guide at top showing your progress
- ✅ Color-coded metrics with progress bars
- ✅ Organized layout with proper spacing
- ✅ Success/warning/error messages with context

### Key Design Principles

1. **Progressive Disclosure**: Steps expand only when relevant
2. **Visual Feedback**: Green = good, yellow = caution, red = problem
3. **Guided Experience**: Workflow guide shows where you are
4. **Contextual Help**: Tooltips explain technical terms
5. **Professional Aesthetics**: Clean, modern, trustworthy design

---

## Step-by-Step Workflow

The enhanced UI guides you through **5 clear steps**:

### Step 1: Setup Scenario & Session

**What You'll See:**
- Scenario selection dropdown with descriptive names
- Key details: Location, focus, weather, media visibility
- Map preview (if available)
- Party selection with flags
- Issue space configuration

**What To Do:**

1. **Select Scenario**:
   - 🏝️ Scenario A: Second Thomas Shoal (Resupply missions)
   - 🎣 Scenario B: Scarborough Shoal (Fishing rights)
   - ⛽ Scenario C: Kasawari Gas Field (Energy resources)
   - 🌊 Scenario D: Natuna Islands (EEZ boundaries)

2. **Choose Parties**:
   - Default: 🇵🇭 Philippines + 🇨🇳 PRC Maritime
   - Can add: 🇻🇳 Vietnam + 🇲🇾 Malaysia

3. **Select Issues**:
   - Resupply SOP (resupply operations)
   - Hotline & CUES (communications)
   - Media Protocol (public information)
   - Fishing Rights (if applicable)

4. **Click "▶️ Start Session"**

**Visual Feedback:**
- ✅ Green success message: "Session started successfully!"
- Workflow guide updates: Step 1 gets a checkmark, Step 2 highlighted
- Session ID displayed in sidebar

### Step 2: Build Agreement Offer

**What You'll See:**
- Three columns for different issue areas
- Sliders and dropdowns for each parameter
- Live preview of agreement JSON (hidden in expander)

**What To Do:**

1. **Resupply Operations** (left column):
   - **Standoff Distance**: 0-10 nautical miles
     - *Lower = more verification, higher = more security*
     - Typical: 3-5 nm
   - **Max Escort Vessels**: 0-5
     - *Fewer = less threatening, more = more security*
     - Typical: 1-2
   - **Pre-Notification**: 0-48 hours
     - *More = predictability, less = operational flexibility*
     - Typical: 12-24 hours

2. **Communication Protocols** (middle column):
   - **Hotline Availability**: Ad-Hoc or 24/7
     - *24/7 = better crisis management*
   - **CUES Compliance**: Select requirements
     - *More = better safety, but more constraints*

3. **Media Management** (right column):
   - **News Embargo**: 0-48 hours
     - *Longer = more face-saving time*
     - Typical: 6-12 hours

4. **Click "➡️ Proceed to Evaluation"**

**Tips:**
- Start with moderate terms (middle of sliders)
- Think about what each party values
- Can always come back and adjust

### Step 3: Evaluate Offer

**What You'll See:**
- Big blue button: "🔍 Calculate Utilities & Acceptance Probabilities"
- After clicking: Beautiful metric cards for each party
- Color-coded utility scores with progress bars
- Overall agreement probability

**What To Do:**

1. **Click "🔍 Calculate..."** button
2. **Read Party Utilities**:
   - Each party gets a card with their flag
   - **Green (>70%)**: Excellent for them
   - **Blue (50-70%)**: Good, acceptable
   - **Orange (40-50%)**: Marginal, at BATNA threshold
   - **Red (<40%)**: Below BATNA, will likely reject

3. **Read Acceptance Probabilities**:
   - Percentage chance each party accepts
   - ✅ >70% = Likely to accept
   - ⚠️ 50-70% = Uncertain
   - ❌ <50% = Likely to reject

4. **Check Overall Probability**:
   - Product of all acceptance probabilities
   - **>60%**: Good chance! Proceed to simulation
   - **30-60%**: Uncertain, consider adjustments
   - **<30%**: Low chance, need major changes

**Interpretation Guide:**

| Situation | What It Means | What To Do |
|-----------|---------------|------------|
| Both parties >60% utility | Win-win agreement | Proceed to simulation |
| One party <40% | Below their BATNA | Adjust to give them more |
| Both 40-60% | Acceptable but not great | Fine, but could improve |
| Acceptance >70% | Very likely to be accepted | Strong agreement |
| Acceptance <30% | Very unlikely | Rethink approach |

**Example:**
```
🇵🇭 Philippines: 65% utility ✅ Good
🇨🇳 PRC: 42% utility ⚠️ Marginal

Philippines Acceptance: 78% ✅
PRC Acceptance: 55% ⚠️

Overall Agreement Probability: 43%
```
**Interpretation**: Philippines happy, China barely at BATNA. Need to sweeten deal for China without hurting Philippines too much.

5. **If Results Good**: Click "➡️ Proceed to Simulation"
6. **If Results Poor**: Go back to Step 2, adjust terms

### Step 4: Simulate Agreement Durability

**What You'll See:**
- Slider to set simulation duration
- Big button: "▶️ Run Simulation"
- Spinner while processing
- After completion: jumps to Step 5

**What To Do:**

1. **Set Duration**:
   - 50-200 steps: Quick test
   - 200-500 steps: Standard (recommended)
   - 500-1000 steps: Thorough analysis

2. **Click "▶️ Run Simulation"**

3. **Wait**: Takes 2-10 seconds depending on duration

**What's Happening:**
- Agent-based model runs in background
- Simulates vessels, patrols, interactions
- Generates incidents based on agreement strength
- Weather and media visibility affect outcomes

### Step 5: Analyze Results & Refine

**What You'll See:**
- 4 metric cards across the top
- 2 charts below: Time series + Severity histogram
- Event log table
- Recommendations section

**What To Do:**

1. **Review Summary Metrics**:

   | Metric | Good | Bad | What It Means |
   |--------|------|-----|---------------|
   | Total Incidents | <25 | >40 | Overall conflict level |
   | Avg Severity | <0.4 | >0.7 | Intensity of incidents |
   | Max Severity | <0.6 | >0.9 | Worst case scenario |
   | Trend | ✅ Declining | ❌ Escalating | Is it getting better or worse? |

2. **Analyze Charts**:
   - **Time Series** (left): Incidents over time
     - Flat line near zero = excellent
     - Declining = agreement working
     - Rising = agreement failing
   - **Severity Distribution** (right): How bad are incidents?
     - Clustered at low values = good
     - Spread out or high values = concerning

3. **Read Recommendations**:
   - ✅ Agreement working well = Success!
   - ⚠️ Consider strengthening = Suggestions provided
   - ❌ Agreement failing = Need major revision

4. **Decide Next Steps**:
   - **If Results Good**: Done! Agreement is viable
   - **If Results Poor**: Click "🔄 Back to Step 2 to Refine Offer"

**Example Interpretations:**

**Scenario 1: Excellent Agreement**
```
Total Incidents: 8 (✅)
Avg Severity: 0.22 (✅)
Trend: ✅ Declining

Recommendation: Agreement is working well!
```

**Scenario 2: Needs Work**
```
Total Incidents: 47 (❌)
Avg Severity: 0.68 (❌)
Trend: ❌ Escalating

Recommendation: Consider strengthening agreement:
- Reduce standoff distance for better verification
- Add 24/7 hotline if not already included
```

---

## Understanding Results

### Utility Scores (0-1 scale)

**What It Is:**
A measure of how satisfied a party is with the agreement, considering:
- How well it meets their interests
- How it compares to their BATNA (fallback option)
- Prospect Theory: Losses hurt more than equivalent gains

**Interpretation:**

| Score | Rating | Meaning | Party Likely To... |
|-------|--------|---------|-------------------|
| 0.8-1.0 | Excellent | Much better than BATNA | Accept enthusiastically |
| 0.6-0.8 | Good | Solidly above BATNA | Accept |
| 0.4-0.6 | Acceptable | Marginally better than BATNA | Consider carefully |
| 0.2-0.4 | Poor | At or below BATNA | Likely reject |
| 0.0-0.2 | Terrible | Much worse than BATNA | Definitely reject |

**Key Insight**: Both parties need >0.4 for viable agreement. Aim for >0.6 for strong agreement.

### Acceptance Probabilities

**What It Is:**
Statistical likelihood that a party will accept the offer, based on their utility and risk attitude.

**Interpretation:**

| Probability | Meaning | What To Expect |
|-------------|---------|----------------|
| >80% | Very likely | Party will almost certainly accept |
| 60-80% | Likely | Good chance of acceptance |
| 40-60% | Uncertain | Could go either way |
| 20-40% | Unlikely | Probably will reject |
| <20% | Very unlikely | Almost certainly will reject |

**Overall Agreement Probability:**
Product of all individual probabilities. Example:
- Party A: 75% acceptance
- Party B: 60% acceptance
- Overall: 75% × 60% = 45% chance both accept

**Key Insight**: Need overall >50% for realistic chance. >60% is strong.

### Simulation Results

**Total Incidents:**
- Count of all interactions that escalated
- Types: water cannon, ramming, detention, near-miss
- **Good**: <25 incidents
- **Concerning**: 25-50 incidents
- **Bad**: >50 incidents

**Avg Severity (0-1 scale):**
- How serious incidents are on average
- 0 = minor (verbal warning)
- 0.5 = moderate (water cannon)
- 1.0 = severe (collision, detention)
- **Good**: <0.4
- **Concerning**: 0.4-0.7
- **Bad**: >0.7

**Trend:**
- Compare early vs late periods
- **Declining**: Late incidents < Early incidents (agreement stabilizing)
- **Stable**: Late ≈ Early (holding steady)
- **Escalating**: Late > Early (agreement breaking down)

---

## Running Live Workshops

### Setup (Before Participants Arrive)

**15 Minutes Before:**

1. **Start Servers**:
   ```bash
   # Terminal 1
   uvicorn src.scs_mediator_sdk.api.server:app --reload

   # Terminal 2
   streamlit run src/scs_mediator_sdk/ui/enhanced_multi_view.py
   ```

2. **Test Access**:
   - Open browser to the Streamlit URL
   - Verify role selection page loads
   - Login as Instructor, verify console loads
   - Logout, verify can login as Party

3. **Share URL**:
   - If localhost: Only works on your machine
   - If need remote access: Use ngrok or deploy to server
   - Give participants the URL

4. **Prepare Materials**:
   - Print or share scenario descriptions
   - Assign roles to participants
   - Explain objectives

### During Workshop

**Phase 1: Introduction (10 min)**

1. **Explain Context**: South China Sea disputes, mediation principles
2. **Assign Roles**:
   - You: Instructor/Mediator
   - Participant 1: 🇵🇭 Philippines Government
   - Participant 2: 🇨🇳 PRC Maritime Forces
   - (Optional) Participants 3-4: Vietnam, Malaysia
3. **Login**: Each participant opens URL, selects their role

**Phase 2: Position Review (10 min)**

1. **Participants Read**: "Your Position" tab
   - Their interests, BATNA, concerns, constraints
2. **You Explain**: The issues to be negotiated
3. **Q&A**: Clarify any confusions

**Phase 3: Initial Offers (15 min)**

1. **Philippines Makes Offer**: Uses "Make Offer" tab
2. **Submits Offer**: Clicks "Submit Offer to Mediator"
3. **You Evaluate** (Instructor Console, Step 2-3):
   - Input the same terms Philippines proposed
   - Click "Calculate Utilities"
   - **DON'T share exact numbers yet** - just say "interesting proposal"

**Phase 4: Counter-Offers (20-30 min)**

1. **China Reviews**: "Current Proposal" tab
2. **China Calculates**: Their own utility (they only see theirs)
3. **China Responds**: Makes counter-offer
4. **You Mediate**:
   - Evaluate each offer
   - Give hints: "Philippines is satisfied, but China needs more"
   - Don't reveal exact numbers - guide them
5. **Iterate**: 2-4 rounds until convergence

**Your Facilitation Techniques:**

| When To Use | What To Say | Don't Say |
|-------------|-------------|-----------|
| One party low utility | "Party X feels this doesn't meet their needs" | "Party X is at 38% utility" |
| Getting close | "You're making progress, keep going" | "Just 5% more and you're there" |
| Stuck | "Think about issue Y - maybe there's room there?" | "Philippines should give on standoff" |
| Success | "Both parties seem satisfied, let's test it" | (Reveal numbers now) |

**Phase 5: Agreement Test (10 min)**

1. **Run Simulation** (Instructor, Step 4-5)
2. **Share Results** with all participants
3. **Discuss**:
   - Were you surprised by incident count?
   - Does trend make sense given your agreement?
   - What would you change?

**Phase 6: Debrief (15-20 min)**

1. **Reveal All Numbers**:
   - Show final utilities for both parties
   - Explain why agreement worked (or didn't)
2. **Discuss Process**:
   - What was hardest part of negotiation?
   - Did limited information (parties can't see each other's utilities) affect strategy?
   - In real mediation, how would this play out?
3. **Key Lessons**:
   - Importance of understanding interests vs positions
   - Role of BATNA in negotiation
   - How agreements can look good but fail under stress
   - Value of simulation/testing

---

## Troubleshooting

### "API not responding"

**Symptoms**: Buttons don't work, errors like "Cannot connect"

**Fix**:
```bash
# Check if API running
curl http://localhost:8000/healthz

# Should see: {"status":"ok"}

# If not, start it:
uvicorn src.scs_mediator_sdk.api.server:app --reload
```

### "Simulation hangs"

**Symptoms**: "Running simulation..." spinner doesn't finish

**Causes**:
- API server crashed
- Very long duration selected (>1000 steps)

**Fix**:
- Check API terminal for errors
- Restart API if needed
- Use shorter duration (300 steps)

### "Utilities seem wrong"

**Symptoms**: Party X should like this offer but utility is low

**Likely Causes**:
- Party weights not configured correctly in scenario
- BATNA threshold set too high
- Prospect Theory loss aversion kicking in

**Fix**:
- Review scenario file (cases/scs/scenario_X.json)
- Check party definitions
- This is normal - parties have different preferences

### "Parties can't see each other's offers"

**Expected Behavior**: This is by design!
- Each browser session is independent
- Party views only show what that party knows
- For live workshops, use verbal communication or shared screen

**Future Enhancement**: Real-time synchronization (WebSockets)

---

## Best Practices

### For Effective Training

1. **Start Simple**:
   - Use Scenario A (Second Thomas Shoal) first
   - Only 2 parties initially
   - 3 issue areas maximum

2. **Let Participants Struggle**:
   - Don't give them the "right" answer
   - Let them discover through negotiation
   - Learning happens through trial and error

3. **Use Data to Guide**:
   - Show simulation results as reality check
   - "The agreement looked good, but simulation shows escalation. Why?"
   - Connect abstract utilities to concrete incidents

4. **Debrief Thoroughly**:
   - Process is as important as outcome
   - Discuss emotions, frustrations, surprises
   - Connect to real-world mediation

### For Solo Analysis

1. **Explore Scenario Space**:
   - Try extreme offers (all favorable to one party)
   - Test impact of each parameter
   - Build intuition for what matters

2. **Compare Scenarios**:
   - Run same agreement terms on different scenarios
   - How do incident patterns differ?
   - What does this tell you about the disputes?

3. **Calibrate the Model**:
   - If you have historical data, use Calibrate tab
   - Fit model parameters to real incident counts
   - Improves predictive accuracy

### For Researchers

1. **Document Everything**:
   - Save agreement JSON for each test
   - Screenshot simulation results
   - Note utility scores and probabilities

2. **Vary Systematically**:
   - Hold all but one parameter constant
   - Test effect of that parameter
   - Build response curves

3. **Export Data**:
   - Simulation returns event log as JSON
   - Can export to CSV for analysis
   - Run statistical tests on incident patterns

---

## Advanced Features

### Calibration (Original UI Only)

The original streamlit_app.py includes full calibration functionality:

1. **Purpose**: Fit model parameters to historical data
2. **How**: Provide actual incident counts per time period
3. **Output**: Optimal alpha (risk scale) and base_p (incident pressure)
4. **Usage**: Improves simulation realism

### Custom Scenarios

You can create your own scenarios:

1. **Copy Template**:
   ```bash
   cp cases/scs/scenario_A_second_thomas.json cases/scs/my_scenario.json
   ```

2. **Edit JSON**:
   - Change id, flashpoint, focus
   - Adjust weather_state, media_visibility
   - Modify party weights and BATNAs

3. **Test**:
   - Select in UI
   - Run through workflow
   - Iterate based on results

### API Direct Access

For automation/research:

```python
import requests

# Start session
r = requests.post("http://localhost:8000/bargain/sessions", json={
    "case_id": "my_test",
    "parties": ["PH_GOV", "PRC_MARITIME"],
    "mediator": "Researcher",
    "issue_space": ["resupply_SOP", "hotline_cues"]
})

# Evaluate offer
r = requests.post("http://localhost:8000/bargain/my_test/offer", json={
    "proposer_party_id": "PH_GOV",
    "agreement_vector": {
        "resupply_SOP": {"standoff_nm": 3, "escort_count": 1, "pre_notification_hours": 12}
    }
})

print(r.json())
```

---

## Summary

### Key Takeaways

✅ **Enhanced UI is much easier to use**: Clear workflow, visual feedback, friendly labels

✅ **5-Step Process**: Setup → Build → Evaluate → Simulate → Analyze

✅ **Rich Visualizations**: Metrics, charts, progress bars, color coding

✅ **Two Usage Modes**: Solo analysis + Live workshops

✅ **Based on Best Practices**: Game theory, mediation literature, real scenarios

### Quick Reference Card

| Task | Where | Action |
|------|-------|--------|
| Start session | Step 1 | Select scenario, parties, issues → Start |
| Build offer | Step 2 | Adjust sliders → Proceed |
| Check utilities | Step 3 | Calculate → Review metrics |
| Test durability | Step 4 | Set duration → Run |
| Analyze results | Step 5 | Review metrics, charts, recommendations |
| Refine | Step 5 | Back to Step 2 button |

### Getting Help

- **Documentation**: `/home/dk/scs_mediator_sdk/MULTI_VIEW_GUIDE.md`
- **Participant Guide**: `/home/dk/scs_mediator_sdk/PARTICIPANT_GUIDE.md`
- **Scenarios**: `/home/dk/scs_mediator_sdk/SCS_SCENARIOS_GUIDE.md`
- **Technical**: `/home/dk/scs_mediator_sdk/README.md`

---

**Ready to facilitate!** 🎓
