import os
from settings import *


class Scores:  
    def __init__(self):        
        self.current_score = 0
        self.get_high_scores()

    def increase_score(self, increase):
        self.current_score += increase

    def reset_score(self):
        self.current_score = 0

    def get_high_scores(self):
        if not os.path.exists(HIGH_SCORES_FILE):
            open(HIGH_SCORES_FILE, "w")
        # set high score dictionaries with default values 
        self.high_scores = [{'name': "N/A", 'score': 0, 'level': 0} for _ in range(NUMBER_OF_HIGH_SCORES)]
        with open(HIGH_SCORES_FILE, 'r+') as file:
            data = file.read()
            scores_list = data.strip().split(",")
            for score_index in range(NUMBER_OF_HIGH_SCORES):
                # checks if the list of scores is long enough; else default is kept
                if len(scores_list) > score_index:                    
                    score_data = scores_list[score_index].strip().split(" ")
                    if len(score_data) == 3:
                        self.high_scores[score_index] = {'name': score_data[0], 
                                                        'score': int(score_data[1]), 
                                                        'level': int(score_data[2])}

        return self.high_scores

    def compare_current_score(self):
        for score_index in range(NUMBER_OF_HIGH_SCORES):
            if self.current_score > self.high_scores[score_index]['score']:
                return score_index
        return None

    def update_high_scores(self, name, level = 1):
        score_rank = self.compare_current_score()
        if score_rank is not None:
            self.high_scores.insert(score_rank,
                                    {'name': name, 
                                    'score': self.current_score, 
                                    'level': level})
            self.high_scores = self.high_scores[:NUMBER_OF_HIGH_SCORES]
            with open(HIGH_SCORES_FILE, 'w+') as file:
                for high_score in self.high_scores:
                    file.write(" ".join([high_score['name'], str(high_score['score']), str(high_score['level'])]) + ",")