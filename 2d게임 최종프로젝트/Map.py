from pico2d import *
import main_state
import random


class Game_Map:
    def __init__(self):
        self.image = load_image('image/Map.png')
        self.font = load_font('ENCR10B.TTf', 12)

    def draw(self):
        self.image.draw(400, 300)
        self.font.draw(600, 575, 'Money: %2d' % main_state.Money, (255, 255, 0))
        self.font.draw(800 // 8, 575, 'Monster Left: %2d' % main_state.stage_monster_num, (255, 0, 0))

    def update(self):
        self.image.draw(400, 300)

    def handle_event(self, event):
        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            x = event.x
            y = event.y
            # x640 y100
            if 638 < x < 800 and 0 < 600 - y - 1 < 200:
                main_state.game_start = True
            elif 100 < x < 200 and 50 < 600 - y - 1 < 200:
                # re-roll
                character_count = random.randint(1, 5)
                main_state.character_in_re_roll_double_number = character_count
                main_state.character_in_re_roll_marco = 5 - main_state.character_in_re_roll_double_number

                pass
