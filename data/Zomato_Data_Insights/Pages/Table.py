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

st.title("Table View")

tables = db_manager.fetch_tables()

if tables:
    selected_table = st.selectbox("Select a Table", tables)
    if selected_table:
        data = db_manager.fetch_data_as_dataframe(f"SELECT * FROM {selected_table}")
        if not data.empty:
            st.dataframe(data)
        else:
            st.write("No data found in the table.")
else:
    st.write("No tables found in the database.")
