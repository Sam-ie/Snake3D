import locale
from argparse import ArgumentParser
import sys

# 输出信息的中英法日对照表
messages = {
    'lang': {
        'en': 'Game configuration parameters',
        'zh': '游戏配置参数',
        'fr': 'Paramètres de configuration du jeu',
        'ja': 'ゲームの設定パラメータ'
    },
    'AI_level': {
        'en': 'Computer level: 1-3',
        'zh': '电脑等级：1-3',
        'fr': 'Niveau de l\'ordinateur : 1-3',
        'ja': 'コンピュータレベル：1-3'
    },
    'num_apples': {
        'en': 'Number of apples',
        'zh': '苹果数量',
        'fr': 'Nombre de pommes',
        'ja': 'りんごの数'
    },
    'score_apples': {
        'en': 'Score per apple: >2',
        'zh': '苹果分值：>2',
        'fr': 'Points par pomme : >2',
        'ja': '1つのりんごあたりのスコア：>2'
    },
    'interval': {
        'en': 'Animation frame rate control',
        'zh': '控制动画帧率',
        'fr': 'Contrôle du taux d\'images par seconde de l\'animation',
        'ja': 'アニメーションのフレームレート制御'
    },
    'barriers': {
        'en': 'Barrier positions (flat list), e.g., 3 3 2 2 1 3',
        'zh': '障碍位置（扁平列表），形如3 3 2 2 1 3',
        'fr': 'Positions des barrières (liste aplatie), par exemple, 3 3 2 2 1 3',
        'ja': '障害物の位置（フラットリスト）、例えば3 3 2 2 1 3'
    },
    'map_size': {
        'en': 'Map size (length x width x height), must specify three values greater than or equal to 2',
        'zh': '地图大小（长x宽x高），必须指定三个大于等于2的值',
        'fr': 'Taille de la carte (longueur x largeur x hauteur), vous devez spécifier trois valeurs supérieures ou égales à 2',
        'ja': 'マップサイズ（長さ×幅×高さ）、2以上で3つの値を指定する必要があります'
    },
    'initial_snake': {
        'en': 'Initial snake position (flat list), e.g., 1 1 0 0 1 0 0 0 0',
        'zh': '蛇的初始位置（扁平列表），形如1 1 0 0 1 0 0 0 0',
        'fr': 'Position initiale du serpent (liste aplatie), par exemple, 1 1 0 0 1 0 0 0 0',
        'ja': '初期のヘビの位置（フラットリスト）、例えば1 1 0 0 1 0 0 0 0'
    },
    'map_size_error': {
        'en': "Error: Map dimensions must contain three values greater than or equal to 2.",
        'zh': "错误：地图尺寸必须包含三个大于等于2的值。",
        'fr': "Erreur : Les dimensions de la carte doivent contenir trois valeurs supérieures ou égales à 2.",
        'ja': "エラー：マップの寸法は2以上の3つの値を含む必要があります。"
    },
    'list_length_error': {
        'en': "Error: The number of provided {name} numbers is not a multiple of 3.",
        'zh': "错误：提供的 {name} 数字数量不是3的倍数。",
        'fr': "Erreur : Le nombre de chiffres fournis pour le {name} n’est pas un multiple de 3.",
        'ja': "エラー：提供された{name}の数値の数は3の倍数ではありません。"
    },
    'out_of_bounds_error': {
        'en': "Error: The coordinate ({x}, {y}, {z}) in {name} exceeds the map boundaries {map_size[0]}x{map_size[1]}x{map_size[2]}.",
        'zh': "错误：{name} 中的坐标 ({x}, {y}, {z}) 超出地图尺寸 {map_size[0]}x{map_size[1]}x{map_size[2]} 的边界。",
        'fr': "Erreur : La coordonnée ({x}, {y}, {z}) dans le {name} dépasse les limites de la carte {map_size[0]}x{map_size[1]}x{map_size[2]}.",
        'ja': "{name}中の座標({x}, {y}, {z})はマップの境界{map_size[0]}x{map_size[1]}x{map_size[2]}を超えています。"
    },
    'overlap_error': {
        'en': "Error: There is an overlap between barriers and the initial snake position.",
        'zh': "错误：障碍物和蛇的初始位置有重合。",
        'fr': "Erreur : Il y a une superposition entre les barrières et la position initiale du serpent.",
        'ja': "エラー：障害物と初期のヘビの位置に重複があります。"
    }
}


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False


class GameConfig:
    def __init__(self, AI_level, num_apples, score_apples, interval, barriers, map_size, initial_snake):
        if barriers is None:
            barriers = []
        if initial_snake is None:
            initial_snake = [Point(1, 1, 0), Point(0, 1, 0), Point(0, 0, 0)]

        self.AI_level = AI_level
        self.num_apples = num_apples
        self.score_apples = score_apples
        self.INTERVAL = interval
        self.barriers = barriers
        self.map_size = map_size
        self.INITIAL_SNAKE = initial_snake

        self.MAP_DATA = self.generate_map()

    def generate_map(self):
        # 创建一个全为0的三维数组
        map_data = [[[0] * self.map_size[2] for _ in range(self.map_size[1])] for _ in range(self.map_size[0])]

        # 将points中的位置设置为-1
        for barrier in self.barriers:
            if 0 <= barrier.x < self.map_size[2] and 0 <= barrier.y < self.map_size[1] and 0 <= barrier.z < \
                    self.map_size[0]:
                map_data[barrier.x][barrier.y][barrier.z] = -1

        # 将initial_snake中的位置设置为-2和-3
        head = self.INITIAL_SNAKE[0]
        map_data[head.x][head.y][head.z] = -3
        for body in self.INITIAL_SNAKE[1:]:
            map_data[body.x][body.y][body.z] = -2

        return map_data


def get_message(key, lang):
    return messages[key][lang]


def process_list(lst, name, map_size, lang):
    if lst is None or len(lst) == 0:
        return None
    if len(lst) % 3 != 0:
        print(get_message('list_length_error', lang).format(name=name))
        sys.exit(1)

    points = []
    for i in range(0, len(lst), 3):
        x, y, z = lst[i:i + 3]
        if not (0 <= x < map_size[0] and 0 <= y < map_size[1] and 0 <= z < map_size[2]):
            print(get_message('out_of_bounds_error', lang).format(x=x, y=y, z=z, name=name, map_size=map_size))
            sys.exit(1)
        points.append(Point(x, y, z))
    return points


def set_parser():
    # 根据环境变量或用户偏好设定语言
    try:
        lang, encoding = locale.getdefaultlocale()
    except:
        lang = 'en_US'
    language = lang.split('.')[0].split('_')[0]
    if language not in ('en', 'zh', 'fr', 'ja'):
        language = 'en'

    parser = ArgumentParser(description=get_message('lang', language))
    parser.add_argument('--AI_level', type=int, default=1, help=get_message('AI_level', language))
    parser.add_argument('--num_apples', type=int, default=1, help=get_message('num_apples', language))
    parser.add_argument('--score_apples', type=int, default=100, help=get_message('score_apples', language))
    parser.add_argument('--interval', type=int, default=40, help=get_message('interval', language))
    parser.add_argument('--barriers', type=int, nargs='*', help=get_message('barriers', language))
    parser.add_argument('--map_size', type=int, nargs=3, default=(7, 5, 3), help=get_message('map_size', language))
    parser.add_argument('--initial_snake', type=int, nargs='*', help=get_message('initial_snake', language))

    args = parser.parse_args()

    if not all(size > 1 for size in args.map_size):
        print(get_message('map_size_error', language))
        sys.exit(1)

    barriers = process_list(args.barriers, 'barriers', tuple(args.map_size), language)
    initial_snake = process_list(args.initial_snake, 'initial_snake', tuple(args.map_size), language)

    if barriers is not None and initial_snake is not None:
        for barrier in barriers:
            if barrier in initial_snake:
                print(get_message('overlap_error', language))
                sys.exit(1)

    # 创建GameConfig实例
    config = GameConfig(
        AI_level=args.AI_level,
        num_apples=args.num_apples,
        score_apples=args.score_apples,
        interval=args.interval,
        barriers=barriers,
        map_size=tuple(args.map_size),
        initial_snake=initial_snake
    )

    return config
