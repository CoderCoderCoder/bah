from LearningAgent import LearningAgent
from importSVM import import_model

#Get the data and the cards, then generate the proper files to send to the Preference Learning Toolbox
la = LearningAgent()
la.process_and_save_data('all_data.csv','processed_deck_features.json','test.cdata','test.pdatas')
la.select_card('Ba3awX1yiTkSIlV7ESWD6Tw', 'WalAkS9-bTt-x2d7Y6RfDVA', 'WkTQ-d3JfSdeAMp2vQMwK6g')

#Get the RankSVM model from the toolbox by choosing the best parameters
#TODO: Add those parameters later

#Create a new Learning Agent based on the model generated using the Preference Learning Toolbox
##bot.learn_from_model('RankSVM.model')

#import_model('RankSVM.model', 'test.cdata')