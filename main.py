# -*- coding:utf-8 -*-
import math
import multiprocessing
import random
import copy
import sys
from Stack import Stack
import tkinter
import threading
from functools import reduce

# 参数
'''
BETA:                       信息启发因子权重
ALPHA:                      信息素因子权重
LOCAL_EVAPORATION：         局部信息素更新蒸发率
GLOBAL_EVAPORATION:         全局信息素更新蒸发率
Q:                          信息素计算分子
SELECT_NEXT                 节点选择比例
OMEGA                       允许释放信息素的蚂蚁数量
G_MAX                       最大迭代次数
Sn                          每代产生的解决方案个数
city_num                    城市个数
density_effect              密度对速度效果参数
'''

(BETA, ALPHA, LOCAL_EVAPORATION, GLOBAL_EVAPORATION, Q, SELECT_NEXT, OMEGA, G_MAX, Sn, city_num, density_effect) = (
    1.0, 2.0, 0.1, 0.1, 100.0, 0.9, 3, 100, 10, 16, 0.5
)

'''
ant_num                     蚂蚁个数
default_base_num            默认基数
capacity                    路径容量
way_selection               1--Pure_Base_Num  2--Extended_Base_Num
default_speed               默认速度
initial_pheromone           初始信息素浓度
unsafe_city                 撤离起点
safe_city                   撤离终点
'''
ant_num = 100
default_base_num = 5
capacity = 100
way_selection = 1
default_speed = 10
initial_pheromone = 0.0
unsafe_city = [0, 1, 2, 3, 4]
safe_city = [12, 13, 14, 15]

distance_x = [
    85, 264, 107, 354, 258, 135, 443, 250, 123, 147, 363, 456, 424, 369, 345, 221]
distance_y = [
    45, 33, 105, 65, 135, 210, 153, 250, 332, 453, 341, 341, 430, 445, 542, 542]

# 城市距离和信息素初始化
distance_graph = [[0.0 for col_d in range(city_num)] for raw_d in range(city_num)]
pheromone_graph = [[0.0 for col_p in range(city_num)] for raw_P in range(city_num)]
density_graph = [[0.0 for col_de in range(city_num)] for raw_de in range(city_num)]
all_distance = 0
all_nodes = 0
ants = []
path_x_y = [
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],  # 10
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 15
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
capacity_graph = [
    [0, capacity, capacity, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, capacity, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, capacity, capacity, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, capacity, 0, capacity, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, capacity, capacity, capacity, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
    [0, 0, 0, 0, 0, 0, 0, 0, capacity, capacity, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, capacity, 0, 0, capacity, capacity, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, capacity, capacity, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, capacity, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, capacity, capacity],  # 10
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, capacity, 0, capacity, capacity, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, capacity, capacity, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 15
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def __cal_density():
    for i in range(city_num):
        for j in range(city_num):
            density_graph[i][j] = (capacity - capacity_graph[i][j]) / (distance_graph[i][j])


# ------------ 蚂蚁 ------------
class Ant(object):
    global ant_num

    # 初始化
    def __init__(self, ID):
        self.ID = ID  # 蚂蚁的ID
        self.__clean_data()  # 随机初始化出生点

    def __set_parm(self, path, move_count, current_city, open_table_city, select_cities_prob, base_num):
        self.__clean_data()
        self.path = path
        self.move_count = move_count
        self.current_city = current_city
        self.open_table_city = open_table_city
        self.select_cities_prob = select_cities_prob
        self.base_num = base_num

    def __clean_data(self):
        self.path = []  # 当前蚂蚁的路径
        self.total_distance = 0.0  # 当前路径的总距离
        self.total_time = 0.0  # 当前路径的总时间
        self.move_count = 0  # 移动次数
        self.current_city = -1  # 当前停留的城市
        self.next_city = -1  # 下一个城市
        self.open_table_city = [False for i in range(city_num)]  # 将要探索城市的状态
        self.select_cities_prob = [0.0 for i in range(city_num)]  # 存储去下一个城市的概率
        self.base_num = default_base_num  # 基数
        self.speed = 0.0  # 移动速度

        city_index = random.randint(0, 4)  # 出生城市随机
        self.current_city = city_index  # 当前城市
        self.path.append(city_index)
        self.open_table_city[city_index] = False
        self.move_count = 1
        self.total_prob = 0.0

    # 选择下一个城市
    def __choose_next_city(self):
        global ant_num
        next_city = -1
        temp_prob = 0.0
        temp_index = -1
        temp_path = []
        #  生成随机数
        random_num = random.uniform(0, 1)
        self.__calculate_next_city_prob()
        #  最优路径 / 轮盘选择
        if random_num <= SELECT_NEXT:
            #  最优路径
            for i in range(city_num):
                if temp_prob < self.select_cities_prob[i]:
                    temp_prob = self.select_cities_prob[i]
                    temp_index = i
            if capacity_graph[self.current_city][temp_index] < self.base_num:
                if way_selection == 1:  # 纯基数
                    for i in range(city_num):
                        if path_x_y[self.current_city][i] == 1:
                            temp_path.append(i)
                    temp_index = random.choice(temp_path)
                    while capacity_graph[self.current_city][temp_index] < self.base_num:
                        temp_index = random.choice(temp_path)
                else:  # 扩展基数
                    self.base_num = capacity_graph[self.current_city][temp_index]
                    ant_num += 1
                    new_ant = Ant(self.ant_num)
                    new_ant.__set_parm(self.path, self.move_count, self.current_city, self.open_table_city,
                                       self.select_cities_prob, self.base_num)
                    ants.append(new_ant)
            self.next_city = temp_index
        else:
            #  轮盘选择
            temp_prob = random.uniform(0.0, self.total_prob)
            for i in range(city_num):
                if self.open_table_city[i]:
                    temp_prob -= self.select_cities_prob[i]
                    if temp_prob < 0.0:
                        temp_index = i
                        break
            if capacity_graph[self.current_city][temp_index] < self.base_num:
                if way_selection == 1:  # 纯基数
                    while capacity_graph[self.current_city][temp_index] < self.base_num:
                        temp_prob = random.uniform(0.0, self.total_prob)
                        for i in range(city_num):
                            if self.open_table_city[i]:
                                temp_prob -= self.select_cities_prob[i]
                                if temp_prob < 0.0:
                                    temp_index = i
                                    break
                else:  # 扩展基数
                    self.base_num = capacity_graph[self.current_city][temp_index]
                    ant_num += 1
                    new_ant = Ant(self.ant_num)
                    new_ant.__set_parm(self.path, self.move_count, self.current_city, self.open_table_city,
                                       self.select_cities_prob, self.base_num)
                    ants.append(new_ant)
            self.next_city = temp_index

    #  计算当前城市到下个城市概率列表
    def __calculate_next_city_prob(self):
        self.total_prob = 0.0
        self.__renew_current_city()
        for i in range(city_num):
            if self.open_table_city[i]:
                try:
                    self.select_cities_prob[i] = pow(pheromone_graph[self.current_city][i], ALPHA) * pow(
                        1.0 / (distance_graph[self.current_city][i] * density_graph[self.current_city][i]), BETA)
                    self.total_prob += self.select_cities_prob[i]
                except ZeroDivisionError as e:
                    print('Ant ID: {ID}, current city: {current}, target city: {target}'.format(ID=self.ID,
                                                                                                current=
                                                                                                self.current_city,
                                                                                                target=i))
                    sys.exit(1)

    #  更新可去节点列表
    def __renew_current_city(self):
        self.open_table_city = [False for i in range(0, city_num)]
        for i in range(0, city_num):
            if path_x_y[self.current_city][i] == 1:
                self.open_table_city[i] = True

    #   计算当前速度
    def __cal_current_speed(self):
        self.speed = default_speed * math.exp(density_effect * (-density_graph[self.current_city][self.next_city]))

    #  计算总距离
    def __cal_total_distance(self):
        temp_distance = 0.0
        start, end = self.path[1], self.path[0]
        for i in range(1, city_num):
            start, end = self.path[i], self.path[i - 1]
            temp_distance += distance_graph[start][end]
        self.total_distance = temp_distance

    #  移动 记得最后再移动！
    def __move(self):
        self.path.append(self.next_city)
        self.total_distance += distance_graph[self.current_city][self.next_city]
        self.total_time += (distance_graph[self.current_city][self.next_city] / self.speed)
        self.current_city = self.next_city
        self.move_count += 1

    def __add_capacity(self):
        capacity_graph[self.current_city][self.next_city] += self.base_num

    def __sub_capacity(self):
        capacity_graph[self.current_city][self.next_city] -= self.base_num

    #  搜索路径
    def __search_path(self):
        self.__clean_data()
        while (self.current_city != 13) or (self.current_city != 13) or (self.current_city != 13) or (
                self.current_city != 13):
            self.__choose_next_city()
            self.__move()
        self.__cal_total_distance()


class TSP(object):

    def __init__(self):
        pass

    def new(self):
        # 计算城市之间的距离
        global all_distance, all_nodes, initial_pheromone
        for i in range(city_num):
            for j in range(city_num):
                temp_distance = pow((distance_x[i] - distance_x[j]), 2) + pow((distance_y[i] - distance_y[j]), 2)
                temp_distance = pow(temp_distance, 0.5)
                distance_graph[i][j] = float(int(temp_distance + 0.5))

        # 初始化信息素浓度
        returning = []
        for origin in unsafe_city:
            for goal in safe_city:
                edge = Stack(city_num, path_x_y)
                edge.push(origin)
                edge.dfsStack(-1, goal)
                returning.append(edge.all_path)
        all_path = returning[0]
        for path in all_path:
            temp_all = len(path)
            i = 1
            while i < temp_all:
                all_distance = all_distance + distance_graph[path[i - 1]][path[i]]
                i = i + 1
            all_nodes = all_nodes + len(path)
        initial_pheromone = 1 / (all_nodes * all_distance)


if __name__ == '__main__':
    edge_capacity = multiprocessing.Manager().list(capacity_graph)
    pool = multiprocessing.Pool(processes=50)
