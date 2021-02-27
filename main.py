"""Robotic Simulation Software
Authors:
Julien Havel
Kamil Inglot
Albert Negura
Sergi Nogues Farres
"""
from gui import *
import  fitness

if __name__ == "__main__":
    pygame.init()


    execute()

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

def pipeline():
    """
     Note that the "robot" parameter defined in config.py is
     the base class used to initialize the "robot_sim" and
     therefore remains unchanged.
    """
    for i in range(math.floor(ITERATIONS)):
        fitness_list = []
        for individual in individuals_list:
            robot_sim = robot
            total_area, collision_number, sensor_values = simulation(robot_sim, individual)
            fitness_list.append(fitness.fitness(total_area, collision_number, sensor_values))

        # Do EA with fitness_list and update individuals_list


def simulation(robot_sim, individual):
    """
    :returns: fitness_parameters to be used in the fitness function
    """
    total_area = []
    collision_number = 0
    sensor_values = []
    for cycle in range(80):  # 80 cycles
        # move robot
        rnn_output = individual.feedforward(robot_sim.sensor_values())
        decode_output(rnn_output, robot_sim)
        robot.move(WALLS)
        robot.adjust_sensors(WALLS)
        robot.adjust_sensors(EDGE_WALLS)
        # calculate total_area, collision_number, sensor_values

    return total_area, collision_number, sensor_values

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
