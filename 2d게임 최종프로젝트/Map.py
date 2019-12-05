from pico2d import *
import main_state

class Game_Map:
    def __init__(self):
        self.image = load_image('image/Map.png')
        self.font = load_font('ENCR10B.TTf', 12)

    def draw(self):
        self.image.draw(400, 300)
        self.font.draw(600, 575, 'Money: %2d' % main_state.Money, (255, 255, 0))
        self.font.draw(800 // 8, 575, 'Monster Left: %2d' % main_state.stage, (255, 0, 0))

    def update(self):
        self.image.draw(400, 300)
