from pico2d import *
import random
import game_world
import math
import game_framework
import main_state
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pynput.mouse import Controller
import Bullet

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
    def enter(marco, event):
        if event == Left_Mouse_Down:
            global x, y
            # 이미 눌러진 상태면은 이동
            if marco.selected and marco.attack_state == False and main_state.Money >= 2:
                marco.x = x
                marco.y = 600 - 1 - y
                marco.selected = False
                main_state.Money -= 2
            # 캐릭터 클릭 및 취소
            else:
                if marco.x - 50 < x < marco.x + 50 and \
                        marco.y - 50 < 600 - y - 1 < marco.y + 50:
                    marco.selected = True
                else:
                    marco.selected = False
        pass

    @staticmethod
    def exit(marco, event):
        pass

    @staticmethod
    def do(marco):
        marco.frame = (marco.frame + 1) % 3
        marco.attack_frame = (marco.attack_frame + 1) % 4
        pass

    @staticmethod
    def draw(marco):
        if not marco.attack_state:
            marco.image.clip_draw(marco.frame * 100, 200, 100, 100, marco.x, marco.y)
            if marco.y >= 160:
                marco.image_hp.clip_draw(0, 0, marco.hp, 11, marco.x - 13, marco.y - 50)
            if marco.selected:
                draw_rectangle(*marco.get_bb())
        else:
            marco.image.clip_draw(marco.attack_frame * 100, 0, 100, 100, marco.x, marco.y + 5)
            marco.image_hp.clip_draw(0, 0, marco.hp, 11, marco.x - 13, marco.y - 50)

        pass


next_state_table = {
    Idle_State: {Left_Mouse_UP: Idle_State, Left_Mouse_Down: Idle_State},
}


class Marco:
    bullet = None
    image = None
    image_hp = None

    def __init__(self):
        self.position = random.randint(5)
        self.y = 85
        if Marco.image == None:
            Marco.image = load_image('image/marco.png')
            Marco.image_hp = load_image('image/hp.png')
        if self.position == 5:
            self.x = 580
        elif self.position == 4:
            self.x = 500
        elif self.position == 3:
            self.x = 410
        elif self.position == 2:
            self.x = 320
        elif self.position == 1:
            self.x = 235

        self.attack_frame = 0
        self.frame = 0
        self.hp = 100
        self.mp = 0
        self.damage = 5
        self.attack_state = False
        self.event_que = []
        self.cur_state = Idle_State
        self.cur_state.enter(self, None)
        self.selected = False
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
