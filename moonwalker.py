class moonwalker:
    def __init__(self):
        self.position = None
        self.point = 0
        self.shot_pos = None

    # перемещение:
    def move_forward(self):
        self.shot_pos = None
        if self.point > 0:
            x, y = self.position
            x -= 1
            if x >= 0:
                self.position = x, y
                self.point -= 1
            else:
                print("Вы на краю карты, движение невозможно")
        return self.position, self.shot_pos

    def move_back(self):
        self.shot_pos = None
        if self.point > 0:
            x, y = self.position
            x += 1
            if x < 8:
                self.position = x, y
                self.point -= 1
            else:
                print("Вы на краю карты, движение невозможно")
            return self.position, self.shot_pos

    def move_left(self):
        self.shot_pos = None
        if self.point > 0:
            x, y = self.position
            y -= 1
            if y >= 0:
                self.position = x, y
                self.point -= 1
            else:
                print("Вы на краю карты, движение невозможно")
            return self.position, self.shot_pos

    def move_right(self):
        self.shot_pos = None
        if self.point > 0:
            x, y = self.position
            y += 1
            if y < 8:
                self.position = x, y
                self.point -= 1
            else:
                print("Вы на краю карты, движение невозможно")
        return self.position, self.shot_pos

    # стрельба:
    def shot_forward(self):
        self.shot_pos = None
        if self.point > 2:
            self.point -= 3
            x, y = self.position
            x -= 1
            self.shot_pos = (x, y)
            print("Объект на точке ({}, {})".format(x, y))
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