from Bot import Bot
import random

class RandomAgent(Bot):

    def select_card(self, black_card, *white_cards):
        random.choice(list(white_cards))
