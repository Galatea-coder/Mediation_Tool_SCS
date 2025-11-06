"""
Confidence-Building Measures (CBMs) Library for Maritime Conflicts

This module provides a comprehensive library of maritime-specific CBMs
for South China Sea scenarios, with sequencing and effectiveness tracking.

Part 2 of 10 Peace Mediation Enhancements.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict


class CBMCategory(Enum):
    """Types of confidence-building measures"""
    COMMUNICATION = "communication"           # Hotlines, protocols
    TRANSPARENCY = "transparency"             # Information sharing, notifications
    CONSTRAINTS = "constraints"               # Voluntary restrictions
    VERIFICATION = "verification"             # Monitoring, inspection
    COOPERATION = "cooperation"               # Joint activities
    SYMBOLIC = "symbolic"                     # Gestures, acknowledgments


@dataclass
class ConfidenceBuildingMeasure:
    """A specific CBM with implementation details"""
    cbm_id: str
    name: str
    category: CBMCategory
    description: str

    # Implementation
    prerequisites: List[str] = field(default_factory=list)
    implementation_steps: List[str] = field(default_factory=list)
    verification_method: str = ""
    timeline_weeks: int = 0

    # Effectiveness
    trust_building_value: float = 0.5  # 0-1
    risk_reduction_value: float = 0.5  # 0-1
    reversibility: str = "easy"  # easy, moderate, difficult
    cost_level: str = "low"  # low, medium, high

    # Political viability
    domestic_acceptability: Dict[str, float] = field(default_factory=dict)  # party -> acceptance
    face_impact: Dict[str, float] = field(default_factory=dict)  # party -> face concern


class CBMLibrary:
    """Library of maritime CBMs for SCS scenarios"""

    def __init__(self):
        self.cbms: Dict[str, ConfidenceBuildingMeasure] = {}
        self._initialize_scs_cbms()

    def _initialize_scs_cbms(self):
        """Load SCS-specific CBMs"""

        # COMMUNICATION CBMs
        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_COMM_001",
            name="Maritime Incident Hotline",
            category=CBMCategory.COMMUNICATION,
            description="24/7 direct communication line between coast guard/navy command centers",
            prerequisites=["Agreement on hotline protocol", "Designated focal points"],
            implementation_steps=[
                "Designate 24/7 duty officers",
                "Establish secure communication channels",
                "Conduct test calls weekly",
                "Develop standard operating procedures",
                "Train personnel on protocols"
            ],
            verification_method="Regular test calls, incident response logs",
            timeline_weeks=4,
            trust_building_value=0.6,
            risk_reduction_value=0.7,
            reversibility="easy",
            cost_level="low"
        ))

        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_COMM_002",
            name="Code for Unplanned Encounters at Sea (CUES)",
            category=CBMCategory.COMMUNICATION,
            description="Standardized signals and procedures for vessel encounters",
            prerequisites=["Training of all maritime personnel"],
            implementation_steps=[
                "Adopt CUES protocol",
                "Translate to all relevant languages",
                "Train coast guard and naval personnel",
                "Display CUES cards on all vessels",
                "Conduct joint CUES exercises"
            ],
            verification_method="Joint exercises, incident reviews",
            timeline_weeks=12,
            trust_building_value=0.5,
            risk_reduction_value=0.6,
            reversibility="easy",
            cost_level="low"
        ))

        # TRANSPARENCY CBMs
        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_TRANS_001",
            name="Pre-Notification of Major Activities",
            category=CBMCategory.TRANSPARENCY,
            description="24-48 hour advance notice of resupply missions, exercises, or large-scale operations",
            prerequisites=["Agreement on notification format", "Communication channels"],
            implementation_steps=[
                "Define 'major activities' requiring notification",
                "Establish notification timeline (24-48 hrs)",
                "Create standard notification format",
                "Set up notification system",
                "Conduct trial notifications"
            ],
            verification_method="Notification logs, compliance monitoring",
            timeline_weeks=8,
            trust_building_value=0.7,
            risk_reduction_value=0.8,
            reversibility="moderate",
            cost_level="low"
        ))

        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_TRANS_002",
            name="AIS Transparency Cell",
            category=CBMCategory.TRANSPARENCY,
            description="Shared maritime domain awareness through AIS data exchange",
            prerequisites=["AIS mandate for all large vessels", "Data sharing agreement"],
            implementation_steps=[
                "Require AIS on all vessels >300 tons",
                "Establish joint AIS monitoring center",
                "Share track data in near-real-time",
                "Create common operational picture",
                "Use for incident prevention"
            ],
            verification_method="AIS coverage reports, data quality audits",
            timeline_weeks=16,
            trust_building_value=0.6,
            risk_reduction_value=0.7,
            reversibility="moderate",
            cost_level="medium"
        ))

        # CONSTRAINTS CBMs
        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_CONST_001",
            name="Standoff Distance Agreement",
            category=CBMCategory.CONSTRAINTS,
            description="Voluntary minimum separation distances during patrols",
            prerequisites=["Definition of operational areas", "Exception procedures"],
            implementation_steps=[
                "Agree on standoff distance (e.g., 3 nautical miles)",
                "Define exceptions (distress, pursuit)",
                "Train personnel on compliance",
                "Monitor through AIS and observation",
                "Report violations through hotline"
            ],
            verification_method="AIS tracking, mutual observation, incident reports",
            timeline_weeks=6,
            trust_building_value=0.5,
            risk_reduction_value=0.8,
            reversibility="easy",
            cost_level="low"
        ))

        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_CONST_002",
            name="Weapons Restraint Protocol",
            category=CBMCategory.CONSTRAINTS,
            description="Agreement not to point weapons or use fire control radar except in self-defense",
            prerequisites=["Clear rules of engagement", "Training"],
            implementation_steps=[
                "Define prohibited actions",
                "Establish self-defense exceptions",
                "Update rules of engagement",
                "Train all personnel",
                "Establish reporting mechanism for violations"
            ],
            verification_method="Incident reports, radar monitoring",
            timeline_weeks=8,
            trust_building_value=0.7,
            risk_reduction_value=0.9,
            reversibility="easy",
            cost_level="low"
        ))

        # VERIFICATION CBMs
        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_VERIF_001",
            name="Joint Fact-Finding Mechanism",
            category=CBMCategory.VERIFICATION,
            description="Rapid investigation of incidents by joint team within 48 hours",
            prerequisites=["Agreement on investigation procedures", "Trained investigators"],
            implementation_steps=[
                "Establish joint investigation team",
                "Develop investigation protocol",
                "Set 48-hour response timeline",
                "Create evidence standards",
                "Agree on report format"
            ],
            verification_method="Investigation reports, response time tracking",
            timeline_weeks=10,
            trust_building_value=0.8,
            risk_reduction_value=0.7,
            reversibility="moderate",
            cost_level="medium"
        ))

        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_VERIF_002",
            name="Third-Party Monitoring",
            category=CBMCategory.VERIFICATION,
            description="ASEAN or UN observers present in disputed areas",
            prerequisites=["Third-party agreement to monitor", "Access permissions"],
            implementation_steps=[
                "Identify acceptable third-party (ASEAN, UN, NGO)",
                "Negotiate observer mandate",
                "Provide access to disputed areas",
                "Establish reporting procedures",
                "Fund monitoring operations"
            ],
            verification_method="Observer reports, transparency",
            timeline_weeks=20,
            trust_building_value=0.7,
            risk_reduction_value=0.8,
            reversibility="difficult",
            cost_level="high"
        ))

        # COOPERATION CBMs
        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_COOP_001",
            name="Joint Marine Scientific Research",
            category=CBMCategory.COOPERATION,
            description="Collaborative oceanographic, fisheries, or environmental studies",
            prerequisites=["Scientific cooperation agreement", "Funding"],
            implementation_steps=[
                "Identify research topics of mutual interest",
                "Form joint research teams",
                "Conduct field work together",
                "Share data and findings",
                "Publish joint reports"
            ],
            verification_method="Research outputs, publications",
            timeline_weeks=52,  # Long-term
            trust_building_value=0.6,
            risk_reduction_value=0.5,
            reversibility="moderate",
            cost_level="medium"
        ))

        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_COOP_002",
            name="Joint Search and Rescue (SAR) Exercises",
            category=CBMCategory.COOPERATION,
            description="Regular joint exercises for maritime emergencies",
            prerequisites=["SAR cooperation agreement"],
            implementation_steps=[
                "Agree on exercise scenarios",
                "Conduct quarterly joint SAR drills",
                "Share best practices",
                "Develop common procedures",
                "Build personal relationships"
            ],
            verification_method="Exercise reports, lessons learned",
            timeline_weeks=16,
            trust_building_value=0.7,
            risk_reduction_value=0.6,
            reversibility="easy",
            cost_level="low"
        ))

        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_COOP_003",
            name="Fisheries Management Cooperation",
            category=CBMCategory.COOPERATION,
            description="Joint management of fish stocks in disputed waters",
            prerequisites=["Scientific baseline data", "Enforcement cooperation"],
            implementation_steps=[
                "Conduct joint stock assessments",
                "Set sustainable catch limits",
                "Share fishing zone access",
                "Cooperate on enforcement",
                "Establish joint management body"
            ],
            verification_method="Stock health, compliance data",
            timeline_weeks=40,
            trust_building_value=0.8,
            risk_reduction_value=0.7,
            reversibility="moderate",
            cost_level="medium"
        ))

        # SYMBOLIC CBMs
        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_SYMB_001",
            name="High-Level Mutual Visit",
            category=CBMCategory.SYMBOLIC,
            description="Exchange visits by defense ministers or coast guard commanders",
            prerequisites=["Political willingness", "Domestic preparation"],
            implementation_steps=[
                "Arrange visit schedule",
                "Prepare domestic audiences",
                "Conduct visit with honors",
                "Issue joint statement",
                "Follow up with working-level contacts"
            ],
            verification_method="Media coverage, public statements",
            timeline_weeks=8,
            trust_building_value=0.6,
            risk_reduction_value=0.3,
            reversibility="easy",
            cost_level="low"
        ))

        self._add_cbm(ConfidenceBuildingMeasure(
            cbm_id="CBM_SYMB_002",
            name="Joint Commemoration",
            category=CBMCategory.SYMBOLIC,
            description="Joint ceremony for maritime disaster victims or shared history",
            prerequisites=["Identification of appropriate occasion"],
            implementation_steps=[
                "Select commemorative event",
                "Plan joint ceremony",
                "Invite both countries' representatives",
                "Issue joint statement of shared values",
                "Use for positive media coverage"
            ],
            verification_method="Public participation, media coverage",
            timeline_weeks=12,
            trust_building_value=0.5,
            risk_reduction_value=0.2,
            reversibility="easy",
            cost_level="low"
        ))

    def _add_cbm(self, cbm: ConfidenceBuildingMeasure):
        """Add CBM to library"""
        self.cbms[cbm.cbm_id] = cbm

    def recommend_cbm_sequence(self,
                                current_trust_level: float,
                                escalation_level: int,
                                available_time_weeks: int) -> List[ConfidenceBuildingMeasure]:
        """
        Recommend sequenced CBMs based on situation

        Principles:
        - Start with easy, low-cost, high-trust CBMs
        - Build from communication to cooperation
        - Match to available time

        Args:
            current_trust_level: Current trust between parties (0-1)
            escalation_level: Current escalation level (1-9)
            available_time_weeks: Time available for implementation

        Returns:
            List of recommended CBMs in sequence
        """
        recommendations = []

        # Phase 1: Communication (Weeks 1-8)
        if current_trust_level < 0.5:
            recommendations.append(self.cbms["CBM_COMM_001"])  # Hotline
            if available_time_weeks >= 12:
                recommendations.append(self.cbms["CBM_COMM_002"])  # CUES

        # Phase 2: Transparency (Weeks 4-16)
        if current_trust_level >= 0.3:
            recommendations.append(self.cbms["CBM_TRANS_001"])  # Pre-notification
            if available_time_weeks >= 16:
                recommendations.append(self.cbms["CBM_TRANS_002"])  # AIS

        # Phase 3: Constraints (Weeks 6-14)
        if escalation_level >= 3:  # Close encounters or higher
            recommendations.append(self.cbms["CBM_CONST_001"])  # Standoff
            recommendations.append(self.cbms["CBM_CONST_002"])  # Weapons restraint

        # Phase 4: Verification (Weeks 10-20)
        if current_trust_level >= 0.5:
            recommendations.append(self.cbms["CBM_VERIF_001"])  # Joint fact-finding

        # Phase 5: Cooperation (Weeks 16+)
        if current_trust_level >= 0.6 and available_time_weeks >= 16:
            recommendations.append(self.cbms["CBM_COOP_002"])  # SAR exercises
            if available_time_weeks >= 40:
                recommendations.append(self.cbms["CBM_COOP_003"])  # Fisheries

        # Filter by timeline
        recommendations = [cbm for cbm in recommendations if cbm.timeline_weeks <= available_time_weeks]

        return recommendations

    def assess_cbm_package(self, cbm_ids: List[str]) -> Dict:
        """
        Assess a package of CBMs for effectiveness and feasibility

        Args:
            cbm_ids: List of CBM IDs to assess

        Returns:
            Dictionary with assessment metrics
        """
        assessment = {
            "total_trust_building": 0.0,
            "total_risk_reduction": 0.0,
            "total_cost": 0,
            "total_timeline_weeks": 0,
            "political_viability": {},
            "implementation_challenges": []
        }

        for cbm_id in cbm_ids:
            if cbm_id in self.cbms:
                cbm = self.cbms[cbm_id]
                assessment["total_trust_building"] += cbm.trust_building_value
                assessment["total_risk_reduction"] += cbm.risk_reduction_value
                assessment["total_timeline_weeks"] = max(
                    assessment["total_timeline_weeks"],
                    cbm.timeline_weeks
                )

                # Check prerequisites
                if cbm.prerequisites:
                    assessment["implementation_challenges"].extend(cbm.prerequisites)

        # Normalize
        if cbm_ids:
            assessment["total_trust_building"] /= len(cbm_ids)
            assessment["total_risk_reduction"] /= len(cbm_ids)

        return assessment

    def get_cbms_by_category(self, category: CBMCategory) -> List[ConfidenceBuildingMeasure]:
        """Get all CBMs of specific category"""
        return [cbm for cbm in self.cbms.values() if cbm.category == category]


# Example usage
if __name__ == "__main__":
    # Create CBM library
    library = CBMLibrary()

    print(f"Total CBMs loaded: {len(library.cbms)}")
    print("\nCBMs by Category:")
    for category in CBMCategory:
        cbms = library.get_cbms_by_category(category)
        print(f"  {category.value}: {len(cbms)} CBMs")

    # Get recommendations
    print("\nRecommended CBM Sequence for Low Trust Scenario:")
    recommendations = library.recommend_cbm_sequence(
        current_trust_level=0.3,
        escalation_level=4,
        available_time_weeks=20
    )

    for i, cbm in enumerate(recommendations, 1):
        print(f"\n{i}. {cbm.name} ({cbm.cbm_id})")
        print(f"   Category: {cbm.category.value}")
        print(f"   Timeline: {cbm.timeline_weeks} weeks")
        print(f"   Trust Building: {cbm.trust_building_value:.1f}")
        print(f"   Risk Reduction: {cbm.risk_reduction_value:.1f}")

    # Assess a CBM package
    print("\nAssessing CBM Package:")
    package = ["CBM_COMM_001", "CBM_TRANS_001", "CBM_CONST_001"]
    assessment = library.assess_cbm_package(package)
    print(f"  Average Trust Building: {assessment['total_trust_building']:.2f}")
    print(f"  Average Risk Reduction: {assessment['total_risk_reduction']:.2f}")
    print(f"  Total Timeline: {assessment['total_timeline_weeks']} weeks")
