class GameStats:
    """Track statistics for Alien Invasion game."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start Alien Inv. game in an inactive state.
        self.game_active = False

        self.level = 1

        # Import high score from a file
        self.import_high_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0

    def import_high_score(self):
            try:
                with open(self.settings.high_score_path, 'r') as f:
                    contents = f.read()
                    print(contents)

                    self.high_score = int(contents[12:])

                    print(f"self.high_score: {self.high_score}")
            except FileNotFoundError:
                self.high_score = 0
