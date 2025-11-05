import random
from datetime import datetime
import hashlib
import os
import sys
import msvcrt  # For Windows

try:
    import termios  # For Unix/Linux/Mac
    import tty
except ImportError:
    pass

current_user = None
login_attempts = {}  # Track login attempts per username

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


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_color(text, color):
    """Print colored text"""
    print(f"{color}{text}{Colors.END}")


def get_password_with_asterisks(prompt):
    """Get password input with asterisks display"""
    print(f"{Colors.YELLOW}{prompt}{Colors.END}", end='', flush=True)
    password = ""

    if os.name == 'nt':  # Windows
        while True:
            char = msvcrt.getch()
            if char in [b'\r', b'\n']:  # Enter key
                print()
                break
            elif char == b'\x08':  # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)
            else:
                password += char.decode('utf-8')
                print('*', end='', flush=True)
    else:  # Unix/Linux/Mac
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char in ['\r', '\n']:  # Enter key
                    print()
                    break
                elif char == '\x7f':  # Backspace
                    if len(password) > 0:
                        password = password[:-1]
                        print('\b \b', end='', flush=True)
                else:
                    password += char
                    print('*', end='', flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return password


def display_header():
    """Display the system header with ASCII art"""
    clear_screen()
    print_color(r"""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀🌙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀✨⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀🍃⠀⠀🛌⠀⠀🍃⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀🌌⠀⠀⠀⠀⠀⠀⠀⠀🌌⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀🌟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀🌟⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀💤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀💤⠀⠀⠀⠀
    ⠀⠀⠀🦋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀🦋⠀⠀⠀
    ⠀⠀🌠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀🌠⠀⠀⠀
    """, Colors.PURPLE)

    print_color("=" * 60, Colors.CYAN)
    print_color("       DREAM JOURNAL & ANALYSIS SYSTEM", Colors.BOLD + Colors.PURPLE)
    print_color("=" * 60, Colors.CYAN)
    print()


def display_welcome():
    """Display welcome screen"""
    clear_screen()
    print_color(r"""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║    🌟 WELCOME TO DREAM JOURNAL & ANALYSIS SYSTEM 🌟      ║
    ║                                                          ║
    ║        "Unlock the secrets of your subconscious"         ║
    ║                                                          ║
    ║    ✨ Record your dreams ✨                              ║
    ║    🔍 Analyze patterns 🔍                                ║
    ║    📚 Discover meanings 📚                               ║
    ║    🌈 Understand yourself 🌈                             ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """, Colors.CYAN + Colors.BOLD)


def display_goodbye():
    """Display goodbye screen"""
    clear_screen()
    print_color(r"""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║                 🌙 Sweet Dreams! 🌙                      ║
    ║                                                          ║
    ║        Thank you for using Dream Journal System          ║
    ║                                                          ║
    ║          May your dreams be peaceful and                 ║
    ║           your subconscious guide you well               ║
    ║                                                          ║
    ║                 🛌 💫 🌠 🦋 🌈 ✨                       ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """, Colors.PURPLE + Colors.BOLD)


def display_success(message):
    """Display success message with design"""
    print_color(f"\n    ✅ {message}", Colors.GREEN + Colors.BOLD)


def display_error(message):
    """Display error message with design"""
    print_color(f"\n    ❌ {message}", Colors.RED + Colors.BOLD)


def display_warning(message):
    """Display warning message with design"""
    print_color(f"\n    ⚠️  {message}", Colors.YELLOW + Colors.BOLD)


def display_info(message):
    """Display info message with design"""
    print_color(f"\n    💡 {message}", Colors.CYAN + Colors.BOLD)


def main_menu():
    """Display main menu and return user choice"""
    display_header()
    if current_user:
        print_color(f"🔐 Logged in as: {current_user['full_name']} (@{current_user['username']})", Colors.GREEN)
        print_color("-" * 60, Colors.CYAN)

    print_color("1. 📝 Add New Dream Entry", Colors.WHITE)
    print_color("2. 📖 View My Dreams", Colors.WHITE)
    print_color("3. 🔍 Search My Dreams", Colors.WHITE)
    print_color("4. 📊 Analyze My Dream Patterns", Colors.WHITE)
    print_color("5. 💭 Get Dream Prompts", Colors.WHITE)
    print_color("6. 📚 View Symbol Dictionary", Colors.WHITE)
    print_color("7. 🎨 Add Custom Symbol", Colors.WHITE)
    print_color("8. 🗑️  Delete Dream Entry", Colors.WHITE)
    print_color("9. 🚪 Logout", Colors.WHITE)
    print_color("-" * 60, Colors.CYAN)

    while True:
        try:
            choice = input(f"{Colors.YELLOW}🎯 Enter your choice (1-9): {Colors.END}").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return choice
            else:
                display_error("Invalid choice! Please enter a number between 1-9.")
        except Exception as e:
            display_error(f"Error: {e}. Please try again.")


def validate_username(username):
    """Validate username format"""
    if not username or not username.strip():
        raise ValueError("Username cannot be empty!")

    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters long!")

    if len(username) > 20:
        raise ValueError("Username must be at most 20 characters long!")

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


def encrypt_data(data):
    """Simple encryption for demonstration"""
    key = "dream_journal_secret_key"
    encrypted = ""
    for i, char in enumerate(data):
        encrypted += chr(ord(char) ^ ord(key[i % len(key)]))
    return encrypted.encode().hex()


def decrypt_data(encrypted_hex):
    """Decrypt data"""
    try:
        encrypted_bytes = bytes.fromhex(encrypted_hex)
        key = "dream_journal_secret_key"
        decrypted = ""
        for i, char_code in enumerate(encrypted_bytes):
            decrypted += chr(char_code ^ ord(key[i % len(key)]))
        return decrypted
    except:
        return None


def reset_password(username):
    """Reset password for a user after failed attempts"""
    clear_screen()
    print_color("=" * 60, Colors.CYAN)
    print_color("                   🔄 PASSWORD RESET", Colors.BOLD + Colors.PURPLE)
    print_color("=" * 60, Colors.CYAN)
    print()

    display_warning(f"Password reset required for user: {username}")
    print_color("You've exceeded the maximum login attempts. Please reset your password.\n", Colors.YELLOW)

    # Read all users
    try:
        with open("users.txt", "r") as file:
            encrypted_users = file.readlines()
    except FileNotFoundError:
        display_error("User database not found!")
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        return False

    user_found = False
    new_users_data = []

    # Find the user and update their password
    for encrypted_user in encrypted_users:
        decrypted_data = decrypt_data(encrypted_user.strip())
        if decrypted_data:
            parts = decrypted_data.split("|")
            if len(parts) >= 3:
                stored_username, stored_password, full_name = parts
                if stored_username.lower() == username.lower():
                    user_found = True

                    # Get new password
                    while True:
                        try:
                            new_password = get_password_with_asterisks("🔒 Enter new password (minimum 6 characters): ")
                            validate_password(new_password)
                            break
                        except ValueError as e:
                            display_error(str(e))

                    # Confirm new password
                    while True:
                        confirm_password = get_password_with_asterisks("🔒 Confirm new password: ")
                        if confirm_password == new_password:
                            break
                        else:
                            display_error("Passwords do not match! Please try again.")
                            # If confirmation fails, go back to entering new password
                            continue

                    # Update the user data with new hashed password
                    new_hashed_password = hash_password(new_password)
                    user_data = f"{stored_username}|{new_hashed_password}|{full_name}"
                    encrypted_data = encrypt_data(user_data)
                    new_users_data.append(encrypted_data + "\n")

                    display_success("Password reset successfully! You can now login with your new password.")

                    # Reset login attempts for this user
                    if username.lower() in login_attempts:
                        del login_attempts[username.lower()]
                else:
                    new_users_data.append(encrypted_user)

    if user_found:
        # Write updated users back to file
        try:
            with open("users.txt", "w") as file:
                file.writelines(new_users_data)
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return True
        except IOError:
            display_error("Could not update user data.")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return False
    else:
        display_error("User not found in database!")
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        return False


def register_user():
    """Register a new user"""
    clear_screen()
    print_color("=" * 60, Colors.CYAN)
    print_color("                    📝 REGISTER NEW ACCOUNT", Colors.BOLD + Colors.PURPLE)
    print_color("=" * 60, Colors.CYAN)
    print()

    try:
        while True:
            try:
                username = input(
                    f"{Colors.YELLOW}👤 Enter username (3-20 characters, letters/numbers/_): {Colors.END}").strip()
                validate_username(username)

                try:
                    with open("users.txt", "r") as file:
                        users = file.readlines()
                        for user in users:
                            stored_data = user.strip()
                            decrypted_data = decrypt_data(stored_data)
                            if decrypted_data:
                                parts = decrypted_data.split("|")
                                if len(parts) >= 3:
                                    stored_username = parts[0]
                                    if stored_username.lower() == username.lower():
                                        display_warning("Username already exists! Please choose another.")
                                        continue
                except FileNotFoundError:
                    pass

                break
            except ValueError as e:
                display_error(str(e))

        # Password entry with confirmation loop
        while True:
            # Get password
            while True:
                try:
                    password = get_password_with_asterisks("🔒 Enter password (minimum 6 characters): ")
                    validate_password(password)
                    break
                except ValueError as e:
                    display_error(str(e))

            # Confirm password
            confirm_password = get_password_with_asterisks("🔒 Confirm password: ")

            if confirm_password == password:
                break
            else:
                display_error("Passwords do not match! Please start over.")
                # This will loop back to entering the password again

        while True:
            try:
                full_name = input(f"{Colors.YELLOW}📛 Enter your full name: {Colors.END}").strip()
                validate_letters_only(full_name, "Full name")
                break
            except ValueError as e:
                display_error(str(e))

        hashed_password = hash_password(password)
        user_data = f"{username}|{hashed_password}|{full_name}"
        encrypted_data = encrypt_data(user_data)

        try:
            with open("users.txt", "a") as file:
                file.write(encrypted_data + "\n")
            display_success("Registration successful! You can now login.")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return True
        except IOError:
            display_error("Could not save user data.")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return False

    except Exception as e:
        display_error(f"Unexpected error: {e}")
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        return False


def login_user():
    """Login existing user with attempt tracking"""
    global current_user, login_attempts

    clear_screen()
    print_color("=" * 60, Colors.CYAN)
    print_color("                        🔐 LOGIN", Colors.BOLD + Colors.PURPLE)
    print_color("=" * 60, Colors.CYAN)
    print()

    try:
        try:
            with open("users.txt", "r") as file:
                encrypted_users = file.readlines()
        except FileNotFoundError:
            display_warning("No users registered yet. Please register first.")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return False

        if not encrypted_users:
            display_warning("No users registered yet. Please register first.")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return False

        username = input(f"{Colors.YELLOW}👤 Enter username: {Colors.END}").strip()
        if not username:
            display_error("Username cannot be empty!")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return False

        # Initialize or get login attempts for this username
        username_lower = username.lower()
        if username_lower not in login_attempts:
            login_attempts[username_lower] = 0

        # Check if user has exceeded login attempts
        if login_attempts[username_lower] >= 5:
            display_warning(f"Too many failed login attempts for user: {username}")
            print_color("You need to reset your password to continue.\n", Colors.YELLOW)
            input(f"\n{Colors.CYAN}Press Enter to reset password...{Colors.END}")
            if reset_password(username):
                # After reset, allow login with new password
                login_attempts[username_lower] = 0
                display_info("Please login with your new password.")
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                return False
            else:
                return False

        password = get_password_with_asterisks("🔒 Enter password: ")
        if not password:
            display_error("Password cannot be empty!")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return False

        hashed_password = hash_password(password)
        user_found = False

        for encrypted_user in encrypted_users:
            try:
                decrypted_data = decrypt_data(encrypted_user.strip())
                if decrypted_data:
                    parts = decrypted_data.split("|")
                    if len(parts) >= 3:
                        stored_username, stored_password, full_name = parts

                        if stored_username.lower() == username_lower:
                            user_found = True
                            if stored_password == hashed_password:
                                current_user = {
                                    'username': stored_username,
                                    'full_name': full_name
                                }
                                # Reset login attempts on successful login
                                login_attempts[username_lower] = 0
                                display_success(f"Login successful! Welcome back, {full_name}! 🌟")
                                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
                                return True
                            else:
                                login_attempts[username_lower] += 1
                                attempts_left = 5 - login_attempts[username_lower]
                                display_error(f"Incorrect password! Attempts left: {attempts_left}")
                                if attempts_left > 0:
                                    input(f"\n{Colors.CYAN}Press Enter to try again...{Colors.END}")
                                    return login_user()  # Recursive call to try again
                                else:
                                    display_warning("Maximum login attempts reached!")
                                    input(f"\n{Colors.CYAN}Press Enter to reset password...{Colors.END}")
                                    if reset_password(username):
                                        login_attempts[username_lower] = 0
                                        return False
                                    else:
                                        return False
            except Exception:
                continue

        if not user_found:
            display_error("Username not found!")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return False

    except Exception as e:
        display_error(f"Unexpected error: {e}")
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        return False


def auth_menu():
    """Display authentication menu"""
    while True:
        clear_screen()
        display_header()
        print_color("1. 🔐 Login", Colors.WHITE)
        print_color("2. 📝 Register", Colors.WHITE)
        print_color("3. 🚪 Exit", Colors.WHITE)
        print_color("-" * 60, Colors.CYAN)

        try:
            choice = input(f"{Colors.YELLOW}🎯 Enter your choice (1-3): {Colors.END}").strip()

            if choice == '1':
                if login_user():
                    return True
            elif choice == '2':
                register_user()
            elif choice == '3':
                display_goodbye()
                return False
            else:
                display_error("Invalid choice! Please enter 1, 2, or 3.")
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        except Exception as e:
            display_error(str(e))
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")


def validate_date(date_str):
    """Validate date format YYYY-MM-DD"""
    if not date_str:
        return True

    if len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
        return False

    parts = date_str.split('-')
    if len(parts) != 3:
        return False

    try:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])

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
    print_color("╔══════════════════════════════════════════════════════════╗", Colors.CYAN)
    print_color("║                   📝 ADD NEW DREAM ENTRY                 ║", Colors.BOLD + Colors.PURPLE)
    print_color("╚══════════════════════════════════════════════════════════╝", Colors.CYAN)
    print()

    try:
        while True:
            date = input(f"{Colors.YELLOW}📅 Enter date (YYYY-MM-DD or press Enter for today): {Colors.END}").strip()
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
                display_info(f"Using today's date: {date}")
                break
            elif validate_date(date):
                break
            else:
                display_error("Invalid date format! Please use YYYY-MM-DD (e.g., 2025-11-01)")

        while True:
            try:
                title = input(f"{Colors.YELLOW}🏷️  Dream title: {Colors.END}").strip()
                validate_text(title, "Title")
                break
            except ValueError as e:
                display_error(str(e))

        while True:
            try:
                description = input(f"{Colors.YELLOW}📖 Dream description: {Colors.END}").strip()
                validate_text(description, "Description")
                break
            except ValueError as e:
                display_error(str(e))

        print_color("\n🎭 Mood options: Happy, Sad, Scared, Confused, Excited, Calm, Anxious", Colors.CYAN)
        while True:
            try:
                mood = input(f"{Colors.YELLOW}😊 Your mood upon waking (letters only): {Colors.END}").strip()
                validate_letters_only(mood, "Mood")
                break
            except ValueError as e:
                display_error(str(e))

        print_color("\n🔮 Dream types: Normal, Nightmare, Lucid, Recurring", Colors.CYAN)
        while True:
            try:
                dream_type = input(f"{Colors.YELLOW}🌙 Dream type (letters only): {Colors.END}").strip()
                validate_letters_only(dream_type, "Dream type")
                break
            except ValueError as e:
                display_error(str(e))

        while True:
            try:
                intensity_input = input(
                    f"{Colors.YELLOW}💥 Emotional intensity (1-10, numbers only): {Colors.END}").strip()
                intensity_num = validate_number(intensity_input, 1, 10, "Intensity")
                intensity = str(intensity_num)
                break
            except ValueError as e:
                display_error(str(e))

        symbols = input(f"{Colors.YELLOW}🔮 Symbols or tags (comma-separated): {Colors.END}").strip()

        dream_entry = f"{current_user['username']}|{date}|{title}|{description}|{mood}|{dream_type}|{intensity}|{symbols}\n"

        try:
            with open("dreams.txt", "a") as file:
                file.write(dream_entry)
            display_success("Dream entry saved successfully! 🌟")
        except IOError:
            display_error("Could not save dream entry to file.")

    except ValueError as ve:
        display_error(str(ve))
    except Exception as e:
        display_error(f"Unexpected error: {e}")
    finally:
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")


def get_user_dreams():
    """Get all dreams for the current user"""
    try:
        with open("dreams.txt", "r") as file:
            dreams = file.readlines()

        user_dreams = []
        for dream in dreams:
            try:
                parts = dream.strip().split("|")
                if len(parts) >= 8:
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
        display_error(f"Error reading dreams: {e}")
        return []


def view_all_dreams():
    """View all dream entries for the current user"""
    clear_screen()
    print_color("╔══════════════════════════════════════════════════════════╗", Colors.CYAN)
    print_color("║                     📖 MY DREAM ENTRIES                  ║", Colors.BOLD + Colors.PURPLE)
    print_color("╚══════════════════════════════════════════════════════════╝", Colors.CYAN)
    print()

    user_dreams = get_user_dreams()

    if not user_dreams:
        display_warning("No dreams found. Start by adding your first dream! 🌟")
    else:
        print_color(f"📊 Total dreams: {len(user_dreams)}\n", Colors.GREEN)
        for i, dream in enumerate(user_dreams, 1):
            print_color(f"┌{'─' * 58}┐", Colors.CYAN)
            print_color(f"│ 🦋 Dream #{i: <51} │", Colors.PURPLE)
            print_color(f"├{'─' * 58}┤", Colors.CYAN)
            print_color(f"│ 📅 Date: {dream['date']: <47} │", Colors.WHITE)
            print_color(f"│ 🏷️  Title: {dream['title']: <46} │", Colors.WHITE)
            print_color(f"│ 📖 Description: {dream['description'][:40]: <37} │", Colors.WHITE)
            print_color(f"│ 😊 Mood: {dream['mood']: <47} │", Colors.WHITE)
            print_color(f"│ 🌙 Type: {dream['dream_type']: <46} │", Colors.WHITE)
            print_color(f"│ 💥 Intensity: {dream['intensity']}/10{' ': <37} │", Colors.WHITE)
            print_color(f"│ 🔮 Symbols: {dream['symbols'][:40]: <38} │", Colors.WHITE)
            print_color(f"└{'─' * 58}┘", Colors.CYAN)
            print()

    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")


def search_dreams():
    """Search dreams by keyword for current user"""
    clear_screen()
    print_color("╔══════════════════════════════════════════════════════════╗", Colors.CYAN)
    print_color("║                     🔍 SEARCH MY DREAMS                  ║", Colors.BOLD + Colors.PURPLE)
    print_color("╚══════════════════════════════════════════════════════════╝", Colors.CYAN)
    print()

    keyword = input(f"{Colors.YELLOW}🔎 Enter keyword to search: {Colors.END}").strip().lower()

    if not keyword:
        display_error("Search keyword cannot be empty!")
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        return

    user_dreams = get_user_dreams()
    found_count = 0

    for i, dream in enumerate(user_dreams, 1):
        dream_text = f"{dream['title']} {dream['description']} {dream['mood']} {dream['dream_type']} {dream['symbols']}".lower()

        if keyword in dream_text:
            found_count += 1
            print_color(f"\n🎯 Match #{found_count} (Dream #{i})", Colors.GREEN)
            print_color(f"📅 Date: {dream['date']}", Colors.CYAN)
            print_color(f"🏷️  Title: {dream['title']}", Colors.CYAN)
            print_color(f"📖 Description: {dream['description']}", Colors.CYAN)
            print_color(f"😊 Mood: {dream['mood']}", Colors.CYAN)
            print_color(f"🌙 Type: {dream['dream_type']}", Colors.CYAN)
            print_color(f"💥 Intensity: {dream['intensity']}/10", Colors.CYAN)
            print_color(f"🔮 Symbols: {dream['symbols']}", Colors.CYAN)
            print_color("-" * 50, Colors.CYAN)

    if found_count == 0:
        display_warning(f"No dreams found containing '{keyword}'")
    else:
        display_success(f"Found {found_count} dream(s) matching '{keyword}'")

    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")


def analyze_patterns():
    """Analyze dream patterns and show statistics for current user"""
    clear_screen()
    print_color("╔══════════════════════════════════════════════════════════╗", Colors.CYAN)
    print_color("║                  📊 MY DREAM PATTERN ANALYSIS            ║", Colors.BOLD + Colors.PURPLE)
    print_color("╚══════════════════════════════════════════════════════════╝", Colors.CYAN)
    print()

    user_dreams = get_user_dreams()

    if not user_dreams:
        display_warning("No dreams to analyze yet.")
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
        return

    total_dreams = len(user_dreams)
    moods = {}
    types = {}
    symbols_count = {}
    intensities = []

    for dream in user_dreams:
        mood = dream['mood'].strip()
        moods[mood] = moods.get(mood, 0) + 1

        dream_type = dream['dream_type'].strip()
        types[dream_type] = types.get(dream_type, 0) + 1

        symbol_list = [s.strip() for s in dream['symbols'].split(",") if s.strip()]
        for symbol in symbol_list:
            symbols_count[symbol] = symbols_count.get(symbol, 0) + 1

        try:
            intensities.append(int(dream['intensity']))
        except ValueError:
            pass

    print_color(f"📈 Total Dreams Recorded: {total_dreams}\n", Colors.GREEN)

    print_color("🎭 MOOD DISTRIBUTION", Colors.PURPLE + Colors.BOLD)
    for mood, count in sorted(moods.items(), key=lambda x: x[1], reverse=True):
        print_color(f"   {mood}: {count} time(s)", Colors.WHITE)

    print_color("\n🔮 DREAM TYPES", Colors.PURPLE + Colors.BOLD)
    for dtype, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
        print_color(f"   {dtype}: {count} time(s)", Colors.WHITE)

    print_color("\n🌟 MOST COMMON SYMBOLS", Colors.PURPLE + Colors.BOLD)
    sorted_symbols = sorted(symbols_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for symbol, count in sorted_symbols:
        print_color(f"   {symbol}: {count} time(s)", Colors.WHITE)

    if intensities:
        avg_intensity = sum(intensities) / len(intensities)
        print_color(f"\n💥 EMOTIONAL INTENSITY", Colors.PURPLE + Colors.BOLD)
        print_color(f"   Average Intensity: {avg_intensity:.1f}/10", Colors.WHITE)
        print_color(f"   Highest Intensity: {max(intensities)}/10", Colors.WHITE)
        print_color(f"   Lowest Intensity: {min(intensities)}/10", Colors.WHITE)

    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")


def get_dream_prompts():
    """Generate random dream prompts to help recall"""
    clear_screen()
    print_color("╔══════════════════════════════════════════════════════════╗", Colors.CYAN)
    print_color("║                   💭 DREAM RECALL PROMPTS                ║", Colors.BOLD + Colors.PURPLE)
    print_color("╚══════════════════════════════════════════════════════════╝", Colors.CYAN)
    print()
    print_color("Answer these questions to help remember your dream:\n", Colors.CYAN)

    try:
        selected_prompts = random.sample(DREAM_PROMPTS, 5)

        for i, prompt in enumerate(selected_prompts, 1):
            print_color(f"{i}. {prompt}", Colors.WHITE)

        print_color("\n🌟 Use these prompts to recall more details about your dream!", Colors.GREEN)

    except Exception as e:
        display_error(f"Error generating prompts: {e}")
    finally:
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")


def view_symbol_dictionary():
    """View dream symbol meanings"""
    clear_screen()
    print_color("╔══════════════════════════════════════════════════════════╗", Colors.CYAN)
    print_color("║                  📚 DREAM SYMBOL DICTIONARY              ║", Colors.BOLD + Colors.PURPLE)
    print_color("╚══════════════════════════════════════════════════════════╝", Colors.CYAN)
    print()

    try:
        print_color("🌟 COMMON DREAM SYMBOLS\n", Colors.GREEN + Colors.BOLD)
        for symbol, meaning in sorted(DREAM_SYMBOLS.items()):
            print_color(f"🔮 {symbol.capitalize()}:", Colors.CYAN + Colors.BOLD)
            print_color(f"   {meaning}\n", Colors.WHITE)

        try:
            with open("custom_symbols.txt", "r") as file:
                custom = file.readlines()
                if custom:
                    print_color("🎨 YOUR CUSTOM SYMBOLS\n", Colors.GREEN + Colors.BOLD)
                    for line in custom:
                        print_color(f"   {line.strip()}", Colors.WHITE)
        except FileNotFoundError:
            pass

    except Exception as e:
        display_error(f"Error displaying symbols: {e}")
    finally:
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")


def add_custom_symbol():
    """Add a custom dream symbol and meaning"""
    clear_screen()
    print_color("╔══════════════════════════════════════════════════════════╗", Colors.CYAN)
    print_color("║                    🎨 ADD CUSTOM SYMBOL                  ║", Colors.BOLD + Colors.PURPLE)
    print_color("╚══════════════════════════════════════════════════════════╝", Colors.CYAN)
    print()

    try:
        symbol = input(f"{Colors.YELLOW}🔮 Enter symbol name: {Colors.END}").strip().lower()
        if not symbol:
            raise ValueError("Symbol name cannot be empty!")

        meaning = input(f"{Colors.YELLOW}💡 Enter your personal meaning: {Colors.END}").strip()
        if not meaning:
            raise ValueError("Meaning cannot be empty!")

        entry = f"{symbol.capitalize()}: {meaning}\n"

        try:
            with open("custom_symbols.txt", "a") as file:
                file.write(entry)
            display_success("Custom symbol added successfully! 🌟")
        except IOError:
            display_error("Could not save custom symbol.")

    except ValueError as ve:
        display_error(str(ve))
    except Exception as e:
        display_error(f"Unexpected error: {e}")
    finally:
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")


def delete_dream():
    """Delete a dream entry for current user"""
    clear_screen()
    print_color("╔══════════════════════════════════════════════════════════╗", Colors.CYAN)
    print_color("║                   🗑️  DELETE DREAM ENTRY                 ║", Colors.BOLD + Colors.PURPLE)
    print_color("╚══════════════════════════════════════════════════════════╝", Colors.CYAN)
    print()

    try:
        user_dreams = get_user_dreams()

        if not user_dreams:
            display_warning("No dreams to delete.")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return

        print_color("Your dreams:\n", Colors.CYAN)
        for i, dream in enumerate(user_dreams, 1):
            print_color(f"{i}. 📅 {dream['date']} - 🏷️  {dream['title']}", Colors.WHITE)

        while True:
            try:
                choice = input(
                    f"\n{Colors.YELLOW}🎯 Enter dream number to delete (1-{len(user_dreams)}) or 0 to cancel: {Colors.END}").strip()
                choice_num = int(choice)

                if choice_num == 0:
                    display_info("Deletion cancelled.")
                    break
                elif 1 <= choice_num <= len(user_dreams):
                    while True:
                        confirm = input(
                            f"{Colors.YELLOW}⚠️  Are you sure you want to delete dream #{choice_num}? (y/yes or n/no): {Colors.END}").strip().lower()
                        if confirm in ["y", "yes"]:
                            with open("dreams.txt", "r") as file:
                                all_dreams = file.readlines()

                            dream_to_delete = user_dreams[choice_num - 1]
                            new_dreams = []

                            for dream_line in all_dreams:
                                try:
                                    parts = dream_line.strip().split("|")
                                    if len(parts) >= 8:
                                        username, date, title, description, mood, dream_type, intensity, symbols = parts
                                        if not (username == dream_to_delete['username'] and
                                                date == dream_to_delete['date'] and
                                                title == dream_to_delete['title']):
                                            new_dreams.append(dream_line)
                                except Exception:
                                    new_dreams.append(dream_line)

                            with open("dreams.txt", "w") as file:
                                file.writelines(new_dreams)

                            display_success("Dream deleted successfully!")
                            break
                        elif confirm in ["n", "no"]:
                            display_info("Deletion cancelled.")
                            break
                        else:
                            display_error("Invalid input! Please type 'y'/'yes' to confirm or 'n'/'no' to cancel.")
                    break
                else:
                    display_error(f"Please enter a number between 1 and {len(user_dreams)}.")
            except ValueError:
                display_error("Invalid input! Please enter a number.")
            except Exception as e:
                display_error(f"Error: {e}")
                break

    except FileNotFoundError:
        display_warning("No dream entries found.")
    except Exception as e:
        display_error(f"Error: {e}")
    finally:
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")


def main():
    """Main program loop"""
    global current_user

    display_welcome()
    input(f"\n{Colors.CYAN}Press Enter to start your dream journey...{Colors.END}")

    while True:
        if not current_user:
            if not auth_menu():
                display_goodbye()
                return
        else:
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
                    display_success("Thank you for using Dream Journal & Analysis System!")
                    print_color("Sweet dreams! 🌙", Colors.PURPLE + Colors.BOLD)
                    current_user = None

            except KeyboardInterrupt:
                display_goodbye()
                break
            except Exception as e:
                display_error(f"Unexpected error: {e}")
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")


if __name__ == "__main__":
    main()