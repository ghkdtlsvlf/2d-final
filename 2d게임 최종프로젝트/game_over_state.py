import game_framework
import main_state
import title_state
from pico2d import *

name = "Gameover_state"
image = None


def enter():
    global image
    image = load_image('image/gameover.PNG')
    pass


def exit():
    global image
    del image
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                main_state.game_start = False
                main_state.stage_count = 0
                main_state.Money = 20
                main_state.character_in_re_roll_double_number = 5
                main_state.character_in_re_roll_marco = 0
                main_state.character_box = [235, 320, 410, 500, 580]
                game_framework.change_state(title_state)

    pass


def draw():
    clear_canvas()
    image.draw(400,300)
    update_canvas()
    pass


def update():
    pass


def pause():
    pass


def resume():
    pass
