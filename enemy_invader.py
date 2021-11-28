import arcade

from constants import *


class EnemyInvader(arcade.Sprite):
    def __init__(self, texture_1, texture_2):
        super().__init__()
        self.texture_1 = texture_1
        self.texture_2 = texture_2
        self.time = 0
        self.dead = False
        self.score = 0

        self.texture = self.texture_1

    def on_update(self, dt):
        self.time += dt
        if self.dead:
            if self.time >= 0.5:
                self.remove_from_sprite_lists()
            return

        t = int(self.time * 2)
        t2 = t % 2
        if t2 == 0:
            self.texture = self.texture_1
        elif t2 == 1:
            self.texture = self.texture_2

    def explode(self):
        self.texture = arcade.load_texture("images/enemy_explosion.png")
        self.dead = True
        self.time = 0
        self.color = ENEMY_EXPLOSION_COLOR
