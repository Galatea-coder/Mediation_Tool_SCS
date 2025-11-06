# Peace Mediation UI - User Guide

## Overview

The Peace Mediation UI integrates all 10 peace mediation enhancements from the SCS Mediator SDK v2 into a single, easy-to-use interface for mediators and instructors.

## Features Integrated

### 1. Escalation Assessment (📊)
- **Module**: `dynamics/escalation_ladder.py`
- **Theory**: Herman Kahn's escalation ladder + Osgood's GRIT
- **Features**:
  - Visual 9-level escalation ladder
  - Real-time risk assessment for proposed actions
  - Counter-escalation predictions
  - De-escalation sequence recommendations
  - Point-of-no-return warnings

### 2. CBM Recommendations (🤝)
- **Module**: `peacebuilding/cbm_library.py`
- **Features**:
  - 15+ maritime-specific CBMs
  - Sequenced recommendations based on:
    - Current trust level
    - Escalation level
    - Available timeline
  - CBM library browser by category
  - Implementation step-by-step guides
  - Effectiveness metrics (trust building, risk reduction)

### 3. Domestic Politics Analysis (🏛️)
- **Module**: `politics/domestic_constraints.py`
- **Theory**: Putnam's Two-Level Game Theory
- **Features**:
  - Win-set size calculator (negotiating flexibility)
  - Domestic deal breaker identification
  - Proposal acceptability testing
  - Ratification probability estimation
  - Required compensations to build support
  - Ratification strategy recommendations
  - Pre-configured for Philippines and China

### 4. Multi-Track Diplomacy (🌐)
- **Module**: `diplomacy/multi_track.py`
- **Theory**: McDonald & Diamond's Multi-Track Diplomacy
- **Features**:
  - Phase-specific track recommendations:
    - Pre-negotiation
    - Negotiation
    - Implementation
  - 10 diplomatic track overview
  - Track coordination mechanisms
  - Track integration guidance

### 5. Spoiler Management (⚠️)
- **Module**: `peacebuilding/spoiler_management.py`
- **Theory**: Stedman's Spoiler Problem Framework
- **Features**:
  - 4 pre-identified SCS spoilers
  - Spoiler type classification (Limited/Greedy/Total)
  - Capability assessment (Low/Medium/High)
  - Position identification (Inside/Outside/Faction)
  - Spoiling risk assessment for proposals
  - Management strategy recommendations:
    - Inducement
    - Socialization
    - Coercion
  - Comprehensive spoiler management plan generator
  - Escalation protocol for each spoiler

## Readability Fixes

All contrast issues have been resolved:

### Before (Problems):
- Light text (#ccc, #ddd) on light backgrounds
- Low contrast ratios (<3:1)
- Streamlit default info/warning boxes with poor contrast

### After (Solutions):
- **Dark text** (#000, #333) on ALL backgrounds
- **Custom CSS** with explicit color overrides
- **High contrast boxes**:
  - Info boxes: Light blue background (#E3F2FD) with dark text
  - Success boxes: Light green background (#E8F5E9) with dark text
  - Warning boxes: Light orange background (#FFF3E0) with dark text
  - Error boxes: Light red background (#FFEBEE) with dark text
- **Colored borders** for visual distinction without relying on text color
- **Metric cards** with dark text on light gray backgrounds
- **Escalation ladder** with color-coded backgrounds and dark text

### Accessibility:
- All text now meets WCAG AA standards (contrast ratio >4.5:1)
- Color is not the only indicator (borders, icons, labels also used)
- Clear visual hierarchy

## How to Run

### Prerequisites
```bash
# Make sure you're in the project directory
cd /home/dk/scs_mediator_sdk_v2

# Install dependencies (if not already installed)
pip install streamlit
```

### Launch the UI

#### Option 1: Run directly
```bash
streamlit run src/scs_mediator_sdk/ui/peace_mediation_ui.py
```

#### Option 2: Run from anywhere
```bash
cd /home/dk/scs_mediator_sdk_v2
python -m streamlit run src/scs_mediator_sdk/ui/peace_mediation_ui.py
```

### Access the UI
- The UI will automatically open in your browser
- Default URL: http://localhost:8501
- If port 8501 is busy, Streamlit will use the next available port

## User Workflow

### For Mediators

#### 1. Start with Escalation Assessment
- Check current escalation level
- Before proposing any action, assess its escalation risk
- Review de-escalation sequences if tensions are high

#### 2. Use CBM Recommendations
- Input current trust level and escalation level
- Get sequenced CBM recommendations
- Review implementation steps for each CBM
- Select CBMs that fit your timeline

#### 3. Test Domestic Acceptability
- Switch between Philippines and China analyzers
- Check win-set size to understand flexibility
- Test your proposal against domestic constraints
- Adjust proposal based on objectors and required compensations
- Get ratification strategy

#### 4. Coordinate Diplomatic Tracks
- Identify current conflict phase
- Get track-specific recommendations
- Ensure Track 1, 1.5, and 2 are coordinated
- Plan Track 3-9 activities for long-term peacebuilding

#### 5. Manage Spoilers
- Review identified spoilers
- Assess spoiling risk for your proposal
- Implement protective measures
- Generate comprehensive spoiler management plan

### For Instructors

#### Training Scenario Design
1. **Set up scenario context**:
   - Current escalation level
   - Trust level between parties
   - Identified spoilers
   - Domestic political landscape

2. **Run through assessment tools**:
   - Show students how to use each tool
   - Demonstrate risk assessment
   - Discuss trade-offs in recommendations

3. **Exercise: Proposal Development**:
   - Have students develop proposals
   - Test proposals against all 5 tools
   - Iterate based on feedback
   - Discuss why certain proposals fail domestic acceptability

4. **Debrief**:
   - Review escalation dynamics
   - Discuss CBM sequencing
   - Analyze domestic constraints
   - Evaluate spoiler management strategies

## Tool-by-Tool Guide

### Escalation Assessment

**Use Case**: You're considering a military escort for a resupply mission.

1. Select "📊 Escalation Assessment"
2. Check current escalation level (visual ladder)
3. Enter proposed action: "Deploy military escort for resupply mission"
4. Click "🔍 Assess Risk"
5. Review:
   - Risk level (Low/Moderate/High)
   - Likely counter-escalation
   - Available de-escalation options
   - Point of no return warning
6. If risk is high, review de-escalation sequence

**Key Insight**: Actions that seem reasonable may trigger escalation spirals. Always assess first.

### CBM Recommendations

**Use Case**: Trust is low, tensions are medium, you have 20 weeks to implement CBMs.

1. Select "🤝 CBM Recommendations"
2. Set sliders:
   - Trust level: 0.3 (Low)
   - Escalation level: 4 (Verbal warnings)
   - Available time: 20 weeks
3. Click "🔍 Get CBM Recommendations"
4. Review sequenced CBMs (typically 4-6)
5. For each CBM:
   - Read description
   - Check timeline and effectiveness
   - Expand to see implementation steps
6. Browse library by category for more options

**Key Insight**: Start with easy, low-cost communication CBMs before moving to cooperation CBMs.

### Domestic Politics Analysis

**Use Case**: Testing if Philippines can accept a fishing access compromise.

1. Select "🏛️ Domestic Politics"
2. Choose "Philippines"
3. Note win-set size (flexibility indicator)
4. Review deal breakers
5. Set sliders:
   - Fisheries Access: 0.6 (60% access)
   - Sovereignty Language: 0.5 (Moderate)
   - Bilateral Tensions: 0.3 (Low)
6. Click "🔍 Test Proposal"
7. Review:
   - Acceptable/Unacceptable verdict
   - Ratification probability
   - Domestic objectors
   - Required compensations
8. Read ratification strategy
9. Adjust proposal if needed

**Key Insight**: Proposals that look good to mediators often fail domestic ratification. Test early and often.

### Multi-Track Diplomacy

**Use Case**: Planning Track 2 dialogue before Track 1 negotiations.

1. Select "🌐 Multi-Track Diplomacy"
2. Choose phase: "Pre-negotiation"
3. Review recommended tracks (typically Track 2, 1.5, and 3)
4. For each track:
   - Note activity type
   - Identify participants
   - Understand purpose
   - Check timeline
5. Expand track overview to understand all 10 tracks
6. Review coordination mechanisms

**Key Insight**: Track 2 can explore options without official commitment. Use it to build relationships before Track 1.

### Spoiler Management

**Use Case**: Assessing if nationalist factions will undermine your agreement.

1. Select "⚠️ Spoiler Management"
2. Review identified spoilers (4 pre-loaded for SCS)
3. For each spoiler:
   - Check threat level (Low/Medium/High)
   - Expand to see detailed analysis
   - Review management strategies
4. Test your proposal:
   - Check/uncheck: Shared Resources, Monitoring, Demilitarization
   - Click "🔍 Assess Spoiling Risk"
5. Review:
   - Overall spoiling risk
   - High-threat spoilers
   - Likely spoiling actions
   - Protective measures needed
6. Click "📋 Generate Comprehensive Spoiler Management Plan"

**Key Insight**: Identify spoilers early and have management strategies ready. Some spoilers need inducement, others need coercion.

## Advanced Usage

### Integrating with Enhanced Multi-View UI

The Peace Mediation UI can be used alongside the existing Enhanced Multi-View UI:

1. **Enhanced Multi-View** (`enhanced_multi_view.py`):
   - Use for scenario setup
   - Build and evaluate offers
   - Run simulations
   - View party-specific information

2. **Peace Mediation UI** (`peace_mediation_ui.py`):
   - Use for deep analysis of proposals
   - CBM sequencing
   - Domestic acceptability testing
   - Spoiler management

**Workflow**:
1. Start in Enhanced Multi-View
2. Build an offer in Step 2
3. Switch to Peace Mediation UI
4. Test offer against all 5 tools
5. Return to Enhanced Multi-View
6. Refine offer based on insights
7. Evaluate and simulate

### Customization

#### Adding More Spoilers
Edit the `create_scs_spoilers()` function in `spoiler_management.py`:

```python
Spoiler(
    name="Your Spoiler Name",
    spoiler_type=SpoilerType.GREEDY,
    capability=SpoilerCapability.MEDIUM,
    position=SpoilerPosition.OUTSIDE,
    interests_threatened=["List", "interests"],
    benefits_from_conflict=["List", "benefits"],
    typical_spoiling_actions=["List", "actions"],
    dependencies=["List", "dependencies"],
    constituencies=["List", "supporters"],
    influence_on_parties={"Party": 0.3}
)
```

#### Adding More CBMs
Edit the `_initialize_scs_cbms()` method in `cbm_library.py`:

```python
self._add_cbm(ConfidenceBuildingMeasure(
    cbm_id="CBM_CUSTOM_001",
    name="Your CBM Name",
    category=CBMCategory.COOPERATION,
    description="Detailed description",
    prerequisites=["List prerequisites"],
    implementation_steps=["Step 1", "Step 2", ...],
    verification_method="How to verify",
    timeline_weeks=12,
    trust_building_value=0.6,
    risk_reduction_value=0.7,
    reversibility="moderate",
    cost_level="medium"
))
```

#### Adding More Domestic Actors
Edit `create_philippines_domestic_actors()` or `create_china_domestic_actors()` in `domestic_constraints.py`:

```python
DomesticConstraint(
    actor=DomesticActor.BUSINESS_INTERESTS,
    issue="Your Issue",
    position="Position description",
    intensity=0.7,
    mobilization_capacity=0.6,
    acceptable_range={"issue_name": (min_value, max_value)},
    pressure_tactics=["List tactics"]
)
```

## Troubleshooting

### UI doesn't load
- Check that all dependencies are installed: `pip install streamlit`
- Verify Python path includes the SDK: `export PYTHONPATH=/home/dk/scs_mediator_sdk_v2/src:$PYTHONPATH`
- Run from project root directory

### Import errors
```bash
# Make sure you're running from the correct directory
cd /home/dk/scs_mediator_sdk_v2
streamlit run src/scs_mediator_sdk/ui/peace_mediation_ui.py
```

### Text readability issues
- The custom CSS should override all Streamlit defaults
- If issues persist, check browser zoom level (100% recommended)
- Try hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

### Port already in use
```bash
# Use a different port
streamlit run src/scs_mediator_sdk/ui/peace_mediation_ui.py --server.port 8502
```

## Best Practices

### 1. Iterative Analysis
- Don't just test once
- Test multiple variations of your proposal
- Iterate based on feedback from all 5 tools

### 2. Tool Synergy
- Use escalation assessment to inform CBM selection
- Use domestic politics to validate CBM acceptability
- Use spoiler management to protect CBM implementation
- Use multi-track to coordinate all activities

### 3. Documentation
- Take screenshots of assessments
- Export results (copy/paste text)
- Track how proposals evolve based on tool feedback

### 4. Training
- Start with low-stakes scenarios
- Build complexity gradually
- Practice with all 5 tools before real negotiations

## Comparison: Before vs After

### Before (enhanced_multi_view.py)
- **Strengths**:
  - Great for scenario setup
  - Good for basic offer evaluation
  - Simulation integration
  - Party-specific views
- **Weaknesses**:
  - No escalation assessment
  - No CBM recommendations
  - No domestic politics analysis
  - No spoiler management
  - Readability issues (light text on light backgrounds)

### After (peace_mediation_ui.py)
- **New Capabilities**:
  - ✅ Escalation risk assessment with 9-level ladder
  - ✅ 15+ maritime-specific CBMs with sequencing
  - ✅ Two-level game domestic politics analysis
  - ✅ Multi-track diplomacy coordination
  - ✅ Comprehensive spoiler management
  - ✅ All text is dark (#000/#333) on light backgrounds
  - ✅ High contrast info/success/warning/error boxes
  - ✅ Visual indicators beyond just color

### Integration Strategy
Both UIs are complementary:
- **Enhanced Multi-View**: Broad workflow, scenario management, simulation
- **Peace Mediation UI**: Deep analysis, specialized tools, risk assessment

## Educational Use

### For Peace & Conflict Studies Courses

#### Week 1-2: Escalation Dynamics
- Teach Kahn's escalation ladder
- Use escalation assessment tool
- Exercise: Assess historical SCS incidents

#### Week 3-4: Confidence-Building
- Teach CBM theory
- Use CBM recommendation tool
- Exercise: Design CBM sequence for a scenario

#### Week 5-6: Domestic Politics
- Teach Putnam's two-level game
- Use domestic politics analyzer
- Exercise: Test proposals against domestic constraints

#### Week 7-8: Multi-Track Diplomacy
- Teach McDonald & Diamond framework
- Use multi-track coordinator
- Exercise: Design multi-track strategy

#### Week 9-10: Spoiler Management
- Teach Stedman's spoiler problem
- Use spoiler management tool
- Exercise: Identify and manage spoilers

### Assessment Ideas

1. **Proposal Development Assignment**:
   - Students develop a negotiation proposal
   - Must pass all 5 tool assessments
   - Written report explaining iterations

2. **Simulation Exercise**:
   - Role-play negotiation
   - Use tools in real-time to assess proposals
   - Debrief on tool effectiveness

3. **Case Study Analysis**:
   - Analyze historical peace process
   - Apply tools retroactively
   - Identify missed opportunities

## Future Enhancements

Potential additions (not yet implemented):

1. **Data Export**:
   - Export assessments to PDF/CSV
   - Share results with team

2. **Historical Tracking**:
   - Track proposal evolution over time
   - Compare iterations

3. **Scenario Presets**:
   - Pre-load common scenarios
   - Quick start templates

4. **Integration with Main UI**:
   - Direct links between UIs
   - Shared session state

5. **Advanced Analytics**:
   - Aggregate tool results
   - Overall proposal score
   - Risk dashboard

## Contact & Support

For questions, issues, or enhancements:
- Check module documentation in source files
- Review theory references in module docstrings
- Consult academic literature cited in modules

## References

### Academic Foundations

1. **Escalation Ladder**: Kahn, H. (1965). *On Escalation: Metaphors and Scenarios*
2. **GRIT**: Osgood, C. (1962). *An Alternative to War or Surrender*
3. **CBMs**: Confidence-building measures in conflict resolution
4. **Two-Level Games**: Putnam, R. (1988). *Diplomacy and domestic politics*
5. **Multi-Track**: McDonald, J. & Diamond, L. (1996). *Multi-Track Diplomacy*
6. **Spoiler Problem**: Stedman, S. (1997). *Spoiler Problems in Peace Processes*

### Maritime Conflict Specific

- UNCLOS (UN Convention on the Law of the Sea)
- CUES (Code for Unplanned Encounters at Sea)
- ASEAN conflict management frameworks
- South China Sea dispute literature

---

**Version**: 1.0
**Date**: 2025-11-03
**Author**: SCS Mediator SDK v2 Team
