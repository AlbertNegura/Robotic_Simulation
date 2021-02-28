"""
Robotic Simulation Software grid display.
Authors:
Albert Negura
"""


class Square:
    lines = None
    left_line = None
    right_line = None
    top_line = None
    bottom_line = None
    position = None
    visited = False
    row = -1
    column = -1

    def add_lines(self):
        """
        Define a square as its 4 lines.
        :return:
        """
        self.position = [self.left_line[0][0], self.left_line[0][1]]
        self.lines.append(self.left_line)
        self.lines.append(self.top_line)
        self.lines.append(self.right_line)
        self.lines.append(self.bottom_line)


def create_square(position, side):
    """
    Create square objects at a position with a given side length.
    :param position: position of the square as the top left points
    :param side: the size of the side of the square
    :return: the created square
    """
    square = Square()
    square.size = side
    square.lines = []

    left_top = position
    right_top = [left_top[0] + side, left_top[1]]
    left_bottom = [left_top[0], left_top[1] + side]
    right_bottom = [left_top[0] + side, left_top[1] + side]

    square.left_line = [left_top, left_bottom]
    square.top_line = [left_top, right_top]
    square.right_line = [right_top, right_bottom]
    square.bottom_line = [right_bottom, left_bottom]

    square.add_lines()

    return square


def create_grid(square_size, width, height):
    """
    Creates a grid of squares
    :param square_size: the side length of the squares
    :param width: the width of the grid
    :param height: the height of the grid
    :return: a complete grid as a 2d list, with the squares spread out over it as evenly as possible
    """
    grid = []
    complete = False
    y = 0
    row_cnt = 0
    # until the grid is complete, go over each x-y coordinate pair and create a new square
    while not complete:
        row_full = False
        x = 0
        squares = []
        col_cnt = 0
        # rows first, then columns
        while not row_full:
            new_square = create_square([x, y], square_size)
            new_square.row = row_cnt
            new_square.column = col_cnt
            squares.append(new_square)
            x += square_size
            col_cnt += 1
            if x >= width:
                row_full = True
        grid.append(squares)
        y += square_size
        row_cnt += 1
        if y >= height:
            complete = True
    return grid


def get_cells_at_position_in_radius(grid, position, size, cleaning_range, clean_cells):
    center_x = int(position[0] / size)
    center_y = int(position[1] / size)
    xs = [center_x + i for i in range(-cleaning_range, cleaning_range + 1)]
    ys = [center_y + i for i in range(-cleaning_range, cleaning_range + 1)]
    for x in xs:
        for y in ys:
            if not grid[y][x].visited:
                clean_cells += 1
                grid[y][x].visited = True
    return clean_cells


def reset_grid(grid):
    """
    resets grid visited positions creating dust everywhere
    Authors:
    Kamil Inglot
    """
    rows = len(grid)
    columns = len(grid[0])
    for i in range(rows):
        for j in range(columns):
            grid[i][j].visited = False
    return grid

