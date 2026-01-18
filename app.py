import streamlit as st
from dataclasses import dataclass
from typing import Dict, Tuple

# ----------------------------
# Config
# ----------------------------
st.set_page_config(
    page_title="NeuroMetric – Risk Calibration",
    page_icon="🧠",
    layout="wide"
)

# ----------------------------
# Core model (deterministic)
# ----------------------------
EPSILON = 0.05  # prevents denominator collapse 🧱

@dataclass
class CalibrationInput:
    L_low: float
    L_mid: float
    L_high: float
    S: float
    coping: float
    rescue: float
    reversibility: float   # 0 = feels permanent, 1 = clearly reversible
    control: float         # 0 = no agency, 1 = high agency

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def expected_harm(L: float, S: float) -> float:
    return clamp01(L) * clamp01(S)

def buffer_score(coping: float, rescue: float, reversibility: float, control: float) -> float:
    # Weighted sum keeps it interpretable and bounded ✅
    # You can tune these weights later.
    b = (0.35 * coping) + (0.35 * rescue) + (0.15 * reversibility) + (0.15 * control)
    return clamp01(b)

def pressure_score(L: float, S: float, buffers: float) -> float:
    # "Pressure" can be >1; that's fine, but bounded inputs + epsilon keep it stable
    return (clamp01(L) * clamp01(S)) / (EPSILON + buffers)

def band_label(x: float) -> str:
    # Simple banding for interpretation (tune later)
    if x < 0.25:
        return "🟢 Low"
    if x < 0.60:
        return "🟡 Medium"
    if x < 1.10:
        return "🟠 High"
    return "🔴 Extreme"

def dominant_driver(ci: CalibrationInput) -> str:
    # Identify what’s *mathematically* driving the score (simple + explainable)
    buffers = buffer_score(ci.coping, ci.rescue, ci.reversibility, ci.control)

    # Compare components
    L_span = abs(ci.L_high - ci.L_low)
    low_buffers = 1.0 - buffers

    # Heuristic logic (transparent + stable)
    if ci.S >= 0.80 and ci.L_mid <= 0.20:
        return "💥 Severity is high while likelihood is low → classic 'rare catastrophe' fear."
    if low_buffers >= 0.55:
        return "🧱 Buffers feel weak (coping/rescue/control/reversibility) → helplessness amplification."
    if L_span >= 0.35:
        return "🎲 Uncertainty is large (wide probability range) → ambiguity-driven anxiety."
    if ci.control <= 0.25:
        return "🕹️ Low perceived control → nervous system stays on high alert."
    return "✅ No single driver dominates → mixed factors."

# ----------------------------
# Scenario classification (rule-based v1)
# ----------------------------
SCENARIOS = {
    "Legal / Court ⚖️": ["court", "trial", "solicitor", "judge", "case", "conviction", "sentence", "prison", "charge"],
    "Health 🧬": ["symptom", "cancer", "doctor", "hospital", "disease", "pain", "scan"]
}
