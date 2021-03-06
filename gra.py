import numpy as np
import pygame
import sys
import math


class Rules:
    ROW_COUNT = 0
    COLUMN_COUNT = 0
    """klasa bazowa dla innych regul, zawiera implementacje metod które są wspolne dla roznych zasad 
                    oraz funkcje wirtualne ktore implementowane są juz przez poszczegolne zasady """

    def __init__(self):
        """funkcja inicjalizująca planszę"""
        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))

    def is_free_space(self, column):
        """funkcja sprawdzajaca czy w danej kolumnie jest wolne miejsce"""
        return self.board[self.ROW_COUNT - 1][column] == 0

    def is_full(self):
        """funkcja sprawdzająca, czy tablica jest pełna"""
        for col in range(self.COLUMN_COUNT):
            if self.is_free_space(col):
                return False
        return True

    def who_won(self):
        """funkcja sprawdzajaca kto wygral"""
        if self.winning_move(1):
            return 1
        elif self.winning_move(2):
            return 2
        else:
            return 0

    def get_row_count(self):
        return self.ROW_COUNT

    def get_column_count(self):
        return self.COLUMN_COUNT

    def print_board(self):
        """funkcja potrzebna do prawidlowego wyświetlenia tablicy (potrzebna w wersji konsolowej)"""
        print(np.flip(self.board, 0))

    def drop_element(self, row, column, element):
        """funkcja zapełniająca wybrany element planszy"""
        self.board[row][column] = element

    def get_next_free_space(self, column):
        """funkcja zwracajaca wiersz w którym jest wolne miejsce (w danej kolumnie)"""
        for row in range(self.ROW_COUNT):
            if self.board[row][column] == 0:
                return row

    def winning_move(self, element):
        """funkcja wirtualna implementowana w zasadach"""
        pass

    def reset_board(self):
        """funkcja wirtualna implementowana w zasadach"""
        pass


class Classic(Rules):
    ROW_COUNT = 6
    COLUMN_COUNT = 7

    def winning_move(self, element):
        # horizontal
        for column in range(self.COLUMN_COUNT - 3):
            for row in range(self.ROW_COUNT):
                if self.board[row][column] == element and self.board[row][column + 1] == element and \
                        self.board[row][column + 2] == element and self.board[row][column + 3] == element:
                    return True

        # vertical
        for column in range(self.COLUMN_COUNT):
            for row in range(self.ROW_COUNT - 3):
                if self.board[row][column] == element and self.board[row + 1][column] == element and \
                        self.board[row + 2][column] == element and self.board[row + 3][column] == element:
                    return True

        # diagonal positive/negative
        for column in range(self.COLUMN_COUNT - 3):
            for row in range(self.ROW_COUNT - 3):
                if self.board[row][column] == element and self.board[row + 1][column + 1] == element and \
                        self.board[row + 2][column + 2] == element and self.board[row + 3][column + 3] == element:
                    return True

        for column in range(self.COLUMN_COUNT - 3):
            for row in range(3, self.ROW_COUNT):
                if self.board[row][column] == element and self.board[row - 1][column + 1] == element and \
                        self.board[row - 2][column + 2] == element and self.board[row - 3][column + 3] == element:
                    return True

    def reset_board(self):
        for row in range(self.ROW_COUNT):
            for column in range(self.COLUMN_COUNT):
                self.board[row][column] = 0


class FiveInRow(Rules):
    ROW_COUNT = 6
    COLUMN_COUNT = 9

    def __init__(self):
        super().__init__()
        for row in range(self.ROW_COUNT):
            if row % 2 == 0:
                self.board[row][0] = 1
                self.board[row][self.COLUMN_COUNT - 1] = 2
            else:
                self.board[row][0] = 2
                self.board[row][self.COLUMN_COUNT - 1] = 1

    def winning_move(self, element):
        """Five In Row polega na tym że mamy dwie dodatkowe kolumny, ale te skrajne są już zapełnione na zmianę
        żetonami graczy, wygrywa ten które pierwszy ustawi 5 w rzędzie"""
        # horizontal
        for column in range(self.COLUMN_COUNT - 4):
            for row in range(self.ROW_COUNT):
                if self.board[row][column] == element and self.board[row][column + 1] == element and \
                        self.board[row][column + 2] == element and self.board[row][column + 3] == element and\
                        self.board[row][column + 4] == element:
                    return True

        # vertical
        for column in range(self.COLUMN_COUNT):
            for row in range(self.ROW_COUNT - 4):
                if self.board[row][column] == element and self.board[row + 1][column] == element and \
                        self.board[row + 2][column] == element and self.board[row + 3][column] == element and \
                        self.board[row + 4][column] == element:
                    return True

        # diagonal positive/negative
        for column in range(self.COLUMN_COUNT - 4):
            for row in range(self.ROW_COUNT - 4):
                if self.board[row][column] == element and self.board[row + 1][column + 1] == element and \
                        self.board[row + 2][column + 2] == element and self.board[row + 3][column + 3] == element and\
                        self.board[row + 4][column + 4] == element:
                    return True

        for column in range(self.COLUMN_COUNT-4):
            for row in range(4, self.ROW_COUNT):
                if self.board[row][column] == element and self.board[row - 1][column + 1] == element and \
                        self.board[row - 2][column + 2] == element and self.board[row - 3][column + 3] == element and \
                        self.board[row - 4][column + 4] == element:
                    return True

    def reset_board(self):
        """Skrajne kolumny wypełnione jak w definicji reguły"""
        for row in range(self.ROW_COUNT):
            if row % 2 == 0:
                self.board[row][0] = 1
                self.board[row][self.COLUMN_COUNT - 1] = 2
            else:
                self.board[row][0] = 2
                self.board[row][self.COLUMN_COUNT - 1] = 1

        for row in range(self.ROW_COUNT):
            for col in range(1, self.COLUMN_COUNT-1):
                self.board[row][col] = 0


class Game:
    SQUARE_SIZE = 75
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)

    def __init__(self):
        ############################################## Fragment odpowiedzialny za graficzny wybór zasad gry.
        pygame.init()
        self.screen = pygame.display.set_mode((350, 350))
        self.myfont = pygame.font.SysFont("monospace", 20)
        wybor = True
        while wybor:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.YELLOW, (0, 0, 175, 350))
                    pygame.draw.rect(self.screen, self.RED, (175, 0, 175, 350))
                    label = self.myfont.render("Classic", 1, self.RED)
                    label2 = self.myfont.render("Five In Row", 1, self.YELLOW)
                    self.screen.blit(label, (40, 10))
                    self.screen.blit(label2, (190, 10))
                    posx, posy = event.pos
                    pygame.draw.circle(self.screen, self.BLUE, (posx, posy), 10)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if posx < 175:
                        self.rule = Classic()
                    else:
                        self.rule = FiveInRow()
                    wybor = False
##################################################################################################

        # Config
        self.width = self.rule.get_column_count() * self.SQUARE_SIZE
        self.height = (self.rule.get_row_count()+1) * self.SQUARE_SIZE
        self.radius = int(self.SQUARE_SIZE/2 - 5)
        self.game_over = False
        self.turn = 0

        # Init
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.myfont = pygame.font.SysFont("monospace", 50)

        self.gra()

    def gra(self):
        """W nieskończonej pętli rysujemy plansze i obsługujem zdarzenia"""
        while 1:
            self.draw()
            self.obsluga_zdarzenia()

    def draw(self):
        """funkcja rysująca planszę na podstawie zasay gry"""
        for c in range(self.rule.COLUMN_COUNT):
            for r in range(self.rule.ROW_COUNT):
                pygame.draw.rect(self.screen, self.BLUE,
                                 (c * self.SQUARE_SIZE, r * self.SQUARE_SIZE + self.SQUARE_SIZE,
                                  self.SQUARE_SIZE, self.SQUARE_SIZE))
                pygame.draw.circle(self.screen, self.BLACK, (
                    int(c * self.SQUARE_SIZE + self.SQUARE_SIZE / 2),
                    int(r * self.SQUARE_SIZE + self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.radius)

        for c in range(self.rule.COLUMN_COUNT):
            for r in range(self.rule.ROW_COUNT):
                if self.rule.board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.RED, (
                        int(c * self.SQUARE_SIZE + self.SQUARE_SIZE / 2),
                        self.height - int(r * self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.radius)
                elif self.rule.board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.YELLOW, (
                        int(c * self.SQUARE_SIZE + self.SQUARE_SIZE / 2),
                        self.height - int(r * self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.radius)
        pygame.display.update()

    def obsluga_zdarzenia(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            #Przycis R zresetuje grę w dowolnym momencie
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_r]:
                self.rule.reset_board()

            #Ruch żetonem wraz z ruchem myszki (zaznaczanie kolumny)
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SQUARE_SIZE))
                posx = event.pos[0]
                if self.turn == 0:
                    pygame.draw.circle(self.screen, self.RED, (posx, int(self.SQUARE_SIZE / 2)), self.radius)
                else:
                    pygame.draw.circle(self.screen, self.YELLOW, (posx, int(self.SQUARE_SIZE / 2)), self.radius)
            pygame.display.update()

            # Wciśnięcie klawisza myszy wrzuci żeton na odpowiednie miejsce
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SQUARE_SIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if self.turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / self.SQUARE_SIZE))

                    if self.rule.is_free_space(col):
                        row = self.rule.get_next_free_space(col)
                        self.rule.drop_element(row, col, 1)
                    else:
                        self.wypisz_wiadomosc("Blad",False)
                        pygame.display.update()
                        pygame.time.wait(1500)
                        continue

                    if self.rule.who_won() == 1:
                        self.wypisz_wiadomosc("Player 1 won!",True)

                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / self.SQUARE_SIZE))

                    if self.rule.is_free_space(col):
                        row = self.rule.get_next_free_space(col)
                        self.rule.drop_element(row, col, 2)
                    else:
                        self.wypisz_wiadomosc("Blad",False)
                        pygame.display.update()
                        pygame.time.wait(1500)
                        continue

                    if self.rule.who_won() == 2:
                        self.wypisz_wiadomosc("Player 2 won!",True)

                if self.rule.who_won() == 0 and self.rule.is_full():
                    self.wypisz_wiadomosc("Remis",True)

                # self.rule.print_board()
                self.draw()

                self.turn += 1
                self.turn = self.turn % 2

                if self.game_over: # jeśli gra się skończy, program odczeka 3s i zresetuje grę
                    pygame.time.wait(3000)
                    self.rule.reset_board()
                    self.draw()
                    self.game_over = False

    def wypisz_wiadomosc(self, arg, game_over):
        label = self.myfont.render(arg, 1, self.WHITE)
        self.screen.blit(label, (40, 10))
        self.game_over = game_over

Game()
