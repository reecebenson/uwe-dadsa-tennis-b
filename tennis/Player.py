"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""

class Player():
    name = None
    gender = None
    season = None
    win_count = None
    lost_count = None
    total_win_count = None
    total_lost_count = None
    total_money = None
    in_first_16 = None

    def __init__(self, _name, _gender, _season):
        self.name = _name
        self.gender = _gender
        self.season = _season
        self.win_count = { }
        self.lost_count = { }
        self.total_win_count = 0
        self.total_lost_count = 0
        self.total_money = { }
        self.score = { }
        self.in_first_16 = False

    def get_name(self):
        return self.name

    def get_gender(self):
        return self.gender

    def get_season(self):
        return self.season

    def set_money(self, tournament_name, money):
        if(tournament_name in self.total_money):
            self.total_money[tournament_name] = money
        else:
            self.total_money.update({ tournament_name: money })

    def get_money(self, tournament_name):
        if(tournament_name in self.total_money):
            return self.total_money[tournament_name]
        else:
            self.set_money(tournament_name, 0)
            return self.get_money(tournament_name)

    def set_score(self, tournament_name, score):
        if(tournament_name in self.score):
            self.score[tournament_name] = score
        else:
            self.score.update({ tournament_name: score })

    def get_score(self, tournament_name):
        if(tournament_name in self.score):
            return self.score[tournament_name]
        else:
            self.set_score(tournament_name, 0)
            return self.get_score(tournament_name)

    def get_wins(self, tournament_name):
        if(tournament_name in self.win_count):
            return self.win_count[tournament_name]
        else:
            self.win_count.update({ tournament_name: 0 })
            return self.get_wins(tournament_name)

    def get_lost(self, tournament_name):
        if(tournament_name in self.lost_count):
            return self.lost_count[tournament_name]
        else:
            self.lost_count.update({ tournament_name: 0 })
            return self.get_lost(tournament_name)

    def get_total_wins(self):
        return self.total_win_count

    def get_total_lost(self):
        return self.total_lost_count

    def increment_wins(self, tournament_name):
        if(tournament_name in self.win_count):
            self.win_count[tournament_name] += 1
            self.total_win_count += 1
            return self.get_wins(tournament_name)
        else:
            self.win_count.update({ tournament_name: 0 })
            return self.increment_wins(tournament_name)

    def increment_losts(self, tournament_name):
        if(tournament_name in self.lost_count):
            self.lost_count[tournament_name] += 1
            self.total_lost_count += 1
            return self.get_lost(tournament_name)
        else:
            self.lost_count.update({ tournament_name: 0 })
            return self.increment_losts(tournament_name)