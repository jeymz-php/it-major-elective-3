import random
from datetime import datetime
import hashlib
import getpass  # Add this import at the top

# Global variable to track current logged-in user
current_user = None

# Dream prompts for helping users recall dreams
DREAM_PROMPTS = [
    "Were there any people in your dream?",
    "What colors do you remember seeing?",
    "How did you feel when you woke up?",
    "Were you indoors or outdoors?",
    "Did you recognize the location?",
    "What sounds or music did you hear?",
    "Were there any animals present?",
    "What was the weather like?",
    "Did you feel any strong emotions?",
    "What time of day was it in the dream?"
]

# Common dream symbols and their meanings
DREAM_SYMBOLS = {
    "water": "Emotions, unconscious mind, purification",
    "flying": "Freedom, ambition, escape from limitations",
    "falling": "Loss of control, insecurity, fear",
    "snake": "Transformation, fear, hidden threats",
    "death": "Change, ending, new beginnings",
    "baby": "New beginnings, innocence, vulnerability",
    "house": "The self, different aspects of personality",
    "car": "Direction in life, control, progress",
    "teeth": "Anxiety, loss, appearance concerns",
    "chase": "Avoidance, running from problems",
    "money": "Self-worth, power, opportunities",
    "fire": "Passion, destruction, transformation",
    "animal": "Instincts, natural desires, untamed aspects",
    "family": "Relationships, support, roots"
}


def clear_screen():
    """Simulates clearing screen with newlines"""
    print("\n" * 2)


def display_header():
    """Display the system header"""
    print("=" * 60)
    print("       DREAM JOURNAL & ANALYSIS SYSTEM")
    print("=" * 60)
    print()


def main_menu():
    """Display main menu and return user choice"""
    display_header()
    if current_user:
        print(f"Logged in as: {current_user['full_name']} (@{current_user['username']})")
        print("-" * 60)
    print("1. Add New Dream Entry")
    print("2. View My Dreams")
    print("3. Search My Dreams")
    print("4. Analyze My Dream Patterns")
    print("5. Get Dream Prompts")
    print("6. View Symbol Dictionary")
    print("7. Add Custom Symbol")
    print("8. Delete Dream Entry")
    print("9. Logout")
    print("-" * 60)

    while True:
        try:
            choice = input("Enter your choice (1-9): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return choice
            else:
                print("Invalid choice! Please enter a number between 1-9.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")


def validate_username(username):
    """Validate username format"""
    if not username or not username.strip():
        raise ValueError("Username cannot be empty!")

    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters long!")

    if len(username) > 20:
        raise ValueError("Username must be at most 20 characters long!")

    # Allow only letters, numbers, and underscore
    for char in username:
        if not (char.isalnum() or char == '_'):
            raise ValueError(f"Username can only contain letters, numbers, and underscore! Found: '{char}'")

    return True


def validate_password(password):
    """Validate password strength"""
    if not password or not password.strip():
        raise ValueError("Password cannot be empty!")

    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters long!")

    if len(password) > 30:
        raise ValueError("Password must be at most 30 characters long!")

    return True


def hash_password(password):
    """Hash password for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():
    """Register a new user"""
    clear_screen()
    print("=" * 60)
    print("                    REGISTER NEW ACCOUNT")
    print("=" * 60)
    print()

    try:
        # Get and validate username
        while True:
            try:
                username = input("Enter username (3-20 characters, letters/numbers/_): ").strip()
                validate_username(username)

                # Check if username already exists
                try:
                    with open("users.txt", "r") as file:
                        users = file.readlines()
                        for user in users:
                            stored_username = user.strip().split("|")[0]
                            if stored_username.lower() == username.lower():
                                print("Username already exists! Please choose another.")
                                continue
                except FileNotFoundError:
                    pass  # File doesn't exist yet, which is fine

                break
            except ValueError as e:
                print(f"Error: {e}")

        # Get and validate password (using getpass to hide input)
        while True:
            try:
                password = getpass.getpass("Enter password (minimum 6 characters): ").strip()
                validate_password(password)
                break
            except ValueError as e:
                print(f"Error: {e}")

        # Confirm password (using getpass to hide input)
        while True:
            confirm_password = getpass.getpass("Confirm password: ").strip()
            if confirm_password == password:
                break
            else:
                print("Passwords do not match! Please try again.")

        # Get full name
        while True:
            try:
                full_name = input("Enter your full name: ").strip()
                validate_letters_only(full_name, "Full name")
                break
            except ValueError as e:
                print(f"Error: {e}")

        # Hash password and save user
        hashed_password = hash_password(password)
        user_entry = f"{username}|{hashed_password}|{full_name}\n"

        try:
            with open("users.txt", "a") as file:
                file.write(user_entry)
            print("\n✓ Registration successful! You can now login.")
            input("\nPress Enter to continue...")
            return True
        except IOError:
            print("\n✗ Error: Could not save user data.")
            input("\nPress Enter to continue...")
            return False

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        input("\nPress Enter to continue...")
        return False


def login_user():
    """Login existing user"""
    global current_user
    clear_screen()
    print("=" * 60)
    print("                        LOGIN")
    print("=" * 60)
    print()

    try:
        # Check if users file exists
        try:
            with open("users.txt", "r") as file:
                users = file.readlines()
        except FileNotFoundError:
            print("No users registered yet. Please register first.")
            input("\nPress Enter to continue...")
            return False

        if not users:
            print("No users registered yet. Please register first.")
            input("\nPress Enter to continue...")
            return False

        # Get username
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty!")
            input("\nPress Enter to continue...")
            return False

        # Get password (using getpass to hide input)
        password = getpass.getpass("Enter password: ").strip()
        if not password:
            print("Password cannot be empty!")
            input("\nPress Enter to continue...")
            return False

        # Hash entered password
        hashed_password = hash_password(password)

        # Check credentials
        for user in users:
            try:
                parts = user.strip().split("|")
                if len(parts) >= 3:
                    stored_username, stored_password, full_name = parts

                    if stored_username.lower() == username.lower():
                        if stored_password == hashed_password:
                            current_user = {
                                'username': stored_username,
                                'full_name': full_name
                            }
                            print(f"\n✓ Login successful! Welcome back, {full_name}!")
                            input("\nPress Enter to continue...")
                            return True
                        else:
                            print("\n✗ Incorrect password!")
                            input("\nPress Enter to continue...")
                            return False
            except Exception:
                continue

        print("\n✗ Username not found!")
        input("\nPress Enter to continue...")
        return False

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        input("\nPress Enter to continue...")
        return False


def auth_menu():
    """Display authentication menu"""
    while True:
        clear_screen()
        print("=" * 60)
        print("       DREAM JOURNAL & ANALYSIS SYSTEM")
        print("=" * 60)
        print()
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        print("-" * 60)

        try:
            choice = input("Enter your choice (1-3): ").strip()

            if choice == '1':
                if login_user():
                    return True  # Successful login
            elif choice == '2':
                register_user()
            elif choice == '3':
                print("\nGoodbye!")
                return False  # Exit program
            else:
                print("Invalid choice! Please enter 1, 2, or 3.")
                input("\nPress Enter to continue...")
        except Exception as e:
            print(f"Error: {e}")
            input("\nPress Enter to continue...")


def validate_date(date_str):
    """Validate date format YYYY-MM-DD"""
    if not date_str:
        return True  # Empty is okay, will use today's date

    # Check format with dashes
    if len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
        return False

    # Check if all parts are numbers
    parts = date_str.split('-')
    if len(parts) != 3:
        return False

    try:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])

        # Basic validation
        if year < 1900 or year > 2100:
            return False
        if month < 1 or month > 12:
            return False
        if day < 1 or day > 31:
            return False

        return True
    except ValueError:
        return False


def validate_text(text, field_name):
    """Validate text fields (letters, numbers, and basic special characters)"""
    if not text or not text.strip():
        raise ValueError(f"{field_name} cannot be empty!")

    # Allow letters, numbers, spaces, and basic punctuation
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?'-:;()&")

    for char in text:
        if char not in allowed_chars:
            raise ValueError(
                f"{field_name} contains invalid character: '{char}'. Only letters, numbers, and basic punctuation allowed.")

    return True


def validate_letters_only(text, field_name):
    """Validate that input contains only letters and spaces"""
    if not text or not text.strip():
        raise ValueError(f"{field_name} cannot be empty!")

    # Allow only letters and spaces
    for char in text:
        if not (char.isalpha() or char.isspace()):
            raise ValueError(f"{field_name} can only contain letters! Found invalid character: '{char}'")

    return True


def validate_number(text, min_val, max_val, field_name):
    """Validate that input is a number within range"""
    try:
        num = int(text)
        if num < min_val or num > max_val:
            raise ValueError(f"{field_name} must be between {min_val} and {max_val}!")
        return num
    except ValueError:
        raise ValueError(f"{field_name} must be a valid number!")


def add_dream_entry():
    """Add a new dream entry to the file"""
    clear_screen()
    print("=== ADD NEW DREAM ENTRY ===\n")

    try:
        # Get and validate date
        while True:
            date = input("Enter date (YYYY-MM-DD or press Enter for today): ").strip()
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
                break
            elif validate_date(date):
                break
            else:
                print("Invalid date format! Please use YYYY-MM-DD (e.g., 2025-11-01)")

        # Get and validate title
        while True:
            try:
                title = input("Dream title: ").strip()
                validate_text(title, "Title")
                break
            except ValueError as e:
                print(f"Error: {e}")

        # Get and validate description
        while True:
            try:
                description = input("Dream description: ").strip()
                validate_text(description, "Description")
                break
            except ValueError as e:
                print(f"Error: {e}")

        # Get and validate mood
        print("\nMood options: Happy, Sad, Scared, Confused, Excited, Calm, Anxious")
        while True:
            try:
                mood = input("Your mood upon waking (letters only): ").strip()
                validate_letters_only(mood, "Mood")
                break
            except ValueError as e:
                print(f"Error: {e}")

        # Get and validate dream type
        print("\nDream types: Normal, Nightmare, Lucid, Recurring")
        while True:
            try:
                dream_type = input("Dream type (letters only): ").strip()
                validate_letters_only(dream_type, "Dream type")
                break
            except ValueError as e:
                print(f"Error: {e}")

        # Get and validate intensity rating
        while True:
            try:
                intensity_input = input("Emotional intensity (1-10, numbers only): ").strip()
                intensity_num = validate_number(intensity_input, 1, 10, "Intensity")
                intensity = str(intensity_num)
                break
            except ValueError as e:
                print(f"Error: {e}")

        # Get symbols/tags
        symbols = input("Symbols or tags (comma-separated): ").strip()

        # Create dream entry with username
        dream_entry = f"{current_user['username']}|{date}|{title}|{description}|{mood}|{dream_type}|{intensity}|{symbols}\n"

        # Save to file
        try:
            with open("dreams.txt", "a") as file:
                file.write(dream_entry)
            print("\n✓ Dream entry saved successfully!")
        except IOError:
            print("\n✗ Error: Could not save dream entry to file.")

    except ValueError as ve:
        print(f"\n✗ Error: {ve}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
    finally:
        input("\nPress Enter to continue...")


def get_user_dreams():
    """Get all dreams for the current user"""
    try:
        with open("dreams.txt", "r") as file:
            dreams = file.readlines()

        user_dreams = []
        for dream in dreams:
            try:
                parts = dream.strip().split("|")
                if len(parts) >= 8:  # Now we have 8 fields including username
                    username, date, title, description, mood, dream_type, intensity, symbols = parts
                    if username == current_user['username']:
                        user_dreams.append({
                            'username': username,
                            'date': date,
                            'title': title,
                            'description': description,
                            'mood': mood,
                            'dream_type': dream_type,
                            'intensity': intensity,
                            'symbols': symbols
                        })
            except Exception:
                continue

        return user_dreams
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error reading dreams: {e}")
        return []


def view_all_dreams():
    """View all dream entries for the current user"""
    clear_screen()
    print("=== MY DREAM ENTRIES ===\n")

    user_dreams = get_user_dreams()

    if not user_dreams:
        print("No dreams found. Start by adding your first dream!")
    else:
        print(f"Total dreams: {len(user_dreams)}\n")
        for i, dream in enumerate(user_dreams, 1):
            print(f"--- Dream #{i} ---")
            print(f"Date: {dream['date']}")
            print(f"Title: {dream['title']}")
            print(f"Description: {dream['description']}")
            print(f"Mood: {dream['mood']}")
            print(f"Type: {dream['dream_type']}")
            print(f"Intensity: {dream['intensity']}/10")
            print(f"Symbols: {dream['symbols']}")
            print("-" * 50)

    input("\nPress Enter to continue...")


def search_dreams():
    """Search dreams by keyword for current user"""
    clear_screen()
    print("=== SEARCH MY DREAMS ===\n")

    keyword = input("Enter keyword to search: ").strip().lower()

    if not keyword:
        print("Search keyword cannot be empty!")
        input("\nPress Enter to continue...")
        return

    user_dreams = get_user_dreams()
    found_count = 0

    for i, dream in enumerate(user_dreams, 1):
        # Search in title, description, mood, type, and symbols
        dream_text = f"{dream['title']} {dream['description']} {dream['mood']} {dream['dream_type']} {dream['symbols']}".lower()

        if keyword in dream_text:
            found_count += 1
            print(f"\n--- Match #{found_count} (Dream #{i}) ---")
            print(f"Date: {dream['date']}")
            print(f"Title: {dream['title']}")
            print(f"Description: {dream['description']}")
            print(f"Mood: {dream['mood']}")
            print(f"Type: {dream['dream_type']}")
            print(f"Intensity: {dream['intensity']}/10")
            print(f"Symbols: {dream['symbols']}")
            print("-" * 50)

    if found_count == 0:
        print(f"\nNo dreams found containing '{keyword}'")
    else:
        print(f"\n✓ Found {found_count} dream(s) matching '{keyword}'")

    input("\nPress Enter to continue...")


def analyze_patterns():
    """Analyze dream patterns and show statistics for current user"""
    clear_screen()
    print("=== MY DREAM PATTERN ANALYSIS ===\n")

    user_dreams = get_user_dreams()

    if not user_dreams:
        print("No dreams to analyze yet.")
        input("\nPress Enter to continue...")
        return

    # Initialize counters
    total_dreams = len(user_dreams)
    moods = {}
    types = {}
    symbols_count = {}
    intensities = []

    # Analyze each dream
    for dream in user_dreams:
        # Count moods
        mood = dream['mood'].strip()
        moods[mood] = moods.get(mood, 0) + 1

        # Count types
        dream_type = dream['dream_type'].strip()
        types[dream_type] = types.get(dream_type, 0) + 1

        # Count symbols
        symbol_list = [s.strip() for s in dream['symbols'].split(",") if s.strip()]
        for symbol in symbol_list:
            symbols_count[symbol] = symbols_count.get(symbol, 0) + 1

        # Collect intensities
        try:
            intensities.append(int(dream['intensity']))
        except ValueError:
            pass

    # Display analysis
    print(f"Total Dreams Recorded: {total_dreams}\n")

    print("--- MOOD DISTRIBUTION ---")
    for mood, count in sorted(moods.items(), key=lambda x: x[1], reverse=True):
        print(f"{mood}: {count} time(s)")

    print("\n--- DREAM TYPES ---")
    for dtype, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
        print(f"{dtype}: {count} time(s)")

    print("\n--- MOST COMMON SYMBOLS ---")
    sorted_symbols = sorted(symbols_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for symbol, count in sorted_symbols:
        print(f"{symbol}: {count} time(s)")

    if intensities:
        avg_intensity = sum(intensities) / len(intensities)
        print(f"\n--- EMOTIONAL INTENSITY ---")
        print(f"Average Intensity: {avg_intensity:.1f}/10")
        print(f"Highest Intensity: {max(intensities)}/10")
        print(f"Lowest Intensity: {min(intensities)}/10")

    input("\nPress Enter to continue...")


def get_dream_prompts():
    """Generate random dream prompts to help recall"""
    clear_screen()
    print("=== DREAM RECALL PROMPTS ===\n")
    print("Answer these questions to help remember your dream:\n")

    try:
        # Shuffle and select random prompts
        selected_prompts = random.sample(DREAM_PROMPTS, 5)

        for i, prompt in enumerate(selected_prompts, 1):
            print(f"{i}. {prompt}")

        print("\nUse these prompts to recall more details about your dream!")

    except Exception as e:
        print(f"Error generating prompts: {e}")
    finally:
        input("\nPress Enter to continue...")


def view_symbol_dictionary():
    """View dream symbol meanings"""
    clear_screen()
    print("=== DREAM SYMBOL DICTIONARY ===\n")

    try:
        # Display built-in symbols
        print("--- COMMON DREAM SYMBOLS ---\n")
        for symbol, meaning in sorted(DREAM_SYMBOLS.items()):
            print(f"{symbol.capitalize()}: {meaning}")

        # Try to load custom symbols
        try:
            with open("custom_symbols.txt", "r") as file:
                custom = file.readlines()
                if custom:
                    print("\n--- YOUR CUSTOM SYMBOLS ---\n")
                    for line in custom:
                        print(line.strip())
        except FileNotFoundError:
            pass

    except Exception as e:
        print(f"Error displaying symbols: {e}")
    finally:
        input("\nPress Enter to continue...")


def add_custom_symbol():
    """Add a custom dream symbol and meaning"""
    clear_screen()
    print("=== ADD CUSTOM SYMBOL ===\n")

    try:
        symbol = input("Enter symbol name: ").strip().lower()
        if not symbol:
            raise ValueError("Symbol name cannot be empty!")

        meaning = input("Enter your personal meaning: ").strip()
        if not meaning:
            raise ValueError("Meaning cannot be empty!")

        entry = f"{symbol.capitalize()}: {meaning}\n"

        try:
            with open("custom_symbols.txt", "a") as file:
                file.write(entry)
            print("\n✓ Custom symbol added successfully!")
        except IOError:
            print("\n✗ Error: Could not save custom symbol.")

    except ValueError as ve:
        print(f"\n✗ Error: {ve}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
    finally:
        input("\nPress Enter to continue...")


def delete_dream():
    """Delete a dream entry for current user"""
    clear_screen()
    print("=== DELETE DREAM ENTRY ===\n")

    try:
        user_dreams = get_user_dreams()

        if not user_dreams:
            print("No dreams to delete.")
            input("\nPress Enter to continue...")
            return

        # Display all user dreams with numbers
        print("Your dreams:\n")
        for i, dream in enumerate(user_dreams, 1):
            print(f"{i}. {dream['date']} - {dream['title']}")

        # Get dream number to delete
        while True:
            try:
                choice = input(f"\nEnter dream number to delete (1-{len(user_dreams)}) or 0 to cancel: ").strip()
                choice_num = int(choice)

                if choice_num == 0:
                    print("Deletion cancelled.")
                    break
                elif 1 <= choice_num <= len(user_dreams):
                    # Keep asking until valid confirmation
                    while True:
                        confirm = input(
                            f"Are you sure you want to delete dream #{choice_num}? (y/yes or n/no): ").strip().lower()
                        if confirm in ["y", "yes"]:
                            # Read all dreams
                            with open("dreams.txt", "r") as file:
                                all_dreams = file.readlines()

                            # Find and remove the specific dream
                            dream_to_delete = user_dreams[choice_num - 1]
                            new_dreams = []

                            for dream_line in all_dreams:
                                try:
                                    parts = dream_line.strip().split("|")
                                    if len(parts) >= 8:
                                        username, date, title, description, mood, dream_type, intensity, symbols = parts
                                        # Only keep if it's not the dream we want to delete
                                        if not (username == dream_to_delete['username'] and
                                                date == dream_to_delete['date'] and
                                                title == dream_to_delete['title']):
                                            new_dreams.append(dream_line)
                                except Exception:
                                    new_dreams.append(dream_line)  # Keep corrupted entries

                            # Write back all dreams except the deleted one
                            with open("dreams.txt", "w") as file:
                                file.writelines(new_dreams)

                            print("\n✓ Dream deleted successfully!")
                            break
                        elif confirm in ["n", "no"]:
                            print("Deletion cancelled.")
                            break
                        else:
                            print("Invalid input! Please type 'y'/'yes' to confirm or 'n'/'no' to cancel.")
                    break
                else:
                    print(f"Please enter a number between 1 and {len(user_dreams)}.")
            except ValueError:
                print("Invalid input! Please enter a number.")
            except Exception as e:
                print(f"Error: {e}")
                break

    except FileNotFoundError:
        print("No dream entries found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        input("\nPress Enter to continue...")


def main():
    """Main program loop"""
    global current_user

    print("\nWelcome to Dream Journal & Analysis System!")
    input("Press Enter to start...")

    # Authentication loop
    while True:
        if not current_user:
            # Show login/register menu
            if not auth_menu():
                return  # User chose to exit
        else:
            # User is logged in, show main menu
            try:
                choice = main_menu()

                if choice == '1':
                    add_dream_entry()
                elif choice == '2':
                    view_all_dreams()
                elif choice == '3':
                    search_dreams()
                elif choice == '4':
                    analyze_patterns()
                elif choice == '5':
                    get_dream_prompts()
                elif choice == '6':
                    view_symbol_dictionary()
                elif choice == '7':
                    add_custom_symbol()
                elif choice == '8':
                    delete_dream()
                elif choice == '9':
                    print("\nThank you for using Dream Journal & Analysis System!")
                    print("Sweet dreams! 🌙")
                    current_user = None  # Logout
                    # Don't break here, go back to auth menu

            except KeyboardInterrupt:
                print("\n\nProgram interrupted. Exiting...")
                break
            except Exception as e:
                print(f"\nUnexpected error: {e}")
                input("Press Enter to continue...")


if __name__ == "__main__":
    main()
