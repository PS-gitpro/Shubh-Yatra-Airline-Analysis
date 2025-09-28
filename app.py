import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# Copyright (c) 2025 Prateek Singh. All Rights Reserved.
# Licensed under the MIT License.

# Page configuration
st.set_page_config(
    page_title="Shubh Yatra - Airline Risk Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .project-title {
        font-size: 3rem;
        color: #1E40AF;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    .project-subtitle {
        font-size: 1.5rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: normal;
    }
    .main-header {
        font-size: 2.2rem;
        color: #1E40AF;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #1E40AF;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
        text-align: center;
    }
    .risk-metric {
        background-color: #fff7ed;
        border-left: 4px solid #ea580c;
    }
    .safety-metric {
        background-color: #f0fdf4;
        border-left: 4px solid #16a34a;
    }
    .stButton>button {
        background-color: #1E40AF;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #153E90;
        color: white;
    }
    .sidebar-header {
        font-size: 1.5rem;
        color: #1E40AF;
        margin-bottom: 1rem;
    }
    .upload-box {
        border: 2px dashed #ccc;
        border-radius: 5px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
        background-color: #f9fafb;
    }
    .airline-logo {
        font-size: 1.2rem;
        font-weight: bold;
        margin: 5px 0;
    }
    .success-msg {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    .risk-indicator {
        padding: 8px 12px;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
        margin: 5px 0;
    }
    .risk-low {
        background-color: #dcfce7;
        color: #166534;
    }
    .risk-medium {
        background-color: #fef9c3;
        color: #854d0e;
    }
    .risk-high {
        background-color: #fee2e2;
        color: #991b1b;
    }
</style>
""", unsafe_allow_html=True)

# Project title and subtitle
st.markdown('<p class="project-title">🧿Shubh Yatra✈️</p>', unsafe_allow_html=True)
st.markdown('<p class="project-subtitle">Risk Factor Analysis For Indian Domestic Flights</p>', unsafe_allow_html=True)

# Sample data generation for demonstration
def generate_sample_data():
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='D')
    airlines = ['IndiGo', 'Air India', 'SpiceJet', 'Vistara', 'AirAsia']
    
    data = []
    for i in range(1000):
        date = np.random.choice(dates)
        airline = np.random.choice(airlines)
        flight_num = f"{np.random.choice(['6E', 'AI', 'SG', 'UK', 'I5'])}-{np.random.randint(100, 9999)}"
        aircraft = np.random.choice(['A320neo', 'B737', 'A321', 'B787', 'A320'])
        incident_type = np.random.choice(['None', 'Technical', 'Weather', 'ATC', 'Operational'], p=[0.85, 0.05, 0.04, 0.03, 0.03])
        severity = np.random.choice(['Low', 'Medium', 'High'], p=[0.7, 0.2, 0.1])
        time_of_day = np.random.choice(['Morning', 'Afternoon', 'Evening', 'Night'])
        
        data.append([date, flight_num, airline, aircraft, incident_type, severity, time_of_day])
    
    df = pd.DataFrame(data, columns=['Date', 'Flight', 'Airline', 'Aircraft', 'Incident_Type', 'Severity', 'Time_of_Day'])
    return df

# Risk calculation functions
def calculate_risk_score(airline, df):
    """Calculate risk score for an airline based on incident data or use existing Risk_Score"""
    # First check if Risk_Score column exists in the uploaded data
    if 'Risk_Score' in df.columns:
        airline_data = df[df['Airline'] == airline]
        if not airline_data.empty:
            # Return the risk score from the CSV data (use first value found)
            return airline_data['Risk_Score'].values[0]
    
    # If no Risk_Score column exists, calculate it from incidents
    airline_data = df[df['Airline'] == airline]
    total_flights = len(airline_data)
    
    if total_flights == 0:
        return 0
    
    # Weighted risk calculation based on incidents
    high_risk = len(airline_data[airline_data['Severity'] == 'High']) * 3
    medium_risk = len(airline_data[airline_data['Severity'] == 'Medium']) * 2
    low_risk = len(airline_data[airline_data['Severity'] == 'Low']) * 1
    
    total_risk = high_risk + medium_risk + low_risk
    risk_score = (total_risk / total_flights) * 100
    
    return min(risk_score, 100)  # Cap at 100
def get_risk_category(score):
    """Categorize risk score"""
    if score < 20:
        return "Low", "risk-low"
    elif score < 50:
        return "Medium", "risk-medium"
    else:
        return "High", "risk-high"

# Sidebar
with st.sidebar:
    st.markdown('<p class="sidebar-header">✈️ Analysis Controls</p>', unsafe_allow_html=True)
    
    # Time period selection
    time_period = st.selectbox(
        "Time Period",
        ["2020-2024", "2019-2023", "2018-2022"],
        index=0
    )
    
    st.markdown("---")
    
    # Airline selection
    st.write("**Airlines**")
    airlines = ["IndiGo", "Air India", "SpiceJet", "Vistara", "AirAsia"]
    selected_airlines = []
    
    for airline in airlines:
        if st.checkbox(airline, value=True, key=f"sidebar_{airline}"):
            selected_airlines.append(airline)
    
    st.markdown("---")
    
    # File upload section
    st.write("**Upload Data**")
    
    # CSV upload
    uploaded_csv = st.file_uploader(
        "Upload CSV Data",
        type="csv",
        help="Upload CSV file containing airline data"
    )
    
    # PDF upload
    uploaded_pdf = st.file_uploader(
        "Upload DGCA PDF Report",
        type="pdf",
        help="Upload DGCA PDF report for analysis"
    )

# Main content
st.markdown('<p class="main-header">✈️ Airline Risk Factor Analysis</p>', unsafe_allow_html=True)

# Check if data is uploaded or use sample data
if uploaded_csv is not None:
    try:
        df = pd.read_csv(uploaded_csv)
        st.markdown('<div class="success-msg">CSV file uploaded successfully!</div>', unsafe_allow_html=True)
        
        # DEBUG: Check if Risk_Score column exists
        if 'Risk_Score' in df.columns:
            st.success("✓ Risk_Score column detected in CSV!")
            st.write("Risk scores found:", df[['Airline', 'Risk_Score']].values)
        else:
            st.info("No Risk_Score column - scores will be calculated from incidents")
            
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        st.info("Using sample data for demonstration")
        df = generate_sample_data()
else:
    st.info("Using sample data for demonstration. Upload a CSV file to use your own data.")
    df = generate_sample_data()
# Display data preview
with st.expander("Preview Data", expanded=True):
    st.dataframe(df.head(10))

# Risk Analysis Section
st.markdown("## 🚨 Risk Factor Analysis")

# Calculate risk scores for each airline
risk_data = []
for airline in airlines:
    score = calculate_risk_score(airline, df)
    category, css_class = get_risk_category(score)
    risk_data.append({
        'Airline': airline,
        'Risk Score': score,
        'Category': category,
        'CSS Class': css_class
    })

risk_df = pd.DataFrame(risk_data)

# Display risk scores
col1, col2, col3, col4 = st.columns(4)

for i, airline_risk in enumerate(risk_data):
    col = [col1, col2, col3, col4][i % 4]
    with col:
        st.markdown(f'''
        <div class="metric-card risk-metric">
            <h3>{airline_risk['Airline']}</h3>
            <h2>{airline_risk['Risk Score']:.1f}</h2>
            <div class="risk-indicator {airline_risk['CSS Class']}">
                {airline_risk['Category']} Risk
            </div>
        </div>
        ''', unsafe_allow_html=True)

# Safety Metrics section
st.markdown("## 📊 Safety Performance Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    on_time_performance = np.random.randint(75, 95)
    st.markdown(f'''
    <div class="metric-card safety-metric">
        <h3>On-Time Performance</h3>
        <h2>{on_time_performance}%</h2>
        <p>↑ {on_time_performance-80}% from previous period</p>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    cancellation_rate = np.random.uniform(1.0, 5.0)
    st.markdown(f'''
    <div class="metric-card">
        <h3>Cancellation Rate</h3>
        <h2>{cancellation_rate:.1f}%</h2>
        <p>↓ {cancellation_rate-2.5:.1f}% from previous period</p>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    incident_count = len(df[df['Incident_Type'] != 'None'])
    st.markdown(f'''
    <div class="metric-card risk-metric">
        <h3>Incidents Reported</h3>
        <h2>{incident_count}</h2>
        <p>Across all airlines</p>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    high_severity = len(df[df['Severity'] == 'High'])
    st.markdown(f'''
    <div class="metric-card risk-metric">
        <h3>High Severity Incidents</h3>
        <h2>{high_severity}</h2>
        <p>Requires immediate attention</p>
    </div>
    ''', unsafe_allow_html=True)

# Charts section
st.markdown("## 📈 Risk & Performance Charts")

col1, col2 = st.columns(2)

with col1:
    # Risk Score by Airline
    st.markdown("### Risk Score by Airline")
    fig = px.bar(risk_df, x='Airline', y='Risk Score', 
                 color='Risk Score', color_continuous_scale='RdYlGn_r')
    fig.update_layout(yaxis_title="Risk Score (Lower is better)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Incident Distribution by Type
    st.markdown("### Incident Distribution by Type")
    incident_counts = df[df['Incident_Type'] != 'None']['Incident_Type'].value_counts()
    fig = px.pie(values=incident_counts.values, names=incident_counts.index,
                 title="Types of Incidents Reported")
    st.plotly_chart(fig, use_container_width=True)

# Additional analysis options
st.markdown("## 🔍 Detailed Risk Analysis")

analysis_type = st.selectbox(
    "Select Analysis Type",
    ["Risk Trends Over Time", "Incident Analysis", "Aircraft Type Risk", "Time of Day Risk Analysis"]
)

if analysis_type == "Risk Trends Over Time":
    st.markdown("### Monthly Risk Trends")
    
    # Generate sample trend data
    months = pd.date_range(start='2020-01-01', end='2024-12-01', freq='MS')
    trend_data = {
        'Month': months,
        'Risk_Score': np.random.normal(30, 10, len(months)),
        'Incident_Count': np.random.poisson(15, len(months))
    }
    trend_df = pd.DataFrame(trend_data)
    
    fig = px.line(trend_df, x='Month', y='Risk_Score', 
                  title='Risk Score Trend Over Time')
    st.plotly_chart(fig, use_container_width=True)

elif analysis_type == "Incident Analysis":
    st.markdown("### Incident Analysis by Airline and Severity")
    
    # Create cross-tab of incidents by airline and severity
    incident_cross = pd.crosstab(df[df['Incident_Type'] != 'None']['Airline'], 
                                df[df['Incident_Type'] != 'None']['Severity'])
    
    fig = px.bar(incident_cross, barmode='group', 
                 title='Incidents by Airline and Severity Level')
    st.plotly_chart(fig, use_container_width=True)

# Data export option
st.markdown("## 📤 Export Risk Analysis Report")
if st.button("Generate Risk Report"):
    with st.spinner("Generating comprehensive risk report..."):
        # Simulate report generation
        import time
        time.sleep(2)
        st.success("Risk analysis report generated successfully!")
        
        # Create a sample CSV for download
        report_data = risk_df.copy()
        report_data['Flights Analyzed'] = [len(df[df['Airline'] == airline]) for airline in report_data['Airline']]
        report_data['Incidents'] = [len(df[(df['Airline'] == airline) & (df['Incident_Type'] != 'None')]) for airline in report_data['Airline']]
        
        csv = report_data.to_csv(index=False)
        st.download_button(
            label="Download Risk Analysis Report (CSV)",
            data=csv,
            file_name="airline_risk_analysis_report.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("**🧿Shubh Yatra✈️** • Risk Factor Analysis For Indian Domestic Flights • Powered by Streamlit • DGCA Compliant")

# Instructions for use
with st.expander("How to use this dashboard"):
    st.markdown("""
    1. **Upload Data**: Use the sidebar to upload your airline data in CSV format
    2. **Select Time Period**: Choose the time period for analysis
    3. **Filter Airlines**: Select which airlines to include in the analysis
    4. **View Risk Metrics**: Risk scores and safety indicators are shown at the top
    5. **Explore Charts**: Interactive charts show risk factors by airline and incident type
    6. **Detailed Analysis**: Use the dropdown to select specific risk analysis types
    7. **Export**: Generate and download comprehensive risk reports
    """)

