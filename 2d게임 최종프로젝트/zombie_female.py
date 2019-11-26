import random
import math
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import main_state

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

animation_names = ['Attack', 'Dead', 'Idle', 'Walk']


def load_images():
    if Zombie.images is None:
        Zombie.images = {}
        for name in animation_names:
            Zombie.images[name] = [load_image("image/zombiefiles/female/" + name + " (%d)" % i + ".png") for i in
                                   range(1, 11)]


class Zombie:
    images = None

    def __init__(self):
        positions = [(700, 400), (-100, 400)]
        self.patrol_positions = []
        for p in positions:
            self.patrol_positions.append((p[0], 600 - p[1]))  # convert for origin at bottom, left
            self.patrol_order = 1
            self.target_x, self.target_y = None, None
            self.x, self.y = self.patrol_positions[0]
            self.attack_state = False

        load_images()
        self.hp = 100
        self.dir = 0
        self.speed = 0
        self.frame = 0
        self.build_behavior_tree()

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to_destination(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        return BehaviorTree.SUCCESS
        pass

    def attack(self):
        if self.hp > 0:
            self.dir = 3.14
            self.speed = 0

            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def dead(self):
        self.x = 900
        self.y = 600 - 400 - 1
        self.attack_state = False
        self.hp = 100
        return BehaviorTree.SUCCESS
        pass

    def get_next_position(self):
        self.target_x, self.target_y = self.patrol_positions[self.patrol_order % len(self.patrol_positions)]
        self.patrol_order += 1
        self.dir = math.atan2(self.target_y - self.y, self.target_x - self.x)
        return BehaviorTree.SUCCESS
        pass

    def move_to_target(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        distance = (self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2
        if self.attack_state:
            self.dir = math.atan2(self.target_y - self.y, self.target_x - self.x)
            return BehaviorTree.FAIL

        if distance < PIXEL_PER_METER ** 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

        pass

    def build_behavior_tree(self):
        # move_attack_node 만들기 move 우선 어택 fail dead 만들기
        get_next_position_node = LeafNode("Get Next Position", self.get_next_position)
        move_to_target_node = LeafNode("Move to Target", self.move_to_target)
        move_node = SequenceNode("Move")
        move_node.add_children(get_next_position_node, move_to_target_node)
        attack_node = LeafNode("Attack", self.attack)
        dead_node = LeafNode("Dead",self.dead)
        move_attack_node = SelectorNode("MoveAttack")
        move_attack_node.add_children(move_node, attack_node,dead_node)
        self.bt = BehaviorTree(move_attack_node)
        pass

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.bt.run()
        pass

    def draw(self):
        if math.cos(self.dir) < 0:
            if self.speed != 0 and self.attack_state == False and self.hp>0:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
            elif self.attack_state:
                Zombie.images['Attack'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            if self.speed != 0 and self.attack_state == False and self.hp>0:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 100, 100)
            elif self.attack_state:
                Zombie.images['Attack'][int(self.frame)].draw(self.x, self.y, 100, 100)

    def handle_event(self, event):
        pass
