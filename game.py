import json
import random
import os
from datetime import datetime

NUM_CARDS = 5

DISCARD_ALL = True

play_data = {}


def pick(deck, k):
    """ Returns a random selection of `k` cards, and the deck without them"""
    ids = list(deck.keys())
    choices = set(random.sample(ids, k=k))
    return {c: deck[c] for c in deck if c in choices}, {c: deck[c] for c in deck if c not in choices}


with open('processed_deck.json') as f:
    data = json.load(f)
    black_deck = data['blackCards']
    white_deck = data['whiteCards']

black_total_num = len(black_deck)

# Get initial hand
hand, white_deck = pick(white_deck, NUM_CARDS)


def print_hand(hand):
    for i, card in enumerate(hand.values()):
        print('[{0}] {1}'.format(i+1, card['text']))


print('Please enter your name')

player_name = input('> ')

print("\n\nLET'S PLAY!\n\n")

if not os.path.exists('data.csv'):
    with open('data.csv', 'w') as f:
        f.write("Timestamp,Player,Black_Card,Selected_card,Ignored_card\n")

while True:

    if len(black_deck) == 0 or len(white_deck) < NUM_CARDS:
        print('\n\nGAME OVER!\n\n')
        break

    bc, black_deck = pick(black_deck, 1)

    black_card_uid = list(bc.items())[0][0]
    black_card = list(bc.items())[0][1]

    print('\n\nBLACK CARD ({0}/{1}):'.format(len(black_deck)+1, black_total_num))
    print("-------------\n")
    print(black_card['text'])
    print("\n-------------\n")

    print_hand(hand)

    card_num = input("> ")

    while not (card_num in ('q', 'Q') or (card_num.isdigit() and 0 < int(card_num) <= len(hand))):
        print('ERROR: Please enter a number between 1 and {}, or `q` to quit'.format(
            len(hand))
        )
        card_num = input("> ")

    if card_num in ('q', 'Q'):
        print('\n\nYOU QUIT!\n\n')
        break

    id = int(card_num) - 1

    # FIXME: The same order is not guaranteed
    selection = list(hand.items())[id]

    print('You have selected: [{}]'.format(selection[1]['text']))

    timestamp = datetime.now().isoformat(timespec='seconds')

    with open('data.csv', 'a') as f:
        for wid in hand:
            if wid == selection[0]:
                continue
            f.write("{0},{1},{2},{3},{4}\n".format(timestamp, player_name,
                                                       black_card_uid, selection[0],
                                                       wid))
    if DISCARD_ALL:
        hand, white_deck = pick(white_deck, NUM_CARDS)
    else:
        del hand[selection[0]]
        wc, white_deck = pick(white_deck, 1)
        hand.update(wc)




