"""
Simple App Calculator
Performs basic arithmetic operations with error handling
File: prac2.py
"""


def display_menu():
    """Display the calculator menu with available operations"""
    print("\n" + "=" * 40)
    print("       SIMPLE CALCULATOR")
    print("=" * 40)
    print("Choose a math operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("=" * 40)


def get_numbers():
    """
    Get two numbers from the user with error handling

    Returns:
    - A tuple containing two float numbers (num1, num2)
    """
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            return num1, num2
        except ValueError:
            print("Error: Please enter valid numbers!")
            print()


def addition(a, b):
    """Perform addition operation"""
    return a + b


def subtraction(a, b):
    """Perform subtraction operation"""
    return a - b


def multiplication(a, b):
    """Perform multiplication operation"""
    return a * b


def division(a, b):
    """
    Perform division operation with zero division error handling

    Returns:
    - The result of division or None if division by zero
    """
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
        return None


def calculate(operation, num1, num2):
    """
    Perform the calculation based on the selected operation

    Parameters:
    - operation: The operation choice (1-4)
    - num1: First number
    - num2: Second number

    Returns:
    - The result of the calculation
    """
    if operation == '1':
        result = addition(num1, num2)
        print(f"\nResult: {num1} + {num2} = {result}")
        return result
    elif operation == '2':
        result = subtraction(num1, num2)
        print(f"\nResult: {num1} - {num2} = {result}")
        return result
    elif operation == '3':
        result = multiplication(num1, num2)
        print(f"\nResult: {num1} * {num2} = {result}")
        return result
    elif operation == '4':
        result = division(num1, num2)
        if result is not None:
            print(f"\nResult: {num1} / {num2} = {result}")
        return result
    else:
        print("Error: Invalid operation choice!")
        return None


def main():
    """Main function to run the Simple Calculator App"""
    print("\n" + "=" * 40)
    print("   Welcome to Simple Calculator App")
    print("=" * 40)

    while True:
        try:
            # Step 1: Display menu and get operation choice
            display_menu()
            operation = input("\nEnter your choice (1-4): ").strip()

            # Validate operation choice
            if operation not in ['1', '2', '3', '4']:
                print("Error: Please choose a valid operation (1-4)!")
                continue

            # Step 2: Get two numbers from user
            print()
            num1, num2 = get_numbers()

            # Step 3: Perform calculation and display result
            calculate(operation, num1, num2)

            # Step 4: Ask if user wants to try again
            print()
            try_again = input("Do you want to try again? [y/n]: ").strip().lower()

            # Step 5 & 6: Check user response
            if try_again == 'n' or try_again == 'no':
                print("\n" + "=" * 40)
                print("Thank you for using the calculator!")
                print("=" * 40)
                break
            elif try_again != 'y' and try_again != 'yes':
                print("Invalid input! Returning to menu...")

        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            print("\n" + "=" * 40)
            print("Thank you!")
            print("=" * 40)
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("Returning to menu...")


# Run the program
if __name__ == "__main__":
    main()