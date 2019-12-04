from pico2d import *


class Game_Map:
    def __init__(self):
        self.image = load_image('image/Map.png')

    def draw(self):
        self.image.draw(400, 300)

    def update(self):
        self.image.draw(400, 300)
