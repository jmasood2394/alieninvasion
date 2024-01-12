class GameStats:
    """ Track game stats """
    def __init__(self, game):
        """ Initialize the stats """
        self.settings = game.settings
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):
        """ Initialize the stats that change during the game """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1


