from datetime import datetime, timedelta
import json
import random
import os

DATA_FILE = "flashcards.json"

# ---------- Load Data ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as json_file:
            data = json.load(json_file)
            # Ensure backward compatibility with old format
            for deck in data:
                for word, val in list(data[deck].items()):
                    if isinstance(val, str):  # old format: definition only
                        data[deck][word] = {
                            "definition": val,
                            "next_review": datetime.now().strftime("%Y-%m-%d")
                        }
                    elif "next_review" not in val:
                        val["next_review"] = datetime.now().strftime("%Y-%m-%d")
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# ---------- Save Data ----------
def save_data():
    with open(DATA_FILE, "w") as json_file:
        json.dump(words, json_file, indent=4)

# ---------- Add Words ----------
def add_words():
    prompt = input("Type 'n' for new deck or 'o' for old one: ").strip().lower()
    if prompt == "n":
        deck = input("Enter a deck name: ").strip()
        if deck not in words:
            words[deck] = {}
            print(f'Deck "{deck}" is created')
        else:
            print(f'Deck "{deck}" already exists, adding words to it...')
        fill_deck(deck)

    elif prompt == "o":
        if not words:
            print("No decks exist yet!")
            return
        for deck in words:
            print(f'- {deck}')
        deck = input("Enter an old deck name: ").strip()
        if deck in words:
            fill_deck(deck)
        else:
            print(f'Deck "{deck}" does not exist')

def fill_deck(deck):
    while True:
        word = input('Enter a word: ').strip()
        if word not in words[deck]:
            definition = input('Enter a definition: ').strip()
            words[deck][word] = {
                "definition": definition,
                "next_review": datetime.now().strftime("%Y-%m-%d")
            }
            save_data()
        else:
            print("This word already exists!")
        more = input("Do you want to add more? (y/n): ").strip().lower()
        if more != "y":
            break

# ---------- Delete ----------
def delete_words():
    choice = input('Type "deck" or "word" for deletion: ').strip().lower()
    if choice == "deck":
        for deck in words:
            print(f'- {deck}')
        deck = input("Enter a deck name to delete: ").strip()
        if deck in words:
            del words[deck]
            save_data()
            print(f'Deck "{deck}" deleted')
        else:
            print("Deck not found")
    elif choice == "word":
        for deck in words:
            print(f'- {deck}')
        deck = input("Enter the deck to delete words from: ").strip()
        if deck not in words:
            print("Deck not found")
            return
        while True:
            for word in words[deck]:
                print(f'- {word}')
            w = input("Enter the word to delete or 'exit': ").strip()
            if w.lower() == "exit":
                break
            if w in words[deck]:
                del words[deck][w]
                save_data()
                print(f'Word "{w}" deleted')
            else:
                print("Word not found")

# ---------- Play ----------
def play():
    if not words:
        print("No decks exist yet!")
        return

    for deck in words:
        print(f'- {deck}')
    deck = input("Which deck do you want to play: ").strip()
    if deck not in words:
        print("Deck not found")
        return

    side = input('Which side do you want to play: "front" or "back"? ').strip().lower()
    today = datetime.now().date()
    word_list = [
        w for w, data in words[deck].items()
        if datetime.strptime(data["next_review"], "%Y-%m-%d").date() <= today
    ]

    if not word_list:
        print("No words are due for review today!")
        return

    random.shuffle(word_list)
    counter = 0

    for word in word_list:
        if side == "front":
            print(f'"{word}"')
            answer = input('Which is the correct answer?: ').strip().lower()
            if answer == words[deck][word]["definition"].lower():
                print("✅ Correct!")
                counter += 1
                words[deck][word]["next_review"] = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
            else:
                print(f"❌ Wrong! Correct answer: {words[deck][word]['definition']}")
        elif side == "back":
            print(f'"{words[deck][word]["definition"]}"')
            answer = input('Which is the correct answer?: ').strip().lower()
            if answer == word.lower():
                print("✅ Correct!")
                counter += 1
                words[deck][word]["next_review"] = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
            else:
                print(f"❌ Wrong! Correct answer: {word}")

    save_data()
    total = len(word_list)
    percentage = counter / total * 100
    print(f'\n📊 You got {counter}/{total} correct ({percentage:.1f}%)')

# ---------- Menu ----------
def start():
    while True:
        choice = input("\nChoose:\n 1. add \n 2. delete \n 3. play \n 4. quit\n> ").strip().lower()
        if choice in ["1", "add"]:
            add_words()
        elif choice in ["2", "delete"]:
            delete_words()
        elif choice in ["3", "play"]:
            play()
        elif choice in ["4", "quit", "q"]:
            break
        else:
            print("Invalid choice")

# ---------- Run ----------
words = load_data()
start()
