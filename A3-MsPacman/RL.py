import csv_util
from collections import Counter
from ale_py import ALEInterface
import copy
import math
import random

ale = None
# Q-table of the agent
Q = {}
alpha = None
gamma = None
epsilon = None

def getQTable(Qfile):
    """Get the Qtable from the csv file storage

    Parameters
    --------
        Qfile : str
            name of csv to read Qtable from
    """
    global Q
    Q = csv_util.read_csv(Qfile)

def saveQTable(Qfile):
    """Save the Qtable to a csv file for later use

    Parameters
    --------
        Qfile : str
            name of csv to write Qtable to
    """
    global Q
    csv_util.write_csv(Qfile, Q)

def convertEnv(env):
    """Convert ALE screen from 1D array to 2D array

    Parameters
    --------
        env : ndarray 1xn
            1D array of the ALE screen where n is 210*160
    Returns
    --------
        list(list(int))
            2D array representation of the game screen
    """
    env_2d = []
    for i in range(210):
        env_2d.append(env[i*160:(i+1)*160].tolist())
    return env_2d

# Memory for game
env_model = [
    [6, 1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 1, 1, 6],
    [6, 2, 6, 6, 1, 6, 1, 6, 6, 6, 6, 6, 6, 1, 6, 1, 6, 6, 2, 6],
    [6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6],
    [6, 6, 1, 6, 1, 6, 6, 1, 6, 6, 6, 6, 1, 6, 6, 1, 6, 1, 6, 6],
    [0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0],
    [6, 6, 1, 6, 6, 6, 6, 1, 6, 6, 6, 6, 1, 6, 6, 6, 6, 1, 6, 6],
    [0, 6, 1, 1, 1, 1, 1, 1, 6, 0, 0, 6, 1, 1, 1, 1, 1, 1, 6, 0],
    [6, 6, 1, 6, 6, 6, 6, 1, 6, 6, 6, 6, 1, 6, 6, 6, 6, 1, 6, 6],
    [0, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 0],
    [6, 6, 1, 6, 1, 6, 1, 6, 1, 6, 6, 1, 6, 1, 6, 1, 6, 1, 6, 6],
    [6, 1, 1, 1, 1, 6, 1, 6, 1, 1, 1, 1, 6, 1, 6, 1, 1, 1, 1, 6],
    [6, 1, 6, 6, 1, 6, 1, 1, 1, 6, 6, 1, 1, 1, 6, 1, 6, 6, 1, 6],
    [6, 2, 6, 6, 1, 6, 6, 6, 1, 6, 6, 1, 6, 6, 6, 1, 6, 6, 2, 6],
    [6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6]
]

blinky_pos = [0, 0, 1]      # Red Ghost last position
pinky_pos = [0, 0, 1]       # Pink Ghost last position
clyde_pos = [0, 0, 1]       # Orange Ghost last position
inky_pos =  [0, 0, 1]       # Blue Ghost last position
pacman_pos = [0, 0]         # Pacman last position

def getState(env):
    """Generates the state from the environment
    In the case of Ms Pacman, the game screen

    Parameters
    --------
        env : list(list(int))
            2D array of pixel values of the environment

    Returns
    --------
        list(list(int))
            2D array representing the state of the game
    """
    global env_model
    global blinky_pos
    global pinky_pos
    global clyde_pos
    global inky_pos
    global pacman_pos
    grid = copy.deepcopy(env_model)
    for i in range(14):
        for j in range(20):
            pixels = []
            for k in range(12):
                for l in range(8):
                    pixels.append(env[i*12+k+2][j*8+l])
            histogram = Counter(pixels)
            color_count = 0
            color_key = None
            for key in histogram:
                # if the tile is empty
                if(key == 144):
                    continue
                if(color_count < histogram[key]):
                    color_count = histogram[key]
                    color_key = key
            # Change dominant color to tile state
            if(color_key is None):          # No majority color
                color_key = 0
            elif(color_key == 74):          # If pink-ish is dominant in tile
                if(color_count == 8):       # Corresponds to a dot, 4x2 pixels of value 74
                    color_key = 1
                elif(color_count == 28):    # Corresponds to a capsule, 4x7 pixels of value 74
                    color_key = 2
                else:                       # Corresponds to a wall
                    color_key = 6
            elif(color_key == 42):          # If yellow is dominant in tile
                pacman_pos.append([i,j])
                continue
            # Corresponds to active ghosts
            elif(color_key == 70):
                blinky_pos.append([i, j, 1])
                continue
            elif(color_key == 184):
                clyde_pos.append([i, j, 1])
                continue
            elif(color_key == 38):
                inky_pos.append([i, j, 1])
                continue
            elif(color_key == 88):
                pinky_pos.append([i, j, 1])
                continue
            elif(color_key == 150):
                if(abs(i-blinky_pos[0])+abs(j-blinky_pos[1]) < 2):
                    blinky_pos.append([i, j, 0])
                elif(abs(i-clyde_pos[0])+abs(j-clyde_pos[1]) < 2):
                    clyde_pos.append([i, j, 0])
                elif(abs(i-inky_pos[0])+abs(j-inky_pos[1]) < 2):
                    inky_pos.append([i, j, 0])
                elif(abs(i-pinky_pos[0])+abs(j-pinky_pos[1]) < 2):
                    pinky_pos.append([i, j, 0])                
                continue

            grid[i][j] = color_key
    
    # Update Pacman positions in memory
    for i in range(2, len(pacman_pos)):
        if(pacman_pos[0] != pacman_pos[i][0] or pacman_pos[1] != pacman_pos[i][1]):
            pacman_pos = [pacman_pos[i][0], pacman_pos[i][1]]
            break
    pacman_pos = [pacman_pos[0], pacman_pos[1]]
    # Update the Ghosts positions in memory
    dist = float('Inf')
    idx = None
    for i in range(3, len(blinky_pos)):
        dx = abs(blinky_pos[i][0]-pacman_pos[0])
        dy = abs(blinky_pos[i][1]-pacman_pos[1])
        delta = 0
        if dx != 0 and dy != 0:
            delta = dx+dy-1
        else:
            delta = dx+dy
        if dist > delta:
            dist = delta
            idx = i
    if(idx is not None):
        blinky_pos = [blinky_pos[idx][0], blinky_pos[idx][1], blinky_pos[idx][2]]
    
    dist = float('Inf')
    idx = None
    for i in range(3, len(inky_pos)):
        dx = abs(inky_pos[i][0]-pacman_pos[0])
        dy = abs(inky_pos[i][1]-pacman_pos[1])
        delta = 0
        if dx != 0 and dy != 0:
            delta = dx+dy-1
        else:
            delta = dx+dy
        if dist > delta:
            dist = delta
            idx = i
    if(idx is not None):
        inky_pos = [inky_pos[idx][0], inky_pos[idx][1], inky_pos[idx][2]]
    
    dist = float('Inf')
    idx = None
    for i in range(3, len(pinky_pos)):
        dx = abs(pinky_pos[i][0]-pacman_pos[0])
        dy = abs(pinky_pos[i][1]-pacman_pos[1])
        delta = 0
        if dx != 0 and dy != 0:
            delta = dx+dy-1
        else:
            delta = dx+dy
        if dist > delta:
            dist = delta
            idx = i
    if(idx is not None):
        pinky_pos = [pinky_pos[idx][0], pinky_pos[idx][1], pinky_pos[idx][2]]

    dist = float('Inf')
    idx = None
    for i in range(3, len(clyde_pos)):
        dx = abs(clyde_pos[i][0]-pacman_pos[0])
        dy = abs(clyde_pos[i][1]-pacman_pos[1])
        delta = 0
        if dx != 0 and dy != 0:
            delta = dx+dy-1
        else:
            delta = dx+dy
        if dist > delta:
            dist = delta
            idx = i
    if(idx is not None):
        clyde_pos = [clyde_pos[idx][0], clyde_pos[idx][1], clyde_pos[idx][2]] 

    # Place last known locations of the entities in the state
    grid[pacman_pos[0]][pacman_pos[1]] = 3
    grid[blinky_pos[0]][blinky_pos[1]] = 4 + blinky_pos[2]
    grid[inky_pos[0]][inky_pos[1]] = 4 + inky_pos[2]
    grid[pinky_pos[0]][pinky_pos[1]] = 4 + pinky_pos[2]
    grid[clyde_pos[0]][clyde_pos[1]] = 4 + clyde_pos[2]

    state = ''
    close_food, food_dir, num_food = findFoodFeatures(grid)
    state = f'{close_food},{food_dir}'
    num_scared, N_risk, E_risk, S_risk, W_risk, flee = findGhostFeatures(grid)
    state = f'{state},{num_scared},{N_risk},{E_risk},{S_risk},{W_risk},{flee}'
    state = f'{state},{findWallFeatures(grid)}'

    return state

def findFoodFeatures(grid):
    """Find the features related to food, namely distance to
    the nearest food position from Ms. Pacman and how many remain

    Parameters
    --------
        grid : list(list(int))
            grid representation of the Atari screen
    
    Returns
    --------
        int
            distance to closest food from Ms. Pacman
        str
            Cardinal direction to food
        int
            number of food pieces left 
    """
    global pacman_pos
    
    dist = float('Inf')
    num_food = 0
    food_dir = ''
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == 1:
                num_food += 1
                dx = abs(pacman_pos[0]-i)
                dy = abs(pacman_pos[1]-j)
                delta = 0
                if dx != 0 and dy != 0:
                    delta = dx+dy-1
                else:
                    delta = dx+dy
                if dist > delta:
                    dist = delta
                    food_dir = ''
                    if((pacman_pos[0]-i) < 0):
                        food_dir += 'S'
                    elif((pacman_pos[0]-i) > 0):
                        food_dir += 'N'
                    if((pacman_pos[1]-j) < 0):
                        food_dir += 'E'
                    elif((pacman_pos[1]-j) > 0):
                        food_dir += 'W'

    return dist, food_dir, num_food

def findGhostFeatures(grid):
    """Find the features related to the Ghosts

    Parameters
    --------
        grid : list(list(int))
            grid representation of the Atari screen
    
    Returns
    --------
        int
            Number of scared ghosts on the screen
        int
            Weight of ghosts within 2 steps of Ms. Pacman from the North
        int
            Weight of ghosts within 2 steps of Ms. Pacman from the East
        int
            Weight of ghosts within 2 steps of Ms. Pacman from the South
        int
            Weight of ghosts within 2 steps of Ms. Pacman from the West
        bool
            Boolean for feed Ms. Pacman or flee Ghosts mode
    """
    global prev_reward
    global blinky_pos
    global pinky_pos
    global clyde_pos
    global inky_pos
    global pacman_pos
    num_scared = 0
    for i in range(0, len(grid)):
        try:
            j = grid[i].index(4)            # Corresponds to scared ghosts
            num_scared += 1

        except ValueError:
            continue

    weights = [
        [0, 0, 1, 0, 0],
        [0, 1, 2, 1, 0],
        [1, 2, 10, 2, 1],
        [0, 1, 2, 1, 0],
        [0, 0, 1, 0, 0]
    ]
    N_risk = 0
    E_risk = 0
    S_risk = 0
    W_risk = 0
    for i in range(-2, 3):
        for j in range(-2, 3):
            try:
                if(grid[pacman_pos[0]+i][pacman_pos[1]+j] == 4 or grid[pacman_pos[0]+i][pacman_pos[1]+j] == 5):
                    if i < 0:
                        N_risk = weights[i+2][j+2]
                    elif i > 0:
                        S_risk = weights[i+2][j+2]
                    if j < 0:
                        W_risk = weights[i+2][j+2]
                    elif j > 0:
                        E_risk = weights[i+2][j+2]
                    if(i == 0 and j == 0):
                        N_risk = weights[i+2][j+2]
                        S_risk = weights[i+2][j+2]
                        W_risk = weights[i+2][j+2]
                        E_risk = weights[i+2][j+2]
            except IndexError:
                continue

    flee_mode = False
    if(
        (
            N_risk > 0 or
            E_risk > 0 or
            S_risk > 0 or
            W_risk > 0
        ) and
        num_scared == 0
    ):
        flee_mode = True

    return num_scared, N_risk, E_risk, S_risk, W_risk, flee_mode

def findWallFeatures(grid):
    """Find the directions of the wall next to pacman

    Parameters
    ---------
        grid : list(list(int))
            grid representation of the Atari screen
    
    Returns
    --------
        str
            Cardinal directions of the walls next to pacman
    """
    Wall_dir = ''
    try:
        if(grid[pacman_pos[0]-1][pacman_pos[1]] == 6):
            Wall_dir += 'N'
    except IndexError:
        Wall_dir += 'N'
    try:
        if(grid[pacman_pos[0]+1][pacman_pos[1]] == 6):
            Wall_dir += 'S'
    except IndexError:
        Wall_dir += 'S'
    try:
        if(grid[pacman_pos[0]][pacman_pos[1]-1] == 6):
            Wall_dir += 'W'
    except IndexError:
        Wall_dir += 'W'
    try:
        if(grid[pacman_pos[0]][pacman_pos[1]+1] == 6):
            Wall_dir += 'E'
    except IndexError:
        Wall_dir += 'E'

    return Wall_dir

def stateReward(state):
    """Punish the AI for bad behavior

    Parameters
    --------
        state : str
            current state of the game

    Returns
    --------
        int
            punishment for AI's bad behavior
    """
    features = state.split(',')
    reward = 5/int(features[0])
    reward += int(features[3])*-100
    reward += int(features[4])*-100
    reward += int(features[5])*-100
    reward += int(features[6])*-100
    if(features[7] == 'False'):
        reward += 10
    return reward

# Q-learning constants
prev_state = None
prev_action = None
prev_reward = None

def Q_learn(state, reward):
    """Q learning algorithm using temporal difference

    Parameters
    --------
        state : str
            current state of the game
        reward : int
            received reward
        action : int
            action to perform
    
    Returns
    -------
        int
            number representing the next action to perform
    """
    global prev_action
    global prev_reward
    global prev_state
    global alpha
    global gamma

    if ale.game_over():
        Q.setdefault(prev_state, 0).append(reward)
    if prev_state is not None:
        s_a = f'{prev_state},{prev_action}'
        Q.setdefault(s_a, 0)                    # If state never encountered before, init to zero
        Q[s_a] = Q[s_a] + alpha*(reward + gamma*maxQ(state) - Q[s_a])
    prev_state = state
    prev_action = explore(state)
    prev_reward = reward
    return prev_action

def maxQ(state):
    """Find maximum Q value from Q table when performing actions in state

    Parameters
    --------
        state : str
            current state of the game in string form
    
    Returns
    --------
        int
            max Q value attainable
    """
    global ale
    actions = ale.getMinimalActionSet()
    actions = actions.tolist()
    max_val = -float('Inf')
    for a in actions:
        s_a = f'{state},{a}'
        Q.setdefault(s_a, 0)
        val = Q[s_a]
        if(val > max_val):
            max_val = val
    return max_val

def explore(state):
    """Function to control the exploration of the agent
    using the Epsilon-Greedy Policy
    
    Parameters
    --------
        state : str
            current state of the game in string form
    
    Returns
    --------
        int
            action to be performed by the agent
    """
    global ale
    global epsilon

    actions = ale.getMinimalActionSet()
    actions = actions.tolist()
    max_val = -float('Inf')
    best_a = 0
    # Randomly Select move
    if(random.random() < epsilon):
        return random.randint(0,len(actions)-1)
    # Select best move
    else:
        for a in actions:
            s_a = f'{state},{a}'
            Q.setdefault(s_a, 0)
            val = Q[s_a]
            if(val > max_val):
                max_val = val
                best_a = a
        return best_a
