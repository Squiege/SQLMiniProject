import mysql.connector
from mysql.connector import Error

# Database connection parameters
def connect_database():
    # Database access
    db_name = "library_db"
    user = "root"
    password = "@Deblin312145"
    host = "localhost"

    try:
        # Connecting into the database
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        # Confirming the database has been connected
        if conn.is_connected():
            print("Connected to MySQL database successfully!")
            return conn

    # Error Handling
    except Error as e:
        print(f"Error: {e}")
        return None