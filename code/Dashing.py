import pygame

class Dash:
    def __init__(self, velocity, run_time):
        self.vector = pygame.Vector2()
        self.velocity = velocity
        self.run_time = run_time
        self.is_dashing = False
        self.timer = -1

    def can_dash(self):
        return not self.is_dashing and self.timer == -1

    def end(self):
        self.is_dashing = False
        self.timer = -1

    def start(self, vector):
        if self.can_dash():
            self.timer = self.run_time
            self.is_dashing = True
            self.vector = vector

    def update(self, delta):
        if self.is_dashing:
            self.timer -= delta
            if self.timer <= 0:
                self.end()