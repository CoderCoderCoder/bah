import json
import random
from pprint import pprint


def load_whites():
    with open('base_deck.json') as f:
        whites = json.load(f)['whiteCards']

    print("imported number of white cards: " + str(len(whites)))
    print("example: " + random.choice(whites))

    return whites


whites = load_whites()
