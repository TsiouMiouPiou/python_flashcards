# TODO 1 = create a function that stores new words in a dictionary

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


# def add_words():
#     word = input('Enter a word: ').strip()
#     definition = input('Enter a definition: ').strip()
#     if word not in words:
#         words[word] = definition
#         json_object = json.dumps(words, indent=4)
#         with open("flashcards.json", "w") as json_file:
#             json_file.write(json_object)
#     else:
#         print("You already have that word!")

def add_words():
    prompt = str(input("Type 'n' for new deck or 'o' for old one ")).strip().lower()

    if prompt == "n":
        deck = str(input("Enter a deck name"))
        if deck in words:
            print("Deck already exists")
        else:
            words[deck] = {} # if deck is new initialize a dictionary

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
         print(WindowsError)





def delete_words():
    word = input('Delete a word: ').strip()
    if word not in words:
        print("You don't have that word!")
    else:
        words.pop(word)
        json_object = json.dumps(words, indent=4)
        with open("flashcards.json", "w") as json_file:
            json_file.write(json_object)


# TODO 2 = create a function that starts the game
def start():
    start_program = True
    while start_program:
        add_words()
        more = str(input("Do you want to add more words? (y/n): ")).lower().strip()
        if more == "y":
            start_program = True
        else:
            start_program = False

start()