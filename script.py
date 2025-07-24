# TODO 3 = display all words in the dictionary
# TODO 4 = predefine the article. if der die das then store it automatically
# TODO 5 = create one dictionary for each type of word (noun, epi8eto, rima)
# TODO 6 = create a function that shows only the one side of the card
# TODO 7 optional -> give hints
import json

try:
    with open("flashcards.json" , "r") as json_file:
        words = json.load(json_file)
except (FileNotFoundError, json.JSONDecodeError):
    words = {}  # start fresh if file not found or empty


def add_words():   # IS WORKING FINE
    prompt = str(input("Type 'n' for new deck or 'o' for old one ")).strip().lower()
    if prompt == "n":
        deck = str(input("Enter a deck name"))
        if deck not in words:
            print(f'Deck "{deck}" is selected')
            words[deck] = {}  # if deck is new initialize a dictionary
        # start filling a new deck
        filling = True
        while filling:
            word = str(input('Enter a word: ')).strip()
            if word not in words[deck]:
                definition = input('Enter a definition: ').strip()
                words[deck][word] = definition
                json_object = json.dumps(words, indent=4)
                with open("flashcards.json", "w") as json_file:
                    json_file.write(json_object)
            else:
                print("This word already exists!")
            more = str(input("Do you want to add more? (y/n) ")).strip().lower()
            if more != "y":
                filling = False
    elif prompt == "o":
         for deck in words:
            print(f'Decks: {deck}')
         deck = str(input("Enter an old deck"))
         if deck in words:
             print(f'Deck "{deck}" is selected')
         elif deck not in words:
            print(f'Deck {deck} does not exist')
            add_words()

        # start filling an old one  = IS WORKING
         filling = True
         while filling:
             word = str(input('Enter a word: ')).strip()
             if word not in words[deck]:
                 definition = input('Enter a definition: ').strip()
                 words[deck][word] = definition
                 json_object = json.dumps(words, indent=4)
                 with open("flashcards.json", "w") as json_file:
                     json_file.write(json_object)
             else:
                 print("This word already exists!")

             more = str(input("Do you want to add more? (y/n) ")).strip().lower()
             if more == "n":
                 filling = False
             elif more == "y":
                 filling = True


def delete_words():
    # Delete a deck
    delete_deck_or_words = str(input('Type "deck" or "word" for deletion: ')).strip().lower()
    if delete_deck_or_words == "deck":
        for deck in words:
            print(f'Decks: "{deck}" ')
        select_deck = str(input("Enter a deck name to delete: "))
        if select_deck in words:
            del words[select_deck]
            print(f'Deck {select_deck} has been deleted')
            json_object = json.dumps(words, indent=4)
            with open("flashcards.json", "w") as json_file:
                json_file.write(json_object)
        elif select_deck not in words:
            print(f'Deck {select_deck} does not exist')
            delete_words()

    # Delete words from a deck
    elif delete_deck_or_words == "word":
        for deck in words:
            print(f'"{deck}" ')
        select_deck = str(input("Enter the deck name to delete the words from it: "))
        if select_deck in words:
            print(f'Selected Deck: "{select_deck}" ')

        for select_deck in words[select_deck]:
            print(f'"{select_deck}"')
        select_word = str(input("Which word do you want to delete: "))
        # Until here it works
        if select_word not in words[select_deck]:
            print(f'Word "{select_word}" does not exist')
            delete_words()
        elif select_word in words[select_deck]:

            del words[select_deck][select_word]
            print(f'Word "{select_word}" has been deleted')
            json_object = json.dumps(words, indent=4)
            with open("flashcards.json", 'w') as json_file:
                json_file.write(json_object)



# TODO 2 = create a function that starts the game
def start():
    add = str(input("Choose: 'add' or 'delete' ")).strip().lower()
    if add == "add":
        add_words()
    elif add == "delete":
        delete_words()
    else:
        print("Invalid input")

start()