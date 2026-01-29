import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    .metric-label {
        color: #8B8B8B;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('sales.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
    df['Month'] = df['Date'].dt.month_name()
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M').dt.hour
    return df

df = load_data()

# Header
st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>SALES ANALYTICS</h1>", unsafe_allow_html=True)

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Revenue", f"${df['Total'].sum():,.0f}")
with col2:
    st.metric("Total Transactions", f"{len(df):,}")
with col3:
    st.metric("Avg Transaction", f"${df['Total'].mean():.2f}")
with col4:
    st.metric("Avg Rating", f"{df['Rating'].mean():.1f} ⭐")

st.markdown("<br>", unsafe_allow_html=True)

# Revenue by Branch and City
col1, col2 = st.columns(2)

with col1:
    branch_revenue = df.groupby('Branch')['Total'].sum().reset_index()
    fig_branch = px.bar(
        branch_revenue,
        x='Branch',
        y='Total',
        title='Revenue by Branch',
        color='Total',
        color_continuous_scale=['#1f77b4', '#3498db', '#5dade2']
    )
    fig_branch.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', size=12),
        title_font=dict(size=16, color='#FFFFFF'),
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2E2E2E')
    )
    st.plotly_chart(fig_branch, use_container_width=True)

with col2:
    city_revenue = df.groupby('City')['Total'].sum().reset_index()
    fig_city = px.pie(
        city_revenue,
        values='Total',
        names='City',
        title='Revenue Distribution by City',
        hole=0.4,
        color_discrete_sequence=['#1f77b4', '#3498db', '#5dade2']
    )
    fig_city.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', size=12),
        title_font=dict(size=16, color='#FFFFFF')
    )
    st.plotly_chart(fig_city, use_container_width=True)

# Product Line Analysis
col1, col2 = st.columns(2)

with col1:
    product_revenue = df.groupby('Product line')['Total'].sum().sort_values(ascending=True).reset_index()
    fig_product = px.bar(
        product_revenue,
        x='Total',
        y='Product line',
        orientation='h',
        title='Revenue by Product Line',
        color='Total',
        color_continuous_scale=['#1f77b4', '#3498db', '#5dade2']
    )
    fig_product.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', size=12),
        title_font=dict(size=16, color='#FFFFFF'),
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor='#2E2E2E'),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_product, use_container_width=True)

with col2:
    payment_dist = df.groupby('Payment')['Total'].sum().reset_index()
    fig_payment = px.pie(
        payment_dist,
        values='Total',
        names='Payment',
        title='Payment Method Distribution',
        hole=0.4,
        color_discrete_sequence=['#1f77b4', '#3498db', '#5dade2']
    )
    fig_payment.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', size=12),
        title_font=dict(size=16, color='#FFFFFF')
    )
    st.plotly_chart(fig_payment, use_container_width=True)

# Customer Insights
col1, col2 = st.columns(2)

with col1:
    gender_revenue = df.groupby('Gender')['Total'].sum().reset_index()
    fig_gender = px.bar(
        gender_revenue,
        x='Gender',
        y='Total',
        title='Revenue by Gender',
        color='Gender',
        color_discrete_map={'Male': '#3498db', 'Female': '#5dade2'}
    )
    fig_gender.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', size=12),
        title_font=dict(size=16, color='#FFFFFF'),
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2E2E2E')
    )
    st.plotly_chart(fig_gender, use_container_width=True)

with col2:
    customer_type = df.groupby('Customer type')['Total'].sum().reset_index()
    fig_customer = px.bar(
        customer_type,
        x='Customer type',
        y='Total',
        title='Revenue by Customer Type',
        color='Customer type',
        color_discrete_map={'Member': '#3498db', 'Normal': '#5dade2'}
    )
    fig_customer.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', size=12),
        title_font=dict(size=16, color='#FFFFFF'),
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2E2E2E')
    )
    st.plotly_chart(fig_customer, use_container_width=True)

# Time-based Analysis
col1, col2 = st.columns(2)

with col1:
    hourly_sales = df.groupby('Hour')['Total'].sum().reset_index()
    fig_hourly = px.line(
        hourly_sales,
        x='Hour',
        y='Total',
        title='Sales by Hour of Day',
        markers=True
    )
    fig_hourly.update_traces(line_color='#3498db', marker_color='#5dade2')
    fig_hourly.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', size=12),
        title_font=dict(size=16, color='#FFFFFF'),
        xaxis=dict(showgrid=True, gridcolor='#2E2E2E'),
        yaxis=dict(showgrid=True, gridcolor='#2E2E2E')
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

with col2:
    rating_dist = df['Rating'].value_counts().sort_index().reset_index()
    rating_dist.columns = ['Rating', 'Count']
    fig_rating = px.bar(
        rating_dist,
        x='Rating',
        y='Count',
        title='Rating Distribution',
        color='Count',
        color_continuous_scale=['#1f77b4', '#3498db', '#5dade2']
    )
    fig_rating.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', size=12),
        title_font=dict(size=16, color='#FFFFFF'),
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2E2E2E')
    )
    st.plotly_chart(fig_rating, use_container_width=True)

# Top Products by Quantity
st.markdown("<br>", unsafe_allow_html=True)
top_products = df.groupby('Product line')['Quantity'].sum().sort_values(ascending=False).reset_index()
fig_top_qty = px.bar(
    top_products,
    x='Product line',
    y='Quantity',
    title='Total Quantity Sold by Product Line',
    color='Quantity',
    color_continuous_scale=['#1f77b4', '#3498db', '#5dade2']
)
fig_top_qty.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#FFFFFF', size=12),
    title_font=dict(size=16, color='#FFFFFF'),
    showlegend=False,
    xaxis=dict(showgrid=False, tickangle=-45),
    yaxis=dict(showgrid=True, gridcolor='#2E2E2E'),
    height=400
)
st.plotly_chart(fig_top_qty, use_container_width=True)