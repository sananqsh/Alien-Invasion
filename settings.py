class Settings:
    """Store Alien Invason settings"""
    def __init__(self, size="Medium"):
        standard_screen_width = 1200
        standard_screen_height = 800

        #Ship settings
        standard_ship_speed = 1.5
        standard_ship_rotate_scale = 5

        self.bg_color = (230, 230, 230)
        self.ship_rotate_scale = standard_ship_rotate_scale

        #Bullet settings
        self.bullet_speed = 0.1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        if size == "Medium":
            self.screen_width = standard_screen_width
            self.screen_height = standard_screen_height

            self.ship_speed = standard_ship_speed

        elif size == "Small":
            self.screen_width = standard_screen_width / 2
            self.screen_height = standard_screen_height / 2

            self.ship_speed = standard_ship_speed / 20
