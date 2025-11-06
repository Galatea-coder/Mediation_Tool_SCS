# Strategic Levers Integration - Hybrid Approach

## Overview

This document describes how strategic/diplomatic actions integrate with the SCS Mediator simulation using a **Hybrid Approach** that combines:
- **Hard parameters** (numerical sliders)
- **Soft power dimensions** (diplomatic capital, legitimacy, credibility)
- **Strategic actions** (high-level diplomatic moves)

## Architecture

### 1. Core Components

**File**: `src/scs_mediator_sdk/dynamics/strategic_context.py`

```
StrategicContext (0-100 scales):
├── diplomatic_capital (ability to influence)
├── international_legitimacy (int'l support)
├── domestic_support (public backing)
└── credibility (reputation for follow-through)
```

### 2. Strategic Actions Library

Six predefined actions based on academic IR theory:

| Action | Type | Parameter Effects | Strategic Effects | Theory |
|--------|------|-------------------|-------------------|---------|
| **Convene Regional Summit** | Diplomatic | hotline→Dedicated, patrol_coordination→Info sharing | -20 capital, +15 legitimacy | Keohane (1984) institutionalism |
| **Propose Joint Development** | Economic | revenue_split=50, moratorium=12mo | +10 capital, -15 domestic | Deng/Fravel (2008) shelving disputes |
| **Launch Track II Dialogue** | CBM | prenotify=6, patrol=Monthly | +10 domestic, +5 credibility | Diamond & McDonald (1996) |
| **Public Commitment to Peace** | Communication | standoff=7, escort=3 | +25 legitimacy, -10 domestic | Fearon (1994) audience costs |
| **Increase Transparency** | CBM | prenotify=9, hotline→Dedicated | +15 credibility | Osgood (1962) GRIT |
| **Offer Economic Incentives** | Economic | traditional_access=80, revenue=60 | -15 capital, +10 credibility | Tollison & Willett (1979) linkage |

### 3. How Soft Power Affects Outcomes

**Escalation Risk Calculation:**

```python
base_risk = calculate_from_parameters(standoff, escort, etc.)

# Apply strategic context modifiers
if international_legitimacy > 70:
    base_risk *= 0.85  # 15% reduction

if credibility < 40:
    base_risk *= 1.25  # 25% increase (opponent doesn't believe)

if domestic_support < 35:
    base_risk *= 1.30  # 30% increase (forced to hardline)

if diplomatic_capital > 70:
    base_risk *= 0.85  # 15% reduction

final_risk = base_risk * combined_modifiers
```

**Example Scenario:**
```
Turn 1 Parameters:
- standoff=5, escort=6, prenotify=4
- Base escalation risk: 45%

Strategic Context:
- diplomatic_capital: 50
- international_legitimacy: 50
- credibility: 50
- domestic_support: 50
→ Modifier: 1.0 (neutral)
→ Final risk: 45%

Turn 2 - Take "Convene Regional Summit":
- Parameters change: hotline→Dedicated, prenotify→8
- Base risk drops: 45% → 38%

Strategic Context changes:
- diplomatic_capital: 50 → 30 (spent capital)
- international_legitimacy: 50 → 65 (+15)
- credibility: 50 → 60 (+10)
→ Modifier: 0.85 (legitimacy bonus)
→ Final risk: 38% * 0.85 = 32.3%

Total improvement: 45% → 32.3% (28% reduction!)
```

## Integration with Existing Systems

### Escalation Assessment

```python
from dynamics.strategic_context import StrategicContext

# Existing code
base_risk = assess_escalation(standoff, escort, prenotify, ...)

# New enhancement
strategic_modifier = context.get_escalation_modifier()
final_risk = base_risk * strategic_modifier

# Display
st.metric(
    "Escalation Risk",
    f"{final_risk:.1f}%",
    delta=f"{(final_risk - base_risk):.1f}% from strategy"
)
```

### Outcome Quality Analysis

```python
# Existing: Calculate outcome based on parameters
base_quality = calculate_outcome_quality(revenue_split, buffer_zone, ...)

# Enhancement: Sustainability depends on strategic context
if context.domestic_support < 40:
    sustainability_risk = "HIGH - domestic opposition threatens implementation"
elif context.credibility < 50:
    sustainability_risk = "MEDIUM - low credibility may lead to non-compliance"
else:
    sustainability_risk = "LOW - strong position for implementation"
```

### AI Guide Integration

The AI already receives simulation parameters. Now it also knows about strategic actions:

```python
# Updated AI context
sim_params = {
    # Existing numerical parameters
    "standoff": "Distance between vessels (0-10)",
    ...

    # New strategic parameters (passed as descriptions)
    "strategic_actions_available": [
        "Convene Regional Summit (costs 20 capital, gains 15 legitimacy)",
        "Launch Track II Dialogue (low risk, builds domestic support)",
        ...
    ],

    # Current strategic position
    "diplomatic_capital": 65,
    "international_legitimacy": 72,
    "credibility": 58,
    "domestic_support": 45
}
```

**AI Response Example:**
```
Based on Putnam's (1988) two-level game theory, your low domestic support (45/100)
constrains your win-set...

RECOMMENDATION 1: Launch Track II Dialogue
📚 Diamond & McDonald (1996) show unofficial channels reduce risk while building relationships
→ SIMULATION ACTION: Select "Launch Track II Dialogue" button
→ PARAMETER EFFECTS: prenotify=6, patrol_frequency=Monthly
→ STRATEGIC EFFECTS: +10 domestic support, +5 credibility
💡 WHY: Builds domestic coalition without requiring concessions that hardliners oppose

RECOMMENDATION 2: Then Increase Transparency
📚 Osgood's (1962) GRIT theory suggests unilateral initiatives signal peaceful intent
→ SIMULATION ACTION: After gaining domestic support, select "Increase Transparency"
→ PARAMETER EFFECTS: prenotify=9, hotline→Dedicated
→ STRATEGIC EFFECTS: +15 credibility
💡 WHY: High credibility (58→73) will reduce escalation risk by 10% via modifier
```

## Benefits

### 1. Educational Value
- **Shows HOW strategy affects outcomes**: Students see soft power isn't just talk
- **Teaches trade-offs**: Diplomatic capital vs legitimacy, domestic vs international
- **Connects theory to practice**: Every action grounded in IR literature

### 2. Realism
- **Models actual diplomacy**: Not just military parameters
- **Captures constraints**: Low domestic support forces hardline positions
- **Represents uncertainty**: Strategic moves have costs and risks

### 3. Analysis Depth
- **Richer debrief discussions**: "Why did Team A succeed with similar parameters?"
  - Answer: Better strategic positioning (higher credibility enabled de-escalation)
- **Quantifiable soft power**: Can track and compare strategic effectiveness
- **Multi-dimensional outcomes**: Success isn't just avoiding escalation, but building sustainable peace

## Future Enhancements (Phase 2 & 3)

### Phase 2: Probabilistic Outcomes
```python
action.success_probability = 0.7  # Based on context

if random() < success_probability:
    apply_positive_effects()
else:
    # Backfire
    credibility -= 20
    domestic_support -= 15
```

### Phase 3: Delayed Effects & Event Chains
```python
action.delayed_effects = [
    DelayedEffect(
        turns=2,
        effect="regional_support_arrives",
        magnitude=+15 legitimacy
    )
]

# Creates dynamic storylines:
# Turn 1: Convene summit
# Turn 2: Negotiations ongoing
# Turn 3: Summit produces joint statement (+15 legitimacy)
```

## Implementation Status

✅ **Phase 1 (Current)**:
- Strategic context module created
- Six strategic actions defined with academic basis
- Escalation risk modifiers implemented
- Ready for UI integration

⏳ **Next Steps**:
1. Add strategic actions UI to participant view
2. Display strategic context dashboard
3. Integrate with escalation assessment display
4. Update AI guide to recommend strategic actions
5. Add strategic context to analysis/debrief reports

## Academic Foundations

All strategic actions grounded in peer-reviewed IR theory:

- **Nye (2004)**: Soft Power framework
- **Keohane (1984)**: Institutional cooperation
- **Schelling (1966)**: Signaling and commitment
- **Fearon (1994)**: Audience costs
- **Osgood (1962)**: GRIT (Graduated Reciprocation in Tension-reduction)
- **Diamond & McDonald (1996)**: Multi-track diplomacy
- **Fravel (2008)**: China's territorial dispute management
- **Tollison & Willett (1979)**: Issue linkage

## Testing

```bash
# Test strategic context module
python3 -c "
from src.scs_mediator_sdk.dynamics.strategic_context import *

# Create context
ctx = StrategicContext()
print('Initial:', ctx.get_summary())

# Apply action
action = STRATEGIC_ACTIONS_LIBRARY['convene_regional_summit']
ctx.apply_action(action)
print('After summit:', ctx.get_summary())
print('Escalation modifier:', ctx.get_escalation_modifier())
"
```

## References

See `src/scs_mediator_sdk/ai_guide/knowledge_base.py` lines 143-176 for full bibliography.
