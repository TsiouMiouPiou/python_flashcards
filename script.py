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


def add_words():
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

        # start filling an old one
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

    for deck in list(words.keys()):
        print(f'"{deck}" ')
        select_deck = str(input("Enter a deck name to delete: "))
        if select_deck in words:
            del words[select_deck]
            print(f'Deck {select_deck} has been deleted')
            json_object = json.dumps(words, indent=4)
            with open("flashcards.json", "w") as json_file:
                json_file.write(json_object)



    # if word not in words:
    #     print("You don't have that word!")
    # else:
    #     words.pop(word)
    #     json_object = json.dumps(words, indent=4)
    #     with open("flashcards.json", "w") as json_file:
    #         json_file.write(json_object)


# TODO 2 = create a function that starts the game
def start():
    add = str(input("Do you want to add words? (y/n) ")).strip().lower()
    if add == "y":
        add_words()
    elif add == "n":
        delete_words()

start()