from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List
import numpy as np

@dataclass
class AgreementVector:
    issues: Dict[str, Dict[str, Any]]
    def to_dict(self): return self.issues

def _extract_features(issues: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
    feats = {"safety":0.5,"face":0.5,"ops_access":0.5,"verification":0.5}
    if "resupply_SOP" in issues:
        rs = issues["resupply_SOP"]
        feats["safety"] += min(0.15, rs.get("standoff_nm",0)*0.02 + rs.get("escort_count",0)*0.01)
        if rs.get("pre_notification_hours",0) >= 12: feats["face"] -= 0.05
    if "hotline_cues" in issues: feats["safety"] += 0.1
    if issues.get("media_protocol",{}).get("embargo_hours",0) >= 6: feats["face"] += 0.03
    if "scarborough_fisheries_corridor" in issues: feats["safety"] += 0.1; feats["ops_access"] += 0.1
    if "ais_transparency_cell" in issues: feats["verification"] += 0.15
    return {k: max(0,min(1,v)) for k,v in feats.items()}

@dataclass
class BargainingSession:
    case_id: str; parties: List[str]; mediator: str; issue_space: List[str]
    priors: Dict[str, Dict[str, float]] = field(default_factory=dict)
    max_rounds: int = 12; round_idx: int = 0
    def party_utility(self, party: str, agreement: AgreementVector) -> float:
        weights = self.priors.get(party, {"safety":1,"face":1,"ops_access":1,"verification":1})
        feats = _extract_features(agreement.to_dict()); total = sum(weights.values()) or 1
        util = sum(weights.get(k,0)*feats.get(k,0) for k in weights)/total
        util += float(np.random.normal(0,0.01))
        return float(max(0,min(1,util)))
    @classmethod
    def start(cls, case_id, parties, mediator, issue_space, priors=None, max_rounds=12):
        return cls(case_id, parties, mediator, issue_space, priors or {}, max_rounds)
    def evaluate_offer(self, proposer: str, agreement: AgreementVector):
        utils = {p:self.party_utility(p, agreement) for p in self.parties}
        thresholds = {p:0.25 for p in self.parties}
        accept = {p:max(0.0, min(1.0, utils[p]-thresholds[p] + self.round_idx*0.02 + 0.2)) for p in self.parties if p!=proposer}
        self.round_idx += 1
        return {"utilities": utils, "acceptance_prob": accept}
