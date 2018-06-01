import json
from pprint import pprint

class Bot:

    cards_path = "data.csv";

    def select_card(self, black_card, *white_cards):
        print("This should be implemented by subclasses")
