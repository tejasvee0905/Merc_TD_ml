# Database Viewer - Streamlit Page for Viewing Prediction History
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import get_all_predictions, get_prediction_stats
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Prediction History",
    page_icon="📊",
    layout="wide"
)

# Dark theme CSS
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    h1, h2, h3 {
        color: #FFFFFF;
        font-weight: 300;
        letter-spacing: 1px;
    }
    .stMetric {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2E2E2E;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>📊 PREDICTION HISTORY</h1>", unsafe_allow_html=True)

# Load data
try:
    df = get_all_predictions()
    stats = get_prediction_stats()
    
    if len(df) == 0:
        st.info("📭 No predictions yet. Make some predictions first!")
        st.stop()
    
    # Statistics cards
    st.markdown("### 📈 Overall Statistics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Predictions", f"{stats['total_predictions']:,}")
    with col2:
        st.metric("Avg Temperature", f"{stats['avg_temperature']}°C")
    with col3:
        st.metric("Min Temperature", f"{stats['min_temperature']}°C")
    with col4:
        st.metric("Max Temperature", f"{stats['max_temperature']}°C")
    with col5:
        st.metric("Avg Humidity", f"{stats['avg_humidity']}%")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature over time with moving average
        df_sorted = df.sort_values('timestamp')
        df_sorted['moving_avg'] = df_sorted['predicted_temperature'].rolling(window=min(5, len(df)), min_periods=1).mean()
        
        fig_temp = go.Figure()
        
        # Add actual temperature line
        fig_temp.add_trace(go.Scatter(
            x=df_sorted['timestamp'],
            y=df_sorted['predicted_temperature'],
            mode='lines+markers',
            name='Predicted',
            line=dict(color='#3498db', width=2),
            marker=dict(size=8, color='#5dade2', line=dict(width=2, color='#FFFFFF')),
            hovertemplate='<b>Time:</b> %{x}<br><b>Temp:</b> %{y:.2f}°C<extra></extra>'
        ))
        
        # Add moving average
        fig_temp.add_trace(go.Scatter(
            x=df_sorted['timestamp'],
            y=df_sorted['moving_avg'],
            mode='lines',
            name='Trend',
            line=dict(color='#48c9b0', width=3, dash='dash'),
            hovertemplate='<b>Avg:</b> %{y:.2f}°C<extra></extra>'
        ))
        
        # Add range band
        fig_temp.add_trace(go.Scatter(
            x=df_sorted['timestamp'].tolist() + df_sorted['timestamp'].tolist()[::-1],
            y=(df_sorted['predicted_temperature'] + 2).tolist() + (df_sorted['predicted_temperature'] - 2).tolist()[::-1],
            fill='toself',
            fillcolor='rgba(52, 152, 219, 0.1)',
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig_temp.update_layout(
            title=dict(
                text='<b>Temperature Predictions Timeline</b>',
                font=dict(size=18, color='#FFFFFF'),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF', size=12),
            xaxis=dict(
                showgrid=True, 
                gridcolor='#2E2E2E', 
                title=dict(text='<b>Time</b>', font=dict(size=14))
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='#2E2E2E', 
                title=dict(text='<b>Temperature (°C)</b>', font=dict(size=14))
            ),
            hovermode='x unified',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                bgcolor='rgba(30,30,30,0.8)'
            )
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # Temperature distribution with box and violin plot
        fig_dist = go.Figure()
        
        # Add violin plot
        fig_dist.add_trace(go.Violin(
            y=df['predicted_temperature'],
            name='Distribution',
            box_visible=True,
            meanline_visible=True,
            fillcolor='rgba(52, 152, 219, 0.5)',
            line_color='#3498db',
            opacity=0.8,
            x0='Temperature'
        ))
        
        # Add histogram overlay
        fig_dist.add_trace(go.Histogram(
            y=df['predicted_temperature'],
            name='Frequency',
            marker_color='rgba(93, 173, 226, 0.7)',
            xaxis='x2',
            nbinsy=25,
            showlegend=False
        ))
        
        fig_dist.update_layout(
            title=dict(
                text='<b>Temperature Distribution Analysis</b>',
                font=dict(size=18, color='#FFFFFF'),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF', size=12),
            yaxis=dict(
                showgrid=True, 
                gridcolor='#2E2E2E', 
                title=dict(text='<b>Temperature (°C)</b>', font=dict(size=14))
            ),
            xaxis=dict(showgrid=False, showticklabels=False),
            xaxis2=dict(
                overlaying='x',
                side='top',
                showgrid=False,
                title='Count'
            ),
            showlegend=False
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    # Correlation heatmap
    st.markdown("### 🔥 Feature Correlation with Temperature")
    
    corr_features = ['humidity_percent', 'pressure_hpa', 'wind_speed_kmph', 
                     'cloud_cover_percent', 'rainfall_mm', 'sunshine_hours', 
                     'predicted_temperature']
    
    corr_matrix = df[corr_features].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        title='Correlation Heatmap',
        color_continuous_scale='Blues',
        aspect='auto'
    )
    fig_corr.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', size=12),
        title_font=dict(size=16, color='#FFFFFF')
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Scatter plots
    col1, col2 = st.columns(2)
    
    with col1:
        fig_scatter1 = px.scatter(
            df,
            x='humidity_percent',
            y='predicted_temperature',
            title='Humidity vs Temperature',
            color='predicted_temperature',
            size='rainfall_mm',
            color_continuous_scale=['#1f77b4', '#3498db', '#5dade2', '#48c9b0'],
            trendline='lowess',
            trendline_color_override='#e74c3c',
            hover_data=['rainfall_mm', 'sunshine_hours']
        )
        fig_scatter1.update_traces(
            marker=dict(
                line=dict(width=1, color='#FFFFFF'),
                opacity=0.8
            )
        )
        fig_scatter1.update_layout(
            title=dict(
                text='<b>Humidity Impact on Temperature</b>',
                font=dict(size=18, color='#FFFFFF'),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF', size=12),
            xaxis=dict(
                showgrid=True, 
                gridcolor='#2E2E2E',
                title=dict(text='<b>Humidity (%)</b>', font=dict(size=14))
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='#2E2E2E',
                title=dict(text='<b>Temperature (°C)</b>', font=dict(size=14))
            ),
            coloraxis_colorbar=dict(
                title=dict(text='Temp (°C)', font=dict(size=12))
            )
        )
        st.plotly_chart(fig_scatter1, use_container_width=True)
    
    with col2:
        fig_scatter2 = px.scatter(
            df,
            x='sunshine_hours',
            y='predicted_temperature',
            title='Sunshine Hours vs Temperature',
            color='cloud_cover_percent',
            size='pressure_hpa',
            color_continuous_scale=['#f39c12', '#e74c3c', '#c0392b'],
            trendline='ols',
            trendline_color_override='#48c9b0',
            hover_data=['humidity_percent', 'wind_speed_kmph']
        )
        fig_scatter2.update_traces(
            marker=dict(
                line=dict(width=1, color='#FFFFFF'),
                opacity=0.8
            )
        )
        fig_scatter2.update_layout(
            title=dict(
                text='<b>Sunshine Effect on Temperature</b>',
                font=dict(size=18, color='#FFFFFF'),
                x=0.5,
                xanchor='center'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF', size=12),
            xaxis=dict(
                showgrid=True, 
                gridcolor='#2E2E2E',
                title=dict(text='<b>Sunshine Hours</b>', font=dict(size=14))
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='#2E2E2E',
                title=dict(text='<b>Temperature (°C)</b>', font=dict(size=14))
            ),
            coloraxis_colorbar=dict(
                title=dict(text='Cloud (%)', font=dict(size=12))
            )
        )
        st.plotly_chart(fig_scatter2, use_container_width=True)
    
    # Recent predictions table
    st.markdown("### 📝 Recent Predictions")
    
    # Format timestamp for display
    df_display = df.copy()
    df_display['timestamp'] = pd.to_datetime(df_display['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Reorder columns
    display_columns = ['id', 'timestamp', 'predicted_temperature', 'humidity_percent', 
                      'pressure_hpa', 'wind_speed_kmph', 'cloud_cover_percent', 
                      'rainfall_mm', 'sunshine_hours']
    
    # Show last 20 predictions
    st.dataframe(
        df_display[display_columns].head(20),
        use_container_width=True,
        height=400
    )
    
    # Download button
    st.markdown("### 💾 Export Data")
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download All Predictions as CSV",
        data=csv,
        file_name=f"weather_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Make sure the database has been initialized and predictions have been made.")
