class Bot:

    cards_path = "data.csv";

    def select_card(self, black_card, *white_cards):
        print("This should be implemented by subclasses")

    def judge_card(self, *white_cards):
        print("This should be implemented by subclasses")