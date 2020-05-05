import socket
import time
from files import moon_map
import json
import random
import numpy

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



salutation_message = """
{
    "message": "Welcome to the game Moonwalker. In this game you will manipulate your vehicle with the next commands: w - move forward, a - move left, d - move right, s - move back. The commnads of navigation take 1 point of your gas. If you wanna shot you should add f to your command. Shotting takes 3 point. Each round you are getting random number of points"
}
"""
err_msg_pos = """
{
    "message": "You can't move your vehicle here. Please change direction!"
}
"""
round_start_message = "Round {} is started. {}, get ready!"

another_player_message = {
    "message": "It is not your turn. Please waiting!",
    "pos": ""
}

send_msg_points = {
    "points": "",
    "message": ""
}
player_two_msg = """
{
    "message": "Player 2, it is your turn"
}
"""

player_points_str = "Player {}, you have {} points"
death_msg = "Player {} won. Game is ended."


def check_death(value):
    if value != 8 and value != 0:
        return True
    else:
        return False


def send_to_all_users(s, clients, message):
    for i in clients:
        s.sendto(message.encode("utf-8"), i)


def made_json_format(current_key, obj):
    obj_str = str(obj)
    d = {current_key: obj_str}
    return json.dumps(d)


def generate_points():
    return random.randint(1, 6)


def launch_game(s, clients):
    # подготовка игры:
    start_msg = salutation_message.encode("utf-8")
    my_map = moon_map.moon_map()
    current_map = my_map.map
    map_msg = made_json_format("map", current_map)
    # отправка сообщений:
    for i in clients:
        s.sendto(start_msg, i)
        s.sendto(map_msg.encode("utf-8"), i)

    # сообщить позицию каждого:
    x, y = my_map.pos_one
    current_map[x][y] = 1
    pos = (x, y)
    pos_msg = made_json_format("pos", pos)
    s.sendto(pos_msg.encode("utf-8"), clients[0])
    x, y = my_map.pos_two
    current_map[x][y] = 2
    pos = (x, y)
    pos_msg = made_json_format("pos", pos)
    s.sendto(pos_msg.encode("utf-8"), clients[1])

    # начало игры, каждый игрок ходит по очереди:
    round_of_game = 0
    while True:
        # начало раунда:
        round_of_game += 1

        # распределение очков:
        first_player_points = generate_points()
        send_msg_points['points'] = first_player_points
        send_msg_points['message'] = player_points_str.format(1, first_player_points)
        s.sendto((json.dumps(send_msg_points)).encode("utf-8"), clients[0])
        second_player_points = generate_points()
        send_msg_points['points'] = second_player_points
        send_msg_points['message'] = player_points_str.format(2, second_player_points)
        s.sendto((json.dumps(send_msg_points)).encode("utf-8"), clients[1])

        rsm = round_start_message.format(round_of_game, 1)
        rsm = made_json_format("message", rsm)
        send_to_all_users(s, clients, rsm)
        map_msg = made_json_format('map', current_map)
        send_to_all_users(s, clients, map_msg)

        # взаимодействие с первым игроком:
        while first_player_points > 0:
            _data, _addr = s.recvfrom(1024)
            if _addr == clients[0]:
                json_string = _data.decode("utf-8")
                print(json_string)
                json_string = json.loads(json_string)
                dict_key_pos = list(json_string.keys())[0]
                dict_key_shot = list(json_string.keys())[1]
                dict_key_points = list(json_string.keys())[2]
                first_player_points = int(json_string[dict_key_points])
                my_list_pos = list(json_string[dict_key_pos])
                x_pos, y_pos = int(my_list_pos[0]), int(my_list_pos[1])
                q, w = my_map.pos_one

                if x_pos == q and y_pos == w:
                    try:
                        my_list_shot = list(json_string[dict_key_shot])
                        print(my_list_shot)
                        x_shot, y_shot = int(my_list_shot[0]), int(my_list_shot[1])
                        if check_death(current_map[x_shot][y_shot]):
                            dm = death_msg.format(1)
                            dm = made_json_format("message", dm)
                            send_to_all_users(s, clients, dm)
                            s.close()
                            break
                        current_map[x_shot][y_shot] = 0
                    except:
                        print("Что-то пошло не так")
                elif (x_pos != q or y_pos != w) and current_map[x_pos][y_pos] != 8 and current_map[x_pos][y_pos] != 2:
                    current_map[q][w] = 0
                    current_map[x_pos][y_pos] = 1
                    my_map.pos_one = x_pos, y_pos
                else:
                    s.sendto(err_msg_pos.encode("utf-8"), clients[0])
                    pos = q, w
                    pos_msg = made_json_format("pos", pos)
                    s.sendto(pos_msg.encode("utf-8"), clients[0])
            elif _addr == clients[1]:
                another_player_message['pos'] = str(my_map.pos_two)
                s.sendto((json.dumps(another_player_message)).encode("utf-8"), clients[1])
            map_msg = made_json_format("map", current_map)
            send_to_all_users(s, clients, map_msg)
        print(1)

        s.sendto(player_two_msg.encode('utf-8'), clients[1])
        print(2)
        while second_player_points > 0:
            _data, _addr = s.recvfrom(1024)
            if _addr == clients[1]:
                json_string = _data.decode("utf-8")
                print(json_string)
                json_string = json.loads(json_string)
                dict_key_pos = list(json_string.keys())[0]
                dict_key_shot = list(json_string.keys())[1]
                dict_key_points = list(json_string.keys())[2]
                second_player_points = int(json_string[dict_key_points])
                my_list_pos = list(json_string[dict_key_pos])
                x_pos, y_pos = int(my_list_pos[0]), int(my_list_pos[1])
                q, w = my_map.pos_two

                if x_pos == q and y_pos == w:
                    try:
                        my_list_shot = list(json_string[dict_key_shot])
                        print(my_list_shot)
                        x_shot, y_shot = int(my_list_shot[0]), int(my_list_shot[1])
                        if check_death(current_map[x_shot][y_shot]):
                            dm = death_msg.format(2)
                            dm = made_json_format("message", dm)
                            send_to_all_users(s, clients, dm)
                            s.close()
                            break
                        current_map[x_shot][y_shot] = 0
                    except:
                        print("Что-то пошло не так")
                elif (x_pos != q or y_pos != w) and current_map[x_pos][y_pos] != 8 and current_map[x_pos][y_pos] != 1:
                    current_map[q][w] = 0
                    current_map[x_pos][y_pos] = 2
                    my_map.pos_two = x_pos, y_pos
                else:
                    s.sendto(err_msg_pos.encode("utf-8"), clients[1])
                    pos = q, w
                    pos_msg = made_json_format("pos", pos)
                    s.sendto(pos_msg.encode("utf-8"), clients[1])
            elif _addr == clients[0]:
                another_player_message['pos'] = str(my_map.pos_two)
                s.sendto((json.dumps(another_player_message)).encode("utf-8"), clients[0])
            map_msg = made_json_format("map", current_map)
            send_to_all_users(s, clients, map_msg)


host = socket.gethostbyname(socket.gethostname())
port = 9090

clients = []
awaiting = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

print("[ Server Started ]")

while True:
    try:
        data, addr = s.recvfrom(1024)
        if addr not in clients:
            clients.append(addr)

        action_time = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

        print("[" + addr[0] + "]=[" + str(addr[1]) + "]=[" + action_time + "]/", end="")
        print(data.decode("utf-8"))

        if len(clients) == 2:
            launch_game(s, clients)

        for client in clients:
            if addr != client:
                s.sendto(data, client)

    except Exception:
        print(Exception)
        print("\n[ Server Stopped ]")

s.close()
