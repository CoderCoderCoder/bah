import random
import operator
import json
from numpy import average, multiply, dot
from numpy.linalg import norm
import spacy

nlp = spacy.load('en_core_web_sm')


def random_bot(black_key, white_keys, blacks, whites):
    """ Receives a black card prompt and a hand.
    Returns: key of randomly selected card"""
    return random.choice(white_keys)


def learning_bot(black_key, white_keys, blacks, whites):
    pass


def embedding_bot(black_key, white_keys, blacks, whites):
    """ Receives a black card prompt and a hand.
    Returns: key of the white card that is closest to
    the black one in word2vec space """

    btext = blacks[black_key]["text"]
    wtexts = [whites[white_key]["text"] for white_key in white_keys]

    b_vec = compute_sentence_embedding(btext)
    w_vecs = [compute_sentence_embedding(wtext) for wtext in wtexts]

    sims = [cos_sim(b_vec, w_vec) for w_vec in w_vecs]

    max_index, max_value = max(enumerate(sims), key=operator.itemgetter(1))

    return white_keys[max_index]


def cos_sim(a, b):
    return dot(a, b)/(norm(a)*norm(b))


def compute_sentence_embedding(sen):
    vecs = []

    doc = nlp(sen)
    for token in doc:
        if token.has_vector and not (token.is_stop or token.is_punct):
            if(token.pos_ == "VERB" or token.pos_ == "NOUN"):
                vecs.append(multiply(token.vector, 1.5))
            else:
                vecs.append(token.vector)

    embedding = average(vecs, axis=0)

    return embedding


if __name__ == "__main__":
    print("loading data...")
    print()
    with open('processed_deck.json') as f:
        deck = json.load(f)

    blacks = deck['blackCards']
    whites = deck['whiteCards']

    # deterministic
    # b = list(blacks.keys())[0]
    # ws = list(whites.keys())[:4]

    # non-determinstic
    b = random.choice(list(blacks.keys()))
    ws = random.sample(list(whites.keys()), 4)

    print("Black card:")
    print(blacks[b]["text"])
    print()
    print("White cards:")
    print([whites[w]["text"] for w in ws])

    print()
    print()
    print("testing...")

    sel_r = random_bot(b, ws, blacks, whites)
    sel_e = embedding_bot(b, ws, blacks, whites)

    print()
    print("Selecetd random: " + whites[sel_r]["text"])
    print("Selecetd embedding: " + whites[sel_e]["text"])
