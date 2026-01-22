import mysql.connector as db
import pandas as pd
import os

def setup():
    connection = None
    try:
        # Connect to server
        print("Connecting to MySQL...")
        connection = db.connect(
            user='root',
            password='123456',
            host='127.0.0.1'
        )
        cursor = connection.cursor()
        
        # Create DB
        print("Creating/Using database zomato_db...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS zomato_db")
        cursor.execute("USE zomato_db")
        
        # Create Tables
        print("Creating tables...")
        # Customers
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Customers (
        customer_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone_number VARCHAR(255) NOT NULL,
        location VARCHAR(255),
        signup_date DATE NOT NULL,
        is_premium BOOLEAN DEFAULT FALSE,
        preferred_cuisine VARCHAR(50),
        total_orders INT DEFAULT 0,
        average_rating FLOAT DEFAULT 0.0);
        """)
        
        # Restaurants
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Restaurants (
        restaurant_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        cuisine_type VARCHAR(50),
        location VARCHAR(255),
        owner_name VARCHAR(255),
        average_delivery_time INT DEFAULT 30,
        contact_number VARCHAR(255) NOT NULL,
        rating FLOAT DEFAULT 0.0,
        total_orders INT DEFAULT 0,
        is_active BOOLEAN DEFAULT TRUE);
        """)

        # Orders
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
        order_id VARCHAR(36) PRIMARY KEY,
        customer_id VARCHAR(36) NOT NULL,
        restaurant_id VARCHAR(36) NOT NULL,
        order_date DATETIME NOT NULL,
        delivery_time DATETIME,
        status VARCHAR(50) DEFAULT 'Pending',
        total_amount FLOAT NOT NULL,
        payment_mode VARCHAR(50),
        discount_applied FLOAT DEFAULT 0.0,
        feedback_rating FLOAT DEFAULT NULL,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
        FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id));
        """)

        # Deliveries
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Deliveries (
        delivery_id VARCHAR(36) PRIMARY KEY,
        order_id VARCHAR(36) NOT NULL,
        delivery_status VARCHAR(50) DEFAULT 'On the way',
        distance FLOAT NOT NULL,
        delivery_time INT,
        estimated_time INT,
        delivery_fee FLOAT NOT NULL,
        vehicle_type VARCHAR(50),
        FOREIGN KEY (order_id) REFERENCES Orders(order_id));
        """)

        connection.commit()
        print("Tables structure ensured.")

        # Clean existing data to avoid duplicates
        print("Cleaning old data...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE Deliveries")
        cursor.execute("TRUNCATE TABLE Orders")
        cursor.execute("TRUNCATE TABLE Customers")
        cursor.execute("TRUNCATE TABLE Restaurants")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        connection.commit()
        
        # Load CSVs
        print("Loading CSVs...")
        
        # Customers
        customers = pd.read_csv('Customers.csv')
        # Replace NaN with None for SQL
        customers = customers.where(pd.notnull(customers), None)
        insert_cust = """
        INSERT INTO Customers (customer_id, name, email, phone_number, location, signup_date, is_premium, preferred_cuisine, total_orders, average_rating) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for _, row in customers.iterrows():
             cursor.execute(insert_cust, tuple(row))
             
        # Restaurants
        restaurants = pd.read_csv('Restaurants.csv')
        restaurants = restaurants.where(pd.notnull(restaurants), None)
        insert_rest = """
        INSERT INTO Restaurants (restaurant_id, name, cuisine_type, location, owner_name, average_delivery_time, contact_number, rating, total_orders, is_active) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for _, row in restaurants.iterrows():
             cursor.execute(insert_rest, tuple(row))

        connection.commit()

        # Orders
        orders = pd.read_csv('Orders.csv')
        orders = orders.where(pd.notnull(orders), None)
        
        insert_ord = """
        INSERT INTO Orders (order_id, customer_id, restaurant_id, order_date, delivery_time, status, total_amount, payment_mode, discount_applied, feedback_rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for _, row in orders.iterrows():
             cursor.execute(insert_ord, tuple(row))

        # Deliveries
        deliveries = pd.read_csv('Deliveries.csv')
        deliveries = deliveries.where(pd.notnull(deliveries), None)
        
        insert_del = """
        INSERT INTO Deliveries (delivery_id, order_id, delivery_status, distance, delivery_time, estimated_time, delivery_fee, vehicle_type) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        for _, row in deliveries.iterrows():
             cursor.execute(insert_del, tuple(row))
             
        connection.commit()
        print("Data inserted successfully.")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    setup()
