# Scenario-Aware UI - Quick Reference Guide

## What Changed?

The UI is now **scenario-aware**: when you select a scenario in Step 1, everything automatically adjusts to match that scenario's context.

---

## The 4 Scenarios

### 🏝️ Scenario A: Second Thomas Shoal (Resupply)
- **Parties**: Philippines + China
- **Focus**: Resupply missions to BRP Sierra Madre
- **Key Issues**: Resupply procedures, hotlines, incident response, naval restrictions
- **Step 2 Shows**: Standoff distance, escort vessels, notification periods
- **CBM Focus**: Hotline establishment, incident reporting, safe passage

### 🎣 Scenario B: Scarborough Shoal (Fishing Rights)
- **Parties**: Philippines + China
- **Focus**: Traditional fishing grounds and access
- **Key Issues**: Fishing rights, access zones, seasonal rules, enforcement
- **Step 2 Shows**: Fishing access %, seasonal closures, joint patrol frequency
- **CBM Focus**: Fisheries cooperation, joint patrols, resource sharing

### ⛽ Scenario C: Kasawari Gas Field (Energy)
- **Parties**: Malaysia + China (+ optional Vietnam)
- **Focus**: Oil and gas exploration rights
- **Key Issues**: Resource extraction, boundaries, joint development, revenue sharing
- **Step 2 Shows**: Exploration zones, joint development, revenue split, moratorium
- **CBM Focus**: Joint development, technical cooperation, revenue mechanisms

### 🌊 Scenario D: Natuna Islands (EEZ Boundaries)
- **Parties**: Malaysia + China (+ optional Vietnam)
- **Focus**: Exclusive Economic Zone disputes
- **Key Issues**: EEZ boundaries, sovereign rights, fishing zones, naval patrols
- **Step 2 Shows**: Delimitation method, buffer zones, patrol coordination
- **CBM Focus**: Boundary clarification, joint patrols, incident prevention

---

## What Automatically Changes?

### ✅ Step 1: Setup
- **Parties**: Pre-selected based on scenario
- **Issues**: Pre-selected based on scenario focus
- **Context Box**: Shows scenario-specific focus area

### ✅ Step 2: Build Offer
- **Parameters**: Only shows relevant sections
  - Scenario A → Resupply parameters
  - Scenario B → Fishing parameters
  - Scenario C → Energy parameters
  - Scenario D → EEZ parameters
- **Scenario Reminder**: Banner at top shows current scenario

### ✅ Step 6: Peace Tools

**Escalation Tab**:
- Shows scenario-specific escalation context
  - Scenario A: "Resupply operations at contested shoal with garrison presence"
  - Scenario B: "Fishing vessel confrontations in contested waters"
  - Scenario C: "Energy exploration activities in overlapping EEZ claims"
  - Scenario D: "Overlapping EEZ claims and patrol activities"

**CBM Tab**:
- Shows priority CBMs for the scenario
  - Scenario A: Hotline, incident reporting, safe passage
  - Scenario B: Fisheries cooperation, joint patrols, resource sharing
  - Scenario C: Joint development, technical cooperation, revenue mechanisms
  - Scenario D: Boundary clarification, joint patrols, incident prevention

**Domestic Politics Tab**:
- Shows only relevant parties
  - Scenario A & B: Philippines, China
  - Scenario C & D: Malaysia, China

---

## Example: Switching from Scenario A to Scenario B

### Before (Scenario A - Resupply):
```
Step 1: Parties = PH_GOV ✓, PRC_MARITIME ✓
        Issues = resupply_SOP ✓, hotline_cues ✓, incident_response ✓

Step 2: Shows → 🚢 Resupply Operations
                 - Standoff Distance
                 - Max Escorts
                 - Pre-Notification

Step 6: CBMs → Hotline Establishment
               Incident Reporting
               Safe Passage Protocol
```

### After (Scenario B - Fishing):
```
Step 1: Parties = PH_GOV ✓, PRC_MARITIME ✓ (same)
        Issues = fishing_rights ✓, access_zones ✓, seasonal_restrictions ✓

Step 2: Shows → 🎣 Fishing & Access Rights
                 - Traditional Access %
                 - Seasonal Closure Days
                 - Joint Patrol Frequency

Step 6: CBMs → Fisheries Cooperation
               Joint Patrols
               Resource Sharing
```

**Notice**: The resupply parameters disappeared and fishing parameters appeared automatically!

---

## Configuration Location

All scenario configurations are defined at the top of `/home/dk/scs_mediator_sdk_v2/src/scs_mediator_sdk/ui/enhanced_multi_view.py` (lines 27-97).

To add a new scenario or modify existing ones, edit the `SCENARIO_CONFIG` dictionary:

```python
SCENARIO_CONFIG = {
    "scenario_A_second_thomas.json": {
        "name": "Second Thomas Shoal (Resupply)",
        "parties": ["PH_GOV", "PRC_MARITIME"],
        "recommended_issues": [...],
        "context": "...",
        "focus_area": "...",
        "cbm_priorities": [...],
        "escalation_context": "..."
    },
    # Add more scenarios here
}
```

---

## Quick Test

1. **Start the app**: `streamlit run src/scs_mediator_sdk/ui/enhanced_multi_view.py`
2. **Select Instructor role**
3. **In Step 1**:
   - Change scenario dropdown between A, B, C, D
   - Watch parties and issues automatically update
4. **Click "Start Session"**
5. **In Step 2**:
   - Notice only relevant parameter sections appear
6. **Jump to Step 6**:
   - Check CBM tab for scenario-specific priorities
   - Check Domestic Politics tab for scenario-specific parties

---

## Key Files Modified

| File | What Changed |
|------|-------------|
| `/src/scs_mediator_sdk/ui/enhanced_multi_view.py` | Added SCENARIO_CONFIG (lines 27-97)<br>Added scenario awareness to Steps 1, 2, and 6<br>Added session state for selected_scenario |

---

## Backward Compatibility

✅ If no scenario is selected, the UI works as before with default values:
- Default parties: PH_GOV, PRC_MARITIME
- Default issues: resupply_SOP, hotline_cues, media_protocol
- All parameter sections remain visible

---

## Summary

**Before**: Generic UI with all options visible for all scenarios

**After**: Smart UI that shows only relevant options based on selected scenario

**Benefit**: Clearer training experience, less confusion, better pedagogical flow
