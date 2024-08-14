# Snake3D
[中文](#Chinese)



3-Dimension snake game implemented using different strategies.



### Requirements



```
matplotlib==3.8.0
numpy==1.23.5
```



### How to start?



1. Copy the project.

2. Install requirements.

3. Run:

   ```python
   python main.py
   ```

   or

   ```python
   python main.py --AI_level 3 --num_apples 2 --score_apples 100 --interval 50 --barriers 3 3 2 2 1 3 --map_size 5 5 5 --initial_snake 1 1 0 0 1 0 0 0 0
   
   ```

   

### Parser

```python
usage: main.py [-h] [--AI_level AI_LEVEL] [--num_apples NUM_APPLES] [--score_apples SCORE_APPLES] [--interval INTERVAL] [--barriers [BARRIERS ...]]
               [--map_size MAP_SIZE MAP_SIZE MAP_SIZE] [--initial_snake [INITIAL_SNAKE ...]]
```

```
optional arguments:
  -h, --help            
  						Show this help message and exit
  --AI_level AI_LEVEL   
  						Computer level: 1-3
  --num_apples NUM_APPLES
                        Number of apples
  --score_apples SCORE_APPLES
                        Score per apple: >2
  --interval INTERVAL   
  						Animation frame rate control
  --barriers [BARRIERS ...]
                        Barrier positions (flat list), e.g., 3 3 2 2 1 3
  --map_size MAP_SIZE MAP_SIZE MAP_SIZE
                        Map size (length x width x height), must specify three values 						  greater than or equal to 2
  --initial_snake [INITIAL_SNAKE ...]
                        Initial snake position (flat list), e.g., 1 1 0 0 1 0 0 0 0
```





# 3维贪吃蛇 {#Chinese}



由不同策略实现的三维贪吃蛇游戏。



### 依赖



```
matplotlib==3.8.0
numpy==1.23.5
```



### 如何使用?



1. 复制项目。

2. 安装依赖。

3. 运行:

   ```python
   python main.py
   ```

   或者

   ```python
   python main.py --AI_level 3 --num_apples 2 --score_apples 100 --interval 50 --barriers 3 3 2 2 1 3 --map_size 5 5 5 --initial_snake 1 1 0 0 1 0 0 0 0
   
   ```

   

### 参数

```python
usage: main.py [-h] [--AI_level AI_LEVEL] [--num_apples NUM_APPLES] [--score_apples SCORE_APPLES] [--interval INTERVAL] [--barriers [BARRIERS ...]]
               [--map_size MAP_SIZE MAP_SIZE MAP_SIZE] [--initial_snake [INITIAL_SNAKE ...]]
```

```
游戏配置参数:
  -h, --help            
  						帮助信息
  --AI_level AI_LEVEL   
  						电脑等级：1-3
  --num_apples NUM_APPLES
                        苹果数量
  --score_apples SCORE_APPLES
                        苹果分值：>2
  --interval INTERVAL   
  						控制动画帧率，50为0.2s一帧
  --barriers [BARRIERS ...]
                        障碍位置（扁平列表），形如3 3 2 2 1 3
  --map_size MAP_SIZE MAP_SIZE MAP_SIZE
                        地图大小（长x宽x高），必须指定三个大于等于2的值
  --initial_snake [INITIAL_SNAKE ...]
                        蛇的初始位置（扁平列表），形如1 1 0 0 1 0 0 0 0
```

