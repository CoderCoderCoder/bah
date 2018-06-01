import csv
import os
import json
import pprint
from Bot import Bot

class LearningAgent(Bot):

    #Processing DataSet
    def select_card(self, black_card, *white_cards):
        print("Not implemented yet")

    def judge_card(self, *white_cards):
        print("Not implemented yet")

    def learn_from_model(self, rank_svm_model):
        #TODO: Import from Phil Lopes code
        pass

    @staticmethod
    def process_and_save_data(data_path, cards_path, combination_path, preference_path):
        comb, pref, lookup = LearningAgent.__process_data(data_path, cards_path)
        print(comb)

        # Print some info for testing
        print('number of combinations: ' + str(len(comb)))
        print('number of pref: ' + str(len(pref)))
        print('number of distinct preferences: ' + str(len(set(pref))))

        # Create combinations file
        with open(combination_path, 'w') as f:
            for key, value in comb.items():
                feature_string = ",".join(map(str, value))
                f.write("{0},{1}\n".format(key, feature_string))

        # Create preference file
        with open(preference_path, 'w') as f:
            for pref in pref:
                f.write("{0}\n".format(pref))

    @staticmethod
    def __generate_combo_key(black, white):
        return black + ' ' + white

    @staticmethod
    def __extract_features(card_features, black, white):
        black_features = card_features[black]
        white_features = card_features[white]

        #TODO: Discover how they are presenting the data. Adjust bellow accordingly
        return {}

    @staticmethod
    def __process_data(data_path, cards_path):
        combinations = dict()
        preferences = list()
        lookup_table = dict()
        card_features = dict()

        #Get the cards features
        with open(cards_path, 'r') as card_file:

            card_data = json.load(card_file)
            for id, card in card_data['blackCards'].items():
                card_features[id] = card["features"]

            for id, card in card_data['whiteCards'].items():
                card_features[id] = card["features"]

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

                    best_card_key = LearningAgent.__generate_combo_key(black_card, best_white_card)
                    worst_card_key = LearningAgent.__generate_combo_key(black_card, worst_white_card)

                    #Check if it was already used
                    if best_card_key not in lookup_table.keys():
                        #Create a new ID
                        best_card_id = lookup_table[best_card_key] = len(lookup_table) + 1
                        #Create a new Combination
                        combinations[best_card_id] = LearningAgent. __extract_features(card_features, black_card, best_white_card)
                    else:
                        # Get the available ID
                        best_card_id = lookup_table[best_card_key]

                    if worst_card_key not in lookup_table.keys():
                        #Create a new ID
                        worst_card_id = lookup_table[worst_card_key] = len(lookup_table) + 1
                        # Create a new Combination
                        combinations[worst_card_id] = LearningAgent.__extract_features(card_features, black_card, worst_white_card)
                    else:
                        #Get the available ID
                        worst_card_id = lookup_table[worst_card_key]

                    #Add to preferences
                    preferences.append(str(best_card_id) + ',' + str(worst_card_id))

                n_row += 1
                print(row)

        return combinations, preferences, lookup_table