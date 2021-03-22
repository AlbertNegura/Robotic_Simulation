"""
Robotic Simulation Software grid display.
Authors:
Albert Negura
Kamil Inglot
"""
import utils
import numpy as np
import itertools

class Square:
    lines = None
    left_line = None
    right_line = None
    top_line = None
    bottom_line = None
    position = None
    visited = False
    obstacle = False
    beacon = False
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


def get_cells_at_position_in_radius(grid, position, size, cleaning_range, clean_cells, beacons):
    """
    Get the dirty and clean cells around the robot.
    :param grid: the current grid as a 2d list
    :param position: the position of the robot
    :param size: the size of the dirt
    :param cleaning_range: the range at which to clean
    :param clean_cells: the current number of clean cells
    :return: the new number of clean cells, if any
    """
    center_x = int(position[0] / size)
    center_y = int(position[1] / size)

    xs = [center_x + i for i in range(-cleaning_range, cleaning_range + 1)]
    ys = [center_y + i for i in range(-cleaning_range, cleaning_range + 1)]

    if beacons:
        xs = np.clip(xs,0,len(grid[0])-1)
        ys = np.clip(ys,0,len(grid)-1)

    beacon_cells = []
    obstacle_cells = []
    clean_cells_list = [] # unused currently
    for x, y in itertools.product(xs, ys):
        if not beacons:
            if not grid[y][x].visited:
                clean_cells += 1
                grid[y][x].visited = True
        else:
            if grid[y][x].beacon:
                beacon_cells.append((x,y))
        if grid[y][x].obstacle:
            obstacle_cells.append(((y,x)))

    if not beacons:
        return clean_cells, clean_cells_list, obstacle_cells
    else:
        return beacon_cells, [center_x, center_y], obstacle_cells


def reset_grid(grid):
    """
    Resets grid visited positions creating dust everywhere
    :param grid: the grid to reset as a 2d list
    """
    rows = len(grid)
    columns = len(grid[0])
    for i,j in itertools.product(range(rows), range(columns)):
        grid[i][j].visited = False
        grid[i][j].obstacle = False
        grid[i][j].beacon = False
    return grid


def add_grid_obstacles(grid, walls, grid_size, width, height):
    # for each wall (two points), calculate all x,y positions between those points in the given resolution
    # set the square containing that obstacle to true grid[x][y].obstacle = True
    rows = len(grid)
    columns = len(grid[0])
    obstacle_cells = []
    non_obstacle_cells = []
    beacons = 0
    beacon_cells = []
    obstacles = 0
    for i,j in itertools.product(range(rows), range(columns)):
        for wall in walls:
            if (i+1)*grid_size < min(wall[0][1],wall[1][1]) or (j+1)*grid_size < min(wall[0][0],wall[1][0]) or (i-1)*grid_size > max(wall[0][1],wall[1][1]) or (j-1)*grid_size > max(wall[0][0],wall[1][0]):
                continue
            if not grid[i][j].obstacle:
                wall_line = np.array([wall[0], wall[1]])
                if utils.intersection(grid[i][j].left_line, wall_line) or utils.intersection(grid[i][j].right_line, wall_line) or utils.intersection(grid[i][j].top_line, wall_line) or utils.intersection(grid[i][j].bottom_line, wall_line):
                    if not grid[i][j].obstacle:
                        grid[i][j].obstacle = True
                        obstacles += 1
                        obstacle_cells.append((i,j))
                beacons_temp, beacon_cells_temp = quick_add_grid_beacons_wall(grid, wall, grid_size, width, height, rows, columns)
                beacons += beacons_temp
                beacon_cells.extend(beacon_cells_temp)
            else:
                break
        if not grid[i][j].obstacle:
            non_obstacle_cells.append((i,j))
    return obstacles, obstacle_cells, non_obstacle_cells, beacons, beacon_cells


def add_grid_beacons_wall(grid, walls, grid_size, width, height):
    # set the grid[x][y].beacon to true if that location is a beacon - note that it can be an obstacle!
    beacon_cells = []
    beacons = 0
    for wall in walls:
        if wall[0][0] <= 5 or wall[0][0] >= width or wall[0][1] <= 5 or wall[0][1] >= height - int(height/3) or wall[1][0] <= 5 or wall[1][0] >= width or wall[1][1] <= 5 or wall[1][1] >= height - int(height/3):
            continue

        wall_originx = int(wall[0][0] / grid_size)
        wall_originy = int(wall[0][1] / grid_size)
        wall_endx = int(wall[1][0] / grid_size)
        wall_endy = int(wall[1][1] / grid_size)

        if not grid[wall_endy][wall_endx].beacon:
            grid[wall_endy][wall_endx].beacon = True
            beacon_cells.append((wall_endy,wall_endx))
            beacons += 1
        if not grid[wall_originy][wall_originx].beacon:
            grid[wall_originy][wall_originx].beacon = True
            beacon_cells.append((wall_originy,wall_originx))
            beacons += 1
    return beacons, beacon_cells

def quick_add_grid_beacons_wall(grid, wall, grid_size, width, height, x_length, y_length):
    beacon_cells = []
    beacons = 0


    if wall[0][0] < 0 or wall[0][0] > width or wall[0][1] < 0 or wall[0][1] > height - int(height / 3) or wall[1][
        0] < 0 or wall[1][0] > width or wall[1][1] < 0 or wall[1][1] > height - int(height / 3):
        return beacons, beacon_cells
    wall_originx = np.clip(int(wall[0][0] / grid_size),0,y_length-1)
    wall_originy = np.clip(int(wall[0][1] / grid_size),0,x_length-1)
    wall_endx = np.clip(int(wall[1][0] / grid_size),0,y_length-1)
    wall_endy = np.clip(int(wall[1][1] / grid_size),0,x_length-1)

    if not grid[wall_endy][wall_endx].beacon:
        addx = 0 if wall_endx == y_length-1 else 1
        addy = 0 if wall_endy == x_length-1 else 1
        subx = 0 if wall_endx == 0 else -1
        suby = 0 if wall_endy == 0 else -1
        if not (grid[wall_endy+addy][wall_endx+addx].beacon or
                grid[wall_endy][wall_endx+addx].beacon or
                grid[wall_endy+addy][wall_endx].beacon or
                grid[wall_endy][wall_endx+subx].beacon or
                grid[wall_endy+addy][wall_endx+subx].beacon or
                grid[wall_endy+suby][wall_endx+subx].beacon or
                grid[wall_endy+suby][wall_endx+addx].beacon or
                grid[wall_endy+suby][wall_endx].beacon):

            grid[wall_endy][wall_endx].beacon = True
            beacon_cells.append((wall_endx, wall_endy))
            beacons += 1
    if not grid[wall_originy][wall_originx].beacon:
        addx = 0 if wall_originx == y_length-1 else 1
        addy = 0 if wall_originy == x_length-1 else 1
        subx = 0 if wall_originx == 0 else -1
        suby = 0 if wall_originy == 0 else -1
        if not (grid[wall_originy+addy][wall_originx+addx].beacon or
                grid[wall_originy][wall_originx+addx].beacon or
                grid[wall_originy+addy][wall_originx].beacon or
                grid[wall_originy][wall_originx+subx].beacon or
                grid[wall_originy+addy][wall_originx+subx].beacon or
                grid[wall_originy+suby][wall_originx+subx].beacon or
                grid[wall_originy+suby][wall_originx+addx].beacon or
                grid[wall_originy+suby][wall_originx].beacon):

            grid[wall_originy][wall_originx].beacon = True
            beacon_cells.append((wall_originx, wall_originy))
            beacons += 1

    return beacons, beacon_cells
