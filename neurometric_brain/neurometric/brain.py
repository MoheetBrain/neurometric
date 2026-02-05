from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Tuple
import math

@dataclass(frozen=True)
class BioState:
    # 1. Prediction / Entropy (Anxiety)
    threat_prob: float = 0.5    # Likelihood of bad thing
    uncertainty: float = 0.5    # Entropy (I don't know what will happen)
    coping: float = 0.5         # Self-efficacy
    
    # 2. Reward / Dopamine (Frustration/Sadness)
    reward_expected: float = 0.8
    reward_received: float = 0.2
    
    # 3. Social (Loneliness/Shame)
    social_req: float = 0.8
    social_obs: float = 0.2
    judgment_weight: float = 0.5  # How much I care what they think
    
    # 4. Agency / Time (Regret/Hopelessness)
    agency: float = 0.5           # Control over outcome
    counterfactual_val: float = 0.8 # Value of "What I should have done"
    reversibility: float = 0.2    # Can I fix it?

# ----------------------------
# The 5 Master Equations
# ----------------------------

def eq_anxiety(s: BioState) -> Dict[str, Any]:
    """
    Model: Entropy & Signal-to-Noise
    Anxiety = (Threat x Entropy) / Coping
    """
    numerator = s.threat_prob * (1.0 + s.uncertainty)
    denominator = s.coping + 0.1
    score = min(1.0, numerator / denominator)
    return {
        "score": score,
        "formula": "Anxiety = (Threat × Uncertainty) / Coping",
        "vars": {"Threat": s.threat_prob, "Uncertainty": s.uncertainty, "Coping": s.coping},
        "protocol": "DIALOGUEPOD",
        "fix": "Reduce Uncertainty (Info Gathering) or Increase Coping (Micro-wins)."
    }

def eq_frustration(s: BioState) -> Dict[str, Any]:
    """
    Model: Reward Prediction Error (RPE)
    Frustration = (Expected - Received) x Effort
    """
    rpe = max(0.0, s.reward_expected - s.reward_received)
    score = min(1.0, rpe * 1.5) # Scale up because RPE hurts
    return {
        "score": score,
        "formula": "Frustration = Expected_Reward - Received_Reward",
        "vars": {"Expected": s.reward_expected, "Received": s.reward_received},
        "protocol": "RESET_DOPAMINE",
        "fix": "Update Priors. Your expectation was a hallucination. Accept reality data."
    }

def eq_regret(s: BioState) -> Dict[str, Any]:
    """
    Model: Counterfactual Comparison
    Regret = (Value_Foregone - Value_Realized) x Responsibility
    """
    diff = max(0.0, s.counterfactual_val - s.reward_received)
    # Regret only happens if you had Agency (Responsibility)
    score = min(1.0, diff * (1.0 - s.reversibility)) 
    return {
        "score": score,
        "formula": "Regret = (Best_Option - Chosen_Option) × Irreversibility",
        "vars": {"Best_Option": s.counterfactual_val, "Chosen": s.reward_received, "Permanent": 1.0-s.reversibility},
        "protocol": "EGOSNAP",
        "fix": "The past is a read-only file. Reduce 'Counterfactual Value' to 0."
    }

def eq_loneliness(s: BioState) -> Dict[str, Any]:
    """
    Model: Homeostatic Error
    Loneliness = Required - Observed
    """
    score = max(0.0, s.social_req - s.social_obs)
    return {
        "score": score,
        "formula": "Loneliness = Social_Required - Social_Observed",
        "vars": {"Required": s.social_req, "Observed": s.social_obs},
        "protocol": "SEEK_TRIBE",
        "fix": "Homeostatic deficit. Must intake social calories immediately."
    }

def eq_hopelessness(s: BioState) -> Dict[str, Any]:
    """
    Model: Learned Helplessness
    Hopelessness = Pain x (1 - Agency)
    """
    pain = max(s.social_req - s.social_obs, s.threat_prob)
    score = min(1.0, pain * (1.0 - s.agency))
    return {
        "score": score,
        "formula": "Hopelessness = Current_Pain × (1 - Agency)",
        "vars": {"Pain": pain, "Agency": s.agency},
        "protocol": "MICRO_WINS",
        "fix": "Agency is 0. Hack the system by doing 1 tiny mechanical task."
    }
