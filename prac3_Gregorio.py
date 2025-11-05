"""
Text File Reader and Word Counter
Reads sentences from a text file, displays in uppercase, and counts words
File: prac3.py
"""


def count_words(sentence):
    """
    Count the number of words in a sentence

    Parameters:
    - sentence: A string containing the sentence

    Returns:
    - Integer count of words
    """
    # Split the sentence into words and count them
    words = sentence.strip().split()
    return len(words)


def process_file(filename):
    """
    Read a text file and process each line

    Parameters:
    - filename: Name of the text file to read
    """
    try:
        # Open and read the file
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Check if file is empty
        if not lines:
            print(f"The file '{filename}' is empty.")
            return

        # Process each line
        print("=" * 50)
        print("File Content Analysis")
        print("=" * 50)
        print()

        for line in lines:
            # Remove leading/trailing whitespace
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Convert to uppercase
            uppercase_line = line.upper()

            # Count words
            word_count = count_words(line)

            # Display results
            print(uppercase_line)
            print(f"Total number of words: {word_count}")
            print()

        print("=" * 50)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        print("Please make sure 'data.txt' exists in the same directory.")
    except PermissionError:
        print(f"Error: Permission denied to read '{filename}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_sample_file():
    """
    Create a sample data.txt file with the required content
    (This is a helper function to set up the file)
    """
    content = """Python Programming Essential Course
the quick brown fox jumps over a lazy dog"""

    try:
        with open('data.txt', 'w') as file:
            file.write(content)
        print("Sample 'data.txt' file created successfully!")
        print()
    except Exception as e:
        print(f"Error creating file: {e}")


def main():
    """Main function to run the program"""
    filename = "data.txt"

    print("\n" + "=" * 50)
    print("   Text File Reader and Word Counter")
    print("=" * 50)
    print()

    # Check if file exists, if not offer to create it
    import os
    if not os.path.exists(filename):
        print(f"'{filename}' not found.")
        create_choice = input("Do you want to create a sample data.txt? [y/n]: ").strip().lower()
        if create_choice == 'y' or create_choice == 'yes':
            create_sample_file()
        else:
            print("Program will exit. Please create 'data.txt' manually.")
            return

    # Process the file
    process_file(filename)


# Run the program
if __name__ == "__main__":
    main()