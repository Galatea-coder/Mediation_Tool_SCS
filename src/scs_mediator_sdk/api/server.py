from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from scs_mediator_sdk.engines.bargaining_engine import BargainingSession, AgreementVector
from scs_mediator_sdk.sim.mesa_abm import MaritimeModel

app = FastAPI(title="SCS Mediator SDK API", version="0.4.0")

class SessionCreate(BaseModel):
    case_id: str; parties: List[str]; mediator: str; issue_space: List[str]
    priors: Optional[Dict[str, Dict[str, float]]] = None
    max_rounds: int = 12

class Offer(BaseModel):
    proposer_party_id: str
    agreement_vector: Dict[str, Dict[str, Any]]

class SimRun(BaseModel):
    steps: int = 200
    environment: Dict[str, Any]
    agreement_vector: Dict[str, Dict[str, Any]]
    seed: Optional[int]=None

_sessions: Dict[str, BargainingSession] = {}

@app.get("/healthz")
def healthz(): return {"status":"ok"}

@app.post("/bargain/sessions")
def start_session(req: SessionCreate):
    s = BargainingSession.start(req.case_id, req.parties, req.mediator, req.issue_space, req.priors, req.max_rounds)
    _sessions[req.case_id] = s
    return {"session_id": req.case_id, "status":"ready"}

@app.post("/bargain/{session_id}/offer")
def make_offer(session_id: str, offer: Offer):
    s = _sessions[session_id]; av = AgreementVector(offer.agreement_vector)
    return s.evaluate_offer(offer.proposer_party_id, av)

@app.post("/sim/run")
def run_sim(run: SimRun):
    m = MaritimeModel(steps=run.steps, environment=run.environment, agreement=run.agreement_vector, seed=run.seed)
    df = m.run()
    if df.empty:
        summary = {"incidents":0,"max_severity":0}
        rows = []
    else:
        summary = {"incidents":int(len(df)), "max_severity": float(df["severity"].max())}
        rows = df.to_dict(orient="records")
    return {"summary": summary, "events": rows}

class CalibratePayload(BaseModel):
    steps: int = 300
    environment: Dict[str, Any]
    agreement_vector: Dict[str, Dict[str, Any]]
    # Historical counts per N-step bucket, e.g., {0:3,20:5,40:2,...}
    historical: Dict[int, int]
    bucket: int = 20
    seeds: List[int] | None = None

def _score_model(params, steps, env, av, hist, bucket, seeds):
    alpha, base_p = params
    import numpy as np
    total_err = 0.0; runs = seeds or [42, 1337, 7]
    for sd in runs:
        m = MaritimeModel(steps=steps, environment=env, agreement=av, seed=sd)
        # apply params: scale agent risk and base pressure
        m.incident_pressure = max(0.01, min(0.95, base_p))
        for a in m.schedule.agents:
            a.risk_bias *= alpha
        df = m.run()
        if df.empty:
            sim_counts = {}
        else:
            df['bucket'] = (df['step']//bucket)*bucket
            sim_counts = df.groupby('bucket').size().to_dict()
        # align keys union
        keys = set(list(hist.keys()) + list(sim_counts.keys()))
        for k in keys:
            total_err += (sim_counts.get(k,0) - hist.get(k,0))**2
    return total_err

@app.post("/sim/calibrate")
def sim_calibrate(req: CalibratePayload):
    # Simple grid search over alpha (risk scale) and base_p (initial pressure)
    alphas = [0.6,0.8,1.0,1.2,1.4]
    bases = [0.10,0.20,0.25,0.30,0.35]
    best = {"alpha":1.0,"base_p":0.25,"score":1e9}
    for a in alphas:
        for b in bases:
            s = _score_model((a,b), req.steps, req.environment, req.agreement_vector, req.historical, req.bucket, req.seeds)
            if s < best["score"]:
                best = {"alpha":a,"base_p":b,"score":float(s)}
    return {"best_params": best}

from fastapi import Body

# Global sim params (server-wide defaults). Trainers can override via PUT.
_sim_params = {"alpha": 1.0, "base_p": 0.25}

@app.get("/sim/params")
def get_params():
    return {"params": _sim_params}

@app.put("/sim/params")
def set_params(params: Dict[str, float] = Body(..., embed=True)):
    # Expect keys like {"alpha": 1.0, "base_p": 0.25}
    for k in ["alpha","base_p"]:
        if k in params:
            _sim_params[k] = float(params[k])
    return {"params": _sim_params}
