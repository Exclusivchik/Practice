from tkinter import *
from tkinter import messagebox
from random import choice, randint, sample
from functools import partial

window = Tk()
window.title("Sea battle")
window.geometry('700x550')

transform = {0: "one", 1: "two", 2: "three", 3: "four"}

field = [["□" for i in range(10)] for j in range(10)]
ships_cnt = [4, 3, 2, 1]

status_bar = []
for i in range(4): # Статус кораблей
    status_bar.append(Label(window, text = transform[i] + "-deck ships left: " + str(ships_cnt[i]), font = ("Arial Bold", 15)))
    status_bar[i].grid(column = 13, row = 3 + i, sticky=W)

def print_field():
    print("    0 1 2 3 4 5 6 7 8 9")
    print("  ____________________")
    for i in range(10):
        print(i, "|", *field[i])


def change(location):
    for i in location:
        field[i[0]][i[1]] = "■"


def check(pos, length, dir):
    n = 10
    to_clean = []
    location = [[-1, -1] for i in range(length)]
    if dir == 0:
        if pos[0] - length < 0: return []
        else:
            for i in range(max(pos[1] - 1, 0), min(pos[1] + 1 + 1, n)):
                for j in range(max(pos[0] - length, 0), min(pos[0] + 1 + 1, n)):
                    if field[j][i] == "■": return []
                    else: to_clean.append([j, i])
        for i in range(length):
            location[i] = [pos[0] - i, pos[1]]
    if dir == 1:
        if pos[0] + length > n - 1: return []
        else:
            for i in range(max(pos[1] - 1, 0), min(pos[1] + 1 + 1, n)):
                for j in range(max(pos[0] - 1, 0), min(pos[0] + length + 1, n)):
                    if field[j][i] == "■": return []
                    else: to_clean.append([j, i])
        for i in range(length):
            location[i] = [pos[0] + i, pos[1]]
    if dir == 2:
        if pos[1] + length > n - 1: return []
        else:
            for i in range(max(pos[0] - 1, 0), min(pos[0] + 1 + 1, n)):
                for j in range(max(pos[1] - 1, 0), min(pos[1] + length + 1, n)):
                    if field[i][j] == "■": return []
                    else: to_clean.append([i, j])
        for i in range(length):
            location[i] = [pos[0], pos[1] + i]
    if dir == 3:
        if pos[1] - length < 0: return []
        else:
            for i in range(max(pos[0] - 1, 0), min(pos[0] + 1 + 1, n)):
                for j in range(max(pos[1] - length, 0), min(pos[1] + 1 + 1, n)):
                    if field[i][j] == "■": return []
                    else: to_clean.append([i, j])
        for i in range(length):
            location[i] = [pos[0], pos[1] - i]
    return [to_clean, location]


def build_ship(length):
    while 1:
        pos = choice(moves)
        posible_directions = set(range(4)) #Вверх вниз вправо влево
        while len(posible_directions) != 0:
            dir = choice(tuple(posible_directions))
            to_wipe = check(pos, length, dir)
            if len(to_wipe) == 0:
                posible_directions.remove(dir)
                continue
            else:
                change(to_wipe[1])
                for i in to_wipe[0]: #Чистим поле от занятых клеток
                    try:
                        it = moves.index(i)
                        del moves[it] #Возможно мы уже затёрли эту позицию, когда ставили другой корабль, поэтому делаем try
                    except: continue

                return to_wipe


def wipe_around(sea_battle, ship):
    for i in ship[0]:
        if i not in ship[1]:
            sea_battle[i[1]][i[0]].configure(bg = "GREY", state = "disabled")


def cmd(x, y, sea_battle, ships_location, temp_game):
    ship_type, ship_number, to_del = -1, -1, -1
    for i in range(4):
        for j in range(len(temp_game[i])):
            for k in range(len(temp_game[i][j][1])):
                if [y, x] == temp_game[i][j][1][k]:
                    ship_type = i
                    ship_number = j
                    to_del = k
                    flg = 1
                    break
    if ship_type == -1:
        sea_battle[x][y].configure(bg = "GREY", state = "disabled")
    else:
        sea_battle[x][y].configure(bg = "RED", state = "disabled")
        del temp_game[ship_type][ship_number][1][to_del]
        if len(temp_game[ship_type][ship_number][1]) == 0:
            ships_cnt[ship_type] -= 1
            status_bar[ship_type].configure(text = transform[ship_type] + "-deck ships left: " + str(ships_cnt[ship_type]))
            wipe_around(sea_battle, ships_location[ship_type][ship_number])
            for i in ships_location[ship_type][ship_number][1]:
                sea_battle[i[1]][i[0]].configure(bg = "BLACK")
            if sum(ships_cnt) == 0:
                messagebox.showinfo('Message', "Game over. You win!")
                quit()


moves = [[i, j] for i in range(10) for j in range(10)] #Возможные позиции для расстановки кораблей

ships_location = [[build_ship(1), build_ship(1), build_ship(1), build_ship(1)],[build_ship(2), build_ship(2), build_ship(2)], [build_ship(3), build_ship(3)], [build_ship(4)]]
temp_game = [[] for i in range(4)]
for i in range(4):  #Копирование массива
    for j in range(len(ships_location[i])):
        temp = [[], []]
        for q in range(2):
            for k in ships_location[i][j][q]:
                temp[q].append(k)
        temp_game[i].append(temp)

for i in range(10): #Буквы на поле
    lbl = Label(window, text = "ABCDEFGHIJ"[i], font = ("Arial Bold", 10))
    lbl.grid(column = i + 1, row = 0)
for i in range(10): #Цифры на поле
    lbl = Label(window, text = str(i + 1), font = ("Arial Bold", 10))
    lbl.grid(column = 0, row = i + 1)

sea_battle = [[Button() for i in range(10)] for j in range(10)] #Кнопки
for i in range(10):
    for j in range(10):
        action = partial(cmd, i, j, sea_battle, ships_location, temp_game)
        sea_battle[i][j] = Button(window, height = 2, width = 4, relief = GROOVE, command = action)
        sea_battle[i][j].grid(column = i + 1, row = j + 1)

print_field()

window.mainloop()
