import mysql.connector
import csv

def create_connection():
    connection = mysql.connector.connect(
        host='localhost',
        database='attendance_system',
        user='root',
        password='admin'
    )
    if connection.is_connected():
        print("Connected to MySQL database")
        return connection
    else:
        print("Failed to connect to MySQL database")
        return None

def create_table(connection):
    cursor = connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_name VARCHAR(255) NOT NULL,
        date DATE NOT NULL,
        status ENUM('Present', 'Absent') NOT NULL
    )
    """
    cursor.execute(query)
    connection.commit()
    print("Table 'attendance' created successfully.")

def validate_student_name(name):
    return all(char.isalpha() or char.isspace() for char in name)

def validate_date(date):
    parts = date.split('-')
    if len(parts) != 3:
        return False
    year, month, day = parts
    return len(year) == 4 and year.isdigit() and len(month) == 2 and month.isdigit() and 1 <= int(month) <= 12 and len(day) == 2 and day.isdigit() and 1 <= int(day) <= 31

def mark_attendance(connection, student_name, date, status):
    if not validate_student_name(student_name):
        print("Invalid student name. Only alphabetic characters and spaces are allowed.")
        return
    if not validate_date(date):
        print("Invalid date format. Use YYYY-MM-DD.")
        return
    if status not in ["Present", "Absent"]:
        print("Invalid attendance status. Use 'Present' or 'Absent'.")
        return

    cursor = connection.cursor()
    query = "INSERT INTO attendance (student_name, date, status) VALUES (%s, %s, %s)"
    values = (student_name, date, status)
    cursor.execute(query, values)
    connection.commit()
    print("Attendance marked successfully.")

def search_attendance(connection, student_name):
    if not validate_student_name(student_name):
        print("Invalid student name. Only alphabetic characters and spaces are allowed.")
        return

    cursor = connection.cursor()
    query = "SELECT * FROM attendance WHERE student_name = %s"
    cursor.execute(query, (student_name,))
    records = cursor.fetchall()
    for record in records:
        print(record)

def update_attendance(connection, student_name, date, status):
    if not validate_student_name(student_name):
        print("Invalid student name. Only alphabetic characters and spaces are allowed.")
        return
    if not validate_date(date):
        print("Invalid date format. Use YYYY-MM-DD.")
        return
    if status not in ["Present", "Absent"]:
        print("Invalid attendance status. Use 'Present' or 'Absent'.")
        return

    cursor = connection.cursor()
    query = "UPDATE attendance SET status = %s WHERE student_name = %s AND date = %s"
    values = (status, student_name, date)
    cursor.execute(query, values)
    connection.commit()
    print("Attendance updated successfully.")

def delete_attendance(connection, student_name, date):
    if not validate_student_name(student_name):
        print("Invalid student name. Only alphabetic characters and spaces are allowed.")
        return
    if not validate_date(date):
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    cursor = connection.cursor()
    query = "DELETE FROM attendance WHERE student_name = %s AND date = %s"
    cursor.execute(query, (student_name, date))
    connection.commit()
    print("Attendance record deleted successfully.")

def bulk_mark_attendance(connection, entries):
    for entry in entries:
        student_name, date, status = entry
        if not validate_student_name(student_name):
            print(f"Invalid student name: {student_name}. Only alphabetic characters and spaces are allowed.")
            continue
        if not validate_date(date):
            print(f"Invalid date format for {student_name}. Use YYYY-MM-DD.")
            continue
        if status not in ["Present", "Absent"]:
            print(f"Invalid attendance status for {student_name}. Use 'Present' or 'Absent'.")
            continue

        cursor = connection.cursor()
        query = "INSERT INTO attendance (student_name, date, status) VALUES (%s, %s, %s)"
        values = (student_name, date, status)
        cursor.execute(query, values)
        connection.commit()

    print("Bulk attendance marked successfully.")

def export_to_csv(connection, file_name):
    cursor = connection.cursor()
    query = "SELECT * FROM attendance"
    cursor.execute(query)
    records = cursor.fetchall()

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Student Name', 'Date', 'Status'])
        for record in records:
            writer.writerow(record)
    print(f"Data exported to {file_name} successfully.")

def show_menu():
    print("\nSmart Attendance System Menu")
    print("1. Create Table")
    print("2. Mark Attendance")
    print("3. Search Attendance")
    print("4. Update Attendance")
    print("5. Delete Attendance Record")
    print("6. Bulk Mark Attendance")
    print("7. Export to CSV")
    print("8. Exit")

def main():
    connection = create_connection()
    if connection is None:
        return

    while True:
        show_menu()
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            create_table(connection)
        elif choice == '2':
            student_name = input("Enter student name: ")
            date = input("Enter date (YYYY-MM-DD): ")
            status = input("Enter status (Present/Absent): ")
            mark_attendance(connection, student_name, date, status)
        elif choice == '3':
            student_name = input("Enter student name to search: ")
            search_attendance(connection, student_name)
        elif choice == '4':
            student_name = input("Enter student name: ")
            date = input("Enter date (YYYY-MM-DD): ")
            status = input("Enter new status (Present/Absent): ")
            update_attendance(connection, student_name, date, status)
        elif choice == '5':
            student_name = input("Enter student name: ")
            date = input("Enter date (YYYY-MM-DD): ")
            delete_attendance(connection, student_name, date)
        elif choice == '6':
            entries = []
            while True:
                student_name = input("Enter student name (or type 'done' to finish): ")
                if student_name.lower() == 'done':
                    break
                date = input("Enter date (YYYY-MM-DD): ")
                status = input("Enter status (Present/Absent): ")
                entries.append((student_name, date, status))
            bulk_mark_attendance(connection, entries)
        elif choice == '7':
            file_name = input("Enter CSV file name: ")
            export_to_csv(connection, file_name)
        elif choice == '8':
            print("Exiting...")
            connection.close()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

# Call the main function directly
main()
