import random
import time
import pygame
import csv

class GameControl:

    def __init__(self):

        self.menu = True
        self.board = None
        self.colors = None
        self.screen = None
        self.pseudo = []
        self.step = "JEU"
        self.flags = 0
        self.mines_total = 0

        self.time_start = 0
        self.time = 0

        # Variables
        self.NUM_ROWS = 10
        self.NUM_COLS = 10
        self.BLOCK_SIZE = 40
        self.NUM_MINES = 10

    def interClick(self, x, y):
        m_x, m_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.board[y][x] >= 0:
            self.reveal_tiles(x, y)

        elif pygame.mouse.get_pressed()[2] and self.board[y][x] != -2:
            if self.colors[y][x] == 2:
                self.colors[y][x] = 1
                if self.board[y][x] == -1:
                    self.flags -= 1
            else:
                self.colors[y][x] = 2
                if self.board[y][x] == -1:
                    self.flags += 1

        elif pygame.mouse.get_pressed()[0] and self.board[y][x] == -1:
            self.step = "PERDU"

        if self.verifWin():
            self.step = "WIN"


    def reveal_tiles(self, x, y):
        if x < 0 or x > self.NUM_COLS - 1 or y < 0 or y > self.NUM_ROWS - 1:
            return

        if self.colors[y][x] == 1 and self.board[y][x] == 0:
            self.colors[y][x] = 3
            self.reveal_tiles(x + 1, y)
            self.reveal_tiles(x - 1, y)
            self.reveal_tiles(x, y + 1)
            self.reveal_tiles(x, y - 1)
            self.reveal_tiles(x + 1, y + 1)
            self.reveal_tiles(x + 1, y - 1)
            self.reveal_tiles(x - 1, y + 1)
            self.reveal_tiles(x - 1, y - 1)

        else:
            self.colors[y][x] = 3

    def listToSTR(self, L):
        text = ""
        for i in range(len(L)):
            text += L[i]

        return text


    def displayText(self, texte, x, y, size, font, color):
        if font == "MILITARY":
            font = pygame.font.Font('assets/fonts/MILITARY.TTF', size)
        elif font == "HELVETICA":
            font = pygame.font.Font('assets/fonts/HELVETICA.TTF', size)
        text_display = font.render(texte, True, color)
        text_rect = text_display.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_display, text_rect)

    def goToGame(self):
        if self.pseudo == []:
            self.pseudo = "UNKNOWN"

        self.menu = False

    def mouseClick(self, mouse_pos, image_coord):
        return mouse_pos[0] > image_coord[0][0] and mouse_pos[0] < image_coord[0][1] and mouse_pos[1] > image_coord[1][0] and mouse_pos[1] < image_coord[1][1]

    def generateBoard(self):
        board = [[0 for x in range(self.NUM_COLS)] for y in range(self.NUM_ROWS)]

        self.colors = [[1 for x in range(self.NUM_COLS)] for y in range(self.NUM_ROWS)]

        # Placement aléatoire des mines
        for i in range(self.NUM_MINES):
            x = random.randint(0, self.NUM_COLS - 1)
            y = random.randint(0, self.NUM_ROWS - 1)
            while board[y][x] == -1:
                x = random.randint(0, self.NUM_COLS - 1)
                y = random.randint(0, self.NUM_ROWS - 1)
            board[y][x] = -1
        # Comptage des mines adjacentes
        for y in range(self.NUM_ROWS):
            for x in range(self.NUM_COLS):
                if board[y][x] != -1:
                    count = 0
                    for i in range(y - 1, y + 2):
                        for j in range(x - 1, x + 2):
                            if 0 <= i < self.NUM_ROWS and 0 <= j < self.NUM_COLS:
                                if board[i][j] == -1:
                                    count += 1
                    board[y][x] = count

        self.board = board
        return board

    def displayArray(self):
        for i in range(len(self.board)):
            print(self.board[i])

    def verifWin(self):
        if self.flags >= self.NUM_MINES:

            if self.time == 0:

                self.time = round(time.time() - self.time_start, 2)
                self.step = "GAGNE"

                self.sendScore(self.time)


    def sendScore(self, time):

        data = [self.listToSTR(self.pseudo), time, self.NUM_COLS, self.NUM_MINES]

        with open('leaderboard.csv', 'a', newline='') as file:
            writer_object = csv.writer(file)
            writer_object.writerow(data)

            file.close()

    def displayCsv(self):

        with open('leaderboard.csv', newline='') as file:
            read_object = csv.reader(file, delimiter=',')

            lignes = list(read_object)

        L = self.sortScore(lignes[1:])

        if len(L) > 10:
            R = 10
        else:
            R = len(L)


        for i in range (R):
            c = str(L[i][0]) + "            " + str(L[i][3]) + "            " + str(L[i][2]) + "            " + str(L[i][1])
            self.displayText(c, 250, 150+i*40, 20, "HELVETICA", (0,0,0))


    def sortScore(self, L):
        L2 = []
        while L:
            max = L[0][3]
            compteur = 0
            for i in range(len(L)):
                if L[i][3] > max:
                    min = L[i][3]
                    compteur = i
            L2.append(L[compteur])
            del L[compteur]

        return L2



