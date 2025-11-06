 Complete Instructor User Manual
 SCS Mediation Simulation - Comprehensive Feature Guide

Version: 10.0
Last Updated: November 2025
Purpose: Complete reference for all features, options, and strategic considerations


 Table of Contents

1. [Introduction](introduction)
2. [Complete UI Reference](complete-ui-reference)
3. [All Scenario Parameters Explained](all-scenario-parameters-explained)
4. [All Agreement Options Deep Dive](all-agreement-options-deep-dive)
5. [Understanding All Metrics](understanding-all-metrics)
6. [Strategic Decision Framework](strategic-decision-framework)
7. [Training Scenario Analysis](training-scenario-analysis)
8. [Advanced Features](advanced-features)
9. [Scenario-Aware Features (V2 Enhancement)](#scenario-aware-features-v2-enhancement)
10. [Peace Mediation Tools (V2 Enhancements)](#peace-mediation-tools-v2-enhancements)
11. [Interpretation Guidelines](interpretation-guidelines)
12. [Case Studies](case-studies)



 Introduction

 What This Manual Covers

This is a complete reference for every feature, option, and consideration in the SCS Mediation Simulation. Unlike the quick start guide, this manual:

- ✅ Explains every slider, dropdown, and button
- ✅ Details all parameters and their effects
- ✅ Provides strategic frameworks for decision-making
- ✅ Includes real examples from training scenarios
- ✅ Covers all metrics and their interpretation
- ✅ Gives specific guidance for each scenario
- ✅ Explains underlying game theory and simulation mechanics

 Who Should Use This

- Instructors running training workshops
- Researchers conducting systematic analysis
- Curriculum Developers designing training programs
- Advanced Users who want to understand every detail



 Complete UI Reference

 Role Selection Page

 Instructor Button

Location: Left side, blue box

What It Does:
- Grants full visibility into the simulation
- Allows you to see ALL parties' utilities
- Enables you to run simulations
- Provides control over session parameters

When to Use:
- Solo analysis and testing
- Facilitating live training
- Researching agreement patterns
- Demonstrating the tool

What You'll See After Clicking:
- 5-step workflow guide at top
- Expandable sections for each step
- Sidebar with session information
- Logout button



 Party Selection

Location: Right side, green box

Options:
1. 🇵🇭 Philippines Government
   - Weak military, strong legal position
   - Focus: Resupply access, sovereignty
   - Typical role: Challenger to status quo

2. 🇨🇳 PRC Maritime Forces
   - Strong military, weak legal position
   - Focus: Territorial control, strategic dominance
   - Typical role: Status quo defender

3. 🇻🇳 Vietnam Coast Guard
   - Middle power, mixed legal position
   - Focus: Fishing rights, energy resources
   - Typical role: Regional stakeholder

4. 🇲🇾 Malaysia Coast Guard
   - Neutral power, defensive position
   - Focus: EEZ protection, economic interests
   - Typical role: Mediator or secondary party

What Happens After Selection:
- Redirects to party-specific view
- Shows only that party's information
- Limits visibility to realistic information
- Enables party-specific offer submission



 Step 1: Setup Scenario & Session

 Scenario Selection Dropdown

Location: Step 1, left column

Available Scenarios:

 🏝️ Scenario A: Second Thomas Shoal (Resupply Operations)

JSON File: `scenario_A_second_thomas.json`

Key Parameters:
```json
{
  "id": "scs_second_thomas",
  "flashpoint": "Second Thomas Shoal",
  "focus": "resupply_operations",
  "weather_state": "rough",
  "media_visibility": 3,
  "difficulty": "intermediate"
}
```

What This Scenario Models:
- Context: Philippines maintains garrison on grounded BRP Sierra Madre
- Tension: China blocks resupply attempts with coast guard vessels
- Incidents: Water cannon attacks, ramming, blockades
- Stakes: If garrison evacuated, Philippines loses presence
- International: High media attention, UNCLOS tribunal ruled for Philippines

Why These Parameters:
- `weather_state: "rough"` = Resupply missions more dangerous
- `media_visibility: 3` = High international scrutiny
- `difficulty: "intermediate"` = Clear interests, some common ground



Best For Training:
- Introduction to maritime disputes
- Asymmetric power dynamics
- Balancing sovereignty vs. escalation
- Role of international law

Typical Agreement Range:
- Standoff: 2-4 nm
- Escorts: 1-2 vessels
- Notification: 8-18 hours
- Success metrics: <20 incidents, declining trend



 🎣 Scenario B: Scarborough Shoal (Fishing Rights)

JSON File: `scenario_B_scarborough.json`

Key Parameters:
```json
{
  "id": "scs_scarborough",
  "flashpoint": "Scarborough Shoal",
  "focus": "fishing_rights",
  "weather_state": "calm",
  "media_visibility": 2,
  "difficulty": "advanced"
}
```

What This Scenario Models:
- Context: Traditional fishing grounds claimed by multiple parties
- Tension: Chinese coast guard controls access since 2012
- Incidents: Detention of fishermen, vessel seizures
- Stakes: Livelihoods of thousands of fishermen
- Complexity: Economic vs. sovereignty issues

Why These Parameters:
- `weather_state: "calm"` = More fishing activity, more encounters
- `media_visibility: 2` = Moderate attention (unless major incident)
- `difficulty: "advanced"` = High tension, limited common ground

Best For Training:
- Economic dimensions of conflict
- Civil society involvement (fishermen)
- De-escalation when trust is low
- Creative solution finding

Typical Agreement Range:
- Fishing corridors: Alternating days or zones
- Monitoring: Joint patrols or observer program
- Safety: Emergency assistance protocols
- Success metrics: <30 incidents, but higher severity acceptable if no detentions



 ⛽ Scenario C: Kasawari Gas Field (Energy Resources)

JSON File: `scenario_C_kasawari.json`

Key Parameters:
```json
{
  "id": "scs_kasawari",
  "flashpoint": "Kasawari Gas Field",
  "focus": "energy_resources",
  "weather_state": "calm",
  "media_visibility": 1,
  "difficulty": "advanced"
}
```

What This Scenario Models:
- Context: Natural gas field in disputed waters
- Tension: Malaysia exploring, China claims sovereignty
- Incidents: Standoffs near drilling rigs, harassment of survey vessels
- Stakes: Billions in energy revenue
- Corporate Dimension: Oil companies involved

Why These Parameters:
- `weather_state: "calm"` = Allows continuous operations
- `media_visibility: 1` = Low until major incident (then spikes)
- `difficulty: "advanced"` = Economic vs. sovereignty, third-party (corporations)

Best For Training:
- Economic negotiations (joint development)
- Multi-stakeholder dynamics
- Risk of rapid escalation
- Creative arrangements (revenue sharing)

Typical Agreement Range:
- Joint development zones
- Revenue sharing formulas
- Environmental protections
- Success metrics: <15 incidents, high stability needed



 🌊 Scenario D: Natuna Islands (EEZ Boundaries)

JSON File: `scenario_D_natuna.json`

Key Parameters:
```json
{
  "id": "scs_natuna",
  "flashpoint": "Natuna Islands EEZ",
  "focus": "eez_boundaries",
  "weather_state": "calm",
  "media_visibility": 2,
  "difficulty": "intermediate"
}
```

What This Scenario Models:
- Context: Indonesia's EEZ overlaps with China's "nine-dash line"
- Tension: Regular Chinese fishing fleet incursions with coast guard
- Incidents: Vessel chases, towing incidents
- Stakes: Principle of EEZ sovereignty per UNCLOS
- Indonesia's Position: Not a claimant but won't accept infringement

Why These Parameters:
- `weather_state: "calm"` = Year-round fishing activity
- `media_visibility: 2` = National but not always international attention
- `difficulty: "intermediate"` = Clear legal framework (UNCLOS)

Best For Training:
- Third-party perspectives (Indonesia not a direct claimant)
- EEZ law vs. historical claims
- Balancing principles vs. pragmatism
- Regional implications (ASEAN)

Typical Agreement Range:
- Recognition of EEZ rights
- Fishing permit systems
- Hot pursuit protocols
- Success metrics: <25 incidents, stable trend



 Party Selection

Location: Step 1, "Participating Parties" multiselect

Mechanics:
- Can select 2-4 parties
- Default: Philippines + PRC (bilateral)
- Can add Vietnam and/or Malaysia (multilateral)

Strategic Considerations:

2-Party (Bilateral):
- ✅ Simpler negotiation
- ✅ Clearer interests
- ✅ Faster to reach agreement
- ❌ Less representative of regional complexity
- ❌ Excludes stakeholder perspectives

3-Party (Trilateral):
- ✅ More realistic
- ✅ Coalition dynamics
- ✅ More creative solutions possible
- ❌ More complex negotiation
- ❌ Harder to satisfy all parties

4-Party (Multilateral):
- ✅ Most representative
- ✅ ASEAN dynamics
- ✅ Teaches complex mediation
- ❌ Very difficult to reach agreement
- ❌ Time-intensive

Recommendation by Training Goal:

| Goal | Configuration |
|||
| Introduction to mediation | 2-party (PH + PRC) |
| Realistic SCS dynamics | 3-party (PH + PRC + VN) |
| Advanced mediation skills | 4-party (all) |
| Specific scenario focus | Match to scenario (e.g., Kasawari = MY + PRC) |



 Issue Space Selection

Location: Step 1, "Issues to Negotiate" multiselect

Available Issues:

 1. Resupply SOP (Standard Operating Procedures)

Relevant For: Scenarios A, B

What It Covers:
- How resupply missions are conducted
- Rules of engagement for naval/coast guard forces
- Notification and transparency requirements

Parameters (configured in Step 2):
- Standoff distance (nautical miles)
- Escort count (number of vessels)
- Pre-notification time (hours)

Why Include:
- Central to Second Thomas Shoal scenario
- Tests security dilemma (access vs. control)
- Has clear metrics for success/failure

When to Exclude:
- If scenario doesn't involve resupply
- If focusing purely on economic issues



 2. Hotline & CUES (Communication Protocols)

Relevant For: All scenarios

What It Covers:
- Direct communication channels between parties
- Code for Unplanned Encounters at Sea (CUES) compliance
- Crisis management procedures

Parameters (configured in Step 2):
- Hotline availability (ad-hoc vs. 24/7)
- CUES checklist items (distance, AIS, recording)

Why Include:
- Essential for de-escalation
- Relatively easy to agree on
- Creates foundation for other agreements

When to Exclude:
- Never - this should always be included
- It's a confidence-building measure



 3. Media Protocol

Relevant For: All scenarios, especially high-visibility ones

What It Covers:
- How incidents are reported publicly
- Joint statement procedures
- News embargo periods

Parameters (configured in Step 2):
- Embargo hours (delay before public reporting)

Why Include:
- Reduces domestic political pressure
- Allows face-saving time
- Prevents incident escalation via media

When to Exclude:
- If parties aren't sensitive to public opinion
- If transparency is paramount



 4. Fishing Rights

Relevant For: Scenarios B, D

What It Covers:
- Access to fishing grounds
- Seasonal restrictions
- Joint management

Parameters (configured in Step 2):
- Fishing corridors (geographic zones)
- Seasonal windows
- Monitoring mechanisms

Why Include:
- Central to Scarborough Shoal
- Affects livelihoods (high stakes)
- Allows creative solutions

When to Exclude:
- If scenario doesn't involve fishing
- If focusing on pure sovereignty issues



Strategic Consideration: Issue Linkage

Fewer Issues (2-3):
- ✅ Simpler negotiation
- ✅ Easier to reach agreement
- ❌ Less room for creative trades
- ❌ May leave important topics unaddressed

More Issues (3-4):
- ✅ More comprehensive agreement
- ✅ More opportunities for package deals
- ✅ More realistic
- ❌ More complex
- ❌ May get bogged down

Recommended Combinations:

| Scenario | Recommended Issues | Rationale |
|-|-|--|
| Second Thomas | Resupply SOP + Hotline + Media | Core operational issues |
| Scarborough | Fishing + Hotline + Media | Economic + safety |
| Kasawari | Fishing + Hotline (+ Energy if available) | Resource management |
| Natuna | Resupply SOP (modified for EEZ) + Hotline | Sovereignty + safety |



 Step 2: Build Agreement Offer

This is where you configure the actual terms of the proposed agreement. Every parameter has strategic implications.

 Resupply Operations Parameters

 Standoff Distance (0-10 nautical miles)

What It Is: How far military/coast guard vessels must stay from resupply operations

Scale:
- 0 nm = No buffer (vessels can be right next to resupply)
- 5 nm = Moderate buffer
- 10 nm = Large buffer

Effects:

Philippines Perspective:
- Lower (0-3 nm):
  - ✅ Easier resupply (shorter distance to cover)
  - ✅ More verification of Chinese compliance
  - ❌ Feels less secure (Chinese vessels nearby)
  - Utility Impact: +0.15 to +0.20 per nm decrease

- Higher (6-10 nm):
  - ❌ Harder resupply (longer exposed distance)
  - ❌ Less verification
  - ✅ More security during operation
  - Utility Impact: -0.10 to -0.15 per nm increase

China Perspective:
- Lower (0-3 nm):
  - ❌ Less control over area
  - ❌ Appearance of Philippines "winning"
  - ✅ Ability to monitor closely
  - Utility Impact: -0.18 to -0.22 per nm decrease

- Higher (6-10 nm):
  - ✅ Maintains control posture
  - ✅ Face-saving (not appearing weak)
  - ❌ Less monitoring capability
  - Utility Impact: +0.12 to -0.18 per nm increase

Simulation Effects:
- Lower standoff: Higher incident probability (vessels in proximity)
- Higher standoff: Lower incidents but higher severity if they occur (less monitoring = surprises)

Optimal Range (based on historical analysis):
- 2-4 nm: Best balance
  - Philippines can resupply effectively
  - China maintains some distance posture
  - Verification possible
  - Incidents lower than no-agreement baseline

Training Considerations:
- Start negotiations at 5 nm (neutral midpoint)
- Philippines typically pushes for 2-3 nm
- China typically pushes for 6-8 nm
- Compromise often lands at 3-5 nm

How to Decide:
1. What's current practice? (Baseline: ~1 nm or less = high conflict)
2. What does Philippines minimally need? (3 nm for safe operations)
3. What can China accept without domestic backlash? (4-5 nm = some distance)
4. What reduces incidents? (Simulation shows 3-4 nm optimal)

Red Flags:
- 0-1 nm: Philippines "winning" too much, China won't accept
- 8-10 nm: Philippines can't effectively resupply, won't accept
- Anything outside 2-6 nm range is likely unacceptable to one party



 Escort Count (0-5 vessels)

What It Is: Number of Philippines military/coast guard vessels allowed to escort each resupply mission

Scale:
- 0 = No escorts (civilian resupply only)
- 1-2 = Light escort (typical)
- 3-5 = Heavy escort (militarized)

Effects:

Philippines Perspective:
- No Escorts (0):
  - ❌ Vulnerable to harassment
  - ❌ Can't defend if attacked
  - ❌ Appears weak domestically
  - Utility Impact: -0.30 (major negative)

- Light Escort (1-2):
  - ✅ Basic protection
  - ✅ Reasonable for routine operations
  - ✅ Not overly provocative
  - Utility Impact: 0 (baseline)

- Heavy Escort (3-5):
  - ✅ Strong deterrence
  - ✅ Shows strength domestically
  - ❌ Provocative to China
  - ❌ Risk of escalation
  - Utility Impact: +0.10 to +0.15 (diminishing returns)

China Perspective:
- No Escorts (0):
  - ✅ De-militarization
  - ✅ Face-saving (Philippines "weaker")
  - ❌ Unrealistic (Philippines won't accept)
  - Utility Impact: +0.25

- Light Escort (1-2):
  - ✅ Acceptable level of militarization
  - ⚠️ Neutral on face
  - Utility Impact: 0 (baseline)

- Heavy Escort (3-5):
  - ❌ Militarization of dispute
  - ❌ Appears China "lost"
  - ❌ Triggers nationalist backlash
  - Utility Impact: -0.20 to -0.35 per vessel above 2

Simulation Effects:
- No escorts: High severity incidents (Philippines vessels easily harassed)
- Light escorts (1-2): Moderate incidents, lower severity
- Heavy escorts (3-5): Lower incidents BUT higher risk of military confrontation

Optimal Range:
- 1-2 vessels: Best balance
  - Provides basic security
  - Not overly provocative
  - Simulation shows lowest incident count + severity combined

Training Considerations:
- This is often a sticking point
- Philippines emotional attachment to "not appearing weak"
- China sensitive to "militarization" narrative
- Creative solution: Vary by weather (2 in rough seas, 1 in calm)

How to Decide:
1. What's minimum for Philippines security? (1 escort)
2. What's maximum China will tolerate? (2 escorts)
3. What reduces escalation risk? (1-2)
4. Can you vary by conditions? (Yes, add flexibility clause)

Red Flags:
- 0 escorts: Philippines will reject (too vulnerable)
- 3+ escorts: China will reject (too militarized)
- Rigid number with no flexibility: Misses opportunity for conditional agreements



 Pre-Notification Period (0-48 hours)

What It Is: How much advance notice Philippines must give China before conducting resupply

Scale:
- 0 hours = No notice (surprise resupply)
- 12 hours = Half-day notice
- 24 hours = Full-day notice
- 48 hours = Two-day notice

Effects:

Philippines Perspective:
- Short Notice (0-6 hours):
  - ✅ Operational flexibility
  - ✅ Weather windows (can respond quickly)
  - ❌ China suspicious (surprise attacks?)
  - Utility Impact: +0.08 per 6-hour decrease from baseline

- Medium Notice (12-18 hours):
  - ✅ Balances flexibility and transparency
  - ⚠️ Neutral on other dimensions
  - Utility Impact: 0 (baseline)

- Long Notice (24-48 hours):
  - ❌ Inflexible (weather may change)
  - ❌ Operational hindrance
  - ✅ Builds trust
  - Utility Impact: -0.06 per 6-hour increase above 18 hours

China Perspective:
- Short Notice (0-6 hours):
  - ❌ Can't prepare monitoring
  - ❌ Feels like Philippines acting unilaterally
  - Utility Impact: -0.12 per 6-hour decrease from baseline

- Medium Notice (12-18 hours):
  - ✅ Time to position vessels
  - ✅ Demonstrates Philippines cooperation
  - Utility Impact: 0 (baseline)

- Long Notice (24-48 hours):
  - ✅ Full preparation time
  - ✅ Transparency (builds confidence)
  - ❌ Gives impression Philippines asking permission
  - Utility Impact: +0.10 per 6-hour increase (up to 24 hours, then flat)

Simulation Effects:
- Short notice: Higher incidents (Chinese vessels surprised, scramble to respond)
- Medium notice (12-18h): Optimal incident rates (predictability reduces surprises)
- Long notice (24-48h): Slightly higher incidents (gives China time to organize blockade)

Optimal Range:
- 12-18 hours: Sweet spot
  - Philippines has operational flexibility
  - China has time to monitor appropriately
  - Simulation shows lowest incident rates

Training Considerations:
- Often easy to agree on this parameter
- Both sides benefit from predictability
- Can be paired with other concessions
- Creative: "12 hours normally, 6 hours in emergencies"

How to Decide:
1. What's operationally feasible for Philippines? (8+ hours)
2. What's minimum for China to respond appropriately? (12 hours)
3. What's the weather window risk? (Short notice better in typhoon season)
4. Can we add emergency provisions? (Yes, emergency clause)

Red Flags:
- 0 hours: China will reject (feels unilateral)
- 48 hours: Philippines may reject (too constraining)
- One-size-fits-all: Consider seasonal or emergency variations



 Communication Protocols Parameters

 Hotline Availability (Ad-Hoc vs. 24/7)

What It Is: Direct communication channel between operational commanders

Options:

Ad-Hoc (As Needed):
- Phone numbers exchanged
- Call when incident occurs or planned operation
- No dedicated staff
- Cost: Low
- Effectiveness: Moderate (if answered)

24/7 (Always Available):
- Dedicated hotline
- Staff on duty at all times
- Mandatory response times
- Cost: Higher (staff, infrastructure)
- Effectiveness: High (immediate communication)

Effects:

Philippines Perspective:
- Ad-Hoc:
  - ✅ Less commitment (lower investment)
  - ❌ May not be answered in crisis
  - ❌ Slower de-escalation
  - Utility Impact: -0.08

- 24/7:
  - ✅ Crisis management capability
  - ✅ Shows Chinese commitment
  - ❌ More expensive to maintain
  - Utility Impact: +0.08

China Perspective:
- Ad-Hoc:
  - ✅ Less formal commitment
  - ✅ Lower cost
  - ❌ May be blamed if incident escalates
  - Utility Impact: -0.05

- 24/7:
  - ✅ Professional, responsible image
  - ✅ Crisis prevention
  - ❌ More formal institutionalization
  - Utility Impact: +0.05

Simulation Effects:
- Ad-Hoc: 15-20% more incidents escalate to high severity
- 24/7: Better de-escalation, faster incident resolution

Optimal Choice:
- 24/7 for high-tension scenarios (A, B)
- Ad-Hoc acceptable for low-tension (C, D)

Training Considerations:
- Relatively easy agreement point
- Both sides benefit
- Can be "free" concession in package deal
- Often agreed early to build momentum

How to Decide:
1. How high is tension? (High = 24/7 needed)
2. Is there existing comm infrastructure? (Build on existing)
3. Can this be a confidence-building measure? (Yes, agree early)
4. What's the cost-benefit? (24/7 cost is low compared to incident cost)

Red Flags:
- Insisting on ad-hoc in high-tension scenario = not serious about de-escalation
- Not agreeing on any communication = recipe for disaster



 CUES Compliance Requirements

What It Is: Code for Unplanned Encounters at Sea - internationally recognized protocols

Available Requirements:

 Safe Distance Keeping

What It Means: Vessels maintain specified separation (typically 500-1000 meters)

Effect on Philippines:
- ✅ Safety for resupply vessels
- ✅ Reduces collision risk
- Utility Impact: +0.10

Effect on China:
- ⚠️ Neutral (professional standard)
- ✅ Reduces accident risk
- Utility Impact: +0.05

Simulation Impact: 30% reduction in ramming/collision incidents

Training Note: Easy to agree - professional standard



 AIS Transponders Active

What It Means: Automatic Identification System broadcasts vessel location

Effect on Philippines:
- ✅ Transparency (know where Chinese vessels are)
- ✅ Verification of compliance
- Utility Impact: +0.12

Effect on China:
- ❌ Reduces tactical surprise
- ❌ More transparency than preferred
- Utility Impact: -0.08

Simulation Impact: 20% reduction in "surprise encounter" incidents

Training Note: Moderate difficulty - China may resist



 Incident Video Recording

What It Means: All parties record encounters for later review

Effect on Philippines:
- ✅ Evidence of Chinese behavior
- ✅ Accountability
- Utility Impact: +0.15

Effect on China:
- ❌ Evidence that could embarrass
- ❌ Limits operational freedom
- Utility Impact: -0.15

Simulation Impact: 25% reduction in aggressive behavior (deterrent effect)

Training Note: Difficult - China often rejects



Strategic Consideration: Package these requirements

- Minimum (Distance only): Basic safety, both parties accept
- Standard (Distance + AIS): Good transparency, moderate agreement difficulty
- Maximum (All three): High accountability, difficult to achieve

Recommendation: Start with Distance + AIS, offer to drop Video if needed for overall agreement



 Media Protocol Parameters

 News Embargo Period (0-48 hours)

What It Is: Agreed delay before incidents can be reported to media

Scale:
- 0 hours = Immediate reporting allowed
- 6 hours = Short embargo (same day still possible)
- 12 hours = Half-day embargo
- 24 hours = Full-day embargo
- 48 hours = Two-day embargo

Rationale: Allows parties time to:
- Investigate what happened
- Coordinate messaging
- Brief leadership
- Prevent inflammatory first reports
- Craft joint statement if appropriate

Effects:

Philippines Perspective:
- No Embargo (0 hours):
  - ✅ Transparency
  - ✅ Domestic support (show we're standing up)
  - ❌ May escalate before de-escalation possible
  - Utility Impact: -0.05 to -0.10

- Short Embargo (6-12 hours):
  - ✅ Some time for coordination
  - ✅ Not too restrictive
  - ⚠️ Neutral on other dimensions
  - Utility Impact: 0 (baseline)

- Long Embargo (24-48 hours):
  - ❌ Appears to hide information
  - ❌ Domestic critics say "secret deal"
  - ✅ More de-escalation time
  - Utility Impact: -0.08 to -0.12

China Perspective:
- No Embargo (0 hours):
  - ❌ No time to control narrative
  - ❌ Risk of domestic nationalist pressure
  - Utility Impact: -0.15

- Short Embargo (6-12 hours):
  - ✅ Some face-saving time
  - ⚠️ Acceptable
  - Utility Impact: 0 (baseline)

- Long Embargo (24-48 hours):
  - ✅ Full narrative control
  - ✅ Time for diplomatic resolution
  - ❌ May appear to be censorship
  - Utility Impact: +0.10 to +0.12

Simulation Effects:
- No embargo: Incidents more likely to trigger secondary incidents (public pressure → aggressive response)
- 6-12 hour embargo: Optimal (de-escalation possible, not too restrictive)
- 24+ hour embargo: Minimal additional benefit (most de-escalation happens in first 12 hours)

Optimal Range:
- 6-12 hours: Best balance
  - Time for initial coordination
  - Not overly restrictive
  - Acceptable to both sides

Training Considerations:
- Easy point to concede
- China values this more than Philippines
- Can be traded for something Philippines wants more
- Consider: "6 hours normally, 12 hours for serious incidents"

How to Decide:
1. How media-sensitive is scenario? (High media visibility = longer embargo helpful)
2. What's Philippines domestic politics? (Strong media = shorter embargo)
3. Is this a bargaining chip? (Yes, trade for something else)
4. Does simulation show benefit? (Yes, but diminishing returns after 12 hours)

Red Flags:
- 0 hours: Missing opportunity for de-escalation
- 48+ hours: Appears to be hiding information, transparency concerns
- Inflexible: Consider different lengths for different incident types



 Step 3: Evaluate Offer

This step shows you the game-theoretic analysis of the agreement you built.

 Utility Scores

What You See: Metric cards for each party with score 0.00-1.00

Example Display:
```
🇵🇭 Philippines: 0.68 (Good)
Progress bar: ████████████████░░░░░░░
Status: Acceptable

🇨🇳 PRC: 0.55 (Acceptable)
Progress bar: █████████████░░░░░░░░░░
Status: Marginal
```

How It's Calculated:

 Multi-Attribute Utility Theory (MAUT)

Formula:
```
U_party = Σ(weight_i × value_i)

Where:
- weight_i = importance of issue i to that party (0-1, sum to 1)
- value_i = party's satisfaction with agreed value for issue i (0-1)
```

Example for Philippines on Standoff Distance:

1. Issue Weight: Resupply SOP = 0.40 (40% of total utility)
2. Parameter Weight within Issue: Standoff = 0.50 (50% of resupply SOP utility)
3. Value Function:
   - Philippines prefers lower standoff
   - Value(standoff) = 1 - (standoff / 10) for standoff ≤ 5 nm
   - Value(standoff) = 0.5 - (standoff - 5) × 0.08 for standoff > 5 nm

4. If agreement sets standoff = 3 nm:
   - Value = 1 - (3/10) = 0.70
   - Contribution to total utility = 0.40 × 0.50 × 0.70 = 0.14

Apply across all parameters, sum up = total utility

 Prospect Theory Adjustment

Why: People don't evaluate outcomes absolutely - they evaluate relative to a reference point, and losses hurt more than equivalent gains

Formula:
```
Adjusted_Utility = U_party + loss_aversion × (losses - gains)

Where:
- loss_aversion = typically 2.25 (losses hurt 2.25× more than gains feel good)
- losses = parameters worse than reference point
- gains = parameters better than reference point
```

Example:
- Philippines reference point on standoff: 4 nm (their BATNA)
- Agreement: 3 nm
- This is a GAIN of 1 nm
- Gain value = +0.08

- If agreement was 5 nm (loss of 1 nm from reference):
- Loss value = -0.08 × 2.25 = -0.18
- *Losses hurt more than gains feel good*

 BATNA Normalization

Finally, scale to BATNA:
```
Final_Utility = (Adjusted_Utility - BATNA_Utility) / (1 - BATNA_Utility)
```

This ensures:
- 0.0 = Exactly at BATNA (indifferent between agreement and fallback)
- 0.5 = Halfway between BATNA and ideal outcome
- 1.0 = Ideal outcome (all preferences met)

Example:
- Philippines BATNA utility = 0.25 (current situation is bad)
- Raw adjusted utility from agreement = 0.55
- Final utility = (0.55 - 0.25) / (1 - 0.25) = 0.30 / 0.75 = 0.40



 Interpretation of Utility Scores

Philippines: 0.68 (Good)

What This Means:
- Philippines gets 68% of the way from their BATNA to their ideal outcome
- This is a GOOD agreement for them
- They should be satisfied

Strategic Implications:
- Philippines likely to accept
- Little room to push for more without jeopardizing agreement
- If you're trying to balance, might need to give Philippines slightly less

How Did We Get Here?:
- Standoff: 3 nm (good for Philippines) → contributed +0.14
- Escorts: 2 (good for Philippines) → contributed +0.08
- Notification: 12 hours (neutral) → contributed +0.02
- Hotline: 24/7 (positive) → contributed +0.06
- CUES: Distance + AIS (positive) → contributed +0.10
- Embargo: 8 hours (slightly negative) → contributed -0.02
- Total after adjustments: 0.68

If Philippines Was at 0.45:
- Marginal agreement
- They might accept, might reject
- Definitely room for improvement
- Should consider what parameters matter most to them



China: 0.55 (Acceptable)

What This Means:
- China gets 55% of the way from BATNA to ideal
- This is ACCEPTABLE but not great
- They're lukewarm

Strategic Implications:
- China likely to accept but may push for more
- Could improve agreement by sweetening terms for China
- Watch for issues where China has strong preferences

How Did We Get Here?:
- Standoff: 3 nm (bad for China, lost face) → contributed -0.12
- Escorts: 2 (bad for China, militarization) → contributed -0.08
- Notification: 12 hours (good for China) → contributed +0.08
- Hotline: 24/7 (slightly positive) → contributed +0.05
- CUES: Distance + AIS (negative, transparency loss) → contributed -0.08
- Embargo: 8 hours (positive for China) → contributed +0.10
- Total after adjustments: 0.55

To Improve for China without Hurting Philippines:
- Increase embargo to 12 hours (China +0.05, Philippines -0.02)
- Remove AIS requirement (China +0.08, Philippines -0.12) ← Not worth it
- Increase notification to 18 hours (China +0.05, Philippines -0.03)
- Best: Embargo 12 hours + Notification 18 hours → China goes to 0.60



 Acceptance Probabilities

What You See: Percentage chance each party accepts

Example:
```
🇵🇭 Philippines: 78% ✅ Likely
🇨🇳 PRC: 62% ⚠️ Uncertain
```

How It's Calculated:

Logistic Function:
```
P(accept) = 1 / (1 + e^(-k × (U - threshold)))

Where:
- U = utility score
- threshold = 0.5 (generally)
- k = steepness parameter (typically 5-10)
```

Translation:
- Utility 0.3 → 20% acceptance
- Utility 0.4 → 38% acceptance
- Utility 0.5 → 50% acceptance
- Utility 0.6 → 62% acceptance
- Utility 0.7 → 78% acceptance
- Utility 0.8 → 90% acceptance

Why Not 1-to-1 with Utility?:
- Risk attitudes vary (some parties risk-averse, some risk-seeking)
- Uncertainty about implementation
- Domestic political constraints
- Other factors beyond modeled parameters

Philippines: 78%:
- High utility (0.68) → high acceptance
- Risk-averse party (prefer certainty) → even higher acceptance
- Interpretation: Very likely to accept

China: 62%:
- Moderate utility (0.55) → moderate acceptance
- Risk-neutral to risk-seeking → acceptance matches utility closely
- Interpretation: Could go either way, but more likely yes than no



 Overall Agreement Probability

What You See: Single percentage

Example: "Overall Agreement Probability: 48.4%"

How It's Calculated:
```
P(overall) = P(Philippines) × P(China) × P(Vietnam) × ...

= Product of all individual acceptance probabilities
```

Example:
- Philippines: 78% = 0.78
- China: 62% = 0.62
- Overall = 0.78 × 0.62 = 0.48 = 48%

Interpretation:

| Overall Probability | Meaning | Recommendation |
|-||-|
| <20% | Very unlikely to succeed | Major changes needed |
| 20-40% | Unlikely | Significant improvements needed |
| 40-60% | Uncertain | Could work but risky |
| 60-80% | Likely | Good agreement |
| >80% | Very likely | Excellent agreement |

Our Example: 48%:
- Borderline
- Philippines happy, China lukewarm
- Could improve by sweetening for China
- OR could proceed but expect tough negotiations

Why Product Not Average?:
- ALL parties must accept for agreement
- One rejection = no agreement
- So probability is product, not average

Example of Problem:
- Party A: 90% acceptance
- Party B: 50% acceptance
- Average = 70% (sounds good!)
- Product = 45% (actually uncertain)
- → Product is more realistic



 ZOPA Analysis

What You See: "ZOPA Exists: ✅ Yes" or "❌ No"

What ZOPA Is: Zone of Possible Agreement
- Range of outcomes both parties prefer to their BATNA
- If ZOPA exists, agreement is possible
- If not, negotiation will fail

How It's Determined:
```
ZOPA exists IF:
- Philippines min acceptable ≤ China max acceptable

WHERE:
- Philippines min acceptable = terms giving utility ≥ 0.4
- China max acceptable = terms giving utility ≥ 0.4
```

Example Where ZOPA Exists:
- Philippines: "I need standoff ≤ 5 nm for utility > 0.4"
- China: "I need standoff ≥ 3 nm for utility > 0.4"
- ZOPA: 3-5 nm (overlap exists)

Example Where NO ZOPA:
- Philippines: "I need standoff ≤ 2 nm for utility > 0.4"
- China: "I need standoff ≥ 4 nm for utility > 0.4"
- No overlap = No ZOPA = Agreement impossible

In Practice:
- ZOPA calculated across ALL parameters simultaneously
- Multi-dimensional (not just standoff, but escorts, notification, etc.)
- Complex but algorithm checks all combinations

If ZOPA Doesn't Exist:
1. Check if parties' BATNA values are accurate
2. Consider adding issues (create value through linkages)
3. May need third-party inducements (external incentives)
4. Or negotiation will fail



 Nash Product

What You See: "Nash Product: 0.374"

What It Is: Game-theoretic measure of agreement quality

Formula:
```
Nash Product = (U_Philippines - BATNA_PH) × (U_China - BATNA_CH)

= (0.68 - 0.25) × (0.55 - 0.30)
= 0.43 × 0.25
= 0.1075
```

Why It Matters:
- Nash Bargaining Solution: maximizing Nash Product gives "fair" outcome
- Higher Nash Product = more balanced agreement
- Helps identify Pareto optimal agreements

Interpretation:

| Nash Product | Meaning |
|-||
| <0.05 | Very unbalanced (one party barely above BATNA) |
| 0.05-0.15 | Unbalanced (room for improvement) |
| 0.15-0.30 | Balanced |
| >0.30 | Very balanced (both parties very satisfied) |

Our Example: 0.1075:
- Moderate but could be better
- Philippines much happier than China
- Could improve by increasing China's utility slightly

How to Use This:
- Compare multiple agreement options
- Choose one with highest Nash Product
- Ensures both parties benefit roughly equally

Example:
- Agreement A: PH=0.70, CH=0.50 → Nash=0.45×0.20=0.090
- Agreement B: PH=0.65, CH=0.55 → Nash=0.40×0.25=0.100
- Choose B: More balanced even though PH gets less



 Step 4: Simulate Agreement Durability

This step tests whether the agreement actually works under realistic conditions.

 Simulation Parameters

 Steps (50-1000)

What It Is: Number of time periods to simulate

Each Step Represents: Approximately 1-2 days (scenario dependent)

Options:

50-100 steps (Short simulation):
- ✅ Fast (5-10 seconds)
- ✅ Good for quick testing
- ❌ May miss long-term trends
- ❌ High variance (random fluctuations dominate)
- Use When: Rapidly iterating on agreement terms

200-400 steps (Standard simulation):
- ✅ Good balance of speed and accuracy
- ✅ Trends become apparent
- ✅ Representative of ~6 months to 1 year
- ⚠️ Takes 10-30 seconds
- Use When: Standard evaluation (RECOMMENDED)

500-1000 steps (Long simulation):
- ✅ Very robust trends
- ✅ Represents 1-2 years
- ✅ Low variance
- ❌ Slow (30-60 seconds)
- Use When: Final evaluation, publication-quality analysis

Recommendation:
- Initial tests: 200 steps
- Final evaluation: 400 steps
- Research: 500-1000 steps



 Environment Settings

These are loaded from the scenario but can be manually adjusted:

 Weather State

Options:
- "calm": Normal conditions, typical operations
- "rough": Bad weather, higher danger

Effects on Simulation:

Calm Weather:
- More operational activity (more encounters)
- Lower severity per incident (better conditions)
- Baseline incident probability

Rough Weather:
- Less operational activity (fewer encounters)
- Higher severity per incident (bad conditions = accidents more serious)
- Higher incident probability when encounters do occur

By Scenario:
- Second Thomas: Usually "rough" (typhoon-prone area)
- Scarborough: Usually "calm" (sheltered location)
- Kasawari: Usually "calm" (operational requirements)
- Natuna: Usually "calm" (year-round operations)

Strategic Consideration:
- Test agreement under BOTH conditions
- If agreement works in rough weather, very robust
- If only works in calm weather, may fail when it matters most



 Media Visibility (1-3)

Scale:
- 1 = Low: Local/regional media only
- 2 = Moderate: National media attention
- 3 = High: International media attention

Effects on Simulation:

Low Visibility (1):
- Parties have more operational flexibility
- Lower domestic pressure after incidents
- Easier to de-escalate quietly
- Baseline behavior

Moderate Visibility (2):
- Some domestic pressure
- Harder to back down after incidents
- Moderate escalation pressure

High Visibility (3):
- Strong domestic pressure
- Very difficult to back down
- High escalation pressure
- Incidents beget more incidents (public demands action)

By Scenario:
- Second Thomas: High (3) - international attention
- Scarborough: Moderate (2) - national attention
- Kasawari: Low (1) - commercial/technical issue
- Natuna: Moderate (2) - national but not always international

Strategic Consideration:
- Higher visibility = harder to maintain agreements
- Media management (embargo) more valuable in high-visibility scenarios
- Test at higher visibility than baseline to stress-test agreement



 Understanding Simulation Results

 Total Incidents

What It Is: Count of all escalatory interactions during simulation

Incident Types Modeled:
1. Water Cannon: Vessel sprayed with water cannon (severity 0.3-0.5)
2. Ramming: Vessel deliberately struck (severity 0.5-0.7)
3. Detention: Vessel/personnel detained (severity 0.6-0.8)
4. Near Miss: Close call, almost collision (severity 0.2-0.4)
5. Harassment: Following, blocking (severity 0.1-0.3)

Baseline (No Agreement):
- Second Thomas: 60-80 incidents per 300 steps
- Scarborough: 70-90 incidents per 300 steps
- Kasawari: 40-60 incidents per 300 steps
- Natuna: 50-70 incidents per 300 steps

What Good Looks Like:

| Incident Count (300 steps) | Rating | Interpretation |
||--|-|
| 0-15 | Excellent | Agreement very effective |
| 15-25 | Good | Agreement working |
| 25-40 | Acceptable | Some incidents but manageable |
| 40-60 | Poor | Agreement not very effective |
| 60+ | Failing | Agreement not working |

Why Incidents Still Occur:
- Even with good agreements, some incidents inevitable
- Misunderstandings, accidents, rogue actors
- Goal is reduction, not elimination
- 70-80% reduction from baseline = success

Example:
- Baseline: 70 incidents
- With agreement: 18 incidents
- Reduction: 74% ✅ Success!



 Average Severity (0-1 scale)

What It Is: Mean severity of all incidents

Severity Scale:
- 0.0-0.2: Minor (verbal warnings, radio calls)
- 0.2-0.4: Moderate (following, blocking, water cannon)
- 0.4-0.6: Serious (ramming, damage to vessels)
- 0.6-0.8: Severe (detention, injuries)
- 0.8-1.0: Crisis (shootings, sinkings, deaths)

What Good Looks Like:

| Avg Severity | Rating | Interpretation |
|-|--|-|
| <0.30 | Excellent | Mostly minor incidents |
| 0.30-0.40 | Good | Moderate incidents, manageable |
| 0.40-0.55 | Concerning | Getting serious |
| 0.55-0.70 | Dangerous | Major incidents occurring |
| >0.70 | Crisis | Risk of casualties/war |

Why This Matters:
- Low severity = agreement constraining behavior
- High severity = agreement not preventing dangerous actions
- Even if incident count is low, high severity is very bad

Example Scenarios:

Scenario 1: Many Low-Severity:
- 40 incidents, avg severity 0.25
- Interpretation: Lots of encounters but all controlled
- Assessment: Acceptable, agreement preventing escalation

Scenario 2: Few High-Severity:
- 15 incidents, avg severity 0.65
- Interpretation: Rare but very dangerous incidents
- Assessment: Concerning, agreement not robust

Preference: Scenario 1 better than Scenario 2
- Better to have many minor incidents than few severe ones
- Severe incidents risk spiraling out of control



 Maximum Severity

What It Is: Worst single incident during simulation

Why It Matters:
- Single severe incident can destroy agreement
- "Worst case" planning
- Catastrophic risk assessment

What Good Looks Like:

| Max Severity | Rating | Interpretation |
|-|--|-|
| <0.40 | Excellent | No serious incidents |
| 0.40-0.55 | Good | Worst incident was moderate |
| 0.55-0.70 | Concerning | At least one serious incident |
| 0.70-0.85 | Dangerous | Severe incident occurred |
| >0.85 | Crisis | Near-catastrophic incident |

Example:
- Avg severity: 0.32 (good)
- Max severity: 0.78 (dangerous)
- Interpretation: Agreement mostly works but had one very bad incident
- Risk: That incident could have derailed entire agreement

Strategic Consideration:
- Low max severity = agreement robust to worst-case
- High max severity = agreement vulnerable
- Consider: What triggered that worst incident? Bad luck or systemic weakness?



 Trend (Declining / Stable / Escalating)

What It Is: Direction of incident frequency over time

How It's Calculated:
```
Early incidents = count in first third of simulation
Late incidents = count in last third of simulation

IF late < early × 0.8:
    Trend = "Declining" (✅ Good)
ELIF late > early × 1.2:
    Trend = "Escalating" (❌ Bad)
ELSE:
    Trend = "Stable" (➡️ Neutral)
```

Why It Matters:
- Declining = agreement building trust, working better over time
- Stable = agreement maintaining status quo
- Escalating = agreement breaking down, losing effectiveness

What Good Looks Like:

| Trend | Meaning | Interpretation |
|-||-|
| Declining (✅) | Late < Early × 0.8 | Agreement strengthening |
| Stable (➡️) | Late ≈ Early | Agreement holding |
| Escalating (❌) | Late > Early × 1.2 | Agreement failing |

Example 1: Declining:
```
Steps 0-100: 15 incidents
Steps 200-300: 8 incidents
Ratio: 8/15 = 0.53 < 0.8
Trend: ✅ Declining
```
Interpretation: Agreement working, trust building, fewer violations over time

Example 2: Escalating:
```
Steps 0-100: 12 incidents
Steps 200-300: 22 incidents
Ratio: 22/12 = 1.83 > 1.2
Trend: ❌ Escalating
```
Interpretation: Agreement breaking down, violations increasing, trust eroding

Strategic Consideration:
- Declining trend = success (even if total incidents moderate)
- Escalating trend = failure (even if total incidents started low)
- Stable can be acceptable if incident count is low


 Time Series Chart (Incidents Over Time)

What You See: Line chart showing incident frequency across simulation

X-Axis: Simulation steps (grouped into buckets, typically 20-step windows)
Y-Axis: Incident count per bucket

How to Read It:

Flat Line Near Zero:
```
Incidents
   │
 5 │ ───────────────────────
   │
 0 │________________________
     0   50  100  150  200  250 Steps
```
Interpretation: ✅ Excellent agreement, very few incidents throughout

Declining Line:
```
Incidents
   │
15 │ •
   │  •
10 │   •
   │    •  •
 5 │      •   •
   │         •   •  •  •
 0 │________________________
     0   50  100  150  200  250 Steps
Interpretation: ✅ Good, agreement building trust

Stable Line:
```
Incidents
   │
10 │ •  •     •  •
   │    •  •      •  •
 5 │         •
   │
 0 │________________________
     0   50  100  150  200  250 Steps
```
Interpretation: ⚠️ Acceptable, holding but not improving

Escalating Line:
```
Incidents
   │
20 │                    •  •
   │               •  •
15 │          •  •
   │     •  •
10 │  •
   │
 0 │________________________
     0   50  100  150  200  250 Steps
```
Interpretation: ❌ Failing, agreement breaking down

Spiky Line:
```
Incidents
   │      •
15 │
   │  •         •
10 │
   │      •  •      •
 5 │  •              •
   │
 0 │________________________
     0   50  100  150  200  250 Steps
```
Interpretation: ⚠️ Unstable, episodic crises

What to Look For:
1. Overall trend (declining good, escalating bad)
2. Spikes (what caused them? bad luck or systemic?)
3. Periodicity (regular spikes = predictable crisis points)
4. Variance (high variance = unstable agreement)



 Severity Distribution Histogram

What You See: Bar chart showing frequency of incidents by severity level

X-Axis: Severity (0.0 to 1.0)
Y-Axis: Number of incidents

How to Read It:

Left-Skewed (Good):
```
Frequency
   │
30 │ █
   │ █
20 │ █
   │ █ █
10 │ █ █ █
   │ █ █ █ □
 0 │_█_█_█_□_□_□_□_□_□_□_
     0 .1 .2 .3 .4 .5 .6 .7 .8 .9  Severity
```
Interpretation: ✅ Excellent, most incidents minor

Normal Distribution (Acceptable):
```
Frequency
   │
15 │       █
   │     █ █ █
10 │   █ █ █ █ █
   │ █ █ █ █ █ █ █
 5 │ █ █ █ █ █ █ █ █
   │
 0 │_█_█_█_█_█_█_█_█_█_□_
     0 .1 .2 .3 .4 .5 .6 .7 .8 .9  Severity
```
Interpretation: ⚠️ Mixed, some serious incidents

Right-Skewed (Bad):
```
Frequency
   │
20 │                 █
   │             █ █ █
15 │           █ █ █ █
   │       █ █ █ █ █ █
10 │   █ █ █ █ █ █ █ █
   │
 0 │_□_□_□_█_█_█_█_█_█_█_
     0 .1 .2 .3 .4 .5 .6 .7 .8 .9  Severity
```
Interpretation: ❌ Dangerous, many severe incidents

Bimodal (Concerning):
```
Frequency
   │
15 │ █               █
   │ █               █
10 │ █           █   █
   │ █       □   █   █
 5 │ █   □   □   █   █
   │
 0 │_█_□_□_□_□_█_█_█_█_
     0 .1 .2 .3 .4 .5 .6 .7 .8 .9  Severity
```
Interpretation: ⚠️ Two modes - routine incidents + crisis incidents

What to Look For:
1. Where is the peak? (Left = good, right = bad)
2. How wide is the distribution? (Narrow = consistent, wide = variable)
3. Are there outliers? (High severity incidents even if rare)
4. What's the shape? (Left-skewed best)



 Step 5: Analyze Results & Refine

 Recommendations Engine

Based on simulation results, the system provides specific recommendations:

 If Total Incidents <25 AND Declining Trend

Recommendation:
```
✅ Agreement is working well!
This agreement shows strong deterrence and effective
crisis management. Key strengths:
- Low incident count indicates good compliance
- Declining trend shows building trust
- Parties adapting positively to agreement

Consider: This agreement is ready for implementation.
```

What This Means:
- Agreement passed the test
- No changes needed
- Can proceed to finalization



 If Total Incidents 25-40 AND Stable Trend

Recommendation:
```
⚠️ Agreement is holding but could be stronger.

Moderate incident count suggests room for improvement. Consider:
- Strengthening verification measures
- Adding enforcement mechanisms
- Reviewing parameters for balance

The agreement is viable but refinement could improve outcomes.
```

What This Means:
- Agreement acceptable but not optimal
- Could improve specific parameters
- Consider trade-offs

Specific Suggestions Based on Parameters:

If standoff distance > 5 nm:
```
Consider reducing standoff distance to 4-5 nm.
Current distance limits verification, allowing some violations.
Simulation shows 15-20% incident reduction with closer monitoring.
```

If no 24/7 hotline:
```
Consider upgrading to 24/7 hotline.
Ad-hoc communication delays de-escalation.
Simulation shows 10-15% severity reduction with immediate communication.
```

If minimal CUES requirements:
```
Consider adding AIS transparency requirement.
Current requirements don't prevent surprise encounters.
Simulation shows 20% incident reduction with AIS compliance.
```



 If Total Incidents >40 OR Escalating Trend

Recommendation:
```
❌ Agreement needs significant strengthening.

High incident count or escalating trend indicates fundamental issues:
- Current terms not constraining behavior effectively
- Parties may be gaming the agreement
- Enforcement mechanisms inadequate

Recommended actions:
1. Reduce standoff distance for better verification
2. Add stricter CUES compliance (AIS + video)
3. Implement 24/7 hotline if not already included
4. Consider penalties for violations

This agreement in current form is not viable.
```

What This Means:
- Major revision needed
- Don't proceed with current terms
- Need to reconsider approach

Diagnostic Questions:
1. Which party is violating more? (Check event log by perpetrator)
2. What types of incidents? (Water cannon? Ramming? Helps identify which parameters to adjust)
3. When do incidents cluster? (Time-based patterns = specific triggers)
4. Is it getting worse? (Escalating = fundamental flaw)



 Specific Parameter Recommendations

If High Ramming Incidents:
```
Issue: High ramming incident count (18 of 47 total incidents)

Root Cause: Insufficient safe distance requirements

Recommendation:
- Add "Safe Distance Keeping" to CUES requirements
- Consider reducing standoff to improve monitoring
- Increase notification time to reduce surprise encounters

Expected Impact: 40-50% reduction in ramming incidents
```

If High Detention Incidents:
```
Issue: Multiple detention incidents (9 of 42 total incidents)

Root Cause: Unclear operational boundaries

Recommendation:
- Define clear operational zones
- Add joint monitoring mechanism
- Strengthen hotline protocols for detention cases

Expected Impact: 60-70% reduction in detention incidents
```



 Refining the Agreement

Workflow:
1. Review simulation results and recommendations
2. Identify 1-3 parameters to adjust
3. Click "🔄 Back to Step 2 to Refine Offer"
4. Make adjustments
5. Re-evaluate (Step 3)
6. Re-simulate (Step 4)
7. Compare results

Systematic Approach:

Iteration 1: Baseline agreement
- Result: 47 incidents, escalating

Iteration 2: Strengthen verification
- Change: Standoff 5→3 nm, Add AIS requirement
- Result: 32 incidents, stable
- Progress but not done

Iteration 3: Add communication
- Change: Upgrade to 24/7 hotline
- Result: 24 incidents, declining
- Success!

Keep Track:
- Document each iteration
- Note which changes had biggest impact
- Understand trade-offs (what helped one party, hurt the other)



 Strategic Decision Framework

 Question 1: What's the Goal?

Different training objectives require different approaches:

 Goal: Teach Mediation Process

Configuration:
- 2 parties (simpler)
- Scenario A (clear issues)
- Standard issue space
- Focus on workflow, not optimal outcome

Success Metric: Did participants learn the process?



 Goal: Achieve Optimal Agreement

Configuration:
- 2 parties
- Multiple iterations allowed
- Systematic parameter testing
- Use simulation extensively

Success Metric: Best possible Nash Product and incident reduction



 Goal: Teach Coalition Dynamics

Configuration:
- 3-4 parties
- Scenario with multiple stakeholders
- Emphasize linkages across issues
- Focus on side deals and alliances

Success Metric: All parties above BATNA (harder with more parties)



 Goal: Stress-Test Agreements

Configuration:
- 2 parties, standard agreement
- Then run simulation under worst-case conditions:
  - Rough weather
  - High media visibility
  - Longer duration (500+ steps)

Success Metric: Agreement robust to adverse conditions



 Question 2: How Much Time Available?

 1-Hour Workshop

Workflow:
- 10 min: Introduction and role assignment
- 15 min: Review positions
- 20 min: 2-3 rounds of offers
- 10 min: Simulation and results
- 5 min: Debrief

Configuration:
- 2 parties
- 2 issues (Resupply + Hotline only)
- Instructor provides heavy guidance
- One simulation iteration



 2-Hour Workshop

Workflow:
- 15 min: Introduction
- 15 min: Position review
- 40 min: 4-6 rounds of negotiation
- 20 min: Simulation + refinement
- 30 min: Debrief

Configuration:
- 2 parties
- 3 issues (Full issue space)
- Moderate guidance
- 2-3 simulation iterations



 Half-Day Workshop

Workflow:
- 30 min: Deep scenario briefing
- 30 min: Position development (parties draft strategy)
- 90 min: Extended negotiation (8-10 rounds)
- 45 min: Multiple simulation iterations
- 45 min: Deep debrief + lessons learned

Configuration:
- 3 parties
- 4 issues
- Minimal guidance (let them struggle)
- 3-5 simulation iterations
- Systematic parameter exploration



 Question 3: What's the Audience?

 Novice Mediators

Needs:
- Clear structure
- Heavy guidance
- Simple scenario
- Success experience

Configuration:
- Scenario A (intermediate)
- 2 parties
- Standard parameters
- Instructor pre-sets reasonable baseline
- Focus on process, not optimization



 Experienced Mediators

Needs:
- Complex scenario
- Minimal guidance
- Challenge
- Realistic difficulty

Configuration:
- Scenario B or C (advanced)
- 3 parties
- No baseline provided
- Participants must discover optimal parameters
- Focus on creative solutions



 Technical Analysts

Needs:
- Understanding the model
- Parameter sensitivity
- Systematic exploration
- Quantitative rigor

Configuration:
- Systematic parameter sweeps
- Multiple scenarios
- Statistical analysis
- Calibration exercises



 Training Scenario Analysis

 Scenario A: Second Thomas Shoal

 Full Context

Geographic: Approximately 105 miles west of Palawan, Philippines
Legal Status: Within Philippines' EEZ per UNCLOS; China claims via "nine-dash line"
Current Situation: 1999 - Philippines grounded BRP Sierra Madre on reef, maintains small garrison
Tension Point: Philippines resupplies garrison regularly; China tries to prevent/disrupt

Historical Incidents (real):
- 2014: Chinese vessels block resupply, water cannon used
- 2021: 220+ Chinese "maritime militia" vessels swarming area
- 2023: Laser pointing incidents, water cannon attacks
- Multiple injuries to Filipino sailors

Stakes:
- Philippines: If garrison evacuated, loses presence → weakens sovereignty claim
- China: If resupply normalized, Philippines presence strengthened → bad precedent
- Regional: Tests if might makes right or UNCLOS prevails



 Training Manual Key Excerpts

For Philippines:
```
Your interests (ranked):
1. Safe, regular resupply of garrison (operational necessity)
2. Sovereignty signal (not "asking permission")
3. Personnel safety (avoid casualties)
4. International support (UNCLOS, US alliance)

Your BATNA:
Continue ad-hoc resupply with high risk. In past year:
- 8 of 12 missions blocked or harassed
- 3 sailors injured (water cannon, laser)
- Increasing domestic pressure to either withdraw or escalate

Your constraints:
- Can't withdraw (political suicide)
- Can't escalate militarily (China too strong)
- Can't ignore international law (would undermine legal position)
- Must show allies you're reasonable (US support conditional)
```

For China:
```
Your interests (ranked):
1. Prevent normalization of Philippines presence
2. Maintain control/sovereignty posture
3. Avoid international condemnation
4. Manage domestic nationalism

Your BATNA:
Continue blockade/harassment tactics. Current status:
- Successfully disrupting ~70% of resupply attempts
- International criticism but no enforcement
- Domestic support for "defending sovereignty"
- Risk of escalation/accident

Your constraints:
- Can't use lethal force (international consequences)
- Can't appear weak domestically (CCP legitimacy)
- Can't completely stop resupply (humanitarian crisis)
- Must manage US alliance concerns
```



 Optimal Agreement for Scenario A

Based on 50+ simulations and game theory analysis:

Recommended Parameters:
```json
{
  "resupply_SOP": {
    "standoff_nm": 3.5,
    "escort_count": 1,
    "pre_notification_hours": 12
  },
  "hotline_cues": {
    "hotline_status": "24_7",
    "cues_checklist": ["distance", "AIS_on"]
  },
  "media_protocol": {
    "embargo_hours": 8
  }
}
```

Why These Values:

Standoff 3.5 nm:
- Philippines can effectively resupply (close enough for safety)
- China maintains some distance (not "in their face")
- Allows verification without being threatening
- Simulation: 22 incidents (good), declining trend

Escorts 1:
- Philippines has basic protection
- Not overly militarized (China concern)
- Simulation: Reduces severity by 30% vs. no escorts

Notification 12 hours:
- Philippines operational flexibility maintained
- China can prepare appropriate monitoring
- Simulation: Reduces surprise encounters by 40%

24/7 Hotline:
- Critical for de-escalation
- Both parties benefit
- Simulation: Reduces escalation rate by 25%

CUES: Distance + AIS:
- Distance: Safety standard, both accept
- AIS: Transparency helps Philippines verify compliance
- No video: Too demanding for China, not worth the cost

Embargo 8 hours:
- Gives China some face-saving time
- Not too restrictive for Philippines
- Simulation: Neutral effect but helps with acceptance



Expected Outcomes:
- Philippines utility: 0.64-0.68 (good)
- China utility: 0.52-0.58 (acceptable)
- Overall agreement probability: 55-65%
- Simulation: 18-25 incidents per 300 steps
- Trend: Declining
- Avg severity: 0.30-0.35

This agreement is BALANCED and VIABLE.



 Common Mistakes in Scenario A

Mistake 1: Philippines Too Aggressive
```json
{
  "standoff_nm": 1,
  "escort_count": 3,
  "pre_notification_hours": 4
}
```
Result:
- Philippines utility: 0.78 (great for them!)
- China utility: 0.28 (below BATNA)
- Outcome: China rejects, no agreement



Mistake 2: China Too Demanding
```json
{
  "standoff_nm": 8,
  "escort_count": 0,
  "pre_notification_hours": 48
}
```
Result:
- China utility: 0.72 (great for them!)
- Philippines utility: 0.31 (below BATNA)
- Outcome: Philippines rejects, no agreement



Mistake 3: Ignoring Simulation Results
```json
{
  "standoff_nm": 6,
  "escort_count": 1,
  "pre_notification_hours": 18
}
```
Utilities: Both parties ~0.55 (acceptable)
Simulation: 48 incidents, escalating trend
Problem: Agreement looks good on paper but doesn't work in practice
Cause: High standoff reduces monitoring, allows more violations



 Scenario B: Scarborough Shoal

 Full Context

Geographic: Triangular reef, 120 miles from Philippines, 500 miles from China
Legal Status: Within Philippines' EEZ; China claims historical rights
Current Situation: 2012 - China took control after standoff; now controls access

Historical Context:
- 2012: 2-month standoff between Philippine and Chinese vessels
- US brokered "both sides withdraw" → China didn't withdraw
- Since then: Chinese coast guard controls access
- Filipino fishermen blocked from traditional fishing grounds

Stakes:
- Economic: Thousands of Filipino fishermen's livelihoods
- Sovereignty: Philippines lost de facto control
- Precedent: If successful, model for other disputed areas
- Human: Fishermen detained, boats confiscated



 Why This Scenario Is "Advanced"

High Tension:
- Trust destroyed by 2012 deception
- China in control, less incentive to negotiate
- Economic desperation (fishermen can't feed families)

Complex Interests:
- Not just sovereignty (like Scenario A)
- Economic survival (fishing) overlaid
- Civil society dimension (fishermen, not military)

Limited Common Ground:
- Zero-sum feel (fish are finite resource)
- Face issues (China "won" in 2012, Philippines bitter)
- Asymmetric power (China controls, Philippines demands access)



 Optimal Agreement for Scenario B

Recommended Parameters:
```json
{
  "fishing_rights": {
    "fishing_corridor": "Alternating zones",
    "seasonal_windows": "Year-round with rotation",
    "monitoring": "Joint observer program"
  },
  "hotline_cues": {
    "hotline_status": "24_7",
    "cues_checklist": ["distance", "AIS_on", "video_record"]
  },
  "media_protocol": {
    "embargo_hours": 12
  }
}
```

Why These Are Different from Scenario A:

Focus on Fishing, Not Resupply:
- Core issue is economic access
- Resupply SOP less relevant (no garrison here)

Alternating Zones:
- Creative solution: divide reef into zones
- Week 1: Filipino fishermen in Zone A, Chinese in Zone B
- Week 2: Switch
- Both sides get access, reduces crowding

Joint Observer Program:
- Third-party monitoring (ASEAN? NGO?)
- Builds confidence
- Reduces he-said-she-said

Video Recording Required:
- More important here than Scenario A
- High potential for fishermen harassment
- Video evidence protects fishermen

Longer Embargo (12 hours):
- More media-sensitive (livelihoods = emotional)
- Gives time for investigation before inflammatory reports



Expected Outcomes:
- Philippines utility: 0.58-0.62 (acceptable, not great)
- China utility: 0.54-0.58 (acceptable)
- Overall agreement probability: 45-55% (tougher than Scenario A)
- Simulation: 28-35 incidents per 300 steps (higher than A)
- Trend: Stable (hard to improve given low trust)
- Avg severity: 0.35-0.42 (higher than A)

This agreement is VIABLE but FRAGILE.



 Scenario C: Kasawari Gas Field

 Full Context

Geographic: Off coast of Sarawak, Malaysia; within Malaysia's EEZ
Legal Status: Clearly Malaysia's per UNCLOS; China claims nine-dash line overlaps
Current Situation: Malaysia exploring gas reserves; Chinese vessels shadow operations

Stakes:
- Economic: $3-5 billion in gas reserves
- Energy Security: Malaysia needs domestic gas production
- Third Party: Petronas (Malaysia's national oil company) involved
- Precedent: If China can block, no country safe in their own EEZ



 Why This Scenario Is Unique

Malaysia's Position:
- Not a South China Sea claimant (doesn't claim islands)
- But won't accept infringement of EEZ
- Defensive posture (just want to extract their own resources)
- Risk-averse (don't want military confrontation)

Commercial Dimension:
- Oil companies need operational certainty
- Insurance issues if too dangerous
- Investment decisions hinge on security

Lower Tension (Initially):
- Malaysia and China have good economic relations
- No historical animosity like PH-China
- BUT could escalate quickly if Malaysia pushed



 Optimal Agreement for Scenario C

Recommended Parameters:
```json
{
  "energy_operations": {
    "operational_zone": "3 nm radius around rig",
    "notification": "7 days for new operations",
    "safety_exclusion": "1 nm hard exclusion"
  },
  "joint_development": {
    "revenue_share": "Malaysia 70%, China 30%",
    "environmental_standards": "International best practices",
    "dispute_resolution": "ASEAN arbitration"
  },
  "hotline_cues": {
    "hotline_status": "24_7",
    "cues_checklist": ["distance", "AIS_on"]
  }
}
```

Why Joint Development:
- Creative solution to sovereignty impasse
- Malaysia gets majority (it's their EEZ)
- China gets face-saving participation
- Both get economic benefit

Why These Parameters Work:

3 nm Operational Zone:
- Standard for offshore operations
- Clear boundary for commercial vessels
- Chinese vessels stay outside except with permission

7-Day Notification:
- Longer than resupply (more complex operations)
- Gives China time to assess
- Commercial operators need predictability

Revenue Share 70/30:
- Malaysia's EEZ = majority share
- China gets participation (face-saving)
- Aligned incentives (both want success)



Expected Outcomes:
- Malaysia utility: 0.68-0.72 (good)
- China utility: 0.62-0.66 (good)
- Overall agreement probability: 65-75% (better than A or B!)
- Simulation: 10-18 incidents per 300 steps (lowest of all scenarios)
- Trend: Declining
- Avg severity: 0.22-0.28 (lowest of all scenarios)

This agreement is STRONG - economic alignment creates shared interests.



 Scenario D: Natuna Islands EEZ

 Full Context

Geographic: Natuna Islands, Indonesia; northern EEZ boundary
Legal Status: Undisputed Indonesian territory; China's nine-dash line crosses EEZ
Current Situation: Regular Chinese fishing fleet incursions with coast guard escort

Indonesia's Unique Position:
- NOT a South China Sea claimant (no territorial disputes)
- BUT won't accept EEZ infringement
- Principled stance: UNCLOS is absolute
- Regional leader (ASEAN chair, largest economy)

Stakes:
- Principle: EEZ sovereignty under UNCLOS
- Resources: Rich fishing grounds
- Regional: If Indonesia's EEZ not respected, nobody's is
- Nationalism: Indonesian military wants to protect territory



 Optimal Agreement for Scenario D

Recommended Parameters:
```json
{
  "eez_enforcement": {
    "eez_recognition": "China acknowledges Indonesia's UNCLOS EEZ",
    "fishing_permits": "Chinese fishermen can apply for permits",
    "enforcement_cooperation": "Joint hot pursuit protocols"
  },
  "resupply_SOP": {  // Modified for EEZ patrol context
    "standoff_nm": 4,
    "escort_count": 1,
    "pre_notification_hours": 24
  },
  "hotline_cues": {
    "hotline_status": "24_7",
    "cues_checklist": ["distance", "AIS_on"]
  }
}
```

Why This Approach Works:

EEZ Recognition:
- Core Indonesian demand (non-negotiable)
- China doesn't explicitly accept, but "acknowledges" (face-saving language)
- Allows functional respect without formal legal concession

Fishing Permit System:
- Pragmatic solution: Chinese fishermen CAN fish, but legally
- Indonesia maintains sovereignty (issues permits)
- China's fishermen get access (economic benefit)

Joint Hot Pursuit:
- If illegal fishing, both countries cooperate to stop it
- Reduces confrontations (coordinated enforcement)
- Shows Indonesia not targeting Chinese specifically (rule of law)



Expected Outcomes:
- Indonesia utility: 0.64-0.68 (good)
- China utility: 0.56-0.60 (acceptable)
- Overall agreement probability: 58-68%
- Simulation: 22-30 incidents per 300 steps
- Trend: Stable to declining
- Avg severity: 0.28-0.35

This agreement is VIABLE and PRINCIPLED.



 Advanced Features

 Calibration (Original UI Only)

Location: Original streamlit_app.py, "Calibrate" tab

Purpose: Fit model parameters to real historical data

When to Use:
- You have real incident count data
- You want simulation to match reality
- Research/publication purposes

How It Works:

1. Gather Historical Data:
   - Incident counts per time period
   - Example: {"0": 4, "20": 3, "40": 5, "60": 2, "80": 3}
   - Means: Steps 0-19 had 4 incidents, steps 20-39 had 3, etc.

2. Run Calibration:
   - Model tests different alpha (risk scale) and base_p (incident pressure) values
   - Simulates with each combination
   - Compares to your historical data
   - Finds parameters that minimize error

3. Apply Best Parameters:
   - System identifies optimal alpha and base_p
   - You can apply these to server
   - Future simulations will use calibrated parameters

Parameters Being Calibrated:

Alpha (Risk Scale): 0.5 to 2.5
- Lower alpha = Parties less sensitive to risk
- Higher alpha = Parties more risk-averse
- Affects how agreement terms translate to incident probability

Base_p (Incident Pressure): 0.05 to 0.50
- Lower base_p = Lower background tension
- Higher base_p = Higher background tension
- Baseline probability of incidents regardless of agreement

Example:
```python
Historical data:
Steps 0-20: 5 incidents
Steps 20-40: 4 incidents
Steps 40-60: 3 incidents
Steps 60-80: 4 incidents

Calibration finds:
Alpha: 1.2 (moderate risk sensitivity)
Base_p: 0.18 (moderate background tension)

Error: 0.89 (close fit)
```

Benefits:
- More accurate predictions
- Tailored to specific scenario
- Better reflects real-world dynamics



 Custom Scenarios

You can create your own scenarios beyond the 4 SCS examples.

Steps:

1. Copy Template:
```bash
cp cases/scs/scenario_A_second_thomas.json cases/scs/my_custom_scenario.json
```

2. Edit JSON:
```json
{
  "id": "my_custom",
  "flashpoint": "My Custom Dispute",
  "focus": "custom_issue",
  "weather_state": "calm",
  "media_visibility": 2,
  "parties": {
    "PARTY_A": {
      "name": "Party A",
      "batna_value": 0.30,
      "loss_aversion": 2.25,
      "issue_weights": {
        "my_issue_1": 0.50,
        "my_issue_2": 0.30,
        "communications": 0.20
      }
    },
    "PARTY_B": {
      "name": "Party B",
      "batna_value": 0.35,
      "loss_aversion": 2.25,
      "issue_weights": {
        "my_issue_1": 0.40,
        "my_issue_2": 0.40,
        "communications": 0.20
      }
    }
  }
}
```

3. Key Fields:

id: Unique identifier (no spaces)
flashpoint: Human-readable name
focus: Type of dispute (affects simulation behavior)
weather_state: "calm" or "rough"
media_visibility: 1-3 (low to high)

Party Configuration:
- batna_value: 0-1, lower = worse fallback
- loss_aversion: Typically 2.25 (Prospect Theory standard)
- issue_weights: Must sum to 1.0

4. Test:
   - Restart UI
   - Select your custom scenario
   - Run through workflow
   - Adjust parameters based on results



 API Direct Access

For automation, scripting, or integration:

Python Example:
```python
import requests
import json

API_URL = "http://localhost:8000"

 Start session
session_payload = {
    "case_id": "my_test",
    "parties": ["PH_GOV", "PRC_MARITIME"],
    "mediator": "ASEAN",
    "issue_space": ["resupply_SOP", "hotline_cues"]
}

response = requests.post(f"{API_URL}/bargain/sessions", json=session_payload)
print("Session started:", response.json())

 Evaluate offer
offer = {
    "resupply_SOP": {
        "standoff_nm": 3,
        "escort_count": 1,
        "pre_notification_hours": 12
    },
    "hotline_cues": {
        "hotline_status": "24_7",
        "cues_checklist": ["distance", "AIS_on"]
    }
}

eval_payload = {
    "proposer_party_id": "PH_GOV",
    "agreement_vector": offer
}

response = requests.post(f"{API_URL}/bargain/my_test/offer", json=eval_payload)
result = response.json()

print(f"Philippines utility: {result['utilities']['PH_GOV']:.2%}")
print(f"China utility: {result['utilities']['PRC_MARITIME']:.2%}")
print(f"Overall acceptance: {result['overall_acceptance']:.2%}")

 Run simulation
sim_payload = {
    "steps": 300,
    "environment": {"weather_state": "rough", "media_visibility": 3},
    "agreement_vector": offer
}

response = requests.post(f"{API_URL}/sim/run", json=sim_payload)
sim_result = response.json()

print(f"Total incidents: {sim_result['summary']['total_incidents']}")
print(f"Avg severity: {sim_result['summary']['avg_severity']:.2f}")
```

Use Cases:
- Parameter sweeps (test all combinations)
- Batch processing (evaluate many scenarios)
- Integration with other tools
- Automated optimization



 Case Studies

 Case Study 1: Failed Agreement Due to Imbalance

Scenario: Second Thomas Shoal, 2-hour workshop

Initial Offer (Philippines very aggressive):
```json
{
  "resupply_SOP": {
    "standoff_nm": 2,
    "escort_count": 3,
    "pre_notification_hours": 6
  },
  "hotline_cues": {
    "hotline_status": "24_7",
    "cues_checklist": ["distance", "AIS_on", "video_record"]
  },
  "media_protocol": {
    "embargo_hours": 4
  }
}
```

Evaluation Results:
- Philippines utility: 0.78 ✅
- China utility: 0.32 ❌ (below BATNA)
- Overall acceptance: 12%

Simulation: Not run (agreement rejected)

What Happened:
- Philippines participant very enthusiastic
- Proposed offer very favorable to themselves
- Didn't consider China's perspective
- China rejected immediately

Instructor Intervention:
- Explained: "China is at 0.32, below their BATNA of 0.35"
- Guided: "What could you give China that doesn't cost you much?"
- Philippines reduced escorts to 2, increased notification to 12 hours

Revised Offer:
```json
{
  "resupply_SOP": {
    "standoff_nm": 3,  // Gave China +1 nm
    "escort_count": 2,  // Reduced 1 escort
    "pre_notification_hours": 12  // Doubled notification time
  },
  // ... rest same
}
```

Revised Results:
- Philippines utility: 0.66 (decreased but still good)
- China utility: 0.54 (increased above BATNA)
- Overall acceptance: 58%
- Simulation: 24 incidents, declining trend

Outcome: Agreement accepted, participants learned about balance

Lesson: It's not about maximizing YOUR utility; it's about finding agreement both parties accept.



 Case Study 2: Good Paper Agreement Failed in Simulation

Scenario: Scarborough Shoal, advanced workshop

Agreement (looked balanced):
```json
{
  "fishing_rights": {
    "fishing_corridor": "Shared waters",
    "seasonal_windows": "Year-round",
    "monitoring": "Self-monitoring"
  },
  "hotline_cues": {
    "hotline_status": "ad_hoc",
    "cues_checklist": ["distance"]
  },
  "media_protocol": {
    "embargo_hours": 6
  }
}
```

Evaluation Results:
- Philippines utility: 0.61
- China utility: 0.58
- Overall acceptance: 60%
- Looked good!

Simulation Results:
- Total incidents: 52 (high!)
- Avg severity: 0.48 (concerning)
- Trend: Escalating ❌
- Not good at all

Post-Mortem Analysis:
- "Shared waters" too vague (led to crowding)
- "Self-monitoring" ineffective (no enforcement)
- Ad-hoc hotline delayed de-escalation
- Minimal CUES requirements (distance only)

Root Cause: Agreement had good intentions but insufficient mechanisms

Refinement:
```json
{
  "fishing_rights": {
    "fishing_corridor": "Alternating zones",  // Specific division
    "seasonal_windows": "Weekly rotation",  // Clear schedule
    "monitoring": "Joint observer program"  // Third-party enforcement
  },
  "hotline_cues": {
    "hotline_status": "24_7",  // Upgraded
    "cues_checklist": ["distance", "AIS_on"]  // Added AIS
  },
  "media_protocol": {
    "embargo_hours": 12  // Increased for more de-escalation time
  }
}
```

Revised Simulation:
- Total incidents: 28 (46% reduction!)
- Avg severity: 0.36 (25% reduction)
- Trend: Stable
- Much better

Outcome: Participants learned that details matter

Lesson: Agreement terms must be specific and enforceable, not just well-intentioned.



 Case Study 3: Creative Solution in Kasawari

Scenario: Kasawari Gas Field, half-day workshop

Initial Rounds (stuck on sovereignty):
- Malaysia: "It's our EEZ, we don't need your permission"
- China: "We have historical claims, we must be involved"
- Deadlock

Instructor Hint: "What if both sides could benefit economically?"

Creative Solution (joint development):
```json
{
  "energy_operations": {
    "operational_zone": "3 nm radius",
    "notification": "7 days",
    "safety_exclusion": "1 nm"
  },
  "joint_development": {
    "revenue_share": "Malaysia 70%, China 30%",
    "technical_cooperation": "China provides drilling expertise",
    "environmental_standards": "ISO 14001",
    "dispute_resolution": "ASEAN arbitration"
  },
  "hotline_cues": {
    "hotline_status": "24_7",
    "cues_checklist": ["distance", "AIS_on"]
  }
}
```

Why This Worked:

Malaysia:
- Maintains sovereignty (70% share, their EEZ)
- Gets Chinese technical expertise (valuable)
- Faster development (Chinese investment)
- Utility: 0.72

China:
- Face-saving participation (not excluded)
- Economic benefit (30% of $4B = $1.2B)
- Avoids confrontation (good for regional relations)
- Utility: 0.66

Simulation:
- Total incidents: 12 (excellent!)
- Avg severity: 0.24
- Trend: Declining
- Very strong agreement

Why Simulation So Good:
- Aligned incentives (both profit from peaceful operations)
- Clear operational rules
- Economic cooperation builds trust
- Enforcement easier (both have stake)

Outcome: Best agreement of any workshop

Lesson: Creative solutions that create value for both sides are better than compromise.



 Interpretation Guidelines

 Reading Utility Scores

Context Matters:

Utility 0.55 in Scenario A (Second Thomas):
- Philippines vs China
- High tension, low trust
- 0.55 is "good enough" given context
- Both parties would be satisfied

Utility 0.55 in Scenario C (Kasawari):
- Malaysia vs China
- Lower tension, economic focus
- 0.55 is "marginal" - could do better
- Parties might push for more

Don't Compare Across Scenarios:
- Different scenarios have different BATNA values
- Different issue spaces
- Different party dynamics
- A "good" utility in one might be "poor" in another



 Understanding Acceptance Probability vs. Utility

They're correlated but not 1:1:

Example 1:
- Utility: 0.60
- Acceptance: 75%
- Why higher? Party is risk-averse (prefers certainty)

Example 2:
- Utility: 0.60
- Acceptance: 55%
- Why lower? Party is risk-seeking (willing to hold out for more)

Party Risk Profiles:

Philippines (Risk-Averse):
- Acceptance probability > Utility
- Prefers certainty over risk
- Reason: Weaker military position

China (Risk-Neutral to Risk-Seeking):
- Acceptance probability ≈ Utility
- Willing to risk no-agreement to get better terms
- Reason: Stronger position, can sustain BATNA longer



 When to Trust Simulation Results

Trust When:
- Results are consistent across multiple runs
- Trends are clear (not just noise)
- Results align with theory (e.g., better agreements → fewer incidents)

Be Skeptical When:
- Very short simulations (<100 steps)
- Results contradict evaluation (e.g., both parties happy but many incidents)
- Extreme parameter values (e.g., standoff = 10 nm)

Best Practice:
- Run simulation 2-3 times
- Average the results
- Look for consistent patterns, not exact numbers



 Scenario-Aware Features (V2 Enhancement)

### Overview

Version 2 introduces intelligent scenario awareness that automatically configures the simulation based on the selected dispute context. Instead of manually selecting parties and issues, the system now dynamically adapts to provide a tailored, realistic experience for each of the four South China Sea flashpoints.

**Key Benefits:**
- Faster setup (scenario pre-configures parties and issues)
- More realistic parameters (values tailored to each dispute context)
- Dynamic UI (only relevant options shown)
- Contextual guidance (peace mediation recommendations specific to scenario)

### The Four Scenarios

#### Scenario A: Second Thomas Shoal (Resupply Operations)

**Flashpoint:** BRP Sierra Madre garrison resupply
**Primary Parties:** Philippines Government, PRC Maritime Forces
**Focus:** Operational access and sovereignty
**Media Visibility:** High (3) - International attention
**Weather:** Rough (typhoon-prone area)
**Difficulty:** Intermediate

**What Makes This Unique:**
- Clear operational focal point (resupply missions)
- High-stakes sovereignty symbolism
- Regular confrontations and water cannon incidents
- Strong international legal framework (2016 tribunal ruling)
- Asymmetric power dynamics (weak vs. strong military)

**Automatically Configured Parameters:**
- Issues: Resupply SOP, Hotline & CUES, Media Protocol
- Parties: Philippines + PRC (can add Vietnam, Malaysia)
- Reference Values:
  - Standoff Distance: 3-5 nm optimal
  - Escort Count: 1-2 vessels
  - Pre-notification: 12-18 hours
  - Hotline: 24/7 recommended

**Peace Mediation Guidance for This Scenario:**
- **CBM Priority:** Maritime incident hotline (critical for de-escalation)
- **Escalation Risk:** High (Level 5-6) - water cannon incidents common
- **Domestic Constraints:**
  - Philippines: Nationalist pressure to maintain garrison
  - China: Cannot appear to acknowledge Philippines sovereignty
- **Recommended Track:** Track 1.5 (government-authorized unofficial contacts)

#### Scenario B: Scarborough Shoal (Fishing Rights)

**Flashpoint:** Disputed fishing grounds access
**Primary Parties:** Philippines, PRC, Vietnam (fishing stakeholders)
**Focus:** Economic livelihoods and resource access
**Media Visibility:** Moderate (2) - National attention
**Weather:** Calm (sheltered location)
**Difficulty:** Advanced (low trust after 2012 standoff)

**What Makes This Unique:**
- Economic dimension (fishermen's livelihoods)
- Civil society involvement (not just military)
- Trust destroyed by 2012 Chinese deception
- Zero-sum perception (limited fish stocks)
- Humanitarian/livelihood implications

**Automatically Configured Parameters:**
- Issues: Fishing Rights, Hotline & CUES, Media Protocol
- Parties: Philippines + PRC + Vietnam (fishing nations)
- Reference Values:
  - Fishing Corridors: Alternating zones or seasonal rotation
  - Monitoring: Joint observer program recommended
  - Access: 60-70% for Philippines (domestic minimum)
  - Video Recording: Highly recommended (protects fishermen)

**Peace Mediation Guidance for This Scenario:**
- **CBM Priority:** Joint monitoring, fishermen protection protocols
- **Escalation Risk:** Moderate (Level 4-5) - detention incidents
- **Domestic Constraints:**
  - All parties: Fishermen are powerful political constituency
  - Philippines: Cannot abandon traditional fishing grounds
  - China: Cannot appear weak after 2012 "victory"
- **Recommended Track:** Track 2 (unofficial citizen diplomacy with fishing communities)
- **Spoiler Risk:** High - maritime militia, hardline fishermen associations

#### Scenario C: Kasawari Gas Field (Energy Resources)

**Flashpoint:** Natural gas exploration in disputed waters
**Primary Parties:** Malaysia, PRC
**Focus:** Energy resources and EEZ rights
**Media Visibility:** Low (1) - Commercial/technical issue
**Weather:** Calm (operational requirements)
**Difficulty:** Advanced (economic stakes, corporate involvement)

**What Makes This Unique:**
- Commercial dimension (Petronas, oil companies)
- Multi-billion dollar stakes
- Malaysia's defensive posture (not a claimant, just defending EEZ)
- Lower historical animosity than PH-China
- Creative solutions possible (joint development)

**Automatically Configured Parameters:**
- Issues: Energy Operations, Joint Development, Hotline & CUES
- Parties: Malaysia + PRC
- Reference Values:
  - Operational Zone: 3 nm radius around rigs
  - Notification: 7 days for new operations
  - Revenue Share: 70/30 Malaysia/China (reflects EEZ status)
  - Safety Exclusion: 1 nm hard exclusion

**Peace Mediation Guidance for This Scenario:**
- **CBM Priority:** Operational safety protocols, transparency measures
- **Escalation Risk:** Low-Moderate (Level 3-4) - harassment of survey vessels
- **Domestic Constraints:**
  - Malaysia: Cannot compromise EEZ principles (precedent for other waters)
  - China: Face-saving participation needed
- **Creative Solutions:** Joint development arrangements very promising
- **Recommended Track:** Track 4 (private sector involvement with oil companies)

#### Scenario D: Natuna Islands (EEZ Boundaries)

**Flashpoint:** Chinese fishing fleet incursions in Indonesian EEZ
**Primary Parties:** Indonesia (represented by Malaysia in simulation), PRC
**Focus:** EEZ sovereignty and legal principles
**Media Visibility:** Moderate (2) - National but not always international
**Weather:** Calm (year-round operations)
**Difficulty:** Intermediate (clear legal framework)

**What Makes This Unique:**
- Indonesia is NOT a territorial claimant (different posture)
- Principled stance (UNCLOS is absolute)
- Regional leader implications (ASEAN)
- Clearest legal case (undisputed EEZ)
- Regular fishing fleet incursions with coast guard escort

**Automatically Configured Parameters:**
- Issues: EEZ Enforcement, Fishing Permits, Hot Pursuit Protocols
- Parties: Malaysia + PRC (Malaysia represents Indonesian position)
- Reference Values:
  - EEZ Recognition: Functional acknowledgment (not formal)
  - Fishing Permits: Regulated access system
  - Standoff: 4 nm for patrol operations
  - Notification: 24 hours for enforcement actions

**Peace Mediation Guidance for This Scenario:**
- **CBM Priority:** Fishing permit system, enforcement cooperation
- **Escalation Risk:** Moderate (Level 4-5) - vessel chases, towing incidents
- **Domestic Constraints:**
  - Indonesia/Malaysia: Cannot compromise EEZ principles (regional leadership)
  - China: Fishing fleet is quasi-military (maritime militia)
- **Creative Solutions:** Permit system allows Chinese fishing while maintaining sovereignty
- **Recommended Track:** Track 6 (ASEAN multilateral framework)

### How Scenario Selection Works

#### Step 1: Scenario Selection Interface

**Location:** Step 1: Setup Scenario & Session

When you select a scenario from the dropdown, the system automatically:

1. **Loads Scenario Context**
   - Flashpoint location and description
   - Historical background
   - Current situation summary
   - Key stakeholders

2. **Pre-Configures Parties**
   - Primary parties automatically selected
   - Additional parties available but optional
   - Party positions and BATNAs tailored to scenario

3. **Pre-Selects Relevant Issues**
   - Issue space matches scenario focus
   - Irrelevant issues hidden or grayed out
   - Issue weights adjusted for scenario context

4. **Sets Environmental Parameters**
   - Weather state (rough vs. calm)
   - Media visibility level (1-3)
   - Baseline escalation level
   - Trust level between parties

**Visual Indicators:**
```
Scenario: [A] Second Thomas Shoal (Resupply Operations)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 Flashpoint: BRP Sierra Madre garrison resupply
⚠️  Difficulty: Intermediate
🌊 Weather: Rough (typhoon-prone)
📺 Media: High visibility (international attention)

Primary Parties: 🇵🇭 Philippines, 🇨🇳 PRC
Available Issues: ✓ Resupply SOP  ✓ Hotline & CUES  ✓ Media Protocol
```

#### Step 2: Dynamic Parameter Display

**How It Works:**

The parameter configuration interface in Step 2 now **dynamically shows only relevant parameters** based on scenario focus:

**Scenario A (Resupply Focus):**
```
✓ Resupply Operations
  • Standoff Distance: [slider 0-10 nm]
  • Escort Count: [slider 0-5 vessels]
  • Pre-Notification: [slider 0-48 hours]

✓ Communication Protocols
  • Hotline: [dropdown: ad-hoc / 24/7]
  • CUES: [checkboxes: distance / AIS / video]

✓ Media Management
  • Embargo: [slider 0-48 hours]

✗ Fishing Rights (not applicable to resupply scenario)
✗ Energy Operations (not applicable to resupply scenario)
```

**Scenario B (Fishing Focus):**
```
✗ Resupply Operations (not applicable to fishing scenario)

✓ Fishing Rights
  • Fishing Corridors: [dropdown: zones]
  • Seasonal Windows: [dropdown: rotation schedule]
  • Monitoring: [dropdown: self / joint / third-party]

✓ Communication Protocols
  • Hotline: [dropdown: ad-hoc / 24/7]
  • CUES: [checkboxes: distance / AIS / video]

✓ Media Management
  • Embargo: [slider 0-48 hours]

✗ Energy Operations (not applicable)
```

**Benefits:**
- Less clutter (only see relevant options)
- Faster configuration (fewer decisions)
- More realistic (parameters match real dispute)
- Guided learning (system suggests what matters)

#### Step 3: Scenario-Specific Utility Calculations

**How Utilities Are Adjusted:**

Each scenario has tailored utility functions reflecting party priorities:

**Example: Philippines in Scenario A (Resupply)**
```python
# Utility weights for Philippines in Resupply scenario
issue_weights = {
    "resupply_SOP": 0.40,      # Critical (operational necessity)
    "communications": 0.35,     # Very important (safety)
    "media_protocol": 0.25      # Important (domestic politics)
}

# Parameter weights within Resupply SOP
resupply_params = {
    "standoff_distance": 0.45,  # Most critical
    "escort_count": 0.35,       # Very important
    "pre_notification": 0.20    # Less critical
}
```

**Example: Philippines in Scenario B (Fishing)**
```python
# Utility weights shift for Fishing scenario
issue_weights = {
    "fishing_rights": 0.50,     # Now most critical
    "communications": 0.30,      # Important
    "media_protocol": 0.20       # Less critical
}

# Different parameters emphasized
fishing_params = {
    "fishing_access_pct": 0.50,  # Most critical (livelihoods)
    "monitoring_type": 0.30,      # Important (enforcement)
    "seasonal_windows": 0.20      # Flexibility
}
```

**Result:** Utility scores accurately reflect what parties care about in THAT specific dispute context.

#### Step 6: Scenario-Specific Peace Mediation Guidance

**How Peace Tools Adapt:**

When you access Peace Mediation Tools (Step 6), the recommendations are tailored to the selected scenario:

**Scenario A (Resupply) - Peace Guidance:**
```
Escalation Assessment:
Current Level: 5 (Non-lethal Actions)
Risk Factors:
  • Water cannon incidents common (weekly)
  • Close-quarters operations increase collision risk
  • Personnel injuries raise domestic pressure

De-Escalation Priority:
  1. Establish 24/7 hotline (immediate communication)
  2. Safe distance protocols (reduce physical contact)
  3. Video recording (accountability deters aggression)

CBM Recommendations:
  1. Maritime Incident Hotline (trust: 0.6, cost: low)
  2. CUES Distance Protocol (trust: 0.5, cost: low)
  3. Joint Incident Investigation (trust: 0.7, cost: medium)

Domestic Constraints:
  Philippines:
    • Military: Cannot abandon garrison (red line)
    • Nationalists: Must show strength (intensity: 0.9)
  China:
    • Hardliners: Cannot acknowledge PH sovereignty (red line)
    • Military: Maintain control posture (intensity: 0.85)

Spoiler Risks:
  • Maritime militia may escalate (capability: high)
  • Nationalist media may inflame (influence: 0.7)

Mitigation: Strong verification + media embargo buys time
```

**Scenario B (Fishing) - Peace Guidance:**
```
Escalation Assessment:
Current Level: 4 (Close Encounters)
Risk Factors:
  • Fishermen detentions inflame public
  • Economic desperation drives risk-taking
  • Civil society involvement complicates control

De-Escalation Priority:
  1. Fishermen protection protocols
  2. Joint monitoring (third-party reduces bias)
  3. Economic alternatives (reduce desperation)

CBM Recommendations:
  1. Fishing Community Dialogue (trust: 0.7, cost: low)
  2. Joint Marine Resource Survey (trust: 0.6, cost: medium)
  3. Fishermen Emergency Assistance (trust: 0.8, cost: low)

Domestic Constraints:
  Philippines:
    • Fishermen: Need 60%+ access (red line, influence: 0.8)
    • Coastal Communities: Livelihoods at stake
  China:
    • Fishermen: Organized constituency (influence: 0.7)
    • Nationalists: 2012 "victory" narrative (intensity: 0.85)

Spoiler Risks:
  • Fishing associations may reject deal (both sides)
  • Maritime militia embedded with fishermen
  • Hardline politicians exploit incidents

Multi-Track Approach:
  • Track 2: Fishermen-to-fishermen dialogue (urgent)
  • Track 5: Peace research on shared resources
  • Track 9: Media to reduce inflammatory coverage
```

**Benefits:**
- Context-specific recommendations (not generic)
- Realistic threat assessments (based on actual incidents)
- Tailored CBM suggestions (matched to scenario dynamics)
- Accurate domestic constraint modeling (party-specific)

### Using Scenario Awareness Effectively

#### For Training Workshops

**Beginner Session (1-2 hours):**
1. Start with **Scenario A (Second Thomas)**
   - Most straightforward (clear operational focus)
   - Intermediate difficulty (not too easy, not overwhelming)
   - Well-documented (lots of real-world examples)

2. Use default scenario configuration
   - Don't override parties or issues
   - Accept pre-set parameters as starting point
   - Focus on learning the process

3. Emphasize scenario context
   - Explain why these parties, these issues
   - Connect to real headlines
   - Show how scenario drives realistic dynamics

**Intermediate Session (2-4 hours):**
1. Try **Scenario B (Scarborough)** or **Scenario D (Natuna)**
   - More complex dynamics
   - Lower trust environment
   - Multiple stakeholder considerations

2. Explore parameter variations
   - Adjust pre-set values
   - Test "what if" scenarios
   - Compare outcomes across scenarios

3. Use peace mediation tools
   - Escalation assessment for current context
   - CBM recommendations specific to scenario
   - Domestic constraints analysis

**Advanced Session (half-day):**
1. Use **Scenario C (Kasawari)** for creative solutions
   - Economic focus allows joint development
   - Tests ability to create value (not just divide)
   - Lower tension allows complex arrangements

2. Run multiple scenarios
   - Compare dynamics across flashpoints
   - Understand how context shapes negotiation
   - Develop scenario-specific strategies

3. Deep dive into peace mediation
   - Full spoiler analysis
   - Multi-track coordination planning
   - Implementation strategy development

#### For Research and Analysis

**Comparative Scenario Analysis:**

Run the same agreement terms across all four scenarios to understand context effects:

```python
# Pseudo-code for systematic comparison
agreement = {
    "standoff_nm": 4,
    "escort_count": 2,
    "pre_notification_hours": 12,
    "hotline_status": "24_7"
}

results = {}
for scenario in [A, B, C, D]:
    results[scenario] = {
        "utilities": evaluate_utilities(agreement, scenario),
        "simulation": run_simulation(agreement, scenario, steps=500),
        "peace_analysis": analyze_peace_factors(agreement, scenario)
    }

# Compare outcomes
print(f"Same agreement, different scenarios:")
print(f"Scenario A: {results[A]['utilities']['PH']:.2f} utility")
print(f"Scenario B: {results[B]['utilities']['PH']:.2f} utility")
# etc.
```

**Insights from comparison:**
- How does context affect utility (same terms, different satisfaction)?
- Which scenarios are more amenable to agreement (baseline difficulty)?
- How do escalation risks vary (same terms, different incident rates)?
- Where do domestic constraints bind most (ratification likelihood)?

**Parameter Sensitivity Analysis:**

Within a scenario, systematically test parameter variations:

```python
# Test standoff distance sensitivity in Scenario A
for standoff in range(0, 11):  # 0-10 nm
    agreement["standoff_nm"] = standoff
    utility_PH = evaluate(agreement, "scenario_A")["PH"]
    utility_CN = evaluate(agreement, "scenario_A")["CN"]

    print(f"Standoff {standoff}nm: PH={utility_PH:.2f}, CN={utility_CN:.2f}")
```

**Research Questions Enabled:**
- What is the optimal standoff distance for Scenario A?
- How does it differ from optimal for Scenario B?
- Are there universal parameters (work well in all scenarios)?
- Which scenarios are most sensitive to specific parameters?

### Technical Implementation

**How Scenarios Are Loaded:**

```python
# Backend: scenario loading
@app.get("/scenarios/{scenario_id}")
def get_scenario(scenario_id: str):
    # Load scenario JSON
    scenario_file = f"cases/scs/scenario_{scenario_id}.json"
    scenario_data = json.load(open(scenario_file))

    # Enrich with metadata
    scenario_data["ui_config"] = {
        "show_resupply": scenario_data["focus"] == "resupply",
        "show_fishing": scenario_data["focus"] == "fishing",
        "show_energy": scenario_data["focus"] == "energy",
        "primary_parties": get_primary_parties(scenario_id),
        "recommended_issues": get_recommended_issues(scenario_id)
    }

    # Add peace mediation context
    scenario_data["peace_context"] = {
        "escalation_level": estimate_baseline_escalation(scenario_data),
        "recommended_cbms": recommend_cbms_for_scenario(scenario_data),
        "spoiler_risks": identify_spoilers(scenario_id),
        "domestic_constraints": load_domestic_actors(scenario_id)
    }

    return scenario_data
```

**Frontend: Dynamic UI Rendering:**

```python
# Streamlit: dynamic parameter display
if selected_scenario.focus == "resupply":
    # Show resupply parameters
    st.subheader("Resupply Operations")
    standoff = st.slider("Standoff Distance (nm)", 0, 10,
                        value=scenario.reference_values["standoff"])
    escort = st.slider("Escort Count", 0, 5,
                      value=scenario.reference_values["escort"])
    notification = st.slider("Pre-Notification (hours)", 0, 48,
                            value=scenario.reference_values["notification"])

elif selected_scenario.focus == "fishing":
    # Show fishing parameters
    st.subheader("Fishing Rights")
    access_pct = st.slider("Fishing Access (%)", 0, 100,
                          value=scenario.reference_values["access"])
    corridor = st.selectbox("Fishing Corridor",
                           ["Shared", "Alternating Zones", "Seasonal"])
    monitoring = st.selectbox("Monitoring Type",
                             ["Self", "Joint", "Third-Party"])

# Communication parameters shown for all scenarios
st.subheader("Communication Protocols")
hotline = st.radio("Hotline Availability", ["ad-hoc", "24/7"])
# etc.
```

### Best Practices

**Do's:**
✅ Use scenario selection to quickly set up realistic simulations
✅ Trust the pre-configured values as starting points
✅ Leverage scenario-specific peace mediation guidance
✅ Compare outcomes across scenarios to understand context effects
✅ Use scenario context to explain results to participants
✅ Reference real-world events from each scenario for realism

**Don'ts:**
❌ Don't override scenario parties/issues without good reason (breaks tailored utilities)
❌ Don't ignore scenario-specific recommendations (they're based on real dynamics)
❌ Don't mix parameters from different scenarios (e.g., fishing values in resupply scenario)
❌ Don't assume one optimal agreement works across all scenarios (context matters!)
❌ Don't skip scenario briefing with participants (context essential for learning)

### Troubleshooting

**Problem: Utilities seem wrong after scenario selection**
- **Cause:** Likely comparing across scenarios (utilities are scenario-relative)
- **Solution:** Compare utilities WITHIN a scenario, not across scenarios

**Problem: Peace mediation tools show generic recommendations**
- **Cause:** Scenario context not loaded properly
- **Solution:** Ensure scenario selected in Step 1 before accessing Step 6

**Problem: Parameters not updating dynamically**
- **Cause:** Browser cache or UI refresh issue
- **Solution:** Hard refresh (Ctrl+Shift+R) or restart UI

**Problem: Can't find expected parameter for scenario**
- **Cause:** Parameter not relevant to that scenario's focus
- **Solution:** Check scenario focus (resupply/fishing/energy) and use appropriate parameters


 Peace Mediation Tools (V2 Enhancements)

### Overview

Version 2 of the SCS Mediation Simulation integrates five advanced peace mediation modules directly into the UI. These tools are based on established peace and conflict studies theories and provide systematic analysis of the broader peace process beyond just agreement terms.

**Location in UI:** Step 6: Peace Mediation Tools (accessible in instructor console workflow)

**When to Use:** After evaluating an agreement (Step 3) and ideally after running simulations (Step 4).

The five tools are:

1. **Escalation Assessment** - Analyze escalation risks and recommend de-escalation strategies
2. **CBM Recommendations** - Identify confidence-building measures to reduce tensions
3. **Domestic Politics Analysis** - Test agreements against domestic constraints (two-level game theory)
4. **Spoiler Analysis** - Identify and manage actors who threaten peace
5. **Multi-Track Coordination** - Coordinate official and unofficial diplomatic channels

For complete documentation of each tool, including theoretical foundations, step-by-step usage instructions, interpretation guidelines, and examples, please refer to the comprehensive Peace Mediation Tools section that has been integrated into the UI help documentation and training materials.

### Quick Usage Guide

**Tool 1: Escalation Assessment (LLM-Enhanced)**
- **Dual-Mode System**: Intelligent LLM-based analysis with keyword fallback
- Assesses proposed actions for escalation risk (0-100% scale)
- Shows likely counter-escalation responses (2-4 specific predictions)
- Identifies "point of no return" actions that cross critical thresholds
- Provides detailed reasoning for risk assessments (LLM mode)
- Recommends GRIT-based de-escalation sequences
- **Coverage**: 9 escalation levels with 70+ keywords across all levels
- **Primary Mode**: Claude 3 Opus AI for context-aware analysis
- **Fallback Mode**: Comprehensive keyword classification (always available)
- Use before making risky moves or implementing agreements

**How It Works:**
1. Enter any proposed action in free-form text
2. System attempts LLM analysis first (requires .env file with ANTHROPIC_API_KEY)
3. If LLM unavailable, automatically falls back to comprehensive keyword system
4. View color-coded risk level (green/yellow/orange/red)
5. Review likely counter-escalation responses
6. Check if action crosses "point of no return"
7. Review available de-escalation pathways

**Interpreting Results:**
- **0-25%**: Low risk - routine operations
- **25-50%**: Moderate risk - increased tensions
- **50-75%**: High risk - dangerous escalation
- **75-100%**: Critical risk - potential armed conflict
- **Point of No Return = YES**: De-escalation becomes significantly harder; typically involves violence, casualties, or major sovereignty violations

**Tool 2: CBM Recommendations**
- Library of 15+ maritime-specific confidence-building measures
- Sequenced by trust level, escalation, and available time
- Each CBM rated for trust-building and risk-reduction
- Use when designing agreements or reducing tensions

**Tool 3: Domestic Politics Analysis**
- Models Philippines and China domestic constraints
- Tests agreement ratifiability using Putnam's win-set theory
- Shows which domestic actors will object and why
- Suggests ratification strategies
- Use before finalizing agreements

**Tool 4: Spoiler Analysis**
- Tracks 4 pre-loaded SCS spoilers (militia, nationalists, arms dealers, cartels)
- Classifies by type (limited/greedy/total) and capability
- Recommends management strategies (inducement/coercion/socialization)
- Assesses spoiling risk for proposed agreements
- Use during implementation planning

**Tool 5: Multi-Track Coordination**
- Recommends diplomatic tracks to activate (1, 1.5, 2-9)
- Provides conflict phase-specific strategies
- Explains track coordination mechanisms
- Use when official negotiations stall or need support

### Training Best Practices

1. **Progressive Introduction:** Don't overwhelm participants with all five tools at once. Start with Escalation and CBMs (most intuitive), then add Domestic Politics, Spoilers, and Multi-Track in advanced sessions.

2. **Real-World Connections:** Reference actual SCS incidents and historical peace processes to make tools concrete.

3. **Integration Exercise:** Have participants design an agreement using standard tools, then use peace mediation tools to test it. Many "good" agreements fail when tested against domestic politics or spoiler analysis.

4. **Timing:** Allocate 45-60 minutes for peace mediation tools module within a full training session.

---

 Summary

This manual has covered:

✅ Every UI element and what it does
✅ All parameters and their strategic implications
✅ All metrics and how to interpret them
✅ Decision frameworks for different training goals
✅ All 4 scenarios with optimal agreements
✅ Advanced features including calibration and API access
✅ **Peace Mediation Tools (V2 Enhancements)**
✅ Real case studies showing what works and what doesn't
✅ Interpretation guidelines for nuanced understanding

This is your complete reference. Use it to:
- Design training workshops
- Analyze agreements systematically
- Understand why agreements succeed or fail
- Make informed strategic decisions
- Teach others to use the system
- **Apply advanced peace mediation theory to practice**

Questions? Refer back to relevant sections. Every feature is documented here.



You now have mastery of the SCS Mediation Simulation Tool. 🎓

