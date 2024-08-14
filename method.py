import copy
import heapq
import random
from collections import deque
from heapq import heappop, heappush

from map import Point
import map

directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, -1), (0, 0, 1)]  # 右、左、前、后、下、上


def has_valid_move(head, map_data):
    valid_directions = []

    for dx, dy, dz in directions:
        new_head_x = head.x + dx
        new_head_y = head.y + dy
        new_head_z = head.z + dz

        # 检查新位置是否在地图边界内
        if 0 <= new_head_x < len(map_data) and 0 <= new_head_y < len(map_data[0]) and 0 <= new_head_z < len(
                map_data[0][0]):
            # 检查新位置的map_data值是否<0
            if map_data[new_head_x][new_head_y][new_head_z] >= 0:
                valid_directions.append((dx, dy, dz))

    return valid_directions


def heuristic(a, b):
    # 访问Point对象的x, y, z属性来计算曼哈顿距离
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def astar(map_data, start, goal):
    close_set = set()
    came_from = {start: None}  # 初始化时预设从start到自身的路径
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for dx, dy, dz in directions:
            neighbor = Point(current.x + dx, current.y + dy, current.z + dz)
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor.x < len(map_data) and 0 <= neighbor.y < len(map_data[0]) and 0 <= neighbor.z < len(
                    map_data[0][0]):
                if map_data[neighbor.x][neighbor.y][neighbor.z] >= 0:  # 确保邻居不是障碍
                    if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                        continue

                    if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_g_score
                        fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return None


def find_closest_target(head, map_data):
    if map_data[head.x][head.y][head.z] > 0:
        return head
    queue = deque([head])  # 使用deque作为队列，并使用Point对象
    visited = {head}

    while queue:
        current = queue.popleft()  # 从队列中取出第一个元素
        for dx, dy, dz in directions:
            neighbor = Point(current.x + dx, current.y + dy, current.z + dz)
            if 0 <= neighbor.x < len(map_data) and 0 <= neighbor.y < len(map_data[0]) and 0 <= neighbor.z < len(
                    map_data[0][0]) and neighbor not in visited:
                if map_data[neighbor.x][neighbor.y][neighbor.z] > 0:  # 如果找到一个目标点
                    return neighbor
                visited.add(neighbor)  # 标记为已访问
                queue.append(neighbor)  # 将新的位置添加到队列中

    return None  # 如果没有找到目标点


def bfs_count_connected_regions(map_data, start):
    """
    使用广度优先搜索计算连通的可通行区域的格子数。
    """
    visited = {start}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if map_data[current.x][current.y][current.z] >= 0:
            for dx, dy, dz in directions:
                neighbor = Point(current.x + dx, current.y + dy, current.z + dz)
                if 0 <= neighbor.x < len(map_data) and 0 <= neighbor.y < len(map_data[0]) and 0 <= neighbor.z < len(
                        map_data[0][0]) and \
                        map_data[neighbor.x][neighbor.y][neighbor.z] >= 0 and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
    return len(visited)


def is_opposite(dir1, dir2):
    """判断两个方向是否相对"""
    return all(abs(d1 + d2) == 1 for d1, d2 in zip(dir1, dir2))


def is_quality_move(head, map_data):
    temp_map = copy.deepcopy(map_data)  # 创建地图的深拷贝
    quality_directions = {}
    valid_directions = has_valid_move(head, temp_map)
    total_passable_area = sum(1 for layer in temp_map for row in layer for cell in row if cell >= 0) - 1

    for dx, dy, dz in valid_directions:
        new_head_x = head.x + dx
        new_head_y = head.y + dy
        new_head_z = head.z + dz
        temp_map[new_head_x][new_head_y][new_head_z] = -3  # 标记蛇头位置为不可通行
        new_head = Point(new_head_x, new_head_y, new_head_z)
        next_valid_directions = has_valid_move(new_head, temp_map)

        max_ratio_for_new_head = 0

        penalty = 0
        next_valid_directions_set = set(next_valid_directions)
        for dir1 in directions:
            for dir2 in directions:
                if is_opposite(dir1,
                               dir2) and dir1 not in next_valid_directions_set and dir2 not in next_valid_directions_set:
                    penalty -= 0.1

        for ndx, ndy, ndz in next_valid_directions:
            next_new_head = Point(new_head_x + ndx, new_head_y + ndy, new_head_z + ndz)
            next_new_head_passable_area = bfs_count_connected_regions(temp_map, next_new_head)

            ratio = next_new_head_passable_area / total_passable_area if total_passable_area > 0 else 0
            adjusted_ratio = ratio + penalty
            max_ratio_for_new_head = max(max_ratio_for_new_head, adjusted_ratio)

        # 保存方向及其最大质量值
        quality_directions[(dx, dy, dz)] = max_ratio_for_new_head

        # 恢复地图状态
        temp_map[new_head_x][new_head_y][new_head_z] = 0  # 恢复蛇头位置为可通行

    # 按照比例从小到大排序方向
    sorted_directions = sorted(quality_directions.items(), key=lambda item: item[1], reverse=True)

    return sorted_directions


def find_shortest_path(map_data, start, quality_directions):
    """
    使用广度优先搜索找到从start位置出发，通过quality_directions中给定的方向
    到达任意目标点的最短路径长度。目标点是map_data上值大于0的格子。
    返回一个列表，元素是方向，按照路径长度从小到大排序。
    """
    path_lengths = {}
    for dx, dy, dz in quality_directions:
        distance = None
        new_head = Point(start.x + dx, start.y + dy, start.z + dz)
        closest_target = find_closest_target(new_head, map_data)
        if closest_target:
            path = astar(map_data, new_head, closest_target)
            if path:
                distance = len(path)
        if distance is not None:
            path_lengths[(dx, dy, dz)] = distance

    # 按照路径长度distance排序方向
    sorted_paths = sorted(path_lengths.items(), key=lambda item: item[1])

    return sorted_paths


def decide_simple_direction(head, map_data):
    valid = has_valid_move(head, map_data)
    if valid:
        dx, dy, dz = random.choice(valid)
        return dx, dy, dz
    return 0, 0, 1


def decide_medium_direction(head, map_data):
    closest_target = find_closest_target(head, map_data)
    path = None
    if closest_target:
        path = astar(map_data, head, closest_target)
    if path:
        next_point = path[1]
        dx, dy, dz = next_point.x - head.x, next_point.y - head.y, next_point.z - head.z
        return dx, dy, dz

    valid = has_valid_move(head, map_data)
    if valid:
        dx, dy, dz = random.choice(valid)
        return dx, dy, dz

    return 0, 0, 1  # Default move


def decide_advanced_direction(head, map_data, rate):
    quality = is_quality_move(head, map_data)

    if quality:
        quality_paths = [dir for dir, _ in quality]
        # 寻找最短路径
        shortest_paths = find_shortest_path(map_data, head, quality_paths)

        # 如果shortest_paths不为空，检查其中是否有在quality中排在rate前的元素
        if shortest_paths:
            # 仅保留quality中比例>=0.8的项
            quality_filtered = [dir for dir, val in quality if val >= rate]

            path_order = {path: index for index, (path, _) in enumerate(shortest_paths)}

            # 对quality进行排序，先按比例降序排序，然后在比例相同的情况下，按照shortest_paths中的顺序排序
            quality = sorted(quality, key=lambda x: (-x[1], path_order.get(x[0], float('inf'))))

            # 对于最短路，如果它的质量评分高
            for path in shortest_paths:
                if path[0] in quality_filtered:
                    return path[0]

        # 如果shortest_paths为空或shortest_paths中没有高质量路径，取quality_copy中的第一个元素
        return quality[0][0]

    # 如果quality_copy为空，返回默认方向
    return 0, 0, 1


def decide_direction(head, AI_level, map_data):
    if AI_level == 1:
        return decide_simple_direction(head, map_data)
    elif AI_level == 2:
        return decide_medium_direction(head, map_data)
    elif AI_level == 3:
        return decide_advanced_direction(head, map_data, 0.6)
    else:
        raise ValueError("Invalid AI_level provided.")
