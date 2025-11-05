"""
Course Enrollment & Grade Analyzer
Uses lists, tuples, sets, and dictionaries to manage student records
"""

def display_menu():
    """Display the main menu options"""
    print("\n" + "="*50)
    print("COURSE ENROLLMENT & GRADE ANALYZER")
    print("="*50)
    print("A - Add record")
    print("R - Remove record")
    print("L - List all records")
    print("S - Show statistics")
    print("Q - Query by student or course")
    print("E - Exit")
    print("="*50)

def add_record(records):
    """Add a new student-course-grade record"""
    print("\n--- ADD RECORD ---")
    student_name = input("Enter student name: ").strip()
    course_name = input("Enter course name: ").strip()

    # Validate grade input
    while True:
        try:
            grade = float(input("Enter grade (0-100): "))
            if 0 <= grade <= 100:
                break
            else:
                print("Error: Grade must be between 0 and 100.")
        except ValueError:
            print("Error: Please enter a valid number.")

    # Create tuple and add to list
    new_record = (student_name, course_name, grade)
    records.append(new_record)
    print(f"✓ Record added: {student_name} — {course_name} — {grade}")

def remove_record(records):
    """Remove record(s) matching student and course name"""
    print("\n--- REMOVE RECORD ---")
    student_name = input("Enter student name: ").strip()
    course_name = input("Enter course name: ").strip()

    # Find and remove matching records
    initial_count = len(records)
    records[:] = [r for r in records if not (r[0].lower() == student_name.lower()
                                             and r[1].lower() == course_name.lower())]
    removed_count = initial_count - len(records)

    if removed_count > 0:
        print(f"✓ Removed {removed_count} record(s).")
    else:
        print("✗ No matching record found.")

def list_records(records):
    """Display all records in numbered format"""
    print("\n--- ALL RECORDS ---")
    if not records:
        print("No records available.")
        return

    for i, (student, course, grade) in enumerate(records, 1):
        print(f"{i}. {student} — {course} — {grade}")

def get_student_stats(records):
    """Calculate statistics per student using dictionaries"""
    student_grades = {}

    for student, course, grade in records:
        if student not in student_grades:
            student_grades[student] = []
        student_grades[student].append(grade)

    student_stats = {}
    for student, grades in student_grades.items():
        student_stats[student] = {
            'average': sum(grades) / len(grades),
            'highest': max(grades),
            'lowest': min(grades),
            'count': len(grades)
        }

    return student_stats

def get_course_stats(records):
    """Calculate statistics per course using dictionaries"""
    course_grades = {}

    for student, course, grade in records:
        if course not in course_grades:
            course_grades[course] = []
        course_grades[course].append(grade)

    course_stats = {}
    for course, grades in course_grades.items():
        course_stats[course] = {
            'average': sum(grades) / len(grades),
            'highest': max(grades),
            'lowest': min(grades),
            'count': len(grades)
        }

    return course_stats

def show_statistics(records):
    """Display comprehensive statistics"""
    print("\n--- STATISTICS ---")

    if not records:
        print("No records available.")
        return

    # Total records
    print(f"\nTotal records: {len(records)}")

    # Unique students (using set)
    unique_students = set(student for student, _, _ in records)
    print(f"\nUnique students ({len(unique_students)}): {', '.join(sorted(unique_students))}")

    # Unique courses (using set)
    unique_courses = set(course for _, course, _ in records)
    print(f"\nUnique courses ({len(unique_courses)}): {', '.join(sorted(unique_courses))}")

    # Student statistics
    print("\n--- STUDENT STATISTICS ---")
    student_stats = get_student_stats(records)
    for student in sorted(student_stats.keys()):
        stats = student_stats[student]
        print(f"{student} — Avg: {stats['average']:.2f}, High: {stats['highest']:.1f}, Low: {stats['lowest']:.1f}")

    # Course statistics
    print("\n--- COURSE STATISTICS ---")
    course_stats = get_course_stats(records)
    for course in sorted(course_stats.keys()):
        stats = course_stats[course]
        print(f"{course} — Avg: {stats['average']:.2f}, High: {stats['highest']:.1f}, Low: {stats['lowest']:.1f}")

    # Top 3 students by average grade
    print("\n--- TOP 3 STUDENTS ---")
    sorted_students = sorted(student_stats.items(), key=lambda x: x[1]['average'], reverse=True)
    for i, (student, stats) in enumerate(sorted_students[:3], 1):
        print(f"{i}. {student} — {stats['average']:.2f}")

    # Courses below 60 average (remediation needed)
    print("\n--- COURSES NEEDING REMEDIATION (Avg < 60) ---")
    remediation_courses = [(course, stats['average'])
                          for course, stats in course_stats.items()
                          if stats['average'] < 60]

    if remediation_courses:
        for course, avg in sorted(remediation_courses, key=lambda x: x[1]):
            print(f"{course} — Avg: {avg:.2f}")
    else:
        print("No courses need remediation.")

def query_records(records):
    """Query records by student or course name"""
    print("\n--- QUERY ---")
    print("1 - Search by student name")
    print("2 - Search by course name")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        search_term = input("Enter student name (partial match): ").strip().lower()
        matching_records = [r for r in records if search_term in r[0].lower()]

        if not matching_records:
            print("No matching students found.")
            return

        print(f"\n--- RECORDS FOR STUDENTS MATCHING '{search_term}' ---")
        for i, (student, course, grade) in enumerate(matching_records, 1):
            print(f"{i}. {student} — {course} — {grade}")

        # Calculate statistics for matching students
        student_stats = get_student_stats(matching_records)
        print("\n--- STATISTICS ---")
        for student, stats in sorted(student_stats.items()):
            print(f"{student} — Avg: {stats['average']:.2f}, High: {stats['highest']:.1f}, Low: {stats['lowest']:.1f}")

    elif choice == "2":
        search_term = input("Enter course name (partial match): ").strip().lower()
        matching_records = [r for r in records if search_term in r[1].lower()]

        if not matching_records:
            print("No matching courses found.")
            return

        print(f"\n--- RECORDS FOR COURSES MATCHING '{search_term}' ---")
        for i, (student, course, grade) in enumerate(matching_records, 1):
            print(f"{i}. {student} — {course} — {grade}")

        # Calculate statistics for matching courses
        course_stats = get_course_stats(matching_records)
        print("\n--- COURSE STATISTICS ---")
        for course, stats in sorted(course_stats.items()):
            print(f"{course} — Avg: {stats['average']:.2f}, High: {stats['highest']:.1f}, Low: {stats['lowest']:.1f}")
            print(f"  Students enrolled: {stats['count']}")

    else:
        print("Invalid choice.")

def main():
    """Main program loop"""
    # Initial data
    records = [
        ("Ana Cruz", "Programming 1", 87.5),
        ("Ben Santos", "Databases", 92.0),
        ("Carlo Reyes", "Programming 1", 76.0),
        ("Ana Cruz", "Databases", 91.0),
        ("Dana Lim", "Networking", 58.0),
        ("Eve Torres", "Programming 1", 88.0),
        ("Ben Santos", "Networking", 74.0),
    ]

    print("Welcome to the Course Enrollment & Grade Analyzer!")
    print(f"Loaded {len(records)} initial records.")

    while True:
        display_menu()
        choice = input("\nEnter your choice: ").strip().upper()

        if choice == "A":
            add_record(records)
        elif choice == "R":
            remove_record(records)
        elif choice == "L":
            list_records(records)
        elif choice == "S":
            show_statistics(records)
        elif choice == "Q":
            query_records(records)
        elif choice == "E":
            print("\nThank you for using the Grade Analyzer. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()