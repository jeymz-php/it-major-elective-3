def main():
    # Dictionary to store records
    records = {}

    while True:
        print("\n--- Record Keeping App ---")
        print("a. Add Data")
        print("b. Delete Data")
        print("c. End")

        choice = input("Choose an option (a/b/c): ").strip().lower()

        if choice == 'a':
            # Add Data
            key = input("Enter Key: ").strip()
            value = input("Enter Value: ").strip()

            if key in records:
                print(f"Key '{key}' already exists with value '{records[key]}'")
                overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
                if overwrite != 'y':
                    print("Data not added.")
                    continue

            records[key] = value
            print("Data added successfully!")

        elif choice == 'b':
            # Delete Data
            if not records:
                print("No records to delete!")
                continue

            key = input("Enter Key: ").strip()

            if key in records:
                del records[key]
                print(f"Key '{key}' has been deleted.")
            else:
                print(f"Key '{key}' not found in records.")

        elif choice == 'c':
            # End program
            print("THANK YOU!")
            break

        else:
            print("Invalid option! Please choose a, b, or c.")
            continue

        # Display current records
        print("\nCurrent Records:")
        if records:
            print("Key: Value")
            for key, value in records.items():
                print(f"{key}: {value}")
        else:
            print("No records yet.")


if __name__ == "__main__":
    main()