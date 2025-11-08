# Simulation Workflow Guide
## Understanding the SCS Mediator Training Simulation

**Last Updated**: January 2025
**Version**: 9.0.0

---

## 🎯 Key Concept: Single-User Mediation Training Tool

### What This Tool Is

This is a **single-user training simulation** for mediators and facilitators. You are learning mediation skills by testing different agreement designs and seeing how they perform.

### What This Tool Is NOT

- ❌ NOT a multiplayer game where different people play different countries
- ❌ NOT a role-playing simulation with human stakeholders
- ❌ NOT a negotiation game where you compete against other players

### Who Are The "Stakeholders"?

The countries (Philippines, China, Vietnam, Malaysia) are **AI agents** in the simulation. They:
- Evaluate agreement proposals based on their interests
- React to incidents during simulations
- Make decisions according to their behavioral models
- Are NOT controlled by human players

### Your Role: The Mediator/Facilitator

**You are the mediator** trying to design an agreement that:
- Satisfies all parties (AI agents)
- Reduces conflict incidents
- Maintains stability over time
- Balances competing interests

---

## 📋 The 5-Step Workflow

The simulation follows a structured workflow for iterative learning:

```
┌─────────────────────────────────────────────────────┐
│  Step 1: Setup Session                              │
│  ↓                                                   │
│  Step 2: Build Agreement Offer                      │
│  ↓                                                   │
│  Step 3: Evaluate Offer (AI Analysis)               │
│  ↓                                                   │
│  Step 4: Simulate Agreement Durability              │
│  ↓                                                   │
│  Step 5: Analyze Results & Refine                   │
│  ↓                                                   │
│  ← Return to Step 2 to improve agreement ←          │
└─────────────────────────────────────────────────────┘
```

---

### STEP 1: 🎬 Setup Session

**Who**: Facilitator (you)

**What**: Choose scenario and configure the negotiation context

**Actions**:
1. Select your role: **Facilitator**
2. Choose a scenario:
   - 📍 Scenario A: Second Thomas Shoal (Resupply)
   - 📍 Scenario B: Scarborough Shoal (Fishing Rights)
   - 📍 Scenario C: Kasawari Gas Field (Energy)
   - 📍 Scenario D: Natuna Islands (EEZ Boundaries)
3. Review parties involved (e.g., PH_GOV, PRC_MARITIME)
4. Select issues to negotiate (resupply procedures, hotlines, fishing rights, etc.)
5. Click **"▶️ Start Session"**

**What Happens**:
- System creates a bargaining session with the selected parameters
- Issue space is defined for the negotiation
- Session is ready for agreement design

**Duration**: 2-3 minutes

---

### STEP 2: 📝 Build Agreement Offer

**Who**: Facilitator (you)

**What**: Design the proposed agreement terms

**Actions** (Example: Second Thomas Shoal):

**🚢 Resupply Operations:**
- Set **Standoff Distance** (0-10 nautical miles)
  - How far naval vessels must stay from resupply operations
- Set **Maximum Escort Vessels** (0-5 vessels)
  - Number of military escorts allowed per mission
- Set **Pre-Notification Period** (0-48 hours)
  - Advance notice required before missions

**📞 Communication Protocols:**
- **Hotline Availability**: 24/7 or Ad-Hoc
- **CUES Compliance**: Safe distance, AIS on, video recording

**📰 Media Management:**
- **News Embargo Period** (0-48 hours)
  - Time before incidents can be reported publicly

**Actions for Fishing Scenarios:**
- **Traditional Fishing Access** (0-100%)
- **Seasonal Closures** (0-180 days/year)
- **Joint Patrol Frequency** (weekly/monthly/quarterly)

**What Happens**:
- System stores your agreement configuration
- Agreement is ready for evaluation
- Click **"💾 Save Offer"**

**Duration**: 5-10 minutes

**Key Insight**: You're designing ONE agreement for ALL parties, not making separate offers for each side.

---

### STEP 3: 🤔 Evaluate Offer

**Who**: Facilitator triggers evaluation, AI agents analyze

**What**: Analyze if parties would accept your proposed agreement

**Actions**:
1. Click **"🔍 Evaluate This Offer"**
2. Wait for analysis (5-10 seconds)
3. Review results

**What Happens**:

The **Bargaining Engine** calculates for each party:

**1. Utility Score (0-100%)**
- How good is this deal for them?
- Based on their interests, constraints, and BATNA
- Higher = better for that party

**2. Acceptance Probability (0-100%)**
- Will they say "yes" to this deal?
- Based on utility score and risk tolerance
- Higher = more likely to accept

**3. Overall Agreement Probability**
- Product of all parties' acceptance probabilities
- Shows if deal will succeed

**Example Output**:

```
┌──────────────────────────────────────────────┐
│ 🇵🇭 Philippines Government                    │
│ Utility: 72%           [Green Box]           │
│ Status: Strong                               │
│ Acceptance Probability: 85% ✅               │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ 🇨🇳 PRC Maritime Forces                       │
│ Utility: 38%           [Yellow Box]          │
│ Status: Marginal                             │
│ Acceptance Probability: 48% ⚠️               │
└──────────────────────────────────────────────┘

────────────────────────────────────────────────
Overall Agreement Probability: 41%
(85% × 48% = 41%)

⚠️ Agreement is uncertain. Consider adjusting
   terms to improve acceptance.

ANALYSIS:
• Philippines gets good resupply access (72% utility)
• China feels standoff distance is too restrictive
• Consider reducing escort vessels or increasing
  standoff distance
```

**Duration**: 10-30 seconds

**Decision Point**:
- ✅ If overall probability > 60%: Proceed to simulation
- ⚠️ If 30-60%: Consider refinements
- ❌ If < 30%: Go back to Step 2 and adjust terms

---

### STEP 4: 🎮 Simulate Agreement Durability

**Who**: Facilitator triggers, AI agents act over time

**What**: Test how the agreement holds up under realistic conditions

**Actions**:
1. Set **Simulation Duration** (50-1000 steps)
   - 1 step ≈ 1-2 days
   - 300 steps ≈ 6-12 months
2. Click **"▶️ Run Simulation"**
3. Wait for simulation to complete

**What Happens Behind The Scenes**:

The **Agent-Based Model** runs for the specified duration:

```
Simulation running (300 time steps)...

Step 1:
  → China CCG patrol near shoal (within agreement terms)
  → No incident

Step 15:
  → PH resupply mission notified 24h in advance ✓
  → PH sends 1 escort vessel (within agreement) ✓
  → China CCG maintains 3nm distance (agreement) ✓
  → Mission successful, no incident

Step 42:
  → Chinese fishing militia approaches to 2nm
  → VIOLATION: Below 3nm standoff ⚠️
  → Incident triggered
  → Hotline activated
  → Incident recorded: Severity 0.25

Step 78:
  → PH resupply mission
  → China CCG maintains distance ✓
  → Mission successful

Step 156:
  → Weather bad, high seas
  → Fishing vessel drifts close accidentally
  → Incident recorded: Severity 0.15
  → No escalation (weather-related)

...continues for 300 steps...
```

**AI Agents Include**:
- China Coast Guard vessels
- Philippines Coast Guard vessels
- Maritime militia boats
- Fishing vessels
- All following behavioral rules based on:
  - The agreement terms you designed
  - Their interests and aggression levels
  - Environmental factors (weather, visibility)
  - Previous incidents (memory and learning)
  - Domestic political pressure

**Duration**: 30 seconds - 2 minutes (depending on simulation length)

**Output**: Complete incident log with timestamps, actors, severity, and escalation levels

---

### STEP 5: 📈 Analyze Results & Refine

**Who**: Facilitator (you)

**What**: Review simulation results and improve your agreement

**Results Displayed**:

**1. Summary Metrics:**

```
┌─────────────────────────────────────────────┐
│ 📊 SIMULATION SUMMARY                       │
├─────────────────────────────────────────────┤
│ Total Incidents: 23                         │
│   Status: ✅ Good (threshold: <25)          │
│                                             │
│ Avg Severity: 0.31 / 1.0                    │
│   Status: ✅ Low (threshold: <0.40)         │
│                                             │
│ Max Severity: 0.68 / 1.0                    │
│                                             │
│ Trend: ✅ Declining                         │
│   (Early: 12 incidents, Late: 6 incidents)  │
└─────────────────────────────────────────────┘
```

**2. Interpretation Guide:**

```
✅ GOOD OUTCOME:
- Total incidents: 0-25
- Average severity: < 0.40
- Trend: Declining or Stable
→ Agreement appears SUSTAINABLE

⚠️ MIXED OUTCOME:
- Total incidents: 25-40
- Average severity: 0.40-0.60
- Trend: Stable
→ Agreement needs minor adjustments

❌ CONCERNING OUTCOME:
- Total incidents: > 40
- Average severity: > 0.60
- Trend: Escalating
→ Agreement needs major revision
```

**3. Detailed Breakdown:**

```
Incident Types:
• Close approach (no contact): 15 incidents
• Verbal warning exchange: 5 incidents
• Water cannon use: 2 incidents
• Collision: 1 incident

Hotline Usage:
• Calls made: 18
• Successful de-escalation: 16 (89%)
• Failed to prevent escalation: 2 (11%)

Media Embargo Effectiveness:
• Incidents kept confidential: 19 (83%)
• Leaked early: 4 (17%)

Agreement Compliance:
• Full compliance: 78%
• Minor violations: 18%
• Major violations: 4%
```

**What You Learn**:
- Which agreement terms are working
- Which terms are frequently violated
- What types of incidents are most common
- How the situation evolves over time
- Whether your agreement is sustainable

**Duration**: 5-15 minutes (review and analysis)

**Decision Point**:
1. **Satisfied with results?** → Done! (or explore Peace Context features)
2. **Want to improve?** → Return to Step 2, adjust terms, test again
3. **Major issues?** → Rethink approach, try different parameter combinations

---

## 🔄 The Iterative Learning Process

The core learning happens through iteration:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Design Agreement (Step 2)                      │
│         ↓                                       │
│  Evaluate Acceptance (Step 3)                   │
│         ↓                                       │
│  Simulate Durability (Step 4)                   │
│         ↓                                       │
│  Analyze Results (Step 5)                       │
│         ↓                                       │
│  ← Refine & Try Again (Back to Step 2) ←       │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Example Learning Progression**:

**Attempt 1:**
- Standoff: 5nm, Escorts: 2, Notification: 24h
- China acceptance: 48% (too restrictive)
- Don't proceed to simulation

**Attempt 2:**
- Standoff: 3nm, Escorts: 1, Notification: 24h
- Both parties: 67%+ acceptance
- Proceed to simulation
- Result: 45 incidents (high), avg severity 0.52 (high)
- Issue: Too many militia violations

**Attempt 3:**
- Standoff: 3nm, Escorts: 1, Notification: 48h
- Add joint monitoring patrols
- Both parties: 72%+ acceptance
- Result: 23 incidents (good), avg severity 0.31 (low)
- SUCCESS! ✅

---

## 🎯 Concrete Example: Second Thomas Shoal Scenario

Let's walk through a **complete session** from start to finish:

### Context

**Situation**: The Philippines maintains a garrison on BRP Sierra Madre (a grounded ship) at Second Thomas Shoal. China tries to block resupply missions. Tensions are high.

**Your Goal**: Create an agreement that allows safe resupply while managing China's security concerns.

---

### Session Walkthrough

#### **STEP 1: Setup** (2 minutes)

1. Open the app
2. Select role: **Facilitator**
3. Choose scenario: **📍 Scenario A: Second Thomas Shoal (Resupply)**
4. Review context:
   - Parties: Philippines Government, PRC Maritime Forces
   - Issues: Resupply procedures, hotlines, incident response
5. Click **"▶️ Start Session"**

✅ Session created

---

#### **STEP 2: Build Agreement** (7 minutes)

**Your First Attempt:**

**🚢 Resupply Operations:**
- Standoff Distance: **5 nautical miles**
  - *Reasoning: Give plenty of space to avoid confrontation*
- Maximum Escort Vessels: **2**
  - *Reasoning: Philippines needs security*
- Pre-Notification Period: **24 hours**
  - *Reasoning: Reasonable advance notice*

**📞 Communication:**
- Hotline: **24/7 Direct Line**
- CUES: **All compliance options checked**

**📰 Media:**
- Embargo: **12 hours**

Click **"💾 Save Offer"**

---

#### **STEP 3: Evaluate** (30 seconds)

Click **"🔍 Evaluate This Offer"**

**Results:**

```
🇵🇭 Philippines: 72% utility → 85% acceptance ✅
🇨🇳 PRC: 38% utility → 48% acceptance ⚠️

Overall Probability: 41% (too low)

Analysis: China feels 5nm standoff and 2 escorts
are too restrictive. They want more control.
```

**Your Decision**: "This won't work. Let me adjust..."

---

#### **STEP 2: Refine Agreement** (3 minutes)

**Your Second Attempt (adjustments):**

**🚢 Resupply Operations:**
- Standoff Distance: **3 nautical miles** (↓ reduced from 5)
- Maximum Escort Vessels: **1** (↓ reduced from 2)
- Pre-Notification Period: **24 hours** (unchanged)

**📞 Communication:** (unchanged)

**📰 Media:** (unchanged)

Click **"💾 Save Offer"**

---

#### **STEP 3: Re-Evaluate** (30 seconds)

Click **"🔍 Evaluate This Offer"**

**New Results:**

```
🇵🇭 Philippines: 68% utility → 78% acceptance ✅
🇨🇳 PRC: 52% utility → 67% acceptance ✅

Overall Probability: 52% (borderline)

Better! Still uncertain but worth testing.
```

**Your Decision**: "Let's see how this performs over time."

Click **"➡️ Proceed to Simulation"**

---

#### **STEP 4: Simulate** (1 minute)

Set simulation:
- Duration: **300 steps** (≈ 6 months)

Click **"▶️ Run Simulation"**

**Simulation runs...**

```
⏳ Running simulation...

Timeline:
• Days 1-30: Quiet period, compliance high
• Days 31-60: 3 minor incidents (fishing militia)
• Days 61-120: 8 incidents (2 water cannon use)
• Days 121-180: 6 incidents (tension stabilizing)
• Days 181-240: 4 incidents (hotline effective)
• Days 241-300: 2 incidents (trend improving)

Total: 23 incidents over 6 months
```

✅ Simulation complete

---

#### **STEP 5: Analyze** (10 minutes)

**Results:**

```
📊 SIMULATION SUMMARY

Total Incidents: 23 ✅
   (Good outcome: <25)

Avg Severity: 0.31 / 1.0 ✅
   (Low severity: <0.40)

Max Severity: 0.68 / 1.0
   (One serious incident, but isolated)

Trend: ✅ Declining
   (Early period: 12, Late period: 6)
```

**Detailed Analysis:**

```
Incident Types:
• Close approach without contact: 15
• Verbal warning exchanges: 5
• Water cannon directed at vessel: 2
• Minor collision (fishing boat): 1

When Did Incidents Occur?
• During resupply missions: 8 (35%)
• During routine patrols: 10 (43%)
• Fishing-related: 5 (22%)

Hotline Effectiveness:
• Total hotline calls: 18
• De-escalation successful: 16 (89%)
• Failed to prevent escalation: 2 (11%)

Agreement Compliance:
• Philippines full compliance: 92%
• China full compliance: 81%
• Militia violations (China-linked): 7%
```

**What Worked:**
- ✅ 3nm standoff reduced confrontations
- ✅ 24h notification allowed coordination
- ✅ Hotline de-escalated 89% of incidents
- ✅ Trend declining (situation improving)

**What Didn't Work:**
- ⚠️ Maritime militia still causing 7 violations
- ⚠️ 2 serious water cannon incidents
- ⚠️ Media embargo leaked 4 times (17%)

**Interpretation:**

```
✅ OVERALL ASSESSMENT: SUSTAINABLE

This agreement creates a workable framework:
• Low incident count (23 over 6 months)
• Low average severity (0.31)
• Improving trend (declining incidents)
• High compliance rate (81-92%)
• Effective de-escalation mechanisms (89%)

RECOMMENDATION:
Agreement is viable for implementation.
Monitor militia compliance and consider adding
joint patrol mechanisms to reduce violations further.
```

---

#### **Your Next Steps:**

**Option 1: Refine Further**
- Could you reduce incidents from 23 to <15?
- Add joint monitoring patrols?
- Strengthen militia command-and-control?
- Test again with adjusted terms

**Option 2: Explore Peace Context**
- Check escalation ladder assessment
- Review confidence-building measures (CBMs)
- Analyze spoiler risks
- Explore multi-track diplomacy options

**Option 3: Done**
- Accept this as a viable agreement
- Document your findings
- Present results to stakeholders (in real scenario)

---

## 🎮 Additional Features

### Peace Context Tab (Step 6)

After completing the 5-step workflow, explore additional analysis:

**1. Escalation Ladder**
- Assess current conflict level (1-10)
- Identify escalation risks
- Get de-escalation recommendations

**2. Confidence-Building Measures (CBMs)**
- Browse 45+ CBM options by category:
  - Communication & Transparency
  - Military & Security
  - Economic Cooperation
  - Symbolic Gestures
- Get implementation recommendations

**3. Domestic Constraints**
- Analyze win-sets (range of acceptable deals)
- Review domestic political actors
- Understand ratification challenges

**4. Spoiler Management**
- Identify potential spoilers
- Assess spoiling risk
- Get protective measures

**5. Multi-Track Diplomacy**
- Coordinate Tracks 1-9
- Get phase-specific recommendations
- Plan complementary diplomatic activities

---

### Strategic Levers (In Agreement Evaluation)

When evaluating agreements, you can also test **Strategic Actions**:

**Types of Actions:**

**1. Goodwill Gestures**
- Unilateral patrol reduction
- Fishing zone access
- Humanitarian cooperation
- Cultural exchanges

**2. Media Management**
- Joint press statements
- Media blackouts
- Strategic transparency
- Narrative framing

**3. Economic Incentives**
- Joint development zones
- Trade benefits
- Investment packages
- Economic aid

**4. Security Measures**
- Military de-escalation
- Buffer zones
- Joint exercises
- Arms limitations

**How It Works:**
1. Select action type and intensity
2. System simulates impact on:
   - Acceptance probabilities (changes in utility)
   - Domestic political support
   - Regional stability
   - International perception
3. See predicted outcomes before implementing
4. Add to agreement if beneficial

---

## ❓ Frequently Asked Questions

### About Roles

**Q: Do Philippines and China players log in separately?**

**A**: NO! They are AI agents in the simulation, not human players. You (the facilitator) control the entire session.

---

**Q: Who are the "stakeholders"?**

**A**: AI agents representing countries (PH_GOV, PRC_MARITIME, VN_CG, MY_CG) that:
- Evaluate agreement proposals
- React to incidents in simulations
- Make decisions based on their interests
- Are NOT controlled by humans

---

**Q: Can I invite participants to play as different countries?**

**A**: Not currently. This is designed as a single-user training tool for mediators. However, you could:
- Use it in a classroom setting where students take turns being the mediator
- Project the screen and discuss decisions as a group
- Have students work in pairs/groups on different scenarios

---

**Q: What's the facilitator/mediator doing?**

**A**: Learning mediation skills by:
- Analyzing conflict situations
- Designing balanced agreements
- Predicting stakeholder reactions
- Testing agreement durability
- Refining based on results
- Understanding peace-building tools

---

### About Workflow

**Q: Do I make separate offers to each party?**

**A**: NO! You design ONE agreement that applies to ALL parties. The AI agents then evaluate whether they would accept that single agreement.

This reflects real mediation: mediators propose framework agreements, not separate bilateral deals.

---

**Q: What if acceptance probability is low (e.g., 30%)?**

**A**: Go back to Step 2 and adjust your terms:
- If one party has low utility: make concessions that benefit them
- If both parties have marginal utility: find creative solutions
- Use the AI Guide to get suggestions
- Try different parameter combinations

The tool is designed for iteration!

---

**Q: How long does a typical session take?**

**A**:
- **Quick test**: 15-20 minutes (1-2 iterations)
- **Thorough exploration**: 45-60 minutes (4-5 iterations + peace context)
- **Classroom session**: 90 minutes (including discussion)

---

**Q: Can I save my session and come back later?**

**A**: Currently, sessions are stored in browser memory. To preserve work:
- Keep your browser tab open
- Take screenshots of key results
- Export agreement configurations (if available)
- Document findings in separate notes

---

### About Simulations

**Q: Are the simulation results deterministic?**

**A**: No, they include randomness (stochastic elements):
- Agent decisions have probabilistic components
- Environmental factors vary (weather, visibility)
- Incident triggers have random elements

Running the same agreement twice may yield slightly different results. This reflects real-world uncertainty.

---

**Q: What does "300 steps" mean?**

**A**: Each step represents approximately 1-2 days:
- 50 steps ≈ 3 months
- 150 steps ≈ 6 months
- 300 steps ≈ 12 months (1 year)
- 600 steps ≈ 2 years

Longer simulations test long-term durability but take more time to run.

---

**Q: What's a "good" result?**

**A**:
- **Total incidents**: < 25 (excellent), 25-40 (acceptable), > 40 (concerning)
- **Average severity**: < 0.30 (excellent), 0.30-0.50 (acceptable), > 0.50 (concerning)
- **Trend**: Declining or Stable (good), Escalating (bad)

Context matters! A high-tension scenario (e.g., disputed sovereignty) will naturally have more incidents than a low-tension one (e.g., fishing cooperation).

---

**Q: Why do AI agents sometimes violate the agreement?**

**A**: This reflects reality:
- Imperfect command-and-control (especially with militias)
- Domestic political pressure
- Opportunistic behavior
- Accidents and misunderstandings
- Spoiler actions

Perfect compliance is unrealistic. The goal is to minimize violations and have effective response mechanisms (like hotlines).

---

### About Learning

**Q: What should I learn from this tool?**

**A**:
- **Balance**: Finding terms acceptable to all parties
- **Trade-offs**: Understanding what concessions create stability
- **Prediction**: Anticipating how agreements perform over time
- **Iteration**: Refining proposals based on feedback
- **Context**: Applying appropriate peace-building tools
- **Complexity**: Managing multi-dimensional conflicts

---

**Q: How realistic are the simulations?**

**A**: The model is based on:
- Historical SCS incidents (2012-2024)
- Academic literature on maritime conflicts
- Rational choice theory and game theory
- Agent-based modeling best practices

However, it's a **training tool**, not a policy prediction system. Real-world conflicts involve factors (personalities, unexpected events, international dynamics) that models can't fully capture.

Validation shows 72% accuracy against historical incidents.

---

**Q: Can I use this for actual policy-making?**

**A**: The tool is designed for:
- ✅ Education and training
- ✅ Exploring "what-if" scenarios
- ✅ Understanding conflict dynamics
- ✅ Testing mediation concepts

It should NOT be used for:
- ❌ Making actual diplomatic decisions
- ❌ Predicting specific real-world outcomes
- ❌ Advising governments without expert validation
- ❌ Replacing professional mediators

Think of it like a flight simulator: great for training, but you wouldn't use it to plan an actual flight.

---

## 📚 Next Steps

### For First-Time Users

1. **Start with Scenario A** (Second Thomas Shoal): Most straightforward
2. **Run through all 5 steps** once without optimization
3. **Try 2-3 refinement iterations** to see how changes affect results
4. **Explore Peace Context features** after mastering the core workflow

### For Advanced Users

1. **Test extreme scenarios**: What happens with very restrictive vs. very permissive terms?
2. **Compare scenarios**: How do fishing disputes differ from resupply conflicts?
3. **Optimize systematically**: Can you achieve < 15 incidents with high acceptance?
4. **Combine with strategic levers**: Test how goodwill gestures affect outcomes

### For Instructors/Facilitators

1. **Prepare scenarios in advance**: Know which parameters to focus on
2. **Use projector for group discussion**: Discuss decisions collectively
3. **Assign different scenarios to different groups**: Compare approaches
4. **Focus on learning goals**: Balance, trade-offs, iteration, not "winning"

---

## 🔗 Related Documentation

- **DEPLOYMENT_GUIDE.md**: How to deploy to Streamlit Cloud
- **MODEL_ASSUMPTIONS_AND_VALIDATION.md**: How the simulation works
- **API_DOCUMENTATION.md**: Technical API reference (for developers)

---

## 🆘 Getting Help

### AI Guide Feature

Both facilitators and participants have access to an **AI Guide**:
- Located in the sidebar
- Ask questions about the scenario
- Get suggestions for agreement terms
- Understand simulation results
- Learn about peace-building tools

Example questions:
- "What standoff distance would China find acceptable?"
- "Why did incidents increase in the simulation?"
- "What CBMs would help with fishing disputes?"

### Contact & Support

For questions, feedback, or issues:
- Check this documentation first
- Use the AI Guide for scenario-specific help
- Review MODEL_ASSUMPTIONS_AND_VALIDATION.md for technical details

---

**Last Updated**: January 2025
**Version**: 9.0.0
**For**: SCS Mediator SDK Training Simulation
