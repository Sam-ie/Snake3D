import random
from collections import deque
from heapq import heappop, heappush

from map import Point
import map

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # 右、左、下、上


def has_valid_move(head):
    valid_directions = []

    for dx, dy in directions:
        new_head_x = head.x + dx
        new_head_y = head.y + dy

        # 检查新位置是否在地图边界内
        if 0 <= new_head_x < len(map.MAP_DATA[0]) and 0 <= new_head_y < len(map.MAP_DATA):
            # 检查新位置的map.MAP_DATA值是否<0
            if map.MAP_DATA[new_head_x][new_head_y] >= 0:
                valid_directions.append((dx, dy))

    return valid_directions


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(map_data, start, goal):
    if map_data[goal[0]][goal[1]] > 0:  # 确保目标点的值大于0
        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: heuristic(start, goal)}
        oheap = []

        heappush(oheap, (fscore[start], start))

        while oheap:
            current = heappop(oheap)[1]
            if current == goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data

            close_set.add(current)
            for dx, dy in directions:
                neighbor = current[0] + dx, current[1] + dy
                tentative_g_score = gscore[current] + heuristic(current, neighbor)
                if 0 <= neighbor[0] < len(map_data[0]):
                    if 0 <= neighbor[1] < len(map_data):
                        if map_data[neighbor[0]][neighbor[1]] >= 0:  # 确保邻居不是障碍
                            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                                continue

                            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                                came_from[neighbor] = current
                                gscore[neighbor] = tentative_g_score
                                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                                heappush(oheap, (fscore[neighbor], neighbor))

    return None


def find_closest_target(head, map_data):
    queue = deque([(head.x, head.y)])  # 使用deque作为队列
    visited = {(head.x, head.y)}

    while queue:
        x, y = queue.popleft()  # 从队列中取出第一个元素
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data) and (nx, ny) not in visited:
                if map_data[nx][ny] > 0:  # 如果找到一个目标点
                    return nx, ny
                visited.add((nx, ny))  # 标记为已访问
                queue.append((nx, ny))  # 将新的位置添加到队列中

    return None  # 如果没有找到目标点


def bfs_count_connected_regions(map_data, start):
    """
    使用广度优先搜索计算连通的可通行区域的格子数。
    """
    visited = {(start.x, start.y)}
    queue = deque([(start.x, start.y)])

    while queue:
        cx, cy = queue.popleft()
        if map_data[cx][cy] >= 0:
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < len(map_data[0]) and 0 <= ny < len(map_data) and \
                        map_data[nx][ny] >= 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    return len(visited)


def is_quality_move(head):
    temp_map = [row[:] for row in map.MAP_DATA]  # 创建地图的深拷贝
    quality_directions = {}
    valid_directions = has_valid_move(head)
    total_passable_area = sum(1 for row in temp_map for cell in row if cell >= 0) - 1

    for dx, dy in valid_directions:
        new_head_x = head.x + dx
        new_head_y = head.y + dy
        temp_map[new_head_x][new_head_y] = -3  # 标记蛇头位置为不可通行
        new_head = Point(new_head_x, new_head_y)
        next_valid_directions = has_valid_move(new_head)

        max_ratio_for_new_head = 0

        next_valid_directions_set = set(next_valid_directions)
        # 检查是否只有两个相反方向
        if len(next_valid_directions_set) == 2 and any(
                (-dx, -dy) in next_valid_directions_set for dx, dy in next_valid_directions_set):
            # 只有两个相反方向，计算比例时将应用-0.1的惩罚
            penalty = -0.1
        else:
            penalty = 0

        for ndx, ndy in next_valid_directions:
            next_new_head = Point(new_head_x + ndx, new_head_y + ndy)
            next_new_head_passable_area = bfs_count_connected_regions(temp_map, next_new_head)

            ratio = next_new_head_passable_area / total_passable_area if total_passable_area > 0 else 0
            adjusted_ratio = ratio + penalty
            max_ratio_for_new_head = max(max_ratio_for_new_head, adjusted_ratio)

        # 保存方向及其最大质量值
        quality_directions[(dx, dy)] = max_ratio_for_new_head

        # 恢复地图状态
        temp_map[new_head_x][new_head_y] = 0  # 恢复蛇头位置为可通行

    # 按照比例从小到大排序方向
    sorted_directions = sorted(quality_directions.items(), key=lambda item: item[1], reverse=True)

    return sorted_directions


def bfs(map_data, start):
    """
    使用广度优先搜索从start位置出发到达最近的目标点（值大于0的格子）的最短距离。
    返回距离，如果找不到目标则返回None。
    """
    queue = deque([start])
    visited = set([start])
    distance = 0

    while queue:
        for _ in range(len(queue)):
            current = queue.popleft()
            if map_data[current.x][current.y] > 0:
                return distance

            for dx, dy in directions:
                next_x, next_y = current.x + dx, current.y + dy
                if (0 <= next_x < len(map_data) and 0 <= next_y < len(map_data[0]) and (next_x, next_y) not in visited
                        and map_data[next_x][next_y] >= 0):
                    queue.append(Point(next_x, next_y))
                    visited.add((next_x, next_y))
        distance += 1
    return None


def bfs_find_shortest_path(map_data, start, quality_directions):
    """
    使用广度优先搜索找到从start位置出发，通过quality_directions中给定的方向
    到达任意目标点的最短路径长度。目标点是map_data上值大于0的格子。
    返回一个列表，元素是方向，按照路径长度从小到大排序。
    """
    path_lengths = {}
    for dx, dy in quality_directions:
        new_start = Point(start.x + dx, start.y + dy)
        distance = bfs(map_data, new_start)
        if distance is not None:
            path_lengths[(dx, dy)] = distance

    # 按照路径长度distance排序方向
    sorted_paths = sorted(path_lengths.items(), key=lambda item: item[1])

    return sorted_paths


def decide_simple_direction(head):
    valid = has_valid_move(head)
    if valid:
        dx, dy = random.choice(valid)
        return dx, dy
    return 0, 1


def decide_medium_direction(head):
    closest_target = find_closest_target(head, map.MAP_DATA)
    path = None
    if closest_target:
        path = astar(map.MAP_DATA, (head.x, head.y), closest_target)
    if path:
        next_point = path[-1]
        dx, dy = next_point[0] - head.x, next_point[1] - head.y
        return dx, dy

    valid = has_valid_move(head)
    if valid:
        dx, dy = random.choice(valid)
        return dx, dy

    return 0, 1  # Default move


def decide_advanced_direction(head, rate):
    quality = is_quality_move(head)

    if quality:
        quality_paths = [dir for dir, _ in quality]
        # 使用BFS寻找最短路径
        shortest_paths = bfs_find_shortest_path(map.MAP_DATA, head, quality_paths)

        # 如果shortest_paths不为空，检查其中是否有在quality中排在rate前的元素
        if shortest_paths:
            # 仅保留quality中比例>=0.8的项
            quality_filtered = [dir for dir, val in quality if val >= rate]

            path_order = {path: index for index, (path, _) in enumerate(shortest_paths)}

            # 对quality进行排序，先按比例降序排序，然后在比例相同的情况下，按照shortest_paths中的顺序排序
            quality = sorted(quality, key=lambda x: (-x[1], path_order.get(x[0], float('inf'))))

            # 找到第一个不在(0, 0)位置的元素
            for path in shortest_paths:
                if path[0] in quality_filtered:
                    return path[0]

        # 如果shortest_paths为空或shortest_paths中没有高质量路径，取quality_copy中的第一个元素
        return quality[0][0]

    # 如果quality_copy为空，返回默认方向(0, 1)
    return 0, 1


def decide_super_advanced_direction(head):
    # 可以使用深度Q网络 (Deep Q-Network, DQN)，项目见D3QN-Snake-master
    # (https://github.com/panjd123/D3QN-Snake)
    return decide_simple_direction(head)


def decide_direction(head, AI_level):
    if AI_level == 1:
        return decide_simple_direction(head)
    elif AI_level == 2:
        return decide_medium_direction(head)
    elif AI_level == 3:
        return decide_advanced_direction(head, 0.6)
    elif AI_level == 4:
        return decide_super_advanced_direction(head)
    else:
        raise ValueError("Invalid AI_level provided.")
