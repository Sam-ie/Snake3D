import random

import method
from map import Point
import map


class Apple:
    def __init__(self, config):
        self.map_data = config.MAP_DATA
        self.score_apples = config.score_apples
        self.apples = []
        for _ in range(config.num_apples):
            while True:
                x = random.randint(0, len(self.map_data) - 1)
                y = random.randint(0, len(self.map_data[0]) - 1)
                z = random.randint(0, len(self.map_data[0][0]) - 1)
                # Check if the position is empty (value is 0)
                if self.map_data[x][y][z] == 0:
                    self.map_data[x][y][z] = self.score_apples  # Set the value to 1000 for the apple
                    self.apples.append(Point(x, y, z))
                    break

    def del_and_gen(self, point):
        # 删除指定位置的苹果
        self.apples = [apple for apple in self.apples if not (apple.x == point.x and apple.y == point.y and apple.z == point.z)]

        # 查找map.MAP_DATA中值为0的随机位置
        empty_spots = [(x, y, z) for x in range(len(self.map_data)) for y in range(len(self.map_data[x])) for z in
                       range(len(self.map_data[x][y])) if self.map_data[x][y][z] == 0]

        if empty_spots:
            new_spot = random.choice(empty_spots)
            self.map_data[new_spot[0]][new_spot[1]][new_spot[2]] = self.score_apples  # 更新地图数据

            # 生成新苹果
            self.apples.append(Point(new_spot[0], new_spot[1], new_spot[2]))


class Snake:
    def __init__(self, apples, config):
        # 使用INITIAL_SNAKE_BODY的第一个元素作为头部，其余作为身体
        self.head = config.INITIAL_SNAKE[0]
        self.body = [pos for pos in config.INITIAL_SNAKE[1:]]
        self.score = 0
        self.apples = apples

        self.map_data = config.MAP_DATA
        self.AI_level = config.AI_level

    def eat(self, new_head):
        if self.map_data[new_head.x][new_head.y][new_head.z] > 0:
            self.score += self.map_data[new_head.x][new_head.y][new_head.z]
            self.apples.del_and_gen(new_head)
            return True
        return False

    def move(self):
        dx, dy, dz = method.decide_direction(self.head, self.AI_level, self.map_data)
        new_head = Point(self.head.x + dx, self.head.y + dy, self.head.z + dz)

        # 检查新位置是否在地图边界内和是否与自己碰撞
        if not self.is_valid_move(new_head):
            return False  # 结束动画，因为蛇撞到了障碍物或自身

        # 更新地图数据
        if not self.eat(new_head):
            self.map_data[self.body[-1].x][self.body[-1].y][self.body[-1].z] = 0  # 清除身体位置
            self.body.pop()

        self.body.insert(0, Point(self.head.x, self.head.y, self.head.z))  # 将旧头插入到body前
        self.map_data[self.head.x][self.head.y][self.head.z] = -2  # 更新新的身体位置
        self.head = new_head
        self.map_data[new_head.x][new_head.y][new_head.z] = -3  # 更新新的头部位置

        return True  # 返回True以继续动画

    def is_valid_move(self, new_head):
        # 检查新位置是否在地图边界内
        if not (0 <= new_head.x < len(self.map_data) and 0 <= new_head.y < len(self.map_data[0]) and 0 <= new_head.z < len(self.map_data[0][0])):
            return False

        # 检查新位置是否与地图上的障碍物和自身碰撞
        if self.map_data[new_head.x][new_head.y][new_head.z] < 0:
            return False

        return True
