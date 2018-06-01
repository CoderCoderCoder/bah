import random
import json


def random_bot(black_key, white_keys, blacks, whites):
    """ Receives a black card prompt and a hand.
    Returns: key of randomly selected card"""
    return random.choice(white_keys)


def learning_bot(black_key, white_keys, blacks, whites):
    pass


def embedding_bot(black_key, white_keys, blacks, whites):
    pass


if __name__ == "__main__":
    print("loading data...")
    with open('processed_deck.json') as f:
        deck = json.load(f)

    blacks = deck['blackCards']
    whites = deck['whiteCards']

    print("testing...")

    b = list(blacks.keys())[0]
    ws = list(whites.keys())[:4]
    print(b)
    print(ws)

    sel = random_bot(b, ws, blacks, whites)

    print("Selecetd: " + sel)
