# 🌊 Using SCS Training Scenarios with the Simulation Tool

## ✅ YES! The Simulation Tool is Ready

Your SCS scenarios **already work** with the simulation tool. Everything is configured and ready to use.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
cd /home/dk/scs_mediator_sdk
pip install -e .
```

This installs: numpy, pandas, mesa, streamlit, fastapi, and all other requirements.

### Step 2: Start the Servers

**Terminal 1 - API Server:**
```bash
uvicorn src.scs_mediator_sdk.api.server:app --reload
```

**Terminal 2 - UI:**
```bash
# Option A: Original UI (simpler, proven)
streamlit run src/scs_mediator_sdk/ui/streamlit_app.py

# Option B: Enhanced UI (full mediation process)
streamlit run src/scs_mediator_sdk/ui/enhanced_app.py
```

### Step 3: Use It!

Open browser: **http://localhost:8501**

---

## 📋 Your 4 SCS Scenarios

All located in: `/home/dk/scs_mediator_sdk/cases/scs/`

### Scenario A: Second Thomas Shoal
- **File**: `scenario_A_second_thomas.json`
- **Manual**: `SCS_Training_Manuals/Manual_A_Second_Thomas.docx`
- **Focus**: Resupply operations
- **Flashpoint**: Philippine garrison resupply
- **Difficulty**: Intermediate

### Scenario B: Scarborough Shoal
- **File**: `scenario_B_scarborough.json`
- **Manual**: `SCS_Training_Manuals/Manual_B_Scarborough.docx`
- **Focus**: Fishing rights
- **Flashpoint**: Traditional fishing grounds
- **Difficulty**: Advanced (high tension)

### Scenario C: Kasawari Gas Field
- **File**: `scenario_C_kasawari.json`
- **Manual**: `SCS_Training_Manuals/Manual_C_Kasawari.docx`
- **Focus**: Energy resources
- **Flashpoint**: Natural gas exploration
- **Difficulty**: Advanced (economic stakes)

### Scenario D: Natuna Islands
- **File**: `scenario_D_natuna.json`
- **Manual**: `SCS_Training_Manuals/Manual_D_Natuna.docx`
- **Focus**: EEZ boundaries
- **Flashpoint**: Exclusive Economic Zone
- **Difficulty**: Intermediate

---

## 🎯 What You Can Do with Each Scenario

### 1. Build Agreements

Use the UI sliders to configure:

**Resupply Standard Operating Procedures (SOP)**:
- Standoff distance (0-10 nautical miles)
- Number of escorts (0-5)
- Pre-notification time (0-48 hours)

**Communication Protocols**:
- Hotline status (ad-hoc vs 24/7)
- CUES compliance (collision avoidance)
- AIS transparency requirements

**Media Management**:
- News embargo period (0-24 hours)
- Joint statement protocols

**Fisheries (where applicable)**:
- Fishing corridors
- Seasonal restrictions
- Joint monitoring

### 2. Evaluate Offers

The system calculates:
- **Utility scores** (0-1) for each party
  - >0.8 = Excellent
  - 0.6-0.8 = Good
  - 0.4-0.6 = Acceptable
  - <0.4 = Below BATNA (reject)

- **Acceptance probabilities** (%)
  - >70% = Likely to accept
  - 50-70% = Uncertain
  - <50% = Likely to reject

- **Overall agreement probability**
  - Product of all acceptance probabilities

### 3. Run Simulations

Test agreement durability over time (50-1000 steps):

**Results show**:
- Total incident count
- Severity distribution
- Incident types (water cannon, ramming, detention, near-miss)
- Trend analysis (escalating vs declining)
- Time-series visualization
- Severity histogram

### 4. Calibrate Parameters

Fit model to historical data:
- Upload incident counts per time period
- System finds optimal risk parameters
- Improves predictive accuracy

---

## 💡 Example Workflow

### Scenario A: Second Thomas Shoal

**Context** (from training manual):
- Philippines maintains garrison on grounded ship
- Regular resupply missions required
- China blocks/harasses resupply attempts
- High tension, risk of escalation

**Your Task**:
1. **Select** scenario_A_second_thomas.json in UI
2. **Analyze** the baseline conditions
3. **Design** agreement terms:
   - Standoff: 3 nm (balance security/access)
   - Escorts: 1 (minimal but present)
   - Notification: 12 hours (advance warning)
   - Hotline: 24/7 (crisis management)
   - Embargo: 6 hours (face-saving delay)

4. **Evaluate**: Click "Evaluate Offer"
   - Check utilities > 0.5 for both parties
   - Verify acceptance >60%

5. **Simulate**: Click "Run Simulation" (300 steps)
   - Target: <20 incidents
   - Target: Declining trend
   - Max severity <0.6

6. **Iterate**: Adjust terms based on results

---

## 📊 Understanding Results

### Good Agreement Indicators

✅ **Both parties above BATNA** (utility >0.4)
✅ **Acceptance probability >60%** for all
✅ **Low incident count** in simulation (<25)
✅ **Declining trend** (late < early incidents)
✅ **Low severity** (avg <0.4)

### Warning Signs

⚠️ **One party below BATNA** → Renegotiate
⚠️ **Low acceptance (<50%)** → Adjust terms
⚠️ **High incidents (>40)** → Strengthen provisions
⚠️ **Escalating trend** → Agreement not working
⚠️ **High severity (>0.7)** → Crisis risk

---

## 🎓 Training Manual Integration

We've extracted content from your 4 training manuals and created enhanced scenarios:

**Location**: `/home/dk/scs_mediator_sdk/cases/scs_enhanced/`

These include:
- Background context (3000+ chars each)
- Party positions and interests
- Legal/political context
- Learning objectives
- Historical incidents

**To use**:
```python
import json

# Load enhanced scenario
with open('cases/scs_enhanced/scenario_A_enhanced.json', 'r') as f:
    enhanced = json.load(f)

# Access training manual content
background = enhanced['scenario_info']['background']
manual_excerpt = enhanced['manual_text_excerpt']
```

---

## 🔧 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -e .
```

### API not responding
```bash
# Check if running
curl http://localhost:8000/healthz

# Should return: {"status":"ok"}
```

### UI won't load
```bash
# Check Streamlit version
streamlit --version

# Should be >=1.36.0
pip install --upgrade streamlit
```

### Scenarios not showing
Check file path in UI:
```
Case folder: cases/scs  (default)
```

---

## 🚀 Advanced Usage

### Python API

```python
from scs_mediator_sdk.engines.bargaining_engine import BargainingSession, AgreementVector

# Create session
session = BargainingSession.start(
    case_id="scs_second_thomas",
    parties=['PH_GOV', 'PRC_MARITIME'],
    mediator='ASEAN',
    issue_space=['resupply_SOP', 'hotline_cues']
)

# Evaluate offer
agreement = AgreementVector({"resupply_SOP": {"standoff_nm": 3}})
result = session.evaluate_offer('PH_GOV', agreement)

print(result['utilities'])
print(result['acceptance_prob'])
```

### REST API

```bash
# Start session
curl -X POST http://localhost:8000/bargain/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "scs_test",
    "parties": ["PH_GOV", "PRC_MARITIME"],
    "mediator": "ASEAN",
    "issue_space": ["resupply_SOP"]
  }'

# Evaluate offer
curl -X POST http://localhost:8000/bargain/scs_test/offer \
  -H "Content-Type: application/json" \
  -d '{
    "proposer_party_id": "PH_GOV",
    "agreement_vector": {
      "resupply_SOP": {"standoff_nm": 3}
    }
  }'

# Run simulation
curl -X POST http://localhost:8000/sim/run \
  -H "Content-Type: application/json" \
  -d '{
    "steps": 300,
    "environment": {"weather_state": "rough"},
    "agreement_vector": {"resupply_SOP": {"standoff_nm": 3}}
  }'
```

---

## 📚 Next Steps

1. **Install and test**
   ```bash
   pip install -e .
   python3 quick_demo.py
   ```

2. **Run UI and try all 4 scenarios**
   - Start with Scenario A (easier)
   - Progress to B, C, D (more complex)

3. **Review training manuals**
   - Read the .docx files for context
   - Understand party positions
   - Identify interests vs positions

4. **Create your own scenarios**
   - Copy existing scenario JSON
   - Modify parameters
   - Test with simulation

5. **Run a training workshop**
   - Use War Room format
   - Have participants negotiate
   - Analyze results together

---

## ✅ Summary

**You have**:
- ✅ 4 working SCS scenarios
- ✅ Training manuals with context
- ✅ Working simulation tool (original + enhanced)
- ✅ Complete documentation

**To use**:
1. Install: `pip install -e .`
2. Start: API + UI (2 terminals)
3. Open: http://localhost:8501
4. Select: Scenario A, B, C, or D
5. Build: Agreement terms
6. Evaluate: See results
7. Simulate: Test durability

**It's ready to use RIGHT NOW!** 🚀
