from pico2d import *
import random

Left_Mouse_Down = False
Left_Mouse_UP, D_Pressed = range(2)
key_event_table = {
    (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT): Left_Mouse_Down,
    (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT): Left_Mouse_UP,
    (SDL_KEYDOWN, SDLK_d): D_Pressed,
}


class Idle_State:
    @staticmethod
    def enter(double_gun_chac, event):
        pass

    @staticmethod
    def exit(double_gun_chac, event):
        pass

    @staticmethod
    def do(double_gun_chac):
        double_gun_chac.frame = (double_gun_chac.frame + 1) % 6

        pass

    @staticmethod
    def draw(double_gun_chac):
        double_gun_chac.image.clip_draw(double_gun_chac.frame * 50, 0, 50, 50, double_gun_chac.x, double_gun_chac.y)
        delay(0.5)
        pass


class Attack_State:
    @staticmethod
    def enter(double_gun_chac, event):
        pass

    @staticmethod
    def exit(double_gun_chac, event):
        pass

    @staticmethod
    def do(double_gun_chac):
        double_gun_chac.frame = (double_gun_chac.frame + 1) % 6

        pass

    @staticmethod
    def draw(double_gun_chac):
        double_gun_chac.image.clip_draw(double_gun_chac.frame * 0, 0, 50, 50, double_gun_chac.x, double_gun_chac.y)
        pass


next_state_table = {
    Idle_State: {D_Pressed: Idle_State, Left_Mouse_UP: Idle_State},

}


class Double_Gun_Character:

    def __init__(self):
        self.x, self.y = 235, 85
        self.image = load_image('First_Double_gunCharacter.png')
        self.frame = 0
        self.timer = 0
        self.event_que = []
        self.cur_state = Idle_State
        self.cur_state.enter(self, None)
        # fill here
        pass

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
        pass

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        if (event.type, event.button) in key_event_table:
            global Left_Mouse_Down
            if (event.type,event.button) == (SDL_MOUSEBUTTONUP,SDL_BUTTON_LEFT):
                Left_Mouse_Down = False
            elif (event.type,event.button) == (SDL_MOUSEBUTTONDOWN,SDL_BUTTON_LEFT):
                Left_Mouse_Down = True
        if event.type == SDL_MOUSEMOTION:
            if Left_Mouse_Down:
                self.x = event.x
                self.y = 600 - 1 - event.y

        pass
