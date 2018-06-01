import json
import spacy
import string
import random
import nltk
from nltk import wordnet as wn
from pprint import pprint
from agents import compute_sentence_embedding, cos_sim

nlp = spacy.load('en_core_web_sm')


def load_texts(whites_only=False):
    with open('processed_deck.json') as f:
        deck = json.load(f)

    blacks = deck['blackCards']
    whites = deck['whiteCards']

    if whites_only:
        return [whites[key]["text"] for key in whites]

    all_c = blacks.copy()
    all_c.update(whites)
    return [all_c[key]["text"] for key in all_c]


def load_jsons():
    with open('processed_deck.json') as f:
        deck = json.load(f)

    blacks = deck['blackCards']
    whites = deck['whiteCards']

    print("imported number of white cards: " + str(len(whites)))
    print("imported number of black cards: " + str(len(blacks)))

    return blacks, whites


def save_json(blacks, whites):
    data = {'blackCards': blacks, 'whiteCards': whites}

    with open('processed_deck_features.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


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


def feature_most_freq_noun_hypernym(noun_hypernyms, doc):
    """ Choose the most frequent noun hypernym in a setence
        among all the dataset
        return: int (hash of hypernym string)
    """

    mostCommonHypernym = ''
    freqMostCommonHypernym = 0
    for token in doc:
        if token.pos_ == 'NOUN' and len(wn.wordnet.synsets(token.lemma_, pos='n')) > 0:
            hypernyms = wn.wordnet.synsets(token.lemma_, pos='n')[0].hypernym_paths()[0]
            max_index = len(hypernyms) - 1
            if len(hypernyms) > 3:
                max_index = 3
            chosenHypernym = str(hypernyms[max_index]).split('.')[0].split('\'')[1]
            if noun_hypernyms[chosenHypernym] > freqMostCommonHypernym:
                freqMostCommonHypernym = noun_hypernyms[chosenHypernym]
                mostCommonHypernym = chosenHypernym

    return hash(mostCommonHypernym)


def feature_sentences_similarity(sentence1, sentence2):
    doc = nlp(sentence1)
    sentence1 = ' '.join([token.text for token in doc if not (token.is_stop or token.is_punct)])
    doc = nlp(sentence2)
    sentence2 = ' '.join([token.text for token in doc if not (token.is_stop or token.is_punct)])
    vec1 = compute_sentence_embedding(sentence1)
    vec2 = compute_sentence_embedding(sentence2)
    distance = cos_sim(vec1, vec2)
    return distance


def feature_sexual_content(doc):
    """ Detects if any word contains sexual meaning
        considering a predefined list
        return: int (bool of hypernym string)
    """

    sexual_words =['sex',
    'penis',
    'vagina',
    'boob',
    'gay',
    'intercourse',
    'orgasm',
    'porn',
    'balls',
    'necrophilia',
    'boner',
    'clitoris',
    'viagra']

    for sw in sexual_words:
        for token in doc:
            if token.lemma_.find(sw) != -1:
                return 1
    else:
        return 0


def feature_black_card_type(doc, card_t):
    """ Determines the whether the black card has a whitespace
    or a question.
        return: int (0:whitespace, 1:question, 2:non-black)
    """
    if card_t == "w":
        return 2

    question = False
    white_space = False
    for token in doc:
        if token.text == "_":
            white_space = True
        if token.text == "?":
            question = True

    # make sure that a question in first sentence doesnt conceal a white space
    # in the end
    if white_space:
        return 0
    if question:
        return 1
    return 2


def feature_text_length(doc):
    """ Determines the length of a text ecluding stop words and
        punctuation.
        return: int
    """

    return len([token for token in doc if not (token.is_stop or token.is_punct)])


def feature_ner_type(doc):
    """
        Indetifies the number and types of named entities in the doc,
        returns both.
        return: int
    """
    ents = []
    for ent in doc.ents:
        ents.append(ent.label_)

    return len(ents), hash("".join(ents))


def get_all_noun_hypernyms(sentences):
    """ Counts the frequencies of hypernyms of each noun form of a set of sentences
        return: dictionary
    """

    dictionary = {}

    for sen in sentences:
        doc = nlp(sen)
        for token in doc:
            if token.pos_ == 'NOUN' and len(wn.wordnet.synsets(token.lemma_, pos='n')) > 0:
                hypernyms = wn.wordnet.synsets(token.lemma_, pos='n')[0].hypernym_paths()[0]
                max_index = len(hypernyms) - 1
                if len(hypernyms) > 3:
                    max_index = 3
                chosenHypernym = str(hypernyms[max_index]).split('.')[0].split('\'')[1]

                if chosenHypernym in dictionary:
                    dictionary[chosenHypernym] += 1
                else:
                    dictionary[chosenHypernym] = 1
    return dictionary


def compute_feature_for(sen, noun_hypernyms, card_type):
    doc = nlp(sen)
    f1 = feature_synset_num(doc)
    f2 = feature_root_concept(doc)
    f3 = feature_POS(doc)
    f4 = feature_most_freq_noun_hypernym(noun_hypernyms, doc)
    f5 = feature_sexual_content(doc)
    f6 = feature_black_card_type(doc, card_type)
    f7 = feature_text_length(doc)
    f8, f9 = feature_ner_type(doc)

    features = {"ambiguity": f1, "root_concept": f2, "POS": f3,
                "best_hypernym": f4, "sexual_content": f5,
                "black_card_type": f6, "text_len": f7,
                "num_ne": f8, "nes": f9}

    #print(sen)
    #print(features)
    #print()

    return features


def compute_all_features():
    blacks, whites = load_jsons()

    texts = load_texts()
    noun_hypernyms = get_all_noun_hypernyms(texts)

    # compute black features
    for key in list(blacks.keys()):
        sen = blacks[key]["text"]
        features = compute_feature_for(sen, noun_hypernyms, blacks[key]["color"])
        blacks[key]["features"] = features

    # compute white features
    for key in list(whites.keys()):
        sen = whites[key]["text"]
        features = compute_feature_for(sen, noun_hypernyms, whites[key]["color"])
        whites[key]["features"] = features

    return blacks, whites


if __name__ == "__main__":
    bs, ws = compute_all_features()
    save_json(bs, ws)
