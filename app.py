import streamlit as st
import json
import time
import random

# Page Configuration
st.set_page_config(
    page_title="NeuroMetric Analyzer (Simulation Mode)",
    page_icon="🧠",
    layout="wide"
)

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ System Status")
    st.success("🟢 Simulation Mode Active")
    st.info("No API Key required. Running localized stochastic modeling.")
    
    st.divider()
    st.markdown("""
    ### 🔬 Scientific Framework
    * **RPE:** Reward Prediction Error
    * **Entropy:** Uncertainty/Anxiety
    * **Counterfactual:** Regret
    """)

# --- MAIN APP ---
st.title("🧠 NeuroMetric: Computational Affective Modeling")
st.caption("Mode: SIMULATION (Stochastic Generation)")

# --- USER INPUT ---
user_entry = st.text_area(
    "Input Raw Data (Journal Entry):", 
    height=150, 
    placeholder="e.g. Went to the Buddhist Centre. Saw a girl. Froze. Felt ashamed."
)

if st.button("Run Computation"):
    if not user_entry:
        st.warning("Please enter text to analyze.")
    else:
        # SIMULATING THE AI THINKING
        with st.spinner("Running Inference Model..."):
            time.sleep(2) # Fake processing time to feel real
            
            # GENERATING DUMMY DATA (STOCHASTIC)
            # This simulates what the AI would output based on your mood
            data = {
                "Reward_Prediction_Error": round(random.uniform(-5.0, 5.0), 1),
                "Uncertainty_Coefficient": round(random.uniform(0.1, 0.9), 2),
                "Counterfactual_Loss": round(random.uniform(1.0, 9.0), 1),
                "Cognitive_Dissonance": round(random.uniform(2.0, 8.0), 1),
                "Recommended_Algorithm": random.choice([
                    "DialoguePod Activation", 
                    "Machine Gun Protocol", 
                    "The Metaview", 
                    "Cognitive Reframing"
                ])
            }
            
            # --- VISUALIZATION ---
            st.success("Analysis Complete.")
            
            # Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("RPE (Dopamine)", f"{data['Reward_Prediction_Error']}", delta="Prediction Error")
            
            with col2:
                st.metric("Entropy (Anxiety)", f"{data['Uncertainty_Coefficient']}/1.0", delta_color="inverse")
                
            with col3:
                st.metric("Counterfactual Loss", f"{data['Counterfactual_Loss']}/10", delta_color="inverse")
                
            with col4:
                st.metric("Dissonance", f"{data['Cognitive_Dissonance']}/10", delta_color="inverse")
            
            st.divider()
            
            # Strategic Output
            st.subheader("🤖 Recommended Protocol")
            st.info(f"**Strategy: {data['Recommended_Algorithm']}**")
            
            with st.expander("View Raw JSON Output"):
                st.json(data)

# Footer
st.markdown("---")
st.caption("NeuroMetric v1.0 | Built with Python & Streamlit")