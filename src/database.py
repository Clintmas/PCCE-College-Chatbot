
import sqlite3
from pathlib import Path


# 1. Define database location
BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "college.db"


# 2. Create database connection
def get_connection():

    connection = sqlite3.connect(DB_PATH)

    return connection


# 3. Create database tables
def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    # Table for general college information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS college_details (
            topic TEXT PRIMARY KEY,
            information TEXT NOT NULL
        )
    """)

    # Table for available courses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_name TEXT PRIMARY KEY,
            level TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


# 4. Insert college information
def insert_college_details():

    connection = get_connection()

    cursor = connection.cursor()

    details = [
        (
            "address",
            "Agnel Technical Education Complex, Agnelganv, Verna, Goa - 403722"
        ),
        (
            "email",
            "agnelpcce@gmail.com"
        ),
        (
            "administration_phone",
            "0832-2791267"
        ),
        (
            "exam_cell_phone",
            "0832-2791266"
        ),
        (
            "website",
            "https://pccegoa.edu.in/"
        )
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO college_details
        (topic, information)
        VALUES (?, ?)
    """, details)

    connection.commit()

    connection.close()


# 5. Insert course information
def insert_courses():

    connection = get_connection()

    cursor = connection.cursor()

    courses = [
        ("Mechanical Engineering", "Bachelor's"),
        ("Computer Engineering", "Bachelor's"),
        ("Electronics and Computer Engineering", "Bachelor's"),
        ("Computer Science and Engineering (AI & ML)", "Bachelor's"),
        ("Artificial Intelligence and Data Science", "Master's")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO courses
        (course_name, level)
        VALUES (?, ?)
    """, courses)

    connection.commit()

    connection.close()


# 6. Retrieve all courses
def get_all_courses():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM courses")

    results = cursor.fetchall()

    connection.close()

    return results


# 7. Retrieve specific college information
def get_college_detail(topic):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT information
        FROM college_details
        WHERE topic = ?
    """, (topic,))

    result = cursor.fetchone()

    connection.close()

    return result[0] if result else None


# 8. Initialize the database
def initialize_database():

    create_tables()

    insert_college_details()

    insert_courses()

    print("College database created successfully!")


# Run initialization
if __name__ == "__main__":

    initialize_database()
