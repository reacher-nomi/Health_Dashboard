# auth.py
import pymysql
from database import get_connection

def register_user(name, email, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return False, "User already exists."

        # Insert new user
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        conn.commit()
        return True, "Registration successful!"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def get_user_id_by_email(email):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching user id: {e}")
        return None
    finally:
        conn.close()
        
def login_user(email, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch user
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

        return True if user else False
    except Exception as e:
        print(f"Login error: {e}")
        return False
    finally:
        conn.close()
