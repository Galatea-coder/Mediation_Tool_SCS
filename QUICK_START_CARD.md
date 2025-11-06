# Peace Mediation UI - Quick Start Card

## 🚀 Launch

```bash
cd /home/dk/scs_mediator_sdk_v2
./run_peace_mediation_ui.sh
```

Opens at: http://localhost:8501

---

## 🛠️ 5 Tools Available

### 1. 📊 Escalation Assessment
**What**: Risk assessment for proposed actions
**Use When**: Before taking any action that could escalate tensions
**Key Output**: Risk level + counter-escalation predictions + de-escalation steps

**Quick Example**:
1. Check current escalation level (visual ladder)
2. Enter proposed action: "Deploy military escort"
3. Click "Assess Risk"
4. Review risk level (LOW/MODERATE/HIGH)

---

### 2. 🤝 CBM Recommendations
**What**: Confidence-building measure recommendations
**Use When**: Planning trust-building activities
**Key Output**: Sequenced list of CBMs with implementation guides

**Quick Example**:
1. Set trust level: 0.3 (low)
2. Set escalation level: 4 (verbal warnings)
3. Set available time: 20 weeks
4. Click "Get CBM Recommendations"
5. Review 4-6 recommended CBMs

---

### 3. 🏛️ Domestic Politics
**What**: Tests if proposals can be ratified domestically
**Use When**: Before finalizing any agreement
**Key Output**: Ratification probability + objectors + required compensations

**Quick Example**:
1. Select party: Philippines or China
2. Check win-set size (flexibility indicator)
3. Set proposal sliders (fisheries, sovereignty, tensions)
4. Click "Test Proposal"
5. Review acceptability verdict

---

### 4. 🌐 Multi-Track Diplomacy
**What**: Coordination guidance for different diplomatic tracks
**Use When**: Planning negotiation strategy
**Key Output**: Phase-specific track recommendations

**Quick Example**:
1. Select phase: Pre-negotiation / Negotiation / Implementation
2. Review recommended tracks (Track 1, 1.5, 2, etc.)
3. Plan activities for each track
4. Note coordination mechanisms

---

### 5. ⚠️ Spoiler Management
**What**: Identifies actors who may undermine peace
**Use When**: Planning implementation and protection
**Key Output**: Spoiler list + management strategies + risk assessment

**Quick Example**:
1. Review 4 identified spoilers
2. Check threat levels
3. Set proposal checkboxes (shared resources, monitoring, etc.)
4. Click "Assess Spoiling Risk"
5. Review protective measures needed

---

## 📊 Typical Workflow

### Scenario: Testing a Proposal

```
1. Escalation Assessment
   → Current level: Level 4 (Verbal Warnings)
   → Risk: Moderate ⚠️

2. CBM Recommendations
   → Recommend: Hotline + Pre-notification + Standoff distance
   → Timeline: 12 weeks

3. Domestic Politics (Philippines)
   → Win-set: 48% (constrained)
   → Ratification: 78% ✅
   → Objectors: None

4. Domestic Politics (China)
   → Win-set: 52% (constrained)
   → Ratification: 72% ✅
   → Objectors: None

5. Spoiler Management
   → Overall risk: Moderate
   → High-threat: Maritime Militia
   → Protective measures: 5 recommended

RESULT: Proposal is acceptable but needs protective measures
```

---

## ⚠️ Common Issues

### Import Error
```bash
# Set PYTHONPATH
export PYTHONPATH=/home/dk/scs_mediator_sdk_v2/src:$PYTHONPATH
streamlit run src/scs_mediator_sdk/ui/peace_mediation_ui.py
```

### Port Busy
```bash
# Use different port
streamlit run src/scs_mediator_sdk/ui/peace_mediation_ui.py --server.port 8502
```

### Streamlit Not Found
```bash
pip install streamlit
```

---

## 📚 Documentation

- **Full Guide**: PEACE_MEDIATION_UI_GUIDE.md
- **Comparison**: UI_COMPARISON_AND_FEATURES.md
- **Report**: PEACE_MEDIATION_UI_REPORT.md
- **This Card**: QUICK_START_CARD.md

---

## ✅ Validation Test

```bash
# Quick test that everything works
cd /home/dk/scs_mediator_sdk_v2
python3 -c "
import sys
sys.path.insert(0, 'src')
from scs_mediator_sdk.dynamics.escalation_ladder import EscalationManager
from scs_mediator_sdk.peacebuilding.cbm_library import CBMLibrary
from scs_mediator_sdk.politics.domestic_constraints import WinSetAnalyzer
from scs_mediator_sdk.diplomacy.multi_track import MultiTrackMediator
from scs_mediator_sdk.peacebuilding.spoiler_management import SpoilerManager
print('✅ All modules ready!')
"
```

---

## 💡 Pro Tips

1. **Start with Escalation**: Always assess escalation risk first
2. **Test Domestically**: Proposals that look good often fail domestic ratification
3. **Sequence CBMs**: Start with easy communication CBMs before cooperation
4. **Manage Spoilers Early**: Identify and plan for spoilers from the beginning
5. **Use Multi-Track**: Don't rely only on Track 1 (official) negotiations

---

## 🎯 Key Metrics to Watch

### Escalation
- Current level < 6 ✅
- Risk level < 0.6 ✅
- Point of no return: False ✅

### CBMs
- Trust building > 0.5 ✅
- Risk reduction > 0.6 ✅
- Timeline < available time ✅

### Domestic Politics
- Win-set size > 0.4 ✅
- Ratification probability > 0.6 ✅
- Objectors = 0 ✅

### Spoilers
- Overall risk < 0.5 ✅
- High-threat spoilers = 0 ✅
- Protective measures implemented ✅

---

## 🔗 Integration with Enhanced Multi-View

### Enhanced Multi-View UI
**Use for**: Scenario setup, offer building, simulation

### Peace Mediation UI
**Use for**: Risk assessment, deep analysis, theory-based recommendations

### Recommended Workflow
1. Setup scenario in Enhanced Multi-View
2. Build offer in Enhanced Multi-View
3. **Switch to Peace Mediation UI**
4. Test offer with all 5 tools
5. **Return to Enhanced Multi-View**
6. Refine offer based on insights
7. Run simulation in Enhanced Multi-View
8. **Switch to Peace Mediation UI for post-analysis**

---

## 📖 Theory Quick Reference

| Tool | Theory | Scholar | Year |
|------|--------|---------|------|
| Escalation | Escalation Ladder | Herman Kahn | 1965 |
| Escalation | GRIT | Charles Osgood | 1962 |
| CBM | CBMs | Various | 1970s-90s |
| Domestic | Two-Level Game | Robert Putnam | 1988 |
| Multi-Track | Multi-Track Diplomacy | McDonald & Diamond | 1996 |
| Spoiler | Spoiler Problem | Stephen Stedman | 1997 |

---

## 🎓 Educational Use

### Week 1-2: Escalation
- Teach theory, use Escalation Assessment tool

### Week 3-4: CBMs
- Teach theory, use CBM Recommendations tool

### Week 5-6: Domestic
- Teach theory, use Domestic Politics tool

### Week 7-8: Multi-Track
- Teach theory, use Multi-Track tool

### Week 9-10: Spoilers
- Teach theory, use Spoiler Management tool

---

## 🏁 Ready to Start?

```bash
./run_peace_mediation_ui.sh
```

**That's it!** The UI will open in your browser at http://localhost:8501

Select a tool from the sidebar and start analyzing!

---

**Version**: 1.0 | **Date**: 2025-11-03 | **Status**: ✅ Production Ready
