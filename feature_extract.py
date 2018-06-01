import json
import random
import spacy
import string
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


# counting the frequencies of hypernyms of each noun form
for sen in whites:
    doc = nlp(sen)
    for token in doc:
        if token.pos_ == 'NOUN' and len(wn.wordnet.synsets(token.lemma_, pos='n')) > 0:
            hypernyms = wn.wordnet.synsets(token.lemma_, pos='n')[0].hypernym_paths()[0]
            max_index = len(hypernyms) - 1
            if len(hypernyms) > 3:
                max_index = 3
            chosenHypernym = str(hypernyms[max_index]).split('.')[0].split('\'')[1]

            if chosenHypernym in dictionary:
                dictionary[chosenHypernym] +=1
            else:
                dictionary[chosenHypernym] =1
            #print 'LEMMA: ' + str(token.lemma_) + ' HYPERNYM: ' + str(chosenHypernym)


for sen in whites:
    doc = nlp(sen)
    mostCommonHypernym = ''
    freqMostCommonHypernym = 0
    print sen
    for token in doc:
        if token.pos_ == 'NOUN' and len(wn.wordnet.synsets(token.lemma_, pos='n')) > 0:
            hypernyms = wn.wordnet.synsets(token.lemma_, pos='n')[0].hypernym_paths()[0]
            max_index = len(hypernyms) - 1
            if len(hypernyms) > 3:
                max_index = 3
            chosenHypernym = str(hypernyms[max_index]).split('.')[0].split('\'')[1]
            print 'LEMMA: ' + str(token.lemma_) + ' HYPERNYM: ' + str(chosenHypernym)

            if dictionary[chosenHypernym] > freqMostCommonHypernym:
                freqMostCommonHypernym = dictionary[chosenHypernym]
                mostCommonHypernym = chosenHypernym

    print 'CHOSEN HYPERNYM: ' + chosenHypernym
    print '------------------------------------------'


