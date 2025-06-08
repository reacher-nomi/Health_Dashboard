# database.py
import pymysql
import OS

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',          # use your XAMPP MySQL username
        password='',          # or 'root' or any password you've set
        database='gesundheit_board'
    )

    conn = get_connection()
    print("Connected to database")

db_path = os.path.join(os.path.dirname(__file__), "Database", "gesundheit_dashboard")
