name = input("Enter Name: ")
math = float(input("Enter Math Grade: "))
science = float(input("Enter Science Grade: "))
english = float(input("Enter English Grade: "))

average = (math + science + english) / 3

print(f"\n{name}'s Average Grade: {average:.2f}")

passed_subjects = []
failed_subjects = []

if math >= 75:
    passed_subjects.append("Math")
else:
    failed_subjects.append("Math")

if science >= 75:
    passed_subjects.append("Science")
else:
    failed_subjects.append("Science")

if english >= 75:
    passed_subjects.append("English")
else:
    failed_subjects.append("English")

if average >= 75:
    print("🎉 Congratulations! You passed the semester.")
    if passed_subjects:
        print("✅ Passed Subjects:")
        for subject in passed_subjects:
            print(f"- {subject}")
    if failed_subjects:
        print("⚠️ But you need to take these following subjects:")
        for subject in failed_subjects:
            print(f"- {subject}")
else:
    print("❌ You failed the semester.")
    if failed_subjects:
        print("❌ Failed Subjects:")
        for subject in failed_subjects:
            print(f"- {subject}")
    if passed_subjects:
        print("✅ Passed Subjects:")
        for subject in passed_subjects:
            print(f"- {subject}")