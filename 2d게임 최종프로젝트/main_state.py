from pico2d import *
import game_world
import game_framework
import title_state
import clear_stage
import Ending_Scene
from Double_Gun_Charcter import Double_Gun_Character
from Map import Game_Map
from zombie_female import Zombie
from Marco import Marco
from Bullet import Bullet

'''''''''
남은 구현 사항
애들 배열로 구성
리롤
위치 500,410,330,580
'''''''''

name = "MainState"

game_map = None
double_gun_characters = None
zombies = None
double_gun_character1 = None
marcos = None
bullets = None
fire = False
game_start = False
stage_count = 0
Money = 20
stage_monster_num = 10
character_in_re_roll_double_number = 5
character_in_re_roll_marco = 0
character_box = [235, 320, 410, 500, 580]


def enter():
    global game_map, double_gun_characters, zombies, marcos, bullets

    marcos = [Marco() for i in range(character_in_re_roll_marco)]
    bullets = [Bullet()]
    game_map = Game_Map()
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
    global double_gun_characters, marcos
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(title_state)
        else:
            for double_gun_character in double_gun_characters:
                double_gun_character.handle_event(event)
            for marco in marcos:
                marco.handle_event(event)
            game_map.handle_event(event)

    pass


def update():
    global game_map, double_gun_characters, zombies, marcos, bullets, fire, game_start, stage_monster_num
    if stage_count == 2:
        game_framework.change_state(Ending_Scene)

    if stage_monster_num <= 0:
        game_start = False
        stage_monster_num = 10
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

    for zombie in zombies:
        for marco in marcos:
            if collide(zombie, marco):
                zombie.attack_state = True
                # 총알이랑 판정
            if marco.attack_state:
                for bullet in bullets:
                    if collide(zombie, bullet):
                        zombie.hp -= bullet.damage
                        bullets.remove(bullet)
                        game_world.remove_object(bullet)

                if marco.attack_state and marco.attack_frame == 2:
                    bullets.append(Bullet())
                    for bullet in bullets:
                        bullet.x = marco.x
                        bullet.y = marco.y
                        game_world.add_objects(bullets, 1)

                for bullet in bullets:
                    if bullet.x >= 800:
                        bullets.remove(bullet)
                        game_world.remove_object(bullet)

            if zombie.hp and zombie.y - 50 < marco.y < zombie.y + 50 and game_start > 0:
                marco.attack_state = True
            if zombie.hp < 0:
                marco.attack_state = False

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
