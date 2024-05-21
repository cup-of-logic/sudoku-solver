import pygame
import numpy as np


class SudokuAutoSolver:
    def __init__(self):
        self.board = np.zeros(shape=(9, 9), dtype=np.int16)

        self.WIDTH, self.HEIGHT = 450, 525
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.init()

        self.solved = 0
        self.cell_size = self.WIDTH // 9
        self.active = None

        # COLORS
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (128, 128, 128)
        self.DARK_GREY = (50, 50, 50)
        self.GREEN = (0, 255, 0)
        self.DARK_GREEN = (0, 200, 0)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)

        self.main()

    def check_row(self, row, num):
        for i in self.board[row]:
            if i == num:
                return True
        return False

    def check_col(self, col, num):
        for i in range(len(self.board)):
            if self.board[i][col] == num:
                return True
        return False

    def check_box(self, row, col, num):
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(start_row, start_row+3):
            for j in range(start_col, start_col+3):
                if self.board[i][j] == num:
                    return True
        return False

    def check_valid(self, row, col, num):
        return not self.check_row(row, num) and not self.check_col(col, num) and not self.check_box(row, col, num)

    def solve(self):
        for col in range(len(self.board)):
            for row in range(len(self.board)):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.check_valid(row, col, num):
                            self.board[row][col] = num
                            self.update()
                            if self.solve():
                                return True
                            else:
                                self.board[row][col] = 0
                                self.update()
                    return False
        return True

    def create_grid(self, size, color):
        for x in range(0, self.WIDTH, size):
            pygame.draw.line(self.window, color, (x, 0), (x, self.WIDTH))
        for y in range(0, self.WIDTH, size):
            pygame.draw.line(self.window, color, (0, y), (self.WIDTH, y))
        pygame.draw.line(self.window, color, (0, self.WIDTH), (self.WIDTH, self.WIDTH))

        if self.active:
            x, y = self.active
            x, y = x * self.cell_size, y * self.cell_size
            pygame.draw.line(self.window, self.BLUE, (y, x), (y+self.cell_size, x))
            pygame.draw.line(self.window, self.BLUE, (y, x), (y, x+self.cell_size))
            pygame.draw.line(self.window, self.BLUE, (y+self.cell_size, x), (y+self.cell_size, x+self.cell_size))
            pygame.draw.line(self.window, self.BLUE, (y, x+self.cell_size), (y+self.cell_size, x+self.cell_size))

    def create_grids(self):
        self.create_grid(self.cell_size, self.GREY)
        self.create_grid(self.WIDTH//3, self.BLACK)

    def add_text(self, text, color, size, x, y):
        font = pygame.font.SysFont(None, size)
        screen_text = font.render(text, True, color)
        self.window.blit(screen_text, [x, y])

    def set_numbers(self):
        font_size = int(0.8 * self.cell_size)

        for row in range(len(self.board)):
            for col in range(len(self.board)):
                text = str(self.board[row][col]) if self.board[row][col] else ' '
                self.add_text(text=text, color=self.DARK_GREY, size=font_size, x=row*self.cell_size+(self.cell_size//3), y=col*self.cell_size+(self.cell_size//3))

    def get_grid(self, coord):
        x, y = coord
        grid = (y // self.cell_size, x // self.cell_size)
        return grid

    def update(self):
        self.window.fill(self.WHITE)
        self.create_grids()
        self.set_numbers()
        if self.solved == 1:
            self.add_text(text="Board Solved", color=self.GREEN, size=30, x=160, y=480)
        elif self.solved == -1:
            self.add_text(text="Board Not Solvable!", color=self.RED, size=30, x=130, y=480)
        pygame.display.update()

    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and event.pos[0] <= self.WIDTH and event.pos[1] <= self.WIDTH:
                        self.active = self.get_grid(event.pos)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.active = None
                        if self.solve():
                            self.solved = 1
                        else:
                            self.solved = -1
                    if self.active:
                        if 48 <= event.key <= 57:
                            self.board[self.active[1]][self.active[0]] = int(chr(event.key))
            self.update()


if __name__ == '__main__':
    board = [
        [1, 0, 0,   4, 8, 9,   0, 0, 6],
        [7, 3, 0,   0, 0, 0,   0, 4, 0],
        [0, 0, 0,   0, 0, 1,   2, 9, 5],

        [0, 0, 7,   1, 2, 0,   6, 0, 0],
        [5, 0, 0,   7, 0, 3,   0, 0, 8],
        [0, 0, 6,   0, 9, 5,   7, 0, 0],

        [9, 1, 4,   6, 0, 0,   0, 0, 0],
        [0, 2, 0,   0, 0, 0,   0, 3, 7],
        [8, 0, 0,   5, 1, 2,   0, 0, 4]
    ]

    SudokuAutoSolver()
