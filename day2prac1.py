name = input("Enter Name: ")
math = float(input("Enter Math: "))
science = float(input("Enter Science: "))
english = float(input("Enter English: "))

average = (math + science + english) / 3

print(f"Average Grade: {average:.2f}")

if average >= 75:
    print("Congratulations!")
    print("You passed the semester.")
else:
    print("You failed the semester.")