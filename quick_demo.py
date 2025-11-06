#!/usr/bin/env python3
"""
Quick Demo using ORIGINAL working modules
"""

import json
import sys
sys.path.insert(0, 'src')

# Use ORIGINAL working modules (not enhanced ones that need numpy)
from scs_mediator_sdk.engines.bargaining_engine import BargainingSession, AgreementVector
from scs_mediator_sdk.sim.mesa_abm import MaritimeModel

print("=" * 70)
print("🌊 SCS SIMULATION - WORKING DEMO")
print("=" * 70)
print()

# Load Second Thomas Shoal scenario
with open('cases/scs/scenario_A_second_thomas.json', 'r') as f:
    scenario = json.load(f)

print(f"📍 Scenario: {scenario['flashpoint']}")
print(f"   ID: {scenario['id']}")
print(f"   Focus: {scenario['focus']}")
print(f"   Weather: {scenario['weather_state']}")
print(f"   Media Visibility: {scenario['media_visibility']}/3")
print()

# Create bargaining session
print("🤝 Creating Bargaining Session...")
session = BargainingSession.start(
    case_id=scenario['id'],
    parties=['PH_GOV', 'PRC_MARITIME'],
    mediator='ASEAN_Facilitator',
    issue_space=['resupply_SOP', 'hotline_cues', 'media_protocol']
)
print(f"   ✓ Session created with {len(session.parties)} parties")
print()

# Create agreement proposal
print("📝 Agreement Proposal:")
agreement = AgreementVector({
    "resupply_SOP": {
        "standoff_nm": 3,
        "escort_count": 1,
        "pre_notification_hours": 12
    },
    "hotline_cues": {
        "hotline_status": "24_7"
    },
    "media_protocol": {
        "embargo_hours": 6
    }
})

for issue, terms in agreement.to_dict().items():
    print(f"   • {issue}: {terms}")
print()

# Evaluate offer
print("🎲 Evaluating Offer...")
result = session.evaluate_offer('PH_GOV', agreement)

print("\n📊 RESULTS:")
print()
print("Utilities (0-1 scale):")
for party, utility in result['utilities'].items():
    bar = "█" * int(utility * 20)
    print(f"   {party:20s} {utility:.3f} {bar}")

print()
print("Acceptance Probabilities:")
for party, prob in result['acceptance_prob'].items():
    status = "✅" if prob > 0.7 else "⚠️" if prob > 0.5 else "❌"
    bar = "█" * int(prob * 20)
    print(f"   {party:20s} {prob:.3f} {bar} {status}")

# Calculate overall acceptance
import numpy as np
overall = np.prod(list(result['acceptance_prob'].values()))
print()
print(f"Overall Agreement Probability: {overall:.1%}")
print()

# Run ABM simulation
print("🎮 Running Maritime Simulation (300 steps)...")
model = MaritimeModel(
    steps=300,
    environment={
        'weather_state': scenario['weather_state'],
        'media_visibility': scenario['media_visibility']
    },
    agreement=agreement.to_dict()
)

df = model.run()

print()
print("📈 SIMULATION RESULTS:")
if not df.empty:
    print(f"   Total Incidents: {len(df)}")
    print(f"   Avg Severity: {df['severity'].mean():.2f}/1.0")
    print(f"   Max Severity: {df['severity'].max():.2f}/1.0")
    print()
    print("   Top Incident Types:")
    for itype, count in df['incident_type'].value_counts().head(3).items():
        print(f"      • {itype}: {count} times")

    # Trend
    early = len(df[df['step'] < 100])
    late = len(df[df['step'] >= 200])
    if late < early * 0.8:
        print(f"\n   Trend: ✅ Declining ({early}→{late}) - Agreement working!")
    elif late > early * 1.2:
        print(f"\n   Trend: ❌ Escalating ({early}→{late}) - Agreement failing")
    else:
        print(f"\n   Trend: ➡️ Stable ({early}→{late})")
else:
    print("   ✅ NO INCIDENTS - Perfect deterrence!")

print()
print("=" * 70)
print("✅ DEMO COMPLETE")
print("=" * 70)
print()
print("💡 Next Steps:")
print("   1. Start API: uvicorn src.scs_mediator_sdk.api.server:app --reload")
print("   2. Start UI:  streamlit run src/scs_mediator_sdk/ui/streamlit_app.py")
print("   3. Try all 4 scenarios (A, B, C, D)")
print()
