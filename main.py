import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap, BoundaryNorm
import map
from map import Point
import model

# 定义颜色映射
colors_rgba = [
    (1.0, 1.0, 0.0, 0.5),  # 黄色，透明度50%
    (0.0, 0.5, 0.0, 0.5),  # 绿色，透明度50%
    (0.5, 0.5, 0.5, 0.5),  # 灰色，透明度50%
    (0.0, 0.0, 0.0, 0.5),  # 黑色，透明度50%
    (1.0, 0.0, 0.0, 0.5)  # 红色，透明度50%
]

# 创建颜色映射
cmap = ListedColormap(colors_rgba)
bounds = [-3.5, -2.5, -1.5, -0.5, 0.5, 1000.5]
norm = BoundaryNorm(bounds, cmap.N)


# 定义生成器函数
def infinite_frames():
    i = 0

    while True:
        if not snake.move():
            break
        yield i
        i += 1
    yield None  # 这里的 None 或其他值用于通知动画结束


def update(frame):
    if frame is None:  # 检查frame是否为None
        anim.event_source.stop()  # 停止动画
        return

    # 更新MAP_DATA
    for i in range(len(config.MAP_DATA)):
        for j in range(len(config.MAP_DATA[0])):
            for k in range(len(config.MAP_DATA[0][0])):
                if config.MAP_DATA[i][j][k] > 0:
                    config.MAP_DATA[i][j][k] -= 1
                    if config.MAP_DATA[i][j][k] == 0:
                        apples.del_and_gen(Point(i, j, k))

    draw_map()

    return [ax]  # 返回ax以触发重绘


def draw_map():
    # 清除旧的voxels
    ax.clear()

    # 如果config.MAP_DATA是一个列表，你需要将其转换成numpy数组
    map_data = np.array(config.MAP_DATA)

    face_colors = cmap(norm(map_data))
    ax.voxels(map_data != 0, facecolors=face_colors, edgecolor='none')

    # 设置坐标轴的范围和标签
    ax.set_xlim(0, map_data.shape[0])
    ax.set_ylim(0, map_data.shape[1])
    ax.set_zlim(0, map_data.shape[2])
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title(f"Score: {snake.score}")

    # 设置3D图像的长宽比
    ax.set_box_aspect(map_data.shape)


if __name__ == '__main__':
    config = map.set_parser()

    # 创建一个figure和3D轴
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    apples = model.Apple(config)
    snake = model.Snake(apples, config)

    # 创建动画
    draw_map()
    anim = FuncAnimation(fig, update, frames=infinite_frames, interval=config.INTERVAL)

    plt.show(block=True)
