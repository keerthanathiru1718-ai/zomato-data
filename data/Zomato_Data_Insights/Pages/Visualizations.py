import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
from scipy.stats import pearsonr

# Add parent directory to path to import classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from class_DatabaseManager import DatabaseManager

# Set page config
st.set_page_config(page_title="Data Visualization", layout="wide")

# Page title
st.title("📊 Data Visualization & Insights")
st.markdown("Comprehensive analysis of Zomato data with various visualization techniques")

try:
    db_manager = DatabaseManager()
    st.success("Database connection established successfully.")
except Exception as e:
    st.error(f"Failed to connect to the database: {e}")
    st.stop()

# Fetch data from database
@st.cache_data
def load_data():
    try:
        customers = pd.read_sql("SELECT * FROM Customers", con=db_manager.connection)
        restaurants = pd.read_sql("SELECT * FROM Restaurants", con=db_manager.connection)
        orders = pd.read_sql("SELECT * FROM Orders", con=db_manager.connection)
        deliveries = pd.read_sql("SELECT * FROM Deliveries", con=db_manager.connection)
        return customers, restaurants, orders, deliveries
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

customers, restaurants, orders, deliveries = load_data()

if customers is None:
    st.stop()

# Create tabs for different visualizations
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Bar Charts",
    "🥧 Pie Charts",
    "🔥 Heatmaps",
    "📊 Count Plots",
    "📉 Correlations"
])

# ============= TAB 1: BAR CHARTS =============
with tab1:
    st.header("Bar Chart Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Restaurants by Rating")
        top_restaurants = restaurants.nlargest(10, 'rating')[['name', 'rating', 'total_orders']]
        
        fig = px.bar(
            top_restaurants,
            x='rating',
            y='name',
            orientation='h',
            color='rating',
            color_continuous_scale='viridis',
            hover_data=['total_orders'],
            title="Top Restaurants by Rating"
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Top 10 Restaurants by Orders")
        top_order_restaurants = restaurants.nlargest(10, 'total_orders')[['name', 'total_orders', 'rating']]
        
        fig = px.bar(
            top_order_restaurants,
            x='total_orders',
            y='name',
            orientation='h',
            color='total_orders',
            color_continuous_scale='plasma',
            hover_data=['rating'],
            title="Top Restaurants by Total Orders"
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Top 10 Locations by Restaurant Count")
        location_counts = restaurants['location'].value_counts().head(10)
        
        fig = px.bar(
            x=location_counts.index,
            y=location_counts.values,
            color=location_counts.values,
            color_continuous_scale='viridis',
            title="Top Locations by Restaurant Count",
            labels={'x': 'Location', 'y': 'Restaurant Count'}
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, width='stretch')
    
    with col4:
        st.subheader("Top 10 Cuisines")
        cuisine_counts = restaurants['cuisine_type'].value_counts().head(10)
        
        fig = px.bar(
            x=cuisine_counts.index,
            y=cuisine_counts.values,
            color=cuisine_counts.values,
            color_continuous_scale='plasma',
            title="Most Popular Cuisines",
            labels={'x': 'Cuisine Type', 'y': 'Count'}
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, width='stretch')
    
    # Average delivery time by cuisine
    col5, col6 = st.columns(2)
    
    with col5:
        st.subheader("Average Delivery Time by Cuisine")
        delivery_by_cuisine = restaurants.groupby('cuisine_type')['average_delivery_time'].mean().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=delivery_by_cuisine.index,
            y=delivery_by_cuisine.values,
            color=delivery_by_cuisine.values,
            color_continuous_scale='rdylbu',
            title="Avg Delivery Time by Cuisine",
            labels={'x': 'Cuisine', 'y': 'Minutes'}
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, width='stretch')
    
    with col6:
        st.subheader("Average Order Value by Status")
        if 'status' in orders.columns and 'total_amount' in orders.columns:
            order_status = orders.groupby('status')['total_amount'].mean()
            
            fig = px.bar(
                x=order_status.index,
                y=order_status.values,
                color=order_status.values,
                color_continuous_scale='viridis',
                title="Average Order Value by Status",
                labels={'x': 'Status', 'y': 'Amount ($)'}
            )
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, width='stretch')

# ============= TAB 2: PIE CHARTS =============
with tab2:
    st.header("Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Order Status Distribution")
        status_dist = orders['status'].value_counts()
        
        fig = px.pie(
            values=status_dist.values,
            names=status_dist.index,
            title="Order Status Distribution",
            hole=0.3
        )
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.subheader("Payment Mode Distribution")
        if 'payment_mode' in orders.columns:
            payment_dist = orders['payment_mode'].value_counts()
            
            fig = px.pie(
                values=payment_dist.values,
                names=payment_dist.index,
                title="Payment Mode Distribution",
                hole=0.3
            )
            st.plotly_chart(fig, width='stretch')
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Active vs Inactive Restaurants")
        active_dist = restaurants['is_active'].value_counts()
        labels = ['Active', 'Inactive']
        
        fig = px.pie(
            values=active_dist.values,
            names=labels,
            title="Restaurant Activity Status",
            color_discrete_map={'Active': '#2ecc71', 'Inactive': '#e74c3c'}
        )
        st.plotly_chart(fig, width='stretch')
    
    with col4:
        st.subheader("Premium vs Regular Customers")
        premium_dist = customers['is_premium'].value_counts()
        labels = ['Regular', 'Premium']
        
        fig = px.pie(
            values=premium_dist.values,
            names=labels,
            title="Customer Type Distribution",
            color_discrete_map={False: '#3498db', True: '#f39c12'}
        )
        st.plotly_chart(fig, width='stretch')
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.subheader("Top 8 Cuisine Types")
        cuisine_dist = restaurants['cuisine_type'].value_counts().head(8)
        
        fig = px.pie(
            values=cuisine_dist.values,
            names=cuisine_dist.index,
            title="Cuisine Type Distribution",
        )
        st.plotly_chart(fig, width='stretch')
    
    with col6:
        st.subheader("Top 8 Locations")
        location_dist = restaurants['location'].value_counts().head(8)
        
        fig = px.pie(
            values=location_dist.values,
            names=location_dist.index,
            title="Restaurant Location Distribution",
        )
        st.plotly_chart(fig, width='stretch')

# ============= TAB 3: HEATMAPS =============
with tab3:
    st.header("Heatmap & Correlation Analysis")
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.subheader("Restaurant Metrics Correlation Heatmap")
        
        # Select numeric columns from restaurants
        restaurant_numeric = restaurants[['rating', 'total_orders', 'average_delivery_time']].copy()
        correlation_matrix = restaurant_numeric.corr()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='RdBu_r', 
                    center=0, cbar_kws={'label': 'Correlation'}, ax=ax,
                    vmin=-1, vmax=1, linewidths=1, linecolor='white')
        ax.set_title('Restaurant Metrics Correlation', fontsize=14, fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Key Insights")
        st.info("""
        **Correlation Coefficients:**
        
        🔹 Rating vs Orders: Measures how popular highly-rated restaurants are
        
        🔹 Rating vs Delivery Time: Shows if faster delivery affects ratings
        
        🔹 Orders vs Delivery Time: Shows delivery time impact on order volume
        """)
    
    # Order metrics heatmap
    st.subheader("Order Metrics Heatmap")
    col3, col4 = st.columns([1.2, 1])
    
    with col3:
        order_numeric = orders[['total_amount', 'feedback_rating']].copy()
        order_numeric = order_numeric.dropna()
        
        if len(order_numeric) > 0:
            correlation = order_numeric.corr()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(correlation, annot=True, fmt='.2f', cmap='RdYlGn',
                       center=0, cbar_kws={'label': 'Correlation'}, ax=ax,
                       vmin=-1, vmax=1, linewidths=2, linecolor='white')
            ax.set_title('Order Amount vs Customer Rating', fontsize=14, fontweight='bold')
            st.pyplot(fig)
    
    with col4:
        st.info("""
        **Order Analysis:**
        
        💰 Order Amount vs Rating: Shows if higher spends lead to better satisfaction
        """)
    
    # Delivery metrics heatmap
    st.subheader("Delivery Performance Heatmap")
    col5, col6 = st.columns([1.2, 1])
    
    with col5:
        delivery_numeric = deliveries[['distance', 'delivery_time', 'estimated_time']].copy()
        delivery_numeric = delivery_numeric.dropna()
        
        if len(delivery_numeric) > 0:
            correlation = delivery_numeric.corr()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(correlation, annot=True, fmt='.2f', cmap='YlGnBu',
                       center=0, cbar_kws={'label': 'Correlation'}, ax=ax,
                       linewidths=2, linecolor='white')
            ax.set_title('Delivery Metrics Correlation', fontsize=14, fontweight='bold')
            st.pyplot(fig)
    
    with col6:
        st.info("""
        **Delivery Insights:**
        
        🚚 Distance vs Time: Shows efficiency of delivery
        
        ⏱️ Estimated vs Actual: Shows prediction accuracy
        """)

# ============= TAB 4: COUNT PLOTS =============
with tab4:
    st.header("Frequency Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Orders by Status")
        status_counts = orders['status'].value_counts().sort_values(ascending=True)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(status_counts.index, status_counts.values, color=sns.color_palette('viridis', len(status_counts)))
        ax.set_xlabel('Count', fontsize=12)
        ax.set_title('Order Status Frequency', fontsize=14, fontweight='bold')
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                   f'{int(width)}', ha='left', va='center', fontweight='bold')
        
        st.pyplot(fig)
    
    with col2:
        st.subheader("Delivery Status Frequency")
        if 'delivery_status' in deliveries.columns:
            delivery_status_counts = deliveries['delivery_status'].value_counts().sort_values(ascending=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(delivery_status_counts.index, delivery_status_counts.values, 
                          color=sns.color_palette('plasma', len(delivery_status_counts)))
            ax.set_xlabel('Count', fontsize=12)
            ax.set_title('Delivery Status Frequency', fontsize=14, fontweight='bold')
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2,
                       f'{int(width)}', ha='left', va='center', fontweight='bold')
            
            st.pyplot(fig)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Payment Method Frequency")
        if 'payment_mode' in orders.columns:
            payment_counts = orders['payment_mode'].value_counts().sort_values(ascending=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(payment_counts.index, payment_counts.values, 
                          color=sns.color_palette('Set2', len(payment_counts)))
            ax.set_xlabel('Count', fontsize=12)
            ax.set_title('Payment Method Frequency', fontsize=14, fontweight='bold')
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2,
                       f'{int(width)}', ha='left', va='center', fontweight='bold')
            
            st.pyplot(fig)
    
    with col4:
        st.subheader("Vehicle Type Distribution")
        if 'vehicle_type' in deliveries.columns:
            vehicle_counts = deliveries['vehicle_type'].value_counts().sort_values(ascending=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(vehicle_counts.index, vehicle_counts.values,
                          color=sns.color_palette('Set3', len(vehicle_counts)))
            ax.set_xlabel('Count', fontsize=12)
            ax.set_title('Vehicle Type Frequency', fontsize=14, fontweight='bold')
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height()/2,
                       f'{int(width)}', ha='left', va='center', fontweight='bold')
            
            st.pyplot(fig)

# ============= TAB 5: CORRELATIONS =============
with tab5:
    st.header("Correlation & Statistical Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Restaurant Ratings Distribution")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(restaurants['rating'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Rating', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Distribution of Restaurant Ratings', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add statistics
        mean_rating = restaurants['rating'].mean()
        median_rating = restaurants['rating'].median()
        ax.axvline(mean_rating, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_rating:.2f}')
        ax.axvline(median_rating, color='green', linestyle='--', linewidth=2, label=f'Median: {median_rating:.2f}')
        ax.legend()
        
        st.pyplot(fig)
    
    with col2:
        st.subheader("💰 Order Amount Distribution")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(orders['total_amount'], bins=40, color='lightcoral', edgecolor='black', alpha=0.7)
        ax.set_xlabel('Order Amount ($)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.set_title('Distribution of Order Amounts', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add statistics
        mean_amount = orders['total_amount'].mean()
        median_amount = orders['total_amount'].median()
        ax.axvline(mean_amount, color='blue', linestyle='--', linewidth=2, label=f'Mean: ${mean_amount:.2f}')
        ax.axvline(median_amount, color='purple', linestyle='--', linewidth=2, label=f'Median: ${median_amount:.2f}')
        ax.legend()
        
        st.pyplot(fig)
    
    st.subheader("📈 Statistical Summary")
    
    col3, col4, col5, col6 = st.columns(4)
    
    with col3:
        st.metric(label="Avg Restaurant Rating", value=f"{restaurants['rating'].mean():.2f}/5")
    with col4:
        st.metric(label="Avg Order Amount", value=f"${orders['total_amount'].mean():.2f}")
    with col5:
        st.metric(label="Avg Delivery Time", value=f"{restaurants['average_delivery_time'].mean():.1f} min")
    with col6:
        st.metric(label="Total Orders", value=f"{len(orders):,}")
    
    # Box plots for comparison
    col7, col8 = st.columns(2)
    
    with col7:
        st.subheader("Rating by Active Status")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        active_ratings = restaurants[restaurants['is_active'] == True]['rating']
        inactive_ratings = restaurants[restaurants['is_active'] == False]['rating']
        
        bp = ax.boxplot([active_ratings, inactive_ratings], labels=['Active', 'Inactive'],
                       patch_artist=True, widths=0.6)
        
        for patch, color in zip(bp['boxes'], ['lightgreen', 'lightcoral']):
            patch.set_facecolor(color)
        
        ax.set_ylabel('Rating', fontsize=12)
        ax.set_title('Restaurant Ratings: Active vs Inactive', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig)
    
    with col8:
        st.subheader("Order Value by Premium Status")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Merge orders with customers to get premium status
        orders_with_customer = orders.merge(customers[['customer_id', 'is_premium']], on='customer_id', how='left')
        regular_orders = orders_with_customer[orders_with_customer['is_premium'] == False]['total_amount']
        premium_orders = orders_with_customer[orders_with_customer['is_premium'] == True]['total_amount']
        
        bp = ax.boxplot([regular_orders, premium_orders], labels=['Regular', 'Premium'],
                       patch_artist=True, widths=0.6)
        
        for patch, color in zip(bp['boxes'], ['lightblue', 'gold']):
            patch.set_facecolor(color)
        
        ax.set_ylabel('Order Amount ($)', fontsize=12)
        ax.set_title('Order Value: Regular vs Premium Customers', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig)
    
    # Key metrics
    st.divider()
    st.subheader("Key Correlations & Insights")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.success("""
        ✅ **Top Findings:**
        
        1. **Restaurant Quality**: Average rating shows restaurant quality distribution
        2. **Order Trends**: Order amount distribution reveals customer spending patterns
        3. **Service Performance**: Delivery time correlates with distance
        4. **Customer Behavior**: Premium customers may have different patterns
        """)
    
    with col_right:
        st.info("""
        💡 **Recommendations:**
        
        1. Focus on restaurants with lower ratings for improvement
        2. Optimize delivery times in high-demand areas
        3. Create targeted promotions for order value optimization
        4. Develop premium customer retention strategies
        """)

st.divider()
st.markdown("---")
st.caption("Data Visualization Dashboard | Powered by Streamlit, Plotly & Seaborn")
