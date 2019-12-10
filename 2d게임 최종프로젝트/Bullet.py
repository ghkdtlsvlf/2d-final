from pico2d import *
import game_world

import game_framework


class Bullet:
    image = None

    def __init__(self, x=400, y=200):
        if Bullet.image == None:
            Bullet.image = load_image('image/bullet_attack.png')

        self.x = x
        self.y = y
        self.attack_speed = 40
        self.damage = 3

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

        pass

    def update(self):
        self.x += self.attack_speed
        if self.x >= 800:
            game_world.remove_object(self)
        pass

    def draw(self):
        self.image.draw(self.x + 40, self.y + 22)
        pass
