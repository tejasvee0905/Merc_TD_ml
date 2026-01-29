# Weather Temperature Prediction - Streamlit Frontend
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Weather Temperature Prediction",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .stMetric {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2E2E2E;
    }
    h1, h2, h3 {
        color: #FFFFFF;
        font-weight: 300;
        letter-spacing: 1px;
    }
    .prediction-box {
        background-color: #1E1E1E;
        padding: 30px;
        border-radius: 12px;
        border: 2px solid #3498db;
        text-align: center;
        margin: 20px 0;
    }
    .big-temp {
        font-size: 72px;
        font-weight: bold;
        color: #3498db;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>🌡️ WEATHER TEMPERATURE PREDICTION</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8B8B8B; margin-bottom: 40px;'>AI-Powered Temperature Forecasting System</p>", unsafe_allow_html=True)

# Add button to view history
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("📊 View Prediction History", use_container_width=True):
        st.info("💡 To view prediction history, run: `streamlit run view_history.py` in another terminal")

# Sidebar for input
st.sidebar.markdown("### 📊 Weather Parameters")
st.sidebar.markdown("---")

humidity = st.sidebar.slider(
    "Humidity (%)",
    min_value=0.0,
    max_value=100.0,
    value=60.0,
    step=0.1,
    help="Relative humidity percentage"
)

pressure = st.sidebar.slider(
    "Atmospheric Pressure (hPa)",
    min_value=950.0,
    max_value=1050.0,
    value=1013.0,
    step=0.1,
    help="Atmospheric pressure in hectopascals"
)

wind_speed = st.sidebar.slider(
    "Wind Speed (km/h)",
    min_value=0.0,
    max_value=50.0,
    value=15.0,
    step=0.1,
    help="Wind speed in kilometers per hour"
)

cloud_cover = st.sidebar.slider(
    "Cloud Cover (%)",
    min_value=0.0,
    max_value=100.0,
    value=45.0,
    step=0.1,
    help="Percentage of sky covered by clouds"
)

rainfall = st.sidebar.slider(
    "Rainfall (mm)",
    min_value=0.0,
    max_value=50.0,
    value=5.0,
    step=0.1,
    help="Rainfall in millimeters"
)

sunshine_hours = st.sidebar.slider(
    "Sunshine Hours",
    min_value=0.0,
    max_value=12.0,
    value=6.5,
    step=0.1,
    help="Hours of sunshine per day"
)

st.sidebar.markdown("---")

# API endpoint (can be changed if API is running on different port)
API_URL = "http://localhost:5000/predict"

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Current Weather Conditions")
    
    # Display metrics in a grid
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.metric("Humidity", f"{humidity}%")
        st.metric("Pressure", f"{pressure} hPa")
    
    with metric_col2:
        st.metric("Wind Speed", f"{wind_speed} km/h")
        st.metric("Cloud Cover", f"{cloud_cover}%")
    
    with metric_col3:
        st.metric("Rainfall", f"{rainfall} mm")
        st.metric("Sunshine", f"{sunshine_hours} hrs")

with col2:
    st.markdown("### Quick Info")
    
    # Weather condition description
    if rainfall > 20:
        weather_desc = "🌧️ Heavy Rain"
    elif rainfall > 5:
        weather_desc = "🌦️ Rainy"
    elif cloud_cover > 75:
        weather_desc = "☁️ Cloudy"
    elif cloud_cover > 50:
        weather_desc = "⛅ Partly Cloudy"
    else:
        weather_desc = "☀️ Clear Sky"
    
    st.info(f"**Condition:** {weather_desc}")
    
    if wind_speed > 30:
        st.warning("⚠️ Strong winds")
    elif humidity > 80:
        st.info("💧 High humidity")

st.markdown("---")

# Prediction button
if st.button("🔮 PREDICT TEMPERATURE", use_container_width=True):
    with st.spinner("Analyzing weather conditions..."):
        try:
            # Prepare data for API
            data = {
                'humidity_percent': humidity,
                'pressure_hpa': pressure,
                'wind_speed_kmph': wind_speed,
                'cloud_cover_percent': cloud_cover,
                'rainfall_mm': rainfall,
                'sunshine_hours': sunshine_hours
            }
            
            # Make API request
            response = requests.post(API_URL, json=data, timeout=5)
            
            if response.status_code == 200:
                result = response.json()
                predicted_temp = result['predicted_temperature']
                prediction_id = result.get('prediction_id', 'N/A')
                
                # Display prediction
                st.success(f"✅ Prediction saved to database (ID: {prediction_id})")
                st.markdown("<br>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"""
                        <div class='prediction-box'>
                            <h3 style='color: #8B8B8B; margin-bottom: 10px;'>PREDICTED TEMPERATURE</h3>
                            <div class='big-temp'>{predicted_temp}°C</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Temperature gauge with better design
                fig_gauge = go.Figure()
                
                fig_gauge.add_trace(go.Indicator(
                    mode="gauge+number+delta",
                    value=predicted_temp,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "<b>Temperature Prediction</b>", 'font': {'color': '#FFFFFF', 'size': 20}},
                    delta={'reference': 60, 'suffix': '°C'},
                    number={'suffix': '°C', 'font': {'size': 50, 'color': '#3498db'}},
                    gauge={
                        'axis': {
                            'range': [None, 100], 
                            'tickwidth': 2, 
                            'tickcolor': '#FFFFFF',
                            'tickfont': {'size': 14}
                        },
                        'bar': {'color': '#3498db', 'thickness': 0.75},
                        'bgcolor': 'rgba(0,0,0,0)',
                        'borderwidth': 3,
                        'bordercolor': '#3498db',
                        'steps': [
                            {'range': [0, 30], 'color': '#1e3a5f', 'name': 'Cold'},
                            {'range': [30, 45], 'color': '#2c5282', 'name': 'Cool'},
                            {'range': [45, 60], 'color': '#48c9b0', 'name': 'Moderate'},
                            {'range': [60, 75], 'color': '#f39c12', 'name': 'Warm'},
                            {'range': [75, 100], 'color': '#e74c3c', 'name': 'Hot'}
                        ],
                        'threshold': {
                            'line': {'color': '#FFFFFF', 'width': 6},
                            'thickness': 0.85,
                            'value': predicted_temp
                        }
                    }
                ))
                
                fig_gauge.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#FFFFFF', 'size': 14},
                    height=350,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                # Temperature interpretation
                st.markdown("### 📊 Analysis")
                
                if predicted_temp < 40:
                    st.success("❄️ **Cool Temperature** - Pleasant weather conditions")
                elif predicted_temp < 60:
                    st.info("🌤️ **Moderate Temperature** - Comfortable weather")
                else:
                    st.warning("🔥 **Warm Temperature** - Hot weather conditions")
                
                # Feature contribution visualization
                st.markdown("### 🎯 Input Parameters Analysis")
                
                col_viz1, col_viz2 = st.columns(2)
                
                with col_viz1:
                    # Radial/Polar chart for parameters
                    features_normalized = {
                        'Humidity': humidity,
                        'Pressure': (pressure - 950) / (1050 - 950) * 100,
                        'Wind Speed': wind_speed * 2,
                        'Cloud Cover': cloud_cover,
                        'Rainfall': rainfall * 2,
                        'Sunshine': sunshine_hours * 8.33
                    }
                    
                    fig_radar = go.Figure()
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=list(features_normalized.values()),
                        theta=list(features_normalized.keys()),
                        fill='toself',
                        fillcolor='rgba(52, 152, 219, 0.3)',
                        line=dict(color='#3498db', width=3),
                        marker=dict(size=8, color='#5dade2'),
                        name='Current Values'
                    ))
                    
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 100],
                                gridcolor='#2E2E2E',
                                tickfont=dict(color='#8B8B8B')
                            ),
                            angularaxis=dict(
                                gridcolor='#2E2E2E',
                                tickfont=dict(color='#FFFFFF', size=12)
                            ),
                            bgcolor='rgba(0,0,0,0)'
                        ),
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#FFFFFF', size=12),
                        title=dict(
                            text='<b>Parameter Distribution</b>',
                            font=dict(size=16, color='#FFFFFF'),
                            x=0.5,
                            xanchor='center'
                        ),
                        height=400
                    )
                    
                    st.plotly_chart(fig_radar, use_container_width=True)
                
                with col_viz2:
                    # Waterfall chart showing parameter influence estimation
                    features_df = pd.DataFrame({
                        'Feature': ['Base', 'Humidity', 'Pressure', 'Wind', 'Cloud', 'Rain', 'Sun', 'Total'],
                        'Value': [50, 
                                 -humidity*0.15, 
                                 (pressure-1013)*0.02,
                                 -wind_speed*0.1,
                                 -cloud_cover*0.05,
                                 -rainfall*0.3,
                                 sunshine_hours*1.5,
                                 predicted_temp],
                        'Type': ['Base'] + ['Relative']*6 + ['Total']
                    })
                    
                    fig_waterfall = go.Figure(go.Waterfall(
                        orientation='v',
                        measure=['relative', 'relative', 'relative', 'relative', 'relative', 'relative', 'relative', 'total'],
                        x=features_df['Feature'],
                        y=features_df['Value'],
                        text=[f"{v:.1f}°C" for v in features_df['Value']],
                        textposition='outside',
                        connector={'line': {'color': '#3498db'}},
                        decreasing={'marker': {'color': '#5dade2'}},
                        increasing={'marker': {'color': '#48c9b0'}},
                        totals={'marker': {'color': '#3498db'}}
                    ))
                    
                    fig_waterfall.update_layout(
                        title=dict(
                            text='<b>Temperature Build-up</b>',
                            font=dict(size=16, color='#FFFFFF'),
                            x=0.5,
                            xanchor='center'
                        ),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#FFFFFF', size=11),
                        xaxis=dict(showgrid=False, tickfont=dict(size=10)),
                        yaxis=dict(showgrid=True, gridcolor='#2E2E2E', title='Temperature (°C)'),
                        height=400,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig_waterfall, use_container_width=True)
                
            else:
                st.error(f"❌ API Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ **Connection Error**: Cannot connect to the API server. Please make sure the Flask API is running on port 5000.")
            st.info("💡 **To start the API**: Run `python weather_api.py` in your terminal")
        except requests.exceptions.Timeout:
            st.error("❌ **Timeout Error**: The API request took too long.")
        except Exception as e:
            st.error(f"❌ **Error**: {str(e)}")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8B8B8B; font-size: 12px;'>Weather Temperature Prediction System | Powered by Machine Learning</p>", unsafe_allow_html=True)
