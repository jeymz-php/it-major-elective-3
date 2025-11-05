"""
Student Information Management System
A file-based system for managing student records with CRUD operations
File: student_management.py
"""

import os

# File name constant
FILENAME = "students.txt"


def display_menu():
    """Display the main menu options"""
    print("\n" + "=" * 40)
    print("=== Student Information System ===")
    print("=" * 40)
    print("a. Add Student Record")
    print("b. View All Records")
    print("c. Search Record")
    print("d. Update Record")
    print("e. Delete Record")
    print("f. End")
    print("=" * 40)


def add_student():
    """Add a new student record to the file"""
    print("\n--- Add Student Record ---")

    # Get student information from user
    student_id = input("Enter Student ID: ").strip()
    name = input("Enter Full Name: ").strip()
    course = input("Enter Course: ").strip()
    year = input("Enter Year Level: ").strip()

    # Validate inputs
    if not student_id or not name or not course or not year:
        print("Error: All fields are required!")
        return

    # Check if student ID already exists
    try:
        with open(FILENAME, 'r') as file:
            for line in file:
                if f"ID: {student_id}" in line:
                    print(f"Error: Student ID {student_id} already exists!")
                    return
    except FileNotFoundError:
        # File doesn't exist yet, which is fine for first record
        pass

    # Format the record
    record = f"ID: {student_id} | Name: {name} | Course: {course} | Year: {year}\n"

    # Append record to file
    try:
        with open(FILENAME, 'a') as file:
            file.write(record)
        print("\nRecord successfully added!")

        # Display current records
        print("\nCurrent Records:")
        view_all_records(show_header=False)
    except Exception as e:
        print(f"Error saving record: {e}")


def view_all_records(show_header=True):
    """Display all student records from the file"""
    if show_header:
        print("\n--- All Student Records ---")

    try:
        with open(FILENAME, 'r') as file:
            records = file.readlines()

            if not records:
                print("No records found.")
            else:
                for record in records:
                    print(record.strip())
                print(f"\nTotal Records: {len(records)}")
    except FileNotFoundError:
        print("No records found. The file does not exist yet.")
    except Exception as e:
        print(f"Error reading records: {e}")


def search_record():
    """Search for a student record by ID"""
    print("\n--- Search Record ---")
    search_id = input("Enter Student ID to search: ").strip()

    if not search_id:
        print("Error: Student ID cannot be empty!")
        return

    try:
        with open(FILENAME, 'r') as file:
            found = False
            for line in file:
                if f"ID: {search_id}" in line:
                    print("\nRecord Found:")
                    print(line.strip())
                    found = True
                    break

            if not found:
                print(f"No record found with ID: {search_id}")
    except FileNotFoundError:
        print("No records found. The file does not exist yet.")
    except Exception as e:
        print(f"Error searching record: {e}")


def update_record():
    """Update an existing student record by ID"""
    print("\n--- Update Record ---")
    update_id = input("Enter Student ID to update: ").strip()

    if not update_id:
        print("Error: Student ID cannot be empty!")
        return

    try:
        with open(FILENAME, 'r') as file:
            records = file.readlines()

        found = False
        updated_records = []

        for record in records:
            if f"ID: {update_id}" in record:
                found = True
                print("\nCurrent Record:")
                print(record.strip())

                # Get new information
                print("\nEnter new information (press Enter to keep current value):")
                new_name = input("Enter Full Name: ").strip()
                new_course = input("Enter Course: ").strip()
                new_year = input("Enter Year Level: ").strip()

                # Parse current record
                parts = record.split('|')
                current_name = parts[1].split(':')[1].strip() if len(parts) > 1 else ""
                current_course = parts[2].split(':')[1].strip() if len(parts) > 2 else ""
                current_year = parts[3].split(':')[1].strip() if len(parts) > 3 else ""

                # Use new values or keep current ones
                final_name = new_name if new_name else current_name
                final_course = new_course if new_course else current_course
                final_year = new_year if new_year else current_year

                # Create updated record
                updated_record = f"ID: {update_id} | Name: {final_name} | Course: {final_course} | Year: {final_year}\n"
                updated_records.append(updated_record)

                print("\nRecord updated successfully!")
                print("Updated Record:")
                print(updated_record.strip())
            else:
                updated_records.append(record)

        if not found:
            print(f"No record found with ID: {update_id}")
            return

        # Write updated records back to file
        with open(FILENAME, 'w') as file:
            file.writelines(updated_records)

    except FileNotFoundError:
        print("No records found. The file does not exist yet.")
    except Exception as e:
        print(f"Error updating record: {e}")


def delete_record():
    """Delete a student record by ID"""
    print("\n--- Delete Record ---")
    delete_id = input("Enter Student ID to delete: ").strip()

    if not delete_id:
        print("Error: Student ID cannot be empty!")
        return

    try:
        with open(FILENAME, 'r') as file:
            records = file.readlines()

        found = False
        remaining_records = []

        for record in records:
            if f"ID: {delete_id}" in record:
                found = True
                print("\nRecord to be deleted:")
                print(record.strip())

                # Confirm deletion
                confirm = input("\nAre you sure you want to delete this record? (yes/no): ").strip().lower()
                if confirm == 'yes' or confirm == 'y':
                    print("Record deleted successfully!")
                else:
                    print("Deletion cancelled.")
                    remaining_records.append(record)
            else:
                remaining_records.append(record)

        if not found:
            print(f"No record found with ID: {delete_id}")
            return

        # Write remaining records back to file
        with open(FILENAME, 'w') as file:
            file.writelines(remaining_records)

    except FileNotFoundError:
        print("No records found. The file does not exist yet.")
    except Exception as e:
        print(f"Error deleting record: {e}")


def main():
    """Main function to run the Student Information Management System"""
    print("\n" + "=" * 40)
    print("Welcome to Student Information System")
    print("=" * 40)

    while True:
        display_menu()
        choice = input("\nChoose an option: ").strip().lower()

        if choice == 'a':
            add_student()
        elif choice == 'b':
            view_all_records()
        elif choice == 'c':
            search_record()
        elif choice == 'd':
            update_record()
        elif choice == 'e':
            delete_record()
        elif choice == 'f':
            print("\n" + "=" * 40)
            print("Thank you for using the Student Information System!")
            print("Goodbye!")
            print("=" * 40)
            break
        else:
            print("\nInvalid option! Please choose a valid option (a-f).")


# Run the program
if __name__ == "__main__":
    main()