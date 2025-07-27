from datetime import datetime, timedelta
import json
import random

try:
    with open("flashcards.json" , "r") as json_file:
        words = json.load(json_file)
except (FileNotFoundError, json.JSONDecodeError):
    words = {}  # start fresh if file not found or empty

def save_data():
    try:
        with open("flashcards.json", "w")as json_file:
            json.dump(words, json_file, indent=4)
    except FileNotFoundError:
        with open("flashcards.json", "w") as json_file:
            json.dump(words, json_file, indent=4)

        

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
                save_data()
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

         filling = True
         while filling:
             word = str(input('Enter a word: ')).strip()
             if word not in words[deck]:
                 definition = input('Enter a definition: ').strip()
                 words[deck][word] = definition
                 save_data()
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
    while delete_deck_or_words == "deck":
        for deck in words:
            print(f'Decks: "{deck}" ')
        select_deck = str(input("Enter a deck name to delete: "))
        if select_deck in words:
            del words[select_deck]
            print(f'Deck {select_deck} has been deleted')
            save_data()
        elif select_deck not in words:
            print(f'Deck {select_deck} does not exist')
            delete_words()

    # Delete words from a deck
    if delete_deck_or_words == "word":
        deleting = True
        for deck in words:
            print(f'"{deck}" ')
        select_deck = str(input("Enter the deck name to delete the words from it or type 'exit' to exit: "))
        if select_deck in words:
            print(f'Selected Deck: "{select_deck}" ')
        while deleting:
            for word in words[select_deck]:
                print(f'"{word}"')
            select_word = str(input("Which word do you want to delete or type 'exit' to exit: "))
            if select_word == "exit":
                deleting = False
                start()
            elif select_word not in words[select_deck]:
                print(f'Word "{select_word}" does not exist')
                delete_words()
            elif select_word in words[select_deck]:
                del words[select_deck][select_word]
                print(f'Word "{select_word}" has been deleted')
                save_data()


def play():
    for deck in words:
        print(f'"{deck}"')
    deck = str(input("Which deck do you want to play: ")).strip().lower()
    if deck not in words:
        print(f'Deck "{deck}" does not exist')
    elif deck in words:
        print(f'Deck "{deck}" is selected')
        side = str(input('Which side do you want to play: "front" or "back" ?')).strip().lower()
        # FRONT SIDE
        if side == "front":
                word_list = list(words[deck].keys())
                random.shuffle(word_list)
                counter = 0
                for word in word_list: # word is the key
                    print(f'"{word}"')
                    answer = str(input('Which is the correct answer?: ')).strip().lower()
                    if answer == words[deck][word]: # answer is the value
                        print("Correct!")
                        counter += 1
                    # Then mark it as corrected and play it after 5 days
                    else:
                         print("Wrong!")
                         counter = counter
                    total = len(word_list) # length of words that I played
                    percentage = counter / total * 100
                    print(f'You found {counter} out of {total} words with {percentage:}% success')

        # BACK SIDE
        elif side == "back":
            word_list = list(words[deck].keys())
            random.shuffle(word_list)
            counter = 0
            for word in word_list:
                print(f'"{words[deck][word]}"') # print the values or definition
                answer = str(input('Which is the correct answer?: ')).strip().lower()
                if answer == word:
                    print("Correct!")
                    counter += 1
                else:
                    print("Wrong!")
                total = len(word_list)
                percentage = counter / total * 100
                print(f'You found {counter} out of {total} words, with {percentage:}% success rate')




def start():
    add = str(input("Choose:\n 1.add \n 2.delete \n 3.play ")).strip().lower()
    if add == "add":
        add_words()
    elif add == "delete":
        delete_words()
    elif add == "play":
        play()
    else:
        print("Invalid input")

start()