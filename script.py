from datetime import datetime, timedelta
import json
import random

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATA_FILE = "flashcards.json"
# Load data from JSON or start fresh
try:
    with open("flashcards.json", "r") as json_file:
        words = json.load(json_file)
except (FileNotFoundError, json.JSONDecodeError):
    words = {}

def save_data():
    try:
        with open("flashcards.json", "w") as json_file:
            json.dump(words, json_file, indent=4)
    except FileNotFoundError:
        with open("flashcards.json", "w") as json_file:
            json.dump(words, json_file, indent=4)

def add_words():
    prompt = input("Type 'n' for new deck or 'o' for old one: ").strip().lower()
    if prompt == "n":
        deck = input("Enter a deck name: ").strip()
        if deck not in words:
            print(f'Deck "{deck}" is selected')
            words[deck] = {}
        else:
            print(f'Deck "{deck}" already exists, adding words to it...')

        filling = True
        while filling:
            word = input('Enter a word: ').strip()
            if word not in words[deck]:
                definition = input('Enter a definition: ').strip()
                words[deck][word] = {
                    "definition": definition,
                    "next_review": datetime.now().strftime(DATE_TIME_FORMAT)
                }
                save_data()
            else:
                print("This word already exists!")
            more = input("Do you want to add more? (y/n): ").strip().lower()
            if more != "y":
                filling = False

    elif prompt == "o":
        if not words:
            print("No decks available. Please create a new deck first.")
            return
        for d in words:
            print(f'- {d}')
        deck = input("Enter an old deck: ").strip()
        if deck in words:
            print(f'Deck "{deck}" is selected')
            filling = True
            while filling:
                word = input('Enter a word: ').strip()
                if word not in words[deck]:
                    definition = input('Enter a definition: ').strip()
                    words[deck][word] = {
                        "definition": definition,
                        "next_review": datetime.now().strftime(DATE_TIME_FORMAT)
                    }
                    save_data()
                else:
                    print("This word already exists!")
                more = input("Do you want to add more? (y/n): ").strip().lower()
                if more != "y":
                    filling = False
        else:
            print(f'Deck "{deck}" does not exist.')

def delete_words():
    choice = input('Type "deck" or "word" for deletion: ').strip().lower()
    if choice == "deck":
        if not words:
            print("No decks available to delete.")
            return
        for d in words:
            print(f'- {d}')
        deck = input("Enter a deck name to delete: ").strip()
        if deck in words:
            del words[deck]
            save_data()
            print(f'Deck "{deck}" has been deleted.')
        else:
            print(f'Deck "{deck}" does not exist.')

    elif choice == "word":
        if not words:
            print("No decks available.")
            return
        for d in words:
            print(f'- {d}')
        deck = input("Enter the deck name to delete words from or type 'exit': ").strip()
        if deck == "exit":
            return
        if deck not in words:
            print(f'Deck "{deck}" does not exist.')
            return
        while True:
            if not words[deck]:
                print(f'Deck "{deck}" is empty.')
                break
            for w in words[deck]:
                print(f'- {w}')
            word = input("Enter the word to delete or type 'exit': ").strip()
            if word == "exit":
                break
            if word in words[deck]:
                del words[deck][word]
                save_data()
                print(f'Word "{word}" deleted.')
            else:
                print(f'Word "{word}" does not exist.')

def play():
    if not words:
        print("No decks available to play.")
        return

    for deck in words:
        print(f'- {deck}')
    deck = input("Which deck do you want to play: ").strip().lower()

    if deck not in words:
        print(f'Deck "{deck}" does not exist.')
        return

    print(f'Deck "{deck}" is selected')

    now = datetime.now()
    due_words = [
        word for word, data in words[deck].items()
        if datetime.strptime(data["next_review"], DATE_TIME_FORMAT) <= now
    ]

    if not due_words:
        print("No cards are due for review right now.")
        return

    side = input('Which side do you want to play: "front" or "back"? ').strip().lower()
    random.shuffle(due_words)
    counter = 0

    if side == "front":
        for word in due_words:
            print(f'"{word}"')
            answer = input('Which is the correct definition?: ').strip().lower()
            correct_answer = words[deck][word]["definition"].lower()
            if answer == correct_answer:
                print("Correct!")
                counter += 1
                # IF CORRECT PLAY THE CARD AFTER 5 DAYS
                words[deck][word]["next_review"] = (datetime.now() + timedelta(days=5)).strftime(DATE_TIME_FORMAT)
            else:
                print(f"Wrong! Correct answer: {words[deck][word]['definition']}")
                # IF WRONG PLAY AFTER 5 MINS
                words[deck][word]["next_review"] = (datetime.now() + timedelta(minutes=5)).strftime(DATE_TIME_FORMAT)

    elif side == "back":
        for word in due_words:
            print(f'"{words[deck][word]["definition"]}"')
            answer = input('Which is the correct word?: ').strip().lower()
            if answer == word.lower():
                print("Correct!")
                counter += 1
                words[deck][word]["next_review"] = (datetime.now() + timedelta(days=5)).strftime(DATE_TIME_FORMAT)
            else:
                print(f"Wrong! Correct answer: {word}")
                words[deck][word]["next_review"] = (datetime.now() + timedelta(minutes=5)).strftime(DATE_TIME_FORMAT)

    total = len(due_words)
    percentage = counter / total * 100
    print(f'You found {counter} out of {total} words with {percentage:.2f}% success rate')

    save_data()

def show():
    if not words:
        print("No decks to show.")
        return
    for deck, cards in words.items():
        print(f"Deck: {deck}")
        for word, info in cards.items():
            definition = info["definition"]
            next_review = info["next_review"]
            print(f"  Word: {word}")
            print(f"    Definition: {definition}")
            print(f"    Next Review: {next_review}")

def start():
    while True:
        option = input(
            "Choose:\n 1.add \n 2.delete \n 3.play \n 4.show \n 5.quit\n"
        ).strip().lower()
        if option == "1" or option == "add":
            add_words()
        elif option == "2" or option == "delete":
            delete_words()
        elif option == "3" or option == "play":
            play()
        elif option == "4" or option == "show":
            show()
        elif option == "5" or option == "quit":
            print("Goodbye!")
            break
        else:
            print("Invalid input, please try again.")

start()
