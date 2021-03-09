# Robotic Simulation Software

#### Software Authors: Albert Negura, Julien Havel, Kamil Inglot, Sergi Nogues Farres

#### README: Albert Negura

#### Documentation: Albert Negura, Kamil Inglot, Sergi Nogues Farres

### Instructions

To install dependencies, run: 

    pip install -r reqs.txt
    
To execute the simulation, run: 

    python main 

For the evolved controller, the robot will utilize the weights in the best_individuals.txt file automatically. In order to train a new best_individuals.txt file, you can edit the config and run:
    
    python plot_evolution.py
    
    

### Config

A config.ini file is used to edit all the constants of the simulation. Currently, the following constants are used (with their corresponding default values):

1. DEFAULT
- WIDTH = 1600 - the width component of the resolution of the window
- HEIGHT = 900 - the height component of the resolution of the window
2. ROBOT
- RADIUS = 20 - the radius of the robot
- TICK_RATE = 60 - the tick rate of the simulation
- LEFT = 0 - the ID of the left wheel - generally leave untouched
- RIGHT = 1 - the ID of the right wheel - generally leave untouched
- BOTH = 2 - the ID of controlling both wheels simultaneously - generally leave untouched
- FORWARD = 1 - the acceleration multiplier for moving forwards
- BACKWARD = -1 - the acceleration multiplier for moving backwards
- STOP = 0 - the acceleration multiplier for stopping
- ACCELERATION = 0.02 - the acceleration, can be modified freely
- SENSORS = 12 - the number of sensors belonging to the robot, spaced equally around the robot
- SENSOR-LENGTH = 150 - the length of the sensors from which they give a response
- GRID_SIZE = 10 - the size of the squares in the grid
3. MODEL
- HIDDEN_NODES = 4 - the number of hidden nodes in the network
- POPULATION = 20 - the population for the evolutionary algorithm
- LIFESPAN = 50 - the number of generations
- ITERATIONS = 30 - the lifespan of an individual in seconds
- SELECTION = tournament - the selection strategy - currently supported are elitism, steady-state, roulette, tournament, custom
- MUTATIONS = 8 - the number of genes modified per mutation event
- MUTATION = 0.1 - the rate at which mutations happen (deprecated)
- MUTATION_RATE = 0.1 - the rate at which mutations happen
- SHOW_EVERY_X_GENERATIONS = 10 - show individual in gui ever x generations (unused)
- SELECTED_WALLS = 2 - walls selected for the evolution (see gui for wall configurations)
4. TERRAIN
- DIRT = 10 - the resolution of the dirt - smaller is more computationally expensive but produces a better robot cleaning path
- DIRT_VALUE = 2000 - the weight of the dirt when cleaned in the fitness function
- COLLISION_VALUE = -2000 - the weight of each collision in the fitness function
- SENSOR_VALUE = -10 - the weight of the sum of sensor values in the fitness function
- SENSOR_EXPONENTIAL = False - whether to utilize an exponential form of the fitness function for the sensor values
5. VISUALIZATION
- WALL_WIDTH = 5 - the width of the drawn walls
- TICK_RATE = 60 - the tick rate of the visualization of the simulation, not related to robot tick rate
- KEY_SIZE = 60 - the size of the keyboard keys - generally leave untouched
6. MULTIPROCESSING
- MULTIPROCESSING = False - whether to use multiprocessing for the evolution
- PROCESSES = 20 - the number of processes - set to population value for best results
7. DEBUG
- SHOW_ALL = True - start the simulation with all debug options on 
- SHOW_VELOCITY_PER_WHEEL = True - show the velocity of both wheels on top of the robot
- SHOW_SENSORS = True - show the sensor lines
- SHOW_SENSOR_INFO = True - show the sensor distance to collision or SENSOR_LENGTH, whichever one comes first
- DRAW_GRID = True - draw a grid to reduce eyestrain of visualization
- DRAW_TRAIL = True - draw the trail the robot took since the beginning of the simulation
- DISAPPEARING_TRAIL = True - draw a gradually disappearing trail of the robot's movement in the past 100 frames, overrides DRAW_TRAIL
- DRAW_GHOSTS = False - show all individuals of a generation in the gui (unused)
- CLEANING_MODE = True - whether the clean cells are drawn or not
- AUTONOMOUS_MODE = False - whether the robot starts in autonomous mode (controlled by the corresponding neural network with the corresponding weights)
- RNN = True - whether the network used is a single-hidden-layer RNN or ANN network
- EVOLVE = False - whether to evolve the robot during the gui simulation (unused)

### Controls

Currently, the following controls are supported:

- W - accelerate left wheel forward
- S - accelerate left wheel backward
- O - accelerate right wheel forward
- L - accelerate right wheel backward
- T - accelerate robot forward
- V - accelerate robot backward
- X - stop the robot's velocity
- V - reset the simulation
- E - edit mode (toggle key) - click, drag and release mouse to draw a straight line (wall) from the position the wall was place to when the mouse was released
- C - cleaning mode (toggle key) - whether the robot cleans
- A - autonomous mode (toggle key) - whether the robot is controlled by the corresponding weight vector
- Q - next generation of weights from the best_individuals.txt file
- Z - previous generation of weights from the best_individuals.txt file
- \[ - previous map from preprogrammed maps
- \] - next map from preprogrammed maps
- N - remove all walls
- M - menu mode - opens the map configuration menu which allows users to save the current wall configuartion or load existing configurations - can press ESC or the Go Back button to go back.
- 1 - Toggle SHOW_VELOCITY_PER_WHEEL constant
- 2 - Toggle SHOW_SENSORS constant
- 3 - Toggle SHOW_SENSOR_INFO constant
- 4 - Toggle DRAW_GRID constant
- 5 - Toggle DRAW_TRAIL constant
- 6 - Toggle DISAPPEARING_TRAIL constant
    
### Disclaimer:

All content in this repository was designed and programmed by the authors. If an author made a significant contribution to a file, their name is listed in the authors at the top of each file, a significant contribution representing at least a contribution of multiple lines of code which affect the overall behaviour of the software in a meaningful manner.

Several available code snippets were reused for the drawing/visualization functions from various sources such as StackOverflow and other GitHub repositories, but they were used in a (hopefully) unique way for this software.
