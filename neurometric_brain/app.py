import streamlit as st
import time
from neurometric.brain import BioState, eq_anxiety, eq_frustration, eq_regret, eq_loneliness, eq_hopelessness

st.set_page_config(page_title="MoheetBrain v3.0", page_icon="📐", layout="centered")

# --- AUTO-ROUTER (The "Classifier") ---
def analyze_signal(text):
    text = text.lower()
    
    # 1. Loneliness (Needs)
    if any(w in text for w in ["lonely", "alone", "girl", "virgin", "missed out"]):
        return "loneliness", BioState(social_req=0.9, social_obs=0.1)
        
    # 2. Regret (Past + Choice)
    if any(w in text for w in ["should have", "mistake", "regret", "idiot", "why did i"]):
        return "regret", BioState(counterfactual_val=0.9, reward_received=0.2, reversibility=0.1)
        
    # 3. Frustration (Blocked Goal)
    if any(w in text for w in ["angry", "stuck", "blocked", "fuck", "annoying"]):
        return "frustration", BioState(reward_expected=0.9, reward_received=0.1)
        
    # 4. Hopelessness (No Agency)
    if any(w in text for w in ["pointless", "never", "always", "give up", "loop"]):
        return "hopelessness", BioState(agency=0.1, social_req=0.8, social_obs=0.2)
        
    # 5. Anxiety (Future + Uncertainty) - DEFAULT
    return "anxiety", BioState(threat_prob=0.8, uncertainty=0.7, coping=0.3)

# --- UI ---
st.title("MoheetBrain v3.0")
st.caption("Universal Emotional Calculus Engine")

with st.container():
    journal_text = st.text_area("Input Stream", height=100, 
        placeholder="e.g. 'I should have spoken to her, I'm such an idiot...'")
    run_btn = st.button("SOLVE EQUATION", type="primary", use_container_width=True)

if run_btn and journal_text:
    with st.spinner("Mapping variables..."):
        time.sleep(0.4)
        
        # A. Route to correct equation
        eq_type, state = analyze_signal(journal_text)
        
        # B. Calculate
        if eq_type == "anxiety": res = eq_anxiety(state)
        elif eq_type == "frustration": res = eq_frustration(state)
        elif eq_type == "regret": res = eq_regret(state)
        elif eq_type == "loneliness": res = eq_loneliness(state)
        elif eq_type == "hopelessness": res = eq_hopelessness(state)
        
        # C. Display
        st.divider()
        st.markdown(f"### 🛑 DETECTED: {eq_type.upper()} ({res['score']*100:.1f}%)")
        
        # The Math Box
        st.info(f"**The Algorithm:**\n\n`{res['formula']}`")
        
        # Variable Breakdown
        cols = st.columns(len(res['vars']))
        for i, (k, v) in enumerate(res['vars'].items()):
            cols[i].metric(k, f"{v:.2f}")
            
        # The Fix
        st.markdown(f"""
        ### 🛠️ The Fix: {res['protocol']}
        
        **Correction:** {res['fix']}
        """)

elif run_btn:
    st.warning("Input required.")
