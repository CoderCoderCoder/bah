import json
import random
import spacy
import nltk
from nltk import wordnet as wn
from pprint import pprint


def load_whites():
    with open('base_deck.json') as f:
        whites = json.load(f)['whiteCards']

    print("imported number of white cards: " + str(len(whites)))

    return whites


whites = load_whites()
nlp = spacy.load('en_core_web_sm')
dictionary = {}
print 'hypernym example: ' + str(wn.wordnet.synset('clitoris.n.01').hypernyms())


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