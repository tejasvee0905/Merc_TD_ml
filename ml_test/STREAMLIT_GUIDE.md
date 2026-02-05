# Customer Segmentation Streamlit App Guide

## 📋 Overview
This Streamlit application provides a user-friendly interface for customer segmentation using the trained K-Means clustering model.

## 🚀 Setup Instructions

### 1. Install Required Packages
```bash
pip install streamlit plotly
```

### 2. Save Model Files
Run the last cell (cell 29) in the `data.ipynb` notebook to generate the required pickle files:
- `customer_cluster_model.pkl` - Trained KMeans model
- `scaler.pkl` - StandardScaler for preprocessing
- `label_encoders.pkl` - Label encoders for categorical variables
- `feature_names.pkl` - Feature names for reference

### 3. Run the Streamlit App
```bash
streamlit run customer_segmentation_app.py
```

The app will open in your default web browser at `http://localhost:8501`

## 🎯 Features

### Page 1: Customer Prediction
- **Input Customer Details:**
  - Age, Gender, Annual Income
  - Total Spent, Average Order Value, Monthly Purchases
  - Discount Usage, App Time, Preferred Shopping Time

- **Get Predictions:**
  - Predicted customer cluster (0, 1, or 2)
  - Customer segment name
  - Personalized offers based on cluster
  - Customer profile summary

### Page 2: Cluster Analytics
- **View Cluster Definitions:**
  - Characteristics of each cluster
  - Customer distribution
  - Average spending and income per cluster

- **Visual Analytics:**
  - Customer count per cluster
  - Average spending comparison
  - Average income comparison

## 🎁 Cluster Offers

### Cluster 0: High-Value Loyal Customers 👑
- Exclusive early access to new products
- Premium membership with free express delivery
- VIP customer support
- Personalized shopping experience

### Cluster 1: Value-Seeking Regular Customers 🎁
- Festival discounts (10–15%)
- Loyalty reward points on every purchase
- Birthday special offers
- Seasonal sale early access

### Cluster 2: Price-Sensitive Occasional Customers 💰
- Flash sales and coupon-based discounts
- Free shipping on minimum order value
- Special bundle offers
- First-time buyer discounts

## 📊 Model Pipeline

1. **Load Models** - Automatically loads saved pickle files
2. **Input Processing** - Encodes categorical variables
3. **Scaling** - Applies StandardScaler transformation
4. **Prediction** - Uses KMeans model to predict cluster
5. **Offer Generation** - Maps cluster to personalized offers
6. **Display Results** - Shows segment and recommendations

## 🛠️ Troubleshooting

### Models Not Loading
- Ensure all pickle files are in the same directory as the app
- Run cell 29 in the notebook to regenerate pickle files

### Import Errors
- Install missing packages: `pip install streamlit plotly pandas numpy scikit-learn`

### Port Already in Use
- Use a different port: `streamlit run customer_segmentation_app.py --server.port 8502`

## 📁 Required Files
```
ml_test/
├── customer_segmentation_app.py  (Streamlit app)
├── customer_cluster_model.pkl     (KMeans model)
├── scaler.pkl                     (StandardScaler)
├── label_encoders.pkl             (Label encoders)
├── feature_names.pkl              (Feature list)
└── CustomerData.csv               (Optional: for analytics)
```

## 🎨 UI Features
- Clean, modern interface
- Color-coded clusters
- Interactive forms
- Real-time predictions
- Visual analytics with Plotly charts
- Responsive design

## 💡 Usage Tips
1. Start with the **Customer Prediction** page to test individual predictions
2. Switch to **Cluster Analytics** to view overall distribution
3. Experiment with different customer profiles to see how offers change
4. Use the metrics to understand customer segments

## 🔒 Deployment Notes
For production deployment, consider:
- Adding authentication
- Implementing API rate limiting
- Storing models in cloud storage
- Using environment variables for configuration
- Adding logging and monitoring
