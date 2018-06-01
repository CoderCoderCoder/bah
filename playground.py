from LearningAgent import LearningAgent

#Get the data and the cards, then generate the proper files to send to the Preference Learning Toolbox
LearningAgent.process_and_save_data('data.csv','processed_deck.json','test.cdata','test.pdatas')

#Get the RankSVM model from the toolbox by choosing the best parameters
#TODO: Add those parameters later

#Create a new Learning Agent based on the model generated using the Preference Learning Toolbox
bot = LearningAgent()
bot.learn_from_model('RankSVM.model')

