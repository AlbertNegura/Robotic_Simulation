from config import *
import numpy as np
import fitness
import robotics
import neuralnetwork
import grid
import operator

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
        self.genome = np.random.uniform(0, 1, self.genome_size)

        for i in range(size):
            self.genome[i] = weights[i]


    def evaluate(self, cells_covered, num_collisions, sensor_values):
        self.fitness = fitness.fitness(cells_covered, num_collisions, sensor_values)
        return self.fitness


    def cross_over(self, dad, mom):
        dad_sel = np.random.choice(range(self.genome_size),int(self.genome_size/2), replace = False)
        mom_sel = [i for i in range(self.genome_size) if i not in dad_sel]
        self.genome[dad_sel] = dad.genome[dad_sel]
        self.genome[mom_sel] = mom.genome[mom_sel]
        return self

    def mutate(self):
        pos = np.random.choice(range(self.genome_size), MUTATIONS, replace=False)
        self.genome[pos] = np.random.uniform()
        return self



class Evolution:
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

    def __init__(self, this_grid):
        self.population = POPULATION
        self.iterations = ITERATIONS * TICK_RATE
        self.generations = LIFESPAN
        self.current_generation = 0
        self.nn = [neuralnetwork.RNN(np.random.uniform(0, SENSOR_LENGTH, SENSORS), np.array([0,0]), SENSORS, HIDDEN_NODES, 2) for _ in range(self.population)]
        self.weights = [nn.weight_vector() for nn in self.nn]
        self.map = [this_grid.copy() for _ in range(self.population)]
        self.robots = [robotics.create_robot(init_pos=(WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)), radius=RADIUS, acceleration=ACCELERATION, num_sensors=SENSORS, max_radius=SENSOR_LENGTH) for _ in range(self.population)]
        self.genome_list = [Genome(self.robots[i], self.map[i], self.weights[i]) for i in range(self.population)]
        self.fitnesses = []


    def evolve(self):
        """
        :return: the evolved population after 30 generations
        """
        for gen in range(self.generations):
            # Simulate all individuals with current wights config and get fitness value list [self.fitnesses]
            # ind_fitness is the individual fitness value list and fitnesses is the list of ind_fitness
            self.single_gen_step()
            genome_best, index, value = self.get_current_best()
            print("Current best: ", index+1, ", with fitness value: ", value)

    def single_gen_step(self):
        ind_fitness = []
        for ind in range(self.population):
            total_area, collision_number, sensor_values = self.step(self.genome_list[ind], self.map[ind], self.nn[ind])
            ind_fitness.append(fitness.fitness(total_area, collision_number, sensor_values))
            print("individual:", ind+1, "/", POPULATION, ", generation:", self.current_generation+1, "/", LIFESPAN, ", fitness:", np.round(ind_fitness[ind],2), ", n.collisions: ", collision_number, ", area:", total_area, ", sensors:",sensor_values)
        self.fitnesses.append(ind_fitness)
        self.update(genetic_algorithm(self.fitnesses[self.current_generation], self.genome_list))
        self.current_generation = self.current_generation+1

    def update(self, new_weights):
        for i in range(self.population):
            self.nn[i].update_weights(new_weights[i])
        self.weights = [nn.weight_vector() for nn in self.nn]
        self.genome_list = [Genome(self.robots[i], self.map[i], self.weights[i]) for i in range(self.population)]


    def step(self, genome, map, nn):
        """
        :returns: Given one individual, simulates 6000 iterations and returns fitness_parameters to be used in the fitness function
        """
        robot = genome.robot
        robot.collisions = 0
        clean_cells = 0
        for cycle in range(self.iterations):
            rnn_output = nn.feedforward(robot.sensor_values())
            decode_output(rnn_output, robot)
            robot.move(WALLS)
            robot.adjust_sensors(WALLS)
            robot.adjust_sensors(EDGE_WALLS)
            clean_cells = grid.get_cells_at_position_in_radius(map, robot.position, GRID_SIZE, CLEANING_RANGE, clean_cells)
        map = grid.reset_grid(map)
        total_area = round(clean_cells/len(map)/len(map[0])*100,3)
        collision_number = robot.collisions
        sensor_values = np.sum(robot.sensor_values()) - robot.radius * SENSORS
        return total_area, collision_number, sensor_values

    def get_current_best(self):
        index, value = max(enumerate(self.fitnesses[self.current_generation-1]), key=operator.itemgetter(1))
        return self.nn[index], index, value

def decode_output(rnn_output, robot_sim):
    """
    Mapping of the RNN output to robot's wheel velocities. Same as gui.accelerate()
    """
    robot_sim.velocity_left += ACCELERATION*rnn_output[0]
    robot_sim.velocity_right += ACCELERATION*rnn_output[1]

def decode_output_deprecated(rnn_output, robot_sim):
    """
    DEPRECATED
    Mapping of the RNN output to robot's wheel velocities. Same as gui.accelerate()
    """
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

def genetic_algorithm(fitness_list, genome_list):
    """
    :param fitness_list: fitness_list.size = POPULATION
    :param genome_list: genome_list.size = POPULATION containing self.genome_list[i].genome a list of "weights" of size 12*4 + 4*4 + 4*2 = 72 (see RNN)
    :return:
    """

    num_selected = int(POPULATION/5) if SELECTION == "elitism" or SELECTION == "roulette" else int(POPULATION/5*4) if SELECTION == "steady" else int(POPULATION/2)
    selected_agents = []
    # region SELECTION
    if SELECTION == "elitism" or SELECTION == "steady":
        selected_agents = np.argpartition(fitness_list, num_selected+1)
    elif SELECTION == "tournament":
        random_order = np.random.choice(range(POPULATION),POPULATION, replace=False)
        left_bracket = random_order[:num_selected]
        right_bracket = random_order[num_selected:]
        for i in range(num_selected):
            selected_agent = left_bracket[i] if fitness_list[left_bracket[i]] > fitness_list[right_bracket[i]] else right_bracket[i] if fitness_list[left_bracket[i]] < fitness_list[right_bracket[i]] else np.random.choice([left_bracket[i], right_bracket[i]])
            selected_agents.append(selected_agent)
    elif SELECTION == "roulette":
        total_fitness = np.sum(fitness_list)
        random_order = np.random.choice(range(POPULATION), POPULATION, replace=False)
        roulette_selection = {int(i) : fitness_list[int(i)] for i in random_order}
        chance = np.random.uniform(0, total_fitness)
        i = 0
        current = 0
        for key, value in roulette_selection.items():
            current += value
            if current > chance:
                selected_agents.append(key)
                i+=1
                if i >= num_selected:
                    break
    else: # in case of error, default to elitism
        selected_agents = np.argpartition(fitness_list, num_selected+1)
    # endregion

    # region REPRODUCTION
    for x in range(len(genome_list)):
            if x in selected_agents[:num_selected]:
                new_agent = genome_list[x]
            else:
                # CROSSOVER
                if len(selected_agents) > 0:
                    dad = np.random.choice(selected_agents)
                    mom = np.random.choice(selected_agents)
                    while dad == mom:
                        mom = np.random.choice(selected_agents)
                else: # Roulette selection is special
                    parents = np.random.choice(range(POPULATION), 2, replace=False)
                    dad = parents[0]
                    mom = parents[1]
                new_agent = genome_list[x].cross_over(genome_list[dad],genome_list[mom])

                # MUTATION
                if np.random.rand() < MUTATION_RATE:
                    new_agent = genome_list[x].mutate()

            genome_list[x] = new_agent
    #endregion

    return genome_list


if __name__ == "__main__":
    this_grid = grid.create_grid(GRID_SIZE, WIDTH, HEIGHT)
    WALLS.extend([[[0,0],[-1,-1]], [[650,0],[650,125]],[[650,175],[650,425]], [[650, 475], [650, 600]], [[0,300],[305, 300]],[[345,300],[955,300]], [[995, 300], [1300, 300]]])
    #WALLS.extend([[[280, 124], [282, 281]], [[282, 281], [431, 290]], [[433, 124], [426, 286]], [[522, 295], [525, 453]], [[520, 295], [679, 297]], [[679, 297], [676, 105]], [[97, 361], [75, 535]], [[75, 535], [317, 550]], [[850, 362], [844, 545]], [[844, 545], [733, 549]], [[1112, 79], [1121, 280]], [[1121, 280], [980, 286]], [[1116, 77], [930, 92]], [[973, 522], [963, 366]], [[963, 366], [1107, 344]], [[1107, 344], [1117, 440]], [[774, 249], [768, 104]], [[62, 50], [174, 54]], [[108, 173], [106, 263]]])
    e = Evolution(this_grid)
    e.evolve()






