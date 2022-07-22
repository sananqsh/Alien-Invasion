class Settings:
    """Store Alien Invason settings"""
    def __init__(self, size="Medium"):
        # Screen settings
        self.bg_color = (230, 230, 230)
        self.screen_width = 1200
        self.screen_height = 800

        # Ship settings
        self.ship_rotate_scale = 5

        # Pause time when ship got hit
        self.time_after_ship_hit = 0.5

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # Game statistics
        self.ship_limit = 3

        # Speed up scale
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

        if size != "Medium":
            self.modify_settings_by_size(size)

    def modify_settings_by_size(self, size):
        """modify settings based on size, if size of the game was not Medium"""
        if size == "Fullscreen":
            self.ship_speed *= 1.2
            self.bullet_speed *= 1.2
        elif size == "Small":
            self.screen_width //= 2
            self.screen_height //= 2

            self.ship_speed /= 20
            self.bullet_speed /= 10

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 4
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_intensity(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.speedup_scale)
