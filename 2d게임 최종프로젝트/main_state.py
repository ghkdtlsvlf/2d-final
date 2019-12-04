from pico2d import *
import game_world
import game_framework
import title_state
import clear_stage
from Double_Gun_Charcter import Double_Gun_Character
from Map import Game_Map
from zombie_female import Zombie
from Marco import Marco
from Bullet import Bullet
'''''''''
남은 구현 사항
합성
리롤
게임 돈 표시
스테이지 남은 몹 표시
엔딩 보스몹
마르코 공격 상태
'''''''''

name = "MainState"

game_map = None
double_gun_character = None
zombie = None
double_gun_character1 = None
marco = None
bullets = None
fire = False
Money = 50
stage = 2


def enter():
    global game_map, double_gun_character, zombie, marco, bullets

    marco = Marco()
    bullets = [Bullet()]
    game_map = Game_Map()
    double_gun_character = Double_Gun_Character()
    zombie = Zombie()
    game_world.add_object(game_map, 0)
    game_world.add_object(zombie, 1)
    game_world.add_object(double_gun_character, 1)
    game_world.add_object(marco, 1)
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
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(title_state)
        else:
            double_gun_character.handle_event(event)
            marco.handle_event(event)

    pass


def update():
    global game_map, double_gun_character, zombie, marco, bullets, fire,stage
    if stage == 0:
        game_framework.push_state(clear_stage)

    if collide(zombie, double_gun_character):
        zombie.attack_state = True
        double_gun_character.attack_state = True
        zombie.hp -= double_gun_character.attack_damage
        double_gun_character.hp -= zombie.damage
    else:
        zombie.attack_state = False
        double_gun_character.attack_state = False
    if collide(zombie, marco):
        zombie.attack_state = True
    # 총알이랑 판정
    if marco.attack_state:
        for bullet in bullets:
            if collide(zombie, bullet):
                bullets.remove(bullet)
                zombie.hp -= bullet.damage
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

    if zombie.hp and zombie.y-50<marco.y < zombie.y+50 > 0:
        marco.attack_state = True

    if zombie.hp <= 0:
        double_gun_character.attack_state = False
        marco.attack_state = False

    for game_object in game_world.all_objects():
        game_object.update()

    pass


def draw():
    clear_canvas()

    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
    pass
