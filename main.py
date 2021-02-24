"""Robotic Simulation Software
Authors:
Julien Havel
Kamil Inglot
Albert Negura
Sergi Nogues Farres
"""
from gui import *

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
