import mysql.connector
try:
    conn = mysql.connector.connect(user='root', password='123456', host='localhost', database='zomato_db')
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Tables in zomato_db:", tables)
    cursor.close()
    conn.close()
except Exception as e:
    print("Error:", e)
