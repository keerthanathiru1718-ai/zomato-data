import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to import classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from class_DatabaseManager import DatabaseManager

try:
    db_manager = DatabaseManager()
    st.success("Database connection established successfully.")
except Exception as e:
    st.error(f"Failed to connect to the database: {e}")
    st.stop()

st.title("Query View")


sql_queries = [
    "SELECT location AS Peak_Order_Locations FROM customers WHERE total_orders = (SELECT max(total_orders) FROM customers);",
    "SELECT preferred_cuisine, count(*) AS customer_count, sum(total_orders) AS most_ordered FROM customers GROUP BY preferred_cuisine ORDER BY most_ordered DESC;",
    "SELECT customer_id, count(*) AS total_orders FROM orders GROUP BY customer_id ORDER BY total_orders DESC;",
    "SELECT is_premium, AVG(total_orders) AS average_orders, AVG(average_rating) AS average_rating FROM customers GROUP BY is_premium;",
    "SELECT name, email, total_orders FROM customers WHERE total_orders > 5 ORDER BY total_orders DESC;",
    "SELECT average_rating, AVG(total_orders) as average_orders FROM customers GROUP BY average_rating ORDER BY average_rating DESC;",
    "SELECT is_premium, count(*) as customer_count, sum(total_orders) as total_orders FROM customers GROUP BY is_premium ORDER BY total_orders DESC;",
    "SELECT name, total_orders, average_rating FROM customers WHERE total_orders > 3 AND average_rating >= 4 ORDER BY total_orders DESC;",
    "SELECT name, sum(total_orders) AS orders_list FROM restaurants GROUP by name ORDER by orders_list DESC;",
    "SELECT extract(HOUR FROM order_date) as order_hour,count(*) as total_orders FROM orders GROUP BY extract(HOUR FROM order_date) ORDER BY total_orders DESC;",
    "SELECT DATE(order_date) AS order_day, count(*) AS total_orders FROM orders GROUP BY DATE(order_date) ORDER BY total_orders DESC;",
    "SELECT status AS popular_status, count(*) as total_orders FROM orders GROUP BY status ORDER BY total_orders DESC;",

    "SELECT payment_mode, count(*) AS total_orders FROM orders GROUP BY payment_mode ORDER BY total_orders DESC;",
    "SELECT discount_applied, count(*) AS total_orders FROM orders GROUP BY discount_applied ORDER BY total_orders DESC;",
    "SELECT * FROM deliveries WHERE delivery_time > estimated_time AND delivery_status != 'Cancelled';",
    "SELECT * FROM deliveries WHERE delivery_status = 'Cancelled';",
    "SELECT vehicle_type, count(*) as Frequency FROM deliveries GROUP BY vehicle_type ORDER BY Frequency DESC;",
    "SELECT AVG(delivery_time) AS Average_Time_Taken FROM deliveries ORDER BY Average_Time_Taken;",
    "SELECT AVG(delivery_fee) AS Average_Delivery_Fee FROM deliveries ORDER BY Average_Delivery_Fee;",
    "SELECT AVG(distance) AS Average_Distance_Covered FROM deliveries ORDER BY Average_Distance_Covered;",
]
query_title = ["Peak Ordering Locations","Analyzing Customer Preferences","Top Customer Preferences","Customer Segmentation","Active Customers","Rating vs Orders","Customer Retention Patterns","High Value Customers","Frequent Restaurant Ordered","Peak Orderings of the Day",
               "Order Trends Over Time","Analyzing popular status","Top Payment Methods","Frequent Discount Usage","Tracking Delay Deliveries","Tracking Cancelled Deliveries","Frequent Vehicle Used for Delivery","Average Delivery Time","Average Delivery fee","Average Distance Covered"]

query_dict = {title: sql_queries[i] for i, title in enumerate(query_title)}

select_query = st.selectbox("Select A Query", query_title)

if select_query in query_dict:
    df = db_manager.fetch_data_as_dataframe(query_dict[select_query])
    st.dataframe(df)