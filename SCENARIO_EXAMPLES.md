# Scenario-Aware UI: Detailed Examples

This document provides concrete examples of how the UI behaves for each of the 4 scenarios.

---

## Example 1: Scenario A - Second Thomas Shoal (Resupply)

### Context
The Philippines maintains a small garrison on the grounded BRP Sierra Madre at Second Thomas Shoal. Regular resupply missions bring food and supplies to the troops, but Chinese maritime forces often block or harass these missions. The focus is on creating procedures for safe resupply operations.

### Step 1: What You See

**Scenario Selection:**
```
Dropdown: "🏝️ Scenario A: Second Thomas Shoal (Resupply)"
```

**Scenario Context Box:**
```
┌─────────────────────────────────────────────────────────────┐
│ Scenario Context                                            │
│ Focus: Ensuring safe passage for humanitarian resupply     │
│        missions while managing naval presence               │
│ Context: Philippine resupply missions to BRP Sierra Madre   │
└─────────────────────────────────────────────────────────────┘
```

**Participating Parties (pre-populated):**
```
✓ Recommended for this scenario: PH GOV, PRC MARITIME

[X] 🇵🇭 Philippines
[X] 🇨🇳 PRC Maritime
[ ] 🇻🇳 Vietnam
[ ] 🇲🇾 Malaysia
```

**Issues to Negotiate (pre-populated):**
```
✓ Recommended for this scenario: Resupply Standard Operating Procedures,
  Hotline & CUES Protocols, Incident Response Procedures, Naval Movement
  Restrictions

[X] Resupply Standard Operating Procedures
[X] Hotline & CUES Protocols
[X] Incident Response Procedures
[X] Naval Movement Restrictions
[ ] Media & Public Communication
[ ] Fishing Rights & Access
```

### Step 2: What You See

**Scenario Reminder Banner:**
```
┌─────────────────────────────────────────────────────────────┐
│ Scenario: Second Thomas Shoal (Resupply)                   │
│ Ensuring safe passage for humanitarian resupply missions   │
│ while managing naval presence                              │
└─────────────────────────────────────────────────────────────┘
```

**Visible Parameter Sections:**

```
┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐
│ 🚢 Resupply     │  │ 📞 Communication │  │ 📰 Media        │
│    Operations   │  │    Protocols     │  │    Management   │
├─────────────────┤  ├──────────────────┤  ├─────────────────┤
│ Standoff        │  │ Hotline          │  │ News Embargo    │
│ Distance:       │  │ Availability:    │  │ Period:         │
│ [====|====] 3nm │  │ [24/7 Direct]    │  │ [==|======] 6hr │
│                 │  │                  │  │                 │
│ Max Escorts:    │  │ CUES Compliance: │  │                 │
│ [=|=========] 1 │  │ [X] Safe Distance│  │                 │
│                 │  │ [X] AIS Active   │  │                 │
│ Pre-Notify:     │  │ [ ] Video Record │  │                 │
│ [==|======] 12hr│  │                  │  │                 │
└─────────────────┘  └──────────────────┘  └─────────────────┘

HIDDEN SECTIONS (not shown):
❌ Fishing & Access Rights
❌ Energy & Resource Rights
❌ EEZ & Maritime Boundaries
```

**Generated Agreement JSON:**
```json
{
  "resupply_SOP": {
    "standoff_nm": 3,
    "escort_count": 1,
    "pre_notification_hours": 12
  },
  "hotline_cues": {
    "hotline_status": "24_7",
    "cues_checklist": ["distance", "AIS_on"]
  },
  "media_protocol": {
    "embargo_hours": 6
  }
}
```

### Step 6: What You See

**Escalation Assessment Tab:**
```
┌─────────────────────────────────────────────────────────────┐
│ Scenario Context: Resupply operations at contested shoal   │
│ with garrison presence                                      │
└─────────────────────────────────────────────────────────────┘

Current Escalation Level: Level 4: Naval Presence

Assess Proposed Action:
"Deploy additional coast guard vessels to escort resupply mission"

[Assess Escalation Risk]
```

**CBM Recommendations Tab:**
```
┌─────────────────────────────────────────────────────────────┐
│ Priority CBMs for Second Thomas Shoal (Resupply):          │
│ • Hotline Establishment                                     │
│ • Incident Reporting                                        │
│ • Safe Passage Protocol                                     │
└─────────────────────────────────────────────────────────────┘
```

**Domestic Politics Tab:**
```
┌─────────────────────────────────────────────────────────────┐
│ Parties in this scenario: PH GOV, PRC MARITIME             │
└─────────────────────────────────────────────────────────────┘

Select Party to Analyze:
[ Philippines ▼ ]  (Dropdown only shows: Philippines, China)
  China
```

---

## Example 2: Scenario B - Scarborough Shoal (Fishing Rights)

### Context
Scarborough Shoal is a rich fishing ground traditionally used by Filipino fishermen. China has asserted control, blocking access. The focus is on balancing traditional fishing access with territorial claims.

### Step 1: What You See

**Scenario Selection:**
```
Dropdown: "🎣 Scenario B: Scarborough Shoal (Fishing Rights)"
```

**Scenario Context Box:**
```
┌─────────────────────────────────────────────────────────────┐
│ Scenario Context                                            │
│ Focus: Balancing traditional fishing access with            │
│        territorial claims                                   │
│ Context: Traditional fishing grounds and access rights      │
└─────────────────────────────────────────────────────────────┘
```

**Participating Parties (pre-populated):**
```
✓ Recommended for this scenario: PH GOV, PRC MARITIME

[X] 🇵🇭 Philippines
[X] 🇨🇳 PRC Maritime
[ ] 🇻🇳 Vietnam
[ ] 🇲🇾 Malaysia
```

**Issues to Negotiate (pre-populated):**
```
✓ Recommended for this scenario: Fishing Rights & Access,
  Designated Access Zones, Seasonal Access Restrictions,
  Enforcement & Monitoring Protocols

[X] Fishing Rights & Access
[X] Designated Access Zones
[X] Seasonal Access Restrictions
[X] Enforcement & Monitoring Protocols
[ ] Hotline & CUES Protocols
[ ] Media & Public Communication
```

### Step 2: What You See

**Scenario Reminder Banner:**
```
┌─────────────────────────────────────────────────────────────┐
│ Scenario: Scarborough Shoal (Fishing Rights)               │
│ Balancing traditional fishing access with territorial claims│
└─────────────────────────────────────────────────────────────┘
```

**Visible Parameter Sections:**

```
┌────────────────────────────────────────────────────────────┐
│ 🎣 Fishing & Access Rights                                 │
├──────────────────┬──────────────────┬──────────────────────┤
│ Access Zones     │ Seasonal Rules   │ Enforcement          │
├──────────────────┼──────────────────┼──────────────────────┤
│ Traditional      │ Seasonal Closure │ Joint Patrol         │
│ Fishing Access:  │ (days/year):     │ Frequency:           │
│ [======|==] 70%  │ [==|======] 60   │ [Monthly ▼]          │
│                  │                  │  Weekly              │
│                  │                  │  Monthly             │
│                  │                  │  Quarterly           │
└──────────────────┴──────────────────┴──────────────────────┘

HIDDEN SECTIONS (not shown):
❌ Resupply Operations
❌ Energy & Resource Rights
❌ EEZ & Maritime Boundaries
```

**Generated Agreement JSON:**
```json
{
  "fishing_rights": {
    "traditional_access_pct": 70,
    "seasonal_closure_days": 60,
    "patrol_frequency": "monthly"
  },
  "hotline_cues": {
    "hotline_status": "24_7",
    "cues_checklist": ["distance", "AIS_on"]
  },
  "media_protocol": {
    "embargo_hours": 6
  }
}
```

### Step 6: What You See

**Escalation Assessment Tab:**
```
┌─────────────────────────────────────────────────────────────┐
│ Scenario Context: Fishing vessel confrontations in         │
│ contested waters                                            │
└─────────────────────────────────────────────────────────────┘
```

**CBM Recommendations Tab:**
```
┌─────────────────────────────────────────────────────────────┐
│ Priority CBMs for Scarborough Shoal (Fishing Rights):      │
│ • Fisheries Cooperation                                     │
│ • Joint Patrols                                             │
│ • Resource Sharing                                          │
└─────────────────────────────────────────────────────────────┘
```

**Domestic Politics Tab:**
```
┌─────────────────────────────────────────────────────────────┐
│ Parties in this scenario: PH GOV, PRC MARITIME             │
└─────────────────────────────────────────────────────────────┘
```

---

## Example 3: Scenario C - Kasawari Gas Field (Energy)

### Context
The Kasawari gas field lies in waters claimed by both Malaysia and China. Malaysia wants to develop the field, but China opposes unilateral extraction. The focus is on managing energy resource extraction and revenue distribution.

### Step 1: What You See

**Scenario Selection:**
```
Dropdown: "⛽ Scenario C: Kasawari Gas Field (Energy)"
```

**Scenario Context Box:**
```
┌─────────────────────────────────────────────────────────────┐
│ Scenario Context                                            │
│ Focus: Managing energy resource extraction and revenue      │
│        distribution                                         │
│ Context: Oil and gas exploration rights in contested EEZ    │
└─────────────────────────────────────────────────────────────┘
```

**Participating Parties (pre-populated):**
```
✓ Recommended for this scenario: MY CG, PRC MARITIME

[ ] 🇵🇭 Philippines
[X] 🇨🇳 PRC Maritime
[X] 🇻🇳 Vietnam          ← Note: Vietnam now AVAILABLE
[X] 🇲🇾 Malaysia
```

**Issues to Negotiate (pre-populated):**
```
✓ Recommended for this scenario: Resource Extraction Rights,
  Maritime Boundary Delimitation, Joint Development Agreements,
  Revenue Sharing Mechanisms

[X] Resource Extraction Rights
[X] Maritime Boundary Delimitation
[X] Joint Development Agreements
[X] Revenue Sharing Mechanisms
[ ] Exploration Rights Management
[ ] Hotline & CUES Protocols
```

### Step 2: What You See

**Scenario Reminder Banner:**
```
┌─────────────────────────────────────────────────────────────┐
│ Scenario: Kasawari Gas Field (Energy)                      │
│ Managing energy resource extraction and revenue distribution│
└─────────────────────────────────────────────────────────────┘
```

**Visible Parameter Sections:**

```
┌────────────────────────────────────────────────────────────┐
│ ⛽ Energy & Resource Rights                                │
├──────────────────┬──────────────────┬──────────────────────┤
│ Exploration      │ Joint Development│ Timeline             │
│ Rights           │                  │                      │
├──────────────────┼──────────────────┼──────────────────────┤
│ Approved         │ [X] Enable Joint │ Initial Moratorium:  │
│ Exploration      │     Development  │ [==|======] 12 mo    │
│ Zones:           │                  │                      │
│ [X] Zone A       │ Revenue Split:   │                      │
│ [ ] Zone B       │ [====|====] 50%  │                      │
│ [ ] Zone C       │                  │                      │
│ [ ] Zone D       │                  │                      │
└──────────────────┴──────────────────┴──────────────────────┘

HIDDEN SECTIONS (not shown):
❌ Resupply Operations
❌ Fishing & Access Rights
```

**Generated Agreement JSON:**
```json
{
  "resource_extraction": {
    "exploration_zones": ["Zone A"],
    "joint_development": true,
    "revenue_split_pct": 50,
    "moratorium_months": 12
  },
  "hotline_cues": {
    "hotline_status": "24_7",
    "cues_checklist": ["distance", "AIS_on"]
  }
}
```

### Step 6: What You See

**Escalation Assessment Tab:**
```
┌─────────────────────────────────────────────────────────────┐
│ Scenario Context: Energy exploration activities in         │
│ overlapping EEZ claims                                      │
└─────────────────────────────────────────────────────────────┘
```

**CBM Recommendations Tab:**
```
┌─────────────────────────────────────────────────────────────┐
│ Priority CBMs for Kasawari Gas Field (Energy):             │
│ • Joint Development                                         │
│ • Technical Cooperation                                     │
│ • Revenue Mechanisms                                        │
└─────────────────────────────────────────────────────────────┘
```

**Domestic Politics Tab:**
```
┌─────────────────────────────────────────────────────────────┐
│ Parties in this scenario: MY CG, PRC MARITIME              │
└─────────────────────────────────────────────────────────────┘

Select Party to Analyze:
[ Malaysia ▼ ]  (Dropdown only shows: Malaysia, China)
  China
```

---

## Example 4: Scenario D - Natuna Islands (EEZ Boundaries)

### Context
Indonesia and Malaysia's EEZ claims overlap with China's nine-dash line near the Natuna Islands. The focus is on clarifying maritime boundaries and sovereign rights in contested waters.

### Step 1: What You See

**Scenario Selection:**
```
Dropdown: "🌊 Scenario D: Natuna Islands (EEZ Boundaries)"
```

**Scenario Context Box:**
```
┌─────────────────────────────────────────────────────────────┐
│ Scenario Context                                            │
│ Focus: Clarifying maritime boundaries and sovereign rights  │
│        in contested waters                                  │
│ Context: Exclusive Economic Zone boundary disputes          │
└─────────────────────────────────────────────────────────────┘
```

**Participating Parties (pre-populated):**
```
✓ Recommended for this scenario: MY CG, PRC MARITIME

[ ] 🇵🇭 Philippines
[X] 🇨🇳 PRC Maritime
[X] 🇻🇳 Vietnam          ← Note: Vietnam available
[X] 🇲🇾 Malaysia
```

**Issues to Negotiate (pre-populated):**
```
✓ Recommended for this scenario: EEZ Boundary Clarification,
  Sovereign Rights Recognition, Fishing Zone Management,
  Naval Patrol Coordination

[X] EEZ Boundary Clarification
[X] Sovereign Rights Recognition
[X] Fishing Zone Management
[X] Naval Patrol Coordination
[ ] Resource Extraction Rights
[ ] Hotline & CUES Protocols
```

### Step 2: What You See

**Scenario Reminder Banner:**
```
┌─────────────────────────────────────────────────────────────┐
│ Scenario: Natuna Islands (EEZ Boundaries)                  │
│ Clarifying maritime boundaries and sovereign rights        │
└─────────────────────────────────────────────────────────────┘
```

**Visible Parameter Sections:**

```
┌────────────────────────────────────────────────────────────┐
│ 🌊 EEZ & Maritime Boundaries                               │
├─────────────────────────────┬──────────────────────────────┤
│ Boundary Clarification      │ Patrol Coordination          │
├─────────────────────────────┼──────────────────────────────┤
│ Delimitation Method:        │ Coordination Level:          │
│ [Negotiated ▼]              │ [Notification ▼]             │
│  Equidistance               │  None                        │
│  Natural Prolongation       │  Notification                │
│  Negotiated                 │  Joint Patrols               │
│                             │                              │
│ [X] Provisional Arrangement │ Buffer Zone:                 │
│                             │ [===|=====] 12 nm            │
└─────────────────────────────┴──────────────────────────────┘

HIDDEN SECTIONS (not shown):
❌ Resupply Operations
❌ Fishing & Access Rights (detailed)
❌ Energy & Resource Rights (detailed)
```

**Generated Agreement JSON:**
```json
{
  "eez_boundaries": {
    "delimitation_method": "negotiated",
    "provisional_arrangement": true,
    "patrol_coordination": "notification",
    "buffer_zone_nm": 12
  },
  "hotline_cues": {
    "hotline_status": "24_7",
    "cues_checklist": ["distance", "AIS_on"]
  }
}
```

### Step 6: What You See

**Escalation Assessment Tab:**
```
┌─────────────────────────────────────────────────────────────┐
│ Scenario Context: Overlapping EEZ claims and patrol        │
│ activities                                                  │
└─────────────────────────────────────────────────────────────┘
```

**CBM Recommendations Tab:**
```
┌─────────────────────────────────────────────────────────────┐
│ Priority CBMs for Natuna Islands (EEZ Boundaries):         │
│ • Boundary Clarification                                    │
│ • Joint Patrols                                             │
│ • Incident Prevention                                       │
└─────────────────────────────────────────────────────────────┘
```

**Domestic Politics Tab:**
```
┌─────────────────────────────────────────────────────────────┐
│ Parties in this scenario: MY CG, PRC MARITIME              │
└─────────────────────────────────────────────────────────────┘

Select Party to Analyze:
[ Malaysia ▼ ]  (Dropdown only shows: Malaysia, China)
  China
```

---

## Key Differences Summary Table

| Feature | Scenario A | Scenario B | Scenario C | Scenario D |
|---------|-----------|-----------|-----------|-----------|
| **Icon** | 🏝️ | 🎣 | ⛽ | 🌊 |
| **Primary Parties** | PH, China | PH, China | MY, China | MY, China |
| **Optional Parties** | None | None | Vietnam | Vietnam |
| **Main Issue Category** | Resupply | Fishing | Energy | EEZ |
| **Step 2 Unique Params** | Standoff, Escorts | Access %, Closures | Exploration, Revenue | Delimitation, Buffer |
| **CBM Focus** | Hotlines, Incidents | Cooperation, Patrols | Joint Dev, Tech | Boundaries, Patrols |
| **Escalation Context** | Garrison resupply | Fishing confrontations | Energy exploration | EEZ overlaps |

---

## Testing Each Scenario

### Quick Test Procedure

1. **Select scenario in Step 1**
2. **Verify auto-populated parties match table above**
3. **Verify auto-populated issues match scenario focus**
4. **Click "Start Session"**
5. **In Step 2, verify only relevant parameter sections appear**
6. **Skip to Step 6, verify:**
   - Escalation context matches table
   - CBM priorities match table
   - Domestic politics dropdown only shows relevant parties

### Expected Results

✅ **All scenarios should show different UI elements in Step 2**
✅ **No scenario should show all parameter sections**
✅ **Step 6 should always show scenario-specific context**
✅ **Party dropdowns should filter based on scenario**

---

## Conclusion

The UI now provides 4 distinct, contextualized training experiences rather than one generic interface. Each scenario presents only the information relevant to that specific maritime dispute, improving clarity and pedagogical effectiveness.
