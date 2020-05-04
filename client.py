import socket
import threading
import time
import json


class moonwalker:
    def __init__(self):
        self.position = None
        self.point = 0
        self.shot_pos = None

    # перемещение:
    def move_forward(self):
        if self.point > 0:
            x, y = self.position
            x -= 1
            if x >= 0:
                self.position = x, y
                self.point -= 1
            else:
                print("Вы на краю карты, движение невозможно")
        return self.position, None

    def move_back(self):
        if self.point > 0:
            x, y = self.position
            x += 1
            if x < 8:
                self.position = x, y
                self.point -= 1
            else:
                print("Вы на краю карты, движение невозможно")
            return self.position, None

    def move_left(self):
        if self.point > 0:
            x, y = self.position
            y -= 1
            if y >= 0:
                self.position = x, y
                self.point -= 1
            else:
                print("Вы на краю карты, движение невозможно")
            return self.position, None

    def move_right(self):
        if self.point > 0:
            x, y = self.position
            y += 1
            if y < 8:
                self.position = x, y
                self.point -= 1
            else:
                print("Вы на краю карты, движение невозможно")
        return self.position, None

    # стрельба:
    def shot_forward(self):
        self.shot_pos = None
        if self.point > 2:
            self.point -= 3
            x, y = self.position
            x -= 1
            self.shot_pos = (x, y)
            print("Объект на точке ({}, {}) уничтожен".format(x, y))
        else:
            print("У вас законочились боеприпасы")
        return self.position, self.shot_pos

    def shot_back(self):
        self.shot_pos = None
        if self.point > 2:
            self.point -= 3
            x, y = self.position
            x += 1
            self.shot_pos = (x, y)
            print("Объект на точке (", x, ", ", y, ") уничтожен")
        else:
            print("У вас закончились боеприпасы")
        return self.position, self.shot_pos

    def shot_left(self):
        self.shot_pos = None
        if self.point > 2:
            self.point -= 3
            x, y = self.position
            y -= 1
            self.shot_pos = (x, y)
            print("Объект на точке (", x, ", ", y, ") уничтожен")
        else:
            print("У вас закончились боеприпасы")
        return self.position, self.shot_pos

    def shot_right(self):
        self.shot_pos = None
        if self.point > 2:
            self.point -= 3
            x, y = self.position
            y += 1
            self.shot_pos = (x, y)
            print("Объект на точке (", x, ", ", y, ") уничтожен")
        else:
            print("У вас закончились боеприпасы")
        return self.position, self.shot_pos


key = 8194

shutdown = False
join = False


def try_to_made_command(com):
    if com == 'w':
        return player.move_forward()
    elif com == 's':
        return player.move_back()
    elif com == 'a':
        return player.move_left()
    elif com == 'd':
        return player.move_right()
    elif com == 'wf':
        return player.shot_forward()
    elif com == 'sf':
        return player.shot_back()
    elif com == 'af':
        return player.shot_left()
    elif com == 'df':
        return player.shot_right()
    else:
        print("This command is not available, please keep instructions")
        return player.position, None


def launch_game():
    while True:
        command = input()
        actions = try_to_made_command(command)
        print("У вас осталось {} очков".format(player.point))
        data_set = {"pos": actions[0], "shot": actions[1], "points": player.point}
        json_data_set = json.dumps(data_set)
        s.sendto(json_data_set.encode('utf-8'), server)


def receving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                json_string = data.decode("utf-8")
                data = json.loads(json_string)
                dict_key = list(data.keys())[0]

                if dict_key == "message":
                    print(data['message'])
                elif dict_key == 'map':
                    print(data['map'])
                elif dict_key == "pos":
                    my_list = list(data['pos'])
                    x, y = int(my_list[1]), int(my_list[4])
                    player.position = x, y
                elif dict_key == "points":
                    player.point = int(data['points'])
                    print(data["message"])

                time.sleep(0.2)
        except:
            pass


host = socket.gethostbyname(socket.gethostname())
port = 0

server = ("192.168.1.117", 9090)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

alias = input("Name: ")

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()
player = moonwalker()

while shutdown == False:
    if join == False:
        s.sendto(("[" + alias + "] => join the game ").encode("utf-8"), server)
        join = True
    else:
        try:
            launch_game()
            message = input()

            if message != "":
                s.sendto(("[" + alias + "] :: " + message).encode("utf-8"), server)

            time.sleep(0.2)
        except:
            s.sendto(("[" + alias + "] <= left chat ").encode("utf-8"), server)
            shutdown = True

rT.join()
s.close()