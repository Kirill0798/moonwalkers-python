import numpy
import random
import json


class moon_map:
    def __init__(self, m=8, n=8, count_of_stones=40):
        self.map = self.fill_map_with_stones(m, n, count_of_stones)
        self.pos_one = self.define_user_pos(self.map)
        self.pos_two = self.define_user_pos(self.map)

    @staticmethod
    def create_empty_map(m, n):
        return numpy.zeros(shape=(m, n), dtype=int)

    @staticmethod
    def create_stones(count):
        """создается массив кортежей, в котором указывается позиция на карте в декартовых координатах"""
        arr = []
        count_of_stones = random.randint(0, count)
        for i in range(count_of_stones):
            arr.append((random.randint(0, 7), random.randint(0, 7)))
        return arr

    @staticmethod
    def define_user_pos(map_for_user):
        while True:
            x, y = random.randint(0, 7), random.randint(0, 7)
            if map_for_user[x][y] != 1:
                return x, y

    def fill_map_with_stones(self, m, n, count_of_stones):
        empty_map = self.create_empty_map(m, n)
        stones = self.create_stones(count_of_stones)
        for stone in stones:
            x, y = stone
            # есть камень - 1
            empty_map[x][y] = 8

        return empty_map


