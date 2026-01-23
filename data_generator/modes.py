from enum import Enum

class SimulationMode(Enum):
    NORMAL = "normal"
    FAULT = "fault"
    NOISE = "noise"

def apply_mode(mode):
    if mode == SimulationMode.FAULT:
        return {"fault": True, "noise_multiplier": 1.0}
    if mode == SimulationMode.NOISE:
        return {"fault": False, "noise_multiplier": 3.0}
    return {"fault": False, "noise_multiplier": 1.0}
