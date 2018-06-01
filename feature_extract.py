import json
import spacy
import nltk
from nltk import wordnet as wn
from pprint import pprint

nlp = spacy.load('en_core_web_sm')


def load_texts(whites=False):
    with open('processed_deck.json') as f:
        deck = json.load(f)

    blacks = deck['blackCards']
    whites = deck['whiteCards']

    print("imported number of white cards: " + str(len(whites)))
    print("imported number of black cards: " + str(len(blacks)))

    if whites:
        return [whites[key]["text"] for key in whites]

    all_c = blacks.copy()
    all_c.update(whites)
    return [all_c[key]["text"] for key in all_c]


def check_wn_installed():
    print("Checking if wordnet is already installed, installl if not")
    try:
        nltk.data.find('wordnet')
    except LookupError:
        nltk.download('wordnet')


def get_root(doc):
    root = ""
    for token in doc:
        if token.dep_ == "ROOT":
            root = token.lemma_
    return root


def go_to_wn_level(syn, level=3):
    hypernyms = syn.hypernym_paths()[0]
    max_index = len(hypernyms) - 1
    if len(hypernyms) > level:
        max_index = level
    return hypernyms[max_index]


def feature_synset_num(doc):
    """" Computes the average number of synsets in the card excluding stop words.
         rerturn: float"""
    syn_num = 0
    word_count = 0
    for token in doc:
        if not (token.is_stop or token.is_punct):
            syn_num += len(wn.wordnet.synsets(token.lemma_))
            word_count += 1
    return syn_num/word_count


def feature_root_concept(doc):
    """ Computes the head word of the sentence; if it is in wordnet, identifies
        its base-level category (level=3, avg_num of instaces per cat: 4.7),
        otherwise uses just the word itself (fallback)
        return: int (hash of category/word)
    """
    head = get_root(doc)

    syns = wn.wordnet.synsets(head)
    if syns:
        concept = go_to_wn_level(syns[0], level=3)
        return hash(concept.name())

    return hash(head)


def feature_POS(doc):
    """ Determines the POS of the text, ignoringstop words and punctation
        (average num of POS sequence re-occurance is ~2.1)
        return: int (hash of POS string)
    """
    pos_string = ""
    for token in doc:
        if not (token.is_stop or token.is_punct):
            pos_string += token.pos_

    return hash(pos_string)


def compute_all_features():
    texts = load_texts()
    for sen in texts[:15]:
        doc = nlp(sen)
        f1 = feature_synset_num(doc)
        f2 = feature_root_concept(doc)
        f3 = feature_POS(doc)
        print(sen)
        print(f1, f2, f3)
        print()


whites = load_texts(whites=True)
dictionary = {}
print('hypernym example: ' + str(wn.wordnet.synset('clitoris.n.01').hypernyms()))


for sen in whites:
    doc = nlp(sen)
    for token in doc:
        if token.pos_ == 'NOUN' and len(wn.wordnet.synsets(token.lemma_, pos='n')) > 0:
            hypernyms = wn.wordnet.synsets(token.lemma_, pos='n')[0].hypernym_paths()[0]
            max_index = len(hypernyms) - 1
            if len(hypernyms) > 3:
                max_index = 3
            if hypernyms[max_index] in dictionary:
                dictionary[hypernyms[max_index]] +=1
            else:
                dictionary[hypernyms[max_index]] =1
#print 'LEMMA: ' + str(token.lemma_) + ' HYPERNYM: ' + str(wn.wordnet.synset(token.lemma_ + '.n.01').hypernyms())


pprint(dictionary)
