# Nested if statement
print("A.")
age = 61
if age >= 1:
    if age >= 150:
        print("Age out of range")
    elif age >=60:
        print("Senior Citizen")
    else:
        print("Not a Senior Citizen")
else:
    print("Age out of range")

print("\nB.")
a = 3
b = 2
c = 4
if a > b:
    if a > c:
        print("a is the highest")
    else:
        print("c is the highest")
else:
    print("b is the highest")