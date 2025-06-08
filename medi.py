# medication.py
from database import get_connection

def add_medication(user_id, name, dosage, frequency, start_date, end_date, reminder_status):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO medications 
        (user_id, medicine_name, dosage, frequency, start_date, end_date, reminder_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (user_id, name, dosage, frequency, start_date, end_date, reminder_status))
        conn.commit()
        return True, "Medication added successfully."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def get_medications(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        SELECT id, medicine_name, dosage, frequency, start_date, end_date, reminder_status
        FROM medications
        WHERE user_id = %s
        ORDER BY start_date DESC
        """
        cursor.execute(sql, (user_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

def delete_medication(med_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM medications WHERE id = %s"
        cursor.execute(sql, (med_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()
