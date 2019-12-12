from pico2d import *
import game_world
import game_framework
import title_state
import clear_stage
import Ending_Scene
import game_over_state
from Double_Gun_Charcter import Double_Gun_Character
from Map import Game_Map
from zombie_female import Zombie
from Marco import Marco
from Bullet import Bullet
import random

name = "MainState"

game_map = None
double_gun_characters = None
zombies = None
double_gun_character1 = None
marcos = None
bullets = None
fire = False
game_start = False
stage_count = 1
Money = 20
stage_monster_num = 10 * stage_count
character_in_re_roll_double_number = 5
character_in_re_roll_marco = 0
character_box = [235, 320, 410, 500, 580]


def enter():
    global game_map, double_gun_characters, zombies, marcos, bullets

    bullets = [Bullet()]
    game_map = Game_Map()
    marcos = [Marco() for i in range(character_in_re_roll_marco)]
    double_gun_characters = [Double_Gun_Character() for i in range(character_in_re_roll_double_number)]
    zombies = [Zombie() for i in range(stage_monster_num)]
    game_world.add_object(game_map, 0)
    game_world.add_objects(zombies, 1)
    game_world.add_objects(double_gun_characters, 1)
    game_world.add_objects(marcos, 1)
    pass


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def exit():
    game_world.clear()
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global double_gun_characters, marcos, game_start, character_in_re_roll_double_number, character_in_re_roll_marco, character_box, Money
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(title_state)

        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            for double_gun_character in double_gun_characters:
                double_gun_character.handle_event(event)
            for marco in marcos:
                marco.handle_event(event)
            x = event.x
            y = event.y
            # x640 y100
            if 638 < x < 800 and 0 < 600 - y - 1 < 200:
                game_start = True
            elif 80 < x < 150 and 40 < 600 - y - 1 < 130:
                # re-roll
                num_double =0
                for double_gun_character in double_gun_characters:
                    if double_gun_character.y <= 150:
                        num_double += 1

                Money -= 1
                while num_double > 0:
                    for double_gun_character in double_gun_characters:
                        if double_gun_character.y <= 150:
                            game_world.remove_object(double_gun_character)
                            double_gun_characters.remove(double_gun_character)
                            num_double -= 1
                num_marco =0
                for marco in marcos:
                    if marco.y <= 150:
                        num_marco +=1
                while num_marco>0:
                    for marco in marcos:
                        if marco.y <= 150:
                            game_world.remove_object(marco)
                            marcos.remove(marco)
                            num_marco -= 1
                character_count = random.randint(1, 5)
                character_in_re_roll_double_number = character_count
                character_in_re_roll_marco = 5 - character_in_re_roll_double_number
                character_box = [320, 235, 580, 500, 410]
                marcos += [Marco() for i in range(character_in_re_roll_marco)]
                double_gun_characters += [Double_Gun_Character() for i in range(character_in_re_roll_double_number)]
                game_world.add_objects(double_gun_characters, 1)
                game_world.add_objects(marcos, 1)
    pass


def update():
    global game_map, double_gun_characters, zombies, marcos, bullets, fire, game_start, stage_monster_num
    for zombie in zombies:
        if zombie.x <= 0:
            game_framework.change_state(game_over_state)
    if stage_count == 3:
        game_framework.change_state(Ending_Scene)

    if stage_monster_num <= 0:
        game_start = False
        stage_monster_num = 10 * (stage_count+1)
        zombies = [Zombie() for i in range(stage_monster_num)]
        game_world.add_objects(zombies, 1)
        game_framework.push_state(clear_stage)

    for zombie in zombies:
        for double_gun_character in double_gun_characters:
            if collide(zombie, double_gun_character):
                zombie.attack_state = True
                double_gun_character.attack_state = True
                zombie.hp -= double_gun_character.attack_damage
                if double_gun_character.hp > 0:
                    double_gun_character.hp -= zombie.damage
                else:
                    zombie.attack_state = False
                    double_gun_character.attack_damage = 0
                    game_world.remove_object(double_gun_character)

            if zombie.hp <= 0:
                double_gun_character.attack_state = False

    for double_gun_character in double_gun_characters:
        if double_gun_character.hp <= 0:
            double_gun_characters.remove(double_gun_character)
            for zombie in zombies:
                zombie.attack_state = False

    for zombie in zombies:
        for marco in marcos:
            if collide(zombie, marco):
                zombie.attack_state = True
                marco.hp -= zombie.damage
                if marco.hp <= 0:
                    zombie.attack_state = False
                    game_world.remove_object(marco)
                # 총알이랑 판정
            if marco.attack_state:
                for bullet in bullets:
                    if collide(zombie, bullet):
                        zombie.hp -= bullet.damage
                        bullets.remove(bullet)
                        game_world.remove_object(bullet)

                if marco.attack_state and marco.attack_frame == 3:
                    bullets.append(Bullet())
                    for bullet in bullets:
                        bullet.x = marco.x
                        bullet.y = marco.y
                        game_world.add_objects(bullets, 1)

                for bullet in bullets:
                    if bullet.x >= 800:
                        bullets.remove(bullet)
                        game_world.remove_object(bullet)

            if zombie.hp > 0 and zombie.y - 50 < marco.y < zombie.y + 50 and game_start > 0 \
                    and zombie.x < 800:
                marco.attack_state = True
            if zombie.hp <= 0:
                for marco in marcos:
                    marco.attack_state = False

    for marco in marcos:
        if marco.hp <= 0:
            marcos.remove(marco)
            for zombie in zombies:
                zombie.attack_state = False

    for game_object in game_world.all_objects():
        game_object.update()
    delay(0.1)

    pass


def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
    pass
