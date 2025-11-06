#!/usr/bin/env python3
"""
Quick test of SCS simulation with enhanced framework
"""

import json
import sys
sys.path.insert(0, 'src')

from scs_mediator_sdk.engines.enhanced_bargaining import BargainingEngine, Party, Attribute, AgreementVector
from scs_mediator_sdk.sim.enhanced_abm import MaritimeModel, ConflictSimulation

print("=" * 60)
print("SCS SIMULATION TEST - Second Thomas Shoal Scenario")
print("=" * 60)
print()

# Load scenario
with open('cases/scs/scenario_A_second_thomas.json', 'r') as f:
    scenario = json.load(f)

print(f"📋 Scenario: {scenario['flashpoint']}")
print(f"   Focus: {scenario['focus']}")
print(f"   Weather: {scenario['weather_state']}")
print(f"   Media: {scenario['media_visibility']}")
print()

# Setup bargaining
print("🎲 Setting up enhanced bargaining engine...")
engine = BargainingEngine()

# Add parties
parties_config = {
    'PH_GOV': {'name': 'Philippines Government', 'batna': 0.25},
    'PRC_MARITIME': {'name': 'PRC Maritime Forces', 'batna': 0.30}
}

for party_id, config in parties_config.items():
    party = Party(
        party_id=party_id,
        name=config['name'],
        batna_value=config['batna'],
        loss_aversion=2.25  # Prospect Theory
    )

    # Add attributes
    for attr in ['safety', 'face', 'ops_access', 'verification']:
        party.attributes[attr] = Attribute(
            name=attr,
            weight=1.0,
            min_value=0.0,
            max_value=1.0,
            reference_point=0.3,
            aspiration_level=0.8
        )

    engine.add_party(party)

print(f"   ✓ Added {len(engine.parties)} parties with MAUT + Prospect Theory")
print()

# Create agreement proposal
print("📝 Proposed Agreement:")
agreement_offer = {
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

for key, value in agreement_offer.items():
    print(f"   • {key}: {value}")
print()

# Evaluate with enhanced engine
print("🔍 Evaluating with Enhanced Game Theory Engine...")
agreement = AgreementVector(agreement_offer)
results = engine.evaluate_offer('PH_GOV', agreement)

print(f"\n📊 BARGAINING RESULTS:")
print(f"   Round: {results['round']}")
print()
print("   Utilities:")
for party, utility in results['utilities'].items():
    threshold = results['batna_thresholds'][party]
    surplus = results['surplus'][party]
    print(f"      {party}: {utility:.2%} (BATNA: {threshold:.2%}, Surplus: {surplus:+.2%})")

print()
print("   Acceptance Probabilities:")
for party, prob in results['acceptance_probabilities'].items():
    status = "✅ Likely" if prob > 0.7 else "⚠️ Uncertain" if prob > 0.5 else "❌ Unlikely"
    print(f"      {party}: {prob:.1%} {status}")

print()
print(f"   Overall Agreement Chance: {results['overall_acceptance_probability']:.1%}")
print(f"   ZOPA Exists: {'✅ Yes' if results['analysis']['zopa_exists'] else '❌ No'}")
print(f"   Nash Product: {results['analysis']['nash_product']:.3f}")
print()

# Run ABM simulation
print("🎮 Running Agent-Based Simulation...")
print("   (Testing agreement durability over 300 steps)")

sim = ConflictSimulation(
    steps=300,
    domain="maritime",
    environment={
        'weather_bad': scenario['weather_state'] == 'rough',
        'media_visibility': scenario['media_visibility']
    },
    agreement=agreement_offer
)

df = sim.run()

print()
print("📈 SIMULATION RESULTS:")
if not df.empty:
    print(f"   Total Incidents: {len(df)}")
    print(f"   Average Severity: {df['severity'].mean():.2f}")
    print(f"   Max Severity: {df['severity'].max():.2f}")

    # Trend analysis
    early_incidents = len(df[df['step'] < 100])
    late_incidents = len(df[df['step'] >= 200])

    if late_incidents < early_incidents:
        trend = "✅ Declining (Agreement Working!)"
    elif late_incidents > early_incidents * 1.2:
        trend = "❌ Escalating (Agreement Failing)"
    else:
        trend = "➡️ Stable"

    print(f"   Trend: {trend}")
    print()
    print("   Incident Types:")
    for itype, count in df['incident_type'].value_counts().head(3).items():
        print(f"      • {itype}: {count}")
else:
    print("   ✅ NO INCIDENTS - Perfect Agreement!")

print()
print("=" * 60)
print("✅ SCS SIMULATION COMPLETE")
print("=" * 60)
print()
print("💡 To run interactively:")
print("   streamlit run src/scs_mediator_sdk/ui/streamlit_app.py")
print("   OR")
print("   streamlit run src/scs_mediator_sdk/ui/enhanced_app.py")
