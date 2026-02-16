import datetime

class Score:
    def __init__(self):
        self.scores = []
        file = open("scores.txt", mode="r")
        self.sort_score(file.readlines())
        self.this_score = 0
        file.close()

    def sort_score(self, previous_scores):
        all_scores = []

        for info in previous_scores:
            all_info = info.split("<>")
            score_int = int(all_info[2].strip())
            all_scores.append((score_int, all_info))
        
        all_scores.sort(key=lambda x: x[0], reverse=True)
        self.scores = all_scores

    def save_score(self, user):
        today = datetime.date.today()
        new_save = f"{today.year}-{today.month:02d}-{today.day:02d} <> {user} <> {self.this_score}"
        with open("scores.txt", "a") as file:
            file.write(new_save + "\n")
        