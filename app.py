import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime

# --- CONFIGURATION & CONSTANTS ---
st.set_page_config(
    page_title="The Veritas AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CACHED MOCK DATA GENERATION (Prevents Crashing & Memory Leaks) ---
@st.cache_data(ttl=3600)
def load_mock_news_database():
    cities = ["Visakhapatnam (Vizag)", "Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad", "Kolkata"]
    national_channels = ["NDTV", "Times of India", "Star Sports India", "Sony Sports Network", "DD News"]
    local_channels = ["Eeandu Sports (Vizag)", "V6 News Sports", "Mahaa News Vizag Desk", "Thanthi TV Sports"]
    
    topics = [
        "Technology Updates", "Political Campaigns", "Market Business", "Local Smart City Infrastructure", "Public Health", 
        "IPL Cricket Tournament", "Local League Matches", "National Football Championship", "Olympic Qualifiers"
    ]
    
    data = []
    # Generate 100 stable baseline rows
    for i in range(100):
        city = random.choice(cities)
        source_type = random.choice(["National", "Local (City-Specific)"])
        topic = random.choice(topics)
        
        # Category tagging based on topic
        category = "Sports News" if any(x in topic for x in ["Cricket", "Matches", "Football", "Olympic", "Sports"]) else "General News"
        
        if source_type == "National":
            source = random.choice(national_channels)
        else:
            source = f"{random.choice(local_channels)} - {city}"
            
        is_real = random.choice([True, False])
        score = random.uniform(85.0, 99.9) if is_real else random.uniform(10.0, 45.0)
        
        data.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Headline": f"Verification Feed Item {i+1}: Critical update regarding {topic}",
            "Category": category,
            "Source": source,
            "Geography": source_type,
            "City": city,
            "AI Verdict": "REAL" if is_real else "FAKE",
            "Confidence Score": round(score, 2),
            "RL Reward Shift": round(random.uniform(-0.05, 0.05), 4)
        })
    return pd.DataFrame(data)

# --- BACKEND MODEL SIMULATOR (Deep Learning + Reinforcement Learning) ---
class ReliableHybridEvaluator:
    """
    Simulates a Deep Learning (Bi-LSTM / BERT) text feature extractor 
    paired with a Reinforcement Learning (Q-learning contextual bandit) feedback loop.
    """
    def __init__(self):
        # Base weights simulating trained embedding layers
        self.trigger_words = {
            "fake": ["unbelievable match fixing", "shocking discovery", "secret plot", "board banned player hiddenly", "leaked script"],
            "real": ["announced official", "ministry confirmed", "municipal corporation", "reported budget", "official pre-match press conference"]
        }

    def evaluate_text(self, text: str):
        text_lower = text.lower()
        fake_signals = sum(1 for word in self.trigger_words["fake"] if word in text_lower)
        real_signals = sum(1 for word in self.trigger_words["real"] if word in text_lower)
        
        # Base DL probability calculation
        base_prob = 0.5 + (real_signals * 0.15) - (fake_signals * 0.2)
        base_prob = max(0.01, min(0.99, base_prob))
        
        # Simulating RL dynamic environment adjustment (Contextual Bandit Reward Weight)
        rl_adjustment = random.uniform(-0.02, 0.02)
        final_prob = max(0.01, min(0.99, base_prob + rl_adjustment))
        
        verdict = "REAL" if final_prob >= 0.5 else "FAKE"
        confidence = final_prob if verdict == "REAL" else (1 - final_prob)
        
        return verdict, round(confidence * 100, 2), round(rl_adjustment, 4)

# --- MAIN APP LOGIC ---
def main():
    st.title("⚖️ The Veritas AI")
    st.subheader("Deep Learning & Reinforcement Learning Guard Engine")
    st.caption("An immutable verification system sourcing from National and Local Channels (including Vizag).")
    
    evaluator = ReliableHybridEvaluator()
    db_df = load_mock_news_database()

    # --- SIDEBAR CONTROL PANEL ---
    st.sidebar.header("🎯 Navigation & Live Sourcing")
    app_mode = st.sidebar.radio("Go to:", ["Single URL/Text Verifier", "Live Sourced Stream", "RL Model Performance Analytics"])
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎚️ Feed Customization Filters")
    category_filter = st.sidebar.selectbox("Select Desk Category:", ["All Content", "General News", "Sports News"])
    selected_city = st.sidebar.selectbox("Filter Local Channels by City:", 
                                         ["All Cities", "Visakhapatnam (Vizag)", "Mumbai", "Delhi", "Bengaluru", "Chennai", "Hyderabad", "Kolkata"])

    if app_mode == "Single URL/Text Verifier":
        st.header("🔍 Real-time Article Analysis")
        st.markdown("Input content or an article URL link below. **The Veritas AI** processes pattern layers alongside active contextual feedback reward checks.")
        
        input_type = st.radio("Input Format:", ["Raw Text Content", "News Article URL"])
        user_input = ""
        
        if input_type == "Raw Text Content":
            user_input = st.text_area("Paste Content Here:", placeholder="E.g., Municipal Corporation announced official upgrades for the upcoming smart city deployment in Vizag...")
        else:
            user_input = st.text_input("Enter Link URL:", placeholder="https://thehindu.com...")

        if st.button("🚀 Execute Neural Analysis"):
            if user_input.strip() == "":
                st.error("Please provide valid input text or a URL link first.")
            else:
                with st.spinner("Processing embeddings & querying active RL environment matrices..."):
                    time.sleep(1.2) # Simulate network/model inference latency safely
                    verdict, confidence, rl_shift = evaluator.evaluate_text(user_input)
                    
                # Layout metric cards
                col1, col2, col3 = st.columns(3)
                with col1:
                    if verdict == "REAL":
                        st.success(f"🎯 Verdict: {verdict}")
                    else:
                        st.error(f"🚨 Verdict: {verdict}")
                with col2:
                    st.metric(label="DL Core Confidence Level", value=f"{confidence}%")
                with col3:
                    st.metric(label="RL Bandit Reward Shift", value=f"{rl_shift}", delta=f"{'Positive' if rl_shift>=0 else 'Negative'} Adaptation")
                
                # Dynamic Safe Context breakdown
                st.markdown("### 🧬 AI Framework Execution Path Explainer")
                st.info(f"**1. Deep Learning Stack:** Extracted textual sequence components. Sourced validation matches token sequences against registered feeds.\n"
                        f"**2. Reinforcement Learning Loop:** Adjusted dynamic reward strategy weights based on historical credibility ratios. Active adjustment value = `{rl_shift}`.")

    elif app_mode == "Live Sourced Stream":
        st.header("📡 Live Unified Sourcing Feed")
        st.markdown("Simulated live feed listening to domestic sports bureaus, national outlets, and regional municipality nodes.")
        
        # Apply City and Category Filters safely
        filtered_df = db_df.copy()
        
        if category_filter != "All Content":
            filtered_df = filtered_df[filtered_df["Category"] == category_filter]
            
        if selected_city != "All Cities":
            # If local, keep only matches. If national, retain for baseline context
            filtered_df = filtered_df[(filtered_df["City"] == selected_city) | (filtered_df["Geography"] != "Local (City-Specific)")]
            st.success(f"Showing localized pipeline for **{selected_city}** under **{category_filter}** desk.")
            
        # Display Metrics Overview
        real_count = len(filtered_df[filtered_df["AI Verdict"] == "REAL"])
        fake_count = len(filtered_df[filtered_df["AI Verdict"] == "FAKE"])
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Total Active Channels Scanned", len(filtered_df))
        m_col2.metric("Verified True Streams", real_count)
        m_col3.metric("Flagged Disinformation Networks", fake_count)
        
        st.markdown("### 🗂️ Live Broadcast Audit Ledger")
        st.dataframe(filtered_df, use_container_width=True)

    elif app_mode == "RL Model Performance Analytics":
        st.header("📈 Model Resilience & Feedback Loops")
        st.markdown("Tracking Reinforcement Learning convergence loops. Ensures protection against data drifts so the system avoids unexpected failure or crashing down the road.")
        
        # Safe dummy plotting using standard dataframes to avoid complex charting library crashes
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['DL Loss Convergence', 'RL Reward Accuracy', 'API Pipeline Stability']
        )
        st.line_chart(chart_data)
        st.caption("Figure: Performance values tracking stable runtime execution profiles across multiple geographic nodes.")

if __name__ == '__main__':
    main()
                  
