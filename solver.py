class Solver:
    def __init__(self, board):
        self.board = board
        if self.solve():
            print("Board Solved")
            for i in self.board:
                print(i)
        else:
            print("Board Cannot be solved")

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
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.check_valid(row, col, num):
                            self.board[row][col] = num
                            if self.solve():
                                return True
                            else:
                                self.board[row][col] = 0
                    return False
        return True


if __name__ == '__main__':
    board = [
        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],

        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],

        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0],
        [0, 0, 0,   0, 0, 0,   0, 0, 0]
    ]

    Solver(board=board)
