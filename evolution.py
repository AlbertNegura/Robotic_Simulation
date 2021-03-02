from config import *
import numpy as np
import fitness
import robotics
import neuralnetwork
import grid

# sensors * hidden nodes because fully connected input + hidden layer
# hidden nodes * 2 because each hidden node is fully connected to output
# IF RNN, hidden -> hidden so hidden nodes * hidden nodes
# output has exactly 2 nodes - Vl and Vr
# if not RNN
# total weights for 12 sensors and 4 hidden nodes = 12*4 + 4*2 = 56
# if RNN
# total weights for 12 sensors and 4 hidden nodes = 12*4 + 4*4 + 4*2 = 56

class Genome:
    genome_size =  SENSORS*HIDDEN_NODES+HIDDEN_NODES*HIDDEN_NODES + HIDDEN_NODES*2 if RNN else SENSORS*HIDDEN_NODES+HIDDEN_NODES*2 if HIDDEN_NODES > 0 else SENSORS * 2
    genome = None
    robot = None
    grid = None
    fitness = None


    def __init__(self, robot, grid, weights):
        size = len(weights)
        assert size >= self.genome_size, "Expected {} weights, got {} instead".format(self.genome_size,size)
        self.robot = robot
        self.grid = grid
        self.genome = np.random.randint(0, 1, self.genome_size)

        for i in range(size):
            self.genome[i] = weights[i]


    def evaluate(self, cells_covered, num_collisions):
        self.fitness = fitness.fitness(cells_covered, num_collisions, 0)
        return self.fitness



class Evolution:


    def __init__(self, this_grid):
        self.population = POPULATION
        self.iterations = ITERATIONS * TICK_RATE
        self.generations = LIFESPAN
        self.nn = [neuralnetwork.RNN(np.random.uniform(0, SENSOR_LENGTH, SENSORS), np.array([0,0]), SENSORS, HIDDEN_NODES, 2) for _ in range(self.population)]
        self.weights = [nn.weight_vector() for nn in self.nn]
        self.map = [this_grid.copy() for _ in range(self.population)]
        self.robots = [robotics.create_robot(init_pos=(WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)), radius=RADIUS, acceleration=ACCELERATION, num_sensors=SENSORS, max_radius=SENSOR_LENGTH) for _ in range(self.population)]
        self.genome_list = [Genome(self.robots[i], self.map[i], self.weights[i]) for i in range(self.population)]
        self.fitnesses = []


    def evolve(self):
        """
         Note that the "robot" parameter defined in config.py is
         the base class used to initialize the "robot_sim" and
         therefore remains unchanged.
        """
        for i in range(self.generations):
            fitness_list = []
            for i in range(self.population):
                total_area, collision_number, sensor_values = self.step(self.genome_list[i], self.map[i], self.nn[i])
                fitness_list.append(fitness.fitness(total_area, collision_number, sensor_values))
            self.fitnesses.append(fitness_list)

            # TODO: Do EA with fitness_list and update individuals_list

    def step(self, genome, map, nn):
        """
        :returns: fitness_parameters to be used in the fitness function
        """
        total_area = []
        collision_number = 0
        sensor_values = []
        robot = genome.robot
        # TODO: use passed map parameter
        for cycle in range(self.iterations):
            # move robot
            rnn_output = nn.feedforward(robot.sensor_values())
            decode_output(rnn_output, robot)
            robot.move(WALLS)
            robot.adjust_sensors(WALLS)
            robot.adjust_sensors(EDGE_WALLS)
            # TODO: calculate total_area, collision_number, sensor_values

        return total_area, collision_number, sensor_values


"""
PIPELINE
1) Initialization:
    - Robot: position, sensors, wheels, ..
    - POPULATION: 80 individuals (Individual = RNN weight configuration)
    - Maze: Walls, grid, ..
2) Foreach individual do Robot simulation. 80 cycles (24s), 0.3 s/cycle
    - ANN Cycle (control robot every 0.3s): sensor values -> RNN -> wheel velocities
    - Simulation output:
        - number of grid cells covered (area explored)
        - number of collisions
        - average sensor values?
3) Fitness value foreach individual
4) EA: Selection + Crossover & Mutation
5) Reproduction of new individuals 
6) Go back to step 2
"""

# Substitutes gui.accelerate()
def decode_output(rnn_output, robot_sim):
    # rnn_output[0] -> Vl
    if rnn_output[0] == 1:
        robot_sim.velocity_left += ACCELERATION*FORWARD
    elif rnn_output[0] == 0.5:
        robot_sim.velocity_left = STOP
    elif rnn_output[0] == 0:
        robot_sim.velocity_left += ACCELERATION*BACKWARD
    # rnn_output[1] -> Vr
    if rnn_output[1] == 1:
        robot_sim.velocity_right += ACCELERATION*FORWARD
    elif rnn_output[1] == 0.5:
        robot_sim.velocity_right = STOP
    elif rnn_output[1] == 0:
        robot_sim.velocity_right += ACCELERATION*BACKWARD


if __name__ == "__main__":
    this_grid = grid.create_grid(GRID_SIZE, WIDTH, HEIGHT)
    e = Evolution(this_grid)
    print(e.weights)

