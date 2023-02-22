from GameControl import *

# Importation de la class GameControl
game = GameControl()

# Définition des couleurs
BLUE = (110, 114, 249)
BLACK = (0, 0, 0)
RED = (249, 110, 110)
GREY = (100, 121, 142)
BLACK_GREY = (88, 106, 124)

# Ressources
logo = pygame.transform.scale(pygame.image.load("assets/img/logo.png"), (400,140))
pseudo_entry = pygame.transform.scale(pygame.image.load("assets/img/pseudo_entry.png"), (375,110))
select = pygame.transform.scale(pygame.image.load("assets/img/select.png"), (375,110))

if game.menu:

    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Démineur")

    game.screen = screen

    menu_active = True
    while menu_active:

        screen.fill((100, 121, 142))

        screen.blit(logo, (500 / 2 - 200, 15))

        game.displayText("Tapez votre pseudo :", 500/2-86, 150, 20, "HELVETICA", BLACK)
        screen.blit(pseudo_entry, (500 / 2 - 375 / 2, 160))

        game.displayText(game.listToSTR(game.pseudo), 500 / 2, 220, 60, "MILITARY", BLACK)

        coords_btn_l, coords_btn_r = [(60,120),(275, 360)], [(390,440),(275,360)]
        coords_btn_l_2, coords_btn_r_2 = [(60,120),(275+100, 360+100)], [(390,440),(275+100,360+100)]

        screen.blit(select, (500 / 2 - 372/2, 260))
        screen.blit(select, (500 / 2 - 372/2, 360))


        mines = str(game.NUM_MINES) + " MINES"
        game.displayText(mines, 500 / 2, 325, 50, "MILITARY", BLACK)

        taille = str(game.NUM_COLS) + " TAILLE"
        game.displayText(taille, 500 / 2, 425, 50, "MILITARY", BLACK)

        game.displayText("Appuyez sur ESPACE pour continuer...", 180, 485, 20, "HELVETICA", BLACK)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    game.pseudo = game.pseudo[:-1]
                elif event.key == pygame.K_SPACE:

                    menu_active = False
                    game.goToGame()

                else:
                    if len(game.pseudo) < 9:
                        game.pseudo += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Choix du nombre de mines
                if game.mouseClick(pos, coords_btn_l):
                    if game.NUM_MINES > 1:
                        game.NUM_MINES -= 1

                elif game.mouseClick(pos, coords_btn_r):
                    if game.NUM_MINES < 40:
                        game.NUM_MINES += 1

                # Choix de la taille
                elif game.mouseClick(pos, coords_btn_l_2):
                    if game.NUM_COLS > 5:
                        game.NUM_COLS -= 1
                        game.NUM_ROWS -= 1

                elif game.mouseClick(pos, coords_btn_r_2):
                    if game.NUM_COLS < 25:
                        game.NUM_COLS += 1
                        game.NUM_ROWS += 1


def drawBoard(board):
    for x in range(game.NUM_COLS):
        for y in range(game.NUM_ROWS):
            rect = pygame.Rect(x * game.BLOCK_SIZE, y * game.BLOCK_SIZE, game.BLOCK_SIZE, game.BLOCK_SIZE)

            if game.colors[y][x] == 1:
                color = GREY
            elif game.colors[y][x] == 2:
                color = BLUE
            elif game.colors[y][x] == 3:
                color = BLACK_GREY


            pygame.draw.rect(screen, color, rect)
            if board[y][x] > 0 and board[y][x] != -2 and game.colors[y][x] == 3:
                text = str(board[y][x])
                font = pygame.font.Font('assets/fonts/freesansbold.ttf', 20)
                text_surface = font.render(text, True, BLACK)
                screen.blit(text_surface, (x * game.BLOCK_SIZE + 10, y * game.BLOCK_SIZE + 10))


# LANCEMENT DU JEU

game.board = game.generateBoard()
game.displayArray()
pygame.init()
screen = pygame.display.set_mode((game.NUM_COLS*game.BLOCK_SIZE, game.NUM_ROWS*game.BLOCK_SIZE))

game.screen = screen

game_active = True
while game_active:

    screen.fill((100, 121, 142))

    if game.step == "JEU":

        if game.time_start == 0:
            game.time_start = time.time()

        pygame.display.set_caption(str("Temps écoulé : ") + str(round(time.time()-game.time_start, 2)) + str("s"))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                x = int(m_x / game.BLOCK_SIZE)
                y = int(m_y / game.BLOCK_SIZE)
                game.interClick(x, y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.step = "GAGNE"

        drawBoard(game.board)
        pygame.display.update()

    elif game.step == "PERDU":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        game.displayText("Dommage, vous avez perdu...", 200, 200, 20, "HELVETICA", BLACK)

        pygame.display.update()

    elif game.step == "GAGNE":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.step = "SCORE"

        game.displayText("Bravo vous avez gagné!", 200, 200, 20, "HELVETICA", BLACK)

        game.displayText(str(game.time) + " secondes", 200, 250, 20, "HELVETICA", BLACK)

        game.displayText("Appuyez sur ESPACE pour afficher les meilleurs joueurs...", (game.BLOCK_SIZE*game.NUM_ROWS)/2, game.BLOCK_SIZE*game.NUM_ROWS-20, 15, "HELVETICA", BLACK)



        pygame.display.update()

    elif game.step == "SCORE":

        pygame.init()
        screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Démineur - Meilleurs joueurs")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill((100, 121, 142))

        game.displayText("Meilleurs joueurs :", 250, 20, 20, "HELVETICA", BLACK)

        game.displayText("Pseudo          Mines          Taille          Temps", 250, 75, 20, "HELVETICA", BLACK)

        game.displayCsv()

        pygame.display.update()




