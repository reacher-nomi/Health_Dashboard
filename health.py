# health.py
import mysql
from database import get_connection
from datetime import date

def calculate_bmi(weight, height_cm):
    try:
        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)
        return round(bmi, 2)
    except ZeroDivisionError:
        return 0

def save_health_record(user_id, weight, height, blood_group, mental_health_status):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Calculate BMI and save the health record
        bmi = calculate_bmi(weight, height)
        record_date = date.today()

        sql = """
        INSERT INTO health_records (user_id, weight, height, blood_group, mental_health_status, BMI, record_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (user_id, weight, height, blood_group, mental_health_status, bmi, record_date))
        conn.commit()
        return True, f"Health record saved. BMI: {bmi}"
    
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()


def get_latest_health_record(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        print(f"Fetching latest health record for user_id: {user_id}")

        cursor.execute("""
        SELECT weight, height, blood_group, mental_health_status, BMI, record_date
        FROM health_records
        WHERE user_id = %s
        ORDER BY record_date DESC
        LIMIT 1
        """, (user_id,))

        record = cursor.fetchone()
        if record is None:
            print(f"No health records found for the given: {user_id}.")
            return None

        print(f"Query result: {record}")
        return record
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()
