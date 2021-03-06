from config import *
import numpy as np
import fitness
import robotics
import neuralnetwork
import grid
import operator
from multiprocessing.dummy import Pool
import matplotlib.pyplot as plt

# sensors * hidden nodes because fully connected input + hidden layer
# hidden nodes * 2 because each hidden node is fully connected to output
# IF RNN, hidden -> hidden so hidden nodes * hidden nodes
# output has exactly 2 nodes - Vl and Vr
# if not RNN
# total weights for 12 sensors and 4 hidden nodes = 12*4 + 4*2 = 56
# if RNN
# total weights for 12 sensors and 4 hidden nodes = 12*4 + 4*4 + 4*2 = 56
ALLWALLS = [
           [[[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

           [[[0, 0], [-1, -1]], [[352, 82], [349, 264]], [[349, 263], [494, 258]], [[494, 258], [497, 80]],
               [[497, 80], [352, 80]], [[776, 242], [764, 486]], [[764, 486], [956, 493]], [[956, 493], [947, 242]],
               [[947, 242], [775, 243]],
            [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

            [[[0, 0], [-1, -1]], [[650, 0], [650, 125]], [[650, 175], [650, 425]], [[650, 475], [650, 600]],
               [[0, 300], [305, 300]], [[345, 300], [955, 300]], [[995, 300], [1300, 300]],
             [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

            [[[0, 0], [-1, -1]], [[106, 96], [1201, 95]], [[1178, 362], [1001, 241]], [[1001, 241], [812, 362]],
            [[812, 362], [673, 238]], [[673, 238], [505, 352]], [[505, 352], [331, 218]], [[331, 218], [184, 351]],
            [[85, 509], [1185, 507]],
             [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

            [[[0, 0], [-1, -1]], [[311, 6], [308, 171]], [[309, 246], [307, 384]], [[305, 471], [293, 600]], [[429, 247],
           [531, 166]], [[531, 166], [689, 248]], [[689, 249], [875, 158]], [[883, 163], [1106, 260]], [[1106, 369],
           [977, 479]], [[977, 479], [825, 382]], [[824, 382], [621, 480]], [[621, 480], [440, 389]],
             [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

           [[[5, 5], [5, 595]], [[5, 595], [1600, 595]], [[5, 5], [1600, 5]], [[1295, 5], [1295, 595]], [[5, 5], [0, 0]], [[0, 0], [0, 600]], [[0, 600], [1600, 600]], [[0, 0], [1600, 0]], [[1295, 5], [1295, 595]], [[164, 122], [185, 277]], [[183, 278], [389, 268]], [[389, 268], [373, 128]], [[374, 124], [166, 125]], [[840, 136], [842, 287]], [[842, 287], [1102, 294]], [[1102, 294], [1105, 142]], [[1107, 138], [843, 131]], [[500, 220], [635, 162]], [[635, 162], [743, 261]], [[971, 499], [745, 371]], [[738, 366], [680, 435]], [[680, 435], [573, 351]], [[573, 351], [443, 431]], [[973, 366], [975, 525]], [[975, 525], [1134, 519]], [[1134, 519], [1141, 372]], [[1135, 371], [973, 368]], [[135, 468], [236, 395]], [[236, 395], [280, 480]],
            [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

           [[[5, 5], [5, 595]], [[5, 595], [1600, 595]], [[5, 5], [1600, 5]], [[1295, 5], [1295, 595]], [[5, 5], [0, 0]], [[0, 0], [0, 600]], [[0, 600], [1600, 600]], [[0, 0], [1600, 0]], [[1295, 5], [1295, 595]], [[252, 110], [255, 245]], [[255, 245], [481, 248]], [[481, 248], [487, 119]], [[488, 117], [252, 113]], [[580, 245], [822, 238]], [[928, 113], [960, 248]], [[960, 248], [1088, 241]], [[1088, 241], [1085, 111]], [[1085, 110], [932, 113]], [[1091, 238], [1222, 241]], [[255, 245], [86, 236]], [[468, 596], [478, 334]], [[972, 323], [981, 596]], [[579, 244], [587, 355]], [[587, 355], [833, 358]], [[833, 358], [824, 241]],
            [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]],

            [[[5, 5], [5, 595]], [[5, 595], [1600, 595]], [[5, 5], [1600, 5]], [[1295, 5], [1295, 595]], [[5, 5], [0, 0]], [[0, 0], [0, 600]], [[0, 600], [1600, 600]], [[0, 0], [1600, 0]], [[1295, 5], [1295, 595]], [[78, 92], [472, 83]], [[471, 83], [470, 348]], [[574, 348], [584, 90]], [[584, 88], [869, 101]], [[870, 101], [876, 5]], [[93, 195], [389, 190]], [[389, 190], [378, 595]], [[103, 595], [113, 270]], [[114, 270], [298, 280]], [[298, 280], [288, 380]], [[288, 380], [196, 376]], [[383, 427], [882, 423]], [[743, 422], [744, 169]], [[998, 14], [989, 427]], [[594, 430], [603, 518]], [[603, 514], [786, 510]], [[990, 422], [1143, 423]], [[1294, 347], [1222, 343]], [[1144, 9], [1145, 249]],
             [[0,5],[WIDTH-int(HEIGHT/3),5]],[[0,HEIGHT-int(HEIGHT/3)-5],[WIDTH-int(HEIGHT/3),HEIGHT-int(HEIGHT/3)-5]],[[5,0],[5,HEIGHT-int(HEIGHT/3)]],[[WIDTH-int(HEIGHT/3)-5,0],[WIDTH-int(HEIGHT/3)-5,HEIGHT-int(HEIGHT/3)]]]]


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
        self.nn = [neuralnetwork.RNN(np.random.uniform(0, SENSOR_LENGTH, SENSORS), np.array([0,0]), SENSORS, HIDDEN_NODES, 2) for _ in range(self.population)]
        self.weights = [nn.weight_vector() for nn in self.nn]
        self.map = [this_grid.copy() for _ in range(self.population)]
        self.robots = [robotics.create_robot(init_pos=(200,200), radius=RADIUS, acceleration=ACCELERATION, num_sensors=SENSORS, max_radius=SENSOR_LENGTH) for _ in range(self.population)]
        self.genome_list = [Genome(self.robots[i], self.map[i], self.weights[i]) for i in range(self.population)]
        self.current_generation = 0
        self.printed_generation = 0
        self.fitnesses = []
        self.WALLS1 = [[[0, 0], [-1, -1]], [[352, 82], [349, 264]], [[349, 263], [494, 258]], [[494, 258], [497, 80]],
               [[497, 80], [352, 80]], [[776, 242], [764, 486]], [[764, 486], [956, 493]], [[956, 493], [947, 242]],
               [[947, 242], [775, 243]], [[0, 0], [0, HEIGHT - int(HEIGHT / 3)]],
               [[0, HEIGHT - int(HEIGHT / 3)], [WIDTH, HEIGHT - int(HEIGHT / 3)]], [[0, 0], [WIDTH, 0]],
               [[WIDTH - int(HEIGHT / 3), 0], [WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)]]]
        self.WALLS2 = [[[0, 0], [-1, -1]], [[650, 0], [650, 125]], [[650, 175], [650, 425]], [[650, 475], [650, 600]],
               [[0, 300], [305, 300]], [[345, 300], [955, 300]], [[995, 300], [1300, 300]],
               [[0, 0], [0, HEIGHT - int(HEIGHT / 3)]],
               [[0, HEIGHT - int(HEIGHT / 3)], [WIDTH, HEIGHT - int(HEIGHT / 3)]], [[0, 0], [WIDTH, 0]],
               [[WIDTH - int(HEIGHT / 3), 0], [WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)]]]
        self.WALLS3 = [[[0, 0], [-1, -1]], [[106, 96], [1201, 95]], [[1178, 362], [1001, 241]], [[1001, 241], [812, 362]],
          [[812, 362], [673, 238]], [[673, 238], [505, 352]], [[505, 352], [331, 218]], [[331, 218], [184, 351]],
          [[85, 509], [1185, 507]],[[0, 0], [0, HEIGHT - int(HEIGHT / 3)]],[[0, HEIGHT - int(HEIGHT / 3)],
           [WIDTH, HEIGHT - int(HEIGHT / 3)]], [[0, 0], [WIDTH, 0]],[[WIDTH - int(HEIGHT / 3), 0],
           [WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)]]]
        self.EDGEWALLS = [[[0, 0], [0, HEIGHT - int(HEIGHT / 3)]],[[0, HEIGHT - int(HEIGHT / 3)], [WIDTH, HEIGHT - int(HEIGHT / 3)]],[[0, 0], [WIDTH, 0],[WIDTH - int(HEIGHT / 3), 0]], [[WIDTH - int(HEIGHT / 3), HEIGHT - int(HEIGHT / 3)]]]
        self.walls = self.WALLS1
        self.area_cleaned = []
        self.av_fitness = []
        self.fitness_error = []
        self.diversity = []
        self.diversity_error = []
        self.best_fitness_error = []
        self.best_fitness = []
        self.most_area_cleaned = []
        self.writer = open("best_individuals.txt", "w+")

    def evolve(self):
        """
        :return: the evolved population after 30 generations
        """
        self.WALLS = ALLWALLS[SELECTED_WALLS]
        if MULTIPROCESSING:
            self.fitnesses = np.zeros((self.generations, self.population))
            self.area_cleaned = np.zeros((self.generations, self.population))
        for gen in range(self.generations-1):
            # Simulate all individuals with current wights config and get fitness value list [self.fitnesses]
            # ind_fitness is the individual fitness value list and fitnesses is the list of ind_fitness
            genome_best, index, value, area = self.get_current_best()
            print("Generation: ", self.current_generation, ", Current best: ", index + 1, ", Fitness value: ", np.round(value,3),
                  ", Area Cleaned: ", area, ", Weights:\n", self.weights[index])
            self.writer.write(str(self.weights[index]))
            self.most_area_cleaned.append(area)
            self.best_fitness.append(value)
            self.writer.write(" ")
            self.single_gen_step()

        genome_best, index, value, area = self.get_current_best()
        print("Generation: ", self.current_generation,", Current best: ", index+1, ", Fitness value: ", np.round(value,3), ", Weights:\n", self.weights[index])
        self.most_area_cleaned.append(area)
        self.best_fitness.append(value)
        self.writer.write(str(self.weights[index]))
        self.writer.write(" ")
        print("Generation\tFitness Value\tError\tArea Cleaned\tAverage Fitness\tError\tDiversity\tError\n")
        for i in range(len(self.best_fitness)):
            print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(i, round(self.best_fitness[i],3),round(self.best_fitness_error[i],3),round(self.most_area_cleaned[i],3), round(self.av_fitness[i],3),round(self.fitness_error[i],3),round(self.diversity[i],3),round(self.diversity_error[i],3)))

        plt.figure()
        plt.errorbar(range(len(self.best_fitness)),self.best_fitness,yerr=self.best_fitness_error, color="b", ecolor='k')
        plt.errorbar(range(len(self.av_fitness)),self.av_fitness,yerr=self.fitness_error, color="r", ecolor='gray')
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.legend(["Best Fitness","Average Fitness"])
        plt.show()
        plt.figure()
        ax1 = plt.subplot()
        plt.errorbar(range(len(self.best_fitness)),self.best_fitness,yerr=self.best_fitness_error,color="b", label="Fitness", ecolor='k')
        plt.ylabel("Fitness")
        ax2 = ax1.twinx()
        ax2.errorbar(range(len(self.diversity)),self.diversity,yerr=self.diversity_error,color="r", label="Diversity", ecolor='gray')
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc=0)
        plt.xlabel("Generation")
        plt.ylabel("Diversity")
        plt.show()
        plt.figure()
        ax3 = plt.subplot()
        plt.errorbar(range(len(self.best_fitness)),self.best_fitness,yerr=self.best_fitness_error,color="b", label="Fitness", ecolor='k')
        plt.ylabel("Fitness")
        ax4 = ax3.twinx()
        ax4.plot(range(len(self.area_cleaned)),self.most_area_cleaned, color="r", label="Area cleaned", ecolor='gray')
        lines, labels = ax3.get_legend_handles_labels()
        lines2, labels2 = ax4.get_legend_handles_labels()
        ax4.legend(lines + lines2, labels + labels2, loc=0)
        plt.xlabel("Generation")
        plt.ylabel("Area Cleaned")
        plt.show()

        self.writer.close()

    def evaluate(self):
        if MULTIPROCESSING:
            pool = Pool(PROCESSES)
            self.fitnesses.append(np.zeros(self.population))
            pool.map(self.parallel_evaluation,range(self.population))
            pool.close()
        else:
            ind_fitness = []
            ind_areas = []
            for ind in range(self.population):
                total_area, collision_number, sensor_values = self.step(self.genome_list[ind], self.map[ind], self.nn[ind])
                ind_areas.append(total_area)
                ind_fitness.append(fitness.fitness(total_area, collision_number, sensor_values))
                print("individual:", ind+1, "/", POPULATION, ", generation:", self.printed_generation, "/", LIFESPAN-1, ", fitness:", np.round(ind_fitness[ind],2), ", n.collisions: ", collision_number, ", area:", np.round(total_area,3), ", sensors:",np.round(sensor_values,3))
            self.fitnesses.append(ind_fitness)
            self.av_fitness.append(np.average(ind_fitness))
            self.fitness_error.append(1.96*np.std(ind_fitness)/np.sqrt(self.population))
            diversity = 0
            genome = []
            for i in range(len(self.genome_list)):
                genome.append(self.genome_list[i].genome)
            for i in range(len(self.genome_list)):
                for j in range(len(self.genome_list)):
                    if i != j:
                        diversity += np.linalg.norm(np.array(self.genome_list[i].genome)-np.array(self.genome_list[j].genome))
            self.diversity.append(diversity)
            self.diversity_error.append(1.96*np.std(genome)/np.sqrt(self.population))
            self.area_cleaned.append(ind_areas)
            sorted_fitnesses = np.sort(ind_fitness)
            self.best_fitness_error.append(1.96*np.std(sorted_fitnesses[:int(self.population/4*3)])/np.sqrt(int(self.population/4*3)))
        self.printed_generation+=1
        if(self.printed_generation==self.generations):
            self.printed_generation = 0



    def parallel_evaluation(self, ind):
        total_area, collision_number, sensor_values = self.step(self.genome_list[ind], self.map[ind], self.nn[ind])
        self.area_cleaned[current_generation][ind] = total_area
        self.fitnesses[current_generation][ind] = (fitness.fitness(total_area, collision_number, sensor_values))
        print("individual:", ind+1, "/", POPULATION, ", generation:", self.printed_generation, "/", LIFESPAN-1, ", fitness:", np.round(self.fitnesses[-1][ind],2), ", n.collisions: ", collision_number, ", area:", np.round(total_area,3), ", sensors:",np.round(sensor_values,3))



    def single_gen_step(self):
        self.update(genetic_algorithm(self.fitnesses[self.current_generation], self.genome_list))
        self.evaluate()

    def update(self, new_weights):
        for i in range(self.population):
            self.nn[i].update_weights(new_weights[i])
        self.weights = [nn.weight_vector() for nn in self.nn]
        self.genome_list = [Genome(self.robots[i], self.map[i], self.weights[i]) for i in range(self.population)]
        self.current_generation = self.current_generation+1


    def step(self, genome, map, nn):
        """
        :returns: Given one individual, simulates 6000 iterations and returns fitness_parameters to be used in the fitness function
        """
        robot = genome.robot
        robot.collisions = 0
        clean_cells = 0
        total_sensor_values = 0
        for cycle in range(self.iterations):
            rnn_output = nn.feedforward(robot.sensor_values())
            decode_output(rnn_output, robot)
            robot.move(self.walls)
            robot.adjust_sensors(self.walls)
            clean_cells = grid.get_cells_at_position_in_radius(map, robot.position, GRID_SIZE, CLEANING_RANGE, clean_cells)
            total_sensor_values += np.sum(robot.sensor_values())
        map = grid.reset_grid(map)
        total_area = round(clean_cells/len(map)/len(map[0])*100,3)
        collision_number = robot.collisions
        sensor_values = total_sensor_values/(SENSOR_LENGTH*SENSORS*ITERATIONS)
        return total_area, collision_number, sensor_values

    def get_current_best(self):
        index, value = max(enumerate(self.fitnesses[self.current_generation]), key=operator.itemgetter(1))
        area = self.area_cleaned[self.current_generation][index]
        return self.nn[index], index, value, area

def decode_output(rnn_output, robot_sim):
    """
    Mapping of the RNN output to robot's wheel velocities. Same as gui.accelerate()
    """
    robot_sim.velocity_left = robot_sim.max_vel*rnn_output[0]
    robot_sim.velocity_right = robot_sim.max_vel*rnn_output[1]

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

    num_selected = int(POPULATION/2) if SELECTION == "elitism" or SELECTION == "roulette" else int(POPULATION/5*4) if SELECTION == "steady" else int(POPULATION/2)
    selected_agents = []
    # region SELECTION
    if SELECTION == "elitism" or SELECTION == "steady":
        selected_agents = np.argpartition(fitness_list, num_selected+1)
    elif SELECTION == "tournament":
        random_order = np.random.choice(range(POPULATION),POPULATION, replace=False)
        left_bracket = random_order[:num_selected]
        right_bracket = random_order[num_selected:]
        sorted_order = np.argsort(fitness_list)
        selected_sorted_order = [i for i in sorted_order if fitness_list[i] > np.min(fitness_list)+1]
        if len(selected_sorted_order) == 0:
            selected_sorted_order.append(sorted_order[0])
            selected_sorted_order.append(sorted_order[1])
            selected_sorted_order.append(sorted_order[2])
        for i in range(num_selected):
            if fitness_list[left_bracket[i]] < np.min(fitness_list)+1.0:
                left_bracket[i] = np.random.choice(selected_sorted_order,1, replace = False)
            if fitness_list[right_bracket[i]] < np.min(fitness_list)+1.0:
                left_bracket[i] = np.random.choice(selected_sorted_order,1, replace = False)
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
    elif SELECTION == "custom":
        selected_agents_temp = np.argsort(fitness_list)
        print(fitness_list)
        print(selected_agents_temp)
        best_agent = fitness_list[selected_agents_temp[0]]
        selected_agents = np.zeros(num_selected+1)
        j = 0
        for i in range(len(selected_agents)):
            if j > num_selected+1:
                break
            if fitness_list[i] > best_agent/2:
                selected_agents[j] = selected_agents_temp[i]
            else:
                selected_agents[j] = selected_agents_temp[0]
            j+=1
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
                    parents = np.random.choice(selected_agents,2,replace=False)
                    dad = parents[0]
                    mom = parents[1]
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
    #WALLS.extend([[[280, 124], [282, 281]], [[282, 281], [431, 290]], [[433, 124], [426, 286]], [[522, 295], [525, 453]], [[520, 295], [679, 297]], [[679, 297], [676, 105]], [[97, 361], [75, 535]], [[75, 535], [317, 550]], [[850, 362], [844, 545]], [[844, 545], [733, 549]], [[1112, 79], [1121, 280]], [[1121, 280], [980, 286]], [[1116, 77], [930, 92]], [[973, 522], [963, 366]], [[963, 366], [1107, 344]], [[1107, 344], [1117, 440]], [[774, 249], [768, 104]], [[62, 50], [174, 54]], [[108, 173], [106, 263]]])
    e = Evolution(this_grid)
    e.evolve()






