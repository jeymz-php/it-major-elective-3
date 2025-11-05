import random
from datetime import datetime

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
    print("1. Add New Dream Entry")
    print("2. View All Dreams")
    print("3. Search Dreams")
    print("4. Analyze Dream Patterns")
    print("5. Get Dream Prompts")
    print("6. View Symbol Dictionary")
    print("7. Add Custom Symbol")
    print("8. Delete Dream Entry")
    print("9. Exit")
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

        # Create dream entry
        dream_entry = f"{date}|{title}|{description}|{mood}|{dream_type}|{intensity}|{symbols}\n"

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


def view_all_dreams():
    """View all dream entries"""
    clear_screen()
    print("=== ALL DREAM ENTRIES ===\n")

    try:
        with open("dreams.txt", "r") as file:
            dreams = file.readlines()

        if not dreams:
            print("No dreams found. Start by adding your first dream!")
        else:
            for i, dream in enumerate(dreams, 1):
                try:
                    parts = dream.strip().split("|")
                    if len(parts) >= 7:
                        date, title, description, mood, dream_type, intensity, symbols = parts
                        print(f"\n--- Dream #{i} ---")
                        print(f"Date: {date}")
                        print(f"Title: {title}")
                        print(f"Description: {description}")
                        print(f"Mood: {mood}")
                        print(f"Type: {dream_type}")
                        print(f"Intensity: {intensity}/10")
                        print(f"Symbols: {symbols}")
                        print("-" * 50)
                except Exception:
                    print(f"Dream #{i}: [Corrupted entry]")
                    continue

    except FileNotFoundError:
        print("No dream entries found. The dreams file doesn't exist yet.")
    except Exception as e:
        print(f"Error reading dreams: {e}")
    finally:
        input("\nPress Enter to continue...")


def search_dreams():
    """Search dreams by keyword"""
    clear_screen()
    print("=== SEARCH DREAMS ===\n")

    keyword = input("Enter keyword to search: ").strip().lower()

    if not keyword:
        print("Search keyword cannot be empty!")
        input("\nPress Enter to continue...")
        return

    try:
        with open("dreams.txt", "r") as file:
            dreams = file.readlines()

        found_count = 0
        for i, dream in enumerate(dreams, 1):
            try:
                if keyword in dream.lower():
                    parts = dream.strip().split("|")
                    if len(parts) >= 7:
                        date, title, description, mood, dream_type, intensity, symbols = parts
                        found_count += 1
                        print(f"\n--- Match #{found_count} (Dream #{i}) ---")
                        print(f"Date: {date}")
                        print(f"Title: {title}")
                        print(f"Description: {description}")
                        print(f"Mood: {mood}")
                        print(f"Type: {dream_type}")
                        print(f"Intensity: {intensity}/10")
                        print(f"Symbols: {symbols}")
                        print("-" * 50)
            except Exception:
                continue

        if found_count == 0:
            print(f"\nNo dreams found containing '{keyword}'")
        else:
            print(f"\n✓ Found {found_count} dream(s) matching '{keyword}'")

    except FileNotFoundError:
        print("No dream entries found yet.")
    except Exception as e:
        print(f"Error searching dreams: {e}")
    finally:
        input("\nPress Enter to continue...")


def analyze_patterns():
    """Analyze dream patterns and show statistics"""
    clear_screen()
    print("=== DREAM PATTERN ANALYSIS ===\n")

    try:
        with open("dreams.txt", "r") as file:
            dreams = file.readlines()

        if not dreams:
            print("No dreams to analyze yet.")
            input("\nPress Enter to continue...")
            return

        # Initialize counters
        total_dreams = len(dreams)
        moods = {}
        types = {}
        symbols_count = {}
        intensities = []

        # Analyze each dream
        for dream in dreams:
            try:
                parts = dream.strip().split("|")
                if len(parts) >= 7:
                    date, title, description, mood, dream_type, intensity, symbols = parts

                    # Count moods
                    mood = mood.strip()
                    moods[mood] = moods.get(mood, 0) + 1

                    # Count types
                    dream_type = dream_type.strip()
                    types[dream_type] = types.get(dream_type, 0) + 1

                    # Count symbols
                    symbol_list = [s.strip() for s in symbols.split(",") if s.strip()]
                    for symbol in symbol_list:
                        symbols_count[symbol] = symbols_count.get(symbol, 0) + 1

                    # Collect intensities
                    try:
                        intensities.append(int(intensity))
                    except ValueError:
                        pass
            except Exception:
                continue

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

    except FileNotFoundError:
        print("No dream entries found yet.")
    except Exception as e:
        print(f"Error analyzing patterns: {e}")
    finally:
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
    """Delete a dream entry"""
    clear_screen()
    print("=== DELETE DREAM ENTRY ===\n")

    try:
        with open("dreams.txt", "r") as file:
            dreams = file.readlines()

        if not dreams:
            print("No dreams to delete.")
            input("\nPress Enter to continue...")
            return

        # Display all dreams with numbers
        print("Your dreams:\n")
        for i, dream in enumerate(dreams, 1):
            try:
                parts = dream.strip().split("|")
                if len(parts) >= 2:
                    print(f"{i}. {parts[0]} - {parts[1]}")
            except Exception:
                print(f"{i}. [Corrupted entry]")

        # Get dream number to delete
        while True:
            try:
                choice = input(f"\nEnter dream number to delete (1-{len(dreams)}) or 0 to cancel: ").strip()
                choice_num = int(choice)

                if choice_num == 0:
                    print("Deletion cancelled.")
                    break
                elif 1 <= choice_num <= len(dreams):
                    # Keep asking until valid confirmation
                    while True:
                        confirm = input(
                            f"Are you sure you want to delete dream #{choice_num}? (y/yes or n/no): ").strip().lower()
                        if confirm in ["y", "yes"]:
                            dreams.pop(choice_num - 1)
                            with open("dreams.txt", "w") as file:
                                file.writelines(dreams)
                            print("\n✓ Dream deleted successfully!")
                            break
                        elif confirm in ["n", "no"]:
                            print("Deletion cancelled.")
                            break
                        else:
                            print("Invalid input! Please type 'y'/'yes' to confirm or 'n'/'no' to cancel.")
                    break
                else:
                    print(f"Please enter a number between 1 and {len(dreams)}.")
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
    print("\nWelcome to Dream Journal & Analysis System!")
    input("Press Enter to start...")

    while True:
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
                break

        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()