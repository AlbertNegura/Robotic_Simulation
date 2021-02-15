class Square:
    lines = None
    left_line = None
    right_line = None
    top_line = None
    bottom_line = None
    position = None
    row = -1
    column = -1

    def add_lines(self):
        self.position = [self.left_line[0][0],self.left_line[0][1]]
        self.lines.append(self.left_line)
        self.lines.append(self.top_line)
        self.lines.append(self.right_line)
        self.lines.append(self.bottom_line)

def create_square(position, side):
    square = Square()
    square.size = side
    square.lines = []

    left_top = position
    right_top = [left_top[0] + side, left_top[1]]
    left_bottom = [left_top[0], left_top[1] + side]
    right_bottom = [left_top[0] + side, left_top[1] + side]

    square.left_line = [left_top,left_bottom]
    square.top_line = [left_top,right_top]
    square.right_line = [right_top,right_bottom]
    square.bottom_line = [right_bottom,left_bottom]

    square.add_lines()

    return square


def create_grid(square_size, width, height):
    grid = []
    complete = False
    y = 0
    row_cnt = 0
    while not complete:
        row_full = False
        x = 0
        squares = []
        col_cnt = 0
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