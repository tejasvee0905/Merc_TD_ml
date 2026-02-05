import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Customer Segmentation System",
    page_icon="🎯",
    layout="wide"
)

# Load the saved models and preprocessors
@st.cache_resource
def load_models():
    with open('customer_cluster_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    with open('label_encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)
    
    with open('feature_names.pkl', 'rb') as f:
        features = pickle.load(f)
    
    with open('cluster_mapping.pkl', 'rb') as f:
        mapping = pickle.load(f)
    
    return model, scaler, encoders, features, mapping

# Load models
try:
    kmeans_model, scaler, label_encoders, feature_names, cluster_mapping = load_models()
    models_loaded = True
except Exception as e:
    st.error(f"Error loading models: {e}")
    models_loaded = False

# Define cluster offers
CLUSTER_OFFERS = {
    0: {
        "name": "High-Value Loyal Customers",
        "color": "#FF6B6B",
        "icon": "👑",
        "offers": [
            "Exclusive early access to new products",
            "Premium membership with free express delivery",
            "VIP customer support",
            "Personalized shopping experience"
        ]
    },
    1: {
        "name": "Value-Seeking Regular Customers",
        "color": "#4ECDC4",
        "icon": "🎁",
        "offers": [
            "Festival discounts (10–15%)",
            "Loyalty reward points on every purchase",
            "Birthday special offers",
            "Seasonal sale early access"
        ]
    },
    2: {
        "name": "Price-Sensitive Occasional Customers",
        "color": "#45B7D1",
        "icon": "💰",
        "offers": [
            "Flash sales and coupon-based discounts",
            "Free shipping on minimum order value",
            "Special bundle offers",
            "First-time buyer discounts"
        ]
    }
}

# Title and description
st.title("🎯 Customer Segmentation & Personalized Offers")
st.markdown("---")

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select Page", ["Customer Prediction", "Cluster Analytics"])

if page == "Customer Prediction":
    st.header("Enter Customer Details")
    
    if not models_loaded:
        st.warning("⚠️ Models not loaded. Please ensure all pickle files are present.")
    else:
        # Create input form
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            gender = st.selectbox("Gender", ["F", "M"])
            annual_income = st.number_input("Annual Income (₹)", min_value=0, max_value=10000000, value=500000, step=10000)
        
        with col2:
            total_spent = st.number_input("Total Spent (₹)", min_value=0, max_value=5000000, value=100000, step=5000)
            avg_order_value = st.number_input("Average Order Value (₹)", min_value=0, max_value=500000, value=2000, step=100)
            monthly_purchases = st.number_input("Monthly Purchases", min_value=0, max_value=50, value=5)
        
        with col3:
            discount_usage = st.selectbox("Discount Usage", ["High", "Medium", "Low"])
            app_time_minutes = st.number_input("App Time (minutes)", min_value=0, max_value=300, value=45)
            shopping_time = st.selectbox("Preferred Shopping Time", ["Day", "Night"])
        
        # Predict button
        if st.button("🔮 Predict Customer Segment", type="primary", use_container_width=True):
            try:
                # Encode categorical variables
                gender_encoded = label_encoders['le_gender'].transform([gender])[0]
                discount_encoded = label_encoders['le_discount'].transform([discount_usage])[0]
                time_encoded = label_encoders['le_time'].transform([shopping_time])[0]
                
                # Create input array in the same order as training
                input_data = np.array([[
                    age,
                    gender_encoded,
                    annual_income,
                    total_spent,
                    avg_order_value,
                    monthly_purchases,
                    discount_encoded,
                    app_time_minutes,
                    time_encoded
                ]])
                
                # Scale the input
                input_scaled = scaler.transform(input_data)
                
                # Get raw prediction and apply mapping
                cluster_raw = kmeans_model.predict(input_scaled)[0]
                cluster = cluster_mapping[cluster_raw]
                
                # Display results
                st.markdown("---")
                st.success("✅ Prediction Complete!")
                
                cluster_info = CLUSTER_OFFERS[cluster]
                
                # Display cluster information
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown(f"### {cluster_info['icon']} Cluster {cluster}")
                    st.markdown(f"#### **{cluster_info['name']}**")
                    st.markdown(f"<div style='background-color: {cluster_info['color']}; padding: 20px; border-radius: 10px; text-align: center;'>"
                               f"<h2 style='color: white; margin: 0;'>Cluster {cluster}</h2></div>", 
                               unsafe_allow_html=True)
                
                with col2:
                    st.markdown("### 🎁 Personalized Offers")
                    for offer in cluster_info['offers']:
                        st.markdown(f"✅ {offer}")
                
                # Display customer profile
                st.markdown("---")
                st.subheader("📊 Customer Profile Summary")
                
                profile_col1, profile_col2, profile_col3, profile_col4 = st.columns(4)
                
                with profile_col1:
                    st.metric("Annual Income", f"₹{annual_income:,}")
                    st.metric("Age", f"{age} years")
                
                with profile_col2:
                    st.metric("Total Spent", f"₹{total_spent:,}")
                    st.metric("Avg Order Value", f"₹{avg_order_value:,}")
                
                with profile_col3:
                    st.metric("Monthly Purchases", monthly_purchases)
                    st.metric("App Time", f"{app_time_minutes} min")
                
                with profile_col4:
                    st.metric("Discount Usage", discount_usage)
                    st.metric("Shopping Time", shopping_time)
                
            except Exception as e:
                st.error(f"Error during prediction: {e}")

elif page == "Cluster Analytics":
    st.header("📈 Cluster Distribution & Analytics")
    
    if not models_loaded:
        st.warning("⚠️ Models not loaded.")
    else:
        # Load the main dataset for analytics
        try:
            # Try to load the processed data
            df = pd.read_csv('CustomerData.csv')
            from io import StringIO
            with open('CustomerData.csv', 'r') as f:
                lines = [line.strip().strip('"') for line in f.readlines()]
            csv_string = '\n'.join(lines)
            df = pd.read_csv(StringIO(csv_string))
            df.rename(columns={df.columns[0]: 'CustomerID'}, inplace=True)
            
            # Display cluster information
            st.subheader("🎯 Cluster Definitions")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"### {CLUSTER_OFFERS[0]['icon']} Cluster 0")
                st.markdown(f"**{CLUSTER_OFFERS[0]['name']}**")
                st.markdown("**Characteristics:**")
                st.markdown("- High annual income")
                st.markdown("- Very high total spending")
                st.markdown("- Frequent purchases")
                st.markdown("- Low discount usage")
                st.markdown("- Long app usage")
            
            with col2:
                st.markdown(f"### {CLUSTER_OFFERS[1]['icon']} Cluster 1")
                st.markdown(f"**{CLUSTER_OFFERS[1]['name']}**")
                st.markdown("**Characteristics:**")
                st.markdown("- Medium annual income")
                st.markdown("- Moderate spending")
                st.markdown("- Regular purchases")
                st.markdown("- Moderate discount usage")
                st.markdown("- Average app usage")
            
            with col3:
                st.markdown(f"### {CLUSTER_OFFERS[2]['icon']} Cluster 2")
                st.markdown(f"**{CLUSTER_OFFERS[2]['name']}**")
                st.markdown("**Characteristics:**")
                st.markdown("- Low annual income")
                st.markdown("- Low total spending")
                st.markdown("- Infrequent purchases")
                st.markdown("- High discount usage")
                st.markdown("- Short app usage")
            
            st.markdown("---")
            
            # Visualization section
            st.subheader("📊 Visual Analytics")
            
            # Create sample data for visualization (you can load actual cluster data here)
            cluster_data = pd.DataFrame({
                'Cluster': [0, 1, 2],
                'Customer_Count': [25, 45, 30],
                'Avg_Spending': [850000, 320000, 85000],
                'Avg_Income': [1200000, 650000, 350000]
            })
            
            # Customer count visualization
            fig1 = px.bar(cluster_data, x='Cluster', y='Customer_Count',
                         title='Customer Count per Cluster',
                         color='Cluster',
                         color_discrete_map={0: '#FF6B6B', 1: '#4ECDC4', 2: '#45B7D1'},
                         text='Customer_Count')
            fig1.update_traces(textposition='outside')
            st.plotly_chart(fig1, use_container_width=True)
            
            # Spending comparison
            col1, col2 = st.columns(2)
            
            with col1:
                fig2 = px.bar(cluster_data, x='Cluster', y='Avg_Spending',
                             title='Average Spending per Cluster',
                             color='Cluster',
                             color_discrete_map={0: '#FF6B6B', 1: '#4ECDC4', 2: '#45B7D1'})
                st.plotly_chart(fig2, use_container_width=True)
            
            with col2:
                fig3 = px.bar(cluster_data, x='Cluster', y='Avg_Income',
                             title='Average Income per Cluster',
                             color='Cluster',
                             color_discrete_map={0: '#FF6B6B', 1: '#4ECDC4', 2: '#45B7D1'})
                st.plotly_chart(fig3, use_container_width=True)
            
        except Exception as e:
            st.warning(f"Could not load analytics data: {e}")
            st.info("Run the clustering notebook first to generate the necessary data files.")

# Footer
st.markdown("---")
st.markdown("**Customer Segmentation System** | Powered by K-Means Clustering | Built with Streamlit")
