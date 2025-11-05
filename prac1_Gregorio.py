"""
Name Generator App
Generates random names using lists and random selection
File: prac1.py
"""

from random import randint


def generate_random_name(first_names, middle_names, last_names):
    """
    Generate a random name by selecting items from three lists

    Parameters:
    - first_names: list of first names
    - middle_names: list of middle names
    - last_names: list of last names

    Returns:
    - A string containing the full generated name
    """
    # Generate random indices (0-4)
    first_index = randint(0, 4)
    middle_index = randint(0, 4)
    last_index = randint(0, 4)

    # Select names using random indices
    first = first_names[first_index]
    middle = middle_names[middle_index]
    last = last_names[last_index]

    # Return the full name
    return f"{first} {middle} {last}"


def main():
    """Main function to run the Name Generator App"""

    # Step 1: Create 3 lists with 5 items each
    first_names = ["Juan", "John", "Maria", "Sarah", "Michael"]
    middle_names = ["Cruz", "Doe", "Anne", "Lee", "James"]
    last_names = ["Reyes", "Gates", "Smith", "Chen", "Johnson"]

    # List to store all generated names
    generated_names = []

    # Step 2: Ask user if they want to generate a new name
    while True:
        user_input = input("Do you want to generate a new name? [y/n]: ").strip().lower()

        # Step 3 & 4: If yes, generate and display name
        if user_input == 'y' or user_input == 'yes':
            new_name = generate_random_name(first_names, middle_names, last_names)
            print(f"Your new name is {new_name}")
            print()  # Blank line for better readability

            # Store the generated name
            generated_names.append(new_name)

        # Step 5: If no, display thank you message and all generated names
        elif user_input == 'n' or user_input == 'no':
            print("\nThank you!")

            # Display all generated names
            if generated_names:
                print("\nList of names generated:")
                for name in generated_names:
                    print(name)
            else:
                print("\nNo names were generated.")

            break  # Exit the loop

        else:
            print("Invalid input! Please enter 'y' for yes or 'n' for no.")
            print()


# Run the program
if __name__ == "__main__":
    main()