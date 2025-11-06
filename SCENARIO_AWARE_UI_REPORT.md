# Scenario-Aware UI Implementation Report

## Overview

The SCS Mediator SDK UI has been successfully enhanced to be **scenario-aware**, meaning that when an instructor selects a scenario in Step 1, all subsequent UI elements automatically adjust to match that scenario's specific context, parties, issues, and focus areas.

## 1. Scenario Configuration System

### Location: Lines 24-97 in `enhanced_multi_view.py`

Added a comprehensive `SCENARIO_CONFIG` dictionary that defines all scenario-specific settings:

```python
SCENARIO_CONFIG = {
    "scenario_A_second_thomas.json": {
        "name": "Second Thomas Shoal (Resupply)",
        "parties": ["PH_GOV", "PRC_MARITIME"],
        "recommended_issues": ["resupply_SOP", "hotline_cues", "incident_response", "naval_restrictions"],
        "all_issues": [...],  # Full list of applicable issues
        "context": "Philippine resupply missions to BRP Sierra Madre",
        "focus_area": "Ensuring safe passage for humanitarian resupply missions while managing naval presence",
        "cbm_priorities": ["hotline_establishment", "incident_reporting", "safe_passage_protocol"],
        "escalation_context": "Resupply operations at contested shoal with garrison presence"
    },
    # ... configurations for scenarios B, C, and D
}
```

### Also Added: Issue Display Names (Lines 77-97)

A mapping of technical issue IDs to human-readable names for consistent UI display:

```python
ISSUE_DISPLAY_NAMES = {
    "resupply_SOP": "Resupply Standard Operating Procedures",
    "hotline_cues": "Hotline & CUES Protocols",
    "fishing_rights": "Fishing Rights & Access",
    # ... 16 total issue types
}
```

## 2. Session State Management

### Location: Lines 101-118 in `enhanced_multi_view.py`

Added two new session state variables:

```python
if 'selected_scenario' not in st.session_state:
    st.session_state.selected_scenario = None
if 'scenario_config' not in st.session_state:
    st.session_state.scenario_config = None
```

These store:
- **selected_scenario**: The filename of the selected scenario (e.g., "scenario_A_second_thomas.json")
- **scenario_config**: The full configuration dictionary for quick access throughout the UI

## 3. Step 1: Scenario Selection (Setup)

### Location: Lines 257-381 in `enhanced_multi_view.py`

### What Changed:

#### 3.1 Scenario Selection & Storage
When a scenario is selected, it's immediately stored in session state:

```python
if scenario != "(none)" and scenario != st.session_state.selected_scenario:
    st.session_state.selected_scenario = scenario
    st.session_state.scenario_config = SCENARIO_CONFIG.get(scenario, None)
```

#### 3.2 Scenario Context Display
Shows a visual context box explaining the scenario's focus:

```python
<div style="background-color: #e3f2fd; ...">
    <h4>Scenario Context</h4>
    <p><strong>Focus:</strong> Ensuring safe passage for humanitarian resupply missions...</p>
    <p><strong>Context:</strong> Philippine resupply missions to BRP Sierra Madre</p>
</div>
```

#### 3.3 Dynamic Party Selection
Parties are pre-selected based on the scenario:

- **Scenario A & B**: Philippines + PRC Maritime (default)
- **Scenario C & D**: Malaysia + PRC Maritime (default), with Vietnam as optional

```python
if st.session_state.scenario_config:
    default_parties = st.session_state.scenario_config.get('parties', ["PH_GOV", "PRC_MARITIME"])
    all_parties = default_parties + st.session_state.scenario_config.get('optional_parties', [])
```

The UI shows a helpful caption: "✓ Recommended for this scenario: Philippines, PRC Maritime"

#### 3.4 Dynamic Issue Selection
Issues are pre-selected based on scenario focus:

- **Scenario A**: resupply_SOP, hotline_cues, incident_response, naval_restrictions
- **Scenario B**: fishing_rights, access_zones, seasonal_restrictions, enforcement_protocols
- **Scenario C**: resource_extraction, maritime_boundaries, joint_development, revenue_sharing
- **Scenario D**: eez_boundaries, sovereign_rights, fishing_zones, naval_patrols

```python
default_issues = st.session_state.scenario_config.get('recommended_issues', [...])
all_issues = st.session_state.scenario_config.get('all_issues', default_issues)
```

The UI shows: "✓ Recommended for this scenario: Resupply Standard Operating Procedures, Hotline & CUES Protocols..."

#### 3.5 Issue Storage
When the session starts, selected issues are stored for Step 2:

```python
st.session_state.selected_issues = issue_space  # Store for Step 2
```

## 4. Step 2: Build Agreement Offer

### Location: Lines 383-587 in `enhanced_multi_view.py`

### What Changed:

#### 4.1 Scenario Context Reminder
At the top of Step 2, displays the selected scenario:

```python
<div style="background-color: #fff8e1; ...">
    <p><strong>Scenario:</strong> Second Thomas Shoal (Resupply)</p>
    <p>Ensuring safe passage for humanitarian resupply missions while managing naval presence</p>
</div>
```

#### 4.2 Dynamic Parameter Sections
The UI now shows **only relevant parameter sections** based on selected issues:

**For Scenario A (Second Thomas Shoal - Resupply):**
```python
if has_resupply:  # Shows if resupply_SOP, incident_response, or naval_restrictions selected
    - Standoff Distance slider
    - Maximum Escort Vessels slider
    - Pre-Notification Period slider
```

**For Scenario B (Scarborough Shoal - Fishing):**
```python
if has_fishing:  # Shows if fishing_rights, access_zones, etc. selected
    - Traditional Fishing Access slider (0-100%)
    - Seasonal Closure slider (days/year)
    - Joint Patrol Frequency dropdown
```

**For Scenario C (Kasawari Gas Field - Energy):**
```python
if has_energy:  # Shows if resource_extraction, joint_development, etc. selected
    - Approved Exploration Zones (multi-select)
    - Enable Joint Development checkbox
    - Revenue Split slider (%)
    - Initial Moratorium slider (months)
```

**For Scenario D (Natuna Islands - EEZ):**
```python
if has_eez:  # Shows if eez_boundaries, sovereign_rights, etc. selected
    - Delimitation Method dropdown
    - Provisional Arrangement checkbox
    - Patrol Coordination dropdown
    - Buffer Zone slider (nautical miles)
```

#### 4.3 Intelligent Issue Detection
The system checks which issue categories are relevant:

```python
has_resupply = any(issue in selected_issues for issue in ["resupply_SOP", "incident_response", ...])
has_fishing = any(issue in selected_issues for issue in ["fishing_rights", "access_zones", ...])
has_energy = any(issue in selected_issues for issue in ["resource_extraction", ...])
has_eez = any(issue in selected_issues for issue in ["eez_boundaries", ...])
```

## 5. Step 6: Peace Mediation Tools

### Location: Lines 884-1317 in `enhanced_multi_view.py`

### What Changed:

#### 5.1 Escalation Assessment Tab
Now includes scenario-specific escalation context:

```python
<div style="background-color: #e3f2fd; ...">
    <p><strong>Scenario Context:</strong> Resupply operations at contested shoal with garrison presence</p>
</div>
```

**Examples by Scenario:**
- **Scenario A**: "Resupply operations at contested shoal with garrison presence"
- **Scenario B**: "Fishing vessel confrontations in contested waters"
- **Scenario C**: "Energy exploration activities in overlapping EEZ claims"
- **Scenario D**: "Overlapping EEZ claims and patrol activities"

#### 5.2 CBM Recommendations Tab
Shows scenario-specific priority CBMs:

```python
<div style="background-color: #e8f5e9; ...">
    <p><strong>Priority CBMs for Second Thomas Shoal (Resupply):</strong></p>
    <ul>
        <li>Hotline Establishment</li>
        <li>Incident Reporting</li>
        <li>Safe Passage Protocol</li>
    </ul>
</div>
```

**CBM Priorities by Scenario:**
- **Scenario A**: hotline_establishment, incident_reporting, safe_passage_protocol
- **Scenario B**: fisheries_cooperation, joint_patrols, resource_sharing
- **Scenario C**: joint_development, technical_cooperation, revenue_mechanisms
- **Scenario D**: boundary_clarification, joint_patrols, incident_prevention

#### 5.3 Domestic Politics Tab
Shows only parties relevant to the selected scenario:

```python
<div style="background-color: #fff8e1; ...">
    <p><strong>Parties in this scenario:</strong> PH GOV, PRC MARITIME</p>
</div>
```

The party selection dropdown is dynamically populated:
- **Scenario A & B**: Philippines, China
- **Scenario C & D**: Malaysia, China (Vietnam if included)

## 6. How It All Works Together

### Example Flow for Scenario A (Second Thomas Shoal):

```
STEP 1: INSTRUCTOR SELECTS SCENARIO
┌─────────────────────────────────────────────────────────────┐
│ 1. Instructor selects "Scenario A: Second Thomas Shoal"    │
│ 2. UI stores: selected_scenario = "scenario_A_second..."   │
│ 3. UI loads: scenario_config = SCENARIO_CONFIG[...]        │
│ 4. UI displays scenario context box                        │
│ 5. Parties pre-populated: PH_GOV ✓, PRC_MARITIME ✓        │
│ 6. Issues pre-populated: resupply_SOP ✓, hotline_cues ✓   │
│ 7. Instructor clicks "Start Session"                       │
│ 8. Selected issues stored in session state                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
STEP 2: BUILD AGREEMENT OFFER
┌─────────────────────────────────────────────────────────────┐
│ 1. UI shows: "Scenario: Second Thomas Shoal (Resupply)"    │
│ 2. UI detects has_resupply = True (from selected issues)   │
│ 3. UI shows Resupply Operations section:                   │
│    - Standoff Distance slider                              │
│    - Maximum Escort Vessels slider                         │
│    - Pre-Notification Period slider                        │
│ 4. UI detects has_communication = True                     │
│ 5. UI shows Communication Protocols section                │
│ 6. Other sections (fishing, energy, EEZ) hidden            │
└─────────────────────────────────────────────────────────────┘
                            ↓
STEP 6: PEACE MEDIATION TOOLS
┌─────────────────────────────────────────────────────────────┐
│ ESCALATION TAB:                                             │
│ - Shows: "Scenario Context: Resupply operations at         │
│           contested shoal with garrison presence"           │
│                                                             │
│ CBM TAB:                                                    │
│ - Shows: "Priority CBMs: Hotline Establishment,            │
│           Incident Reporting, Safe Passage Protocol"        │
│                                                             │
│ DOMESTIC POLITICS TAB:                                      │
│ - Shows: "Parties in this scenario: PH GOV, PRC MARITIME"  │
│ - Dropdown options: Philippines, China only                │
└─────────────────────────────────────────────────────────────┘
```

### Example Flow for Scenario B (Scarborough Shoal):

```
STEP 1: DIFFERENT SCENARIO SELECTED
┌─────────────────────────────────────────────────────────────┐
│ Instructor selects "Scenario B: Scarborough Shoal"         │
│ Parties pre-populated: PH_GOV ✓, PRC_MARITIME ✓           │
│ Issues pre-populated: fishing_rights ✓, access_zones ✓     │
│                       seasonal_restrictions ✓               │
└─────────────────────────────────────────────────────────────┘
                            ↓
STEP 2: DIFFERENT PARAMETERS SHOWN
┌─────────────────────────────────────────────────────────────┐
│ UI shows: "Scenario: Scarborough Shoal (Fishing Rights)"   │
│ UI detects has_fishing = True                              │
│ UI shows Fishing & Access Rights section:                  │
│ - Traditional Fishing Access slider (0-100%)               │
│ - Seasonal Closure slider (days/year)                      │
│ - Joint Patrol Frequency dropdown                          │
│ Resupply section hidden (not relevant)                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
STEP 6: FISHING-FOCUSED TOOLS
┌─────────────────────────────────────────────────────────────┐
│ ESCALATION TAB:                                             │
│ - Shows: "Fishing vessel confrontations in contested        │
│           waters"                                           │
│                                                             │
│ CBM TAB:                                                    │
│ - Shows: "Priority CBMs: Fisheries Cooperation,            │
│           Joint Patrols, Resource Sharing"                  │
└─────────────────────────────────────────────────────────────┘
```

### Example Flow for Scenario C (Kasawari Gas Field):

```
STEP 1: ENERGY SCENARIO
┌─────────────────────────────────────────────────────────────┐
│ Instructor selects "Scenario C: Kasawari Gas Field"        │
│ Parties pre-populated: MY_CG ✓, PRC_MARITIME ✓            │
│ Optional: VN_CG available                                  │
│ Issues pre-populated: resource_extraction ✓,               │
│                       maritime_boundaries ✓,               │
│                       joint_development ✓,                 │
│                       revenue_sharing ✓                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
STEP 2: ENERGY PARAMETERS
┌─────────────────────────────────────────────────────────────┐
│ UI shows: "Scenario: Kasawari Gas Field (Energy)"          │
│ UI detects has_energy = True                               │
│ UI shows Energy & Resource Rights section:                 │
│ - Approved Exploration Zones (multi-select)                │
│ - Enable Joint Development checkbox                        │
│ - Revenue Split slider (%)                                 │
│ - Initial Moratorium slider (months)                       │
│ Resupply and fishing sections hidden                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
STEP 6: ENERGY-FOCUSED TOOLS
┌─────────────────────────────────────────────────────────────┐
│ ESCALATION TAB:                                             │
│ - Shows: "Energy exploration activities in overlapping      │
│           EEZ claims"                                       │
│                                                             │
│ CBM TAB:                                                    │
│ - Shows: "Priority CBMs: Joint Development,                │
│           Technical Cooperation, Revenue Mechanisms"        │
│                                                             │
│ DOMESTIC POLITICS TAB:                                      │
│ - Shows: "Parties: MY CG, PRC MARITIME"                    │
│ - Dropdown options: Malaysia, China                        │
└─────────────────────────────────────────────────────────────┘
```

## 7. Key Benefits

### 7.1 Contextual Relevance
Every part of the UI now reflects the specific scenario being trained:
- **Parties**: Only relevant countries are suggested
- **Issues**: Only relevant negotiation topics are pre-selected
- **Parameters**: Only relevant agreement terms are shown
- **Peace Tools**: CBMs and analysis reflect scenario focus

### 7.2 Reduced Cognitive Load
Instructors and participants don't see irrelevant options:
- Fishing parameters hidden in resupply scenarios
- Energy parameters hidden in fishing scenarios
- Domestic politics analysis limited to relevant parties

### 7.3 Pedagogical Clarity
Each scenario has clear context explanations:
- Visual context boxes explain the scenario focus
- Priority CBMs guide peace-building efforts
- Escalation contexts frame risk assessments

### 7.4 Backward Compatibility
The system remains functional even without scenario selection:
- Falls back to default parties (PH_GOV, PRC_MARITIME)
- Shows common issues (resupply_SOP, hotline_cues, media_protocol)
- All parameters remain accessible

## 8. Configuration Details

### Scenario A: Second Thomas Shoal (Resupply)

**Primary Parties**: Philippines (PH_GOV), China (PRC_MARITIME)
**Key Issues**: resupply_SOP, hotline_cues, incident_response, naval_restrictions
**Focus**: Philippine resupply missions to BRP Sierra Madre
**CBM Priorities**: Hotline establishment, incident reporting, safe passage protocol
**Escalation Context**: Resupply operations at contested shoal with garrison presence

**UI Behavior**:
- Shows resupply operation parameters (standoff distance, escorts, notification)
- Shows communication protocol parameters (hotline, CUES compliance)
- Shows media management parameters
- Hides fishing, energy, and EEZ parameters

### Scenario B: Scarborough Shoal (Fishing Rights)

**Primary Parties**: Philippines (PH_GOV), China (PRC_MARITIME)
**Key Issues**: fishing_rights, access_zones, seasonal_restrictions, enforcement_protocols
**Focus**: Traditional fishing grounds and access
**CBM Priorities**: Fisheries cooperation, joint patrols, resource sharing
**Escalation Context**: Fishing vessel confrontations in contested waters

**UI Behavior**:
- Shows fishing rights parameters (access %, seasonal closures, patrols)
- Shows communication protocol parameters
- Shows media management parameters
- Hides resupply, energy, and EEZ parameters

### Scenario C: Kasawari Gas Field (Energy)

**Primary Parties**: Malaysia (MY_CG), China (PRC_MARITIME)
**Optional Parties**: Vietnam (VN_CG)
**Key Issues**: resource_extraction, maritime_boundaries, joint_development, revenue_sharing
**Focus**: Oil and gas exploration rights
**CBM Priorities**: Joint development, technical cooperation, revenue mechanisms
**Escalation Context**: Energy exploration activities in overlapping EEZ claims

**UI Behavior**:
- Shows energy resource parameters (exploration zones, joint development, revenue split, moratorium)
- Shows communication protocol parameters
- Hides resupply, fishing, and detailed EEZ parameters

### Scenario D: Natuna Islands (EEZ Boundaries)

**Primary Parties**: Malaysia (MY_CG), China (PRC_MARITIME)
**Optional Parties**: Vietnam (VN_CG)
**Key Issues**: eez_boundaries, sovereign_rights, fishing_zones, naval_patrols
**Focus**: Exclusive Economic Zone disputes
**CBM Priorities**: Boundary clarification, joint patrols, incident prevention
**Escalation Context**: Overlapping EEZ claims and patrol activities

**UI Behavior**:
- Shows EEZ boundary parameters (delimitation method, provisional arrangement, patrol coordination, buffer zones)
- Shows communication protocol parameters
- Hides resupply, fishing, and detailed energy parameters

## 9. Technical Implementation Notes

### 9.1 Session State Flow
```python
# Step 1: Scenario selected
st.session_state.selected_scenario = "scenario_A_second_thomas.json"
st.session_state.scenario_config = SCENARIO_CONFIG["scenario_A_second_thomas.json"]

# Step 1: Session started
st.session_state.selected_issues = ["resupply_SOP", "hotline_cues", ...]

# Step 2: Issues checked
has_resupply = any(issue in selected_issues for issue in ["resupply_SOP", ...])

# Step 2: Parameters shown conditionally
if has_resupply:
    # Show resupply sliders

# Step 6: Scenario context displayed
if st.session_state.scenario_config:
    escalation_context = st.session_state.scenario_config['escalation_context']
    cbm_priorities = st.session_state.scenario_config['cbm_priorities']
```

### 9.2 Key Functions and Locations

| Function/Section | Lines | Purpose |
|-----------------|-------|---------|
| SCENARIO_CONFIG | 27-74 | Master scenario configuration dictionary |
| ISSUE_DISPLAY_NAMES | 77-97 | Human-readable issue names |
| init_session_state() | 101-130 | Initialize scenario tracking variables |
| Step 1 - Scenario selection | 272-282 | Store selected scenario in session |
| Step 1 - Context display | 294-303 | Show scenario focus and context |
| Step 1 - Dynamic parties | 325-353 | Pre-populate relevant parties |
| Step 1 - Dynamic issues | 358-368 | Pre-populate relevant issues |
| Step 1 - Store issues | 376 | Save selected issues for Step 2 |
| Step 2 - Context reminder | 390-396 | Display current scenario |
| Step 2 - Issue detection | 400-415 | Check which issue categories selected |
| Step 2 - Resupply params | 418-447 | Conditional resupply UI |
| Step 2 - Fishing params | 488-516 | Conditional fishing UI |
| Step 2 - Energy params | 518-548 | Conditional energy UI |
| Step 2 - EEZ params | 550-578 | Conditional EEZ UI |
| Step 6 - Escalation context | 905-910 | Show scenario escalation context |
| Step 6 - CBM priorities | 993-1002 | Show scenario CBM priorities |
| Step 6 - Party filtering | 1071-1093 | Filter parties to scenario-relevant |

## 10. Testing Recommendations

### 10.1 Scenario A Testing
1. Select "Scenario A: Second Thomas Shoal"
2. Verify parties default to PH_GOV, PRC_MARITIME
3. Verify issues default to resupply_SOP, hotline_cues, incident_response, naval_restrictions
4. Start session
5. In Step 2, verify only resupply, communication, and media sections appear
6. In Step 6, verify escalation context shows "Resupply operations at contested shoal"
7. In Step 6, verify CBM priorities show hotline, incident reporting, safe passage

### 10.2 Scenario B Testing
1. Select "Scenario B: Scarborough Shoal"
2. Verify parties default to PH_GOV, PRC_MARITIME
3. Verify issues default to fishing_rights, access_zones, seasonal_restrictions
4. Start session
5. In Step 2, verify fishing parameters appear (access %, seasonal closures, patrols)
6. In Step 6, verify escalation context shows "Fishing vessel confrontations"
7. In Step 6, verify CBM priorities show fisheries cooperation, joint patrols

### 10.3 Scenario C Testing
1. Select "Scenario C: Kasawari Gas Field"
2. Verify parties default to MY_CG, PRC_MARITIME
3. Verify issues default to resource_extraction, maritime_boundaries, joint_development
4. Start session
5. In Step 2, verify energy parameters appear (exploration zones, revenue split, moratorium)
6. In Step 6, verify domestic politics dropdown shows Malaysia, China (not Philippines)

### 10.4 Scenario D Testing
1. Select "Scenario D: Natuna Islands"
2. Verify parties default to MY_CG, PRC_MARITIME
3. Verify issues default to eez_boundaries, sovereign_rights, fishing_zones
4. Start session
5. In Step 2, verify EEZ parameters appear (delimitation method, buffer zones)
6. In Step 6, verify escalation context shows "Overlapping EEZ claims"

### 10.5 Backward Compatibility Testing
1. Do NOT select a scenario in Step 1
2. Verify default parties and issues work
3. Verify Step 2 shows basic resupply/communication/media parameters
4. Verify Step 6 works without scenario context

## 11. Summary

The SCS Mediator SDK UI is now fully scenario-aware across all 6 workflow steps:

✅ **Step 1**: Scenario selection drives all subsequent UI behavior
✅ **Step 2**: Parameters shown dynamically based on selected issues
✅ **Step 3-5**: Work with any scenario configuration
✅ **Step 6**: Peace tools reflect scenario-specific context, CBMs, and parties

**Key Achievement**: The UI now provides a coherent, contextualized training experience where every element reflects the specific maritime dispute scenario being simulated, reducing confusion and improving pedagogical effectiveness.
