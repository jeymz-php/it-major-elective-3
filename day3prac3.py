def word_bank_program():
    words = []

    print("Welcome to the Word Bank Program!")
    print("=" * 40)

    while True:
        word = input("Enter a word: ").strip()

        if word:
            words.append(word)

        while True:
            choice = input("Do you want to try again? (y/n): ").strip().lower()
            if choice in ['y', 'n']:
                break
            else:
                print("Please enter 'y' for Yes or 'n' for No.")

        if choice == 'n':
            break

    print("=" * 20)

    print(f"Total number of words: {len(words)}")

    print("Words in the list:")
    for word in words:
        print(word)

    if words:
        sorted_words = sorted(words)
        print("Sorted words:")
        for word in sorted_words:
            print(word)

        longest_word = max(words, key=len)
        shortest_word = min(words, key=len)
        print(f"Longest word: {longest_word}")
        print(f"Shortest word: {shortest_word}")

        # Word search functionality
        search_word = input("Enter a word to search: ").strip()
        if search_word in words:
            print(f"'{search_word}' found in the word bank!")
        else:
            print(f"'{search_word}' not found in the word bank.")
    else:
        print("No words entered in the word bank.")

if __name__ == "__main__":
    word_bank_program()