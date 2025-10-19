# Custom CSS for luxury dark theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #0A0A0A;
        color: #FAFAFA;
    }
    
    [data-testid="stSidebar"] {
        background-color: #141414;
        border-right: 1px solid #1F1F1F;
    }
    
    h1 {
        color: #D4AF37;
        font-weight: 300;
        letter-spacing: 2px;
        font-size: 2.5rem !important;
    }
    
    h2 {
        color: #FAFAFA;
        font-weight: 300;
        font-size: 1.8rem !important;
        margin-top: 2rem;
    }
    
    h3 {
        color: #A0A0A0;
        font-weight: 400;
        font-size: 1.2rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 200;
        color: #FAFAFA;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #A0A0A0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    hr {
        border-color: #1F1F1F;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)"""
QUANTIVIDA INTERACTIVE WELLNESS DASHBOARD
Built with Streamlit for pilot demos

Install: pip3 install streamlit plotly
Run: streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import csv

# ============================================
# PAGE CONFIG - LUXURY AESTHETIC
# ============================================

st.set_page_config(
    page_title="Quantivida | Wellness Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LOAD DATA (WITHOUT PANDAS)
# ============================================

@st.cache_data
def load_data():
    """Load wellness dashboard data from CSV"""
    data = []
    with open('framer_wellness_dashboard.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Convert numeric fields
            row['readiness_score'] = float(row['readiness_score'])
            row['hrv_proxy'] = float(row['hrv_proxy'])
            row['sleep_efficiency'] = float(row['sleep_efficiency'])
            row['stress_level'] = int(row['stress_level'])
            row['mental_clarity'] = int(row['mental_clarity'])
            row['recovery_score'] = int(row['recovery_score'])
            row['energy_level'] = int(row['energy_level'])
            row['training_load'] = float(row['training_load'])
            row['anabolic_index'] = float(row['anabolic_index'])
            row['circadian_score'] = float(row['circadian_score'])
            row['cognitive_load'] = float(row['cognitive_load'])
            row['day1_optimistic'] = float(row['day1_optimistic'])
            row['day1_baseline'] = float(row['day1_baseline'])
            row['day1_pessimistic'] = float(row['day1_pessimistic'])
            row['day2_optimistic'] = float(row['day2_optimistic'])
            row['day2_baseline'] = float(row['day2_baseline'])
            row['day3_optimistic'] = float(row['day3_optimistic'])
            row['day3_baseline'] = float(row['day3_baseline'])
            data.append(row)
    return data

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_status_color(value, thresholds):
    """Get color based on value and thresholds"""
    if value >= thresholds['excellent']:
        return '#10B981'  # Success green
    elif value >= thresholds['good']:
        return '#3B82F6'  # Blue
    elif value >= thresholds['moderate']:
        return '#F59E0B'  # Warning amber
    else:
        return '#DC2626'  # Critical red

def create_readiness_gauge(readiness):
    """Create beautiful gauge chart for readiness"""
    
    if readiness >= 85:
        color = '#10B981'
        descriptor = 'Peak State'
    elif readiness >= 75:
        color = '#3B82F6'
        descriptor = 'High Capacity'
    elif readiness >= 65:
        color = '#3B82F6'
        descriptor = 'Moderate'
    elif readiness >= 50:
        color = '#F59E0B'
        descriptor = 'Suboptimal'
    else:
        color = '#DC2626'
        descriptor = 'Recovery Needed'
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = readiness,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': descriptor, 'font': {'size': 16, 'color': '#A0A0A0'}},
        number = {'font': {'size': 60, 'color': '#FAFAFA'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#1F1F1F"},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "#1F1F1F",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': '#1A1A1A'},
                {'range': [50, 75], 'color': '#141414'},
                {'range': [75, 100], 'color': '#0F0F0F'}
            ],
            'threshold': {
                'line': {'color': "#D4AF37", 'width': 4},
                'thickness': 0.75,
                'value': readiness
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='#0A0A0A',
        plot_bgcolor='#0A0A0A',
        font={'color': "#FAFAFA", 'family': "Inter"},
        height=350,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def create_biometric_bars(user_data):
    """Create horizontal bar chart for biometrics"""
    
    metrics = {
        'HRV Proxy': user_data['hrv_proxy'],
        'Sleep Efficiency': user_data['sleep_efficiency'],
        'Stress (inv)': 100 - (user_data['stress_level'] * 10),
        'Recovery': user_data['recovery_score'] * 10,
        'Mental Clarity': user_data['mental_clarity'] * 10,
        'Energy': user_data['energy_level'] * 10
    }
    
    colors = []
    for value in metrics.values():
        if value >= 75:
            colors.append('#10B981')
        elif value >= 60:
            colors.append('#3B82F6')
        elif value >= 40:
            colors.append('#F59E0B')
        else:
            colors.append('#DC2626')
    
    fig = go.Figure(go.Bar(
        y=list(metrics.keys()),
        x=list(metrics.values()),
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='#1F1F1F', width=1)
        ),
        text=[f'{v:.0f}' for v in metrics.values()],
        textposition='outside',
        textfont=dict(color='#FAFAFA', size=12)
    ))
    
    fig.update_layout(
        paper_bgcolor='#0A0A0A',
        plot_bgcolor='#0A0A0A',
        font={'color': "#A0A0A0", 'family': "Inter"},
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(
            range=[0, 100],
            gridcolor='#1F1F1F',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False
        ),
        showlegend=False
    )
    
    return fig

def create_forecast_chart(user_data, current_readiness):
    """Create 3-day forecast line chart"""
    
    days = ['Today', 'Day 1', 'Day 2', 'Day 3']
    
    optimistic = [
        current_readiness,
        user_data['day1_optimistic'],
        user_data['day2_optimistic'],
        user_data['day3_optimistic']
    ]
    
    baseline = [
        current_readiness,
        user_data['day1_baseline'],
        user_data['day2_baseline'],
        user_data['day3_baseline']
    ]
    
    pessimistic = [
        current_readiness,
        user_data['day1_pessimistic'],
        user_data['day2_baseline'],
        user_data['day3_baseline']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=days, y=optimistic,
        mode='lines+markers',
        name='With Adherence',
        line=dict(color='#10B981', width=3),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=days, y=baseline,
        mode='lines+markers',
        name='Current Path',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=days, y=pessimistic,
        mode='lines+markers',
        name='Without Changes',
        line=dict(color='#DC2626', width=3, dash='dash'),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        paper_bgcolor='#0A0A0A',
        plot_bgcolor='#0A0A0A',
        font={'color': "#A0A0A0", 'family': "Inter"},
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(
            showgrid=False
        ),
        yaxis=dict(
            range=[0, 100],
            gridcolor='#1F1F1F',
            showgrid=True,
            title='Readiness Score'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )
    
    return fig

def create_advanced_metrics_radar(user_data):
    """Create radar chart for advanced metrics"""
    
    categories = ['Anabolic\nIndex', 'Circadian\nScore', 'Cognitive\nCapacity',
                  'Recovery', 'HRV', 'Sleep Quality']
    
    values = [
        user_data['anabolic_index'] * 10,
        user_data['circadian_score'] * 10,
        (10 - user_data['cognitive_load']) * 10,
        user_data['recovery_score'] * 10,
        user_data['hrv_proxy'],
        user_data['sleep_efficiency']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(212, 175, 55, 0.2)',
        line=dict(color='#D4AF37', width=2),
        marker=dict(size=8, color='#D4AF37')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='#1F1F1F',
                tickfont=dict(color='#A0A0A0')
            ),
            angularaxis=dict(
                gridcolor='#1F1F1F',
                linecolor='#1F1F1F',
                tickfont=dict(color='#FAFAFA', size=11)
            ),
            bgcolor='#0A0A0A'
        ),
        paper_bgcolor='#0A0A0A',
        font={'family': "Inter"},
        height=350,
        margin=dict(l=60, r=60, t=40, b=40),
        showlegend=False
    )
    
    return fig

# ============================================
# MAIN APP
# ============================================

def main():
    
    # Load data
    data = load_data()
    
    # Sidebar - User Selection
    with st.sidebar:
        st.markdown("## QUANTIVIDA")
        st.markdown("### Select User")
        
        user_names = [user['full_name'] for user in data]
        selected_user = st.selectbox(
            "Choose a user to view their wellness intelligence:",
            user_names,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Get selected user data
        user_data = next(user for user in data if user['full_name'] == selected_user)
        
        st.markdown("### Quick Stats")
        st.metric("Readiness", f"{user_data['readiness_score']:.0f}/100")
        st.metric("HRV Proxy", f"{user_data['hrv_proxy']:.0f}/100")
        st.metric("Sleep Efficiency", f"{user_data['sleep_efficiency']:.0f}%")
        
        st.markdown("---")
        st.caption(f"Report Date: {user_data['date']}")
        st.caption("Model: Quantivida v2.0")
    
    # Main content
    first_name = selected_user.split()[0]
    
    # Header
    st.markdown(f"# {selected_user}")
    st.markdown("### Wellness Intelligence Report")
    st.markdown("*Predictive by Nature. Personal by Design.*")
    st.markdown("---")
    
    # Row 1: Readiness Gauge + Key Metrics
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### System Readiness")
        fig_gauge = create_readiness_gauge(user_data['readiness_score'])
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        st.markdown("#### Biometric Profile")
        fig_bars = create_biometric_bars(user_data)
        st.plotly_chart(fig_bars, use_container_width=True)
    
    st.markdown("---")
    
    # Row 2: Advanced Metrics + Forecast
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Advanced Metrics Profile")
        fig_radar = create_advanced_metrics_radar(user_data)
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        st.markdown("#### 3-Day Readiness Forecast")
        fig_forecast = create_forecast_chart(user_data, user_data['readiness_score'])
        st.plotly_chart(fig_forecast, use_container_width=True)
    
    st.markdown("---")
    
    # Row 3: Detailed Metrics Grid
    st.markdown("#### Detailed Biometrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Anabolic Index",
            f"{user_data['anabolic_index']:.1f}/10",
            help="Building vs. breaking down state"
        )
    
    with col2:
        st.metric(
            "Circadian Score",
            f"{user_data['circadian_score']:.1f}/10",
            help="Sleep-wake rhythm health"
        )
    
    with col3:
        st.metric(
            "Cognitive Load",
            f"{user_data['cognitive_load']:.1f}/10",
            help="Mental processing demand",
            delta=f"{10 - user_data['cognitive_load']:.1f} capacity",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            "Training Load",
            f"{user_data['training_load']:.0f}",
            help="Current training stress"
        )
    
    st.markdown("---")
    
    # Row 4: Insights
    st.markdown("#### Personalized Insights")
    
    insights = [
        {
            'type': user_data['insight_1_type'],
            'category': user_data['insight_1_category'],
            'title': user_data['insight_1_title'],
            'message': user_data['insight_1_message']
        },
        {
            'type': user_data['insight_2_type'],
            'category': user_data['insight_2_category'],
            'title': user_data['insight_2_title'],
            'message': user_data['insight_2_message']
        },
        {
            'type': user_data['insight_3_type'],
            'category': user_data['insight_3_category'],
            'title': user_data['insight_3_title'],
            'message': user_data.get('insight_3_message', '')
        }
    ]
    
    for idx, insight in enumerate(insights):
        if insight['title']:
            
            # Color coding
            type_colors = {
                'critical': '🚨',
                'warning': '⚠️',
                'action': '🎯',
                'positive': '✅',
                'strength': '💪',
                'intelligence': '🧬',
                'system_state': '📊'
            }
            
            icon = type_colors.get(insight['type'], '•')
            
            with st.expander(f"{icon} {insight['category']}: {insight['title']}", expanded=(idx==0)):
                st.markdown(f"**{insight['title']}**")
                st.write(insight['message'])
                
                if 'insight_1_action' in user_data and idx == 0 and user_data['insight_1_action']:
                    st.markdown("**🎯 Recommended Action:**")
                    st.info(user_data['insight_1_action'])
    
    st.markdown("---")
    
    # Row 5: Context
    st.markdown("#### User Context")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if user_data['wellness_goals']:
            st.markdown("**Primary Wellness Goals:**")
            st.write(user_data['wellness_goals'])
    
    with col2:
        if user_data['pain_point']:
            st.markdown("**Key Challenge:**")
            st.write(user_data['pain_point'])
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #707070; font-size: 0.9rem; padding: 2rem;'>
        <p><strong>QUANTIVIDA</strong> • The Human Algorithm</p>
        <p style='font-size: 0.8rem;'>Wellness Intelligence • Powered by Advanced Biometric Modeling</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()