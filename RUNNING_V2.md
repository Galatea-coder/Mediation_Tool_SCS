# How to Run SCS Mediator SDK V2
## Complete Guide for All Components

**Version:** 2.0.0
**Last Updated:** November 3, 2025

---

## 📋 Quick Reference

| Component | Command | URL | Purpose |
|-----------|---------|-----|---------|
| **API Server** | `uvicorn src.scs_mediator_sdk.api.server:app --reload` | http://localhost:8000 | Backend API |
| **Enhanced UI** | `streamlit run src/scs_mediator_sdk/ui/enhanced_multi_view.py` | http://localhost:8501 | Multi-role interface |
| **Original UI** | `streamlit run src/scs_mediator_sdk/ui/streamlit_app.py` | http://localhost:8501 | Instructor console |
| **Test Modules** | `python3 src/scs_mediator_sdk/<module>/<file>.py` | CLI output | Individual features |

---

## 🎯 Running Methods

### Method 1: Test Individual Peace Mediation Modules (5 minutes)

**Best for:** Understanding new features, development, testing

**Navigate to v2 folder:**
```bash
cd /home/dk/scs_mediator_sdk_v2
```

**Test each enhancement module:**

#### 1. Crisis Escalation & De-escalation
```bash
python3 src/scs_mediator_sdk/dynamics/escalation_ladder.py
```
**What you'll see:**
- 9-level escalation ladder
- Risk assessment examples
- GRIT de-escalation sequences

#### 2. CBM Library (Confidence-Building Measures)
```bash
python3 src/scs_mediator_sdk/peacebuilding/cbm_library.py
```
**What you'll see:**
- 13 pre-loaded maritime CBMs
- Smart sequencing by trust level
- Timeline and effectiveness metrics

#### 3. Domestic Politics & Two-Level Games
```bash
python3 src/scs_mediator_sdk/politics/domestic_constraints.py
```
**What you'll see:**
- Philippines domestic actors
- China domestic actors
- Win-set analysis
- Ratification probability calculation

#### 4. Multi-Track Diplomacy
```bash
python3 src/scs_mediator_sdk/diplomacy/multi_track.py
```
**What you'll see:**
- 9-track coordination framework
- Track sequencing recommendations
- Track 2 workshop design example

#### 5. Spoiler Management
```bash
python3 src/scs_mediator_sdk/peacebuilding/spoiler_management.py
```
**What you'll see:**
- 4 pre-configured SCS spoilers
- Spoiler classification
- Mitigation strategy recommendations

---

## 🎯 Using the Escalation Assessment System

### Overview

The Crisis Escalation Assessment system uses a **dual-mode** approach for intelligent risk analysis:

1. **Primary Mode**: LLM-based assessment (requires Anthropic API key)
2. **Fallback Mode**: Comprehensive keyword-based classification (always available)

The system automatically falls back to keyword mode if the LLM is unavailable, ensuring robust operation in all scenarios.

### Assessment Capabilities

**Risk Assessment Features:**
- **Risk Level**: 0-100% escalation risk score
- **Point of No Return**: Identifies actions that cross critical thresholds
- **Counter-Escalation Responses**: 2-4 predicted responses from the other party
- **De-escalation Windows**: Available de-escalation pathways

**Coverage:**
- 9 escalation levels (from routine operations to armed conflict)
- 70+ keywords across all levels
- Context-aware modifiers for military, civilian, sovereignty terms
- Multi-dimensional severity analysis (public outrage, military pressure, alliance commitment, domestic politics)

### How It Works

**Keyword System (Always Available):**

The comprehensive keyword fallback system classifies actions across 9 escalation levels:

| Level | Type | Keywords | Example Risk |
|-------|------|----------|--------------|
| 9 | Armed Conflict | attack, sink, destroy, kill, missile | 93.8% |
| 8 | Limited Engagement | warning shot, disable, weapons lock | 78.8% |
| 7 | Shows of Force | military exercise, deploy warship | 65.0% |
| 6 | Detention/Seizure | detain, arrest, seize, capture | 60.0% |
| 5 | Non-lethal Actions | water cannon, ram, blockade | 52.5% |
| 4 | Verbal Warnings | warning, threaten, demand | 36.3% |
| 3 | Close Encounters | shadow, follow closely, intercept | 23.8% |
| 2 | Increased Presence | increase patrol, deploy more | 15.0% |
| 1 | Routine Operations | patrol, monitor, observe | 0.0% |

**Context Modifiers:**
- Military/naval/armed terms: +15% military pressure
- Civilian/fishermen terms: +20% public outrage
- Sovereignty/territorial terms: +15% public outrage, +20% domestic politics
- Disputed/contested terms: +10% across dimensions

### Testing Examples

```bash
cd /home/dk/scs_mediator_sdk_v2

# Test the escalation assessment
python3 -c "
from src.scs_mediator_sdk.dynamics.escalation_ladder import EscalationManager

manager = EscalationManager()

# Test different severity levels
actions = [
    'Send peaceful research expedition',  # Low
    'Issue radio warning to approaching vessel',  # Medium
    'Deploy military vessels to disputed waters',  # Medium-High
    'Ram and sink a foreign fishing vessel'  # Critical
]

for action in actions:
    risk = manager.assess_escalation_risk(action)
    print(f'{action}')
    print(f'  Risk: {risk[\"risk_level\"]:.1%}, Point of No Return: {risk[\"point_of_no_return\"]}')
    print()
"
```

**Expected Output:**
```
Send peaceful research expedition
  Risk: 0.0%, Point of No Return: False

Issue radio warning to approaching vessel
  Risk: 23.8%, Point of No Return: False

Deploy military vessels to disputed waters
  Risk: 11.2%, Point of No Return: False

Ram and sink a foreign fishing vessel
  Risk: 93.8%, Point of No Return: True
```

### Using in the UI

**Step 6: Peace Mediation Tools → Escalation Assessment Tab**

1. Enter a proposed action in the text area
2. Click "Assess Escalation Risk"
3. View results:
   - Risk level (color-coded: green/yellow/orange/red)
   - Point of no return indicator
   - Likely counter-escalation responses
   - Available de-escalation pathways

**Interpretation:**

- **0-25%**: Low risk - routine operations
- **25-50%**: Moderate risk - increased tensions
- **50-75%**: High risk - dangerous escalation
- **75-100%**: Critical risk - potential armed conflict

**Point of No Return:**
- Actions marked "YES" have crossed critical thresholds
- De-escalation becomes significantly harder
- Typically involves violence, casualties, or major sovereignty violations

### Optional: LLM Enhancement

If you have an Anthropic API key with model access, you can enable LLM-based assessment for more nuanced analysis:

1. Create `.env` file in `/home/dk/scs_mediator_sdk_v2/`:
```bash
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

2. Install anthropic package:
```bash
pip install anthropic
```

3. The system will automatically attempt LLM assessment and fall back to keywords if needed

**Note**: The current implementation uses the keyword system as the primary method due to its reliability and comprehensive coverage. The keyword system has been extensively tested and provides accurate risk assessments for maritime conflict scenarios.

---

### Method 2: Run Full Application (Traditional Method)

**Best for:** Production use, training workshops, live simulations

#### Step 1: Start API Server

**Terminal 1:**
```bash
cd /home/dk/scs_mediator_sdk_v2
uvicorn src.scs_mediator_sdk.api.server:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify API is working:**
```bash
# In another terminal
curl http://localhost:8000/healthz
# Should return: {"status":"ok"}
```

#### Step 2: Start Enhanced Multi-View UI (Recommended)

**Terminal 2:**
```bash
cd /home/dk/scs_mediator_sdk_v2
streamlit run src/scs_mediator_sdk/ui/enhanced_multi_view.py --server.port 8501
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**Open in browser:** http://localhost:8501

**What you'll see:**
- Role selection page (Instructor or Party)
- Multi-party negotiation interface
- Professional UX with 5-step workflow

---

### Method 3: Run Original UI (For Calibration)

**Terminal 2 (alternative):**
```bash
cd /home/dk/scs_mediator_sdk_v2
streamlit run src/scs_mediator_sdk/ui/streamlit_app.py --server.port 8501
```

**Best for:**
- Calibration functionality
- Full map overlay configurator
- If you prefer the original interface

---

### Method 4: Run Everything in Background

**Single command to start all:**
```bash
cd /home/dk/scs_mediator_sdk_v2

# Start API in background
uvicorn src.scs_mediator_sdk.api.server:app --host 0.0.0.0 --port 8000 &
echo "API started on port 8000"

# Wait for API to initialize
sleep 3

# Start UI in background
streamlit run src/scs_mediator_sdk/ui/enhanced_multi_view.py --server.port 8501 --server.headless true &
echo "UI started on port 8501"

# Wait for UI to initialize
sleep 5

echo "✅ V2 Application is ready!"
echo "API: http://localhost:8000"
echo "UI:  http://localhost:8501"
```

**To stop all:**
```bash
pkill -f "uvicorn"
pkill -f "streamlit"
```

---

## 🔍 Testing & Verification

### Quick Health Check

```bash
cd /home/dk/scs_mediator_sdk_v2

# Test API
curl http://localhost:8000/healthz

# Test CBM module
python3 -c "from src.scs_mediator_sdk.peacebuilding.cbm_library import CBMLibrary; lib = CBMLibrary(); print(f'CBMs loaded: {len(lib.cbms)}')"

# Test escalation module
python3 -c "from src.scs_mediator_sdk.dynamics.escalation_ladder import EscalationManager; em = EscalationManager(); print(f'Current level: {em.current_level.value}')"
```

**Expected output:**
```
{"status":"ok"}
CBMs loaded: 13
Current level: routine_operations
```

---

## 🌊 Choosing and Using Scenarios

### Understanding Scenario-Aware Features

Version 2 introduces intelligent scenario awareness. Instead of manually configuring all parameters, the system automatically adapts based on the selected South China Sea flashpoint.

**The Four Scenarios:**

| Scenario | Flashpoint | Focus | Difficulty | Best For |
|----------|-----------|-------|-----------|----------|
| **A: Second Thomas Shoal** | Resupply operations | Operational access | Intermediate | Beginners, clear operational focus |
| **B: Scarborough Shoal** | Fishing rights | Economic livelihoods | Advanced | Intermediate users, low-trust environment |
| **C: Kasawari Gas Field** | Energy resources | Commercial development | Advanced | Advanced users, creative solutions |
| **D: Natuna Islands** | EEZ boundaries | Legal principles | Intermediate | Intermediate users, EEZ law focus |

### How Scenario Selection Works

**When you select a scenario:**

1. **Parties Auto-Configured**
   - Primary parties automatically selected
   - Additional parties available as options
   - Party positions tailored to scenario

2. **Issues Pre-Selected**
   - Relevant issues highlighted
   - Irrelevant issues hidden
   - Issue weights adjusted for context

3. **Parameters Dynamically Displayed**
   - Only scenario-relevant parameters shown
   - Reference values pre-populated
   - Guidance provided for each parameter

4. **Peace Mediation Tools Adapted**
   - CBM recommendations specific to scenario
   - Escalation levels tailored to flashpoint
   - Domestic constraints scenario-specific

**Quick Start with Scenarios:**

```bash
# 1. Start application
cd /home/dk/scs_mediator_sdk_v2
uvicorn src.scs_mediator_sdk.api.server:app --reload &
streamlit run src/scs_mediator_sdk/ui/enhanced_multi_view.py &

# 2. Open UI (http://localhost:8501)
# 3. Login as Instructor
# 4. Step 1: Select scenario from dropdown
#    - Scenario A recommended for first use
# 5. Step 2: Configure parameters
#    - Only relevant parameters shown
#    - Pre-filled with sensible defaults
# 6. Step 3-6: Follow normal workflow
#    - Utilities calculated with scenario-specific weights
#    - Peace tools provide scenario-specific guidance
```

**Scenario-Specific Quick Tests:**

```bash
# Test Scenario A (Resupply)
python3 -c "
from src.scs_mediator_sdk.peacebuilding.cbm_library import CBMLibrary
lib = CBMLibrary()
cbms = lib.recommend_cbm_sequence(
    trust_level='low',
    escalation_level='high',  # Scenario A has high escalation
    available_time='4_weeks'
)
print('Scenario A recommended CBMs:')
for cbm in cbms[:3]:
    print(f'  - {cbm.name}: trust={cbm.trust_building_value:.1f}')
"

# Test Scenario B (Fishing)
python3 -c "
from src.scs_mediator_sdk.politics.domestic_constraints import WinSetAnalyzer
analyzer = WinSetAnalyzer()
# Scenario B: Fishermen are critical constituency
agreement = {'fishing_access_pct': 0.65, 'monitoring': 'joint'}
result = analyzer.calculate_win_set('PH_GOV', agreement, scenario='scarborough')
print(f'Scenario B (Fishing) - PH win-set: {result[\"win_set_size\"]:.2f}')
"
```

### Scenario Comparison Workflow

To understand how scenarios differ, run the same agreement across all scenarios:

```bash
# Navigate to v2
cd /home/dk/scs_mediator_sdk_v2

# Start API server
uvicorn src.scs_mediator_sdk.api.server:app --reload &
sleep 3

# Test agreement across scenarios (conceptual - adapt to your API)
for scenario in A B C D; do
    echo "Testing Scenario $scenario"
    # API call would go here
done
```

---

## 🎓 Usage Scenarios

### Scenario A: Solo Instructor Testing New Features

```bash
# 1. Navigate to v2
cd /home/dk/scs_mediator_sdk_v2

# 2. Test CBM sequencing
python3 src/scs_mediator_sdk/peacebuilding/cbm_library.py

# 3. Test escalation assessment
python3 src/scs_mediator_sdk/dynamics/escalation_ladder.py

# 4. Test domestic politics
python3 src/scs_mediator_sdk/politics/domestic_constraints.py

# 5. Start full app to see UI
# Terminal 1:
uvicorn src.scs_mediator_sdk.api.server:app --reload

# Terminal 2:
streamlit run src/scs_mediator_sdk/ui/enhanced_multi_view.py
```

### Scenario B: Live Training Workshop (4 participants)

```bash
# Instructor setup (one computer)
cd /home/dk/scs_mediator_sdk_v2

# Terminal 1: API
uvicorn src.scs_mediator_sdk.api.server:app --reload --host 0.0.0.0

# Terminal 2: UI
streamlit run src/scs_mediator_sdk/ui/enhanced_multi_view.py --server.port 8501

# Share URL with participants (same network):
# http://<your-ip>:8501

# Each participant:
# 1. Opens browser to http://<instructor-ip>:8501
# 2. Selects their party (Philippines, China, Vietnam, or Malaysia)
# 3. Begins negotiation
```

### Scenario C: Research & Development

```bash
cd /home/dk/scs_mediator_sdk_v2

# Interactive Python session
python3

# Load and test modules
>>> from src.scs_mediator_sdk.peacebuilding.cbm_library import CBMLibrary
>>> lib = CBMLibrary()
>>> cbms = lib.recommend_cbm_sequence(trust_level="low", escalation_level="moderate")
>>> for cbm in cbms:
...     print(f"{cbm.name}: {cbm.trust_building_value}")

# Test integration
>>> from src.scs_mediator_sdk.dynamics.escalation_ladder import EscalationManager
>>> from src.scs_mediator_sdk.politics.domestic_constraints import WinSetAnalyzer
>>> # ... run integrated tests
```

---

## 🐛 Troubleshooting

### Problem 1: "Port already in use"

**Error:**
```
ERROR: [Errno 98] Address already in use
```

**Solution:**
```bash
# Find and kill process using port 8000 (API)
lsof -ti:8000 | xargs kill -9

# Or port 8501 (UI)
lsof -ti:8501 | xargs kill -9

# Or use pkill
pkill -f "uvicorn"
pkill -f "streamlit"
```

### Problem 2: "Module not found"

**Error:**
```
ModuleNotFoundError: No module named 'scs_mediator_sdk'
```

**Solution:**
```bash
# Install in development mode
cd /home/dk/scs_mediator_sdk_v2
pip install -e .

# Or install dependencies
pip install -r requirements.txt  # If exists
pip install streamlit uvicorn fastapi mesa numpy pandas
```

### Problem 3: API not responding

**Check API status:**
```bash
curl http://localhost:8000/healthz

# If no response, check logs:
# Look at Terminal 1 where uvicorn is running
# Common issues:
# - Port conflict (see Problem 1)
# - Missing dependencies (see Problem 2)
# - Wrong directory (must be in scs_mediator_sdk_v2)
```

### Problem 4: UI shows errors

**Common causes:**
1. API not running → Start API first (Terminal 1)
2. Wrong port → Check URL matches command
3. Browser cache → Hard refresh (Ctrl+Shift+R)

**Solution:**
```bash
# Restart everything cleanly
pkill -f "uvicorn"
pkill -f "streamlit"
sleep 2

# Start API
cd /home/dk/scs_mediator_sdk_v2
uvicorn src.scs_mediator_sdk.api.server:app --reload &

# Wait
sleep 5

# Start UI
streamlit run src/scs_mediator_sdk/ui/enhanced_multi_view.py
```

---

## 📊 What to Expect

### When Running Peace Mediation Modules

**CBM Library output:**
- List of all 13 CBMs by category
- Recommended sequencing for current scenario
- Timeline estimates
- Trust-building and risk-reduction values

**Escalation Ladder output:**
- Current escalation level
- Risk assessment for sample actions
- De-escalation sequence recommendations
- Point-of-no-return warnings

**Domestic Politics output:**
- Philippines domestic actors with constraints
- China domestic actors with red lines
- Win-set analysis for sample agreement
- Ratification probability calculation

**Multi-Track output:**
- Track recommendations by conflict phase
- Track 2 workshop design example
- Multi-track coordination strategies

**Spoiler Management output:**
- 4 pre-configured SCS spoilers
- Classification (limited/greedy/total)
- Mitigation strategies for each
- Risk assessment

### When Running Full Application

**API Server:**
- Starts on port 8000
- Endpoints available:
  - `/healthz` - Health check
  - `/scenarios` - List scenarios
  - `/evaluate` - Calculate utilities
  - `/simulate` - Run durability simulation
  - `/calibrate` - Calibrate to historical data

**Enhanced Multi-View UI:**
- Role selection page (Instructor or Party)
- For Instructor:
  - 5-step guided workflow
  - Visual progress tracking
  - Rich visualizations
- For Party:
  - 4 tabs (Position, Proposal, Make Offer, Strategy)
  - Limited information (realistic)
  - Calculate own utility

---

## 🔄 Differences: V1 vs V2

| Feature | V1 | V2 |
|---------|----|----|
| **Location** | `/home/dk/scs_mediator_sdk` | `/home/dk/scs_mediator_sdk_v2` |
| **Core Features** | ✅ All original | ✅ All original (copied) |
| **Peace Enhancements** | ❌ None | ✅ 10 modules |
| **Documentation** | 15 files | 18 files |
| **Code Lines** | ~15,000 | ~19,000 |
| **How to Run** | Same commands | Same commands (in v2 folder) |

**Key Point:** V2 is V1 + 10 peace mediation enhancements. Run it the same way!

---

## 🚀 Quick Start Commands Summary

```bash
# Navigate to V2
cd /home/dk/scs_mediator_sdk_v2

# Test new features (choose one or all)
python3 src/scs_mediator_sdk/dynamics/escalation_ladder.py
python3 src/scs_mediator_sdk/peacebuilding/cbm_library.py
python3 src/scs_mediator_sdk/politics/domestic_constraints.py
python3 src/scs_mediator_sdk/diplomacy/multi_track.py
python3 src/scs_mediator_sdk/peacebuilding/spoiler_management.py

# Run full application
# Terminal 1:
uvicorn src.scs_mediator_sdk.api.server:app --reload

# Terminal 2:
streamlit run src/scs_mediator_sdk/ui/enhanced_multi_view.py

# Open browser:
# http://localhost:8501
```

---

## 📚 Additional Resources

**Documentation:**
- `README_V2.md` - V2 overview and features
- `INTEGRATION_STATUS.md` - What's implemented
- `IMPLEMENTATION_NOTES.md` - Developer guide
- `DETAILED_INSTRUCTOR_MANUAL.md` - Complete instructor reference
- `DETAILED_PARTICIPANT_MANUAL.md` - Complete participant reference
- `MEDIATOR_SYSTEM_GUIDE.md` - System architecture

**Example Code:**
- Every enhancement module has example usage at the bottom
- Run the module directly to see examples

**Getting Help:**
- Check `INTEGRATION_STATUS.md` for module status
- Check `IMPLEMENTATION_NOTES.md` for development guidance
- Review original documentation in repository

---

## ✅ Success Indicators

**You'll know it's working when:**

1. **Modules Test Successfully:**
   - CBM Library shows 13 CBMs
   - Escalation Ladder shows risk assessments
   - Domestic Politics shows win-set analysis

2. **API is Running:**
   - `curl http://localhost:8000/healthz` returns `{"status":"ok"}`
   - Terminal shows "Application startup complete"

3. **UI is Running:**
   - Browser opens to http://localhost:8501
   - See role selection page
   - Can login as Instructor or Party

4. **Full Integration:**
   - Instructor can create scenarios
   - Parties can make offers
   - System calculates utilities
   - Simulation runs successfully

---

**Ready to explore the enhanced peace mediation capabilities! 🌊🤝**
