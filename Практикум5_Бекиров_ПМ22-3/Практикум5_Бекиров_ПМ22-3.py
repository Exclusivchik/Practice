from tkinter import *
from tkinter import messagebox
import copy

window = Tk()
window.title("Chess")
window.geometry('700x700')

temp_turn = 0
turns_cnt = 0
temp_str = ""
t = Label(window, text = f"number of moves: {turns_cnt}", font = ("Arial Bold", 15))
t.grid(column = 10, row = 5)
last = []
for_cmd = 0

for i in range(8): #Буквы и цифры на поле
    Label(window, text = "ABCDEFGH"[i], font = ("Arial Bold", 15)).grid(column = i + 1, row = 0)
    Label(window, text = "ABCDEFGH"[i], font = ("Arial Bold", 15)).grid(column = i + 1, row = 9)
    Label(window, text = str(8 - i), font = ("Arial Bold", 15)).grid(column = 0, row = i + 1)
    Label(window, text = str(8 - i), font = ("Arial Bold", 15)).grid(column = 9, row = i + 1)


def tips(cells, color, unable = True):
    if unable:
        if color == "white":
            for temp in cells:
                x, y = temp
                if a[x][y].color == "black":
                    a[x][y].button.config(bg = ("blue"))
                else:
                    a[x][y].button.config(bg = ("grey"))
        if color == "black":
            for temp in cells:
                x, y = temp
                if a[x][y].color == "white":
                    a[x][y].button.config(bg = ("blue"))
                else:
                    a[x][y].button.config(bg = ("grey"))
    else:
        for temp in cells:
            x, y = temp
            a[x][y].button.config(bg = ["white", "green"][(x + y) % 2])


def update_figs():
    for r in range(8):
        for c in range(8):
            a[r][c].upd_moves()
            if (not temp_turn and a[r][c].color == "black") or (temp_turn and a[r][c].color == "white"):
                a[r][c].cells.clear()


def game(fig):
    global temp_turn, turns_cnt
    if len(fig.cells) == 0 and len(last) == 0:
        return
    last.append(fig)
    if len(last) == 1:
        tips(fig.cells, fig.color, True)
    if len(last) != 2: return

    first, second = last
    f_x, f_y = first.pos
    s_x, s_y = second.pos
    tips(first.cells, first.color, False)
    if second.pos in first.cells:
        temp_turn, turns_cnt = abs(temp_turn - 1), turns_cnt + 1

        if type(first) == Pawn:
            a[s_x][s_y] = Pawn  (first.color, s_x, s_y)
        if type(first) == Rook:
            a[s_x][s_y] = Rook  (first.color, s_x, s_y)
        if type(first) == Knight:
            a[s_x][s_y] = Knight(first.color, s_x, s_y)
        if type(first) == Bishop:
            a[s_x][s_y] = Bishop(first.color, s_x, s_y)
        if type(first) == Queen:
            a[s_x][s_y] = Queen (first.color, s_x, s_y)
        if type(first) == King:
            a[s_x][s_y] = King  (first.color, s_x, s_y)
        if type(first) == Trez:
            a[s_x][s_y] = Trez  (first.color, s_x, s_y)
        if type(first) == Swoop:
            a[s_x][s_y] = Swoop (first.color, s_x, s_y)
        if type(first) == Cross:
            a[s_x][s_y] = Cross (first.color, s_x, s_y)

        if type(second) == King:
            a[f_x][f_y] = Empty(f_x, f_y)
            messagebox.showinfo('Message', f"Game over. {first.color} wins!")
            quit()

        a[f_x][f_y] = Empty(f_x, f_y)

        t["text"] = f"number of moves: {turns_cnt}"

    update_figs()
    last.clear()


class Pawn():
    def __init__(self, color, r, c, first = False):
        self.first, self.color, self.pos = first, color, (r, c)
        self.image = PhotoImage(file = f"Figures/{color}_pawn.png")
        self.button = Button(window, image = self.image, bg = ["white", "green"][(r + c) % 2], height = 45, width = 45, command = self.cmd)
        self.button.grid(row = r + 1, column = c + 1)
        self.cells = []

    def moves(self):
        x, y = self.pos
        if self.color == "white": return [a[x - 1][y + i].pos for i in [-1, 1] if 0 <= y + i < 8 and x - 1 >= 0 and type(a[x - 1][y + i]) != Empty and a[x - 1][y + i].color == "black"] + [(x - 1, y) for i in [1] if x - 1 >= 0 and type(a[x - 1][y]) == Empty] + [(x - 2, y) for i in [1] if x - 1 >= 0 and type(a[x - 1][y]) == Empty and x - 2 >= 0 and self.first and type(a[x - 2][y]) == Empty]
        return [a[x + 1][y + i].pos for i in [-1, 1] if 0 <= y + i < 8 and x + 1 <= 7 and type(a[x + 1][y + i]) != Empty and a[x + 1][y + i].color == "white"] + [(x + 1, y) for i in [1] if x + 1 <= 7 and type(a[x + 1][y]) == Empty] + [(x + 2, y) for i in [1] if x + 1 <= 7 and type(a[x + 1][y]) == Empty and x + 2 <= 7 and self.first and type(a[x + 2][y]) == Empty]

    def upd_moves(self):
        self.cells = copy.deepcopy(self.moves())

    def __str__(self):
        return f"{self.pos, self.color, self.cells}"

    def cmd(self):
        #print(self)
        game(self)

class Trez():
    def __init__(self, color, r, c):
        self.color, self.pos = color, (r, c)
        self.image = PhotoImage(file = f"Figures/{color}_trez.png")
        self.button = Button(window, image = self.image, bg = ["white", "green"][(r + c) % 2], height = 45, width = 45, command = self.cmd)
        self.button.grid(row = r + 1, column = c + 1)
        self.cells = []

    def moves(self):
        x, y = self.pos
        if self.color == "white":
            return [a[x - 1][y + i].pos for i in [-1, 0, 1] if 0 <= y + i < 8 and x - 1 >= 0 and a[x - 1][y + i].color != "white"]
        else:
            return [a[x + 1][y + i].pos for i in [-1, 0, 1] if 0 <= y + i < 8 and x + 1 < 8 and a[x + 1][y + i].color != "black"]

    def upd_moves(self):
        self.cells = copy.deepcopy(self.moves())

    def __str__(self):
        return f"{self.pos, self.color, self.cells}"

    def cmd(self):
        game(self)

class Swoop():
    def __init__(self, color, r, c):
        self.color, self.pos = color, (r, c)
        self.image = PhotoImage(file = f"Figures/{color}_swoop.png")
        self.button = Button(window, image = self.image, bg = ["white", "green"][(r + c) % 2], height = 45, width = 45, command = self.cmd)
        self.button.grid(row = r + 1, column = c + 1)
        self.cells = []

    def moves(self):
        x, y = self.pos
        if self.color == "white":
            return [a[x + i][y].pos for i in range(-2, 2 + 1) if 0 <= x + i < 8 and a[x + i][y].color != "white"]
        else:
            return [a[x + i][y].pos for i in range(-2, 2 + 1) if 0 <= x + i < 8 and a[x + i][y].color != "black"]

    def upd_moves(self):
        self.cells = copy.deepcopy(self.moves())

    def __str__(self):
        return f"{self.pos, self.color, self.cells}"

    def cmd(self):
        game(self)

class Swoop():
    def __init__(self, color, r, c):
        self.color, self.pos = color, (r, c)
        self.image = PhotoImage(file = f"Figures/{color}_swoop.png")
        self.button = Button(window, image = self.image, bg = ["white", "green"][(r + c) % 2], height = 45, width = 45, command = self.cmd)
        self.button.grid(row = r + 1, column = c + 1)
        self.cells = []

    def moves(self):
        x, y = self.pos
        if self.color == "white":
            return [a[x + i][y].pos for i in range(-2, 2 + 1) if 0 <= x + i < 8 and a[x + i][y].color != "white"]
        else:
            return [a[x + i][y].pos for i in range(-2, 2 + 1) if 0 <= x + i < 8 and a[x + i][y].color != "black"]

    def upd_moves(self):
        self.cells = copy.deepcopy(self.moves())

    def __str__(self):
        return f"{self.pos, self.color, self.cells}"

    def cmd(self):
        game(self)

class Cross():
    def __init__(self, color, r, c):
        self.color, self.pos = color, (r, c)
        self.image = PhotoImage(file = f"Figures/{color}_cross.png")
        self.button = Button(window, image = self.image, bg = ["white", "green"][(r + c) % 2], height = 45, width = 45, command = self.cmd)
        self.button.grid(row = r + 1, column = c + 1)
        self.cells = []

    def moves(self):
        x, y = self.pos
        if self.color == "white":
            return [a[x + i][y].pos for i in range(-2, 2 + 1) if 0 <= x + i < 8 and a[x + i][y].color != "white"] + [a[x][y + i].pos for i in range(-2, 2 + 1) if 0 <= y + i < 8 and a[x][y + i].color != "white"]
        else:
            return [a[x + i][y].pos for i in range(-2, 2 + 1) if 0 <= x + i < 8 and a[x + i][y].color != "black"] + [a[x][y + i].pos for i in range(-2, 2 + 1) if 0 <= y + i < 8 and a[x][y + i].color != "black"]

    def upd_moves(self):
        self.cells = copy.deepcopy(self.moves())

    def __str__(self):
        return f"{self.pos, self.color, self.cells}"

    def cmd(self):
        game(self)

class Rook():
    def __init__(self, color, r, c):
        self.color = color
        self.image = PhotoImage(file = f"Figures/{color}_rook.png")
        self.pos = (r, c)
        self.button = Button(window, image = self.image, bg = ["white", "green"][(r + c) % 2], height = 45, width = 45, command = self.cmd)
        self.button.grid(row = r + 1, column = c + 1)
        self.cells = []

    def moves(self):
        cells = []
        x, y = self.pos
        for c in range(y + 1, 8):
            temp = a[x][c]
            if type(temp) == Empty:
                cells.append((x, c))
            elif temp.color != self.color:
                cells.append((x, c))
                break
            else: break
        for c in range(y - 1, -1, -1):
            temp = a[x][c]
            if type(temp) == Empty:
                cells.append((x, c))
            elif temp.color != self.color:
                cells.append((x, c))
                break
            else: break
        for r in range(x + 1, 8):
            temp = a[r][y]
            if type(temp) == Empty:
                cells.append((r, y))
            elif temp.color != self.color:
                cells.append((r, y))
                break
            else: break
        for r in range(x - 1, -1, -1):
            temp = a[r][y]
            if type(temp) == Empty:
                cells.append((r, y))
            elif temp.color != self.color:
                cells.append((r, y))
                break
            else: break
        return cells

    def upd_moves(self):
        self.cells = copy.deepcopy(self.moves())

    def __str__(self):
        return f"{self.pos, self.color, self.cells}"

    def cmd(self):
        #print(self)
        game(self)

class King():
    def __init__(self, color, r, c):
        self.color = color
        self.image = PhotoImage(file = f"Figures/{color}_king.png")
        self.pos = (r, c)
        self.button = Button(window, image = self.image, bg = ["white", "green"][(r + c) % 2], height = 45, width = 45, command = self.cmd)
        self.button.grid(row = r + 1, column = c + 1)
        self.cells = []

    def moves(self):
        x, y = self.pos
        return [(i, j) for i in range(max(x - 1, 0), min(x + 1, 7) + 1) for j in range(max(y - 1, 0), min(y + 1, 7) + 1) if (i + j) and (type(a[i][j]) == Empty or a[i][j].color != self.color)]

    def upd_moves(self):
        self.cells = copy.deepcopy(self.moves())

    def __str__(self):
        return f"{self.pos, self.color, self.cells}"

    def cmd(self):
        #print(self)
        game(self)

class Queen():
    def __init__(self, color, r, c):
        self.color = color
        self.image = PhotoImage(file = f"Figures/{color}_queen.png")
        self.pos = (r, c)
        self.button = Button(window, image = self.image, bg = ["white", "green"][(r + c) % 2], height = 45, width = 45, command = self.cmd)
        self.button.grid(row = r + 1, column = c + 1)
        self.cells = []

    def moves(self):
        cells = []
        x, y = self.pos
        for c in range(y + 1, 8):
            temp = a[x][c]
            if type(temp) == Empty:
                cells.append((x, c))
            elif temp.color != self.color:
                cells.append((x, c))
                break
            else:
                break
        for c in range(y - 1, -1, -1):
            temp = a[x][c]
            if type(temp) == Empty:
                cells.append((x, c))
            elif temp.color != self.color:
                cells.append((x, c))
                break
            else:
                break
        for r in range(x + 1, 8):
            temp = a[r][y]
            if type(temp) == Empty:
                cells.append((r, y))
            elif temp.color != self.color:
                cells.append((r, y))
                break
            else:
                break
        for r in range(x - 1, -1, -1):
            temp = a[r][y]
            if type(temp) == Empty:
                cells.append((r, y))
            elif temp.color != self.color:
                cells.append((r, y))
                break
            else:
                break


        for i in range(1, 8):
            if x + i < 8 and y + i < 8:
                temp = a[x + i][y + i]
                if type(temp) == Empty:
                    cells.append((x + i, y + i))
                elif temp.color != self.color:
                    cells.append((x + i, y + i))
                    break
                else:
                    break
        for i in range(1, 8):
            if x - i >= 0 and y - i >= 0:
                temp = a[x - i][y - i]
                if type(temp) == Empty:
                    cells.append((x - i, y - i))
                elif temp.color != self.color:
                    cells.append((x - i, y - i))
                    break
                else:
                    break
        for i in range(1, 8):
            if x + i < 8 and y - i >= 0:
                temp = a[x + i][y - i]
                if type(temp) == Empty:
                    cells.append((x + i, y - i))
                elif temp.color != self.color:
                    cells.append((x + i, y - i))
                    break
                else:
                    break
        for i in range(1, 8):
            if x - i >= 0 and y + i < 8:
                temp = a[x - i][y + i]
                if type(temp) == Empty: cells.append((x - i, y + i))
                elif temp.color != self.color:
                    cells.append((x - i, y + i))
                    break
                else:
                    break

        return cells

    def upd_moves(self):
        self.cells = copy.deepcopy(self.moves())

    def __str__(self):
        return f"{self.pos, self.color, self.cells}"

    def cmd(self):
        #print(self)
        game(self)

class Bishop():
    def __init__(self, color, r, c):
        self.color = color
        self.image = PhotoImage(file = f"Figures/{color}_bishop.png")
        self.pos = (r, c)
        self.button = Button(window, image = self.image, bg = ["white", "green"][(r + c) % 2], height = 45, width = 45, command = self.cmd)
        self.button.grid(row = r + 1, column = c + 1)
        self.cells = []

    def moves(self):
        cells = []
        x, y = self.pos
        for i in range(1, 8):
            if x + i < 8 and y + i < 8:
                temp = a[x + i][y + i]
                if type(temp) == Empty:
                    cells.append((x + i, y + i))
                elif temp.color != self.color:
                    cells.append((x + i, y + i))
                    break
                else:
                    break
        for i in range(1, 8):
            if x - i >= 0 and y - i >= 0:
                temp = a[x - i][y - i]
                if type(temp) == Empty:
                    cells.append((x - i, y - i))
                elif temp.color != self.color:
                    cells.append((x - i, y - i))
                    break
                else:
                    break
        for i in range(1, 8):
            if x + i < 8 and y - i >= 0:
                temp = a[x + i][y - i]
                if type(temp) == Empty:
                    cells.append((x + i, y - i))
                elif temp.color != self.color:
                    cells.append((x + i, y - i))
                    break
                else:
                    break
        for i in range(1, 8):
            if x - i >= 0 and y + i < 8:
                temp = a[x - i][y + i]
                if type(temp) == Empty: cells.append((x - i, y + i))
                elif temp.color != self.color:
                    cells.append((x - i, y + i))
                    break
                else:
                    break

        return cells

    def upd_moves(self):
        self.cells = copy.deepcopy(self.moves())

    def __str__(self):
        return f"{self.pos, self.color, self.cells}"

    def cmd(self):
        #print(self)
        game(self)

class Knight():
    def __init__(self, color, r, c):
        self.color = color
        self.image = PhotoImage(file = f"Figures/{color}_knight.png")
        self.pos = (r, c)
        self.button = Button(window, image = self.image, bg = ["white", "green"][(r + c) % 2], height = 45, width = 45, command = self.cmd)
        self.button.grid(row = r + 1, column = c + 1)
        self.cells = []

    def moves(self):
        x, y = self.pos
        cells = [(x + i, y + j) for i in [-2, -1, 1, 2] for j in [-2, -1, 1, 2] if abs(i) + abs(j) == 3 and 0 <= x + i <= 7 and 0 <= y + j <= 7 and (type(a[x + i][y + j]) == Empty or a[x + i][y + j].color != self.color)]
        return cells

    def upd_moves(self):
        self.cells = copy.deepcopy(self.moves())

    def __str__(self):
        return f"{self.pos, self.color, self.cells}"

    def cmd(self):
        #print(self)
        game(self)

class Empty():
    def __init__(self, r, c):
        self.image = PhotoImage(file = f"Figures/dot.png")
        self.pos = (r, c)
        self.button = Button(window, image = self.image, bg = ["white", "green"][(r + c) % 2], height = 45, width = 45, command = self.cmd)
        self.button.grid(row = r + 1, column = c + 1)
        self.cells = []
        self.color = ""

    def upd_moves(self):
        self.cells = []

    def __str__(self):
        return f"{self.pos, self.cells}"

    def cmd(self):
        #print(self)
        game(self)

a = [[Pawn("black" if r == 1 else "white", r, c, first = True) if (r in [1, 6] and c != 3 and c != 4 and c != 0 and c != 7) else (Cross("black" if r == 1 else "white", r, c) if (r in [1, 6] and c in [0, 7]) else (Swoop("black" if r == 1 else "white", r, c) if (r in [1, 6] and c == 4) else (Trez("black" if r == 1 else "white", r, c) if (r in [1, 6] and c == 3) else (Empty(r, c) if r in [2, 3, 4, 5] else (King("black" if r == 0 else "white", r, c) if c in [4] else (Queen("black" if r == 0 else "white", r, c) if c in [3] else (Bishop("black" if r == 0 else "white", r, c) if c in [2, 5] else (Knight("black" if r == 0 else "white", r, c) if c in [1, 6] else Rook("black" if r == 0 else "white", r, c))))))))) for c in range(8)] for r in range(8)]

update_figs()
window.mainloop()
