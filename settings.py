class Settings:
    """Store Alien Invason settings"""
    def __init__(self, size="Medium"):
        self.bg_color = (230, 230, 230)
        # This line is for size="Fullscreen"; it needs to be refactorized
        self.ship_speed = 0.2

        #Bullet settings
        self.bullet_speed = 0.1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        if size == "Medium":
            self.screen_width = 1200
            self.screen_height = 800
            self.ship_speed = 1.5

        elif size == "Small":
            self.screen_width = 600
            self.screen_height = 440
            # Ship settings
            self.ship_speed = 0.07

            # #Bullet settings
            # self.bullet_speed = 0.1
            # self.bullet_width = 3
            # self.bullet_height = 15
            # self.bullet_color = (60, 60, 60)
