# 🕊️ Advanced Mediation Simulation Tool

**Version 9.0** - A comprehensive training platform for conflict mediators and peacemakers

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 What is This?

An **advanced simulation tool** that combines game theory, agent-based modeling, and mediation best practices to train conflict mediators. Based on research from Christopher Moore, Fisher & Ury, UN DPPA, and leading conflict resolution scholars.

### Key Features

✅ **Moore's 6-Phase Mediation Process** - Systematic framework from initial contact to implementation
✅ **Advanced Game Theory** - MAUT, Prospect Theory, BATNA, Nash Equilibrium, Pareto Efficiency
✅ **Agent-Based Modeling** - Realistic conflict dynamics with BDI architecture
✅ **Generalized Framework** - Support for maritime, territorial, resource, political, and ethnic conflicts
✅ **Learning Analytics** - Track progress, receive personalized feedback, unlock achievements
✅ **Mediator Toolkit** - 17 evidence-based interventions with implementation guides
✅ **User-Friendly UI** - Interactive process navigation for non-technical users

---

## 🚀 Quick Start

### Installation (2 minutes)

```bash
# Clone and install
git clone https://github.com/your-org/scs_mediator_sdk.git
cd scs_mediator_sdk
pip install -e .
```

### Run Your First Simulation (3 minutes)

```bash
# Terminal 1: Start API
uvicorn src.scs_mediator_sdk.api.server:app --reload

# Terminal 2: Start Enhanced UI
streamlit run src/scs_mediator_sdk/ui/enhanced_app.py
```

Open `http://localhost:8501` and follow the guided process!

**📖 Full Guide**: [docs/QUICK_START.md](docs/QUICK_START.md)

---

## 🎓 Who Should Use This?

- **Conflict Mediators** - Learn systematic mediation approaches
- **Trainers & Facilitators** - Run engaging workshops and War Room exercises
- **Students** - Practice negotiation in conflict resolution programs
- **Researchers** - Study negotiation dynamics and validate theories
- **Diplomats** - Prepare for real-world negotiations

---

## 📚 What's Included

### Core Modules

```
scs_mediator_sdk/
├── mediation/              # Moore's 6-Phase Process
│   ├── process/           # Phases 1-6 implementation
│   └── interventions/     # 17 evidence-based interventions
├── engines/               # Game theory engines
│   ├── enhanced_bargaining.py  # MAUT, Prospect Theory, BATNA
│   └── ...
├── sim/                   # Agent-based modeling
│   └── enhanced_abm.py    # BDI agents, escalation dynamics
├── scenarios/             # Generalization framework
│   └── templates/         # Domain-agnostic scenario builder
├── analytics/             # Learning analytics
│   ├── process_quality.py    # How well you mediated
│   ├── outcome_quality.py    # What you achieved
│   └── learning_tracker.py   # Progress over time
└── ui/                    # User interfaces
    ├── enhanced_app.py    # Full-featured UI with process navigation
    └── streamlit_app.py   # Original UI (backward compatible)
```

### Pre-built Scenarios (15 total)

**Maritime (4)**
- Second Thomas Shoal Resupply
- Scarborough Shoal Fisheries
- Kasawari Gas Field
- Natuna Islands

**Territorial (3)**
- India-Pakistan Kashmir
- Ethiopia-Eritrea Border
- Cyprus Reunification

**Resource (3)**
- Nile River Water
- Arctic Oil
- Amazon Conservation

**Political (3)**
- Yemen Power-Sharing
- Myanmar Federalism
- Venezuela Transition

**Ethnic (2)**
- Rohingya Refugees
- Nagorno-Karabakh

---

## 🎯 Key Capabilities

### 1. Systematic Mediation Process

Follow **Moore's research-based 6-phase framework**:

1. **Initial Contact** - Build trust, assess ripeness
2. **Conflict Analysis** - Understand positions vs. interests
3. **Agenda Setting** - Reframe and sequence issues
4. **Option Generation** - Create value before claiming it
5. **Bargaining** - Negotiate with game theory support
6. **Implementation** - Monitor and ensure compliance

### 2. Advanced Game Theory

**Multi-Attribute Utility Theory (MAUT)**
- Non-linear value functions
- Attribute interactions and synergies
- Satiation points

**Prospect Theory**
- Loss aversion (λ = 2.25)
- Reference dependence
- Framing effects (gain vs. loss frames)

**BATNA & Nash Analysis**
- Dynamic reservation points
- Zone of Possible Agreement (ZOPA)
- Pareto efficiency assessment
- Nash bargaining solution

### 3. Realistic Simulation

**BDI Agent Architecture**
- Beliefs (about environment and others)
- Desires (goals)
- Intentions (committed actions)

**Emergent Dynamics**
- Escalation spirals
- Contagion effects
- Tipping points
- Path dependence

**Domain-Specific Incidents**
- Maritime: water cannon, ramming, detention
- Territorial: border crossings, skirmishes
- Resource: unauthorized extraction, sabotage

### 4. Learning Analytics

**Process Quality Metrics**
- Intervention timing
- Strategy appropriateness
- Phase completion
- Power balancing
- Cultural sensitivity

**Outcome Quality Metrics**
- Pareto efficiency
- Fairness
- Durability
- Feasibility
- Sustainability

**Progress Tracking**
- Concept mastery (novice → intermediate → expert)
- Trend analysis (improving/stable/declining)
- Personalized recommendations
- Achievement unlocks

---

## 💡 Example Usage

### Python API

```python
from scs_mediator_sdk.engines.enhanced_bargaining import BargainingEngine, Party, Attribute, AgreementVector

# Create engine
engine = BargainingEngine()

# Define parties
party_a = Party(
    party_id="country_a",
    name="Country A",
    batna_value=0.3,
    loss_aversion=2.25
)
party_a.attributes["security"] = Attribute(name="security", weight=1.0)
engine.add_party(party_a)

# Evaluate offer
agreement = AgreementVector({"security_provisions": {"level": 0.7}})
results = engine.evaluate_offer("country_a", agreement)

print(f"Utilities: {results['utilities']}")
print(f"Acceptance: {results['acceptance_probabilities']}")
print(f"ZOPA Exists: {results['analysis']['zopa_exists']}")
```

### Mediation Process

```python
from scs_mediator_sdk.mediation.process import PreMediationAssessment, Stakeholder

# Phase 1-2: Assessment
assessment = PreMediationAssessment("Border Dispute")

stakeholder = Stakeholder(
    name="Country A",
    power_level=0.7,
    stated_positions=["Must control territory"],
    underlying_interests=["Security", "Resources", "National pride"]
)
assessment.add_stakeholder(stakeholder)

# Assess ripeness
ripeness = assessment.conduct_ripeness_assessment()
print(f"Readiness: {ripeness.overall_readiness.value}")
print(f"Score: {ripeness.calculate_readiness_score():.2f}")
```

### Scenario Creation

```python
from scs_mediator_sdk.scenarios import ScenarioBuilder, ConflictDomain

scenario = (ScenarioBuilder("custom_001", "Water Dispute", "River allocation conflict", ConflictDomain.RESOURCE)
    .add_party("upstream", "Upstream Country", "government", power_level=0.8)
    .add_party("downstream", "Downstream Country", "government", power_level=0.6)
    .add_issue("allocation", "Water Allocation", "How to split river water", "numeric")
    .set_difficulty("intermediate")
    .build())

scenario.to_json("scenarios/custom/water_dispute.json")
```

---

## 📊 Research Foundation

Built on peer-reviewed research:

### Mediation Process
- **Moore (2014)**: *The Mediation Process* - 6-phase framework
- **UN DPPA (2017)**: *Guidance for Effective Mediation*
- **Zartman & Touval (1985)**: Ripeness theory

### Game Theory
- **Raiffa (1982)**: *The Art and Science of Negotiation*
- **Fisher & Ury (1981)**: *Getting to Yes* - BATNA
- **Kahneman & Tversky (1979)**: Prospect Theory
- **Nash (1950)**: Bargaining theory

### Agent-Based Modeling
- **Epstein (1999)**: Agent-based computational models
- **Cederman (2003)**: Modeling conflict dynamics
- **Rao & Georgeff (1995)**: BDI architecture

---

## 🗺️ Roadmap

### ✅ Version 9.0 (Current)
- Moore's 6-phase process implementation
- Enhanced bargaining with Prospect Theory
- Generalization framework
- Learning analytics
- Enhanced UI with process navigation

### 🚧 Version 9.1 (Next - Q1 2026)
- Phase 5-6 enhancements (bargaining refinements)
- Advanced visualization dashboards
- Multi-language support
- Mobile-responsive UI

### 🔮 Version 10.0 (Future - Q2 2026)
- Real-time collaborative features (War Room mode)
- VR/AR integration for immersive training
- AI-powered mediator coach
- Scenario marketplace

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas we need help with:**
- Additional scenario templates
- Translations
- Documentation improvements
- Bug reports and feature requests

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 📞 Support

- **Documentation**: [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
- **Quick Start**: [docs/QUICK_START.md](docs/QUICK_START.md)
- **API Docs**: http://localhost:8000/docs (when server running)
- **Issues**: [GitHub Issues](https://github.com/your-org/scs_mediator_sdk/issues)

---

## 🙏 Acknowledgments

This tool builds on decades of conflict resolution research and practice. Special thanks to:

- Christopher Moore for the mediation process framework
- Roger Fisher & William Ury for negotiation principles
- UN DPPA for mediation guidance
- The agent-based modeling community
- All contributors and users

---

## 📈 Stats

- **Version**: 9.0.0
- **Code**: 8,000+ lines
- **Modules**: 15+
- **Scenarios**: 15 pre-built
- **Interventions**: 17 evidence-based
- **Documentation**: 100+ pages

---

**Ready to get started?** → [Quick Start Guide](docs/QUICK_START.md)

**Need help?** → [User Guide](docs/USER_GUIDE.md)

**Want to contribute?** → [Contributing Guide](CONTRIBUTING.md)
