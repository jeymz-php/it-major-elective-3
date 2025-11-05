name = str(input("Enter Employee Name: "))
hours = int(input("Enter number of hours rendered: "))
rate = int(input("Enter rate per hour: "))
gsis = int(input("GSIS Premium: "))
philhealth = int(input("PhilHealth: "))
loan = int(input("Housing Loan: "))
tax = int(input("Tax rate: "))

print(f"\nEnter Employee Name: {name}")
print(f"Enter number of hours rendered: {hours}")
print(f"Enter rate per hour: {rate}")
print(f"GSIS Premium: {gsis}")
print(f"PhilHealth: {philhealth}")
print(f"Housing loan: {loan}")
print(f"Tax rate: {tax}")

gross = hours * rate
tax = gross * (tax / 100)
total_deductions = gsis + philhealth + loan + tax
net = gross - total_deductions

print(f"\nGross Salary: {gross:.2f}")
print(f"Total deductions: {total_deductions:.2f}")
print(f"Net Salary: {net:.2f}")