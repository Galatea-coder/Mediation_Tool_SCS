"""
Facilitator and Player Guides for South China Sea Negotiation Scenarios

This module provides:
1. Facilitator Guides: Literature-backed explanations for each scenario and proposal option
2. Player Guides: Country-specific strategic considerations

Part of the SCS Mediator SDK v2 - Multiplayer Enhancement
"""

# ============================================================================
# FACILITATOR GUIDES
# ============================================================================

FACILITATOR_GUIDES = {
    'scenario_A': {
        'name': 'Second Thomas Shoal (Resupply)',
        'overview_guide': '''
### Facilitator Guide: Second Thomas Shoal Resupply Scenario

**Scenario Context:**
The BRP Sierra Madre, deliberately grounded in 1999, serves as a Philippine military outpost. Regular resupply missions have become flashpoints for confrontation with Chinese maritime forces. This scenario requires balancing sovereignty assertions with crisis prevention.

**Key Theoretical Framework (Kahn, 1965):**
Herman Kahn's escalation ladder shows this dispute currently sits at **Level 4-5** (Verbal Warnings to Non-lethal Actions). Water cannon use, ramming, and blockade attempts represent dangerous escalation risks.

**Mediation Objective:**
Establish procedural norms that:
- Allow humanitarian resupply (reducing immediate crisis risk)
- Avoid legitimizing territorial claims on either side
- Create communication channels for future incidents
- Demonstrate cooperation possibilities without prejudicing legal positions

**Academic Foundation:**
- **Kahn (1965)**: "On Escalation" - Crisis ladder framework
- **Schelling (1960)**: "The Strategy of Conflict" - Focal points and tacit bargaining
- **Putnam (1988)**: "Diplomacy and Domestic Politics" - Two-level game constraints
- **Fravel (2008)**: "Strong Borders, Secure Nation" - China's compromise patterns
''',
        'parameter_guides': {
            'standoff_nm': {
                'title': 'Standoff Distance (nautical miles)',
                'description': '''
**What This Controls:** Minimum distance Chinese vessels must maintain from resupply operations.

**Theoretical Significance (Schelling, 1960):**
Physical distance serves as a "focal point" - a naturally salient compromise that both sides can coordinate on without explicit negotiation. Larger distances reduce accident risk but may signal Philippine weakness.

**Options Analysis:**

**0-2 nm (Close Proximity):**
- **Pros**: Allows Chinese monitoring, shows goodwill gesture
- **Cons**: High collision risk, intimidation potential, escalation danger
- **Theory**: Fearon (1994) shows close encounters risk "spiral dynamics" - accidental escalation
- **Recommendation**: ⚠️ High risk unless excellent communication

**3-5 nm (Moderate Distance):**
- **Pros**: Reduces accident risk, allows visual monitoring, balances interests
- **Cons**: May be seen as legitimizing Chinese presence
- **Theory**: Schelling (1960) identifies "natural boundaries" as stable focal points
- **Recommendation**: ✅ Good starting point for initial agreement

**6-10 nm (Wide Buffer):**
- **Pros**: Minimizes escalation risk, emphasizes humanitarian nature
- **Cons**: China may reject as "interference" with monitoring
- **Theory**: Kahn (1965) - larger buffers aid de-escalation
- **Recommendation**: ⚠️ May be too ambitious for initial agreement

**Academic Citations:**
- Schelling, Thomas C. (1960). *The Strategy of Conflict*. Harvard University Press.
- Fearon, James D. (1994). "Domestic Political Audiences and the Escalation of International Disputes." *American Political Science Review* 88(3): 577-592.
- Kahn, Herman (1965). *On Escalation: Metaphors and Scenarios*. Praeger.
''',
                'recommendations': [
                    '**Initial Proposal**: Start with 3-5 nm as a moderate compromise',
                    '**Framing**: Emphasize "safety buffer" not "sovereignty zone"',
                    '**Escalation Clause**: Include review mechanism if incidents occur',
                    '**Academic Support**: Cite Schelling\'s focal point theory'
                ]
            },
            'escort_count': {
                'title': 'Maximum Escort Vessels',
                'description': '''
**What This Controls:** Number of Philippine military vessels that may escort resupply ships.

**Theoretical Significance (Jervis, 1978 - Security Dilemma):**
Escort numbers signal either defensive intent (humanitarian protection) or offensive capability (sovereignty assertion). Each side interprets based on worst-case assumptions.

**Options Analysis:**

**0 Escorts:**
- **Pros**: Emphasizes humanitarian mission, reduces China's security concerns
- **Cons**: Leaves resupply vulnerable to harassment, may appear as capitulation domestically
- **Theory**: Putnam (1988) - violates Philippine domestic "win-set" (politically unacceptable)
- **Recommendation**: ❌ Likely unacceptable to Philippines

**1-2 Escorts:**
- **Pros**: Minimal security presence, signals defensive intent
- **Cons**: Limited deterrence against harassment
- **Theory**: Axelrod (1984) - demonstrates cooperation while maintaining reciprocity capability
- **Recommendation**: ✅ Balanced approach

**3-5 Escorts:**
- **Pros**: Strong deterrence, satisfies Philippine military
- **Cons**: Appears offensive, may trigger Chinese counter-deployment
- **Theory**: Jervis (1978) - security dilemma intensifies with ambiguous capabilities
- **Recommendation**: ⚠️ Risk of triggering counter-escalation

**Academic Citations:**
- Jervis, Robert (1978). "Cooperation Under the Security Dilemma." *World Politics* 30(2): 167-214.
- Putnam, Robert D. (1988). "Diplomacy and Domestic Politics: The Logic of Two-Level Games." *International Organization* 42(3): 427-460.
- Axelrod, Robert (1984). *The Evolution of Cooperation*. Basic Books.
''',
                'recommendations': [
                    '**Initial Proposal**: 1-2 escorts as confidence-building measure',
                    '**Framing**: Emphasize "safety escort" not "sovereignty patrol"',
                    '**Reciprocity**: Link to Chinese vessel restraint (Axelrod\'s tit-for-tat)',
                    '**Review Clause**: Allow adjustment if harassment continues'
                ]
            },
            'pre_notification_hours': {
                'title': 'Pre-Notification Period (hours)',
                'description': '''
**What This Controls:** How far in advance Philippines must notify China of resupply missions.

**Theoretical Significance (Osgood, 1962 - GRIT):**
Pre-notification is a classic "confidence-building measure" that reduces uncertainty and accident risk without compromising core interests. Demonstrates transparency and predictability.

**Options Analysis:**

**0-6 Hours (Short Notice):**
- **Pros**: Maintains operational flexibility, reduces opportunity for Chinese interference
- **Cons**: Insufficient time for Chinese force adjustment, accident risk
- **Theory**: Kahn (1965) - insufficient warning time increases crisis risk
- **Recommendation**: ⚠️ Too short for effective coordination

**12-24 Hours (Standard Notice):**
- **Pros**: Balances transparency with flexibility, allows force positioning
- **Cons**: Gives China time to prepare harassment
- **Theory**: Osgood (1962) - graduated steps build confidence without vulnerability
- **Recommendation**: ✅ Standard international practice

**48+ Hours (Extended Notice):**
- **Pros**: Maximum transparency, demonstrates peaceful intent
- **Cons**: Allows extensive Chinese preparation, may enable blockade
- **Theory**: Putnam (1988) - long delays may violate Philippine win-set (garrison needs)
- **Recommendation**: ⚠️ May be exploited by China

**Academic Citations:**
- Osgood, Charles E. (1962). *An Alternative to War or Surrender*. University of Illinois Press.
- Kahn, Herman (1965). *On Escalation: Metaphors and Scenarios*. Praeger.
- Putnam, Robert D. (1988). "Diplomacy and Domestic Politics." *International Organization* 42(3).
''',
                'recommendations': [
                    '**Initial Proposal**: 24 hours as international norm',
                    '**GRIT Application**: Propose unilateral 48-hour notice for first mission as goodwill gesture',
                    '**Emergency Clause**: Allow 6-hour notice for medical emergencies',
                    '**Verification**: Use formal diplomatic channels (demonstrates seriousness)'
                ]
            }
        }
    },
    'scenario_B': {
        'name': 'Scarborough Shoal (Fishing)',
        'overview_guide': '''
### Facilitator Guide: Scarborough Shoal Fishing Scenario

**Scenario Context:**
Scarborough Shoal (Huangyan Island/Panatag Shoal) has been controlled by China since 2012 but remains within the Philippines' EEZ under UNCLOS. Traditional fishing grounds for Filipino fishermen have become inaccessible, creating humanitarian and economic hardship.

**Key Theoretical Framework (Haas, 1980 - Regime Theory):**
Fishing agreements are classic examples of "resource regime" cooperation even amid broader disputes. Both parties benefit from sustainable resource management and avoiding depletion.

**Mediation Objective:**
Create practical fishing arrangement that:
- Restores Filipino access to traditional grounds
- Addresses Chinese control concerns
- Prevents resource depletion (mutual interest)
- Avoids prejudicing sovereignty claims

**Academic Foundation:**
- **Haas (1980)**: Regime theory - cooperation despite conflict
- **Ostrom (1990)**: "Governing the Commons" - resource management
- **Fravel (2008)**: China compromises when economic benefits clear
- **UNCLOS (1982)**: Legal framework for EEZ rights
''',
        'parameter_guides': {
            'daily_quota_kg': {
                'title': 'Daily Catch Quota (per vessel)',
                'description': '''
**What This Controls:** Maximum daily catch allowed per fishing vessel.

**Theoretical Significance (Ostrom, 1990):**
Common-pool resource management requires clear limits to prevent "tragedy of the commons." Quotas must be:
1. Ecologically sustainable
2. Economically viable for fishermen
3. Verifiable/enforceable
4. Perceived as fair by both sides

**Options Analysis:**

**100-500 kg (Low Quota):**
- **Pros**: Ensures sustainability, easy to monitor
- **Cons**: Below subsistence level for Filipino fishermen, politically unacceptable
- **Theory**: Putnam (1988) - violates Philippine domestic win-set
- **Recommendation**: ❌ Too restrictive

**1000-2000 kg (Moderate Quota):**
- **Pros**: Economically viable, sustainable if vessel limits enforced
- **Cons**: Requires monitoring infrastructure
- **Theory**: Ostrom (1990) - moderate limits more likely to be complied with
- **Recommendation**: ✅ Balanced approach

**3000-5000 kg (High Quota):**
- **Pros**: Maximizes economic benefit for fishermen
- **Cons**: Sustainability concerns, encourages over-fishing, difficult to enforce
- **Theory**: Hardin (1968) - high limits lead to resource depletion
- **Recommendation**: ⚠️ Risk of over-exploitation

**Academic Citations:**
- Ostrom, Elinor (1990). *Governing the Commons*. Cambridge University Press.
- Hardin, Garrett (1968). "The Tragedy of the Commons." *Science* 162(3859): 1243-1248.
- Putnam, Robert D. (1988). *International Organization* 42(3).
''',
                'recommendations': [
                    '**Initial Proposal**: 1000-1500 kg as sustainable baseline',
                    '**Scientific Backing**: Cite marine biology studies on reef capacity',
                    '**Adaptive Management**: Include annual quota review based on catch data',
                    '**Verification**: Require catch logs (builds trust, enables adjustment)'
                ]
            },
            'vessel_limit': {
                'title': 'Maximum Fishing Vessels',
                'description': '''
**What This Controls:** Total number of vessels allowed to fish simultaneously.

**Theoretical Significance (Ostrom, 1990):**
Vessel limits are easier to verify than catch quotas (visual observation vs. inspection). Critical for:
- Preventing overcrowding (safety)
- Enabling sustainable harvest
- Practical enforcement

**Options Analysis:**

**1-10 Vessels (Restricted Access):**
- **Pros**: Easy to monitor, minimal ecological impact, simple enforcement
- **Cons**: Benefits too few fishermen, may be politically unacceptable
- **Theory**: Putnam (1988) - small win-set may violate domestic acceptability
- **Recommendation**: ⚠️ May be too restrictive unless rotational system

**10-30 Vessels (Moderate Access):**
- **Pros**: Balances access with sustainability, manageable monitoring
- **Cons**: Requires coordination mechanism (vessel registration/rotation)
- **Theory**: Ostrom (1990) - medium-scale systems need institutional structure
- **Recommendation**: ✅ Workable with proper institutions

**50+ Vessels (Open Access):**
- **Pros**: Maximizes Filipino fishermen access
- **Cons**: Difficult to monitor, over-exploitation risk, safety concerns
- **Theory**: Hardin (1968) - open access leads to tragedy of commons
- **Recommendation**: ❌ Unsustainable without strict catch limits

**Academic Citations:**
- Ostrom, Elinor (1990). *Governing the Commons*. Cambridge University Press.
- Hardin, Garrett (1968). "The Tragedy of the Commons." *Science* 162(3859).
''',
                'recommendations': [
                    '**Initial Proposal**: 15-20 vessels with rotation system',
                    '**Registration**: Require vessel registration with both authorities',
                    '**Verification**: Chinese coast guard monitors numbers, not catches',
                    '**Fairness**: Rotate access among larger pool of registered fishermen'
                ]
            },
            'permitted_gear': {
                'title': 'Permitted Fishing Gear Types',
                'description': '''
**What This Controls:** Types of fishing equipment allowed (nets, lines, traps).

**Theoretical Significance (Ostrom, 1990):**
Gear restrictions serve multiple purposes:
- **Ecological**: Prevent destructive methods (bottom trawling, blast fishing)
- **Safety**: Avoid entanglement hazards
- **Verification**: Easier to inspect gear than catch
- **Cultural**: Respect traditional fishing methods

**Options Analysis:**

**Lines Only (Most Restrictive):**
- **Pros**: Lowest ecological impact, selective harvest, easy verification
- **Cons**: Least productive method, may not match traditional practices
- **Theory**: May violate Putnam's (1988) win-set - economically unviable
- **Recommendation**: ⚠️ Too restrictive unless premium prices available

**Nets + Lines (Moderate):**
- **Pros**: Balances productivity with sustainability, matches traditional methods
- **Cons**: Net size/type regulations needed to prevent overfishing
- **Theory**: Ostrom (1990) - multiple gear types need specific rules
- **Recommendation**: ✅ Practical approach with proper specifications

**All Gear Types (Permissive):**
- **Pros**: Maximum flexibility for fishermen, highest productivity
- **Cons**: Allows destructive methods (blast fishing, cyanide, bottom trawling)
- **Theory**: Leads to ecological damage and resource depletion
- **Recommendation**: ❌ Unsustainable without extensive regulations

**Specific Gear Considerations:**

**Traditional Nets:**
- Allow handline nets and cast nets (low impact)
- Prohibit drift nets and purse seines (high bycatch)
- Specify mesh size (allow juvenile fish escape)

**Hook and Line:**
- Most sustainable method
- Lowest bycatch
- Labor-intensive (limits catch naturally)

**Traps/Pots:**
- Moderate impact if checked regularly
- Risk of "ghost fishing" if lost
- Require size specifications

**Academic Citations:**
- Ostrom, Elinor (1990). *Governing the Commons*. Cambridge University Press.
- Berkes, Fikret (1989). *Common Property Resources*. Belhaven Press.
''',
                'recommendations': [
                    '**Initial Proposal**: Allow nets (with mesh size limits) and lines',
                    '**Prohibited**: Explicitly ban blast fishing, cyanide, bottom trawling',
                    '**Traditional Methods**: Frame as respecting cultural practices',
                    '**Verification**: Gear inspections before entering fishing zone'
                ]
            },
            'zone_radius_nm': {
                'title': 'Fishing Zone Radius (nautical miles)',
                'description': '''
**What This Controls:** Size of designated fishing area around Scarborough Shoal.

**Theoretical Significance (Schelling, 1960):**
Geographic boundaries serve as focal points for coordination. Zone size affects:
- Resource availability (larger = more fish)
- Monitoring difficulty (larger = harder to enforce)
- Sovereignty implications (larger = more Philippine assertion)

**Legal Context (UNCLOS):**
Scarborough Shoal lies within Philippines' 200nm EEZ. However, China maintains effective control since 2012. Zone size signals relative sovereignty claims.

**Options Analysis:**

**1-3 nm (Minimal Zone):**
- **Pros**: Easy to monitor, less sovereignty assertion, acceptable to China
- **Cons**: Insufficient fishing area, minimal economic benefit
- **Theory**: Putnam (1988) - too small may violate Philippine win-set
- **Recommendation**: ⚠️ May be insufficient for viable fishing

**5-12 nm (Moderate Zone):**
- **Pros**: Adequate fishing area, balances interests, manageable monitoring
- **Cons**: Still limited compared to EEZ rights
- **Theory**: Schelling (1960) - 12nm parallels territorial sea (natural focal point)
- **Recommendation**: ✅ Practical compromise

**12-20 nm (Extended Zone):**
- **Pros**: Substantial fishing area, approaches EEZ rights
- **Cons**: China likely to reject as excessive, difficult monitoring
- **Theory**: May exceed Chinese win-set (Putnam, 1988)
- **Recommendation**: ⚠️ Ambitious, may require phased implementation

**Academic Citations:**
- Schelling, Thomas C. (1960). *The Strategy of Conflict*. Harvard University Press.
- Putnam, Robert D. (1988). "Diplomacy and Domestic Politics." *International Organization* 42(3).
- UNCLOS (1982). United Nations Convention on the Law of the Sea.
''',
                'recommendations': [
                    '**Initial Proposal**: 8-12 nm as moderate compromise',
                    '**GRIT Application**: Start smaller, expand if compliance demonstrated',
                    '**Framing**: "Provisional arrangement without prejudice to legal positions"',
                    '**Academic Support**: Cite Osgood (1962) on graduated trust-building'
                ]
            }
        }
    }
}


# ============================================================================
# PLAYER GUIDES
# ============================================================================

PLAYER_GUIDES = {
    'PH_GOV': {
        'name': '🇵🇭 Philippines Government',
        'strategic_overview': '''
## Strategic Guidance for Philippines Representative

### Your Core Interests:
1. **Sovereignty**: Maintain legal claims under UNCLOS and 2016 Arbitral Award
2. **Humanitarian**: Ensure safe resupply to BRP Sierra Madre garrison
3. **Economic**: Protect Filipino fishermen's livelihoods and traditional fishing grounds
4. **Domestic Politics**: Respond to nationalist sentiment while avoiding escalation

### Your Key Constraints (Putnam's Two-Level Game):

**Domestic "Win-Set" (What You Can Accept):**
- **High Public Scrutiny**: 78% of Filipinos view China negatively (Pew 2023)
- **Nationalist Pressure**: Perceived weakness will face political backlash
- **Fishing Communities**: Dependent on access to traditional grounds
- **Military**: Wants stronger sovereignty assertion
- **Congress**: Senate must approve major agreements

**International Level:**
- **Alliance with US**: Provides security guarantee but limits flexibility
- **ASEAN Relations**: Some members align with China economically
- **Legal Victory**: 2016 Arbitral Award provides legitimacy
- **Economic Dependence**: China is largest trading partner ($67B in 2022)

### Strategic Recommendations:

**1. Frame as "Provisional Arrangement" (Schelling, 1960):**
- Any agreement is "without prejudice" to legal sovereignty claims
- Cite 2016 Arbitral Award in preamble (establishes legal position)
- Emphasize humanitarian and practical cooperation, not sovereignty concession

**2. Use Two-Level Game Leverage (Putnam, 1988):**
- Reference domestic political constraints: "I cannot accept X without Congress support"
- Cite nationalist pressure to explain red lines
- Signal that moderate terms help you sell agreement domestically

**3. BATNA (Fisher & Ury, 1981 - Best Alternative to Negotiated Agreement):**
**Your Alternatives if No Agreement:**
- Continue dangerous confrontations at sea (water cannons, ramming)
- Risk escalation to armed conflict
- Filipino fishermen remain blocked from traditional grounds
- BRP Sierra Madre garrison at risk during resupply

**Assessment**: Your BATNA is WEAK. You need an agreement more than China does because:
- Current status quo favors Chinese control
- Each confrontation risks escalation you cannot win militarily
- Fishermen suffering economic hardship
- International support is rhetorical, not material

**Implication**: You should accept moderate compromises to lock in practical improvements, even if less than full sovereignty rights.

**4. Issue Linkage (Sebenius, 1983):**
**Trade-Offs You Can Make:**
- Accept smaller standoff distance → Request guaranteed resupply schedule
- Accept pre-notification requirement → Request no harassment commitment
- Accept vessel limits → Request higher catch quotas per vessel
- Accept Chinese monitoring → Request formal hotline and incident protocol

**5. De-escalation Signaling (Osgood, 1962 - GRIT):**
**Unilateral Gestures You Can Offer:**
- Extended pre-notification (48 hours instead of 24) for first resupply
- Reduce escort vessels for initial missions
- Invite Chinese observers to verify humanitarian cargo
- Propose joint fishery research (build scientific cooperation)

### Specific Scenario Guidance:

#### Second Thomas Shoal (Resupply):

**Your Red Lines (Cannot Concede):**
- ❌ Zero resupply access (garrison must be sustained)
- ❌ Chinese veto over resupply operations
- ❌ Abandonment of BRP Sierra Madre
- ❌ Explicit sovereignty concession

**Your Ideal Outcome:**
- ✅ Regular, predictable resupply schedule
- ✅ Minimal harassment during operations
- ✅ Communication hotline for coordination
- ✅ Incident response protocol

**Realistic Compromise:**
- Accept 3-5nm standoff distance (reduces confrontation risk)
- Accept 24-hour pre-notification (international norm)
- Accept 1-2 escort limit initially (can increase if needed)
- Insist on formal communication channel

**Framing for Domestic Audience:**
"We secured safe, regular resupply to our servicemen while maintaining our legal sovereignty under the 2016 Arbitral Award. This practical arrangement reduces confrontation risk without conceding our territorial rights."

#### Scarborough Shoal (Fishing):

**Your Red Lines:**
- ❌ Permanent exclusion of Filipino fishermen
- ❌ Recognition of Chinese sovereignty
- ❌ Fishing rights dependent on Chinese "permission"

**Your Ideal Outcome:**
- ✅ Restoration of traditional fishing access
- ✅ Economically viable catch quotas
- ✅ Safety for fishermen (no harassment)
- ✅ Co-management framework (implies shared authority)

**Realistic Compromise:**
- Accept vessel limits (15-20 boats) with rotation system
- Accept daily catch quotas (1000-1500 kg/vessel)
- Accept registration requirement (builds cooperation)
- Accept traditional gear only (sustainable harvest)
- Insist on "traditional fishing grounds" language (historical rights)

**Framing for Domestic Audience:**
"We restored access to our fishermen's traditional grounds while ensuring sustainable practices. This arrangement respects their livelihoods without prejudicing our EEZ rights under UNCLOS."

### Negotiation Tactics:

**1. Anchoring (Kahneman & Tversky, 1979):**
- Start with ambitious initial position (wider zones, more vessels)
- Makes your true target appear as reasonable compromise
- Example: Propose 10nm zone, settle for 8nm (your actual target)

**2. Salami Tactics (Schelling, 1966):**
- Accept smaller initial agreement with built-in expansion mechanisms
- "Start with 10 vessels, expand to 20 if successful"
- Each phase locks in gains, builds confidence

**3. Face-Saving for China (Goffman, 1967):**
- Allow China to maintain control appearance (monitoring, registration)
- Frame as "cooperative management" not "Philippine victory"
- Emphasize mutual benefit, not zero-sum

**4. Academic Framing:**
- Cite Osgood (1962) on graduated reciprocation
- Reference Ostrom (1990) on common resource management
- Use neutral academic language to depoliticize

### Warning Signs - When to Walk Away:

**Reject Agreement If:**
- Contains explicit sovereignty concession language
- Gives China veto power over your operations
- Insufficient to meet garrison/fishermen needs
- No enforcement/dispute mechanism
- Violates 2016 Arbitral Award principles

**Remember**: No agreement is better than a bad agreement that undermines legal position or creates dangerous precedent.

### Academic References:
- Putnam, Robert D. (1988). "Diplomacy and Domestic Politics"
- Schelling, Thomas C. (1960). *The Strategy of Conflict*
- Osgood, Charles E. (1962). *An Alternative to War or Surrender*
- Fisher, Roger & Ury, William (1981). *Getting to Yes*
- Fravel, M. Taylor (2008). *Strong Borders, Secure Nation*
''',
        'scenario_tips': {
            'scenario_A': '''
**Philippines - Second Thomas Shoal Tips:**

**Pre-Negotiation Preparation:**
1. Emphasize humanitarian nature of resupply (wounded soldiers, food, water)
2. Document history of Chinese harassment (water cannons, blocking, laser incidents)
3. Prepare domestic political cover: "protecting our servicemen while de-escalating"

**During Negotiation:**
- **Opening Position**: 5nm standoff, 3 escorts, 12-hour notice
- **Target Position**: 3nm standoff, 1-2 escorts, 24-hour notice
- **Fall-Back Position**: 2nm, 1 escort, 24-hour notice with hotline
- **Red Line**: Cannot accept zero escorts or Chinese veto

**Key Talking Points:**
- "These are Filipino servicemen on Philippine territory under the 2016 Arbitral Award"
- "We seek predictable, safe resupply - not confrontation"
- "Humanitarian operations should not be politicized"
- "We're willing to provide transparency through pre-notification"

**Academic Support:**
- Cite Osgood (1962): "Unilateral conciliatory gestures build trust"
- Cite Schelling (1960): "Focal points enable tacit coordination"

**If Stuck:**
- Propose "trial period" - agree to 3 months, then review
- Suggest graduated approach - start restrictive, relax if successful
- Offer symbolic concession (extended notice) for substantive gain (guaranteed access)
            ''',
            'scenario_B': '''
**Philippines - Scarborough Shoal Fishing Tips:**

**Pre-Negotiation Preparation:**
1. Document economic hardship of fishing communities since 2012
2. Emphasize "traditional fishing grounds" (historical rights pre-date Chinese control)
3. Prepare sustainability arguments (scientific studies on reef capacity)

**During Negotiation:**
- **Opening Position**: 15nm zone, 30 vessels, all traditional gear
- **Target Position**: 10nm zone, 20 vessels, nets + lines
- **Fall-Back Position**: 8nm zone, 15 vessels with rotation, lines + limited nets
- **Red Line**: Cannot accept <5nm zone or <10 vessels (economically unviable)

**Key Talking Points:**
- "Filipino fishermen have worked these waters for generations"
- "This is about livelihoods, not sovereignty assertion"
- "Sustainable fishing benefits both sides - prevents resource depletion"
- "Co-management approach respects both parties' interests"

**Academic Support:**
- Cite Ostrom (1990): "Common resource management requires cooperation"
- Cite Fravel (2008): "China compromises when economic interests align"

**Issue Linkage Opportunities:**
- Accept vessel registration → Request no harassment/arbitrary detention
- Accept catch quotas → Request adequate zone size
- Accept gear restrictions → Request higher vessel numbers
- Accept Chinese monitoring → Request joint scientific research

**If Stuck:**
- Propose pilot program: 10 vessels for 6 months, expand if successful
- Suggest seasonal arrangement: Start with one season, extend if productive
- Offer transparency: GPS tracking on vessels, catch logs, joint inspections
            '''
        }
    },
    'PRC_MARITIME': {
        'name': '🇨🇳 China Maritime Forces',
        'strategic_overview': '''
## Strategic Guidance for China Representative

### Your Core Interests:
1. **Sovereignty**: Maintain "indisputable sovereignty" over features within nine-dash line
2. **Strategic Control**: Ensure no permanent foreign military presence in claimed waters
3. **Deterrence**: Prevent "normalization" of Philippine presence that undermines claims
4. **Domestic Politics**: Appear strong on territorial integrity (CCP legitimacy issue)

### Your Key Constraints (Putnam's Two-Level Game):

**Domestic "Win-Set" (What You Can Accept):**
- **Nationalist Pressure**: 80%+ of Chinese public supports strong SCS stance
- **CCP Legitimacy**: Territorial integrity central to Communist Party narrative
- **Military Pressure**: PLA Navy and Coast Guard want assertive posture
- **Historical Narrative**: "Century of humiliation" frames any concession as weakness
- **Internal Politics**: Appearing soft on sovereignty is career-ending

**International Level:**
- **UNCLOS**: Rejected 2016 Arbitral Award but must maintain legal respectability
- **ASEAN**: Cultivating economic ties with Southeast Asian nations
- **US Competition**: Strategic rivalry frames SCS as zero-sum
- **Economic**: Philippines is BRI partner - economic leverage available

### Strategic Recommendations:

**1. Salami Tactics (Schelling, 1966):**
Your strength is maintaining ambiguity while consolidating control incrementally:
- Accept "provisional arrangements" without sovereignty concession language
- Use any agreement to normalize your presence/authority
- Emphasize your "administration" role (monitoring, enforcement, registration)

**2. Use Your BATNA Leverage (Fisher & Ury, 1981):**
**Your Alternatives if No Agreement:**
- Continue current harassment/blockade of Philippine operations
- Maintain effective control without formal agreement
- Use coast guard to enforce de facto exclusion
- Build artificial islands to strengthen claims

**Assessment**: Your BATNA is STRONG. Status quo favors you because:
- You have effective control since 2012 (Scarborough) / since 2013 (Second Thomas)
- You have superior maritime forces (more/larger vessels)
- Philippines cannot remove you militarily
- International criticism is rhetorical, not material

**Implication**: You can demand significant concessions because Philippines needs agreement more than you do. However, excessive demands may trigger Philippines to internationalize dispute or strengthen US alliance.

**3. Two-Level Game Strategy (Putnam, 1988):**
**Tactics to Limit Concessions:**
- Claim domestic constraints: "Nationalist pressure prevents me from accepting X"
- Reference "historical waters" doctrine (creates impression of non-negotiable position)
- Signal that any concession requires maximum Philippine reciprocity

**Strategic Consideration**:
Your domestic win-set appears smaller than it is. CCP has authoritarian control - if leadership decides agreement serves strategic interests, they can manage nationalist backlash. However, appearing weak is genuinely costly politically.

**4. Issue Framing (Schelling, 1960):**
**Frame Agreements as Chinese Strength:**
- Not "concession" but "humanitarian gesture"
- Not "Philippine rights" but "provisional arrangement under Chinese administration"
- Not "shared control" but "orderly management of activities in Chinese waters"

**Domestic Narrative**: "We maintain sovereignty while responsibly managing humanitarian situations and fishery resources in waters under our jurisdiction."

**5. Long-Term Strategic Patience:**
Every year Philippines doesn't remove you strengthens your claim through:
- Adverse possession (continuous control)
- Normalization (international acceptance of status quo)
- Philippine fatigue (economic/military limits)

### Specific Scenario Guidance:

#### Second Thomas Shoal (Resupply):

**Your Strategic Goals:**
1. Prevent reinforcement/repair of BRP Sierra Madre
2. Demonstrate your administrative control
3. Extract maximum concessions for minimal permission
4. Avoid incident that triggers US intervention

**Your Red Lines (Cannot Concede):**
- ❌ Recognition of Philippine sovereignty
- ❌ Permanent/enhanced Philippine garrison
- ❌ Construction materials for ship repair
- ❌ Normalization of large-scale military resupply

**Your Ideal Outcome:**
- ✅ Veto power over resupply (advance approval)
- ✅ Inspection rights (verify "humanitarian only")
- ✅ Minimal Philippine escorts (limits military normalization)
- ✅ Your monitoring = demonstrates administrative control

**Realistic Compromise:**
- Accept humanitarian resupply (food, water, medicine, personnel rotation)
- Require 24-48 hour advance notification (allows you to position forces)
- Demand minimal escorts (1 or none)
- Insist on small standoff distance (2-3nm) so you can monitor
- Prohibit construction materials (prevents ship reinforcement)
- Frame as "provisional humanitarian arrangement in waters under Chinese administration"

**Framing for Domestic Audience:**
"We maintain sovereignty while responsibly managing the humanitarian situation. Philippine activities require our notification and occur under our monitoring. No sovereignty concession."

**Academic Foundation:**
- Fravel (2008): China compromises when:
  1. Security threat is low (small garrison poses no real threat)
  2. Economic/diplomatic benefits clear (reduces US intervention risk)
  3. Compromise doesn't set precedent for other disputes
  4. Domestic framing preserves face

**Application**: You can accept limited resupply if framed as humanitarian gesture demonstrating responsible sovereignty, not recognition of Philippine rights.

#### Scarborough Shoal (Fishing):

**Your Strategic Goals:**
1. Maintain effective control established in 2012
2. Demonstrate administrative authority (registration, monitoring, enforcement)
3. Prevent "joint management" language (implies shared sovereignty)
4. Extract economic leverage from fishing access

**Your Red Lines:**
- ❌ "Traditional fishing grounds" language (implies historical Philippine rights)
- ❌ "Co-management" framework (implies shared authority)
- ❌ Reference to 2016 Arbitral Award or UNCLOS EEZ rights

**Your Ideal Outcome:**
- ✅ Filipino fishing occurs under Chinese "permission"
- ✅ Registration requirement (demonstrates administrative control)
- ✅ Your enforcement = legitimizes authority
- ✅ Strict vessel limits (controllable number)

**Realistic Compromise:**
- Accept limited Filipino fishing access (10-15 vessels initially)
- Require registration with your authorities (demonstrates control)
- Accept traditional gear only (limits productivity, easier monitoring)
- Impose strict catch quotas (shows your regulatory authority)
- Frame as "provisional permission to fish in waters administered by China"

**Framing for Domestic Audience:**
"We maintain sovereignty while allowing limited fishing under our administration and regulation. All vessels must register with Chinese authorities and follow our rules."

**Strategic Leverage - Graduated Implementation:**
- Start with trial period (3-6 months)
- Require demonstrated compliance before expansion
- Retain right to suspend if "violations" occur
- Each renewal reinforces your administrative authority

### Negotiation Tactics:

**1. Start with Maximalist Position:**
- Demand extensive notification (48+ hours)
- Propose minimal Philippine presence (no escorts)
- Request inspection rights
- Then "compromise" to your actual target

**2. Divide and Conquer:**
- Offer better terms if Philippines:
  - Doesn't reference 2016 Arbitral Award
  - Uses neutral sovereignty language
  - Doesn't coordinate with US/allies

**3. Economic Leverage:**
- Remind of $67B trade relationship
- Reference BRI infrastructure projects
- Suggest fishing access could expand with "good relations"

**4. Time Pressure:**
- You control timing - no urgency on your side
- Filipino fishermen/garrison under pressure
- Delay tactics work in your favor

**5. Academic Framing:**
- Cite Grotius (mare liberum) on resource sharing
- Reference Ostrom (1990) on sustainable management
- Use neutral academic language to obscure power dynamics

### Warning Signs - When to Walk Away:

**Reject Agreement If:**
- Contains explicit sovereignty recognition for Philippines
- References 2016 Arbitral Award in operative text
- Uses "co-management" or "joint authority" language
- Allows unrestricted Philippine military presence
- Sets precedent that weakens claims elsewhere (Spratlys, etc.)

**Strategic Consideration**: Walking away maintains status quo which favors you. Only accept agreement if it:
1. Doesn't undermine sovereignty narrative
2. Demonstrates your administrative control
3. Is domestically defensible as "humanitarian gesture from position of strength"

### Advanced Strategy - Normalization through Agreement:

**Key Insight**: Any agreement that requires Philippine compliance with "your" rules gradually normalizes your authority:
- Registration requirements → Administrative control
- Advance notification → Permission framework
- Monitoring → Enforcement authority
- Quotas/regulations → Regulatory sovereignty

**Long-term Goal**: Transition from contested waters to "administered waters where limited Philippine activity occurs under Chinese permission."

### Academic References:
- Fravel, M. Taylor (2008). *Strong Borders, Secure Nation*
- Schelling, Thomas C. (1960). *The Strategy of Conflict*
- Putnam, Robert D. (1988). "Diplomacy and Domestic Politics"
- Hayton, Bill (2014). *The South China Sea: The Struggle for Power in Asia*
- Johnston, Alastair Iain (2003). "Is China a Status Quo Power?" *International Security* 27(4)
''',
        'scenario_tips': {
            'scenario_A': '''
**China - Second Thomas Shoal Tips:**

**Pre-Negotiation Preparation:**
1. Emphasize "indisputable sovereignty" over Ren'ai Reef (your name for Second Thomas)
2. Frame Philippine presence as "illegal occupation" being tolerated temporarily
3. Document any Philippine attempts to reinforce/repair BRP Sierra Madre

**During Negotiation:**
- **Opening Position**: 48hr notice, 0 escorts, 1nm standoff, inspection rights
- **Target Position**: 24hr notice, 1 escort max, 2-3nm standoff, manifest disclosure
- **Fall-Back Position**: 24hr notice, 2 escorts, 3nm standoff, cargo restrictions
- **Red Line**: Cannot accept no notification or unrestricted resupply

**Key Talking Points:**
- "We exercise sovereignty over these waters but show humanitarian flexibility"
- "Advance notification is standard international practice"
- "Minimal escorts demonstrate humanitarian, not military, mission"
- "This is provisional arrangement, not recognition of Philippine claims"

**Academic Support:**
- Cite Fravel (2008): "China compromises when security threat is low"
- Cite Schelling (1960): "Tacit coordination through focal points"

**Negotiation Leverage:**
- Philippines NEEDS resupply (garrison at risk)
- You control access (coast guard blockade capability)
- US unlikely to intervene over humanitarian resupply
- Each delay costs Philippines more than you

**Key Trade-Offs:**
- Accept 3nm standoff → Demand strict cargo restrictions
- Accept 1-2 escorts → Demand 48-hour notification
- Accept regular schedule → Demand inspection/manifest rights
- Accept hotline → Frame as "Philippines reporting to Chinese authorities"

**If Stuck:**
- Propose trial period with strict limits
- Suggest graduated relaxation if Philippines "complies"
- Threaten to withdraw permission if "violations"
            ''',
            'scenario_B': '''
**China - Scarborough Shoal Fishing Tips:**

**Pre-Negotiation Preparation:**
1. Emphasize effective control since 2012 (10+ years)
2. Frame as "orderly fishery management in Chinese waters"
3. Prepare sustainability arguments (prevents over-exploitation)

**During Negotiation:**
- **Opening Position**: 5 vessels, registration required, 5nm zone, inspection rights
- **Target Position**: 10-12 vessels, registration required, 8nm zone, catch quotas
- **Fall-Back Position**: 15 vessels, registration required, 10nm zone, monitoring
- **Red Line**: Cannot accept "co-management" language or >20 vessels initially

**Key Talking Points:**
- "Sustainable fishing requires proper management"
- "Registration ensures orderly operations"
- "We maintain sovereignty while showing economic flexibility"
- "This is provisional fishing permission, not rights recognition"

**Academic Support:**
- Cite Ostrom (1990): "Resource management requires clear rules"
- Cite Hardin (1968): "Tragedy of commons without regulation"

**Negotiation Leverage:**
- Filipino fishermen have been excluded for 10+ years
- You have established control (fait accompli)
- Economic pressure on fishing communities
- Philippines needs agreement more than you do

**Key Trade-Offs:**
- Accept 15-20 vessels → Demand strict registration/quotas
- Accept larger zone (10-12nm) → Demand monitoring rights
- Accept traditional gear → Demand catch reporting
- Accept longer fishing season → Demand compliance enforcement

**Strategic Frame:**
- Every requirement (registration, reporting, quotas) = demonstration of your authority
- Use "provisional fishing permission" language
- Retain right to suspend if "violations"
- Trial period allows you to maintain leverage

**If Stuck:**
- Start with very limited trial (5-10 vessels, 3 months)
- Require demonstrated compliance before expansion
- Use expansion as leverage for broader cooperation
- Frame generosity as Chinese magnanimity, not Philippine rights
            '''
        }
    }
}


def get_facilitator_guide(scenario_id: str, parameter: str = None) -> str:
    """
    Get facilitator guide for a scenario or specific parameter

    Args:
        scenario_id: Scenario identifier (e.g., 'scenario_A')
        parameter: Optional parameter name (e.g., 'standoff_nm')

    Returns:
        Formatted guide text
    """
    if scenario_id not in FACILITATOR_GUIDES:
        return f"No guide available for scenario: {scenario_id}"

    guide = FACILITATOR_GUIDES[scenario_id]

    if parameter is None:
        # Return overview guide
        return guide['overview_guide']

    if parameter not in guide.get('parameter_guides', {}):
        return f"No guide available for parameter: {parameter}"

    param_guide = guide['parameter_guides'][parameter]

    # Format parameter guide
    output = f"### {param_guide['title']}\n\n"
    output += param_guide['description']

    if 'recommendations' in param_guide:
        output += "\n\n**Facilitator Recommendations:**\n"
        for rec in param_guide['recommendations']:
            output += f"\n{rec}"

    return output


def get_player_guide(role: str, scenario_id: str = None) -> str:
    """
    Get player guide for a specific role

    Args:
        role: Player role (e.g., 'PH_GOV', 'PRC_MARITIME')
        scenario_id: Optional scenario-specific tips

    Returns:
        Formatted guide text
    """
    if role not in PLAYER_GUIDES:
        return f"No guide available for role: {role}"

    guide = PLAYER_GUIDES[role]

    output = guide['strategic_overview']

    if scenario_id and scenario_id in guide.get('scenario_tips', {}):
        output += "\n\n---\n\n"
        output += guide['scenario_tips'][scenario_id]

    return output
