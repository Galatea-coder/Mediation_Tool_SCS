from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List
import random
import pandas as pd
from mesa import Model, Agent
from mesa.time import RandomActivation

class MaritimeAgent(Agent):
    def __init__(self, unique_id, model, kind:str):
        super().__init__(unique_id, model)
        self.kind = kind
        self.risk_bias = {"CCG":0.15,"PCG":0.10,"Militia":0.20,"Fisher":0.05}.get(kind,0.1)
    def step(self):
        delta = self.risk_bias
        av = self.model.agreement or {}
        if av.get("hotline_cues"): delta -= 0.04
        if av.get("resupply_SOP"):
            rs = av["resupply_SOP"]; delta -= min(0.06, 0.02*rs.get("standoff_nm",0) + 0.01*rs.get("escort_count",0))
        if av.get("scarborough_fisheries_corridor"): delta -= 0.05
        if av.get("ais_transparency_cell"): delta -= 0.04
        if self.model.weather == "rough": delta += 0.07
        if self.model.media_visibility >= 2: delta -= 0.02
        self.model.incident_pressure = max(0.01, self.model.incident_pressure + delta*0.01)

class MaritimeModel(Model):
    def __init__(self, steps:int=200, environment:Dict[str,Any]=None, agreement:Dict[str,Any]=None, seed:int=None):
        super().__init__(seed=seed)
        self.schedule = RandomActivation(self)
        self.steps = steps
        env = environment or {}
        self.weather = env.get("weather_state","calm")
        self.media_visibility = env.get("media_visibility",2)
        self.incident_pressure = 0.25
        self.agreement = agreement or {}
        kinds = ["CCG"]*3 + ["PCG"]*2 + ["Militia"]*4 + ["Fisher"]*6
        for i, k in enumerate(kinds):
            self.schedule.add(MaritimeAgent(i, self, k))
        self.history: List[Dict[str,Any]] = []
    def step(self):
        self.schedule.step()
        p = max(0.01, min(0.95, self.incident_pressure))
        if random.random() < p:
            itype = random.choices(["water_cannon","ramming","detention_attempt","near_miss"], [0.35,0.2,0.2,0.25])[0]
            sev = random.random()*(1.0 if itype!="near_miss" else 0.5)
            self.history.append({"step": self.schedule.steps, "incident_type": itype, "severity": sev})
    def run(self)->pd.DataFrame:
        for _ in range(self.steps): self.step()
        return pd.DataFrame(self.history)
