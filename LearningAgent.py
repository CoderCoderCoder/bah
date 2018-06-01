import csv
import os
import json
import random
from pprint import  pprint
from Bot import Bot
from importSVM import import_model
import sys

class LearningAgent(Bot):

    def __init__(self):
        self.combinations = dict()
        self.preferences = list()
        self.lookup_table = dict()
        self.card_features = dict()
        self.global_order = dict()

    #Processing DataSet
    def select_card(self, black_card, *white_cards):

        better_card = 0
        better_position = -sys.maxsize - 1

        for white_card in list(white_cards):
            #Get the combo key  and look into the translation
            combo_id = self.lookup_table[self.__generate_combo_key(black_card, white_card)]
            combo_features = self.combinations[combo_id]
            print(combo_features)
            #TODO: Know what is in the keys in global order

            combo_position = self.global_order[combo_features]
            if(combo_position < better_position):
                better_card = white_card
                better_position = combo_position

        return better_card

    def __get_card_features(self, card_key):
        return self.card_features[card_key]

    def learn_from_model(self, rank_svm_model):
        #Import from Phil Lopes code
        self.global_order = import_model(rank_svm_model,'all_data.csv') #this should be assigned to a variable

    def process_and_save_data(self, data_path, cards_path, combination_path, preference_path):
        comb, pref, lookup, card_features = self.__process_data(data_path, cards_path)

        # Print some info for testing
        print('number of combinations: ' + str(len(comb)))
        print('number of pref: ' + str(len(pref)))
        print('number of distinct preferences: ' + str(len(set(pref))))

        # Create combinations file
        with open(combination_path, 'w') as f:
            id, card = random.choice(list(card_features.items()))
            black_features_name = ['b_{0}'.format(i) for i in card.keys()]
            white_features_name = ['w_{0}'.format(i) for i in card.keys()]
            f.write("{0},{1},{2}\n".format('ID', ','.join(black_features_name), ','.join(white_features_name)))
            for key, value in comb.items():
                feature_string = ",".join(map(str, value))
                f.write("{0},{1}\n".format(key, feature_string))

        # Create preference file
        with open(preference_path, 'w') as f:
            for pref in pref:
                f.write("{0}\n".format(pref))

    def __generate_combo_key(self, black, white):
        return black + ' ' + white

    def __process_data(self, data_path, cards_path):

        #Get the cards features
        with open(cards_path, 'r') as card_file:

            card_data = json.load(card_file)
            for id, card in card_data['blackCards'].items():
                self.card_features[id] = card["features"]

            for id, card in card_data['whiteCards'].items():
                self.card_features[id] = card["features"]

        #Create all possible combinations
        with open(cards_path, 'r') as card_file:
            card_data = json.load(card_file)

            #Update lookup table and combination
            lookup_table_id = 0
            for b_id, b_card in card_data['blackCards'].items():
                for w_id, w_card in card_data['whiteCards'].items():

                    #Create lookup entry
                    combined_card_name = self.__generate_combo_key(b_id, w_id)
                    self.lookup_table[combined_card_name] = lookup_table_id
                    lookup_table_id += 1

                    #Create the combination feature
                    combined_features = list(self.card_features[b_id].values()) + list(self.card_features[w_id].values())
                    self.combinations[self.lookup_table[combined_card_name]] = combined_features

        #Process the playing hands
        with open(data_path, 'r') as csv_file:
            csv_stream = csv.reader(csv_file, delimiter =',')

            n_row = 0

            for row in csv_stream:
                if n_row == 0:
                    #This is a header
                    print('THIS IS A HEADER')
                else:
                    black_card = row[2]
                    best_white_card = row[3]
                    worst_white_card = row[4]

                    best_card_key = self.__generate_combo_key(black_card, best_white_card)
                    worst_card_key = self.__generate_combo_key(black_card, worst_white_card)

                    best_card_combo_id = self.lookup_table[best_card_key]
                    worst_card_combo_id = self.lookup_table[worst_card_key]
                    self.preferences.append(str(best_card_combo_id) + ',' + str(worst_card_combo_id))

                n_row += 1

        return self.combinations, self.preferences, self.lookup_table, self.card_features
