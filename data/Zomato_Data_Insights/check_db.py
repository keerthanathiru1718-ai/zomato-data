import mysql.connector
from config import DB_CONFIG

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Tables in zomato_db:", tables)
    cursor.close()
    conn.close()
except Exception as e:
    print("Error:", e)
