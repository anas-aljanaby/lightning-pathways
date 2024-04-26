import time
import random
from cells import Cell

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None, sleep=0.05):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self.sleep = sleep 
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self.num_cols):
            col_cells = []
            for j in range(self.num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)    

    def _draw_cell(self, i, j):
        if self._win is None:
            return 
        x1 = self.x1 + self.cell_size_x * i 
        y1 = self.y1 + self.cell_size_y * j 
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()


    def _animate(self):
        if self._win:
            self._win.redraw()
        time.sleep(self.sleep)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self._draw_cell(self.num_cols-1, self.num_rows-1)

    def get_neighbors(self, i, j):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for di, dj in directions:
            ni, nj = i + di, j +dj
            if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows:
                if not self._cells[ni][nj].visited:
                    neighbors.append((ni, nj))
        return neighbors

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1, j))
            if i < self.num_cols - 1 and not self._cells[i+1][j].visited:
                to_visit.append((i+1, j))
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append((i, j-1))
            if j < self.num_rows - 1 and not self._cells[i][j+1].visited:
                to_visit.append((i, j+1))

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            direction_index = random.randrange(len(to_visit))
            next_index = to_visit[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False


    def solve(self):
        return self._solve_r(0, 0)
       
    def get_valid_directions(self, i, j):
        directions = []
        if i > 0 and not self._cells[i-1][j].visited and not self._cells[i][j].has_left_wall:
            directions.append((i-1, j))
         
        if i < self.num_cols - 1 and not self._cells[i+1][j].visited and not self._cells[i][j].has_right_wall:
            directions.append((i+1, j))
        
        if j > 0 and not self._cells[i][j-1].visited and not self._cells[i][j].has_top_wall:
            directions.append((i, j-1))

        if j < self.num_rows - 1 and not self._cells[i][j+1].visited and not self._cells[i][j].has_bottom_wall:
            directions.append((i, j+1))
        return directions


    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i==self.num_cols - 1 and j==self.num_rows - 1:
            return True
        
        for new_i, new_j in self.get_valid_directions(i, j):
            self._cells[i][j].draw_move(self._cells[new_i][new_j])
            if self._solve_r(new_i, new_j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[new_i][new_j], undo=True)
                     
        return False





