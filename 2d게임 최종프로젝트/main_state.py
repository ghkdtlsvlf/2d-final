import random
import json
import os

from pico2d import *

import game_framework
import title_state
import Member_function
from Map import Game_Map
from Double_Gun_Charcter import Double_Gun_Character

name = "MainState"

Main_Game_Wait_Timer = Member_function.GAME_WAIT_TIMER
Main_Game_Play_Timer = Member_function.GAME_PLAY_TIMER

game_map = None
double_gun_character = None
double_gun_character1 = None


def enter():
    global game_map, double_gun_character
    game_map = Game_Map()
    double_gun_character = Double_Gun_Character()
    double_gun_character1 = Double_Gun_Character()
    pass


def exit():
    global game_map, double_gun_character
    del game_map
    del double_gun_character
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(title_state)
        else:
            double_gun_character.handle_event(event)

    pass


def update():
    double_gun_character.update()
    pass


def draw():
    clear_canvas()
    game_map.draw()
    double_gun_character.draw()
    update_canvas()
    pass
