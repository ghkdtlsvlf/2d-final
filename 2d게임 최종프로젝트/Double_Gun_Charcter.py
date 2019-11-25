from pico2d import *
import random
import game_world
import math
import game_framework
import main_state
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode


# gun_c Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# gun_c Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


from Member_function import *

Left_Mouse_Down = False
Left_Mouse_UP, D_Pressed, Attack_Timer, Wait_Timer = range(4)

key_event_table = {
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): Left_Mouse_Down,
    (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT): Left_Mouse_UP,
    (SDL_KEYDOWN, SDLK_d): D_Pressed,
}


class Idle_State:
    @staticmethod
    def enter(double_gun_chac, event):
        if event == D_Pressed:
            x = random.randint(0, 4)
            double_gun_chac.x = 235 + 80 * x
            double_gun_chac.y = 85
        double_gun_chac.timer = 90
        pass

    @staticmethod
    def exit(double_gun_chac, event):
        pass

    @staticmethod
    def do(double_gun_chac):
        double_gun_chac.frame = (double_gun_chac.frame + 1) % 6
        double_gun_chac.timer -= 1
        if double_gun_chac.timer == 0:
            double_gun_chac.add_event(Attack_Timer)

        pass

    @staticmethod
    def draw(double_gun_chac):
        double_gun_chac.image.clip_draw(double_gun_chac.frame * 100, 0, 100, 100, double_gun_chac.x, double_gun_chac.y)
        delay(0.1)
        pass


class Attack_State:
    @staticmethod
    def enter(double_gun_chac, event):
        double_gun_chac.timer = 3000
        pass

    @staticmethod
    def exit(double_gun_chac, event):
        pass

    @staticmethod
    def do(double_gun_chac):
        double_gun_chac.frame = (double_gun_chac.frame + 1) % 6
        double_gun_chac.timer -= 1
        double_gun_chac.attack_frame = (double_gun_chac.attack_frame + 1) % 6
        if double_gun_chac.timer == 0:
            double_gun_chac.add_event(Wait_Timer)
        pass

    @staticmethod
    def draw(double_gun_chac):
        double_gun_chac.image.clip_draw(double_gun_chac.frame * 100, 200, 80, 100, double_gun_chac.x,
                                        double_gun_chac.y )
        double_gun_chac.image_attack.clip_draw(double_gun_chac.attack_frame * 130, 0, 120, 150,
                                               double_gun_chac.x + 70, double_gun_chac.y + 40)
        delay(0.2)

        pass


next_state_table = {
    Idle_State: {D_Pressed: Idle_State, Left_Mouse_UP: Idle_State, Attack_Timer: Attack_State},
    Attack_State: {Wait_Timer: Idle_State}
}


class Double_Gun_Character:

    def __init__(self):
        self.x, self.y = 230, 85
        self.image = load_image('image/Double_gun_mode.png')
        self.image_attack = load_image('image/gun_fire2.png')
        self.attack_frame = 0
        self.frame = 0
        self.timer = 0
        self.Hp = 100
        self.Mp = 0
        self.event_que = []
        self.cur_state = Idle_State
        self.cur_state.enter(self, None)
        pass

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def change_state(self, state):

        pass

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
        draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        if (event.type, event.button) in key_event_table:
            global Left_Mouse_Down
            if (event.type, event.button) == (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT):
                Left_Mouse_Down = False
            elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
                Left_Mouse_Down = True
        if event.type == SDL_MOUSEMOTION:
            if Left_Mouse_Down:
                self.x = event.x
                self.y = 600 - 1 - event.y

        pass
