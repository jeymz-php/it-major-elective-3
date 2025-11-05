student_ids = set()
student_records = dict()


def add_student():
    student_id = input("Enter Student ID: ")
    if student_id in student_ids:
        print(f"Student ID {student_id} already exists!")
        return
    name = input("Enter Name: ")
    course = input("Enter Course: ")

    record = (student_id, name, course)

    student_ids.add(student_id)
    student_records[student_id] = record
    print(f"Student {name} added successfully!")


def display_students():
    if not student_records:
        print("No student records found.")
    else:
        print("--- Student Records ---")
        for sid, record in student_records.items():
            print(f"ID: {record[0]}, Name: {record[1]}, Course: {record[2]}")


def search_student():
    search_id = input("Enter Student ID to search: ")
    if search_id in student_records:
        record = student_records[search_id]
        print(f"Found: ID: {record[0]}, Name: {record[1]}, Course: {record[2]}")
    else:
        print("Student not found.")


def main():
    while True:
        print("\n--- Student Record App ---")
        print("1. Add Student")
        print("2. Display All Students")
        print("3. Search Student")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
