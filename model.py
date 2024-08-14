import random

import method
from map import Point
import map


class Apple:
    def __init__(self, map_data, n=1):
        self.map_data = map_data
        self.apples = []
        for _ in range(n):
            while True:
                x = random.randint(0, len(map_data[0]) - 1)
                y = random.randint(0, len(map_data) - 1)
                # Check if the position is empty (value is 0)
                if map_data[x][y] == 0:
                    map_data[y][x] = map.score_apples  # Set the value to 1000 for the apple
                    self.apples.append(Point(x, y))
                    break

    def del_and_gen(self, point):
        # 删除指定位置的苹果
        self.apples = [apple for apple in self.apples if not (apple.x == point.x and apple.y == point.y)]

        # 查找map.MAP_DATA中值为0的随机位置
        empty_spots = [(x, y) for y in range(len(map.MAP_DATA)) for x in range(len(map.MAP_DATA[y])) if
                       map.MAP_DATA[y][x] == 0]

        if empty_spots:
            new_spot = random.choice(empty_spots)
            map.MAP_DATA[new_spot[1]][new_spot[0]] = map.score_apples  # 更新地图数据

            # 生成新苹果
            self.apples.append(Point(new_spot[0], new_spot[1]))


class Snake:
    def __init__(self, head, body, apples):
        self.head = head
        self.body = body
        self.score = 0
        self.apples = apples

    def eat(self, new_head, map_data):
        if map_data[new_head.x][new_head.y] > 0:
            self.score += map_data[new_head.x][new_head.y]
            self.apples.del_and_gen(new_head)
            return True
        return False

    def move(self):
        dx, dy = method.decide_direction(self.head, map.AI_level)
        new_head = Point(self.head.x + dx, self.head.y + dy)

        # 检查新位置是否在地图边界内和是否与自己碰撞
        if not self.is_valid_move(new_head, map.MAP_DATA):
            return False  # 结束动画，因为蛇撞到了障碍物或自身

        # 更新地图数据
        if not self.eat(new_head, map.MAP_DATA):
            map.MAP_DATA[self.body[-1].x][self.body[-1].y] = 0  # 清除身体位置
            self.body.pop()

        self.body.insert(0, Point(self.head.x, self.head.y))  # 将旧头插入到body前
        map.MAP_DATA[self.head.x][self.head.y] = -2  # 更新新的身体位置
        self.head = new_head
        map.MAP_DATA[new_head.x][new_head.y] = -3  # 更新新的头部位置

        return True  # 返回True以继续动画

    def is_valid_move(self, new_head, map_data):
        # 检查新位置是否在地图边界内
        if not (0 <= new_head.x < len(map_data[0]) and 0 <= new_head.y < len(map_data)):
            return False

        # # 检查新位置是否与自己的身体碰撞
        # if (new_head.x, new_head.y) in [(point.x, point.y) for point in self.body]:
        #     return False

        # 检查新位置是否与地图上的障碍物和自身碰撞
        if map_data[new_head.x][new_head.y] < 0:
            return False

        return True
