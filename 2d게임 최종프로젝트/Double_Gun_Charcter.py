from pico2d import *
import random
import game_world
import math
import game_framework
import main_state
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pynput.mouse import Controller

# gun_c Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

from Member_function import *

Left_Mouse_UP, Left_Mouse_Down = range(2)

key_event_table = {
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): Left_Mouse_Down,
    (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT): Left_Mouse_UP
}


class Idle_State:
    @staticmethod
    def enter(double_gun_chac, event):
        if event == Left_Mouse_Down:
            global x, y
            # 이미 눌러진 상태면은 이동
            if double_gun_chac.selected and double_gun_chac.attack_state == False and main_state.Money >= 2:
                double_gun_chac.x = x
                double_gun_chac.y = 600 - 1 - y
                double_gun_chac.selected = False
                main_state.Money -= 2
            # 캐릭터 클릭 및 취소
            else:
                if double_gun_chac.x - 50 < x < double_gun_chac.x + 50 and \
                        double_gun_chac.y - 50 < 600 - y - 1 < double_gun_chac.y + 50:
                    double_gun_chac.selected = True
                else:
                    double_gun_chac.selected = False
        pass

    @staticmethod
    def exit(double_gun_chac, event):
        pass

    @staticmethod
    def do(double_gun_chac):
        double_gun_chac.frame = (double_gun_chac.frame + 1) % 6
        double_gun_chac.attack_frame = (double_gun_chac.attack_frame + 1) % 6
        pass

    @staticmethod
    def draw(double_gun_chac):
        if not double_gun_chac.attack_state:
            double_gun_chac.image.clip_draw(double_gun_chac.frame * 100, 0, 100, 100, double_gun_chac.x,
                                            double_gun_chac.y)
            if double_gun_chac.y >= 160:
                double_gun_chac.image_hp.clip_draw(0, 0, double_gun_chac.hp, 11, double_gun_chac.x - 13,
                                                   double_gun_chac.y - 50)
            if double_gun_chac.selected:
                draw_rectangle(*double_gun_chac.get_bb())
        else:
            double_gun_chac.image.clip_draw(double_gun_chac.frame * 100, 200, 80, 100, double_gun_chac.x,
                                            double_gun_chac.y)
            double_gun_chac.image_attack.clip_draw(double_gun_chac.attack_frame * 130, 0, 120, 150,
                                                   double_gun_chac.x + 70, double_gun_chac.y + 40)
            double_gun_chac.image_hp.clip_draw(0, 0, double_gun_chac.hp, 11, double_gun_chac.x - 13,
                                               double_gun_chac.y - 50)
            if double_gun_chac.attack_frame ==1:
                double_gun_chac.gun_fire()
        pass


next_state_table = {
    Idle_State: {Left_Mouse_UP: Idle_State, Left_Mouse_Down: Idle_State},
}


class Double_Gun_Character:
    image = None
    image_attack = None
    image_hp = None

    def __init__(self):

        self.y = 85
        if Double_Gun_Character.image == None:
            Double_Gun_Character.image = load_image('image/Double_gun_mode.png')
            Double_Gun_Character.image_attack = load_image('image/gun_fire2.png')
            Double_Gun_Character.image_hp = load_image('image/hp.png')

        self.x = main_state.character_box[0]
        main_state.character_box.remove(main_state.character_box[0])
        self.attack_frame = 0
        self.frame = 0
        self.hp = 100
        self.mp = 0
        self.attack_state = False
        self.attack_damage = 5
        self.event_que = []
        self.cur_state = Idle_State
        self.cur_state.enter(self, None)
        self.selected = False
        self.gun_sound = load_wav('sounds/20-gauge-shotgun-gunshot.wav')
        self.gun_sound.set_volume(30)
        pass
    def gun_fire(self):
        self.gun_sound.play()
        pass

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def add_event(self, event):
        self.event_que.insert(0, event)
        pass

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        pass

    def draw(self):

        self.cur_state.draw(self)
        pass

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        if (event.type, event.button) in key_event_table:
            button_event = key_event_table[(event.type, event.button)]
            global x, y
            x, y = event.x, event.y
            self.add_event(button_event)

        pass
