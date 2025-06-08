# appointment.py
from database import get_connection

def add_appointment(user_id, appointment_date, doctor, notes, location):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO appointments (user_id, appointment_date, doctor, notes, location)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (user_id, appointment_date, doctor, notes, location))
        conn.commit()
        return True, "Appointment added successfully."
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def get_appointments(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        SELECT appointment_date, doctor, notes, location
        FROM appointments
        WHERE user_id = %s AND appointment_date >= CURDATE()
        ORDER BY appointment_date ASC
        """
        cursor.execute(sql, (user_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

