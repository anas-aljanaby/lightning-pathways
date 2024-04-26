import unittest
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )


    def test_maze_entry_exit(self):
        m = Maze(350, 100, 12, 10, 25,25)
        self.assertEqual(False, m._cells[-1][-1].has_bottom_wall)
        self.assertEqual(False, m._cells[0][0].has_top_wall)


    def test_reset_cells_visited(self):
        m = Maze(350, 100, 12, 10, 25,25, seed=3)
        for i in range(m.num_cols):
            for j in range(m.num_rows):
                self.assertEqual(False,
                                 m._cells[i][j].visited)



if __name__ == "__main__":
    unittest.main()

