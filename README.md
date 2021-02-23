# Robotic Simulation Software

#### Software Authors: Albert Negura, Julien Havel, Kamil Inglot, Sergi Nogues Farres

#### README: Albert Negura

#### Documentation: Albert Negura, Kamil Inglot, Sergi Nogues Farres

#### Instructions

To install dependencies, run: 

    pip install -r reqs.txt
    
To execute the simulation, run: 

    python main 
    

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
- SENSOR-LENGTH = 100 - the length of the sensors from which they give a response
- GRID_SIZE = 10 - the size of the squares in the grid
3. VISUALIZATION
- WALL_WIDTH = 5 - the width of the drawn walls
- TICK_RATE = 60 - the tick rate of the visualization of the simulation, not related to robot tick rate
- KEY_SIZE = 60 - the size of the keyboard keys - generally leave untouched
4. DEBUG
- SHOW_ALL = True - start the simulation with all debug options on
- SHOW_VELOCITY_PER_WHEEL = True - show the velocity of both wheels on top of the robot
- SHOW_SENSORS = True - show the sensor lines
- SHOW_SENSOR_INFO = True - show the sensor distance to collision or SENSOR_LENGTH, whichever one comes first
- DRAW_GRID = True - draw a grid to reduce eyestrain of visualization
- DRAW_TRAIL = True - draw the trail the robot took since the beginning of the simulation
- DISAPPEARING_TRAIL = True - draw a gradually disappearing trail of the robot's movement in the past 100 frames, overrides DRAW_TRAIL

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
