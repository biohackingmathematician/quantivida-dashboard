import streamlit as st
import plotly.graph_objects as go
import csv

st.set_page_config(page_title="Quantivida", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0A0A0A;
        color: #FAFAFA;
    }
    h1 {
        color: #D4AF37;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = []
    with open('framer_wellness_dashboard.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

st.title("🧬 QUANTIVIDA")
st.markdown("### Wellness Intelligence Dashboard")
st.markdown("*Predictive by Nature. Personal by Design.*")

data = load_data()

if data:
    user_names = [row['full_name'] for row in data]
    selected = st.selectbox("Select User", user_names)
    
    user = next(row for row in data if row['full_name'] == selected)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Readiness Score", f"{float(user['readiness_score']):.0f}/100")
    with col2:
        st.metric("HRV Proxy", f"{float(user['hrv_proxy']):.0f}/100")
    with col3:
        st.metric("Sleep Efficiency", f"{float(user['sleep_efficiency']):.0f}%")
    with col4:
        st.metric("Stress Level", f"{user['stress_level']}/10")
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Mental Clarity", f"{user['mental_clarity']}/10")
    with col2:
        st.metric("Recovery Score", f"{user['recovery_score']}/10")
    with col3:
        st.metric("Energy Level", f"{user['energy_level']}/10")
    with col4:
        st.metric("Anabolic Index", f"{float(user['anabolic_index']):.1f}/10")
    
    st.markdown("---")
    st.subheader("📊 Personalized Insights")
    
    if user.get('insight_1_title'):
        with st.expander(f"🎯 {user['insight_1_category']}: {user['insight_1_title']}", expanded=True):
            st.write(user['insight_1_message'])
            if user.get('insight_1_action'):
                st.info(f"**Action:** {user['insight_1_action']}")
    
    if user.get('insight_2_title'):
        with st.expander(f"💡 {user['insight_2_category']}: {user['insight_2_title']}"):
            st.write(user['insight_2_message'])
    
    if user.get('insight_3_title'):
        with st.expander(f"✨ {user['insight_3_category']}: {user['insight_3_title']}"):
            st.write(user.get('insight_3_message', ''))
    
    st.markdown("---")
    st.caption("QUANTIVIDA • The Human Algorithm • Wellness Intelligence v2.0")
